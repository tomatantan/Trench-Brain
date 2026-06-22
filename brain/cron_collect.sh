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
# tweet収集が失敗しても launch pipeline(track/synth) は止めない(独立)。
python3 brain/pipeline.py --collect --twitterapi >> "$LOG" 2>&1 || echo "collect failed(継続)" >> "$LOG"

# auto-synthesis: (1)決定的層=全mint観測→篩→watch→synth_queue(LLM不使用)
python3 brain/track.py run >> "$LOG" 2>&1 || echo "track skipped" >> "$LOG"
# (2)合成層=synth_queue を headless claude が wiki に合成(空なら呼ばない=コスト0)
bash brain/synthesize.sh || echo "synth skipped" >> "$LOG"
# (3)UI連携=entities+track状態 → wiki/ui-data.json(UIチームが消費)
python3 brain/export_ui.py >> "$LOG" 2>&1 || echo "export_ui skipped" >> "$LOG"

git add sources/x wiki/dashboards wiki/entities wiki/concepts wiki/_worklist.md wiki/log.md wiki/ui-data.json >> "$LOG" 2>&1 || true
if git diff --cached --quiet; then
  echo "no new data" >> "$LOG"
else
  git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "$LOG" 2>&1
  git push -q origin main >> "$LOG" 2>&1 && echo "pushed main" >> "$LOG"
fi
echo "=== done ===" >> "$LOG"
