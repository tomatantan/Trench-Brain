#!/bin/bash
# synthesize_gaps.sh — wiki_gaps.json の gap を headless claude が保守的に自動解決する。
# wiki_autofix.py が積んだ concept-gap を消費する。
# queueが空なら claude を呼ばない（コスト0）。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
# ハング防止: timeout があれば claude を上限付きで実行(WSL=有り / macは gtimeout or 無し)。無ければそのまま。
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
SYNTH_TIMEOUT="${SYNTH_TIMEOUT:-900}"   # 秒。合成は通常1-4分・900s(15分)で"ハング"と判断
GAP="brain/state/wiki_gaps.json"
SIG_FILE="brain/state/gaps_last_sig.txt"
MODEL="${SYNTH_MODEL:-sonnet}"   # synthesize.sh と同じ変数名・既定値

# wiki_gaps.json が無い場合は skip
[ -f "$GAP" ] || { echo "gaps: no file, skip" >> "$LOG"; exit 0; }

# 空リスト [] または中身ゼロなら skip（コスト0）
n=$(python3 -c "import json;d=json.load(open('$GAP'));print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo 0)
if [ "$n" -eq 0 ]; then
  echo "gaps: empty, skip" >> "$LOG"
  exit 0
fi

# 署名比較: gap 集合が前回と同じなら skip（既レビュー済・recurring LLMコスト防止）
current_sig=$(python3 -c "
import json,hashlib
d=json.load(open('$GAP'))
concepts=sorted(x['concept'] for x in d if isinstance(x,dict) and 'concept' in x)
print(hashlib.md5(','.join(concepts).encode()).hexdigest())
" 2>/dev/null || echo "")

prev_sig=""
[ -f "$SIG_FILE" ] && prev_sig=$(cat "$SIG_FILE" 2>/dev/null || echo "")

if [ -n "$current_sig" ] && [ "$current_sig" = "$prev_sig" ]; then
  echo "gaps: unchanged since last run, skip" >> "$LOG"
  exit 0
fi

echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) gaps start: $n items (model=$MODEL) ===" >> "$LOG"

if ! command -v claude >/dev/null 2>&1; then
  echo "gaps: claude CLI not found → スキップ(queue保持)" >> "$LOG"
  exit 0
fi

# --strict-mcp-config: MCPを一切起動しない。これが無いと headless claude が
# グローバル有効の telegram プラグインの poller を起動し、getUpdates は1トークン
# 1ポーラー仕様なので本人のチャンネル poller を SIGTERM で乗っ取って切断する
# (2026-06-23 フラッピング原因特定)。gap解決はファイル読み書きのみで telegram不要。
${TIMEOUT_BIN:+$TIMEOUT_BIN $SYNTH_TIMEOUT} claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/gap_prompt.md)" >> "$LOG" 2>&1 \
  && { echo "gaps: done" >> "$LOG"; [ -n "$current_sig" ] && echo "$current_sig" > "$SIG_FILE"; } \
  || echo "gaps: claude error(queue保持)" >> "$LOG"
