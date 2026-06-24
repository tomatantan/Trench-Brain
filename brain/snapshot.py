#!/usr/bin/env python3
"""
snapshot.py — 時系列の背骨。毎cycle 主要metricsを**dated append**で貯める（上書きしない）。

本人指摘「時系列が弱い」＋再監査「stale漸増」への対処。決定的・安価・LLM不使用・append-only＝芯安全(収集でない/backlog増やさない)。
死亡/跳躍台帳は既にappend式。これは"システム全体の状態"を日次snapshotして trajectory を取れるようにする＝
「先週から何が変わった/どれだけ速いか」に答える土台。launch-pulse の 変遷節 と /wiki がこれを読む。

出力: brain/state/pulse_history.jsonl に1行追記（直近を bounded 保持）。
"""
import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
HIST = STATE / "pulse_history.jsonl"
MAX_ROWS = 720  # ~日次なら2年分。bounded（無限肥大防止）

THEMES = {
    "AI/agent": ["ai", "gpt", "agent", "llm", "neural", "quant", "robot"],
    "animal/pet": ["dog", "cat", "inu", "shib", "pepe", "frog", "monke", "goose", "duck", "wif"],
    "political/news": ["trump", "elon", "biden", "maga", "gov", "war", "potus"],
    "IP/brand": ["gta", "pokemon", "mario", "amc", "nvidia", "tesla", "spacex", "spcx"],
    "finance/defi": ["sol", "eth", "btc", "usd", "defi", "yield", "stake", "perp", "dao"],
    "tech/meme": ["grok", "meme", "moon", "based", "chad", "gm"],
}


def _load(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def theme_of(name, sym):
    t = f"{name} {sym}".lower()
    for th, kws in THEMES.items():
        if any(k in t for k in kws):
            return th
    return "other"


def main():
    STATE.mkdir(parents=True, exist_ok=True)
    base = _load(STATE / "base_rate.json", {})
    # health(最新行)
    backlog = single = stale = None
    hf = STATE / "health.jsonl"
    if hf.exists():
        lines = [l for l in hf.read_text(encoding="utf-8").splitlines() if l.strip()]
        if lines:
            try:
                h = json.loads(lines[-1])
                backlog, single, stale = h.get("signal_backlog"), h.get("single_source"), h.get("stale")
            except Exception:
                pass
    # 非scam flow のテーマ分布(launch_queue)
    themes = Counter()
    qf = STATE / "launch_queue.jsonl"
    if qf.exists():
        for l in qf.read_text(encoding="utf-8", errors="replace").splitlines():
            l = l.strip()
            if not l:
                continue
            try:
                d = json.loads(l)
            except Exception:
                continue
            themes[theme_of(d.get("name", ""), d.get("symbol", ""))] += 1
    # 死亡/跳躍台帳の件数(合成済みの型蓄積)
    rug = ROOT / "wiki" / "concepts" / "rug-anatomy.md"
    lp = ROOT / "wiki" / "concepts" / "launchpad-economics.md"
    n_death = len(re.findall(r"^\| \[\[\$", rug.read_text(encoding="utf-8"), re.M)) if rug.exists() else None
    # watchlist 数
    wl = ROOT / "wiki" / "watchlist.md"
    n_wl = None
    if wl.exists():
        t = wl.read_text(encoding="utf-8")
        if "<!-- auto-candidates:start -->" in t:
            t = t[:t.index("<!-- auto-candidates:start -->")]
        n_wl = len(set(re.findall(r"\[\[@([A-Za-z0-9_]+)\]\]", t)))

    row = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "ts": int(time.time()),
        "mints_seen": base.get("mints_seen"), "gate_passed": base.get("gate_passed"),
        "graduated": base.get("graduated"), "died": base.get("died"),
        "signal_backlog": backlog, "single_source": single, "stale": stale,
        "themes": dict(themes.most_common()), "watchlist": n_wl, "death_ledger": n_death,
    }
    rows = []
    if HIST.exists():
        rows = [l for l in HIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    # 同日が末尾なら置換(1日1行=日次snapshot)、違えば追記
    if rows:
        try:
            if json.loads(rows[-1]).get("date") == row["date"]:
                rows = rows[:-1]
        except Exception:
            pass
    rows.append(json.dumps(row, ensure_ascii=False))
    rows = rows[-MAX_ROWS:]
    HIST.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"snapshot: {row['date']} died={row['died']} backlog={row['signal_backlog']} "
          f"stale={row['stale']} watchlist={row['watchlist']} themes={len(row['themes'])} → pulse_history({len(rows)}行)")


if __name__ == "__main__":
    main()
