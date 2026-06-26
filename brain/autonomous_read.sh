#!/bin/bash
# autonomous_read.sh — 自律する魔界脳の proactive read。聞かれてなくても trench を見て、
# genuine に notable な時だけ「今これ見とけ」を自分から push(本人2026-06-26「自律して動く脳に」)。
# ハードに gate(大半は沈黙)・dedup・spam回避。SYNTH_*同様 --strict-mcp-config。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${AUTO_READ_MODEL:-sonnet}"
CHAT="${AUTO_READ_CHAT:-7563521418}"
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 0; }

PULSE="$(python3 brain/launch_pulse.py 2>/dev/null | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in ("flow_count_nonscam","scam_reject_rate","theme_distribution","kol_standouts","traction_candidates","death_denominator")}, ensure_ascii=False)[:1400])
except Exception: print("{}")' 2>/dev/null || echo '{}')"
DISCOVER="$(python3 brain/discover.py 2>/dev/null | head -18)"
# ★A5学習: 過去の自律read仮説と、その後の実outcome を自己レビュー=自分の読みから学ぶ
PAST="$(python3 - <<'PY'
import json, os
hp = "brain/state/hypotheses.jsonl"
if not os.path.exists(hp):
    print("(過去の自律read仮説なし)"); raise SystemExit
try:
    td = json.load(open("brain/state/tracked.json", encoding="utf-8")); items = td if isinstance(td, list) else list(td.values())
    by = {x.get("mint"): x for x in items}
except Exception:
    by = {}
rows = [l for l in open(hp, encoding="utf-8") if l.strip()][-6:]
out = []
for l in rows:
    try: h = json.loads(l)
    except Exception: continue
    fates = []
    for ca in (h.get("cas") or [])[:3]:
        t = by.get(ca)
        fates.append(f"{ca[:6]}={'死' if (t and t.get('status')=='dead') else 'tracked' if t else '未追跡'}")
    out.append(f"[{h.get('date','?')}] 自分の読み: {(h.get('read') or '')[:90]} → 結果: {' '.join(fates) or '対象不明'}")
print("\n".join(out) or "(なし)")
PY
)"
# ★A4自律調査: discover候補の上位CAを自分で on-chain 掘る=aggregateでなく実tokenを調べた上で判断
INVESTIGATED="$(python3 - <<PY
import re, json, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
cas=re.findall(r"[1-9A-HJ-NP-Za-km-z]{32,44}", '''$DISCOVER''')[:3]
out=[]
for ca in cas:
    info={"ca":ca}
    try:
        c=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://frontend-api-v3.pump.fun/coins/{ca}",headers={"User-Agent":UA}),timeout=8).read())
        info.update({"sym":c.get("symbol"),"mcap":c.get("usd_market_cap"),"reply":c.get("reply_count"),"complete":c.get("complete")})
    except Exception: pass
    try:
        d=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://api.rugcheck.xyz/v1/tokens/{ca}/report",headers={"User-Agent":UA}),timeout=10).read())
        th=d.get("topHolders") or []
        info["top_pct"]=round(max((h.get("pct") or 0) for h in th),1) if th else None
        info["insiders"]=bool(d.get("insiderNetworks"))
    except Exception: pass
    out.append(info)
if out: print(json.dumps(out,ensure_ascii=False))
PY
)"
LEDGER="$(sed -n '/死亡台帳/,/浮いている型/p' wiki/concepts/rug-anatomy.md 2>/dev/null | tail -6)"
WORKLIST="$(grep -A18 '§1a' wiki/_worklist.md 2>/dev/null | head -18 || true)"

PROMPT="$(cat brain/autonomous_read_prompt.md)

## 現在の live state:
### launch-pulse(観測の流れ):
$PULSE
### discover(信頼KOLの現役plays):
$DISCOVER
### ★自分で掘った候補の on-chain(top holder集中/insider/mcap=aggregateでなく実態):
$INVESTIGATED
### 死亡台帳の直近:
$LEDGER
### hot discourse(worklist §1a):
$WORKLIST

## ★お前の過去の自律read仮説と、その後の実結果（学べ＝自分の読みが当たったか外れたか）:
$PAST
（過去外したパターンは今回割り引く・当てたパターンは型として強める＝自分の読みから学習する）"

OUT="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"

if printf '%s' "$OUT" | head -1 | grep -qi "NOTABLE:[[:space:]]*true"; then
  READ="$(printf '%s\n' "$OUT" | sed '1d')"
  H="$(printf '%s' "$READ" | { md5 2>/dev/null || md5sum | cut -d' ' -f1; })"
  LASTH="$(cat brain/state/last_auto_read.txt 2>/dev/null || echo none)"
  if [ "$H" = "$LASTH" ]; then echo "自律read: notable だが直近と同一→skip"; exit 0; fi
  printf '%s' "$H" > brain/state/last_auto_read.txt
  # ★A5: この仮説を log=次回 outcome と照合して学ぶ
  python3 - "$READ" <<'PY'
import sys, re, json
from datetime import datetime, timezone
read = sys.argv[1]
cas = re.findall(r"[1-9A-HJ-NP-Za-km-z]{32,44}", read)[:4]
rec = {"date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "cas": cas, "read": read[:200]}
with open("brain/state/hypotheses.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
PY
  TMP="$(mktemp)"; printf '🧠 自律read（聞かれてないけど、今これ見とけ）:\n\n%s' "$READ" > "$TMP"
  TOKEN="$(grep '^TG_WIKI_BOT_TOKEN=' .env | cut -d= -f2)"
  python3 - "$TOKEN" "$CHAT" "$TMP" <<'PY'
import sys, urllib.request, urllib.parse
token, chat, msgf = sys.argv[1], sys.argv[2], sys.argv[3]
msg = open(msgf, encoding="utf-8").read()[:3800]
data = urllib.parse.urlencode({"chat_id": chat, "text": msg}).encode()
try:
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=20)
    print("pushed")
except Exception as e:
    print(f"push err: {e}")
PY
  rm -f "$TMP"
  echo "自律read: NOTABLE→push済"
else
  echo "自律read: NOTABLE: false（沈黙＝正常）"
fi
