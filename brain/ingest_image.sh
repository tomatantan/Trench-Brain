#!/bin/bash
# ingest_image.sh — 画像ミーム/スクショを vision で取り込む。
# 使い方: bash brain/ingest_image.sh <画像パス> "<caption>"
# headless claude(マルチモーダル)が画像を Read→観測(写ってる物/画像内テキスト/ticker)＋推論(ナラティブ/型)を source 化。
# --strict-mcp-config(telegram干渉なし)。--dangerously-skip-permissions(Read tool許可)。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${IMG_MODEL:-sonnet}"
IMG="${1:-}"
CAP="${2:-}"
[ -n "$IMG" ] && [ -f "$IMG" ] || { echo "画像パスが無い: $IMG" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "no claude" >&2; exit 1; }

PROMPT="$(cat brain/ingest_image_prompt.md)
画像パス: $IMG
caption: ${CAP:-（なし）}"
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
