#!/usr/bin/env python3
"""
feedback.py — Feedbackループ。脳が使う「型」を**実outcomeで採点**する（決定的・LLM不使用・芯安全=収集でない）。

本人価値「AIは結果が戻らないと賢くならない」。死亡/跳躍台帳＋tracked.jsonの実outcomeから、
trench の主要仮説(型)の **hit-rate** を計算→「どの型が実際に当たるか」を脳が知る＝過学習を実データで潰す＋学習。
報告のみ(lint同様・自動でconceptを書換えない=CLAUDE.md Lint規約)。出力 wiki/dashboards/feedback.md。

★正直さ: 小N/pending/比較群欠如は隠さず「検証不能/弱い」と出す（断定はデータが出てから=芯）。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKED = ROOT / "brain" / "state" / "tracked.json"
OUT = ROOT / "wiki" / "dashboards" / "feedback.md"


def has_traction(x):
    last = x.get("last") or {}
    rep = last.get("reply") or 0
    kol = bool(x.get("kol_ca") or x.get("kol_ticker"))
    return rep > 0 or kol


def rate(dead, total):
    return f"{dead}/{total} ({100*dead//total if total else 0}%)" if total else "N=0"


def main():
    if not TRACKED.exists():
        return
    d = json.loads(TRACKED.read_text(encoding="utf-8"))
    items = d if isinstance(d, list) else list(d.values())
    dead = [x for x in items if x.get("status") == "dead"]
    alive = [x for x in items if x.get("status") == "tracked"]  # pending(未決着)
    n = len(items)

    # 型1: traction無し → 死ぬ？
    notr = [x for x in items if not has_traction(x)]
    notr_dead = [x for x in notr if x.get("status") == "dead"]
    tr = [x for x in items if has_traction(x)]
    tr_dead = [x for x in tr if x.get("status") == "dead"]

    # gate別 死亡率
    def gate_kind(x):
        g = x.get("gate", "")
        if "graduated" in g:
            return "graduated"
        if "mcap" in g:
            return "mcap勢い門"
        return "other"
    from collections import defaultdict
    gate_tot = defaultdict(int); gate_dead = defaultdict(int)
    for x in items:
        k = gate_kind(x); gate_tot[k] += 1
        if x.get("status") == "dead":
            gate_dead[k] += 1

    lines = [
        "---", "type: dashboard", "title: Feedback — 型の hit-rate（実outcome採点）",
        "updated: auto", "tags: [feedback, learning, hit-rate]", "---", "",
        "# Feedback — 脳の型を実outcomeで採点", "",
        "> `brain/feedback.py` が tracked.json の実死亡/生存から型のhit-rateを計算（報告のみ）。",
        "> 断定はデータが出てから。小N/pending/比較群欠如は正直に出す。", "",
        f"## 母集団: tracked {n}件（dead {len(dead)} / pending(tracked) {len(alive)}）", "",
        "## 型の hit-rate（観測）", "",
        "| 型(仮説) | 検証 | 判定 |",
        "|---|---|---|",
        f"| **traction無し→死ぬ** | 死亡 {rate(len(notr_dead), len(notr))}・残り{len(notr)-len(notr_dead)}はpending | "
        + ("支持(死多)" if len(notr) and len(notr_dead)/max(1,len(notr)) >= 0.4 else "観測中") + " |",
        f"| **traction有り→生存** | traction有り母集団 N={len(tr)}（死{len(tr_dead)}） | "
        + ("検証可" if len(tr) >= 5 else "**検証不能=比較群ほぼ無し**(KOL言及銘柄がtrackedに要る→watchlist拡張①が効く)") + " |",
    ]
    for k in ("graduated", "mcap勢い門", "other"):
        if gate_tot[k]:
            lines.append(f"| gate={k} の死亡率 | {rate(gate_dead[k], gate_tot[k])} | 観測 |")
    lines += [
        "", "## ⚠️ 計測の限界（正直に）",
        f"- pending(tracked)が{len(alive)}件＝まだ生死未決着＝hit-rateは暫定（決着で更新）。",
        "- **traction有り銘柄がほぼゼロ**＝「traction が生存を分ける」仮説の対照群が無い＝今は**反証も確証もできない**。",
        "  → ①watchlist拡張でKOL言及銘柄が tracked に入れば対照群ができ、初めて型が検証可能になる（①と②Feedbackは連動）。",
        "- 全件 同一launchpad/近時間帯＝独立性低い（[[rug-anatomy]]の注記と同じ留保）。", "",
        "関連: [[rug-anatomy]] 死亡台帳 / [[launchpad-economics]] 跳躍台帳・base rate",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"feedback: tracked{n}(dead{len(dead)}/pending{len(alive)}) traction無し死{rate(len(notr_dead),len(notr))} "
          f"traction有りN={len(tr)} → wiki/dashboards/feedback.md")


if __name__ == "__main__":
    main()
