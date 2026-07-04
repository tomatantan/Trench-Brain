#!/bin/bash
# synthesize_revise.sh — G4自己改訂の consumer。revise_detect.py が積んだ stale数値キューを
# headless claude が「推移を保持したまま」再合成する。queueが空なら claude を呼ばない（コスト0）。
# 流儀は synthesize_gaps.sh と同一(署名dedup / timeout / --strict-mcp-config)。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
SYNTH_TIMEOUT="${SYNTH_TIMEOUT:-900}"
QUEUE="brain/state/revise_queue.json"
SIG_FILE="brain/state/revise_last_sig.txt"
MODEL="${SYNTH_MODEL:-sonnet}"

[ -f "$QUEUE" ] || { echo "revise: no queue, skip" >> "$LOG"; exit 0; }

n=$(python3 -c "import json;d=json.load(open('$QUEUE'));print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo 0)
if [ "$n" -eq 0 ]; then
  echo "revise: empty, skip" >> "$LOG"
  exit 0
fi

# 署名dedup: 同じ乖離集合を毎サイクル再合成しない(LLM出力が同じ乖離を残した場合の無限コスト防止)。
# 署名に current(実測側)も含める=実測がさらにドリフトしたら別署名になり再試行される(敵対検証P1: 永久凍結防止)。
current_sig=$(python3 -c "
import json,hashlib
d=json.load(open('$QUEUE'))
keys=sorted(f\"{x['page']}|{x['metric']}|{x['written_pct']}|{x.get('current')}\" for x in d if isinstance(x,dict))
print(hashlib.md5(','.join(keys).encode()).hexdigest())
" 2>/dev/null || echo "")
prev_sig=""
[ -f "$SIG_FILE" ] && prev_sig=$(cat "$SIG_FILE" 2>/dev/null || echo "")
if [ -n "$current_sig" ] && [ "$current_sig" = "$prev_sig" ]; then
  echo "revise: unchanged since last run, skip" >> "$LOG"
  exit 0
fi

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) revise start: $n items (model=$MODEL) ===" >> "$LOG"
if ! command -v claude >/dev/null 2>&1; then
  echo "revise: claude CLI not found → スキップ(queue保持)" >> "$LOG"
  exit 0
fi

# --strict-mcp-config: telegram poller 乗っ取り防止(synthesize_gaps.sh の注記と同じ)。
${TIMEOUT_BIN:+$TIMEOUT_BIN $SYNTH_TIMEOUT} claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/revise_prompt.md)" >> "$LOG" 2>&1 \
  && { echo "revise: done" >> "$LOG"; [ -n "$current_sig" ] && echo "$current_sig" > "$SIG_FILE"; } \
  || echo "revise: claude error(queue保持)" >> "$LOG"
