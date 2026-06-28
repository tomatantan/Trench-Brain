#!/usr/bin/env python3
"""
ui_server.py — Trench-Brain UI の「脳」バックエンド(read-only)

- wiki/ を静的配信         … UI=/ui/index.html / データ=/ui-data.json
- POST /api/ask {question} … brain/ask.sh(実脳=headless claude が全wiki横断・6レンズ・引用) を叩いて合成回答を返す

read-only(ask.sh は wiki を読むだけ=書かない=Windows の合成 writer と衝突しない)。標準ライブラリのみ。
これで UI の chat が「決め打ちmock」から「実脳の合成回答」になる。

起動: python3 brain/ui_server.py [--port 8000] [--host 127.0.0.1]
UI:   http://localhost:8000/ui/index.html
"""
import argparse
import json
import subprocess
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
ASK = ROOT / "brain" / "ask.sh"
ASK_TIMEOUT = 240  # headless claude は 1-3 分かかる


class Handler(SimpleHTTPRequestHandler):
    # --- 全レスポンスに CORS(+GETはno-cache) を付ける ---
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        if self.command == "GET":
            self.send_header("Cache-Control", "no-store")  # ui-data.json の鮮度
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/ask":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
            q = (body.get("question") or "").strip()
        except Exception:
            self._json(400, {"ok": False, "error": "bad request"})
            return
        if not q:
            self._json(400, {"ok": False, "error": "empty question"})
            return
        try:
            r = subprocess.run(
                ["bash", str(ASK), q],
                capture_output=True, text=True, timeout=ASK_TIMEOUT, cwd=str(ROOT),
            )
            ans = (r.stdout or "").strip()
            if not ans:
                self._json(500, {"ok": False, "error": (r.stderr or "ask.sh が空応答")[:500]})
                return
            self._json(200, {"ok": True, "answer": ans})
        except subprocess.TimeoutExpired:
            self._json(504, {"ok": False, "error": "脳の応答タイムアウト(>240s)"})
        except Exception as e:
            self._json(500, {"ok": False, "error": str(e)[:500]})

    def _json(self, code, obj):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):  # 静音
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    handler = partial(Handler, directory=str(WIKI))
    srv = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Trench-Brain UI: http://{args.host}:{args.port}/ui/index.html  (脳=POST /api/ask)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
