#!/usr/bin/env python3
"""
synth_validate.py — 合成出力の機械検証ゲート

synthesize.sh が wiki ページを書き換えた後に呼ぶ。
合成が触った wiki/**/*.md が構造的に健全かを決定的に検査する。

終了コード:
  0 = 全ページ健全 (or 変更0件 or git取得失敗=fail-safe)
  1 = 1件以上不健全 → synthesize.sh は commit せずリトライ

北極星: モデル可搬(Sonnet/ローカルでも)・絶対に失敗しない
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 検査対象は「合成LLMが書く層」だけ。reports/dashboards/index/log/_worklist/
# watchlist/canon/feeds/ui-data 等は合成出力でない(check_conformance 等が生成・
# frontmatter無しが正常)ので検査すると誤FAIL→cronが合成を壊れたと誤認する。
SYNTH_OUTPUT_PREFIXES = (
    "wiki/entities/",
    "wiki/concepts/",
    "wiki/summaries/",
    "wiki/queries/",
)


def _git(args: list[str]) -> list[str]:
    """git コマンドを ROOT で実行し、出力行リストを返す。失敗時は RuntimeError。"""
    result = subprocess.run(
        ["git", "-C", str(ROOT)] + args,
        capture_output=True,
        text=True,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"git {' '.join(args)} failed (rc={result.returncode}): {result.stderr.strip()}"
        )
    return [line for line in result.stdout.splitlines() if line.strip()]


def get_changed_wiki_pages(base: str) -> set[Path]:
    """
    合成が触った wiki/**/*.md のフルパス集合を返す。

    1. git diff --name-only <base> -- wiki  (committed or staged)
    2. git status --porcelain               (unstaged/untracked の wiki/*.md)
    の union。
    """
    paths: set[Path] = set()

    def _is_synth_output(rel: str) -> bool:
        return rel.endswith(".md") and rel.startswith(SYNTH_OUTPUT_PREFIXES)

    # 1. diff vs base
    diff_lines = _git(["diff", "--name-only", base, "--", "wiki"])
    for rel in diff_lines:
        if _is_synth_output(rel):
            paths.add(ROOT / rel)

    # 2. unstaged / untracked (git status --porcelain)
    status_lines = _git(["status", "--porcelain"])
    for line in status_lines:
        # 形式: "XY path" または "XY orig -> path"
        # 最後のトークンがファイルパス
        parts = line.strip().split()
        rel = parts[-1].strip('"')
        if _is_synth_output(rel):
            paths.add(ROOT / rel)

    return paths


# -------------------------------------------------------------------------
# ページ検査
# -------------------------------------------------------------------------

FAILURE_MARKERS_CI = [
    "api error",
    "rate limit",
    "as an ai",
    "i cannot",
    "i'm sorry",
    "i am sorry",
]
CODE_FENCE = "```"


def check_page(path: Path) -> list[str]:
    """
    1ページを検査して fail 理由リストを返す。空リスト = 健全。
    ページ検査自体の例外は fail 扱いにする。
    """
    failures: list[str] = []

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [f"読み取り失敗: {e}"]

    # 4. 空ファイル
    if not content.strip():
        return ["空ファイル(0バイト相当)"]

    # 1. frontmatter 健全性
    #    「---」の substring match (split) ではなく行頭の standalone "---" を探す。
    #    これで本文中に "---" を含む日本語コメントや水平線による誤検知を防ぐ。
    if not content.startswith("---"):
        failures.append("frontmatter: 先頭が --- で始まらない")
    else:
        lines = content.split("\n")
        # lines[0] == "---"。lines[1:] の中で "---" だけの行を閉じデリミタとみなす。
        close_idx: int | None = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                close_idx = i
                break
        if close_idx is None:
            failures.append("frontmatter: 閉じ --- が見つからない(truncated)")
        else:
            fm_body = "\n".join(lines[1:close_idx])
            if "type:" not in fm_body:
                failures.append("frontmatter: 必須キー 'type' が無い")
            # 識別子は title OR ticker(auto-track token entityは title でなく ticker が確立規約・
            # pump合成 synth_prompt 生成。build_entities は title)。どちらか有れば正常(2026-07-02 fix)。
            if "title:" not in fm_body and "ticker:" not in fm_body:
                failures.append("frontmatter: 識別子キー(title/ticker)が無い")

    # 2. synthesis ブロック均衡
    start_count = content.count("<!-- synthesis:start -->")
    end_count = content.count("<!-- synthesis:end -->")
    if start_count != end_count:
        failures.append(
            f"synthesisブロック不均衡: start={start_count} end={end_count}"
        )

    # 3. 失敗/切れマーカー
    content_lower = content.lower()
    for marker in FAILURE_MARKERS_CI:
        if marker in content_lower:
            failures.append(f"失敗マーカー検出: '{marker}'")
            break  # 1つ見つかれば十分

    # 未閉じコードフェンス(``` の総数が奇数)
    fence_count = content.count(CODE_FENCE)
    if fence_count % 2 != 0:
        failures.append(f"未閉じコードフェンス(``` の総数={fence_count} が奇数)")

    return failures


# -------------------------------------------------------------------------
# main
# -------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="合成が触った wiki ページの構造健全性を機械検証する門番"
    )
    parser.add_argument(
        "--base",
        default="HEAD",
        help="合成前の git ref (default: HEAD)",
    )
    args = parser.parse_args()

    # 変更ページ集合を取得
    try:
        pages = get_changed_wiki_pages(args.base)
    except Exception as e:
        print(f"synth_validate: WARN git取得失敗({e}) → fail-safe=合成を通す", file=sys.stderr)
        return 0

    if not pages:
        print("synth_validate: no wiki changes")
        return 0

    # 各ページを検査
    all_ok = True
    results: list[tuple[Path, list[str]]] = []
    for page in sorted(pages):
        try:
            page_failures = check_page(page)
        except Exception as e:
            page_failures = [f"検査中例外: {e}"]
        results.append((page, page_failures))
        if page_failures:
            all_ok = False

    if all_ok:
        print(f"synth_validate: OK ({len(pages)} pages checked)")
        return 0
    else:
        for page, page_failures in results:
            if page_failures:
                rel = page.relative_to(ROOT)
                for reason in page_failures:
                    print(f"  {rel}: {reason}", file=sys.stderr)
        print("synth_validate: FAIL", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
