#!/bin/bash
# Trench-Brain ローカル自動収集＋合成（launchd/cronから叩く）＝両輪を1サイクルで回す。
# 収集(twitterapi)→worklist(鮮度ゲート)→[pump.fun合成 + X合成(headless)]→UI→commit/push。
# 指針3「収集と合成は両輪」: 収集だけでなく合成(判断)まで毎サイクル回す。
#   - pump.fun側: track.py(観測→篩→queue) → synthesize.sh(headless合成)
#   - X側:        pipeline.py が worklist(§1a=鮮度ゲート) → synthesize_x.sh(headless合成 上位3件/複利)
#   どちらも headless claude は --strict-mcp-config(telegram干渉なし) / SYNTH_*_ENABLED で停止可。
set -euo pipefail
cd /Users/toma/trench-brain

export PATH="/usr/bin:/bin:/usr/local/bin:$PATH"
LOG="brain/state/cron.log"
mkdir -p brain/state
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) collect start ===" >> "$LOG"

# 単一枝 main に一本化(2026-06-22 unify)。collect=門付き(watchlist)＝憲法 指針2準拠。
# --autostash: .obsidian 等の未staged変更があっても rebase を通す(無いと pull skip→cloud GHA
# の push と分岐した時に末尾 push が non-fast-forward で失敗する。2026-06-23 cloud冗長化で必須化)。
git pull -q --rebase --autostash origin main >> "$LOG" 2>&1 || echo "pull skipped" >> "$LOG"
# tweet収集が失敗しても launch pipeline(track/synth) は止めない(独立)。
python3 brain/pipeline.py --collect --twitterapi >> "$LOG" 2>&1 || echo "collect failed(継続)" >> "$LOG"

# auto-synthesis: (1)決定的層=全mint観測→篩→watch→synth_queue(LLM不使用)
python3 brain/track.py run >> "$LOG" 2>&1 || echo "track skipped" >> "$LOG"
# (2)pump.fun合成層=synth_queue を headless claude が wiki に合成(空なら呼ばない=コスト0)
bash brain/synthesize.sh || echo "synth skipped" >> "$LOG"
# (2b)X側合成層=worklist §1a(鮮度ゲート通過)上位3件を headless claude が合成(§1a空なら呼ばない=コスト0)
bash brain/synthesize_x.sh || echo "synth-x skipped" >> "$LOG"
# (3)UI連携=entities+track状態 → wiki/ui-data.json(UIチームが消費)
python3 brain/export_ui.py >> "$LOG" 2>&1 || echo "export_ui skipped" >> "$LOG"

# ingested.txt も add=合成dedup状態を版管理(でないと次サイクルで再合成対象に出る)
git add sources/x wiki/dashboards wiki/entities wiki/concepts wiki/_worklist.md wiki/log.md wiki/ui-data.json brain/state/ingested.txt >> "$LOG" 2>&1 || true
if git diff --cached --quiet; then
  echo "no new data" >> "$LOG"
else
  git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "$LOG" 2>&1
  # push直前にもう一度 rebase: cron実行中に cloud GHA collector が push して分岐した場合に対応。
  git pull -q --rebase --autostash origin main >> "$LOG" 2>&1 || echo "pre-push pull skipped" >> "$LOG"
  git push -q origin main >> "$LOG" 2>&1 && echo "pushed main" >> "$LOG" || echo "push failed(次サイクル再試行)" >> "$LOG"
fi
echo "=== done ===" >> "$LOG"
