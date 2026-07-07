#!/bin/bash
# onboard_player.sh — watchlist 新規アカの「収集前の人物理解」profile を作る（本人指示 2026-07-06:
# 「最新投稿を取る前に、どういう人間で保守的なのか攻撃的なのか・バックボーン・立ち位置の理解が要る」）。
# bio+直近実ツイを1回取得→人物profileを合成→entityの <!-- profile:start/end -->（curated層・機械上書き不可）へ書く。
# 恒久機構: 以後 watchlist に誰を足しても「理解→収集」の順を門として踏める。
# 使い方: bash brain/onboard_player.sh <handle(no @)> [--force]
#   既に profile ブロックがある entity はスキップ（--force で上書き）。read-only 取得・wiki 書込は profile ブロックのみ。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${ONBOARD_MODEL:-sonnet}"
H="${1:?handle(no @)を渡して}"
FORCE="${2:-}"
H="$(printf '%s' "$H" | tr -d '@' | tr 'A-Z' 'a-z')"   # entity path は lowercase 正典
ENT="wiki/entities/players/@${H}.md"
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

if [ -f "$ENT" ] && grep -q "profile:start" "$ENT" && [ "$FORCE" != "--force" ]; then
  echo "onboard: @$H は profile 済み → skip（--force で上書き）"; exit 0
fi

# ★prefetch対応(2026-07-07): ONBOARD_DATA_DIR に data_<handle>.json があればAPIを叩かずそれを使う。
#   fetch(レート制限側)とLLM生成(遅い側)の分離＝並列バッチがAPIを乱打してsuccess+0件連鎖する事故の根治。
if [ -n "${ONBOARD_DATA_DIR:-}" ] && [ -s "${ONBOARD_DATA_DIR}/data_${H}.json" ]; then
  DATA="$(cat "${ONBOARD_DATA_DIR}/data_${H}.json")"
else
DATA="$(python3 - "$H" <<'PY'
import sys, json, urllib.request, urllib.parse
H = sys.argv[1]
key = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="):
            key = ln.strip().split("=", 1)[1]
except Exception:
    pass
out = {"handle": H}
tw = []
if key:
    try:
        u = "https://api.twitterapi.io/twitter/user/last_tweets?" + urllib.parse.urlencode({"userName": H})
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"X-API-Key": key}), timeout=20)
        d = json.loads(r.read())
        arr = d.get("tweets") or (d.get("data") or {}).get("tweets") or []
        for t in arr[:25]:
            tw.append({"text": (t.get("text") or "")[:240], "likes": t.get("likeCount"),
                       "views": t.get("viewCount")})
        au = (arr[0].get("author") if arr else None) or {}
        out["profile"] = {"name": au.get("name"), "followers": au.get("followers"),
                          "desc": (au.get("description") or "")[:200]}
    except Exception as e:
        out["fetch_err"] = type(e).__name__
out["recent_tweets"] = tw or "取得不可"
print(json.dumps(out, ensure_ascii=False, indent=1))
PY
)"
fi

# 取得ゼロなら合成しない（薄いデータで人物像を捏造させない）
if printf '%s' "$DATA" | grep -q '"recent_tweets": "取得不可"'; then
  echo "onboard: @$H 実ツイ取得不可 → profile 合成せず skip（後で再試行）" >&2; exit 2
fi

PROMPT="$(cat brain/onboard_player_prompt.md)

## 対象アカウント: @${H}（実データ・これに接地せよ）
$DATA"
PROF="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
# ★構造検証(2026-07-06): tool持ちで起動したclaudeが自分でファイルを書いた気になり
#   stdoutに「作成した。要点:」等の報告文だけ返す個体が出た(13/15)。本文構造が無ければ1回retry→fail。
if ! printf '%s' "$PROF" | grep -q "### 何者か"; then
  echo "onboard: @$H 出力が profile 本文でない(報告文疑い) → retry" >&2
  PROF="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
fi
printf '%s' "$PROF" | grep -q "### 何者か" || { echo "onboard: @$H 構造不合格2回 → fail" >&2; exit 3; }
[ -n "$PROF" ] || { echo "onboard: @$H 合成が空 → skip" >&2; exit 3; }

TMP="$(mktemp)"; printf '%s' "$PROF" > "$TMP"
python3 - "$ENT" "$TMP" "$H" <<'PY'
import sys, os, datetime
ent, prof_f, h = sys.argv[1], sys.argv[2], sys.argv[3]
prof = open(prof_f, encoding="utf-8").read().strip()
today = datetime.date.today().isoformat()
S, E = "<!-- profile:start -->", "<!-- profile:end -->"
block = (f"{S}\n## 深堀りprofile（curated・機械上書き不可）\n\n"
         f"> onboarding調査 {today}（収集開始前の人物理解＝bio+直近実ツイ接地・brain/onboard_player.sh）。\n\n"
         f"{prof}\n{E}")
if os.path.exists(ent):
    t = open(ent, encoding="utf-8").read()
    i, j = t.find(S), t.find(E)
    if i != -1 and j != -1:
        t = t[:i] + block + t[j + len(E):]
    else:
        # synthesis ブロックの直前に置く（無ければ末尾）
        k = t.find("<!-- synthesis:start -->")
        t = (t[:k] + block + "\n\n" + t[k:]) if k != -1 else (t.rstrip() + "\n\n" + block + "\n")
    open(ent, "w", encoding="utf-8").write(t)
else:
    stub = "\n".join([
        "---", "type: entity", "kind: player", f"title: @{h}",
        f"created: {today}", f"updated: {today}",
        "tags: [trench, entity, player, onboarding]", "posts: 0", "---", "",
        f"# @{h}", "",
        f"> watchlist入り {today}（spyzer情報網・本人承認）。収集開始前に onboarding profile を先に作成。",
        "> 投稿の自動集約は収集開始後に build_entities.py が追記する。", "",
        block, ""])
    open(ent, "w", encoding="utf-8").write(stub)
print(f"onboard: profile を {ent} に書込")
PY
rm -f "$TMP"
