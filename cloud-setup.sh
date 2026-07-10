#!/usr/bin/env bash
# cloud-setup.sh — Trench-Brain 公開serving層をクラウドVM(Oracle等)に常駐化する。
# 2026-07-08 「Windowsから卒業」対応。PCが落ちてもサービスが死なない様に serving層
# (ui_server + cloudflared named tunnel + realtime writer)を systemd 常駐にする。
#
# 冪等(何度流してもOK)。Ubuntu(apt) / Oracle Linux(dnf) と x86_64 / aarch64 を自動判別。
# 前提: このリポジトリ(~/trench-brain 一式)と ~/.cloudflared/{cert.pem,<id>.json,config.yml}、
#       ~/trench-brain/.env が WSL から転送済みであること(runbook 参照)。
#
# 使い方:  sudo bash ~/trench-brain/cloud-setup.sh
set -euo pipefail

# --- 実行ユーザー(cloudflared creds / .env の持ち主)を特定 -------------------
SVC_USER="${SUDO_USER:-$(id -un)}"
SVC_HOME="$(getent passwd "$SVC_USER" | cut -d: -f6)"
REPO_DIR="${REPO_DIR:-$SVC_HOME/trench-brain}"
CF_DIR="$SVC_HOME/.cloudflared"
TUNNEL_ID="223e8712-47b3-40a2-a1ed-fc1f7e1a45dd"

echo "== ユーザー=$SVC_USER  home=$SVC_HOME  repo=$REPO_DIR =="

# --- 1. 依存 ------------------------------------------------------------------
echo "== 1. 依存パッケージ =="
if command -v apt-get >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y python3 python3-pip git curl
elif command -v dnf >/dev/null 2>&1; then
  dnf install -y python3 python3-pip git curl
elif command -v yum >/dev/null 2>&1; then
  yum install -y python3 python3-pip git curl
else
  echo "!! apt/dnf/yum が無い。python3/git/curl を手動で入れて再実行して" >&2; exit 1
fi

# requirements.txt があれば入れる
if [ -f "$REPO_DIR/requirements.txt" ]; then
  sudo -u "$SVC_USER" python3 -m pip install --user -r "$REPO_DIR/requirements.txt" || true
fi

# --- 2. cloudflared (arch判別してバイナリ配置) --------------------------------
echo "== 2. cloudflared =="
case "$(uname -m)" in
  x86_64)  CF_ARCH=amd64 ;;
  aarch64) CF_ARCH=arm64 ;;
  *) echo "!! 未知arch $(uname -m) — 手動でcloudflared入れて" >&2; exit 1 ;;
esac
if ! command -v cloudflared >/dev/null 2>&1; then
  curl -fL -o /usr/local/bin/cloudflared \
    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-${CF_ARCH}"
  chmod +x /usr/local/bin/cloudflared
fi
echo -n "cloudflared: "; cloudflared --version || { echo "!! cloudflared起動不可" >&2; exit 1; }

# --- 3. creds / .env の存在チェック -------------------------------------------
echo "== 3. creds / .env =="
[ -f "$CF_DIR/cert.pem" ]            || { echo "!! $CF_DIR/cert.pem が無い。WSLの ~/.cloudflared を転送して" >&2; exit 1; }
[ -f "$CF_DIR/$TUNNEL_ID.json" ]     || { echo "!! $CF_DIR/$TUNNEL_ID.json が無い。転送して" >&2; exit 1; }
[ -f "$REPO_DIR/.env" ]             || { echo "!! $REPO_DIR/.env が無い。転送して" >&2; exit 1; }

# --- 4. config.yml を VM のパスに合わせて再生成 -------------------------------
echo "== 4. config.yml 再生成(credentials-file を $CF_DIR に固定) =="
cat > "$CF_DIR/config.yml" <<YML
tunnel: $TUNNEL_ID
credentials-file: $CF_DIR/$TUNNEL_ID.json

ingress:
  - hostname: trenchbrain.fun
    service: http://127.0.0.1:8000
  - hostname: cave.trenchbrain.fun
    service: http://127.0.0.1:8000
  - hostname: trench.trenchbrain.fun
    service: http://127.0.0.1:8000
  - service: http_status:404
YML
chown -R "$SVC_USER":"$SVC_USER" "$CF_DIR"
chmod 600 "$CF_DIR/$TUNNEL_ID.json" "$CF_DIR/cert.pem" 2>/dev/null || true

# --- 5. systemd unit --------------------------------------------------------
echo "== 5. systemd unit =="
cat > /etc/systemd/system/trench-serve.service <<UNIT
[Unit]
Description=Trench-Brain public serving (ui_server + cloudflared tunnel + realtime)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SVC_USER
WorkingDirectory=$REPO_DIR
Environment=PATH=/usr/local/bin:/usr/bin:/bin:$SVC_HOME/.local/bin
Environment=HOME=$SVC_HOME
Environment=PORT=8000
Environment=ASK_BACKEND=gemini
ExecStart=/usr/bin/env bash $REPO_DIR/brain/serve-named.sh
Restart=always
RestartSec=5
KillMode=control-group

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now trench-serve.service

# --- 6. 検証 ----------------------------------------------------------------
echo "== 6. 起動待ち(15s)して検証 =="
sleep 15
echo -n "local ui_server: "; curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 http://127.0.0.1:8000/ui/index.html || echo "NG"
echo "systemd status:"; systemctl --no-pager --lines=8 status trench-serve.service || true

cat <<'DONE'

=========================================================================
セットアップ完了。次にやること:
  1) 数十秒待って、外から https://trenchbrain.fun/ui/index.html が 200 か確認
       curl -s -o /dev/null -w "%{http_code}\n" https://trenchbrain.fun/ui/index.html
  2) 200 を確認したら Windows 側の serving を止める(二重tunnel=負荷分散で不整合になるため):
       - Startup から trench-serve-named.bat を外す
       - 動いてる WSL 側 cloudflared/ui_server を止める
     ※ synth(trench-synth.bat) と bot(trench-bot.bat) は Windows に残してOK。
  3) ログ確認:  journalctl -u trench-serve.service -f
=========================================================================
DONE
