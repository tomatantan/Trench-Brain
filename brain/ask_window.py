#!/usr/bin/env python3
"""
ask_window.py — ローカル(Windows/WSL)のサブスク claude を、VM 側 ask.sh から叩くための
最小・堅牢な窓口(2026-07-10)。VM は公開URLを持つが Windows は NAT 内で直接到達不可なので、
この窓口を専用 cloudflared tunnel(ask.trenchbrain.fun)で公開する。Windows が落ちてれば到達不能
→VMはGeminiへ自動fallback。

★脅威モデル(2026-07-10 本人合意): 「他人に使われる(サブスク消費)」はリスクとしない。守るのは
**攻撃(RCE/ファイル窃取/マシン侵入)**。よって合言葉(認証)は付けず、代わりに「攻撃対象がそもそも
存在しない」状態を作る:
- claude を **--tools "" (全ツール無効) --strict-mcp-config (MCP無効)** ＋ 権限昇格フラグなしで起動
  ＝Bash/Read/Write/MCP が一切無い"喋るだけ"の箱。どんなプロンプト注入でもコマンド実行/ファイル
  読み書き/データ窃取が構造的に不可能。返せるのはテキストのみ。
- prompt は **stdin で claude に渡す(シェルを通さない・subprocess list形式)** ＝コマンドインジェクション不可。
- POST /ask だけ。他パス/メソッドは 404。
- レート制限(既定 30req/60s)＋prompt 長 上限(既定 200KB)＝DoS 緩和(使用量課金でなくマシン保護目的)。
- model は allowlist(haiku/sonnet)のみ。
- 127.0.0.1 バインド(tunnel 経由のみ)。tunnel はこの1エンドポイントだけ公開(マシン全体は晒さない)。

env: ASK_WINDOW_PORT(既定8791) / ASK_WINDOW_MODEL(既定haiku)
     / CLAUDE_BIN(既定 ~/.local/bin/claude) / ASK_ROOT(既定 ~/trench-brain)
"""
import json
import os
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("ASK_WINDOW_PORT", "8791"))
DEFAULT_MODEL = os.environ.get("ASK_WINDOW_MODEL", "haiku")
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", str(Path.home() / ".local/bin/claude"))
ROOT = Path(os.environ.get("ASK_ROOT", str(Path.home() / "trench-brain")))
MODEL_ALLOW = {"haiku", "sonnet"}
MAX_PROMPT = 200_000          # bytes
CLAUDE_TIMEOUT = 200          # sec
RL_MAX = 30                   # requests
RL_WINDOW = 60               # sec

_hits = []                    # rate-limit タイムスタンプ


def _rate_ok():
    now = time.time()
    _hits[:] = [t for t in _hits if now - t < RL_WINDOW]
    if len(_hits) >= RL_MAX:
        return False
    _hits.append(now)
    return True


def _run_claude(prompt, model):
    p = subprocess.run(
        [CLAUDE_BIN, "--print", "--tools", "", "--strict-mcp-config", "--model", model],
        input=prompt, capture_output=True, text=True, timeout=CLAUDE_TIMEOUT, cwd=str(ROOT),
    )
    return (p.stdout or "").strip()


class H(BaseHTTPRequestHandler):
    server_version = "aw"        # サーバ情報を隠す
    sys_version = ""

    def log_message(self, *a):   # アクセスログにクエリ等を出さない
        pass

    def _send(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path != "/ask":
            self.send_response(404); self.end_headers(); return
        if not _rate_ok():
            self._send(429, {"ok": False, "error": "rate limit"}); return
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._send(400, {"ok": False, "error": "bad length"}); return
        if n > MAX_PROMPT:
            self._send(413, {"ok": False, "error": "too large"}); return
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            prompt = body.get("prompt") or ""
            model = body.get("model") or DEFAULT_MODEL
        except Exception:
            self._send(400, {"ok": False, "error": "bad json"}); return
        if not isinstance(prompt, str) or not prompt.strip():
            self._send(400, {"ok": False, "error": "empty prompt"}); return
        if model not in MODEL_ALLOW:
            model = DEFAULT_MODEL
        try:
            answer = _run_claude(prompt, model)
        except subprocess.TimeoutExpired:
            self._send(504, {"ok": False, "error": "claude timeout"}); return
        except Exception:
            self._send(500, {"ok": False, "error": "claude error"}); return
        if not answer:
            self._send(502, {"ok": False, "error": "empty answer"}); return
        self._send(200, {"ok": True, "answer": answer, "model": model})


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    sys.stderr.write(f"ask_window listening 127.0.0.1:{PORT} model={DEFAULT_MODEL}\n")
    srv.serve_forever()


if __name__ == "__main__":
    main()
