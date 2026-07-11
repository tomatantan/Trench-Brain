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

# A2: Live Activity push(brain/apns_push.py・stdlib only・sibling module)
from apns_push import send_live_activity_push


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
    {"path": "/api/judge", "method": "GET/POST",
     "params": {"e": "entity,entity2,... (GET・カンマ区切り・$有無どちらも可・最大50)"},
     "body": {"entities": ["str", "..."]},
     "desc": "★トークンサーフィン用の一瞬バッジ=networkを呼ばずローカルstateのみで<50ms判定。詳細は/api/scoreへエスカレーション"},
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
    {"path": "/api/la/register", "method": "POST", "body": {"token": "str"},
     "desc": "Register/replace the Live Activity APNs push token (brain/state/la_token.json). No auth, rate-limited only."},
    {"path": "/api/la/push", "method": "POST", "body": {"status": "str", "hook": "str?", "bump": "bool?"},
     "desc": "Push a Live Activity content-state update (status/count/lastHook) via APNs for the registered token. Bearer-authed like /api/detect."},
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


# --- /api/judge: トークンサーフィン用の一瞬バッジ ---
# network呼ばず brain/state/*.json だけを読む決定的判定(LLM不使用)。<50msを狙い、
# 大きい tracked.json(数MB)はモジュールレベルで mtime キャッシュ(変わらない限り再パースしない)。
_JUDGE_CA_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
_STATE_MTIME_CACHE = {}  # name -> (mtime, data)
_TRACKED_CACHE = {"mtime": None, "by_mint": {}, "by_ticker": {}}


def _cached_state_json(name, default):
    """_state_json のキャッシュ版: mtime が変わってなければ再読込しない(judge の性能要件用)。"""
    p = STATE / name
    try:
        mtime = p.stat().st_mtime
    except OSError:
        return default
    cached = _STATE_MTIME_CACHE.get(name)
    if cached is not None and cached[0] == mtime:
        return cached[1]
    data = _state_json(name, default)
    _STATE_MTIME_CACHE[name] = (mtime, data)
    return data


def _tracked_data():
    """tracked.json を mint→rec と ticker(upper・$無し)→[rec,...](first_seen昇順) の両方でキャッシュ。"""
    p = STATE / "tracked.json"
    try:
        mtime = p.stat().st_mtime
    except OSError:
        return {}, {}
    if _TRACKED_CACHE["mtime"] == mtime:
        return _TRACKED_CACHE["by_mint"], _TRACKED_CACHE["by_ticker"]
    by_mint = _state_json("tracked.json", {})
    by_ticker = {}
    for rec in by_mint.values():
        t = (rec.get("ticker") or "").strip().lstrip("$").upper()
        if not t:
            continue
        by_ticker.setdefault(t, []).append(rec)
    for rows in by_ticker.values():
        rows.sort(key=lambda r: r.get("first_seen") or "")
    _TRACKED_CACHE.update({"mtime": mtime, "by_mint": by_mint, "by_ticker": by_ticker})
    return by_mint, by_ticker


def _judge_kols(rec, kol_records):
    """rec の kol_ca+kol_ticker handle を kol_track_records と突合(evaluated>=2のみ・最大3人)。"""
    out, seen = [], set()
    handles = list(rec.get("kol_ca") or []) + list(rec.get("kol_ticker") or [])
    for h in handles:
        key = str(h).strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        kr = kol_records.get(key)
        if kr and (kr.get("evaluated") or 0) >= 2:
            out.append({"handle": kr.get("handle") or h, "death_rate": kr.get("death_rate")})
        if len(out) >= 3:
            break
    return out


def _judge_verdict_tracked(rec):
    """tracked.json のrecから決定的にverdict/headlineを出す(仕様の優先順位そのまま)。"""
    status = rec.get("status")
    gate = rec.get("gate") or ""
    last = rec.get("last") or {}
    has_kol = bool(rec.get("kol_ca")) or bool(rec.get("kol_ticker"))
    if status == "dead":
        return "DEAD", f"死亡確認(peak_mcap=${rec.get('peak_mcap') or 0:,.0f})"
    if "graduated" in gate and not has_kol and (last.get("reply_count") or 0) == 0:
        return "AVOID寄り", "graduated-but-empty型=最頻死型(KOL言及無し・reply0)"
    if "mcap" in gate:
        return "WATCH", "mcap勢い門通過=相対生存層"
    return "OBSERVED", f"追跡中(gate: {gate or '不明'})"


def _judge_lens(rec, verdict, kols):
    """★製品の芯(本人directive 2026-07-04): 結論でなく『見る目』を、しかも雑魚が単体で動けるレベルで渡す。
    本人「これを聞いて雑魚は何も分からない」→ 玄人語(板/traction)を平易に噛み砕き、"どこで・どう見分けて・だから何をするか"まで。
    hook=バッジ一言 / why=なぜ危険/期待か(専門語を説明) / how=自分でどう確かめるか(具体手順) / act=今すること。
    弱いトレーダーを強くする(winners-vs-losers)のが芯。決定的(状況→lens)。"""
    gate = rec.get("gate") or ""
    kname = f"@{kols[0].get('handle')}" if kols else ""
    kdr = (kols[0].get("death_rate") if kols else None)

    if verdict == "DEAD":
        return {
            "hook": "もう死んでる（値ほぼゼロ）。買う所じゃなく“学ぶ”所",
            "why": "この銘柄は結末が出た＝生きた教材。なぜ死んだか（誰も話さなかった/一瞬の噴きだった/大口が抜けた）を1つ覚えると、次に“生きてる同じ型”を見た時に避けられる。",
            "how": "1) DexScreenerで価格チャートを見る＝一度跳ねて即ゼロなら『噴いて即死』型\n2) その時Xで話題だったか思い出す＝無名のまま死んだなら『誰も見てない＝死ぬ』の実例",
            "act": "触らない。この“死に方の形”を1つ頭に入れて次に活かす",
        }
    if "graduated" in gate and verdict == "AVOID寄り":
        return {
            "hook": "卒業したのに誰も話してない＝大口が抜ける準備の典型。触るな",
            "why": "『卒業(graduated)』＝pump.funである程度買いが集まった印。なのにXで無言＝注目が集まった後に消えた＝作った側が売り抜ける直前のパターン。この型はうちの実測で10個中9個死ぬ。",
            "how": "自分で確かめる3つ:\n1) DexScreenerの「Txns（取引）」＝売りばかりなら もう抜けられてる\n2) 「Holders（保有者）」上位が数人で大半持ってたら危険（1人投げたら終わり）\n3) Xで銘柄名を検索→直近1時間に“普通の人”が話してるか。botの定型文だけなら噴きの噴き",
            "act": "触らない。入るなら『有名な人が本気で話し始めたら』まで待つ。来なきゃ見送りが正解",
        }
    if "mcap" in gate:
        return {
            "hook": "今まさに買われてる初期。ここから“伸びる”か“噴いて終わる”かの分かれ目",
            "why": "値が勢いよく上がってる＝誰かが実際に買ってる証拠で、うちの実測でも相対的に生き残りやすい層。ただし保証はない。分かれ目は『その勢いが続くか』と『買ってるのが本物の人かbotか』。",
            "how": "1) DexScreenerで買い（緑）が連続して分厚いか＝本物の需要\n2) Xで銘柄名検索→フォロワーの多い人が話し始めてるか＝勢いが続くサイン"
                   + (f"\n3) 今 {kname} が触れてる" + (f"（過去callは{kdr}%死＝話半分に）" if (kdr or 0) >= 60 else "（実績まずまず）") if kols else ""),
            "act": "乗るなら『小さく・早く利確ライン決めて』。勢いが止まって売りに変わったら即降りる",
        }
    if kols:
        weak = (kdr or 0) >= 60
        return {
            "hook": f"{kname} が推してる。乗る前に“この人は当ててる人か”を見る",
            "why": f"魔界は『何を』より『誰が言ってるか』。{kname} の過去のcallは実測で死{kdr}%。"
                   + ("＝平均以上に外す人＝この人が煽ってる＝むしろ警戒サイン。" if weak
                      else "＝悪くない。ただし件数が少なければ“まだ外してないだけ”かもしれない。過信しない。"),
            "how": "1) その人の過去ツイを遡る＝前に推した銘柄がどうなったか（大体死んでたら今回も期待薄）\n2) 言ってる事と実際の行動が合ってるか＝『選別しろ』と説きながら何十個も連発してたら口だけ",
            "act": "銘柄でなく“推してる人の実績”で決める。実績の悪い人のcallは逆に避ける材料",
        }
    return {
        "hook": "まだ判断材料が薄い。焦って乗る所じゃない",
        "why": "門は通ってるが決め手（KOLの後押し・強い勢い）がまだ無い。魔界は門を通っても大半が死ぬ＝“動いてるだけ”では乗る理由にならない。",
        "how": "1) 誰か実績あるKOLが拾い始めるか待つ\n2) DexScreenerで買いが本物か（Txns・Holders分散）\n3) 作った人（creator）が過去に連続でrugしてないか",
        "act": "様子見。上の1つでも“強い方”に振れたら初めて検討",
    }


def _judge_tracked_result(rec, kol_records):
    verdict, headline = _judge_verdict_tracked(rec)
    kols = _judge_kols(rec, kol_records)
    return {
        "verdict": verdict, "headline": headline, "lens": _judge_lens(rec, verdict, kols),
        "status": rec.get("status"),
        "peak_mcap": rec.get("peak_mcap"), "mcap_now": (rec.get("last") or {}).get("mcap_usd"),
        "gate": rec.get("gate"), "kols": kols,
    }


_DEX_CACHE = {}   # entity -> (ts, dict|None)  DexScreener即席enrichmentのTTLキャッシュ
_DEX_TTL = 90     # memeは値動きが速い→短命キャッシュ(本人「適切に」=鮮度優先)


def _dex_enrich(core, is_ca):
    """UNKNOWN銘柄の実mcap/年齢をDexScreenerの公開APIで即席取得。断定材料を取ってから喋る為(本人「$347Mを"分からん"は無能」)。
    ★tickerは同名別トークンが多数(ANSEM=pump.fun版$317M と 別の$248M版)→trenchツールなので
      solana×pump.fun版を最優先で選ぶ(本人「248じゃねぇ」=違うトークンを拾ってた根因)。
    返り値: {"mcap":float,"age_h":float|None,"name":str,"mint":str} or None。"""
    import time as _t
    key = core.lower()
    hit = _DEX_CACHE.get(key)
    if hit and _t.time() - hit[0] < _DEX_TTL:
        return hit[1]
    out = None
    try:
        if is_ca:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{core}"
        else:
            url = f"https://api.dexscreener.com/latest/dex/search?q={urllib.parse.quote(core)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=4).read())
        pairs = data.get("pairs") or []
        want = None if is_ca else core.lstrip("$").upper()
        cand = [p for p in pairs if not want or (p.get("baseToken") or {}).get("symbol", "").upper() == want]
        cand = cand or pairs

        def rank(p):
            addr = (p.get("baseToken") or {}).get("address", "") or ""
            liq = (p.get("liquidity") or {}).get("usd") or 0
            # 優先度: solana > pump.fun版(mintが"pump"終わり=魔界の本物) > 流動性
            return (p.get("chainId") == "solana", addr.endswith("pump"), liq)
        cand.sort(key=rank, reverse=True)
        if cand:
            p = cand[0]
            mcap = p.get("marketCap") or p.get("fdv")
            created = p.get("pairCreatedAt")
            age_h = (_t.time() - created / 1000) / 3600 if created else None
            if mcap:
                out = {"mcap": float(mcap), "age_h": age_h,
                       "name": (p.get("baseToken") or {}).get("name") or core,
                       "mint": (p.get("baseToken") or {}).get("address")}
    except Exception:  # noqa: BLE001
        out = None
    _DEX_CACHE[key] = (_t.time(), out)
    return out


def _judge_unknown(die_pct, core=None, is_ca=False):
    # ★精度(本人2026-07-04「$347Mを"分からん"は無能」): UNKNOWN(=うちの新規追跡に無い)でも、その場でmcap/年齢を取って
    #   確立済み/新規を判別し実のある読みを返す。取れない時だけ正直に「不明・自分で見分けろ」。
    enr = _dex_enrich(core, is_ca) if core else None
    if enr and enr.get("mcap"):
        mcap = enr["mcap"]
        age_h = enr.get("age_h")
        mstr = f"${mcap/1e6:.1f}M" if mcap >= 1e6 else f"${mcap/1e3:.0f}K"
        agestr = (f"{age_h/24:.0f}日前" if age_h and age_h >= 24 else f"{age_h:.0f}時間前" if age_h else "作成不明")
        # ★魔界基準のスケール(本人2026-07-04「2M超えてまだ小さいはキモい・200越えなんか見ない」):
        #   memeは大半が$100K以下で死ぬ。$1M超=既に生存者。$50M超=大型。$200M超=一握りのトップ級。
        #   TradFi脳($3M=小型)は誤り。生き残った銘柄を"小さい"と言わない。
        if mcap >= 2e8:   # トップ級(ANSEM/BONK級・魔界では稀)
            v, st = "ELITE", "elite"
            hook = f"魔界トップ級（{mstr}）。ここまで来る銘柄は一握り＝博打の枠はとうに抜けてる"
            why = f"memeは大半が$100K以下で死ぬ中、{mstr}は別次元。もう「死ぬ/生きる」の話じゃない。ここで効くのは『まだ上があるか・天井が近いか・高値掴みじゃないか』。"
            act = "初期博打の枠で見るな。天井/高値掴みリスクと、まだ買い需要が続いてるかで判断"
        elif mcap >= 3e7:  # 大型
            v, st = "MAJOR", "major"
            hook = f"大型（{mstr}）。大半が死ぬ魔界で相当生き残った側。小さくない"
            why = f"{mstr}まで育った＝需要と時間を生き延びた実力銘柄。死亡型の枠でなく、今の勢い・板の厚み・誰が今推してるかで読む。"
            act = "『死ぬ博打』でなく勢い・板・高値掴みで判断。乗るなら利確ライン先に決める"
        elif mcap >= 1e6:  # 生存者・中堅(★$1M超は"小さい"と言わない)
            v, st = "SURVIVOR", "survivor"
            hook = f"生き残った側（{mstr}）。ゴミの山を抜けて需要を掴んだ実在の銘柄"
            why = f"魔界は大半が$100K以下で消える。{mstr}まで来た時点で篩は抜けてる＝“小さい新規”ではない。ただ天井かはまだ分からない＝勢いが続くか失速かの分かれ目。"
            act = "勢い(出来高/買い売り比)と、今も実績KOLが推してるかで判断。伸びきってたら見送り"
        else:  # $1M未満＝まだ篩の中(ここが本当の初期/博打ゾーン)
            v, st = "EARLY", "early"
            hook = f"まだ篩の中（{mstr}・{agestr}）＝大半がここで消える博打ゾーン"
            why = f"魔界で$1M未満は初期＝門を通っても大半が死ぬ（base {die_pct}%）帯。伸びる前でもあり死ぬ前でもある＝一番分かれる所。"
            act = "小さく・利確ライン決めて。板が売りに変わったら即降り。実績KOL裏付け無しの噴きは見送り"
        return {"verdict": v, "headline": f"{mstr}・作成{agestr}",
                "lens": {"hook": hook, "why": why,
                         "how": "1) DexScreenerで直近の出来高と買い/売り比＝勢いが続くか失速か\n2) Xで“今”誰が話してるか＝実績KOLか遅れてきた養分か\n3) チャートで既に伸びきってないか（高値掴み）",
                         "act": act},
                "status": st, "peak_mcap": None, "mcap_now": mcap, "gate": None, "kols": []}
    # mcapが取れない＝本当に不明(正直に)
    return {"verdict": "UNKNOWN", "headline": "データ取得不可＝自分で確かめる",
            "lens": {"hook": "この銘柄の情報が取れない＝自分で見分けるしかない",
                     "why": "うちの追跡にもDexScreenerにも今すぐ出てこない＝判断材料ゼロ。ここで断定しないのが精度。焦って乗る所じゃない。",
                     "how": "DexScreenerかpump.funで直接検索:\n・時価総額デカい/作成が古い → 確立済み（勢い・板で見る）\n・小さい/数時間以内 → 新規の博打（門通過でも" + f"{die_pct}%" + "死ぬ前提）",
                     "act": "先に mcap と作成日で『新規の博打』か『確立済み』かを分けてから判断"},
            "status": None, "peak_mcap": None, "mcap_now": None, "gate": None, "kols": []}


def _judge_entity(raw, by_mint, by_ticker, ca_cache, kol_records, die_pct):
    core = raw.strip().lstrip("$")
    if _JUDGE_CA_RE.match(core):
        rec = by_mint.get(core)
        if rec is not None:
            return _judge_tracked_result(rec, kol_records)
        cached = ca_cache.get(core)
        if cached is not None:
            outcome = cached.get("outcome")
            mcap = cached.get("mcap")
            graduated = cached.get("graduated")
            if outcome == "dead":
                return {"verdict": "DEAD",
                        "headline": f"死亡確認(cache: mcap=${mcap or 0:,.0f})",
                        "status": "dead", "peak_mcap": None, "mcap_now": mcap,
                        "gate": None, "kols": []}
            if outcome == "alive":
                grad_note = "・graduated" if graduated else ""
                return {"verdict": "OBSERVED",
                        "headline": f"生存確認(cache: mcap=${mcap or 0:,.0f}{grad_note})",
                        "status": "alive", "peak_mcap": None, "mcap_now": mcap,
                        "gate": None, "kols": []}
            # outcome=="unknown" 等はこれ以上の情報が無い＝enrichで実mcapを取りに行く
        return _judge_unknown(die_pct, core=core, is_ca=True)
    # ticker: tracked.json を ticker(upper・$剥がし)で逆引き
    ticker = core.upper()
    rows = by_ticker.get(ticker)
    if rows:
        rec = rows[-1]  # first_seen 最新(昇順ソート済み配列の末尾)
        out = _judge_tracked_result(rec, kol_records)
        if len(rows) > 1:
            out["candidates"] = len(rows)
        return out
    return _judge_unknown(die_pct, core=core, is_ca=False)


def _judge(entities):
    by_mint, by_ticker = _tracked_data()
    ca_cache = _cached_state_json("ca_outcome_cache.json", {})
    kol_records = _cached_state_json("kol_track_records.json", {})
    br = _cached_state_json("base_rate.json", {})
    gp = br.get("gate_passed") or 1
    die_pct = round(100 * (br.get("died") or 0) / gp, 1)
    results = {}
    for raw in entities:
        results[raw] = _judge_entity(raw, by_mint, by_ticker, ca_cache, kol_records, die_pct)
    return {"ok": True, "results": results, "count": len(results)}


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
    # ★filter→take順(2026-07-11 本人「UIのシグナル欄に出てない」の真因): 検知botはAVOIDを高頻度で
    #   撃つため「末尾n件→AVOID除外」だと直近n件が全AVOIDになりCALL欄が恒常的に空になる
    #   (実測: VM 185件中 REVIEW 18件が全て20件窓の外に埋没)。AVOID除外してから最新n件を取る。
    rows = _tail_jsonl("detections.jsonl", n if include_avoids else max(n * 20, 400))
    if not include_avoids:
        rows = [r for r in rows if str(r.get("verdict", "")).upper() != "AVOID"]
    return rows[-n:][::-1]


def _append_detection(det):
    STATE.mkdir(parents=True, exist_ok=True)
    with open(STATE / "detections.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(det, ensure_ascii=False, separators=(",", ":")) + "\n")


def _normalize_learn(body):
    """1タップ学習の受信を正規化。銘柄/CA/KOL/本文/URLのどれかは要る(全部空は弾く)。"""
    if not isinstance(body, dict):
        raise ValueError("body must be object")
    ca = _clean_text(body.get("ca") or body.get("mint") or body.get("token_ca"), limit=120)
    ticker = _clean_text(body.get("ticker") or body.get("symbol"), limit=40).lstrip("$")
    handle = _clean_text(body.get("handle") or body.get("kol"), limit=40).lstrip("@")
    text = _clean_text(body.get("text") or body.get("tweet"), limit=2000)
    url = _clean_text(body.get("url"), limit=500)
    if not any([ca, ticker, handle, text]):
        raise ValueError("ca/ticker/handle/text のどれかは必須")
    ts = int(time.time())
    return {"id": f"learn_{time.strftime('%Y%m%d_%H%M%S', time.gmtime(ts))}_{uuid.uuid4().hex[:6]}",
            "ca": ca, "ticker": ticker.upper(), "handle": handle.lower(),
            "text": text, "url": url, "source": _clean_text(body.get("source"), "surf", 40),
            "ts": _now_iso(ts), "processed": False}


def _append_learn(item):
    STATE.mkdir(parents=True, exist_ok=True)
    with open(STATE / "learn_queue.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")


# --- A2: Live Activity push token(単一ユーザー)。brain/state/la_token.json に永続化 ---
def _la_load():
    return _state_json("la_token.json", {})


def _la_save(d):
    STATE.mkdir(parents=True, exist_ok=True)
    with open(STATE / "la_token.json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)


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
    # ★VOL/MC比(spyzer guide p.25: 出来高は原則mcapより大きいべき・<80%はほぼbundle)。
    #   ただし本人も「若いコインほど差が大きくあるべき」＝閾値は文脈依存→flagは若い銘柄(48h以内)のみ、
    #   それ以外は info として出すだけ(成熟銘柄で日次vol<mcapは正常＝一律適用は偽赤旗)。
    dx = _http_json(f"https://api.dexscreener.com/latest/dex/tokens/{ca}")
    pairs = (dx or {}).get("pairs") or []
    if pairs:
        p0 = max(pairs, key=lambda p: ((p.get("liquidity") or {}).get("usd") or 0))
        vol24 = ((p0.get("volume") or {}).get("h24") or 0)
        mc_dx = p0.get("marketCap") or p0.get("fdv") or 0
        ratio = round(100 * vol24 / mc_dx, 1) if mc_dx else None
        onchain["dex"] = {"vol24_usd": round(vol24), "mcap_usd": round(mc_dx),
                          "vol_mc_pct": ratio,
                          "liq_usd": round((p0.get("liquidity") or {}).get("usd") or 0)}
        age_h = None
        cts = pf.get("created_timestamp") if pf else None
        if cts:
            age_h = round((time.time() - cts / 1000) / 3600, 1)
            onchain["dex"]["age_h"] = age_h
        if ratio is not None and age_h is not None and age_h <= 48 and ratio < 80:
            flags.append(f"VOL/MC {ratio}%<80%＝bundle疑い(spyzer基準・launch {age_h}h)")
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
        # rate limit(公開保護): score は外部on-chain叩くので厳しめ・judge はnetwork無しなので緩め・他は既定
        if path0.startswith("/api/"):
            ip = _real_ip(self)
            if path0 == "/api/score":
                bucket, limit = "s", 15
            elif path0 == "/api/judge":
                bucket, limit = "j", 240
            else:
                bucket, limit = "g", 90
            if not _rate_ok(f"{ip}:{bucket}", limit):
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
            # ★push可視化(2026-07-10): Windowsのsynth push停止が3〜6日誰にも見えなかった事故の再発防止。
            #   last_commit=repo全体の鮮度(GHA込) / last_synth_push=家の合成push(auto-collect)の最終時刻＝
            #   ここが古い=「公開面が賢くなるのが止まってる」を外から検知できる。
            def _git_ts(*grep):
                try:
                    out = subprocess.run(["git", "log", "-1", "--format=%cI", *grep],
                                         capture_output=True, text=True, timeout=5, cwd=str(ROOT))
                    return out.stdout.strip() or None
                except Exception:
                    return None
            self._json(200, {"ok": True, "signal_backlog": h.get("signal_backlog"),
                             "raw_new": h.get("raw_new"), "single_source": h.get("single_source"),
                             "stale": h.get("stale"), "ts": h.get("ts"),
                             "wiki_pages": _retriever().N, "tracked_passed": br.get("gate_passed"),
                             "last_commit": _git_ts(),
                             "last_synth_push": _git_ts("--grep", "auto-collect")})
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
        # ★トークンサーフィン用インラインバッジ: network無し・ローカルstateのみで<50ms判定
        if path0 == "/api/judge":
            qs = parse_qs(urlparse(self.path).query)
            raw = qs.get("e", [""])[0]
            entities = [p.strip() for p in raw.split(",") if p.strip()]
            if not entities:
                self._json(400, {"ok": False, "error": "e が空(カンマ区切りentity、最大50)"})
                return
            if len(entities) > 50:
                self._json(400, {"ok": False, "error": "最大50個まで"})
                return
            try:
                self._json(200, _judge(entities))
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
        if path0 == "/api/learn":
            # ★1タップ学習(本人2026-07-04): サーフィン中の「これ学習しろ」を即キュー。
            #   人が選んだ=門を通した最強のキュレーション。重い合成は脳側(cron consumer)が裏で。
            if not _rate_ok(f"{_real_ip(self)}:learn", 120):
                self._json(429, {"ok": False, "error": "rate limit(learn)"})
                return
            try:
                body = _read_json_body(self, maxbytes=DETECTION_MAX_BODY)
                item = _normalize_learn(body)
                _append_learn(item)
                self._json(201, {"ok": True, "id": item["id"], "status": "queued"})
            except ValueError as e:
                self._json(400, {"ok": False, "error": str(e)[:200]})
            except Exception as e:
                print(f"[learn] error: {e}", file=sys.stderr)
                self._json(500, {"ok": False, "error": "internal error"})
            return
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
        if path0 == "/api/la/register":
            # push token登録は無害(pushできるだけ)＝認証なし。rate limitのみで保護。
            if not _rate_ok(f"{_real_ip(self)}:la_reg", 60):
                self._json(429, {"ok": False, "error": "rate limit(la/register)"})
                return
            try:
                body = _read_json_body(self, maxbytes=DETECTION_MAX_BODY)
            except OverflowError:
                self._json(413, {"ok": False, "error": "body too large"})
                return
            except Exception:
                self._json(400, {"ok": False, "error": "bad json body"})
                return
            if not isinstance(body, dict):
                body = {}
            token = _clean_text(body.get("token"), limit=500)
            if not token:
                self._json(400, {"ok": False, "error": "token が空"})
                return
            _la_save({"token": token, "count": 0, "updated": _now_iso()})
            self._json(200, {"ok": True})
            return
        if path0 == "/api/la/push":
            # /api/detect と同じ Bearer(DETECT_WEBHOOK_TOKEN) fail-closed パターン
            token_env = os.environ.get("DETECT_WEBHOOK_TOKEN", "").strip()
            if not token_env:
                if os.environ.get("DETECT_ALLOW_UNAUTH") != "1":
                    self._json(503, {"ok": False, "error": "DETECT_WEBHOOK_TOKEN未設定(fail-closed)。devで開けるなら DETECT_ALLOW_UNAUTH=1"})
                    return
            elif self.headers.get("Authorization", "").strip() != f"Bearer {token_env}":
                self._json(401, {"ok": False, "error": "unauthorized"})
                return
            if not _rate_ok(f"{_real_ip(self)}:la_push", 120):
                self._json(429, {"ok": False, "error": "rate limit(la/push)"})
                return
            try:
                body = _read_json_body(self, maxbytes=DETECTION_MAX_BODY)
            except OverflowError:
                self._json(413, {"ok": False, "error": "body too large"})
                return
            except Exception:
                self._json(400, {"ok": False, "error": "bad json body"})
                return
            if not isinstance(body, dict):
                body = {}
            la = _la_load()
            saved_token = la.get("token")
            if not saved_token:
                self._json(200, {"ok": False, "error": "no token registered"})
                return
            status = _clean_text(body.get("status"), default="idle", limit=40)
            hook = _clean_text(body.get("hook"), default=la.get("lastHook") or "", limit=500)
            bump = bool(body.get("bump"))
            count = int(la.get("count") or 0)
            if bump:
                count += 1
            la["count"] = count
            la["lastHook"] = hook
            la["updated"] = _now_iso()
            _la_save(la)
            content_state = {"status": status, "count": count, "lastHook": hook}
            try:
                ok, summary = send_live_activity_push(saved_token, content_state, event="update")
            except Exception as e:
                ok, summary = False, f"send_live_activity_push error: {e}"
            self._json(200, {"ok": ok, "apns": summary, "state": content_state})
            return
        if path0 == "/api/judge":
            if not _rate_ok(f"{_real_ip(self)}:j", 240):
                self._json(429, {"ok": False, "error": "rate limit — 少し待ってから再試行"})
                return
            try:
                body = _read_json_body(self, maxbytes=DETECTION_MAX_BODY)
            except OverflowError:
                self._json(413, {"ok": False, "error": "body too large"})
                return
            except Exception:
                self._json(400, {"ok": False, "error": "bad json body"})
                return
            entities = body.get("entities") if isinstance(body, dict) else None
            if not isinstance(entities, list):
                self._json(400, {"ok": False, "error": "entities(配列)が要る"})
                return
            entities = [str(e).strip() for e in entities if str(e).strip()]
            if not entities:
                self._json(400, {"ok": False, "error": "entities が空"})
                return
            if len(entities) > 50:
                self._json(400, {"ok": False, "error": "最大50個まで"})
                return
            try:
                self._json(200, _judge(entities))
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)[:300]})
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
