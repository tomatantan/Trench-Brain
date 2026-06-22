#!/bin/bash
# Trench-Brain ローカル自動収集（launchd/cronから叩く）。
# 収集(twitterapi)→digest→build_entities→worklist→commit/push。
# ※「貯める＋仕分ける＋整理(背骨)」までの決定的パートだけ。
#   合成(判断)はエージェント工程(brain/INGEST.md)なのでここには含めない。
set -euo pipefail
cd /Users/toma/trench-brain

export PATH="/usr/bin:/bin:/usr/local/bin:$PATH"
LOG="brain/state/cron.log"
mkdir -p brain/state
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) collect start ===" >> "$LOG"

git pull -q --rebase origin Wiki >> "$LOG" 2>&1 || echo "pull skipped" >> "$LOG"
python3 brain/pipeline.py --collect --twitterapi >> "$LOG" 2>&1

git add sources/x wiki/dashboards wiki/entities wiki/_worklist.md >> "$LOG" 2>&1 || true
if git diff --cached --quiet; then
  echo "no new data" >> "$LOG"
else
  git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "$LOG" 2>&1
  git push -q origin Wiki >> "$LOG" 2>&1 && echo "pushed" >> "$LOG"
fi
echo "=== done ===" >> "$LOG"
