#!/bin/bash
# synthesize_lint.sh — 第5の輪＝自己検証(lint)。過学習アナログの対策。
# wiki自身の「小N型/spurious・ナラティブlock-in・矛盾・門バイアス・陳腐化・孤立」を
# headless claude が敵対的に探し wiki/lint-report.md に**報告のみ**(自動修正しない=CLAUDE.md Lint規約)。
# 維持工程なので頻度は低め＝~日次(前回から HRS時間 経過時だけ実行)。cron が前後で git。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
# ハング防止: timeout があれば claude を上限付きで実行(WSL=有り / macは gtimeout or 無し)。無ければそのまま。
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
SYNTH_TIMEOUT="${SYNTH_TIMEOUT:-900}"   # 秒。合成は通常1-4分・900s(15分)で"ハング"と判断
STAMP="brain/state/last_lint"
MODEL="${SYNTH_MODEL:-sonnet}"
ENABLED="${SYNTH_LINT_ENABLED:-1}"
HRS="${LINT_INTERVAL_HRS:-20}"   # この時間内に実行済なら skip(=~日次)

[ "$ENABLED" = "1" ] || { echo "lint: disabled" >> "$LOG"; exit 0; }

# 頻度ゲート: 前回 lint から HRS 時間未満なら skip(コスト0)
if [ -f "$STAMP" ]; then
  last=$(cat "$STAMP" 2>/dev/null || echo 0)
  now=$(date +%s)
  age_h=$(( (now - last) / 3600 ))
  if [ "$age_h" -lt "$HRS" ]; then
    echo "lint: skip(前回から${age_h}h<${HRS}h)" >> "$LOG"
    exit 0
  fi
fi

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) lint start (model=$MODEL) ===" >> "$LOG"
command -v claude >/dev/null 2>&1 || { echo "lint: claude CLI なし→skip" >> "$LOG"; exit 0; }
# --strict-mcp-config 必須(telegram等MCPを起動させない。2026-06-23 切断原因)。
if ${TIMEOUT_BIN:+$TIMEOUT_BIN $SYNTH_TIMEOUT} claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
     "$(cat brain/lint_prompt.md)" >> "$LOG" 2>&1; then
  date +%s > "$STAMP"
  echo "lint: done" >> "$LOG"
else
  echo "lint: claude error(次サイクル再試行)" >> "$LOG"
fi
