#!/bin/bash
# synthesize_players.sh — player mind-model(KOLの"脳"=思考の型)の自動合成driver。
# ★核心成果物(KOLの脳をモデル化)を毎サイクル自動で維持する層。従来は手動(1 handle)で cron 未配線だった。
# 選別(門): 直近48hに投稿があり entity在り synthesis古い/薄い player を優先。上限=PLAYER_SYNTH_MAX(既定3)/サイクル。
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MAX="${PLAYER_SYNTH_MAX:-3}"

CANDIDATES="$(python3 - "$MAX" <<'PY'
import sys, glob, os, time
max_n = int(sys.argv[1]); now = time.time(); WINDOW = 48*3600
active = {}
for p in glob.glob("sources/x/*.md"):
    base = os.path.basename(p)
    if "__" not in base: continue
    h = base.rsplit("__", 1)[0].lower()  # rsplit=末尾_のhandle対応・lowercase=entity path正典
    try: mt = os.path.getmtime(p)
    except OSError: continue
    if now - mt <= WINDOW: active[h] = max(active.get(h,0), mt)
scored = []
for h in active:
    ent = f"wiki/entities/players/@{h}.md"
    if not os.path.exists(ent): continue
    try: body = open(ent, encoding="utf-8", errors="replace").read()
    except OSError: continue
    staleness = (0 if "synthesis:start" not in body else 1, os.path.getmtime(ent))
    scored.append((staleness, h))
scored.sort()
for _, h in scored[:max_n]: print(h)
PY
)"

if [ -z "$CANDIDATES" ]; then
  echo "player合成: 対象なし=スキップ(コスト0)"; exit 0
fi
n=0
for h in $CANDIDATES; do
  echo "player合成: @$h の思考の型を更新..."
  if bash brain/synthesize_player.sh "$h" 2>&1; then n=$((n+1)); else echo "player合成: @$h 失敗(スキップ)"; fi
done
echo "player合成: $n 件更新"
