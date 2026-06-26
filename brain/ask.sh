#!/bin/bash
# ask.sh — 対話脳。trench の問いに wiki横断で答える(§Query)。会話インターフェースの中身。
# 使い方: bash brain/ask.sh "今 trench で一番張る価値のある非対称はどこ?"
# headless claude が wiki を読んで横断回答(読むだけ=wiki編集しない・--strict-mcp-config=telegram干渉なし)。
# 将来この出力を Q&A bot(別トークン)が telegram に返す。中身=このスクリプト。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${ASK_MODEL:-sonnet}"

Q="${*:-}"
[ -n "$Q" ] || { echo "問いを渡して: bash brain/ask.sh \"...\"" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

# 時系列データ(直近)＝「いつ何が変わった/速度/トレンド」の問いに使う。日次snapshot。
TS="$(tail -14 brain/state/pulse_history.jsonl 2>/dev/null || echo '(時系列データなし)')"

# 問いに $TICKER / CA があれば live X検索(今の熱・watchlist外含む)。無ければ空=スキップ(一般問いはcorpusのみ)。
LIVEX="$(python3 - "$Q" <<'PY'
import sys, re, json, urllib.request, urllib.parse
q = sys.argv[1]
ents = list((set(re.findall(r"\$[A-Za-z0-9]{2,15}", q)) | set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q))))[:3]
if not ents: sys.exit(0)
key = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="): key = ln.strip().split("=", 1)[1]
except Exception: pass
if not key: sys.exit(0)
out = []
for e in ents:
    u = f"https://api.twitterapi.io/twitter/tweet/advanced_search?query={urllib.parse.quote(e)}&queryType=Latest"
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'X-API-Key': key}), timeout=12)
        tw = (json.loads(r.read()).get('tweets') or [])[:8]
    except Exception:
        continue
    seen = {}
    for t in tw:
        a = t.get('author') or {}; un = a.get('userName')
        if un and un not in seen:
            seen[un] = {'by': un, 'followers': a.get('followers'), 'text': (t.get('text') or '')[:120]}
    if seen:
        out.append({'entity': e, 'live': sorted(seen.values(), key=lambda x: -(x.get('followers') or 0))[:6]})
if out: print(json.dumps(out, ensure_ascii=False, indent=1))
PY
)"

# ★A3統合: 問いに CA→on-chain / accountリンク/@→そのツイ を gather＝1つの頭で全部読む(道具選ばせない)
ENTDATA="$(python3 - "$Q" <<'PY'
import sys, re, json, urllib.request, urllib.parse
q = sys.argv[1]; UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
key = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="): key = ln.strip().split("=", 1)[1]
except Exception: pass
out = {}
m = re.search(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q)
if m:
    ca = m.group(0)
    try:
        c = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://frontend-api-v3.pump.fun/coins/{ca}", headers={"User-Agent": UA}), timeout=10).read())
        out["token"] = {"sym": c.get("symbol"), "name": c.get("name"), "mcap": c.get("usd_market_cap"), "reply": c.get("reply_count"), "complete": c.get("complete"), "twitter": c.get("twitter")}
    except Exception: pass
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://api.rugcheck.xyz/v1/tokens/{ca}/report", headers={"User-Agent": UA}), timeout=12).read())
        th = d.get("topHolders") or []
        out["token_onchain"] = {"mint_auth": d.get("mintAuthority"), "rugged": d.get("rugged"), "top_pct": round(max((h.get("pct") or 0) for h in th), 1) if th else None, "insiders": bool(d.get("insiderNetworks")), "danger": [r.get("name") for r in (d.get("risks") or []) if r.get("level") == "danger"]}
    except Exception: pass
a = re.search(r"(?:x\.com|twitter\.com)/([A-Za-z0-9_]+)", q) or re.search(r"@([A-Za-z0-9_]{2,15})", q)
if a and key:
    h = a.group(1)
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://api.twitterapi.io/twitter/user/last_tweets?" + urllib.parse.urlencode({"userName": h}), headers={"X-API-Key": key}), timeout=15)
        arr = (json.loads(r.read()).get("tweets") or [])[:15]
        out["account"] = {"handle": h, "recent_tweets": [(t.get("text") or "")[:150] for t in arr]}
    except Exception: pass
if out: print(json.dumps(out, ensure_ascii=False, indent=1))
PY
)"

PROMPT="$(cat brain/ask_prompt.md)

## ★この人(本人)の文脈＝これを前提に「この人のために」考える(A6)
$(cat brain/user_context.md 2>/dev/null)

## 方法論（Skill Graph: 内部でこれに沿って考える・出力は簡潔に合成）
$(cat brain/methodology/lenses.md)
$(cat brain/methodology/source-tiers.md)
$(cat brain/methodology/synthesis-rules.md)

## 時系列データ（直近14日の日次snapshot＝pulse_history）
「先週から何が変わった/トレンド/速度」系の問いは**このデータで答える**（死/backlog/テーマ分布/台帳/watchlistの推移）。スナップショットの差分を読め。死亡/跳躍台帳(append式)も時系列の根拠に使える。
$TS
${LIVEX:+

## live X（問いの \$ticker/CA を今 誰が語ってるか・watchlist外含む・follower重み）
新規/今の熱はこれで読む（大follower数人がCA投げてる=traction兆候／無風=誰も乗ってない）。⚠️語られてる≠良い(bot/pumper疑い)→corpusのKOL track-recordとクロス。
$LIVEX}
${ENTDATA:+

## ★この問いに含まれる銘柄/アカウントの実データ（1つの頭で全部読め＝道具を選ばせない）
問いに CA/アカウントがあれば下に on-chain/ツイを gather 済。これと corpus・合成知識・liveを**統合して1つの読み**にせよ（/check だの /who だの分けない）。
$ENTDATA}

## ユーザーの問い:
$Q"
# --strict-mcp-config 必須(telegram等MCPを起動させない)。read-only(wiki編集しない)。
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
