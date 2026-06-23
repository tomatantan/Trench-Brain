#!/bin/bash
# synthesize_x.sh — X側 auto-synthesis の「合成(LLM)」工程を無人で回す。
# ingest_worklist.py が出した wiki/_worklist.md の §1a(鮮度ゲート通過＝今ホット)を
# headless claude が上位3件だけ合成する(bounded=複利)。§1aが空なら claude を呼ばない(コスト0)。
# cron が前後で git する。pump.fun側の synthesize.sh と対をなす(両輪のX側)。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
WL="wiki/_worklist.md"
MODEL="${SYNTH_MODEL:-sonnet}"        # コスト管理: 既定 sonnet
ENABLED="${SYNTH_X_ENABLED:-1}"       # 0 で無効化(X合成だけ止めたい時)

[ "$ENABLED" = "1" ] || { echo "synth-x: disabled(SYNTH_X_ENABLED=0)" >> "$LOG"; exit 0; }
[ -f "$WL" ] || { echo "synth-x: no worklist" >> "$LOG"; exit 0; }

# §1a テーブルに entity 行(| [[$TICKER]] |)があるか＝合成対象の有無
hot=$(awk '/## 1a\)/{f=1;next} /## 1b\)/{f=0} f && /^\| \[\[\$/{c++} END{print c+0}' "$WL")
if [ "${hot:-0}" -eq 0 ]; then
  echo "synth-x: §1a empty, skip(claude未呼出)" >> "$LOG"
  exit 0
fi

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) synth-x start: §1a=$hot hot (process top3, model=$MODEL) ===" >> "$LOG"
if ! command -v claude >/dev/null 2>&1; then
  echo "synth-x: claude CLI not found → スキップ" >> "$LOG"
  exit 0
fi
# --strict-mcp-config 必須: headless claude に telegram 等の MCP を一切起動させない
# (起動すると getUpdates 1トークン1ポーラー仕様で本人チャンネルを乗っ取り切断する。2026-06-23)。
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/synth_x_prompt.md)" >> "$LOG" 2>&1 \
  && echo "synth-x: done" >> "$LOG" \
  || echo "synth-x: claude error(次サイクル再試行)" >> "$LOG"
