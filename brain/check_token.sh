#!/bin/bash
# check_token.sh — 魔界スクリーニング。CA(or pump.fun URL)を投げたら ape/avoid を判定。
# ★v2(2026-06-24 本人「on-chainしか見てない=LLM wikiである理由ない」批判への fix):
#   LLM Wiki の固有価値＝**合成知識**を lead に据える。on-chain(RugCheck)は commodity な足切りに降格。
#   wiki-edge: ①shill KOL の track-record(過去callの生存率=tracked.jsonから計算・on-chainツールに出せない)
#             ②KOL の entity(信頼性/profile) ③死亡/跳躍台帳の具体型 ④Feedbackの型hit-rate ⑤cross-source
#   corpus接続ゼロ(無名KOL/未言及)なら「wiki signal無し=on-chainのみ=低edge」と正直に出す。
# read-only・--strict-mcp-config。bot /check $CA。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${CHECK_MODEL:-sonnet}"
ARG="${*:-}"
CA="$(printf '%s' "$ARG" | grep -oE '[1-9A-HJ-NP-Za-km-z]{32,44}' | head -1)"
[ -n "$CA" ] || { echo "CA(mint address) か pump.fun URL を渡して: bash brain/check_token.sh <CA>" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

# (1) live on-chain + KOL track-record + cross-source を収集(python)
DATA="$(python3 - "$CA" <<'PY'
import json, sys, urllib.request, glob, re, os, socket
socket.setdefaulttimeout(12)  # 全socket強制timeout=network hang根絶
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
for p in sorted(glob.glob("sources/x/*.md"))[-600:]:
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if CA in t or (sym and len(sym) >= 3 and f"${sym}" in t):
        m = re.search(r"^account:\s*(\S+)", t, re.M)
        if m:
            accts.add(m.group(1))
out["kol_言及"] = sorted(accts) or "言及なし"

# --- ★live X検索(本丸): この銘柄を今 誰が語ってるか(watchlist外含む・新規でも個別signal) ---
TWKEY = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="):
            TWKEY = ln.strip().split("=", 1)[1]
except Exception:
    pass
def x_search(q, n=15):
    if not TWKEY or not q:
        return []
    u = f"https://api.twitterapi.io/twitter/tweet/advanced_search?query={urllib.parse.quote(q)}&queryType=Latest"
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"X-API-Key": TWKEY}), timeout=15)
        return (json.loads(r.read()).get("tweets") or [])[:n]
    except Exception:
        return []
import urllib.parse
live = {}
for q in [CA] + ([f"${sym}"] if sym and len(sym) >= 3 else []):
    for t in x_search(q):
        au = t.get("author") or {}
        u = au.get("userName")
        if not u or u in live:
            continue
        live[u] = {"by": u, "followers": au.get("followers"), "text": (t.get("text") or "")[:140],
                   "likes": t.get("likeCount"), "matched": ("CA" if q == CA else "ticker")}
ranked = sorted(live.values(), key=lambda x: -(x.get("followers") or 0))[:12]
# ★live×corpus融合: 各 live account を corpus(player entity＋過去call track-record)と照合＝「誰が語ってるか」の質
try:
    _td = json.load(open("brain/state/tracked.json", encoding="utf-8"))
    _items = _td if isinstance(_td, list) else list(_td.values())
except Exception:
    _items = []
try:
    _ktr = json.load(open("brain/state/kol_track_records.json", encoding="utf-8"))  # bootstrap済 track-record
except Exception:
    _ktr = {}
for v in ranked:
    a = v["by"]
    ent = os.path.exists(f"wiki/entities/players/@{a}.md")
    tr = _ktr.get(a.lower())
    their = [x for x in _items if a in (x.get("kol_ca") or [])]
    if tr and tr.get("evaluated", 0) >= 2:  # bootstrap済の歴史track-record優先(richer)
        v["corpus"] = f"corpus既知{'(watchlist)' if ent else ''}・歴史track-record: 言及{tr['mentioned']}/評価{tr['evaluated']}中死{tr['dead']}({tr['death_rate']}%死)"
    elif their:
        dd = sum(1 for x in their if x.get("status") == "dead")
        v["corpus"] = f"corpus既知{'(watchlist)' if ent else ''}・過去call{len(their)}件中死{dd}"
    elif ent:
        v["corpus"] = "corpus既知(watchlist entity有・call記録未蓄積)"
    else:
        v["corpus"] = "corpus未知(無名/watchlist外=信頼性不明)"
out["live_X_誰が語ってるか"] = ranked or "X上で言及ゼロ(誰も語ってない=無風・新規の典型)"
out["live_X_要約"] = {"語ってる人数": len(live), "最大follower": (ranked[0]["followers"] if ranked else 0),
                      "CA一致投稿": sum(1 for v in live.values() if v["matched"] == "CA")}

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
  # entity は @<Handle>.md(原case)。見つからなければ小文字でも試す(macOS case)。
  f="wiki/entities/players/@${a}.md"
  [ -f "$f" ] || f="$(ls wiki/entities/players/ 2>/dev/null | grep -ix "@${a}.md" | head -1 | sed 's|^|wiki/entities/players/|')"
  if [ -n "$f" ] && [ -f "$f" ]; then
    # ★思考の型(synthesis block=この人がどう読むか)を優先注入=視点エンジンの燃料。無ければstub先頭。
    prof="$(sed -n '/## 思考の型/,/synthesis:end/p' "$f" | grep -v 'synthesis:end' | head -50)"
    [ -z "$prof" ] && prof="$(head -22 "$f")"
    KOL_ENTITIES="$KOL_ENTITIES

### KOL @$a の思考の型(この人ならどう読むか):
$prof"
  fi
done
LEDGER="$(sed -n '/死亡台帳/,/^## /p' wiki/concepts/rug-anatomy.md 2>/dev/null | head -45)"
FEEDBACK="$(cat wiki/dashboards/feedback.md 2>/dev/null | head -40)"
MANIP="$(cat wiki/concepts/manipulation-playbook.md 2>/dev/null | sed -n '/^## 型/,/出典/p' | head -50)"
EARLY="$(cat wiki/concepts/early-lowcap-entry.md 2>/dev/null | sed -n '/フレームの転換/,/## ⚠️/p' | head -45)"

# ★usageがcorpusを育てる(本人「inputは少なく・autonomousに」): checkした銘柄を tracking に入れfateを学ぶ。
#   本人の自然な /check（実プレイ）が、追加inputなしに死亡/跳躍台帳とKOL track-recordを厚くする＝魔界基盤の autonomous成長。
printf '{"ca":"%s","ts":%d}\n' "$CA" "$(date +%s)" >> brain/state/user_checked.jsonl 2>/dev/null || true

PROMPT="$(cat brain/check_token_prompt.md)

## ★この人(本人)の文脈＝これを前提に「この人のために」読む(A6):
$(cat brain/user_context.md 2>/dev/null)

## 対象トークンの live データ(on-chain=commodity足切り) + wiki合成接続:
$DATA
$KOL_ENTITIES

## 死亡/跳躍台帳(具体型・この銘柄が当てはまる型を探せ):
$LEDGER

## Feedback(型hit-rate・実outcome採点):
$FEEDBACK

## 魔界 manipulation playbook(social手口・live Xがこの型に当てはまるか照合):
$MANIP

## ★low-cap/卒業前なら このフレームで評価せよ(危険一律にしない・本人指摘):
対象が **bonding-curve段階/低mcap/未graduated** なら、「卒業した?流動性ある?」(post-grad指標)で一律dangerにするな＝tautologyで無情報。下の**早期signal(mcap velocity↑/scam clean/organic traction初動/theme-fit/最初のKOL)**で「早期の中で生存を分けるもの」を評価せよ。早期は base-rate最悪だが非対称最大＝サイズ小で early signal の重なりを見る。
$EARLY"
# claude を hard timeout で包む(macOSにtimeout無い→hang根絶)＝空/timeoutなら1回retry→それでも空ならfallback
# (本人2026-06-27 /check空判定bug＝claudeがintermittentにhang/空応答→「判定が空」silentになってた)
run_claude() {
  python3 -c 'import subprocess,sys
try:
    r=subprocess.run(["claude","--print","--model",sys.argv[1],"--dangerously-skip-permissions","--strict-mcp-config",sys.argv[2]],capture_output=True,text=True,timeout=130)
    sys.stdout.write(r.stdout or "")
except Exception: pass' "$MODEL" "$PROMPT"
}
OUT="$(run_claude)"
[ -n "$(printf '%s' "$OUT" | tr -d '[:space:]')" ] || OUT="$(run_claude)"
if [ -z "$(printf '%s' "$OUT" | tr -d '[:space:]')" ]; then
  # fallback は壊れにくい grep/sed のみ(inline python は set -e で死ぬ)
  SYM="$(printf '%s' "$DATA" | grep -oE '"symbol": "[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')"
  MC="$(printf '%s' "$DATA" | grep -oE '"usd_mcap": [0-9.]+' | head -1 | grep -oE '[0-9]+' | head -1)"
  OUT="⚠️ 合成が一時的に応答せず（claudeが遅延/空応答＝負荷時に起きる）。もう一度 /check して。
取れてるon-chain: ${SYM:-?} / mcap \$${MC:-?}"
fi
printf '%s\n' "$OUT"
