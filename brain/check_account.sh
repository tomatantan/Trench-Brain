#!/bin/bash
# check_account.sh — アカウント信頼性スクリーニング。@handle or Xリンクを投げたら
# 「このアカウント主は嘘つき/pumperか、信頼できるか」を、実ツイ+track-record+思考の型から読む(本人2026-06-25)。
# read-only・--strict-mcp-config。bot /who。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${CHECK_MODEL:-sonnet}"
ARG="${*:-}"
H="$(printf '%s' "$ARG" | grep -oE '(x\.com|twitter\.com)/[A-Za-z0-9_]+' | head -1 | sed -E 's|.*/||')"
[ -n "$H" ] || H="$(printf '%s' "$ARG" | grep -oE '@[A-Za-z0-9_]{2,15}' | head -1 | tr -d '@')"
[ -n "$H" ] || H="$(printf '%s' "$ARG" | tr -d ' ' | grep -oE '^[A-Za-z0-9_]{2,15}$' || true)"
[ -n "$H" ] || { echo "アカウントを渡して: /who @handle または Xリンク" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

DATA="$(python3 - "$H" <<'PY'
import sys, json, os, urllib.request, urllib.parse, glob, re
H = sys.argv[1]
key = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="):
            key = ln.strip().split("=", 1)[1]
except Exception:
    pass
out = {"handle": H}
# recent tweets (twitterapi)
tw = []
if key:
    try:
        u = "https://api.twitterapi.io/twitter/user/last_tweets?" + urllib.parse.urlencode({"userName": H})
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"X-API-Key": key}), timeout=15)
        d = json.loads(r.read())
        arr = d.get("tweets") or (d.get("data") or {}).get("tweets") or []
        for t in arr[:25]:
            tw.append({"text": (t.get("text") or "")[:240], "likes": t.get("likeCount"),
                       "retweets": t.get("retweetCount"), "views": t.get("viewCount")})
        # プロフィール
        au = (arr[0].get("author") if arr else None) or {}
        out["profile"] = {"name": au.get("name"), "followers": au.get("followers"),
                          "verified": au.get("isBlueVerified"), "desc": (au.get("description") or "")[:160]}
    except Exception as e:
        out["fetch_err"] = type(e).__name__
out["recent_tweets"] = tw or "取得不可/ツイなし"
# track-record(watchlist KOLなら)
try:
    ktr = json.load(open("brain/state/kol_track_records.json", encoding="utf-8"))
    r = ktr.get(H.lower())
    out["track_record"] = (f"CA言及{r['mentioned']}/評価{r['evaluated']}中 死{r['dead']}({r['death_rate']}%死)"
                           if r else "watchlist内にtrack-record無し(=未知/初見)")
except Exception:
    out["track_record"] = "不明"
# 思考の型(entity synthesis block・有れば)
ent = None
for f in glob.glob("wiki/entities/players/@*.md"):
    if os.path.basename(f).lower() == f"@{H.lower()}.md":
        ent = f; break
if ent:
    t = open(ent, encoding="utf-8").read()
    m = re.search(r"## 思考の型.*?(?=<!-- synthesis:end)", t, re.S)
    out["思考の型_corpus"] = (m.group(0)[:1200] if m else "entity有(思考の型未合成)")
else:
    out["思考の型_corpus"] = "corpus未知(watchlist外=初見)"
print(json.dumps(out, ensure_ascii=False, indent=1))
PY
)"

# ★評価軸の源＝合成された手口の型(manipulation-playbook)を inject＝固定listでなくここから導出(本人2026-06-25)
MANIP="$(sed -n '/^## 型/,/出典/p' wiki/concepts/manipulation-playbook.md 2>/dev/null | head -55)"
PROMPT="$(cat brain/check_account_prompt.md)
## 対象アカウント: @${H}
$DATA

## 合成された魔界の手口の型（[[manipulation-playbook]]＝評価軸はここから導く・実ツイがどの型に当てはまるか照合）:
$MANIP"
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
