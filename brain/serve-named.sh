#!/bin/bash
# serve-named.sh — Trench-Brain を恒久URL(named tunnel)で公開する。
# quick tunnel(URL毎回変わる)の代わりに固定 https://trenchbrain.fun を使う版。
# creds: ~/.cloudflared/{cert.pem,<id>.json,config.yml}（config.yml が 127.0.0.1:8000 を指す）。
# 停止: Ctrl-C。常時ON運用は trench-serve-named.bat(flock respawn)から呼ぶ。
set -euo pipefail
cd "$(dirname "$0")/.."
PORT="${PORT:-8000}"

if [ -f ./.env ]; then set -a; . ./.env; set +a; fi
command -v python3 >/dev/null 2>&1 || { echo "python3 が必要"; exit 1; }
command -v cloudflared >/dev/null 2>&1 || { echo "cloudflared 未インストール"; exit 1; }

PIDS=()
cleanup() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null || true; done; }
trap cleanup EXIT INT TERM

# realtime writer（多重起動guard付なので既存が居ても安全）
if [ "${NO_REALTIME:-}" != "1" ]; then
  python3 brain/launch_stream.py >> brain/state/launch_stream.log 2>&1 &
  PIDS+=("$!")
  python3 brain/live_pulse_writer.py --interval 120 >> brain/state/live_pulse_writer.log 2>&1 &
  PIDS+=("$!")
  echo "realtime writer 起動"
  sleep 1
fi

# 死活監視
python3 brain/watchdog.py --interval 120 --port "$PORT" >> brain/state/watchdog.log 2>&1 &
PIDS+=("$!")
echo "watchdog 起動"

# ui_server（read-only 脳API）
python3 brain/ui_server.py --port "$PORT" --host 127.0.0.1 &
SRV="$!"
PIDS+=("$SRV")
sleep 2
kill -0 "$SRV" 2>/dev/null || { echo "ui_server 起動失敗"; exit 1; }
echo "ui_server: http://127.0.0.1:$PORT"

# 固定URLを記録
echo "https://trenchbrain.fun" > brain/state/public_url.txt
echo "公開URL(恒久): https://trenchbrain.fun"

# named tunnel（config.yml の ingress で 127.0.0.1:8000 → trench.trenchbrain.fun）
echo "named tunnel 起動中..."
exec cloudflared tunnel --no-autoupdate run trench
