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
import re
import subprocess
import sys
import urllib.request
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


STATE = ROOT / "brain" / "state"


def _state_json(name, default):
    try:
        return json.loads((STATE / name).read_text(encoding="utf-8"))
    except Exception:
        return default


def _tail_jsonl(name, n, maxbytes=300000):
    """大きい jsonl の末尾 n 行を効率的に(末尾チャンクのみ読む)。"""
    p = STATE / name
    try:
        size = p.stat().st_size
        with open(p, "rb") as f:
            f.seek(max(0, size - maxbytes))
            chunk = f.read().decode("utf-8", "replace")
        out = []
        for ln in [x for x in chunk.splitlines() if x.strip()][-n:]:
            try:
                out.append(json.loads(ln))
            except Exception:
                pass
        return out
    except Exception:
        return []


_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _http_json(url, timeout=12):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": _UA}), timeout=timeout)
        return json.loads(r.read())
    except Exception:
        return None


def _score_token(token):
    """ape-or-avoid 総合読み(決定的・LLM不使用・$0)＝scam門(rugcheck)+base-rate文脈。
    CA→on-chain判定 / ticker→wikiからCA解決 試行。正直にape断定しない(base-rate厳しい)。"""
    token = token.strip()
    m = re.search(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", token)
    ca = m.group(0) if m else None
    wiki_excerpt = None
    if not ca:  # ticker → 合成wikiページからCAを探す
        d = _retriever().page(token)
        if d:
            wiki_excerpt = d["body"][:600]
            mm = re.search(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", d["body"])
            ca = mm.group(0) if mm else None
        if not ca:
            return {"token": token, "verdict": "需CA",
                    "verdict_reason": "on-chain判定には CA(mint address) が要る。tickerのみだと合成wikiの読みだけ。",
                    "wiki": wiki_excerpt}
    onchain, flags = {}, []
    pf = _http_json(f"https://frontend-api-v3.pump.fun/coins/{ca}")
    if pf:
        onchain["pump"] = {"sym": pf.get("symbol"), "name": pf.get("name"),
                           "mcap": pf.get("usd_market_cap"), "reply": pf.get("reply_count"),
                           "complete": pf.get("complete"), "twitter": pf.get("twitter")}
    rc = _http_json(f"https://api.rugcheck.xyz/v1/tokens/{ca}/report")
    if rc:
        th = rc.get("topHolders") or []
        top_pct = round(max((h.get("pct") or 0) for h in th), 1) if th else None
        danger = [r.get("name") for r in (rc.get("risks") or []) if r.get("level") == "danger"]
        onchain["rugcheck"] = {"rugged": rc.get("rugged"), "mint_auth": rc.get("mintAuthority"),
                               "top_holder_pct": top_pct, "insiders": bool(rc.get("insiderNetworks")),
                               "danger": danger}
        if rc.get("rugged"):
            flags.append("rugged済(資金抜け確認)")
        if rc.get("mintAuthority"):
            flags.append("mint権限残存(増刷可)")
        if top_pct and top_pct > 20:
            flags.append(f"保有集中(top {top_pct}%)")
        if rc.get("insiderNetworks"):
            flags.append("インサイダーnetwork検出")
        flags += [f"危険: {dn}" for dn in danger]
    br = _state_json("base_rate.json", {})
    gp = br.get("gate_passed") or 1
    die_pct = round(100 * (br.get("died") or 0) / gp, 1)
    rugged = bool(onchain.get("rugcheck", {}).get("rugged"))
    if rugged or any(f.startswith("危険") for f in flags):
        verdict = "AVOID"
    elif len(flags) >= 2:
        verdict = "高リスク(避け寄り)"
    elif flags:
        verdict = "要注意"
    elif not rc:
        verdict = "判定不可(on-chain取得失敗)"
    else:
        verdict = "赤旗なし(但base-rate注意)"
    return {"token": token, "ca": ca, "verdict": verdict,
            "flags": flags or (["on-chain赤旗なし"] if rc else ["on-chainデータ無し"]),
            "onchain": onchain,
            "base_rate_note": f"門通過でも約{die_pct}%が死ぬ(pump.fun base rate)＝赤旗無し≠安全。",
            "wiki": wiki_excerpt}


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
        # ★Batch2 real-time/判断機能(state読むだけ・read-only・$0)
        if path0 == "/api/hot":
            live = _state_json("live_pulse.json", {})
            tc = [t for t in live.get("traction_candidates", []) if not t.get("stale")]
            tc.sort(key=lambda t: -(t.get("変化pct") or 0))
            self._json(200, {"ok": True, "hot": tc, "themes": live.get("theme_distribution", {}),
                             "flow": live.get("flow_count_nonscam"), "generated_at": live.get("generated_at")})
            return
        if path0 == "/api/launches":
            qs = parse_qs(urlparse(self.path).query)
            n = min(int(qs.get("n", ["30"])[0] or 30), 200)
            rows = _tail_jsonl("launch_queue.jsonl", n)
            keys = ("mint", "symbol", "name", "creator", "created", "twitter",
                    "usd_mcap", "reply", "rc_score", "top_pct", "insiders", "kol", "reason", "detected_at")
            launches = [{k: r.get(k) for k in keys} for r in rows][::-1]
            self._json(200, {"ok": True, "launches": launches, "count": len(launches)})
            return
        if path0 == "/api/base-rate":
            br = _state_json("base_rate.json", {})
            st = _state_json("launch_stats.json", {})
            gp = br.get("gate_passed") or 0
            self._json(200, {"ok": True,
                             "funnel": {"mints_seen": br.get("mints_seen"), "gate_passed": gp,
                                        "graduated": br.get("graduated"), "died": br.get("died")},
                             "rates": {"gate_pass_pct": round(100 * gp / (br.get("mints_seen") or 1), 3),
                                       "graduate_pct": round(100 * (br.get("graduated") or 0) / (gp or 1), 1),
                                       "die_pct": round(100 * (br.get("died") or 0) / (gp or 1), 1)},
                             "observe_stats": st})
            return
        if path0 == "/api/kol":
            qs = parse_qs(urlparse(self.path).query)
            minev = int(qs.get("min", ["10"])[0] or 10)
            kol = _state_json("kol_track_records.json", {})
            rows = [v for v in kol.values() if (v.get("evaluated") or 0) >= minev]
            rows.sort(key=lambda v: (v.get("death_rate") if v.get("death_rate") is not None else 100))
            self._json(200, {"ok": True, "kol": rows, "min_evaluated": minev})
            return
        if path0 == "/api/death-ledger":
            br = _state_json("base_rate.json", {})
            live = _state_json("live_pulse.json", {})
            gp = br.get("gate_passed") or 0
            self._json(200, {"ok": True,
                             "died": br.get("died"), "graduated": br.get("graduated"),
                             "gate_passed": gp,
                             "death_rate_pct": round(100 * (br.get("died") or 0) / (gp or 1), 1),
                             "death_denominator": live.get("death_denominator", {})})
            return
        # ★本丸: ape-or-avoid 総合スコア(scam門+base-rate・on-chain読む・$0)
        if path0 == "/api/score":
            qs = parse_qs(urlparse(self.path).query)
            tok = (qs.get("token", qs.get("ca", qs.get("name", [""])))[0]).strip()
            if not tok:
                self._json(400, {"ok": False, "error": "token が空(\$ticker か CA)"})
                return
            try:
                self._json(200, {"ok": True, **_score_token(tok)})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★定期ダイジェスト: 日次snapshot差分＝先週/昨日から何が変わったか
        if path0 == "/api/digest":
            hist = _tail_jsonl("pulse_history.jsonl", 8)
            if not hist:
                self._json(200, {"ok": True, "digest": None, "note": "snapshot不足"})
                return
            latest = hist[-1]
            prior = hist[-2] if len(hist) >= 2 else None
            NUM = ["mints_seen", "gate_passed", "graduated", "died", "signal_backlog",
                   "single_source", "stale", "watchlist", "death_ledger"]
            deltas = {}
            if prior:
                for kk in NUM:
                    a, b = latest.get(kk), prior.get(kk)
                    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        deltas[kk] = {"now": a, "prev": b, "delta": round(a - b, 2)}
            self._json(200, {"ok": True, "latest_date": latest.get("date"),
                             "prior_date": (prior or {}).get("date"), "deltas": deltas,
                             "themes_now": latest.get("themes"), "snapshots": len(hist)})
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
