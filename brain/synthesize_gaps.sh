#!/bin/bash
# synthesize_gaps.sh — wiki_gaps.json の gap を headless claude が保守的に自動解決する。
# wiki_autofix.py が積んだ concept-gap を消費する。
# queueが空なら claude を呼ばない（コスト0）。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
GAP="brain/state/wiki_gaps.json"
MODEL="${SYNTH_MODEL:-sonnet}"   # synthesize.sh と同じ変数名・既定値

# wiki_gaps.json が無い場合は skip
[ -f "$GAP" ] || { echo "gaps: no file, skip" >> "$LOG"; exit 0; }

# 空リスト [] または中身ゼロなら skip（コスト0）
n=$(python3 -c "import json;d=json.load(open('$GAP'));print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo 0)
if [ "$n" -eq 0 ]; then
  echo "gaps: empty, skip" >> "$LOG"
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
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/gap_prompt.md)" >> "$LOG" 2>&1 \
  && echo "gaps: done" >> "$LOG" \
  || echo "gaps: claude error(queue保持)" >> "$LOG"
