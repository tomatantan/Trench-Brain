#!/usr/bin/env python3
"""staged_intake.py — 承認済みwatchlist候補の「1人ずつ段階投入」(本人指示 2026-07-07「一気に投入ではなく1人ずつ」).

CORE-CHECK「1ソースずつ・ペース制御」の機械化。cron_collect.sh から毎サイクル呼ばれ、
brain/state/staged_intake_queue.json の先頭から N 人(既定1)だけを watchlist.md 本体
(=収集の門・[[@handle]] が collector に拾われる)へ昇格する。

門が2つ:
  1. 健康ゲート: health.jsonl の signal_backlog が直近で増加中なら投入しない(収集過多でscraper化する前に止まる)。
  2. 理解ゲート: onboarding profile(### 何者か)が entity に無い候補は昇格しない(理解→収集の順・2026-07-06指示)。
決定的・LLM不使用・冪等(queueが空なら何もしない)。STAGED_INTAKE_N でペース変更可。
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "brain" / "state" / "staged_intake_queue.json"
HEALTH = ROOT / "brain" / "state" / "health.jsonl"
WL = ROOT / "watchlist.md"
SECTION = "## spyzer情報網（段階投入・自動 staged_intake.py）"


def _health_ok():
    """直近2点の signal_backlog を比較。増加中なら False(投入見送り)。データ不足は True(投入可)。"""
    try:
        lines = [json.loads(x) for x in HEALTH.read_text(encoding="utf-8").strip().splitlines()[-2:]]
        if len(lines) < 2:
            return True, "health履歴不足=可"
        prev, last = lines[0].get("signal_backlog"), lines[1].get("signal_backlog")
        if isinstance(prev, (int, float)) and isinstance(last, (int, float)) and last > prev:
            return False, f"signal_backlog増加中({prev}→{last})=投入見送り"
        return True, f"backlog健全({prev}→{last})"
    except Exception as e:  # noqa: BLE001
        return True, f"health読取不能({type(e).__name__})=可"


def _has_profile(handle):
    ent = ROOT / "wiki" / "entities" / "players" / f"@{handle.lower()}.md"
    if not ent.exists():
        return False
    t = ent.read_text(encoding="utf-8", errors="replace")
    return "profile:start" in t and "### 何者か" in t


def main():
    n = int(os.environ.get("STAGED_INTAKE_N", "1"))
    if not QUEUE.exists():
        print("staged_intake: queue無し=何もしない")
        return
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    items = q.get("queue") or []
    if not items:
        print("staged_intake: queue空=完了済")
        return

    ok, why = _health_ok()
    if not ok:
        print(f"staged_intake: {why}")
        return

    wl = WL.read_text(encoding="utf-8")
    promoted, rest, skipped = [], [], []
    for it in items:
        h = it.get("handle", "")
        if len(promoted) >= n:
            rest.append(it)
            continue
        if not h or f"[[@{h}]]" in wl:
            skipped.append(h)  # 既に門内 or 不正=落とす(冪等)
            continue
        if not _has_profile(h):
            rest.append(it)  # 理解ゲート未通過=queueに残す(相対順維持)。後続のprofile済みを先に通す(詰まり防止)
            print(f"staged_intake: @{h} profile未作成=理解ゲート待ち(スキップ)")
            continue
        promoted.append(it)

    if not promoted:
        q["queue"] = rest
        QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"staged_intake: 昇格0(残{len(rest)})")
        return

    if SECTION not in wl:
        block = (f"\n{SECTION}\n"
                 "> 承認済み候補([[spyzer-complete-meme-coin-guide-fulltext]]の情報網)を**1人/サイクル**で段階投入"
                 "(本人指示2026-07-07)。健康ゲート=signal_backlog増加中は停止。理解ゲート=onboarding profile必須。\n\n"
                 "| handle | 枠 | followers(取得時) | weight |\n|---|---|---|---|\n")
        # 候補プールの直前に置く
        anchor = "## spyzer情報網 候補プール"
        wl = wl.replace(anchor, block + "\n" + anchor, 1) if anchor in wl else wl.rstrip() + "\n" + block
    for it in promoted:
        h, grp, fol = it["handle"], it.get("group", "main"), it.get("followers", "—")
        row = f"| [[@{h}]] | {grp} | {fol} | 中 |\n"
        # SECTION のテーブル末尾(次の空行/次セクションの前)に行を足す
        i = wl.find(SECTION)
        j = wl.find("\n## ", i + len(SECTION))
        j = j if j != -1 else len(wl)
        seg = wl[i:j].rstrip() + "\n" + row
        wl = wl[:i] + seg + wl[j:]
        print(f"staged_intake: 昇格 @{h} ({grp}/followers {fol})")

    WL.write_text(wl, encoding="utf-8")
    q["queue"] = rest
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"staged_intake: 昇格{len(promoted)}/残{len(rest)}")


if __name__ == "__main__":
    sys.exit(main())
