#!/bin/bash
# serve.sh — Trench-Brain を $0 で公開する（ui_server + cloudflared quick tunnel）。
#
# 使い方(Windows WSL/Ubuntu か Mac):
#   bash brain/serve.sh
#   → 数秒後、公開HTTPS URL (https://xxxx.trycloudflare.com) が表示される。
#     アカウント登録/課金/DNS設定 いっさい不要（quick tunnel＝匿名・無料・即席）。
#   停止: Ctrl-C。
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

# 1) ui_server を background 起動
python3 brain/ui_server.py --port "$PORT" --host 127.0.0.1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT INT TERM
sleep 2
if ! kill -0 "$SRV" 2>/dev/null; then echo "ui_server 起動失敗"; exit 1; fi
echo "✅ ui_server: http://127.0.0.1:$PORT  (脳API=/api/index)"

# 2) cloudflared quick tunnel（匿名・無料）。公開URLは *.trycloudflare.com 行に出る
echo "🌐 公開トンネル起動中… 下の https://*.trycloudflare.com が公開URL:"
exec cloudflared tunnel --url "http://127.0.0.1:$PORT" --no-autoupdate
