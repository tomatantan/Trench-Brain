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
import os
import subprocess
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
ASK = ROOT / "brain" / "ask.sh"
ASK_TIMEOUT = 240  # headless claude は 1-3 分かかる

# ★案A「検索できるLLM Wiki」: rag.py の retriever を遅延ロード(初回検索で索引構築)
sys.path.insert(0, str(Path(__file__).resolve().parent))
_RETRIEVER = None


def _retriever():
    global _RETRIEVER
    if _RETRIEVER is None:
        import rag
        _RETRIEVER = rag.Retriever()
    return _RETRIEVER


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

    def do_GET(self):
        path0 = self.path.split("?")[0]
        # ★案A「検索できるLLM Wiki」: 質問→合成済みwikiページをBM25で返す(クエリ時LLM不要・$0)
        if path0 == "/api/search":
            qs = parse_qs(urlparse(self.path).query)
            q = (qs.get("q", [""])[0]).strip()
            k = min(int(qs.get("k", ["8"])[0] or 8), 20)
            if not q:
                self._json(400, {"ok": False, "error": "q が空"})
                return
            try:
                hits = _retriever().search(q, k)
                results = [{
                    "score": round(s, 2), "title": d["title"], "path": d["path"],
                    "excerpt": d["body"].strip()[:280],
                } for s, d in hits]
                self._json(200, {"ok": True, "query": q, "results": results})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★合成ページ本文を返す(UI表示用)。path= は 'wiki/...md' でも $ticker/stem でも可
        if path0 == "/api/page":
            qs = parse_qs(urlparse(self.path).query)
            ref = (qs.get("path", qs.get("id", [""]))[0]).strip()
            if not ref:
                self._json(400, {"ok": False, "error": "path が空"})
                return
            try:
                d = _retriever().page(ref)
                if not d:
                    self._json(404, {"ok": False, "error": f"ページ無し: {ref}"})
                    return
                self._json(200, {"ok": True, "title": d["title"], "path": d["path"],
                                 "markdown": d["body"].strip()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★知識グラフ navigation: そのページの外向き[[link]]先 と 内向き(被リンク)
        if path0 == "/api/related":
            qs = parse_qs(urlparse(self.path).query)
            ref = (qs.get("path", qs.get("id", [""]))[0]).strip()
            if not ref:
                self._json(400, {"ok": False, "error": "path が空"})
                return
            try:
                rel = _retriever().related(ref)
                self._json(200, {"ok": True, "path": ref, **rel})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★Batch1 知識アクセス機能(全部 rag.py を読むだけ・read-only・$0)
        if path0 == "/api/concepts":
            try:
                self._json(200, {"ok": True, "concepts": _retriever().concepts()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/recent":
            qs = parse_qs(urlparse(self.path).query)
            try:
                n = min(int(qs.get("n", ["30"])[0] or 30), 200)
                kind = (qs.get("kind", [""])[0]).strip() or None
                self._json(200, {"ok": True, "recent": _retriever().recent(n, kind)})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/tags":
            try:
                self._json(200, {"ok": True, "tags": _retriever().tags_index()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/graph":
            qs = parse_qs(urlparse(self.path).query)
            try:
                kinds = tuple(filter(None, (qs.get("kinds", [""])[0]).split(","))) or ("concepts", "queries", "players")
                self._json(200, {"ok": True, **_retriever().graph(kinds)})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/similar":
            qs = parse_qs(urlparse(self.path).query)
            ref = (qs.get("path", qs.get("id", [""]))[0]).strip()
            if not ref:
                self._json(400, {"ok": False, "error": "path が空"})
                return
            try:
                self._json(200, {"ok": True, "path": ref, "similar": _retriever().similar(ref)})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/autocomplete":
            qs = parse_qs(urlparse(self.path).query)
            q = (qs.get("q", [""])[0]).strip()
            try:
                self._json(200, {"ok": True, "suggestions": _retriever().autocomplete(q) if q else []})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/entity":
            qs = parse_qs(urlparse(self.path).query)
            ref = (qs.get("name", qs.get("path", [""]))[0]).strip()
            if not ref:
                self._json(400, {"ok": False, "error": "name が空"})
                return
            try:
                ent = _retriever().entity(ref)
                if not ent:
                    self._json(404, {"ok": False, "error": f"entity無し: {ref}"})
                    return
                self._json(200, {"ok": True, **ent})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # リアルタイム pump 層: brain/state/live_pulse.json を配信(wiki外なので特別route)
        if path0 == "/api/live":
            p = ROOT / "brain" / "state" / "live_pulse.json"
            if not p.exists():
                self._json(404, {"ok": False, "error": "live_pulse 未生成(brain/live_pulse_writer.py を起動)"})
                return
            try:
                b = p.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        super().do_GET()

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
                env={**os.environ, "ASK_UI": "1"},  # UI経由=user-facing出力規律ON(内部状態を見せない)
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
