#!/usr/bin/env python3
"""
Trench-Brain pipeline — 決定的パートを1本に繋ぐ。

  [--collect]  collector/collect.py（任意。新ツイ収集）
  digest.py        仕分け集計 → wiki/dashboards/signal.md
  build_entities.py  entity背骨を冪等更新（synthesis保持）
  ingest_worklist.py  新ソース差分から wiki/_worklist.md を生成

この後、エージェントが brain/INGEST.md に従って worklist を処理し、
brain/mark_ingested.py で消し込む。

使い方:
  python3 brain/pipeline.py              # digest→entities→worklist
  python3 brain/pipeline.py --collect    # 収集も含める(--source twitterapi等は環境で)
"""
import subprocess
import sys
from pathlib import Path

BRAIN = Path(__file__).resolve().parent
ROOT = BRAIN.parent


def run(args):
    print(f"\n$ {' '.join(args)}")
    r = subprocess.run([sys.executable, *args], cwd=ROOT)
    if r.returncode != 0:
        print(f"  ! failed: {args}", file=sys.stderr)
    return r.returncode


def main():
    if "--collect" in sys.argv:
        src = "twitterapi" if "--twitterapi" in sys.argv else "syndication"
        run(["collector/collect.py", "--source", src])
    run(["brain/digest.py"])
    run(["brain/build_entities.py"])
    run(["brain/ingest_worklist.py"])
    print("\n決定的パート完了。次: エージェントが brain/INGEST.md で wiki/_worklist.md を処理→"
          "brain/mark_ingested.py→commit。")


if __name__ == "__main__":
    main()
