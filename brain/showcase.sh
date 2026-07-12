#!/bin/bash
# showcase.sh — 日替わり(毎サイクル)ショーケース回答の生成(2026-07-12 本人「何ができるか分からんで終わりそう」対策)。
# UIを開いた瞬間に「今日の魔界の読み」(型Bの実物)が表示済み＝初見が3秒で製品を理解する。
# 生成は1サイクル1回(haiku=安い)・配信は静的(brain/state/showcase.json→/api/showcase)＝閲覧コスト0。
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${SHOWCASE_MODEL:-haiku}"
command -v claude >/dev/null 2>&1 || { echo "showcase: claude無し=skip"; exit 0; }

# 問いは日替わりローテ(曜日で固定=決定的)。全部「初見に刺さる」型。
QS=(
  "今日の魔界、どう立ち回るのが勝者の型？"
  "今KOLたちの関心はどこに移動してる？それは何のサイン？"
  "今の相場で一番の⚠️矛盾は何？そこから何を学ぶ？"
  "今日いちばん危ない罠は何？"
  "実績のあるKOLたちは今何を待ってる？"
  "今週の流れで一番大きく動いた話題は？乗るべき？"
  "今の地合いで『やらない方がいいこと』は？"
)
DOW=$(date +%u)  # 1-7
Q="${QS[$(( (DOW - 1) % ${#QS[@]} ))]}"

ANSWER="$(ASK_UI=1 ASK_MODEL="$MODEL" bash brain/ask.sh "$Q" 2>/dev/null || true)"
if [ -z "$ANSWER" ]; then
  echo "showcase: 生成失敗=既存を維持"; exit 0
fi
SHOW_Q="$Q" SHOW_A="$ANSWER" python3 - <<'PY'
import json, os, time
out = {"ts": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
       "question": os.environ["SHOW_Q"], "answer": os.environ["SHOW_A"]}
tmp = "brain/state/showcase.json.tmp"
open(tmp, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
os.replace(tmp, "brain/state/showcase.json")
print("showcase: 生成OK", len(out["answer"]), "字")
PY
