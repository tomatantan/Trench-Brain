#!/bin/bash
# synthesize_player.sh — player の「思考の型」を合成し entity の synthesis block に書く。
# 視点エンジン(/check・/wiki)が「この player ならこう読む」を channel する燃料を厚くする(本人reframe 2026-06-24)。
# 使い方: bash brain/synthesize_player.sh <handle(no @)>
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${SYNTH_PLAYER_MODEL:-sonnet}"
H="${1:?handle(no @)を渡して}"
H="$(printf '%s' "$H" | tr 'A-Z' 'a-z')"  # entity pathはlowercase正典(handleはcase-insensitive)
ENT="wiki/entities/players/@${H}.md"
[ -f "$ENT" ] || { echo "entity無し: $ENT" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

POSTS="$(python3 - "$H" <<'PY'
import sys, glob, re
h = sys.argv[1].lower()
posts = []
for p in glob.glob("sources/x/*.md"):
    base = p.split("/")[-1]
    if "__" not in base or base.rsplit("__", 1)[0].lower() != h:
        continue
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    m = re.search(r"^likes:\s*(\d+)", t, re.M)
    likes = int(m.group(1)) if m else 0
    body = t.split("---", 2)[-1].strip().replace("\n", " ")[:280]
    posts.append((likes, body))
posts.sort(reverse=True)
for lk, b in posts[:25]:
    print(f"[{lk}likes] {b}")
PY
)"
TR="$(python3 -c "
import json
try:
    d=json.load(open('brain/state/kol_track_records.json'))
    r=d.get('${H}'.lower())
    print(f\"track-record: CA言及{r['mentioned']}/評価{r['evaluated']}中 死{r['dead']}({r['death_rate']}%死)\" if r else 'track-record: 未蓄積')
except Exception: print('track-record: 不明')
" 2>/dev/null)"

# curated深堀りprofile(<!-- profile:start/end -->・原典/長文ソース由来)があれば文脈として渡す。
# synthesisはこれを「上書き」せず「今の投稿と突き合わせる」＝profileは人/エージェントのcurated層で不可侵。
PROF="$(python3 - "$ENT" <<'PY'
import sys
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
i, j = t.find("<!-- profile:start -->"), t.find("<!-- profile:end -->")
print(t[i:j] if (i != -1 and j != -1) else "")
PY
)"

PROMPT="$(cat brain/synth_player_prompt.md)

## 対象 player: @${H}
$TR
${PROF:+
## curated深堀りprofile（原典由来・不可侵の前提知識。今の投稿がこれと矛盾したら⚠️で指摘）
$PROF}

## 実投稿（エンゲージ上位・これに grounded に）:
$POSTS"

SYN="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
[ -n "$SYN" ] || { echo "合成が空 → skip" >&2; exit 0; }
TMP="$(mktemp)"; printf '%s' "$SYN" > "$TMP"
python3 - "$ENT" "$TMP" <<'PY'
import sys
ent, synf = sys.argv[1], sys.argv[2]
syn = open(synf, encoding="utf-8").read().strip()
t = open(ent, encoding="utf-8").read()
S, E = "<!-- synthesis:start -->", "<!-- synthesis:end -->"
block = f"{S}\n{syn}\n{E}"
i, j = t.find(S), t.find(E)
if i != -1 and j != -1:
    t = t[:i] + block + t[j + len(E):]
else:
    t = t.rstrip() + "\n\n" + block + "\n"
open(ent, "w", encoding="utf-8").write(t)
print(f"思考の型を {ent} に書込")
PY
rm -f "$TMP"
