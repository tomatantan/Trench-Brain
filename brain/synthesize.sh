#!/bin/bash
# synthesize.sh — auto-synthesis の「合成(LLM)」工程を無人で回す。
# track.py が出した synth_queue を headless claude が wiki に合成する。
# キューが空なら claude を呼ばない（コスト0）。cron が前後で git する。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
Q="brain/state/synth_queue.json"
MODEL="${SYNTH_MODEL:-sonnet}"   # コスト管理: 既定 sonnet。SYNTH_MODEL で上書き可
ENABLED="${SYNTH_ENABLED:-1}"    # 0 で無効化(自動課金を止めたい時)

[ "$ENABLED" = "1" ] || { echo "synth: disabled(SYNTH_ENABLED=0)" >> "$LOG"; exit 0; }
[ -f "$Q" ] || { echo "synth: no queue" >> "$LOG"; exit 0; }

n=$(python3 -c "import json;q=json.load(open('$Q'));print(len(q.get('births',[]))+len(q.get('changes',[]))+len(q.get('deaths',[])))" 2>/dev/null || echo 0)
if [ "$n" -eq 0 ]; then
  echo "synth: queue empty, skip(claude未呼出)" >> "$LOG"
  exit 0
fi

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) synth start: $n items (model=$MODEL) ===" >> "$LOG"
if ! command -v claude >/dev/null 2>&1; then
  echo "synth: claude CLI not found → 合成スキップ(queue保持)" >> "$LOG"
  exit 0
fi
claude --print --model "$MODEL" --dangerously-skip-permissions \
  "$(cat brain/synth_prompt.md)" >> "$LOG" 2>&1 \
  && echo "synth: done" >> "$LOG" \
  || echo "synth: claude error(queue保持・次サイクル再試行)" >> "$LOG"
