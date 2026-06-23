#!/bin/bash
# launch_synth.sh — 流れの連続合成(本人意図×芯の両立)。
# 個別ページ量産(firehose/指針2違反)でなく、launch_pulse.py で**流れを集約**→ claude が1回で
# 『launch-pulse concept(今何が発射されてるか)』を更新＋traction+KOL standoutだけ個別採用。
# ＝湯水を止めず"流れの意味"を合成し続ける。--strict-mcp-config(telegram干渉なし)。throughput安全(1合成/回)。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${LAUNCH_SYNTH_MODEL:-sonnet}"
WINDOW_H="${LAUNCH_PULSE_WINDOW_H:-6}"
LOG="brain/state/launch_synth.log"
command -v claude >/dev/null 2>&1 || { echo "no claude" >> "$LOG"; exit 0; }
echo "=== $(date -u +%H:%M:%SZ) launch pulse synth ===" >> "$LOG"

# 流れを集約(決定的)
AGG="$(python3 brain/launch_pulse.py "$WINDOW_H" 2>>"$LOG")"
CNT="$(printf '%s' "$AGG" | python3 -c "import sys,json;print(json.load(sys.stdin).get('flow_count_nonscam',0))" 2>/dev/null || echo 0)"
if [ "${CNT:-0}" = "0" ]; then echo "pulse: 流れ無し(skip)" >> "$LOG"; exit 0; fi

# 流れの意味を合成(pulse concept更新 + standout採用) — 1回のLLM呼び出し
PROMPT="$(cat brain/launch_synth_prompt.md)
$AGG"
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT" >> "$LOG" 2>&1 || echo "pulse synth err" >> "$LOG"

# 連続合成を即永続(cloudと分岐しても壊れない)
if ! git diff --quiet wiki/ 2>/dev/null; then
  git add wiki/concepts/launch-pulse.md wiki/entities/tokens/ wiki/index.md 2>/dev/null || true
  git commit -q -m "launch-pulse: 出来立ての流れを集約合成(launch_stream→pulse)+standout採用" >/dev/null 2>&1 || true
  git pull -q --rebase --autostash origin main >/dev/null 2>&1 || true
  git push -q origin main >/dev/null 2>&1 || true
fi
echo "pulse synth done (flow=$CNT)" >> "$LOG"
