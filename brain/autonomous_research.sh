#!/bin/bash
# autonomous_research.sh — 自律する魔界researcher脳。自分で仮説を立て→tracked dataで検証→
# 確証/反証(=ダメだった)/不確定 を正直に評価→学びを log＋確証は concept に焼く＝試行錯誤で corpus が賢くなる
# (本人2026-06-26「考える→チェック→ダメだったか→試行錯誤と合成・収集」)。--strict-mcp-config。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${RESEARCH_MODEL:-sonnet}"
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 0; }

DATA="$(python3 - <<'PY'
import json
d = json.load(open("brain/state/tracked.json", encoding="utf-8")); items = d if isinstance(d, list) else list(d.values())
TH = {"AI": ["ai","agent","gpt","llm"], "animal": ["dog","cat","inu","pepe","wif","frog","monke"], "political": ["trump","elon","maga"], "finance": ["sol","eth","btc","defi","perp"], "IP": ["gta","pokemon","mario","vinted","toros"]}
def theme(n, s):
    t = f"{n} {s}".lower()
    return next((k for k, ws in TH.items() if any(w in t for w in ws)), "other")
import random as _r
dead=[x for x in items if x.get("status")=="dead"]; alive=[x for x in items if x.get("status")=="tracked"]
items=(dead[:60]+alive[:60])  # sample(生死mix・大prompt回避)
rows = []
for x in items:
    last = x.get("last") or {}
    rows.append({"sym": x.get("ticker"), "gate": (x.get("gate") or "").split("/")[-1], "kol": bool(x.get("kol_ca")),
                 "theme": theme(x.get("name",""), (x.get("ticker") or "")), "peak": x.get("peak_mcap"),
                 "cur": last.get("mcap_usd"), "creator": (last.get("creator") or x.get("creator") or "")[:8],
                 "status": x.get("status")})
print(json.dumps(rows, ensure_ascii=False))
PY
)"
FEEDBACK="$(sed -n '/型の hit-rate/,/計測の限界/p' wiki/dashboards/feedback.md 2>/dev/null | head -18)"
PAST="$(python3 - <<'PY'
import json, os
hp = "brain/state/research_log.jsonl"
if not os.path.exists(hp): print("(過去research無し)"); raise SystemExit
for l in [x for x in open(hp, encoding="utf-8") if x.strip()][-10:]:
    try:
        d = json.loads(l); print(f"- {d.get('hypothesis','')[:80]} → {d.get('result','')[:50]}")
    except Exception: pass
PY
)"

PROMPT="$(cat brain/autonomous_research_prompt.md)

## tracked データ(各銘柄の gate/traction/theme/peak/現mcap/creator/生死):
$DATA

## 既知の型(feedback・これと重複しない仮説を):
$FEEDBACK

## 過去の自分のresearch(再検証を避ける):
$PAST"

OUT="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
# parse(multi-line field対応)＋log＋確証なら concept に焼く を一本化
TMP="$(mktemp)"; printf '%s' "$OUT" > "$TMP"
python3 - "$TMP" <<'PY'
import sys, re, json
from datetime import datetime, timezone
out = open(sys.argv[1], encoding="utf-8").read()
def field(name):
    m = re.search(rf"^{name}\s*[:：]\s*(.*?)(?=^\s*(?:HYPOTHESIS|TEST|RESULT|LEARNING|TARGET)\s*[:：]|\Z)",
                  out, re.S | re.M | re.I)
    return (m.group(1).strip() if m else "")
hyp, res, learn, target = field("HYPOTHESIS"), field("RESULT"), field("LEARNING"), field("TARGET")
target = re.sub(r"[\s（(].*$", "", target).strip()  # 概念名だけ
if not hyp:
    print("research: parse不可→skip"); raise SystemExit
rec = {"date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "hypothesis": hyp[:200],
       "result": res[:120], "learning": learn[:300], "target": target}
open("brain/state/research_log.jsonl", "a", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False) + "\n")
print(f"research: {res[:50]} — {hyp[:70]}")
# 確証だけ TARGET 概念に焼く(反証/不確定は log のみ＝「効かない」記録)
import os
if target and target != "NONE" and "確証" in res:
    cf = f"wiki/concepts/{target}.md"
    if os.path.exists(cf):
        t = open(cf, encoding="utf-8").read()
        if "## ★自律research の学び" not in t:
            t += "\n## ★自律research の学び\n"
        t += f"- ({rec['date']}) {hyp[:120]} ＝ {learn[:160]}\n"
        open(cf, "w", encoding="utf-8").write(t)
        print(f"→ {target} に確証された学びを焼いた")
PY
rm -f "$TMP"
