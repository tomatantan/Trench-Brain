#!/usr/bin/env python3
"""
launch_pulse.py — 流れてくる非scamローンチの"流れそのもの"を集約する(決定的・LLM不使用)。

本人意図(2026-06-23)「湯水のように流れてくるトークンを合成しつづける」を芯のまま実現する核:
個別ページ量産(=firehose/指針2違反)でなく、**流れを集約合成**＝「今 trench が何を発射してるか」を
常時更新される知識(launch pulse)にする。観測≠採用: 観測した全flowを集約、採用(個別page)は traction+KOL。

出力(stdout, JSON): 期間内の non-scam flow の {件数・scam率(stats)・テーマ分布・KOL言及standout・traction候補・新着サンプル}。
launch_synth.sh がこれを claude に渡し『launch-pulse concept』を更新＋standout採用。
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
QUEUE = STATE / "launch_queue.jsonl"
STATS = STATE / "launch_stats.json"
BASE = STATE / "base_rate.json"
WINDOW_H = float(sys.argv[1]) if len(sys.argv) > 1 else 6.0

# テーマ辞書(name/symbol のキーワードでセクター分布を出す)
THEMES = {
    "AI/agent": ["ai", "gpt", "agent", "llm", "neural", "quant", "model", "robot"],
    "animal/pet": ["dog", "cat", "inu", "shib", "pepe", "frog", "monke", "goose", "duck", "bear", "bull", "wif"],
    "political/news": ["trump", "elon", "biden", "maga", "gov", "fed", "war", "vote", "potus"],
    "IP/brand": ["gta", "pokemon", "mario", "disney", "marvel", "amc", "nvidia", "tesla"],
    "finance/defi": ["sol", "eth", "btc", "usd", "defi", "yield", "stake", "perp", "dao", "fi"],
    "tech/meme": ["grok", "x", "meme", "moon", "based", "chad", "gm"],
}


def theme_of(name, sym):
    t = f"{name} {sym}".lower()
    hits = [th for th, kws in THEMES.items() if any(k in t for k in kws)]
    return hits[0] if hits else "other"


def main():
    rows = []
    if QUEUE.exists():
        cut = time.time() - WINDOW_H * 3600
        for l in QUEUE.read_text(encoding="utf-8").splitlines():
            l = l.strip()
            if not l:
                continue
            try:
                d = json.loads(l)
            except Exception:
                continue
            if (d.get("detected_at") or 0) >= cut:
                rows.append(d)

    themes = Counter(theme_of(d.get("name", ""), d.get("symbol", "")) for d in rows)
    kol = [d for d in rows if d.get("kol")]
    # traction候補: reply が立ってる / mcap が乗ってる(出来立てで動意)
    traction = sorted([d for d in rows if (d.get("reply") or 0) > 0 or (d.get("usd_mcap") or 0) > 15000],
                      key=lambda d: ((d.get("reply") or 0), (d.get("usd_mcap") or 0)), reverse=True)
    stats = {}
    if STATS.exists():
        try:
            stats = json.loads(STATS.read_text())
        except Exception:
            stats = {}
    base = {}
    if BASE.exists():
        try:
            base = json.loads(BASE.read_text())
        except Exception:
            base = {}

    obs = stats.get("observed", 0)
    passed = stats.get("passed", 0)
    rejected = stats.get("rejected", 0)
    out = {
        "window_h": WINDOW_H,
        "flow_count_nonscam": len(rows),
        "observed_total": obs,
        "passed_total": passed,
        "scam_reject_total": rejected,
        "scam_reject_rate": round(rejected / max(1, stats.get("rugchecked", 1)), 3),
        "theme_distribution": dict(themes.most_common()),
        "kol_standouts": [{"sym": d.get("symbol"), "mint": d.get("mint"), "twitter": d.get("twitter")} for d in kol[:8]],
        "traction_candidates": [{"sym": d.get("symbol"), "reply": d.get("reply"), "mcap": d.get("usd_mcap"),
                                 "mint": d.get("mint")} for d in traction[:8]],
        "recent_samples": [{"sym": d.get("symbol"), "name": d.get("name"), "theme": theme_of(d.get("name", ""), d.get("symbol", ""))}
                           for d in sorted(rows, key=lambda d: -(d.get("detected_at") or 0))[:12]],
        "death_denominator": {"mints_seen": base.get("mints_seen"), "gate_passed": base.get("gate_passed"),
                              "graduated": base.get("graduated"), "died": base.get("died")},
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
