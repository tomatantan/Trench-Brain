#!/bin/bash
# check_token.sh — 魔界スクリーニング。CA(or pump.fun URL)を投げたら ape/avoid を判定。
# ★v2(2026-06-24 本人「on-chainしか見てない=LLM wikiである理由ない」批判への fix):
#   LLM Wiki の固有価値＝**合成知識**を lead に据える。on-chain(RugCheck)は commodity な足切りに降格。
#   wiki-edge: ①shill KOL の track-record(過去callの生存率=tracked.jsonから計算・on-chainツールに出せない)
#             ②KOL の entity(信頼性/profile) ③死亡/跳躍台帳の具体型 ④Feedbackの型hit-rate ⑤cross-source
#   corpus接続ゼロ(無名KOL/未言及)なら「wiki signal無し=on-chainのみ=低edge」と正直に出す。
# read-only・--strict-mcp-config。bot /check $CA。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${CHECK_MODEL:-sonnet}"
ARG="${*:-}"
CA="$(printf '%s' "$ARG" | grep -oE '[1-9A-HJ-NP-Za-km-z]{32,44}' | head -1)"
[ -n "$CA" ] || { echo "CA(mint address) か pump.fun URL を渡して: bash brain/check_token.sh <CA>" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

# (1) live on-chain + KOL track-record + cross-source を収集(python)
DATA="$(python3 - "$CA" <<'PY'
import json, sys, urllib.request, glob, re, os
CA = sys.argv[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
def get(u, t=12):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=t).read())

out = {"CA": CA}
sym = name = creator = None
# --- pump.fun ---
try:
    c = get(f"https://frontend-api-v3.pump.fun/coins/{CA}", 10)
    sym = (c.get("symbol") or ""); name = (c.get("name") or ""); creator = c.get("creator")
    out["pump"] = {"symbol": sym, "name": name, "usd_mcap": c.get("usd_market_cap"),
                   "reply": c.get("reply_count"), "complete": c.get("complete"),
                   "twitter": c.get("twitter"), "website": c.get("website")}
except Exception as e:
    out["pump"] = f"取得不可({type(e).__name__})=pump.fun銘柄でないかも"
# --- RugCheck(commodity足切り・T1) ---
try:
    d = get(f"https://api.rugcheck.xyz/v1/tokens/{CA}/report", 15)
    th = d.get("topHolders") or []
    top = max((h.get("pct") or 0) for h in th) if th else None
    out["onchain_commodity"] = {"mint_authority": d.get("mintAuthority"), "freeze_authority": d.get("freezeAuthority"),
                       "rugged": d.get("rugged"), "top_holder_pct": round(top, 1) if top else None,
                       "danger": [r.get("name") for r in (d.get("risks") or []) if r.get("level") == "danger"],
                       "insiders": bool(d.get("insiderNetworks")) or bool(d.get("graphInsidersDetected")),
                       "creator_tokens_n": len(d.get("creatorTokens") or []), "lp_locked_pct": d.get("lpLockedPct")}
except Exception as e:
    out["onchain_commodity"] = f"取得不可({type(e).__name__})"

# --- ★KOL-CA照合: このCAを watchlist の誰が言及してるか ---
accts = set()
for p in sorted(glob.glob("sources/x/*.md"))[-2000:]:
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if CA in t or (sym and len(sym) >= 3 and f"${sym}" in t):
        m = re.search(r"^account:\s*(\S+)", t, re.M)
        if m:
            accts.add(m.group(1))
out["kol_言及"] = sorted(accts) or "言及なし"

# --- ★KOL track-record(killer edge): 言及KOLの過去callの生存率(tracked.jsonから) ---
rec = {}
try:
    td = json.load(open("brain/state/tracked.json", encoding="utf-8"))
    items = td if isinstance(td, list) else list(td.values())
    for a in accts:
        their = [x for x in items if a in (x.get("kol_ca") or [])]
        dead = sum(1 for x in their if x.get("status") == "dead")
        if their:
            rec[a] = f"過去言及{len(their)}件中 死{dead}/生存{len(their)-dead}"
        else:
            rec[a] = "trackedに過去call記録なし(track-record未蓄積)"
    # creator が過去 track された銘柄
    if creator:
        cr = [x for x in items if x.get("last", {}).get("creator") == creator or x.get("creator") == creator]
        if cr:
            out["creator_history"] = f"この creator の過去 tracked {len(cr)}件: 死{sum(1 for x in cr if x.get('status')=='dead')}"
except Exception as e:
    rec["err"] = type(e).__name__
out["kol_track_record"] = rec or "言及KOLなし=track-record照合不可"

# --- cross-source: corpus(wiki)で ticker/name が語られてるか ---
hits = []
if sym and len(sym) >= 3:
    for p in glob.glob("wiki/**/*.md", recursive=True):
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if f"${sym}" in t or (name and len(name) >= 4 and name in t):
            hits.append(os.path.relpath(p))
out["corpus_言及ページ"] = hits[:8] or "corpus内に言及なし(新規/無名)"
# theme 判定(narrative接続用)
THEMES = {"AI/agent": ["ai","agent","gpt","llm","robot"], "animal": ["dog","cat","inu","pepe","frog","wif"],
          "political": ["trump","elon","maga","gov"], "finance": ["sol","eth","btc","defi","perp"]}
tl = f"{name} {sym}".lower(); out["theme"] = next((k for k,v in THEMES.items() if any(w in tl for w in v)), "other")
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
)"

# (2) ★合成知識を prompt に inject(claude が Read 任せでなく確実に使う): KOL entity / 死亡台帳 / Feedback / narrative
KOL_ENTITIES=""
for a in $(printf '%s' "$DATA" | grep -oE '"[A-Za-z0-9_]+": "(過去言及|trackedに)' | grep -oE '^"[A-Za-z0-9_]+"' | tr -d '"'); do
  f="wiki/entities/players/$(printf '%s' "$a" | tr 'A-Z' 'a-z').md"
  [ -f "$f" ] && KOL_ENTITIES="$KOL_ENTITIES

### KOL @$a の entity(信頼性/profile):
$(head -40 "$f")"
done
LEDGER="$(sed -n '/死亡台帳/,/^## /p' wiki/concepts/rug-anatomy.md 2>/dev/null | head -45)"
FEEDBACK="$(cat wiki/dashboards/feedback.md 2>/dev/null | head -40)"

PROMPT="$(cat brain/check_token_prompt.md)

## 対象トークンの live データ(on-chain=commodity足切り) + wiki合成接続:
$DATA
$KOL_ENTITIES

## 死亡/跳躍台帳(具体型・この銘柄が当てはまる型を探せ):
$LEDGER

## Feedback(型hit-rate・実outcome採点):
$FEEDBACK"
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
