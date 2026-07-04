#!/usr/bin/env python3
"""
wiki_autofix.py — dangling wikilink を決定的3分岐で処理する。

(a) auto-repair: case/表記ゆれ → 一意解決できる場合のみ機械自動修復
(b) concept-gap: kebab-case slug で実体なし → wiki_gaps.json に積む(合成キュー)
(c) leave: ticker/handle/曖昧/ノイズ → 放置(良性前方参照)

default=dry-run。--apply を付けた時のみファイル書換。
憲法境界=「機械的で曖昧ゼロ=自動 / 判断=キュー経由でLLM / それ以外=放置」。
"""
import argparse
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
GAPS = ROOT / "brain" / "state" / "wiki_gaps.json"
LOG = ROOT / "wiki" / "log.md"
MAX_REPAIRS = 50

# ソース参照パターン(除外): UserName__tweet_id 形式
SOURCE_PAT = re.compile(r"^[A-Za-z0-9_]+__\d{6,}$")
# wikilink target 抽出: [[target]] または [[target|alias]]
LINK_PAT = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
# concept-gap 判定: kebab-case slug (英小文字/数字 + ハイフン、ハイフン必須)
KEBAB_PAT = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")


# ---------------------------------------------------------------------------
# ステップ1: 既存stem集合 と lower→stems マップを構築
# ---------------------------------------------------------------------------

def build_stem_maps():
    """既存stemの集合と lower→{stems} マップを返す。
    同一 lower に複数の stem が存在する場合は「曖昧」として (a) 対象外にする。
    """
    existing = {p.stem for p in WIKI.rglob("*.md")}
    lower_map: dict[str, set[str]] = defaultdict(set)
    for stem in existing:
        lower_map[stem.lower()].add(stem)
        # 表記ゆれ耐性(2026-07-04): space↔hyphen を正規化した鍵も張る。
        # 「[[my concept]]」↔「my-concept.md」の類を一意なら auto-repair できる(dangling蓄積対策)。
        norm = stem.lower().replace(" ", "-")
        if norm != stem.lower():
            lower_map[norm].add(stem)
    return existing, lower_map


# ---------------------------------------------------------------------------
# ステップ2: dangling wikilink を収集
# ---------------------------------------------------------------------------

def find_dangling(existing: set[str]) -> list[tuple[Path, str]]:
    """wiki/ 配下の全 .md を走査し、解決できない wikilink を (file, target) で返す。
    - ソース参照パターン (UserName__id) は除外
    - existing stems に完全一致するものは解決済み=除外
    """
    occurrences: list[tuple[Path, str]] = []
    for md_file in WIKI.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for target in LINK_PAT.findall(text):
            if SOURCE_PAT.match(target):
                continue
            if target in existing:
                continue
            occurrences.append((md_file, target))
    return occurrences


# ---------------------------------------------------------------------------
# ステップ3: 3分岐分類
# ---------------------------------------------------------------------------

def classify(
    occurrences: list[tuple[Path, str]],
    existing: set[str],
    lower_map: dict[str, set[str]],
) -> tuple[dict, dict, set, dict]:
    """dangling を (a)/(b)/(c) に分類。

    Returns:
        repairs      : {target: correct_stem}  — (a) 一意に解決できる表記ゆれ
        gaps         : {target: {filenames}}   — (b) concept-gap
        leave_targets: {target}                — (c) 放置対象ターゲット集合
        repair_files : {target: [file_paths]}  — (a) 各ターゲットのファイル一覧
    """
    repairs: dict[str, str] = {}
    repair_files: dict[str, list[Path]] = defaultdict(list)
    gaps: dict[str, set[str]] = defaultdict(set)
    leave_targets: set[str] = set()

    for file_path, target in occurrences:
        tl = target.lower()

        # $ticker / @handle は auto-repair の対象外。
        # これらの case/表記ゆれを機械小文字化すると「正しい表示大文字」を破壊し、
        # macOS の大小文字衝突churn とも絡む。リンク書換えでなくリゾルバ側の別問題として扱う。
        # → (a)/(b) を素通りして (c)放置(leave) に落とす。
        if target.startswith(("$", "@")):
            leave_targets.add(target)
            continue

        # (a) auto-repair: lower(または space→hyphen正規化) が一意に1つの既存 stem に解決でき、かつ target != stem
        key = tl if tl in lower_map else tl.replace(" ", "-")
        if key in lower_map and len(lower_map[key]) == 1:
            correct_stem = next(iter(lower_map[key]))
            if target != correct_stem:
                repairs[target] = correct_stem
                repair_files[target].append(file_path)
                continue

        # (b) concept-gap: $/@始まりでなく kebab-case で実体なし
        if (
            not target.startswith("$")
            and not target.startswith("@")
            and KEBAB_PAT.match(target)
            and target not in existing
        ):
            gaps[target].add(file_path.name)
            continue

        # (c) 放置: ticker/handle/曖昧/ノイズ/その他
        leave_targets.add(target)

    return repairs, gaps, leave_targets, repair_files


# ---------------------------------------------------------------------------
# アクション (a): atomic ファイル書換
# ---------------------------------------------------------------------------

def apply_repairs(
    repairs: dict[str, str],
    repair_files: dict[str, list[Path]],
    max_repairs: int,
) -> int:
    """修復を適用。atomic(temp→os.replace)。MAX_REPAIRS(unique target 数)で打ち切り。
    Returns: 実際に直したリンク総数。
    """
    total_links_fixed = 0
    targets_applied = 0

    for target, correct_stem in repairs.items():
        if targets_applied >= max_repairs:
            break
        targets_applied += 1

        # [[target]] → [[correct_stem]]  /  [[target|alias]] → [[correct_stem|alias]]
        pat = re.compile(r"\[\[" + re.escape(target) + r"(\|[^\]]+)?\]\]")

        for file_path in repair_files[target]:
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
                new_text, n_subs = pat.subn(
                    lambda m: f"[[{correct_stem}{m.group(1) or ''}]]",
                    text,
                )
                if n_subs == 0 or new_text == text:
                    continue
                # atomic 書込: temp ファイルに書いて os.replace
                dir_ = file_path.parent
                fd, tmp_path = tempfile.mkstemp(dir=dir_, suffix=".tmp")
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(new_text)
                    os.replace(tmp_path, file_path)
                    total_links_fixed += n_subs
                except Exception:
                    try:
                        os.unlink(tmp_path)
                    except OSError:
                        pass
                    raise
            except Exception as e:
                print(f"WARN: repair failed for {file_path}: {e}", file=sys.stderr)

    return total_links_fixed


# ---------------------------------------------------------------------------
# アクション (b): wiki_gaps.json に dedup 追記
# ---------------------------------------------------------------------------

def update_gaps(gaps: dict[str, set[str]]) -> int:
    """GAPS json を dedup追記。既存 concept は referenced_by を union する。
    Returns: GAPS に記録されている concept の総数。
    dry-run でも呼んでよい（非破壊な gap 記録として許可）。
    """
    existing_gaps: dict[str, dict] = {}
    if GAPS.exists():
        try:
            data = json.loads(GAPS.read_text(encoding="utf-8"))
            for item in data:
                existing_gaps[item["concept"]] = item
        except Exception:
            pass

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for target, filenames in gaps.items():
        if target in existing_gaps:
            existing_refs = set(existing_gaps[target].get("referenced_by", []))
            existing_gaps[target]["referenced_by"] = sorted(existing_refs | filenames)
        else:
            existing_gaps[target] = {
                "concept": target,
                "referenced_by": sorted(filenames),
                "first_seen": now_str,
            }

    GAPS.parent.mkdir(parents=True, exist_ok=True)
    out = sorted(existing_gaps.values(), key=lambda x: x["concept"])
    GAPS.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(existing_gaps)


# ---------------------------------------------------------------------------
# アクション: wiki/log.md に1行追記
# ---------------------------------------------------------------------------

def append_log(n_links: int, n_gaps: int) -> None:
    """`--apply` 時のみ呼ぶ。log.md のヘッダ直後に1行挿入。"""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"- {today} autofix: {n_links}件link修復 / gap {n_gaps}件記録\n"
    try:
        if LOG.exists():
            text = LOG.read_text(encoding="utf-8")
            lines = text.splitlines(keepends=True)
            # ヘッダ行(#で始まる)の直後の空行をスキップして挿入
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("#"):
                    insert_idx = i + 1
                    while insert_idx < len(lines) and lines[insert_idx].strip() == "":
                        insert_idx += 1
                    break
            lines.insert(insert_idx, entry)
            LOG.write_text("".join(lines), encoding="utf-8")
        else:
            LOG.write_text(f"# Log\n\n{entry}", encoding="utf-8")
    except Exception as e:
        print(f"WARN: log append failed: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI エントリポイント
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wiki dangling wikilink を決定的3分岐で処理。"
        " default=dry-run（ファイルを書き換えない）。"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="指定時のみ実際にファイルを書換。未指定=dry-run。",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=MAX_REPAIRS,
        help=f"1run あたりの修復ターゲット上限 (default={MAX_REPAIRS})。",
    )
    args = parser.parse_args()

    # ステップ1: stem マップ構築
    existing, lower_map = build_stem_maps()

    # ステップ2: dangling 収集
    occurrences = find_dangling(existing)

    # ステップ3: 分類
    repairs, gaps, leave_targets, repair_files = classify(occurrences, existing, lower_map)

    n_repair = len(repairs)
    n_gap = len(gaps)
    n_leave = len(leave_targets)

    if args.apply:
        # (a) 修復実行
        n_links_fixed = apply_repairs(repairs, repair_files, args.max)
        # (b) gap 記録 (apply 時も常に記録)
        total_gap_count = update_gaps(gaps) if gaps else (
            len(json.loads(GAPS.read_text(encoding="utf-8"))) if GAPS.exists() else 0
        )
        # log 追記(実際に修復が起きた時のみ。0修復はノイズ追記しない)
        if n_links_fixed > 0:
            append_log(n_links_fixed, n_gap)
        print(
            f"autofix: repairable={n_repair} gap-concept={n_gap} leave={n_leave}"
            f" (applied {n_links_fixed})"
        )
    else:
        # dry-run: gap 記録のみ(非破壊)
        if gaps:
            update_gaps(gaps)

        # repair 候補を表示(最大10件)
        if repairs:
            print("[dry-run] repair candidates (先頭10件):")
            for i, (target, stem) in enumerate(repairs.items()):
                if i >= 10:
                    print(f"  ... and {len(repairs) - 10} more")
                    break
                files = [f.name for f in repair_files[target]][:3]
                print(f"  [[{target}]] → [[{stem}]] in {files}")

        print(
            f"autofix: repairable={n_repair} gap-concept={n_gap} leave={n_leave}"
            f" (dry-run)"
        )


if __name__ == "__main__":
    main()
