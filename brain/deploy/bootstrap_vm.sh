#!/bin/bash
# bootstrap_vm.sh — trenchbrain.fun serving層のクラウドVM初期化（家の単一障害点の根治・2026-07-08）。
# 対象: Ubuntu 22.04/24.04 (Oracle always-free A1 ARM 等)。root or sudo で1回実行。
#
# 役割分担（この VM は serving 専任・合成はしない）:
#   - ui_server(read-only API+UI) + cloudflared named tunnel = 公開面
#   - 15分毎 git fetch/reset で repo 追従（家のWindows/Macが全滅しても serving は生き続ける）
#   - /api/ask は gemini($0)。claude CLI は置かない（サブスクToS/コスト・ask.shはgemini専で動く様に対応済）
#
# 使い方（環境変数で渡す・対話なし）:
#   sudo GIT_DEPLOY_KEY_B64=<base64秘密鍵> TUNNEL_TOKEN=<cloudflare tunnel token> \
#        GEMINI_API_KEY=<鍵> [TWITTERAPI_KEY=<鍵>] bash bootstrap_vm.sh
set -euo pipefail

REPO_SSH="git@github.com:tomatantan/Trench-Brain.git"
APP_USER="trench"
APP_DIR="/opt/trench-brain"
PORT=8000

[ "$(id -u)" = "0" ] || { echo "sudo/root で実行して"; exit 1; }
: "${GIT_DEPLOY_KEY_B64:?read-only deploy key (base64) が要る}"
: "${TUNNEL_TOKEN:?cloudflare tunnel token が要る}"
: "${GEMINI_API_KEY:?gemini key が要る(公開askの\$0脳)}"

echo "== 1/6 packages =="
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git python3 curl ca-certificates >/dev/null

echo "== 2/6 app user + deploy key =="
id "$APP_USER" >/dev/null 2>&1 || useradd -m -s /bin/bash "$APP_USER"
install -d -m 700 -o "$APP_USER" -g "$APP_USER" "/home/$APP_USER/.ssh"
printf '%s' "$GIT_DEPLOY_KEY_B64" | base64 -d > "/home/$APP_USER/.ssh/id_ed25519"
chmod 600 "/home/$APP_USER/.ssh/id_ed25519"; chown "$APP_USER:$APP_USER" "/home/$APP_USER/.ssh/id_ed25519"
sudo -u "$APP_USER" ssh-keyscan github.com >> "/home/$APP_USER/.ssh/known_hosts" 2>/dev/null
chown "$APP_USER:$APP_USER" "/home/$APP_USER/.ssh/known_hosts"

echo "== 3/6 clone repo =="
if [ ! -d "$APP_DIR/.git" ]; then
  install -d -o "$APP_USER" -g "$APP_USER" "$APP_DIR"
  sudo -u "$APP_USER" git clone --depth 50 "$REPO_SSH" "$APP_DIR"
fi
# .env（秘密はrepoに置かない・VMローカルのみ）
{
  echo "GEMINI_API_KEY=$GEMINI_API_KEY"
  [ -n "${TWITTERAPI_KEY:-}" ] && echo "TWITTERAPI_KEY=$TWITTERAPI_KEY"
} > "$APP_DIR/.env"
chown "$APP_USER:$APP_USER" "$APP_DIR/.env"; chmod 600 "$APP_DIR/.env"

echo "== 4/6 systemd: ui_server =="
cat > /etc/systemd/system/trench-ui.service <<EOF
[Unit]
Description=trench-brain ui_server (read-only serving)
After=network-online.target
[Service]
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment=ASK_BACKEND=gemini
ExecStart=/usr/bin/python3 $APP_DIR/brain/ui_server.py --host 127.0.0.1 --port $PORT
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF

echo "== 5/6 systemd: 15分毎 repo 追従（read-only消費者=fetch+reset・conflict無縁） =="
cat > /usr/local/bin/trench-pull.sh <<'EOF'
#!/bin/bash
set -e
cd /opt/trench-brain
BEFORE="$(git rev-parse HEAD:brain/ui_server.py 2>/dev/null || true)$(git rev-parse HEAD:brain/rag.py 2>/dev/null || true)"
git fetch -q origin main
git reset -q --hard origin/main
AFTER="$(git rev-parse HEAD:brain/ui_server.py 2>/dev/null || true)$(git rev-parse HEAD:brain/rag.py 2>/dev/null || true)"
# サーバ本体のコードが変わった時だけ再起動（ask.sh/prompt等はリクエスト毎読込=再起動不要）
if [ "$BEFORE" != "$AFTER" ]; then
  systemctl restart trench-ui
fi
EOF
chmod +x /usr/local/bin/trench-pull.sh
cat > /etc/systemd/system/trench-pull.service <<EOF
[Unit]
Description=trench-brain repo pull
[Service]
Type=oneshot
ExecStart=/usr/local/bin/trench-pull.sh
EOF
cat > /etc/systemd/system/trench-pull.timer <<EOF
[Unit]
Description=trench-brain repo pull every 15min
[Timer]
OnBootSec=2min
OnUnitActiveSec=15min
[Install]
WantedBy=timers.target
EOF

echo "== 6/6 cloudflared (named tunnel・token方式) =="
if ! command -v cloudflared >/dev/null 2>&1; then
  ARCH="$(dpkg --print-architecture)"  # arm64 / amd64
  curl -fsSL -o /tmp/cloudflared.deb "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${ARCH}.deb"
  dpkg -i /tmp/cloudflared.deb >/dev/null
fi
cloudflared service install "$TUNNEL_TOKEN" 2>/dev/null || true  # 既installなら無視

systemctl daemon-reload
systemctl enable --now trench-ui.service trench-pull.timer cloudflared 2>/dev/null || systemctl enable --now trench-ui.service trench-pull.timer
sleep 3
echo "== 検証 =="
curl -s -m 10 "http://127.0.0.1:$PORT/api/health" | head -c 200; echo
systemctl is-active trench-ui trench-pull.timer cloudflared || true
echo "== done. Cloudflare dashboard 側で tunnel の Public Hostname を trenchbrain.fun -> http://localhost:$PORT に向ければ公開完了 =="
