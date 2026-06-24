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
    # 各信頼KOLの直近 sources/x → CA言及
    found = {}  # ca -> {kols:set, }
    for p in glob.glob(str(SRC / "*.md")):
        base = os.path.basename(p)
        if "__" not in base:
            continue
        acct = base.split("__")[0].lower()
        if acct not in cred:
            continue
        if os.path.getmtime(p) < cutoff:
            continue
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for ca in CA_RE.findall(t):
            if ca.endswith("pump") or len(ca) >= 40:
                found.setdefault(ca, set()).add(cred[acct]["handle"])
    if not found:
        print(f"信頼KOL{len(cred)}人の直近{RECENT_DAYS}日に新規CA言及なし(=今は無風)。"); return
    # alive のものだけ surface(cache優先)
    rows = []
    for ca, kols in found.items():
        oc = cache.get(ca, {})
        if oc.get("outcome") == "dead":
            continue
        mc = oc.get("mcap")
        rows.append((ca, sorted(kols), mc, oc.get("outcome", "未照合")))
    rows.sort(key=lambda r: -(r[2] or 0))
    out = [f"🔭 credibility-gated discovery（信頼KOL{len(cred)}人の直近{RECENT_DAYS}日の現役言及）", ""]
    if not rows:
        out.append("生存中の新規言及なし(言及はあるが既に死/フェード)。")
    for ca, kols, mc, oc in rows[:8]:
        cinfo = " / ".join(f"@{k}({ktr[k.lower()]['death_rate']}%死)" for k in kols)
        out.append(f"・`{ca}`  mcap{('$'+format(mc,',')) if mc else '?'} [{oc}]")
        out.append(f"   ← {cinfo}  → /check で判定")
    out.append("")
    out.append("⚠️ 候補であってape推奨でない。track-recordは小N・現mcap近似のgate。各々 /check で精査を。")
    print("\n".join(out))


if __name__ == "__main__":
    main()
