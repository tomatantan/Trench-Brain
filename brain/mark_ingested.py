#!/usr/bin/env python3
"""
合成済みの tweet_id を brain/state/ingested.txt に記録する＝次サイクルの worklist から外す。

★重要（CLAUDE.md 憲法 指針3・INGEST.md の「複利」方針）:
  **全件マークはしない**。実際に合成した分だけを明示的にマークする。
  以前は sources/x の全ツイを無条件にマークしていた＝部分合成を「全完了」と詐称し、
  未合成の backlog が worklist から消えていた（嘘の進捗）。これを禁止した。

使い方:
  # 合成で触れた wiki ページ内の [[source]] link から tweet_id を拾ってマーク（推奨）
  python3 brain/mark_ingested.py --from-files wiki/concepts/foo.md "wiki/entities/tokens/$ETH.md" ...
  # tweet_id / source stem を直接指定
  python3 brain/mark_ingested.py --ids CryptoHayes__1904414571642962176 1947195413062111402 ...
  # 引数なし: 現状の登録件数だけ表示し、何もマークしない（footgun防止）
  python3 brain/mark_ingested.py
"""
import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state" / "ingested.txt"

# [[account__1234567890123]] 形式の source link
LINK_RE = re.compile(r"\[\[([A-Za-z0-9_]+__\d{8,25})\]\]")
# 直接指定された tweet_id / stem から末尾の数字idを拾う
ID_RE = re.compile(r"(?:[A-Za-z0-9_]+__)?(\d{8,25})")


def load():
    return set(STATE.read_text(encoding="utf-8").split()) if STATE.exists() else set()


def save(ids):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text("\n".join(sorted(ids)) + "\n", encoding="utf-8")


def ids_from_files(paths):
    out = set()
    for p in paths:
        fp = Path(p)
        if not fp.exists():
            print(f"  skip (not found): {p}", file=sys.stderr)
            continue
        for stem in LINK_RE.findall(fp.read_text(encoding="utf-8")):
            # ID_RE で末尾の数値tweet_idを抽出（split("__")[-1] は
            # account が末尾に `_` を含む/`___` 区切りだと `_<id>` を返し、
            # ingest_worklist の裸の数値idと永久に一致せず backlog を汚染する。2026-07-02 fix）
            m = ID_RE.search(stem)
            if m:
                out.add(m.group(1))
    return out


def normalize(tokens):
    out = set()
    for t in tokens:
        m = ID_RE.search(t)
        if m:
            out.add(m.group(1))
    return out


def main():
    ap = argparse.ArgumentParser(
        description="合成済み tweet_id だけを ingested 登録する（全件マークはしない）"
    )
    ap.add_argument("--from-files", nargs="*", default=[],
                    help="合成で触れた wiki ページ。中の [[source]] link から id を抽出")
    ap.add_argument("--ids", nargs="*", default=[],
                    help="tweet_id か account__id を直接指定")
    a = ap.parse_args()

    have = load()
    if not a.from_files and not a.ids:
        print(f"ingested 登録済み: {len(have)} 件。マーク対象が未指定なので何もしない。")
        print("使い方: --from-files <合成した wiki .md ...>  または  --ids <tweet_id ...>")
        return

    new = ids_from_files(a.from_files) | normalize(a.ids)
    added = new - have
    have |= new
    save(have)
    print(f"marked ingested: +{len(added)} (指定 {len(new)} / total {len(have)})")


if __name__ == "__main__":
    main()
