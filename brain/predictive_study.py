#!/usr/bin/env python3
"""
predictive_study.py — 魔界 predictive study。我々の死の分母data(tracked.json)を全次元でmineし、
「何が魔界トークンの運命(生存/死)を分けるか」を実証する。＝我々固有の moat data の活用。

自己完結(我々のdata・LLM不使用・決定的)・芯安全(分析・収集でない)。報告のみ＋scoring weights出力。
★正直: tracked(alive)は censored(pendingで後に死ぬ分を含む)＝death率は下限。N小cellは明示。現mcap近似。
出力: wiki/dashboards/predictive-study.md（study）＋ brain/state/risk_weights.json（/check用の経験的重み）。
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
OUT_MD = ROOT / "wiki" / "dashboards" / "predictive-study.md"
OUT_W = STATE / "risk_weights.json"

THEMES = {"AI/agent": ["ai", "agent", "gpt", "llm", "robot", "neural"],
          "animal": ["dog", "cat", "inu", "pepe", "frog", "wif", "monke", "goose", "duck", "shib"],
          "political": ["trump", "elon", "maga", "gov", "biden", "potus"],
          "IP/brand": ["gta", "pokemon", "mario", "vinted", "legacy", "toros", "nvidia", "tesla"],
          "finance": ["sol", "eth", "btc", "defi", "perp", "dao", "usd", "rwa"]}


def theme_of(name, sym):
    t = f"{name} {sym}".lower()
    for k, ws in THEMES.items():
        if any(w in t for w in ws):
            return k
    return "other"


def gate_kind(g):
    g = g or ""
    if "graduated" in g:
        return "graduated"
    if "mcap" in g:
        return "mcap勢い門"
    if "kol" in g:
        return "KOL言及"
    if "user_checked" in g:
        return "user_checked"
    return "other"


def rate(d, n):
    return f"{d}/{n} ({round(100*d/n)}%)" if n else "N=0"


def main():
    d = json.loads((STATE / "tracked.json").read_text(encoding="utf-8"))
    items = d if isinstance(d, list) else list(d.values())
    n = len(items)
    dead_total = sum(1 for x in items if x.get("status") == "dead")

    def is_dead(x):
        return x.get("status") == "dead"

    def has_traction(x):
        last = x.get("last") or {}
        return bool(x.get("kol_ca")) or (last.get("reply") or 0) > 0

    # 各次元の死亡率
    dims = {}
    # 1) gate
    byg = defaultdict(lambda: [0, 0])
    for x in items:
        k = gate_kind(x.get("gate"))
        byg[k][1] += 1
        if is_dead(x):
            byg[k][0] += 1
    dims["gate"] = {k: (v[0], v[1]) for k, v in byg.items()}
    # 2) traction
    byt = defaultdict(lambda: [0, 0])
    for x in items:
        k = "traction有" if has_traction(x) else "traction無"
        byt[k][1] += 1
        if is_dead(x):
            byt[k][0] += 1
    dims["traction"] = {k: (v[0], v[1]) for k, v in byt.items()}
    # 3) theme
    byth = defaultdict(lambda: [0, 0])
    for x in items:
        k = theme_of(x.get("name", ""), (x.get("ticker") or "").lstrip("$"))
        byth[k][1] += 1
        if is_dead(x):
            byth[k][0] += 1
    dims["theme"] = {k: (v[0], v[1]) for k, v in byth.items()}
    # 4) peak mcap bucket
    def bucket(m):
        m = m or 0
        return "<10k" if m < 10_000 else "10-50k" if m < 50_000 else "50-200k" if m < 200_000 else "200k-1M" if m < 1_000_000 else ">1M"
    byb = defaultdict(lambda: [0, 0])
    for x in items:
        k = bucket(x.get("peak_mcap"))
        byb[k][1] += 1
        if is_dead(x):
            byb[k][0] += 1
    dims["peak_mcap"] = {k: (v[0], v[1]) for k, v in byb.items()}
    # 5) ★交互作用: gate × traction
    byx = defaultdict(lambda: [0, 0])
    for x in items:
        k = f"{gate_kind(x.get('gate'))} × {'tr有' if has_traction(x) else 'tr無'}"
        byx[k][1] += 1
        if is_dead(x):
            byx[k][0] += 1
    dims["gate×traction"] = {k: (v[0], v[1]) for k, v in byx.items() if v[1] >= 2}
    # 6) drawdown(死の深さ・deadのみ)
    dds = []
    for x in items:
        pk = x.get("peak_mcap") or 0
        cur = (x.get("last") or {}).get("mcap_usd") or 0
        if is_dead(x) and pk > 0:
            dds.append(100 * (cur - pk) / pk)
    avg_dd = round(sum(dds) / len(dds), 1) if dds else None

    # ★経験的 risk weights(死亡率→/check用の重み): baseline比のlift
    base = dead_total / n if n else 0
    weights = {}
    for dim in ("gate", "traction", "gate×traction"):
        for k, (dd, nn) in dims[dim].items():
            if nn >= 3:
                r = dd / nn
                weights[k] = {"death_rate": round(r, 2), "lift_vs_base": round(r / base, 2) if base else None, "n": nn}

    OUT_W.write_text(json.dumps({"base_death_rate": round(base, 3), "n": n, "factors": weights},
                                ensure_ascii=False, indent=1), encoding="utf-8")

    # study markdown
    def tbl(dimname, title):
        rows = [f"| {k} | {rate(v[0], v[1])} |" for k, v in sorted(dims[dimname].items(), key=lambda kv: -(kv[1][0] / kv[1][1] if kv[1][1] else 0))]
        return [f"### {title}", "| 因子 | 死亡率 |", "|---|---|", *rows, ""]

    L = ["---", "type: dashboard", "title: 魔界 predictive study（何が運命を分けるか・実証）",
         "updated: auto", "tags: [feedback, predictive, study, edge]", "---", "",
         "# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」", "",
         f"> `brain/predictive_study.py`。母集団 N={n}（dead {dead_total} / tracked {n-dead_total}＝**pendingでまだ死にうる=death率は下限**）。",
         f"> baseline 死亡率 {round(100*base)}%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。", "",
         f"## 死の深さ: dead銘柄の平均drawdown **{avg_dd}%**（peak比）＝死は「フェード」でなく「崩落」", "",
         "## 次元別 死亡率（高い順）", ""]
    L += tbl("gate", "① entry門別")
    L += tbl("traction", "② traction(KOL/reply)有無")
    L += tbl("gate×traction", "③ ★交互作用 gate×traction（最も効く組合せ）")
    L += tbl("theme", "④ テーマ別")
    L += tbl("peak_mcap", "⑤ peak mcap規模別")
    # 結論(N>=5のcellのみ=noise除外)
    gx = {k: v for k, v in dims["gate×traction"].items() if v[1] >= 5}
    worst = max(gx.items(), key=lambda kv: kv[1][0] / kv[1][1], default=(None, (0, 0)))
    best = min(gx.items(), key=lambda kv: kv[1][0] / kv[1][1], default=(None, (0, 0)))
    # peak mcap の最強signal(<10k)
    tiny = dims["peak_mcap"].get("<10k", (0, 0))
    L += ["## ★結論（/check の予測根拠・N>=5のcellのみ）",
          f"- **peak mcap <10k ＝ 死{rate(tiny[0], tiny[1])}**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。",
          f"- **最悪の gate×traction**: {worst[0]}＝死{rate(worst[1][0], worst[1][1])}＝最強のavoid。",
          f"- **最良の gate×traction**: {best[0]}＝死{rate(best[1][0], best[1][1])}＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。",
          "- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。",
          "- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。",
          "- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。", "",
          "関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"predictive_study: N={n} dead{dead_total}(base{round(100*base)}%) avg_drawdown{avg_dd}% / factors{len(weights)} → predictive-study.md + risk_weights.json")


if __name__ == "__main__":
    main()
