#!/usr/bin/env python3
"""
kol_track_record.py — KOL の track-record を bootstrap。/check の killer edge＝「どのKOLのcallが死ぬか」。

問題: tracked.json の KOL-CA データは新規ingest分だけで薄い(track-recordが育つのに時間)。
これ: watchlist KOL の**歴史的CA言及**(sources/x)を集め、各トークンの**現outcome**(pump.fun mcapで生死)を照合し、
per-KOL の hit-rate(言及N / 現在死んでるM)を**今すぐ bootstrap** する。決定的・LLM不使用・収集でない(既存rawの分析)＝芯安全。
報告のみ(lint/feedback同様)。出力 wiki/dashboards/kol-track-records.md ＋ state(check_token/ask が読む)。

★正直: 「現mcapが低い＝死/フェード」の近似。peak/drawdownは未保存の歴史銘柄では取れない＝鞍替え(Raydium)等で
not-foundは unknown 扱い。小N・近似は明示。断定でなく傾向。
"""
import glob
import json
import os
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
STATE = ROOT / "brain" / "state"
OUT_MD = ROOT / "wiki" / "dashboards" / "kol-track-records.md"
OUT_JSON = STATE / "kol_track_records.json"
CACHE = STATE / "ca_outcome_cache.json"
CA_RE = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")
EVM_RE = re.compile(r"\b0x[a-fA-F0-9]{40}\b")  # 2026-07-12 EVM対応: KOLがEVM CAを言及するケースも拾う
DEAD_MCAP = 12_000     # 現mcapがこれ未満＝死/フェード(近似)。EVMも同一閾値で近似(chain別統計は未収集)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
MAX_CA = 200           # 1回の lookup 上限(bounded)
OUTCOME_TTL = 6 * 3600  # alive/unknown を6h毎に再確認(rug追従・transient回復)


def _fresh(entry):
    # dead は終端(track-record目的では固定)。alive/unknown は TTL 内なら再取得しない。
    if entry.get("outcome") == "dead":
        return True
    return (time.time() - entry.get("ts", 0)) < OUTCOME_TTL


def pf_mcap(ca):
    """3-tuple (mcap, complete, transient) を返す。
    transient=True → timeout/429/5xx 等の一時失敗 → cache しない・次runで再試行。
    transient=False → 成功 or genuine not-found(404) → cache してよい。
    """
    try:
        u = f"https://frontend-api-v3.pump.fun/coins/{ca}"
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10).read())
        return d.get("usd_market_cap"), bool(d.get("complete")), False
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None, False  # genuine not-found(鞍替え/非pump) → cacheしてよい
        return None, None, True       # 402/429/5xx 等 transient → cacheするな
    except Exception:
        return None, None, True       # URLError/timeout/その他 → transient扱い


def dex_mcap(ca):
    """EVM CA版のoutcome取得(2026-07-12)。pf_mcapはpump.fun専用=EVMは常に404になるので、
    dexscreenerの汎用tokensエンドポイントで代替。(mcap, transient, chain)の3-tuple
    (chain=最大流動性ペアのchainId。チェーン別base-rate(KOL言及コホート)の材料=2026-07-12 Phase2-lite)。"""
    try:
        u = f"https://api.dexscreener.com/latest/dex/tokens/{ca}"
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10).read())
        pairs = (d or {}).get("pairs") or []
        if not pairs:
            return None, False, None  # genuine not-found(ペア無し) → cacheしてよい
        p0 = max(pairs, key=lambda p: ((p.get("liquidity") or {}).get("usd") or 0))
        mc = p0.get("marketCap") or p0.get("fdv")
        return mc, False, p0.get("chainId")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, False, None
        return None, True, None
    except Exception:
        return None, True, None


def main():
    # 1) KOL別 CA言及を集計(pump系CA)
    kol_cas = defaultdict(set)
    for p in glob.glob(str(SRC / "*.md")):
        base = os.path.basename(p)
        if "__" not in base:
            continue
        acct = base.rsplit("__", 1)[0]  # rsplit: 末尾_のhandle(badattrading_)を切り落とさない
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for ca in CA_RE.findall(t):
            if ca.endswith("pump") or len(ca) >= 40:
                kol_cas[acct].add(ca)
        for ca in EVM_RE.findall(t):  # 2026-07-12: EVM CAはlowercaseに正規化(dedupe/cache keyをchecksummed表記で割らない)
            kol_cas[acct].add(ca.lower())
    all_cas = set().union(*kol_cas.values()) if kol_cas else set()

    # 2) 各CAの現outcome(cache優先・bounded)
    cache = {}
    if CACHE.exists():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    looked = 0
    for ca in all_cas:
        if ca in cache and _fresh(cache[ca]):
            continue
        if looked >= MAX_CA:
            break
        chain = None
        if ca.startswith("0x"):
            mc, transient, chain = dex_mcap(ca)
            comp = None  # graduated概念はEVMに無い
        else:
            mc, comp, transient = pf_mcap(ca)
        if transient:
            looked += 1  # bounded 維持のためカウントは進める。cache には書かない → 次runで再試行
            time.sleep(0.15)
            continue
        if mc is None:
            cache[ca] = {"outcome": "unknown", "mcap": None, "ts": time.time()}  # 鞍替え/old/非pump
        else:
            cache[ca] = {"outcome": ("dead" if mc < DEAD_MCAP else "alive"), "mcap": round(mc), "graduated": comp, "ts": time.time()}
            if chain:
                cache[ca]["chain"] = chain  # チェーン別base-rate(KOL言及コホート)の材料
        looked += 1
        time.sleep(0.15)
    _tmp = CACHE.with_suffix(".json.tmp")  # atomic(2026-07-02 M2): kill時のtruncated cacheで全キャッシュ喪失を防ぐ
    _tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    os.replace(_tmp, CACHE)

    # 2.5) ★チェーン別base-rate(Phase2-lite・2026-07-12): 「watchlist KOLが言及した0x CA」=門付きコホートの
    # 現生死をchain別に集計。Solanaのbase_rate.json(全mint観測)とは母集団が違う=「KOL言及コホート」と明示して使う。
    chains = defaultdict(lambda: {"n": 0, "dead": 0, "alive": 0})
    for ca, e in cache.items():
        ch = e.get("chain")
        if not ch or e.get("outcome") not in ("dead", "alive"):
            continue
        chains[ch]["n"] += 1
        chains[ch][e["outcome"]] += 1
    if chains:
        crates = {ch: {**v, "death_rate": round(100 * v["dead"] / v["n"])} for ch, v in chains.items() if v["n"]}
        _cb = STATE / "chain_base_rate.json"
        _cbt = _cb.with_suffix(".json.tmp")
        _cbt.write_text(json.dumps({"updated": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                                    "cohort": "watchlist KOLが言及した0x CA(門付き・全mint観測ではない)",
                                    "chains": crates}, ensure_ascii=False), encoding="utf-8")
        os.replace(_cbt, _cb)

    # 3) per-KOL hit-rate
    recs = {}
    for acct, cas in kol_cas.items():
        known = [cache[c] for c in cas if c in cache and cache[c]["outcome"] != "unknown"]
        dead = sum(1 for x in known if x["outcome"] == "dead")
        n = len(known)
        recs[acct.lower()] = {"handle": acct, "mentioned": len(cas), "evaluated": n,
                              "dead": dead, "alive": n - dead,
                              "death_rate": round(100 * dead / n) if n else None,
                              "unknown": len(cas) - n}
    OUT_JSON.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")

    # 4) 報告table(観測のみ・評価N>=2のみ。★2026-08-11: 死亡率を「信頼性edge/読み」として
    #    ランク付け・verdict化するのをやめた＝本人が2026-07-13/07-20/08-11と繰り返し明確に否定した設計
    #    (「死亡率とかどうでもいい・ゴミ指標」「魔界はほぼ全銘柄が死ぬからKOL単体の死亡率はbase rateと
    #    区別つかない」)。数値そのもの(観測)は残すが、順位付け・⚠️call死多/平均的/生存多のような
    #    verdict言葉は出さない(指針10=判断しない・観測の言葉で)。並びは評価N降順(データが厚い順)。
    rows = sorted([r for r in recs.values() if r["evaluated"] >= 2],
                  key=lambda r: -r["evaluated"])
    lines = ["---", "type: dashboard", "title: KOL track-record（言及した銘柄の現outcome・観測のみ）", "updated: auto",
             "tags: [feedback, kol, track-record]", "---", "",
             "# KOL track-record — 言及CAの現outcome（観測。信頼性ランキングではない）", "",
             "> `kol_track_record.py` が各KOLの歴史的CA言及(sources/x)の**現outcome**を照合。",
             "> ★近似: 現mcap<$12k=死/フェード。鞍替え/old=unknown除外。小N・傾向として読む（断定でない）。",
             "> ★死亡率はこのKOLの信頼度/callの質を示す指標ではない＝魔界はほぼ全銘柄が死ぬ母数なので個別",
             "> KOLの死亡率はbase rateとほぼ区別つかない(本人指摘2026-07-13/07-20/08-11)。ランキング・",
             "> verdict化はしない・数値は観測として置くだけ。", "",
             "| KOL | 言及 | 評価 | 死 | 死亡率(観測・参考程度) |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| [[@{r['handle']}]] | {r['mentioned']} | {r['evaluated']} | {r['dead']} | "
                     f"{r['death_rate']}% |")
    lines += ["", f"> 評価N>=2のKOLのみ表示({len(rows)}人・評価N降順)。母集団は魔界=ほぼ死ぬ(base-rate)。",
              "> [[launchpad-economics]] base-rate参照。"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"kol_track_record: {len(kol_cas)}KOL / {len(all_cas)}CA / lookup{looked}件 / 評価可{len(rows)}人 → kol-track-records.md")


if __name__ == "__main__":
    main()
