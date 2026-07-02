#!/bin/bash
# synthesize_longform.sh — 長文ソース(YouTube/podcast transcript)の合成工程を無人で回す。
# collect_youtube.py が貯めた sources/youtube/*.md(synthesized:false)を headless claude が
# 新しい順 最大3本 deep 合成する(bounded=volume制御)。未合成0なら claude を呼ばない(コスト0)。
# X(synthesize_x.sh)/pump(synthesize.sh)に続く第3の合成輪。cron が前後で git する。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
# ハング防止: timeout があれば claude を上限付きで実行(WSL=有り / macは gtimeout or 無し)。無ければそのまま。
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
SYNTH_TIMEOUT="${SYNTH_TIMEOUT:-900}"   # 秒。合成は通常1-4分・900s(15分)で"ハング"と判断
SRC="sources/youtube"
MODEL="${SYNTH_MODEL:-sonnet}"
ENABLED="${SYNTH_LONGFORM_ENABLED:-1}"   # 0 で無効化

[ "$ENABLED" = "1" ] || { echo "synth-longform: disabled" >> "$LOG"; exit 0; }
[ -d "$SRC" ] || { echo "synth-longform: no transcripts dir" >> "$LOG"; exit 0; }

# 未合成(synthesized:false)の本数
pending=$(grep -rl "^synthesized: false" "$SRC" 2>/dev/null | wc -l | tr -d ' ')
if [ "${pending:-0}" -eq 0 ]; then
  echo "synth-longform: 未合成0、skip(claude未呼出)" >> "$LOG"
  exit 0
fi

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) synth-longform start: 未合成${pending}本 (process top3, model=$MODEL) ===" >> "$LOG"
[ "${pending}" -gt 30 ] && echo "synth-longform: ⚠️ 未合成${pending}本 >30 ＝transcript収集が合成を追い越し気味(門/limitを絞る判断材料)。" >> "$LOG"

command -v claude >/dev/null 2>&1 || { echo "synth-longform: claude CLI なし→skip" >> "$LOG"; exit 0; }
# --strict-mcp-config 必須(telegram等MCPを起動させない。2026-06-23 切断原因)。
${TIMEOUT_BIN:+$TIMEOUT_BIN $SYNTH_TIMEOUT} claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/synth_longform_prompt.md)" >> "$LOG" 2>&1 \
  && echo "synth-longform: done" >> "$LOG" \
  || echo "synth-longform: claude error(次サイクル再試行)" >> "$LOG"
