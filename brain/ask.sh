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

PROMPT="$(cat brain/ask_prompt.md)

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

## ユーザーの問い:
$Q"
# --strict-mcp-config 必須(telegram等MCPを起動させない)。read-only(wiki編集しない)。
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
