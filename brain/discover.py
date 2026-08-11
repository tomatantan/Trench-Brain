#!/usr/bin/env python3
"""
discover.py — watchlist-gated discovery。「watchlist KOLが"今"何に乗ってるか」を surface。

本人が銘柄を hunt しなくても、**watchlist(門)のKOL**の**直近の CA言及**(sources/x=既存収集=
収集の時点で既にwatchlist限定)から、まだ生きてる銘柄を提示＝observe→/check→本人決定。
★門付き(watchlist=収集時点で既に限定・全launchでない=firehoseでない・指針2)・read-only・
決定的(LLM不使用)・既存data=安価=芯安全。出力 stdout(bot /discover が telegram に返す)。

★2026-08-11修正: 以前は kol_track_records の死亡率<=45% を追加のcredibility gateにしていたが、
死亡率をKOLの信頼度/信号の質として使うのは本人が2026-07-13/07-20/08-11と繰り返し明確に否定した
設計(「死亡率とかどうでもいい・正しいのかもわからんゴミ指標」「魔界はほぼ全銘柄が死ぬから個別
KOLの死亡率はbase rateと区別つかない」)。実データでも動いた銘柄の大半がKOL言及ゼロ＝KOL言及/
死亡率は動く前のsignalとして機能してない([[no-death-rates-no-kol-mentions]]系の既存結論)。
gateは「watchlistに載ってるか」だけで十分(それ自体が本物のキュレーション＝指針2)。死亡率での
追加選別・追加表示は廃止。
★正直: surfaceは"候補"であって"ape推奨"でない。
"""
import glob
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
STATE = ROOT / "brain" / "state"
CA_RE = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")
RECENT_DAYS = 4
DEAD_MCAP = 12_000


def main():
    cache = {}
    try:
        cache = json.loads((STATE / "ca_outcome_cache.json").read_text(encoding="utf-8"))
    except Exception:
        pass
    cutoff = time.time() - RECENT_DAYS * 86400
    # 各watchlistアカウントの直近 sources/x → CA言及(言及の新しさ mtime も記録=早期/recency優先用)
    # sources/x は収集時点で既にwatchlist限定＝ここでの追加credibility gateは不要(指針2で足りてる)。
    found = {}  # ca -> {"kols":set, "mtime":float}
    for p in glob.glob(str(SRC / "*.md")):
        base = os.path.basename(p)
        if "__" not in base:
            continue
        acct = base.rsplit("__", 1)[0]  # rsplit: 末尾_のhandleを切り落とさない
        mt = os.path.getmtime(p)
        if mt < cutoff:
            continue
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for ca in CA_RE.findall(t):
            if ca.endswith("pump") or len(ca) >= 40:
                e = found.setdefault(ca, {"kols": set(), "mtime": 0})
                e["kols"].add(acct)
                e["mtime"] = max(e["mtime"], mt)
    if not found:
        print(f"watchlist KOLの直近{RECENT_DAYS}日に新規CA言及なし(=今は無風)。"); return
    # ★早期ape機会を優先: alive かつ pump-meme範囲(既にpump済の大型=遅い、は降格)。recency(直近言及)順。
    PUMP_CEIL = 2_000_000   # これ超=既にpump済/majors寄り=魔界の早期apeでない→末尾/除外寄り
    rows = []
    for ca, e in found.items():
        oc = cache.get(ca, {})
        if oc.get("outcome") == "dead":
            continue
        mc = oc.get("mcap")
        # stage: 早期(<50k)/育成($50k-500k)/伸長($500k-2M)/pump済(>2M=遅い)
        if mc is None:
            stage = "未照合"
        elif mc < 50_000:
            stage = "🌱早期"
        elif mc < 500_000:
            stage = "🔼育成中"
        elif mc < PUMP_CEIL:
            stage = "📈伸長"
        else:
            stage = "🏔️pump済(遅い)"
        rows.append({"ca": ca, "kols": sorted(e["kols"]), "mc": mc, "mtime": e["mtime"], "stage": stage,
                     "late": (mc or 0) >= PUMP_CEIL})
    # 並び: 早期(not late)を上 → mcap照合済(alive確認)を未照合より上 → recency(直近言及)順
    rows.sort(key=lambda r: (r["late"], r["mc"] is None, -r["mtime"]))
    out = [f"🔭 discovery（watchlist KOLの直近{RECENT_DAYS}日の言及・**早期×直近を優先**）", ""]
    if not rows:
        out.append("生存中の新規言及なし(言及はあるが既に死/フェード=今は無風)。")
    for r in rows[:8]:
        cinfo = " / ".join(f"@{k}" for k in r["kols"])
        mcs = ("$" + format(r["mc"], ",")) if r["mc"] else "?"
        out.append(f"・{r['stage']} `{r['ca']}`  mcap{mcs}")
        out.append(f"   ← {cinfo}  → /check で判定")
    out.append("")
    out.append("⚠️ 候補であってape推奨でない。早期×直近言及を上に出すが、誰が言及したかは信頼度の証明でない。各々 /check で精査。")
    print("\n".join(out))


if __name__ == "__main__":
    main()
