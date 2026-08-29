#!/bin/bash
# synthesize.sh — auto-synthesis の「合成(LLM)」工程を無人で回す。
# track.py が出した synth_queue を headless claude が wiki に合成する。
# キューが空なら claude を呼ばない（コスト0）。cron が前後で git する。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
# ハング防止: timeout があれば claude を上限付きで実行(WSL=有り / macは gtimeout or 無し)。無ければそのまま。
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
SYNTH_TIMEOUT="${SYNTH_TIMEOUT:-900}"   # 秒。合成は通常1-4分・900s(15分)で"ハング"と判断
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
# --strict-mcp-config: MCPを一切起動しない。これが無いと headless claude が
# グローバル有効の telegram プラグインの poller を起動し、getUpdates は1トークン
# 1ポーラー仕様なので本人のチャンネル poller を SIGTERM で乗っ取って切断する
# (2026-06-23 フラッピング原因特定)。合成はファイル読み書きのみで telegram不要。
# 合成の本命はローカルLLM(2026-08-30)。
#   実障害: claude CLI のトークンが失効し、20分おきに 401 を出しては
#   「queue保持・次サイクル再試行」を書くだけを延々と繰り返していた。
#   cron.log には出ていたが誰にも通知しないので気づかれず、queueは4,319件まで積んだ。
#   認証にも課金にも依存しない経路を既定にする(brain/synthesize_local.py)。
#   ollama が居ない/落ちている時だけ claude に戻る。
#   どちらも失敗したら queue は保持されるので、取りこぼしはしない。
OLLAMA_BASE="${OLLAMA_URL:-http://$(ip route show default 2>/dev/null | awk '{print $3}'):11434}"
if curl -s -m 5 -o /dev/null "$OLLAMA_BASE/api/tags"; then
  ${TIMEOUT_BIN:+$TIMEOUT_BIN $SYNTH_TIMEOUT} python3 brain/synthesize_local.py >> "$LOG" 2>&1 \
    && echo "synth: done(local)" >> "$LOG" \
    || echo "synth: local error(queue保持・次サイクル再試行)" >> "$LOG"
  exit 0
fi
echo "synth: ollama unreachable($OLLAMA_BASE) -> claude にフォールバック" >> "$LOG"
${TIMEOUT_BIN:+$TIMEOUT_BIN $SYNTH_TIMEOUT} claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/synth_prompt.md)" >> "$LOG" 2>&1 \
  && echo "synth: done" >> "$LOG" \
  || echo "synth: claude error(queue保持・次サイクル再試行)" >> "$LOG"
