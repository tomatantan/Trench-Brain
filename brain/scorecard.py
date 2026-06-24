#!/usr/bin/env python3
"""
scorecard.py — 脳の"判定"の的中率＝「良くなってるか」の本当の物差し（本人指摘2026-06-24）。

これまでの計器(conformance/backlog/型hit-rate)は内部衛生。これは**脳の /check 判定そのもの**を実outcomeで採点：
- avoid と言った銘柄が実際に死んだか（=救えたか）
- ape寄りと言った銘柄が実際に生存したか（=勝ちを当てたか・難しい所）
- 確信度の calibration（高確信ほど当たるか）
時系列で見れば「脳が良くなってるか」が数字で分かる。決定的・LLM不使用・芯安全。

★正直: ①魔界は大半死ぬ＝avoid的中は base-rate で当たって当然＝**ape精度と base-rate超過が本当のテスト** ②直近checkは未決着(pending)＝除外 ③小N。
出力 wiki/dashboards/brain-scorecard.md。
"""
import json
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
CALLS = STATE / "brain_calls.jsonl"
OUT = ROOT / "wiki" / "dashboards" / "brain-scorecard.md"
RESOLVE_H = 18  # この時間 生存してたら "survived" 判定に算入(それ未満はpending)


def main():
    if not CALLS.exists():
        return
    td = json.loads((STATE / "tracked.json").read_text(encoding="utf-8"))
    items = td if isinstance(td, list) else list(td.values())
    by_ca = {x.get("mint"): x for x in items if x.get("mint")}
    base_dead = sum(1 for x in items if x.get("status") == "dead")
    base_n = len(items)
    base_rate = base_dead / base_n if base_n else 0

    calls = []
    for ln in CALLS.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            calls.append(json.loads(ln))
        except Exception:
            pass
    # 同一CAは最新の判定のみ
    latest = {}
    for c in calls:
        if c.get("ca"):
            latest[c["ca"]] = c
    now = time.time()

    # 採点
    rows = defaultdict(lambda: {"correct": 0, "wrong": 0, "pending": 0})  # verdict -> tally
    conf_tally = defaultdict(lambda: {"correct": 0, "wrong": 0})  # confidence -> tally
    for ca, c in latest.items():
        v = c.get("verdict")
        tok = by_ca.get(ca)
        if not tok:
            rows[v]["pending"] += 1  # tracked から消えた/未ingest
            continue
        status = tok.get("status")
        age_h = (now - c.get("ts", now)) / 3600
        if status == "dead":
            outcome = "died"
        elif age_h >= RESOLVE_H:
            outcome = "survived"  # 判定からRESOLVE_H時間 生存
        else:
            rows[v]["pending"] += 1
            continue
        # 正誤: avoid→died=正 / ape→survived=正 / watch=中立(集計のみ)
        if v == "avoid":
            ok = (outcome == "died")
        elif v == "ape":
            ok = (outcome == "survived")
        else:
            rows[v]["correct" if outcome == "died" else "wrong"] += 0  # watchは正誤つけない
            rows[v]["pending"] += 0
            continue
        rows[v]["correct" if ok else "wrong"] += 1
        if c.get("confidence") in ("高", "中", "低"):
            conf_tally[c["confidence"]]["correct" if ok else "wrong"] += 1

    def acc(t):
        n = t["correct"] + t["wrong"]
        return f"{t['correct']}/{n} ({round(100*t['correct']/n)}%)" if n else "未決着"

    av, ap = rows.get("avoid", {"correct": 0, "wrong": 0, "pending": 0}), rows.get("ape", {"correct": 0, "wrong": 0, "pending": 0})
    L = ["---", "type: dashboard", "title: 脳スコアカード（判定の的中＝良くなってるかの物差し）",
         "updated: auto", "tags: [scorecard, accuracy, feedback, edge]", "---", "",
         "# 脳スコアカード — /check 判定 vs 実outcome", "",
         f"> 脳の判定そのものの的中率（[[ape-or-avoid]] の実力）。総判定 {len(latest)}件。",
         f"> ★base 死亡率 {round(100*base_rate)}%＝**avoid的中はこれを超えて初めて価値**。ape的中こそ難しいテスト。直近{RESOLVE_H}h未満はpending除外・小N。", "",
         "## 判定種別の的中", "",
         "| 判定 | 的中 | pending | 読み |", "|---|---|---|---|",
         f"| **AVOID→死んだか** | {acc(av)} | {av['pending']} | base{round(100*base_rate)}%超で価値 |",
         f"| **APE→生存したか** | {acc(ap)} | {ap['pending']} | ★勝ちを当てる難テスト |", "",
         "## 確信度 calibration（高確信ほど当たるべき）", "",
         "| 確信度 | 的中 |", "|---|---|"]
    for cf in ("高", "中", "低"):
        L.append(f"| {cf} | {acc(conf_tally[cf])} |")
    L += ["", "## 読み方（本人）",
          "- **avoid的中 > base死亡率** なら「死を避ける」で価値が出てる。同水準なら無情報（base-rateと同じ）。",
          "- **ape的中** が高いほど「勝ちを見つける」力＝魔界で稼ぐ本体。ここが上がるのが「良くなってる」の核。",
          "- 高確信の的中 > 低確信 なら calibration が効いてる（自信の正しさ）。",
          "- **時系列で上記が上がれば脳は良くなってる**。判定が溜まるほど信頼できる（今は小N＝/checkを使うほど鮮明に）。",
          "", "関連: [[ape-or-avoid]] [[predictive-study]] [[feedback]] [[kol-track-records]]"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"scorecard: 総判定{len(latest)} / avoid {acc(av)} / ape {acc(ap)} / base死亡{round(100*base_rate)}% → brain-scorecard.md")


if __name__ == "__main__":
    main()
