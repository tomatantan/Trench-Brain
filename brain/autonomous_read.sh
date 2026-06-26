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
LEDGER="$(sed -n '/死亡台帳/,/浮いている型/p' wiki/concepts/rug-anatomy.md 2>/dev/null | tail -6)"
WORKLIST="$(grep -A18 '§1a' wiki/_worklist.md 2>/dev/null | head -18 || true)"

PROMPT="$(cat brain/autonomous_read_prompt.md)

## 現在の live state:
### launch-pulse(観測の流れ):
$PULSE
### discover(信頼KOLの現役plays):
$DISCOVER
### 死亡台帳の直近:
$LEDGER
### hot discourse(worklist §1a):
$WORKLIST"

OUT="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"

if printf '%s' "$OUT" | head -1 | grep -qi "NOTABLE:[[:space:]]*true"; then
  READ="$(printf '%s\n' "$OUT" | sed '1d')"
  H="$(printf '%s' "$READ" | { md5 2>/dev/null || md5sum | cut -d' ' -f1; })"
  LASTH="$(cat brain/state/last_auto_read.txt 2>/dev/null || echo none)"
  if [ "$H" = "$LASTH" ]; then echo "自律read: notable だが直近と同一→skip"; exit 0; fi
  printf '%s' "$H" > brain/state/last_auto_read.txt
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
