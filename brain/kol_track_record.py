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
DEAD_MCAP = 12_000     # 現mcapがこれ未満＝死/フェード(近似)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
MAX_CA = 200           # 1回の lookup 上限(bounded)


def pf_mcap(ca):
    try:
        u = f"https://frontend-api-v3.pump.fun/coins/{ca}"
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10).read())
        return d.get("usd_market_cap"), bool(d.get("complete"))
    except Exception:
        return None, None


def main():
    # 1) KOL別 CA言及を集計(pump系CA)
    kol_cas = defaultdict(set)
    for p in glob.glob(str(SRC / "*.md")):
        base = os.path.basename(p)
        if "__" not in base:
            continue
        acct = base.split("__")[0]
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for ca in CA_RE.findall(t):
            if ca.endswith("pump") or len(ca) >= 40:
                kol_cas[acct].add(ca)
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
        if ca in cache:
            continue
        if looked >= MAX_CA:
            break
        mc, comp = pf_mcap(ca)
        if mc is None:
            cache[ca] = {"outcome": "unknown", "mcap": None}  # 鞍替え/old/非pump
        else:
            cache[ca] = {"outcome": ("dead" if mc < DEAD_MCAP else "alive"), "mcap": round(mc), "graduated": comp}
        looked += 1
        time.sleep(0.15)
    _tmp = CACHE.with_suffix(".json.tmp")  # atomic(2026-07-02 M2): kill時のtruncated cacheで全キャッシュ喪失を防ぐ
    _tmp.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    os.replace(_tmp, CACHE)

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

    # 4) 報告table(死亡率高い順=信頼性低い順・評価N>=2のみ)
    rows = sorted([r for r in recs.values() if r["evaluated"] >= 2],
                  key=lambda r: -(r["death_rate"] or 0))
    lines = ["---", "type: dashboard", "title: KOL track-record（call の生存率）", "updated: auto",
             "tags: [feedback, kol, track-record]", "---", "",
             "# KOL track-record — call の生死（/check の信頼性 edge）", "",
             "> `kol_track_record.py` が各KOLの歴史的CA言及(sources/x)の**現outcome**を照合。",
             "> ★近似: 現mcap<$12k=死/フェード。鞍替え/old=unknown除外。小N・傾向として読む（断定でない）。", "",
             "| KOL | 言及 | 評価 | 死 | 死亡率 | 読み |", "|---|---|---|---|---|---|"]
    for r in rows:
        verdict = ("⚠️call死多" if (r["death_rate"] or 0) >= 70 else
                   "平均的" if (r["death_rate"] or 0) >= 40 else "生存多(注目)")
        lines.append(f"| [[@{r['handle']}]] | {r['mentioned']} | {r['evaluated']} | {r['dead']} | "
                     f"{r['death_rate']}% | {verdict} |")
    lines += ["", f"> 評価N>=2のKOLのみ表示({len(rows)}人)。母集団は魔界=ほぼ死ぬ(base-rate)＝死亡率高は普通、",
              "> **相対的に低い者＝相対的にcallが残りやすい**と読む。[[launchpad-economics]] base-rate参照。"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"kol_track_record: {len(kol_cas)}KOL / {len(all_cas)}CA / lookup{looked}件 / 評価可{len(rows)}人 → kol-track-records.md")


if __name__ == "__main__":
    main()
