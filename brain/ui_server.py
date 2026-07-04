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
import time
import urllib.request
import uuid
from collections import deque
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# --- 簡易 per-IP rate limit(公開保護・特に score の on-chain呼び)。stdlib のみ・in-memory ---
_RL = {}


def _to_int(v, default):
    """クエリparam等を安全にint化。壊れた値(?k=abc)で公開エンドポイントを落とさない(2026-07-02 fix H2)。"""
    try:
        return int(v)
    except (ValueError, TypeError):
        return default


def _real_ip(handler):
    """cloudflared quick tunnel 越しだと client_address は常に 127.0.0.1＝全公開ユーザーが
    1バケット共有し1人でDoSできる。信頼トンネル(唯一の入口)の Cf-Connecting-IP / XFF先頭を使う(2026-07-02 fix H5)。"""
    h = handler.headers
    ip = h.get("Cf-Connecting-IP") or (h.get("X-Forwarded-For") or "").split(",")[0].strip()
    return ip or handler.client_address[0]


def _rate_ok(key, limit, window=60):
    now = time.time()
    dq = _RL.setdefault(key, deque())
    while dq and dq[0] < now - window:
        dq.popleft()
    if len(dq) >= limit:
        return False
    dq.append(now)
    if len(_RL) > 5000:  # メモリ暴走ガード
        for k in [k for k, v in list(_RL.items()) if not v or v[-1] < now - window]:
            _RL.pop(k, None)
    return True

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
ASK = ROOT / "brain" / "ask.sh"
ASK_TIMEOUT = 240  # headless claude は 1-3 分かかる


def _load_dotenv():
    """起動wrapperが .env を読まない経路(本番で実測)でも DETECT_WEBHOOK_TOKEN 等が
    確実に見えるよう、サーバ自身が repo ルートの .env を読む(2026-07-04)。
    既存の環境変数は上書きしない。ファイル無し等は静かに続行。"""
    try:
        p = ROOT / ".env"
        if not p.exists():
            return
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()
            if k and k not in os.environ:
                os.environ[k] = v
    except Exception:
        pass

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

# UIチームが全機能を発見できる自己ドキュメント(/api/index で返す)
API_INDEX = [
    {"path": "/api/ask", "method": "POST", "body": {"question": "str"},
     "desc": "Q&A脳=claudeが全wiki横断・6レンズ・引用で合成回答(数十秒〜)"},
    {"path": "/api/search", "method": "GET", "params": {"q": "問い", "k": "件数=8"},
     "desc": "合成wikiをBM25検索→Top-Kページ(LLM不要・$0)"},
    {"path": "/api/page", "method": "GET", "params": {"path": "wiki/..md or $ticker/stem"},
     "desc": "合成ページ本文(markdown)を返す"},
    {"path": "/api/related", "method": "GET", "params": {"path": "..."},
     "desc": "知識グラフ=外向き[[link]]+内向き被リンク(concept優先・総数付)"},
    {"path": "/api/concepts", "method": "GET", "desc": "概念ページ一覧(合成の目次)"},
    {"path": "/api/recent", "method": "GET", "params": {"n": "30", "kind": "任意"},
     "desc": "最近更新ページ(日付降順=合成の鮮度)"},
    {"path": "/api/tags", "method": "GET", "desc": "タグ→ページ(件数降順)"},
    {"path": "/api/graph", "method": "GET", "params": {"kinds": "concepts,queries,players"},
     "desc": "知識グラフ nodes/edges(可視化用)"},
    {"path": "/api/similar", "method": "GET", "params": {"path": "..."},
     "desc": "類似ページ(横の発見)"},
    {"path": "/api/autocomplete", "method": "GET", "params": {"q": "前方一致"},
     "desc": "ticker/entity 補完"},
    {"path": "/api/entity", "method": "GET", "params": {"name": "$ticker/handle"},
     "desc": "token/player 構造化(本文+関連グラフ+tags)"},
    {"path": "/api/live", "method": "GET", "desc": "リアルタイムpump観測(live_pulse生)"},
    {"path": "/api/hot", "method": "GET", "desc": "今動いてる銘柄(traction・変化pct順)+theme分布"},
    {"path": "/api/launches", "method": "GET", "params": {"n": "30"},
     "desc": "直近の新規mint(rc_score/insider/kol付)"},
    {"path": "/api/base-rate", "method": "GET", "desc": "mint→passed→graduate/die funnel+rate"},
    {"path": "/api/kol", "method": "GET", "params": {"min": "評価数=10"},
     "desc": "KOL信頼ランク(death_rate昇順)"},
    {"path": "/api/death-ledger", "method": "GET", "desc": "died/graduated/death_rate+分母"},
    {"path": "/api/score", "method": "GET", "params": {"token": "$ticker or CA"},
     "desc": "★ape-or-avoid=scam門(rugcheck)+保有集中+base-rateで張る/避ける判定"},
    {"path": "/api/digest", "method": "GET", "desc": "日次snapshot差分=何が変わった(mints/死/台帳…)"},
    {"path": "/api/contradictions", "method": "GET", "desc": "⚠️矛盾フラグの立ったページ(矛盾の表面化)"},
    {"path": "/api/orphans", "method": "GET", "params": {"kind": "任意"},
     "desc": "孤立ページ(被リンク0=死蔵候補)"},
    {"path": "/api/gaps", "method": "GET", "desc": "繋がり弱い/薄いconcept=知識ギャップ"},
    {"path": "/api/stats", "method": "GET", "desc": "wiki全体統計(kind別/links/orphans/矛盾/tags)"},
    {"path": "/api/survivors", "method": "GET", "desc": "graduated&生存 token(survivor memes・traction先頭)"},
    {"path": "/api/watchlist", "method": "GET", "desc": "現watchlist(追跡アカ)"},
    {"path": "/api/themes", "method": "GET", "desc": "現narrative分布(live_pulse theme)"},
    {"path": "/api/creator", "method": "GET", "params": {"wallet": "creator address"},
     "desc": "creator発行履歴=連続rugger検出(serial_flag)"},
    {"path": "/api/health", "method": "GET", "desc": "脳の健康(signal_backlog/鮮度/wiki規模)"},
    {"path": "/api/sitemap", "method": "GET", "desc": "全ページ一覧(path/title/kind=ナビ/クロール)"},
    {"path": "/api/compare", "method": "GET", "params": {"a": "...", "b": "..."},
     "desc": "2エンティティを並べて比較(token/player)"},
    {"path": "/api/detect", "method": "POST", "body": {"ca": "str", "symbol": "str", "verdict": "APE|REVIEW|AVOID|WATCH|RECOVERED"},
     "desc": "External detector webhook. Appends normalized CALL detections to brain/state/detections.jsonl."},
    {"path": "/api/detections", "method": "GET", "params": {"n": "50", "include_avoids": "1"},
     "desc": "Recent detector events plus CALL-shaped rows for UI/debug."},
    {"path": "/api/feed", "method": "GET",
     "desc": "ホーム用アグリゲート=hot+直近launch+最近更新+themes を1呼びで"},
]


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


DETECTION_VERDICTS = {"APE", "REVIEW", "AVOID", "WATCH", "RECOVERED"}
DETECTION_MAX_BODY = 65536


def _clean_text(value, default="", limit=500):
    if value is None:
        return default
    text = str(value).strip()
    return text[:limit] if text else default


def _clean_number(value, default=0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _clean_reasons(value):
    if isinstance(value, list):
        return [_clean_text(v, limit=180) for v in value if _clean_text(v, limit=180)][:8]
    if value:
        return [_clean_text(value, limit=180)]
    return []


def _now_iso(ts=None):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts or time.time()))


def _normalize_detection(body):
    if not isinstance(body, dict):
        raise ValueError("body must be object")
    # 互換: smart_wallet 検知側は token_ca / token_name / type=MULTI_BUY|3_WALLET_BUY / wallet_count を送る
    # (2026-07-04 依頼仕様)。猫太郎bot は ca|mint / symbol / verdict / metrics を送る。両方受ける。
    ca = _clean_text(
        body.get("ca") or body.get("mint") or body.get("token_ca")
        or body.get("address") or body.get("contract"),
        limit=120,
    )
    if not ca:
        raise ValueError("ca or mint (or token_ca) is required")

    ts = int(time.time())
    verdict = _clean_text(body.get("verdict") or body.get("status") or "REVIEW", "REVIEW", 40).upper()
    if verdict not in DETECTION_VERDICTS:
        verdict = "REVIEW"
    # type は自由記述を保持(検知側が増えるたび enum が嘘になる)。空だけ SMART DETECT に落とす。
    dtype = _clean_text(body.get("signal_type") or body.get("type") or "SMART DETECT", "SMART DETECT", 60).upper()

    metrics = dict(body.get("metrics")) if isinstance(body.get("metrics"), dict) else {}
    # smart_wallet 系の付帯情報は metrics に畳む(正規化スキーマを汚さず保存)
    for k in ("token_price", "token_mc", "timestamp"):
        if body.get(k) is not None and k not in metrics:
            metrics[k] = body.get(k)
    txs = body.get("tx_hashes")
    if isinstance(txs, list) and txs and "tx_hashes" not in metrics:
        metrics["tx_hashes"] = [_clean_text(t, limit=120) for t in txs[:10]]

    wallet_count = body.get("wallet_count")
    det = {
        "id": _clean_text(body.get("id"), limit=80) or f"detect_{time.strftime('%Y%m%d_%H%M%S', time.gmtime(ts))}_{uuid.uuid4().hex[:6]}",
        "source": _clean_text(body.get("source"), "unknown", 80),
        "chain": _clean_text(body.get("chain"), "solana", 40),
        "symbol": _clean_text(body.get("symbol") or body.get("ticker") or body.get("token")
                              or body.get("token_name"), "UNKNOWN", 80),
        "name": _clean_text(body.get("name") or body.get("title") or body.get("token_name"), "UNKNOWN", 160),
        "ca": ca,
        "mint": ca,
        "type": dtype,
        "signal_type": dtype,
        "verdict": verdict,
        "wallet_count": int(_clean_number(wallet_count, 0)) or None,
        "risk_score": _clean_number(body.get("risk_score"), None),
        "reasons": _clean_reasons(body.get("reasons") or body.get("reason") or body.get("why")),
        "metrics": metrics,
        "detected_at": _clean_text(body.get("detected_at") or body.get("observed_at") or body.get("created_at"), _now_iso(ts), 80),
        "url": _clean_text(body.get("url") or body.get("link"), "", 500),
        "received_at": _now_iso(ts),
    }
    return det


def _parse_money(v):
    """"$45K"->45000.0 / "$1.2M"->1200000.0 / "$1,234"->1234.0 / 45000->45000.0 / 不能->0.0
    smart_wallet 検知の metrics.token_mc は money文字列で来る(実測)ため、数値化して使えるようにする。"""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    if not isinstance(v, str):
        return 0.0
    s = v.strip().upper().replace("$", "").replace(",", "")
    if not s:
        return 0.0
    mult = 1.0
    if s[-1] in ("K", "M", "B"):
        mult = {"K": 1e3, "M": 1e6, "B": 1e9}[s[-1]]
        s = s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return 0.0


def _detection_to_call(det):
    metrics = det.get("metrics") if isinstance(det.get("metrics"), dict) else {}
    reasons = det.get("reasons") if isinstance(det.get("reasons"), list) else []
    reason = "; ".join([str(r) for r in reasons[:3]]) or det.get("verdict") or "detected"
    mcap = (metrics.get("mcap_usd") or metrics.get("market_cap") or metrics.get("marketCap")
            or _parse_money(metrics.get("token_mc")) or 0)
    replies = metrics.get("reply_count") or metrics.get("replies") or metrics.get("mentions") or 0
    return {
        "id": det.get("id"),
        "source": det.get("source"),
        "ticker": det.get("symbol"),
        "symbol": det.get("symbol"),
        "name": det.get("name"),
        "ca": det.get("ca"),
        "mint": det.get("mint") or det.get("ca"),
        "type": det.get("type") or det.get("signal_type") or "SMART DETECT",
        "status": det.get("verdict"),
        "verdict": det.get("verdict"),
        "risk_score": det.get("risk_score"),
        "wallet_count": det.get("wallet_count"),
        "reason": reason,
        "gate": reason,
        "mcap": mcap,
        "peak_mcap": metrics.get("peak_mcap") or metrics.get("peak_market_cap") or mcap,
        "reply_count": replies,
        "first_seen": det.get("detected_at"),
        "link": det.get("url"),
        "metrics": metrics,
        "reasons": reasons,
    }


def _recent_detections(n=50, include_avoids=True):
    rows = _tail_jsonl("detections.jsonl", n)
    if not include_avoids:
        rows = [r for r in rows if str(r.get("verdict", "")).upper() != "AVOID"]
    return rows[::-1]


def _append_detection(det):
    STATE.mkdir(parents=True, exist_ok=True)
    with open(STATE / "detections.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(det, ensure_ascii=False, separators=(",", ":")) + "\n")


def _read_json_body(handler, maxbytes=DETECTION_MAX_BODY):
    try:
        n = int(handler.headers.get("Content-Length") or 0)
    except ValueError:
        raise ValueError("bad content-length")
    if n > maxbytes:
        raise OverflowError("body too large")
    return json.loads(handler.rfile.read(n) or b"{}")


def _creator_history(wallet, limit=60):
    """launch_queue を流し読みして creator の発行履歴(連続rugger検出)。`in`前置で高速化。"""
    out = []
    try:
        with open(STATE / "launch_queue.jsonl", encoding="utf-8", errors="replace") as f:
            for ln in f:
                if wallet not in ln:
                    continue
                try:
                    r = json.loads(ln)
                except Exception:
                    continue
                if r.get("creator") == wallet:
                    out.append({k: r.get(k) for k in
                                ("symbol", "name", "mint", "usd_mcap", "rc_score", "top_pct", "insiders", "created")})
    except Exception:
        pass
    return out[-limit:]


_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _http_json(url, timeout=12, retries=2):
    # on-chain(rugcheck/pump)は一時的にコケる→retry で吸収(核の安定)
    for i in range(retries + 1):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": _UA}), timeout=timeout)
            return json.loads(r.read())
        except Exception:
            if i < retries:
                time.sleep(0.6 * (i + 1))
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
        # ATH比は info のみ(flagにしない)＝pump は launch時sniper spikeでathが跳ね、ほぼ全銘柄-99%になり
        # discriminate しない=ノイズ。参考値として残すのみ。
        mc, ath = pf.get("market_cap"), pf.get("ath_market_cap")
        if mc and ath and ath > 0:
            onchain["pump"]["ath_drawdown_pct"] = round(100 * (mc - ath) / ath, 1)
    rc = _http_json(f"https://api.rugcheck.xyz/v1/tokens/{ca}/report")
    if rc:
        # ★LP/market アドレスを除外(spyzercrypto guide: top holderはほぼLP=traderでない→偽の集中flagを除く)
        lp_addrs = set()
        for m in (rc.get("markets") or []):
            for kf in ("pubkey", "liquidityA", "liquidityB", "lp", "mintLP"):
                v = m.get(kf)
                if isinstance(v, str):
                    lp_addrs.add(v)
        th = rc.get("topHolders") or []
        non_lp = [h for h in th if h.get("owner") not in lp_addrs and h.get("address") not in lp_addrs]
        top_pct = round(max((h.get("pct") or 0) for h in non_lp), 2) if non_lp else None
        top5_pct = round(sum((h.get("pct") or 0) for h in non_lp[:5]), 2) if non_lp else None
        insiders_n = sum(1 for h in th if h.get("insider"))
        graph_insiders = rc.get("graphInsidersDetected") or 0
        total_holders = rc.get("totalHolders")
        danger = [r.get("name") for r in (rc.get("risks") or []) if r.get("level") == "danger"]
        onchain["rugcheck"] = {"rugged": rc.get("rugged"), "mint_auth": rc.get("mintAuthority"),
                               "top_holder_pct_nonLP": top_pct, "top5_nonLP_pct": top5_pct,
                               "insiders": bool(rc.get("insiderNetworks")) or insiders_n > 0 or graph_insiders > 0,
                               "insider_holders": insiders_n, "graph_insiders": graph_insiders,
                               "total_holders": total_holders, "rug_score": rc.get("score_normalised"),
                               "lp_usd": round(rc.get("totalMarketLiquidity") or 0), "danger": danger}
        if rc.get("rugged"):
            flags.append("rugged済(資金抜け確認)")
        if rc.get("mintAuthority"):
            flags.append("mint権限残存(増刷可)")
        # ★保有集中の階層閾値(guide: 非LP top holder >3.5% が trenching の赤旗)
        if top_pct is not None:
            if top_pct > 20:
                flags.append(f"保有集中・極大(非LP top {top_pct}%)")
            elif top_pct > 10:
                flags.append(f"保有集中・高(非LP top {top_pct}%)")
            elif top_pct > 3.5:
                flags.append(f"保有集中(非LP top {top_pct}% ＞3.5%基準)")
        # ★bundle検出(guide: 1人が50-80%を複数walletで支配)＝上位集中 or rugcheck graphInsiders
        if top5_pct is not None and top5_pct > 25:
            flags.append(f"bundle疑い(上位5非LP計 {top5_pct}%)")
        if graph_insiders:
            flags.append(f"bundle/insiderグラフ検出({graph_insiders}wallet)")
        elif rc.get("insiderNetworks") or insiders_n:
            flags.append(f"インサイダー検出({insiders_n}wallet)" if insiders_n else "インサイダーnetwork検出")
        # ★holder極少(guide: 少holder×up-only=赤旗)
        if isinstance(total_holders, int) and 0 < total_holders < 15:
            flags.append(f"holder極少({total_holders})")
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
    elif not rc and not pf:
        verdict = "判定不可(on-chain取得失敗・再試行を)"
    elif not rc:
        # rugcheck だけ落ちた=scam門(集中/insider/rugged)未検査→"赤旗なし"は偽の安心なので出さない
        verdict = "部分判定(rugcheck未取得=scam門未検査・pump情報のみ)"
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
        # ルート/ を UI に統合＝公開URLを開いたら即UIが出る（ユーザー導線・dir一覧を出さない）
        if path0 in ("/", "", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/ui/index.html")
            self.end_headers()
            return
        # rate limit(公開保護): score は外部on-chain叩くので厳しめ・他はゆるめ
        if path0.startswith("/api/"):
            ip = _real_ip(self)
            is_score = path0 == "/api/score"
            if not _rate_ok(f"{ip}:{'s' if is_score else 'g'}", 15 if is_score else 90):
                self._json(429, {"ok": False, "error": "rate limit — 少し待ってから再試行"})
                return
        # 自己ドキュメント: 全API機能の一覧(UIチームの発見入口)
        if path0 in ("/api/index", "/api"):
            self._json(200, {"ok": True, "count": len(API_INDEX), "endpoints": API_INDEX})
            return
        # ★案A「検索できるLLM Wiki」: 質問→合成済みwikiページをBM25で返す(クエリ時LLM不要・$0)
        if path0 == "/api/search":
            qs = parse_qs(urlparse(self.path).query)
            q = (qs.get("q", [""])[0]).strip()
            k = min(_to_int(qs.get("k", ["8"])[0] or 8, 8), 20)
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
                n = min(_to_int(qs.get("n", ["30"])[0] or 30, 30), 200)
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
        # ★Batch3 Lint/品質機能(LLM Wikiの核=矛盾surface/孤立/ギャップ・$0)
        if path0 == "/api/contradictions":
            try:
                self._json(200, {"ok": True, "contradictions": _retriever().contradictions()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/orphans":
            qs = parse_qs(urlparse(self.path).query)
            kind = (qs.get("kind", [""])[0]).strip() or None
            try:
                self._json(200, {"ok": True, "orphans": _retriever().orphans(kind)})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/gaps":
            try:
                self._json(200, {"ok": True, "gaps": _retriever().gaps()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/stats":
            try:
                self._json(200, {"ok": True, **_retriever().stats()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★Batch4 intelligence機能(wiki/state読むだけ・$0)
        if path0 == "/api/survivors":
            try:
                self._json(200, {"ok": True, "survivors": _retriever().survivors()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/watchlist":
            try:
                p = WIKI / "watchlist.md"  # wiki直下(rag SUBDIRS外)なので直接読む
                md = None
                if p.exists():
                    md = re.sub(r"\A---\n.*?\n---\n", "", p.read_text(encoding="utf-8"), flags=re.S).strip()
                self._json(200, {"ok": True, "markdown": md})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/themes":
            live = _state_json("live_pulse.json", {})
            th = live.get("theme_distribution", {})
            self._json(200, {"ok": True, "themes": th, "total": sum(th.values()) if th else 0,
                             "generated_at": live.get("generated_at")})
            return
        if path0 == "/api/creator":
            qs = parse_qs(urlparse(self.path).query)
            w = (qs.get("wallet", qs.get("creator", [""]))[0]).strip()
            if not w:
                self._json(400, {"ok": False, "error": "wallet が空"})
                return
            try:
                hist = _creator_history(w)
                self._json(200, {"ok": True, "wallet": w, "token_count": len(hist),
                                 "serial_flag": len(hist) >= 3, "tokens": hist})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★homepage aggregate: hot+launches+recent+themes を1呼びで(UIホーム用)
        if path0 == "/api/feed":
            try:
                r = _retriever()
                live = _state_json("live_pulse.json", {})
                hot = [t for t in live.get("traction_candidates", []) if not t.get("stale")]
                # 門の思想: reply=0(誰も話してない)の未確認moverを変化率だけで先頭にしない。
                # reply>0 を先に、その中で 変化pct 降順。
                hot.sort(key=lambda t: (-(1 if (t.get("reply") or 0) > 0 else 0), -(t.get("変化pct") or 0)))
                # TODO: kol_standouts の先頭挿入は shape検証後(現在0件で未検証・盲目マッピング禁止)。
                calls = [_detection_to_call(x) for x in _recent_detections(20, include_avoids=False)]
                self._json(200, {"ok": True, "hot": hot[:5],
                                 "themes": live.get("theme_distribution", {}),
                                 "recent_launches": [{k: x.get(k) for k in ("symbol", "usd_mcap", "rc_score")}
                                                     for x in _tail_jsonl("launch_queue.jsonl", 5)][::-1],
                                  "recent_wiki": r.recent(6),
                                  "calls": calls,
                                 "generated_at": live.get("generated_at")})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        # ★Batch5 health/sitemap/compare
        if path0 == "/api/health":
            h = (_tail_jsonl("health.jsonl", 1) or [{}])[-1]
            br = _state_json("base_rate.json", {})
            self._json(200, {"ok": True, "signal_backlog": h.get("signal_backlog"),
                             "raw_new": h.get("raw_new"), "single_source": h.get("single_source"),
                             "stale": h.get("stale"), "ts": h.get("ts"),
                             "wiki_pages": _retriever().N, "tracked_passed": br.get("gate_passed")})
            return
        if path0 == "/api/sitemap":
            try:
                self._json(200, {"ok": True, "pages": _retriever().sitemap()})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
            return
        if path0 == "/api/compare":
            qs = parse_qs(urlparse(self.path).query)
            a = (qs.get("a", [""])[0]).strip()
            b = (qs.get("b", [""])[0]).strip()
            if not a or not b:
                self._json(400, {"ok": False, "error": "a と b の両方が要る"})
                return
            try:
                r = _retriever()
                self._json(200, {"ok": True, "a": r.entity(a), "b": r.entity(b)})
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
            n = min(_to_int(qs.get("n", ["30"])[0] or 30, 30), 200)
            rows = _tail_jsonl("launch_queue.jsonl", n)
            keys = ("mint", "symbol", "name", "creator", "created", "twitter",
                    "usd_mcap", "reply", "rc_score", "top_pct", "insiders", "kol", "reason", "detected_at")
            launches = [{k: r.get(k) for k in keys} for r in rows][::-1]
            self._json(200, {"ok": True, "launches": launches, "count": len(launches)})
            return
        if path0 == "/api/detections":
            qs = parse_qs(urlparse(self.path).query)
            n = min(_to_int(qs.get("n", ["50"])[0] or 50, 50), 200)
            include_avoids = str(qs.get("include_avoids", ["1"])[0]).lower() not in ("0", "false", "no")
            detections = _recent_detections(n, include_avoids=include_avoids)
            calls = [_detection_to_call(x) for x in detections]
            self._json(200, {"ok": True, "detections": detections, "calls": calls, "count": len(detections)})
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
            minev = _to_int(qs.get("min", ["10"])[0] or 10, 10)
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
        path0 = self.path.split("?")[0]
        if path0 == "/api/detect":
            token = os.environ.get("DETECT_WEBHOOK_TOKEN", "").strip()
            if not token:
                # トークン未設定＝誰でもPOST可能(本番で素通し実測 2026-07-04)。明示ONでのみ dev 用に開ける
                if os.environ.get("DETECT_ALLOW_UNAUTH") != "1":
                    self._json(503, {"ok": False, "error": "DETECT_WEBHOOK_TOKEN未設定(fail-closed)。devで開けるなら DETECT_ALLOW_UNAUTH=1"})
                    return
            elif self.headers.get("Authorization", "").strip() != f"Bearer {token}":
                self._json(401, {"ok": False, "error": "unauthorized"})
                return
            if not _rate_ok(f"{_real_ip(self)}:detect", 120):
                self._json(429, {"ok": False, "error": "rate limit(detect)"})
                return
            try:
                det = _normalize_detection(_read_json_body(self))
                _append_detection(det)
                self._json(201, {"ok": True, "id": det["id"], "status": "queued", "detection": det})
            except OverflowError:
                self._json(413, {"ok": False, "error": "body too large"})
            except ValueError as e:
                self._json(400, {"ok": False, "error": str(e)[:300]})
            except Exception as e:
                print(f"[detect] error: {e}", file=sys.stderr)
                self._json(500, {"ok": False, "error": "internal error"})
            return
        if path0 != "/api/ask":
            self.send_error(404)
            return
        if not _rate_ok(f"{_real_ip(self)}:ask", 5):  # ask は claude 叩くので厳しめ
            self._json(429, {"ok": False, "error": "rate limit(ask) — 少し待って"})
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
                # 公開=Gemini(無料・ToS安全)を既定・UI規律ON。運用者は ASK_BACKEND=claude で上書き可。
                env={**os.environ, "ASK_UI": "1", "ASK_BACKEND": os.environ.get("ASK_BACKEND", "gemini")},
            )
            ans = (r.stdout or "").strip()
            if not ans:
                print(f"[ask] empty answer; stderr={r.stderr[:500]!r}", file=sys.stderr)  # 詳細はサーバログのみ
                self._json(500, {"ok": False, "error": "脳が応答を返せませんでした"})
                return
            self._json(200, {"ok": True, "answer": ans})
        except subprocess.TimeoutExpired:
            self._json(504, {"ok": False, "error": "脳の応答タイムアウト(>240s)"})
        except Exception as e:
            print(f"[ask] error: {e}", file=sys.stderr)  # 内部詳細(パス等)はクライアントに返さない(info disclosure)
            self._json(500, {"ok": False, "error": "内部エラー"})

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
    _load_dotenv()  # .env 自力読み(未設定キーのみ)。認証トークン等が起動wrapper任せにならないように
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
