#!/bin/bash
# serve-askwin.sh — ローカル(Windows/WSL)のサブスク Haiku 窓口(ask_window.py)を
# 専用 named tunnel(ask.trenchbrain.fun)で公開する(2026-07-10)。VM の ask.sh が
# ここを叩いて Haiku 合成を得る。落ちてれば VM は Gemini に自動fallback。
# 常時ON は trench-askwin.bat(flock respawn)から呼ぶ。停止: Ctrl-C。
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f ./.env ]; then set -a; . ./.env; set +a; fi
command -v python3 >/dev/null 2>&1 || { echo "python3 が必要"; exit 1; }
command -v cloudflared >/dev/null 2>&1 || { echo "cloudflared 未インストール"; exit 1; }
mkdir -p brain/state

PIDS=()
cleanup() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null || true; done; }
trap cleanup EXIT INT TERM

# Haiku 窓口(read-only・全ツール無効の claude を叩くだけ)
ASK_WINDOW_PORT="${ASK_WINDOW_PORT:-8791}" python3 brain/ask_window.py >> brain/state/ask_window.log 2>&1 &
PIDS+=("$!")
sleep 2
kill -0 "${PIDS[0]}" 2>/dev/null || { echo "ask_window 起動失敗"; exit 1; }
echo "ask_window: http://127.0.0.1:${ASK_WINDOW_PORT:-8791}"

# named tunnel(ask.trenchbrain.fun → 127.0.0.1:8791)
echo "ask tunnel 起動中..."
exec cloudflared tunnel --no-autoupdate --config "$HOME/.cloudflared/config-ask.yml" run trench-ask
