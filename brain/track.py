#!/usr/bin/env python3
"""
track.py — auto-synthesis パイプラインの「決定的(安い)層」。LLMは使わない。

設計(CLAUDE.md 憲法 + brain/INGEST.md):
  全mint観測(pump.fun launch feed) → 篩(安全門+勢い門) → PASS=TRACKED登録+合成(誕生)
    → 毎時: 安いウォッチャーが metric を取得 → 変化/死/graduation を検知
       → 誕生/変化/死 だけ「合成キュー」に積む（合成=LLM=エージェントの仕事）

★なぜ firehose でないか: 「全mint観測」は安いカウント＝**観測(篩の材料)**。
  wiki に入る(=合成される)のは篩通過分だけ＝**採用**。観測と採用は別。
★なぜ pump.fun か(DexScreenerでない): DexScreenerは DEXプール後(graduation後)しか見えず、
  bonding-curveの誕生と**そこで死ぬ大多数**を取りこぼす＝生存者バイアスが復活する。
  pump.fun feed は mint時点から見える＝死の分母を取れる。graduation後の metric は DexScreener。

metric source: frontend-api-v3.pump.fun（無料・keyless） / DexScreener（graduation後）。
状態: brain/state/tracked.json（gate通過の全ライフサイクル）/ base_rate.json（観測の分母・集計のみ）
      / synth_queue.json（エージェントが合成すべき 誕生/変化/死）。
"""
import json
import re
import sys
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
STATE = ROOT / "brain" / "state"
TRACKED = STATE / "tracked.json"
BASERATE = STATE / "base_rate.json"
QUEUE = STATE / "synth_queue.json"
UA = "Mozilla/5.0 (trench-brain)"

# ---- 篩の閾値（叩き台・緩めスタート。後で締める）----
PF_MCAP_MIN = 30_000     # 勢い門: usd_market_cap がこれ以上で通過(mint直後の~$4-5kから買われた証)
PF_REPLY_MIN = 50        # 勢い門: reply_count(社会的traction)がこれ以上で通過
# complete(graduation済) or KOL言及 は無条件で勢い門通過(下記)
# ---- 死(RETIRE)トリガ ----
DEATH_MCAP_FLOOR = 6_000   # mcap がこれ未満＝bonding curve 放棄/枯れ
DEATH_DRAWDOWN = 0.90      # peak mcap比 -90% 以下＝実質死
# ---- 「重要な変化」フラグ（=深い再合成に値する）----
CHG_MCAP = 0.40           # mcap が前回比 ±40% 超
CHG_REPLY = 30            # reply_count が前回比 +30 超(話題化)
HISTORY_MAX = 48
PF_SCAN_PAGES = 6         # launch feed を何ページ遡るか(1ページ=50)

TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(p, default):
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def save_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------- pump.fun adapter（launch feed・無料・keyless） ----------
def pumpfun_recent(pages=PF_SCAN_PAGES, page_size=50):
    """created_timestamp DESC で最近の mint を集める。"""
    out = []
    for i in range(pages):
        url = ("https://frontend-api-v3.pump.fun/coins?"
               f"offset={i*page_size}&limit={page_size}"
               "&sort=created_timestamp&order=DESC&includeNsfw=false")
        try:
            d = _get(url)
        except Exception as e:
            print(f"  pumpfun_recent p{i} fail: {e}", file=sys.stderr)
            break
        coins = d if isinstance(d, list) else (d.get("coins") or d.get("data") or [])
        if not coins:
            break
        out.extend(coins)
        time.sleep(0.25)
    return out


def pumpfun_coin(mint):
    try:
        d = _get(f"https://frontend-api-v3.pump.fun/coins/{mint}")
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def pf_metrics(c):
    if not c:
        return None
    return {
        "ts": now_iso(), "source": "pumpfun",
        "mint": c.get("mint"), "symbol": c.get("symbol"), "name": c.get("name"),
        "mcap_usd": c.get("usd_market_cap") or 0,
        "reply_count": c.get("reply_count") or 0,
        "complete": bool(c.get("complete")),
        "pool_address": c.get("pool_address"),
        "real_sol": c.get("real_sol_reserves") or 0,
        "created": c.get("created_timestamp"),
        "twitter": c.get("twitter"), "website": c.get("website"),
        "tokenized_agent": bool(c.get("tokenized_agent")),
        "banned": bool(c.get("is_banned")), "nsfw": bool(c.get("nsfw")),
    }


# ---------- 篩（gate）----------
def safety_ok(m):
    """安全門(最小): banned を弾く。※holder集中/sniper等の深いrug-anatomy判定は
    on-chain が要る→v2。ここは pump.fun フラグベースの最小門。"""
    if m is None:
        return False, "no-data"
    if m["banned"]:
        return False, "banned"
    return True, "ok"


def traction_ok(m, kol=False):
    if kol:
        return True, "kol"
    if m and m["complete"]:
        return True, "graduated"
    if m and m["mcap_usd"] >= PF_MCAP_MIN:
        return True, f"mcap>={PF_MCAP_MIN}"
    if m and m["reply_count"] >= PF_REPLY_MIN:
        return True, f"reply>={PF_REPLY_MIN}"
    return False, "weak"


def is_dead(m, peak_mcap):
    if m is None:
        return False
    mc = m["mcap_usd"]
    if m["complete"]:
        return False  # graduated は別物(DEX側で評価)、bonding死の対象外
    if mc and mc < DEATH_MCAP_FLOOR:
        return True
    if peak_mcap and mc and mc <= peak_mcap * (1 - DEATH_DRAWDOWN):
        return True
    return False


def material_change(m, prev):
    flags = []
    if m is None or prev is None:
        return flags
    if not prev.get("complete") and m.get("complete"):
        flags.append("GRADUATED")  # bonding→Raydium は最重要イベント
    if prev.get("mcap_usd"):
        d = (m["mcap_usd"] - prev["mcap_usd"]) / prev["mcap_usd"]
        if abs(d) > CHG_MCAP:
            flags.append(f"mcap{d*100:+.0f}%")
    if m.get("reply_count", 0) - prev.get("reply_count", 0) > CHG_REPLY:
        flags.append(f"reply+{m['reply_count']-prev['reply_count']}")
    return flags


def _cause(m, peak):
    if m["mcap_usd"] < DEATH_MCAP_FLOOR:
        return f"mcap枯れ(${m['mcap_usd']:.0f})"
    if peak and m["mcap_usd"] <= peak * (1 - DEATH_DRAWDOWN):
        return f"mcap -{DEATH_DRAWDOWN*100:.0f}% from peak(${peak:.0f})"
    return "?"


# ---------- discovery 補助: 既存収集 tweet を1パスで走査 ----------
# v2: KOL門は **CA(mint address)** で照合する（ticker照合は同名衝突で誤マッチ＝
#     $KRILLION 実演で検出したバグ）。ticker は弱シグナル(メタ情報)として保持のみ。
CA_RE = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")  # Solana base58 address


def scan_tweets(limit_files=600):
    """戻り値: (ticker_map{$TK:[acct]}, ca_map{CA:[acct]})。CAが強い門、tickerは弱メタ。"""
    tks, cas = {}, {}
    for p in sorted(SRC.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:limit_files]:
        try:
            t = p.read_text(encoding="utf-8")
        except Exception:
            continue
        parts = t.split("---", 2)
        if len(parts) < 3:
            continue
        fm, body = parts[1], parts[2]
        acct = next((l.split(":", 1)[1].strip() for l in fm.splitlines() if l.startswith("account:")), "")
        for tk in set(TICKER_RE.findall(body)):
            tks.setdefault(tk.upper(), set()).add(acct)
        for ca in set(CA_RE.findall(body)):
            cas.setdefault(ca, set()).add(acct)
    return ({k: sorted(v) for k, v in tks.items()},
            {k: sorted(v) for k, v in cas.items()})


# ---------- メイン ----------
def cmd_run(args):
    tracked = load_json(TRACKED, {})
    base = load_json(BASERATE, {"mints_seen": 0, "gate_passed": 0, "died": 0,
                                "graduated": 0, "last_created_ts": 0})
    queue = {"generated": now_iso(), "births": [], "changes": [], "deaths": []}
    kol_tk, kol_ca = scan_tweets()  # ticker_map(弱メタ), ca_map(強い門)

    # 1) 観測: pump.fun launch feed から新規 mint（前回以降）
    coins = pumpfun_recent()
    newest = base["last_created_ts"]
    fresh = [c for c in coins if (c.get("created_timestamp") or 0) > base["last_created_ts"]]
    print(f"launch feed: {len(coins)} 取得 / 新規 {len(fresh)}(前回以降)")

    for c in fresh:
        base["mints_seen"] += 1
        newest = max(newest, c.get("created_timestamp") or 0)
        m = pf_metrics(c)
        sym = (m["symbol"] or "").upper()
        ca_kol = m["mint"] in kol_ca   # ★v2: CA一致のみ強い門(ticker衝突を回避)
        s_ok, s_why = safety_ok(m)
        if not s_ok:
            continue
        t_ok, t_why = traction_ok(m, kol=ca_kol)
        if not t_ok:
            continue  # ← 観測はしたが採用しない(分母には入る。個別合成しない)
        # 採用 = TRACKED 登録 + 誕生キュー
        base["gate_passed"] += 1
        if t_why == "graduated":
            base["graduated"] += 1
        key = m["mint"]   # ★状態keyは mint(一意)。ticker は衝突する(別mintの同名)ので表示用フィールドに。
        disp = "$" + sym if sym else m["mint"][:6]
        tracked[key] = {
            "ticker": disp, "mint": m["mint"], "name": m["name"],
            "first_seen": now_iso(), "status": "tracked",
            "peak_mcap": m["mcap_usd"],
            "kol_ca": kol_ca.get(m["mint"], []),       # 強い門(CA一致した言及アカ)
            "kol_ticker": kol_tk.get("$" + sym, []),   # 弱メタ($同名言及・自動通過しない)
            "gate": f"safety:{s_why}/traction:{t_why}",
            "tokenized_agent": m["tokenized_agent"],
            "last": m, "history": [m], "last_synth": None, "outcome": None,
        }
        queue["births"].append({"ticker": disp, "mint": m["mint"], "name": m["name"],
                                "gate": tracked[key]["gate"], "kol_ca": tracked[key]["kol_ca"],
                                "kol_ticker": tracked[key]["kol_ticker"], "metrics": m})
    base["last_created_ts"] = newest
    print(f"births(門通過): {len(queue['births'])} / mints_seen累計 {base['mints_seen']} "
          f"/ gate_pass累計 {base['gate_passed']}")

    # 2) watch: TRACKED を pump.fun で再取得（安いウォッチャー＝diff のみ）
    alive = [k for k, v in tracked.items() if v.get("status") == "tracked" and v.get("mint")]
    for k in alive:
        v = tracked[k]
        m = pf_metrics(pumpfun_coin(v["mint"]))
        if m is None:
            continue
        prev = v.get("last")
        if (m["mcap_usd"] or 0) > (v.get("peak_mcap") or 0):
            v["peak_mcap"] = m["mcap_usd"]
        disp = v.get("ticker", k[:6])
        if is_dead(m, v.get("peak_mcap")):
            v["status"], v["outcome"], v["died_at"], v["last"] = "dead", "died", now_iso(), m
            base["died"] += 1
            queue["deaths"].append({"ticker": disp, "mint": k, "peak_mcap": v.get("peak_mcap"),
                                    "last": m, "cause": _cause(m, v.get("peak_mcap"))})
        else:
            flags = material_change(m, prev)
            if flags:
                if "GRADUATED" in flags:
                    v["outcome"] = "graduated"
                queue["changes"].append({"ticker": disp, "mint": k, "flags": flags,
                                         "prev_mcap": prev.get("mcap_usd"), "now": m})
            v["last"] = m
            v["history"] = (v.get("history", []) + [m])[-HISTORY_MAX:]
        time.sleep(0.2)
    print(f"watch: {len(alive)} tracked → {len(queue['changes'])} 変化 / {len(queue['deaths'])} 死")

    save_json(TRACKED, tracked)
    save_json(BASERATE, base)
    save_json(QUEUE, queue)
    n = len(queue["births"]) + len(queue["changes"]) + len(queue["deaths"])
    pr = base["gate_passed"] / base["mints_seen"] if base["mints_seen"] else 0
    print(f"synth_queue → {n} 件合成待ち。base rate: gate通過 {pr*100:.1f}% "
          f"({base['gate_passed']}/{base['mints_seen']}), 死{base['died']} grad{base['graduated']}")
    print("次: エージェントが synth_queue を読み 誕生/変化/死 を合成(brain/INGEST.md)。")


def cmd_status(args):
    tracked = load_json(TRACKED, {})
    by = {}
    for v in tracked.values():
        by[v.get("status", "?")] = by.get(v.get("status", "?"), 0) + 1
    base = load_json(BASERATE, {})
    q = load_json(QUEUE, {})
    print(f"tracked: {len(tracked)} {by}")
    print(f"base_rate: {base}")
    if q:
        print(f"queue: 誕生{len(q.get('births',[]))} 変化{len(q.get('changes',[]))} 死{len(q.get('deaths',[]))}")


def main():
    ap = argparse.ArgumentParser(description="auto-synthesis 決定的層(観測→篩→watch→合成キュー)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("run", help="launch feed→篩→watch を1サイクル→synth_queue 出力")
    sub.add_parser("status", help="現状サマリ")
    a = ap.parse_args()
    cmd_status(a) if a.cmd == "status" else cmd_run(a)


if __name__ == "__main__":
    main()
