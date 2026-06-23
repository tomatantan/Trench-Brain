#!/bin/bash
# synthesize_backfill.sh — 未合成stubの深掘り工程を無人で回す。
# build_entities が事実集約しただけで合成メモ「_（未記入）_」のままの entity のうち、
# **signal が高い(言及≥3・複数アカ)もの最大5件**を headless claude が deep 合成する。
# = グラフ密度(=合成カバレッジ)を構造的に上げる。低signalは観測≠採用で触らない。
# 対象が無くなれば claude を呼ばない(コスト0)＝自己限定(worthy分を埋めたら idle)。
# X(synthesize_x)/pump(synthesize)/長文(synthesize_longform)に続く第4の合成輪。cron が前後で git。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
LOG="brain/state/cron.log"
MODEL="${SYNTH_MODEL:-sonnet}"
ENABLED="${SYNTH_BACKFILL_ENABLED:-1}"
MIN_MENTIONS="${BACKFILL_MIN_MENTIONS:-3}"
TOPN="${BACKFILL_TOPN:-5}"

[ "$ENABLED" = "1" ] || { echo "synth-backfill: disabled" >> "$LOG"; exit 0; }

# 高signal未合成 entity を mentions 降順で TOPN 件、ファイルパスを列挙(決定的選別=signal門)
TARGETS="$(python3 - "$MIN_MENTIONS" "$TOPN" <<'PY'
import glob,re,sys
mn=int(sys.argv[1]); topn=int(sys.argv[2])
rows=[]
for f in glob.glob("wiki/entities/**/*.md",recursive=True):
    t=open(f,encoding="utf-8",errors="replace").read()
    if "_（未記入" not in t: continue
    m=re.search(r"^mentions:\s*(\d+)",t,re.M); a=re.search(r"^accounts:\s*(\d+)",t,re.M)
    men=int(m.group(1)) if m else 0; acc=int(a.group(1)) if a else 0
    if men>=mn and acc>=2:
        rows.append((men,f))
rows.sort(reverse=True)
for men,f in rows[:topn]:
    print(f"- {f} (言及{men})")
PY
)"

if [ -z "$TARGETS" ]; then
  echo "synth-backfill: 高signal未合成なし、skip(claude未呼出)" >> "$LOG"
  exit 0
fi

n=$(printf '%s\n' "$TARGETS" | grep -c '^- ' || true)
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) synth-backfill start: ${n}件 (model=$MODEL) ===" >> "$LOG"
printf '%s\n' "$TARGETS" >> "$LOG"

command -v claude >/dev/null 2>&1 || { echo "synth-backfill: claude CLI なし→skip" >> "$LOG"; exit 0; }
PROMPT="$(cat brain/synth_backfill_prompt.md)
$TARGETS"
# --strict-mcp-config 必須(telegram等MCPを起動させない。2026-06-23 切断原因)。
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$PROMPT" >> "$LOG" 2>&1 \
  && echo "synth-backfill: done" >> "$LOG" \
  || echo "synth-backfill: claude error(次サイクル再試行)" >> "$LOG"
