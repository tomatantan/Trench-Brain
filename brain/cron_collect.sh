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

# 単一枝 main に一本化(2026-06-22 unify)。collect=門付き(watchlist)＝憲法 指針2準拠。
git pull -q --rebase origin main >> "$LOG" 2>&1 || echo "pull skipped" >> "$LOG"
python3 brain/pipeline.py --collect --twitterapi >> "$LOG" 2>&1

# auto-synthesis 決定的層: 全mint観測→篩→watch→synth_queue(LLM不使用・状態はlocal)。
# 合成(LLM)はエージェント工程(brain/INGEST.md synth_queue)で別途。
python3 brain/track.py run >> "$LOG" 2>&1 || echo "track skipped" >> "$LOG"

git add sources/x wiki/dashboards wiki/entities wiki/_worklist.md >> "$LOG" 2>&1 || true
if git diff --cached --quiet; then
  echo "no new data" >> "$LOG"
else
  git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "$LOG" 2>&1
  git push -q origin main >> "$LOG" 2>&1 && echo "pushed main" >> "$LOG"
fi
echo "=== done ===" >> "$LOG"
