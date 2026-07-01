#!/bin/bash
# serve.sh — Trench-Brain を $0 で公開する（ui_server + cloudflared quick tunnel）。
#
# 使い方(Windows WSL/Ubuntu か Mac):
#   bash brain/serve.sh
#   → 数秒後、公開HTTPS URL (https://xxxx.trycloudflare.com) が表示される。
#     アカウント登録/課金/DNS設定 いっさい不要（quick tunnel＝匿名・無料・即席）。
#   停止: Ctrl-C。
#
# 起動するもの（全部入り＝これ1本で全機能ON）:
#   - launch_stream + live_pulse_writer … リアルタイム pump 観測（/api/live /hot /launches /feed を生かす）
#   - ui_server … 脳API 31機能（read-only）
#   - cloudflared quick tunnel … 公開HTTPS URL
#   ※ realtime writer 不要なら NO_REALTIME=1 bash brain/serve.sh
#
# 公開されるもの:
#   - UI:      https://xxxx.trycloudflare.com/ui/index.html   (UIチームのフロント)
#   - 脳API:   https://xxxx.trycloudflare.com/api/index        (backend 31機能・全read-only)
#   - 検索デモ: https://xxxx.trycloudflare.com/ui/wiki.html
#
# ※ ui_server は read-only（wikiを書かない＝Windowsの合成writerと非衝突）。
# ※ trycloudflare の URL は起動ごとに変わる（恒久URLが要るなら named tunnel＝要Cloudflareアカウント・別途）。
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${PORT:-8000}"

command -v python3 >/dev/null 2>&1 || { echo "python3 が必要"; exit 1; }

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "❌ cloudflared 未インストール。入れて再実行:"
  echo "  WSL/Ubuntu: sudo curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && sudo chmod +x /usr/local/bin/cloudflared"
  echo "  Windows直:  winget install --id Cloudflare.cloudflared"
  echo "  Mac:        brew install cloudflared"
  exit 1
fi

PIDS=()
trap 'for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null || true; done' EXIT INT TERM

# 0) リアルタイム pump 観測 writer（launch_stream=全mint観測→queue/base_rate・多重起動guard付 / live_pulse_writer=集約→live_pulse.json）
# これが動いてないと /api/live /hot /launches /feed(hot) が空になる。
if [ "${NO_REALTIME:-}" != "1" ]; then
  python3 brain/launch_stream.py >> brain/state/launch_stream.log 2>&1 & PIDS+=($!)
  python3 brain/live_pulse_writer.py --interval 120 >> brain/state/live_pulse_writer.log 2>&1 & PIDS+=($!)
  echo "✅ realtime writer 起動（launch_stream + live_pulse_writer）→ live_pulse/hot/launches が生きる"
  sleep 1
fi

# 0.5) 死活監視 watchdog（writer/tunnel/ui_server/合成backlog を監視・失敗時に .env の TG_BOT_TOKEN で通知）
python3 brain/watchdog.py --interval 120 --port "$PORT" >> brain/state/watchdog.log 2>&1 & PIDS+=($!)
echo "✅ watchdog 起動（死活監視→ state/watchdog_status.json ・失敗時 telegram通知）"

# 1) ui_server を background 起動
python3 brain/ui_server.py --port "$PORT" --host 127.0.0.1 & SRV=$!; PIDS+=($SRV)
sleep 2
if ! kill -0 "$SRV" 2>/dev/null; then echo "ui_server 起動失敗"; exit 1; fi
echo "✅ ui_server: http://127.0.0.1:$PORT  (脳API=/api/index)"

# 2) cloudflared quick tunnel（匿名・無料）。公開URLを brain/state/public_url.txt に自動記録
#    ＝再起動でURLが変わっても「今のURL」は常にこのファイルで分かる（常時ON運用の要）。
echo "🌐 公開トンネル起動中… 下の https://*.trycloudflare.com が公開URL:"
cloudflared tunnel --url "http://127.0.0.1:$PORT" --no-autoupdate 2>&1 | while IFS= read -r line; do
  echo "$line"
  url=$(printf '%s' "$line" | grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' | head -1)
  if [ -n "$url" ]; then
    printf '%s\n' "$url" > brain/state/public_url.txt
    echo "📌 公開URL を brain/state/public_url.txt に記録: $url"
  fi
done
