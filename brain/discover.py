#!/usr/bin/env python3
"""
discover.py — credibility-gated discovery。「信頼できるKOLが"今"何に乗ってるか」を surface。

本人が銘柄を hunt しなくても、**相対的に call が生き残るKOL**(kol_track_records の低死亡率)の
**直近の CA言及**(sources/x=既存収集)から、まだ生きてる銘柄を提示＝observe→/check→本人決定。
★門付き(信頼KOLのみ・全launchでない=firehoseでない・指針2)・read-only・決定的(LLM不使用)・既存data=安価=芯安全。
出力 stdout(bot /discover が telegram に返す)。

★正直: track-recordは小N・現mcap近似＝「信頼寄り」の弱いgate。surfaceは"候補"であって"ape推奨"でない。
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
DEATH_MAX = 45        # 死亡率これ以下のKOL＝相対的に信頼(gate)
EVAL_MIN = 3          # 評価N下限(小Nノイズ除外)


def main():
    try:
        ktr = json.load(open(STATE / "kol_track_records.json", encoding="utf-8"))
    except Exception:
        print("track-record未生成(brain/kol_track_record.py を先に)"); return
    cache = {}
    try:
        cache = json.loads((STATE / "ca_outcome_cache.json").read_text(encoding="utf-8"))
    except Exception:
        pass
    # 信頼KOL(gate): 死亡率<=45% かつ 評価>=3
    cred = {k: v for k, v in ktr.items()
            if v.get("death_rate") is not None and v["death_rate"] <= DEATH_MAX and v.get("evaluated", 0) >= EVAL_MIN}
    if not cred:
        print("信頼gate通過KOLなし(track-record蓄積待ち)"); return
    cutoff = time.time() - RECENT_DAYS * 86400
    # 各信頼KOLの直近 sources/x → CA言及(言及の新しさ mtime も記録=早期/recency優先用)
    found = {}  # ca -> {"kols":set, "mtime":float}
    for p in glob.glob(str(SRC / "*.md")):
        base = os.path.basename(p)
        if "__" not in base:
            continue
        acct = base.rsplit("__", 1)[0].lower()  # rsplit: 末尾_のhandleを切り落とさない
        if acct not in cred:
            continue
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
                e["kols"].add(cred[acct]["handle"])
                e["mtime"] = max(e["mtime"], mt)
    if not found:
        print(f"信頼KOL{len(cred)}人の直近{RECENT_DAYS}日に新規CA言及なし(=今は無風)。"); return
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
    out = [f"🔭 discovery（信頼KOL{len(cred)}人の直近{RECENT_DAYS}日の言及・**早期×直近を優先**）", ""]
    if not rows:
        out.append("生存中の新規言及なし(言及はあるが既に死/フェード=今は無風)。")
    for r in rows[:8]:
        cinfo = " / ".join(f"@{k}({ktr[k.lower()]['death_rate']}%死)" for k in r["kols"])
        mcs = ("$" + format(r["mc"], ",")) if r["mc"] else "?"
        out.append(f"・{r['stage']} `{r['ca']}`  mcap{mcs}")
        out.append(f"   ← {cinfo}  → /check で判定")
    out.append("")
    out.append("⚠️ 候補であってape推奨でない。早期×信頼KOL言及を上に出すが、track-recordは小N・mcap近似。各々 /check で精査。")
    print("\n".join(out))


if __name__ == "__main__":
    main()
