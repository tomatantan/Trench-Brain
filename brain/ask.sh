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

PROMPT="$(cat brain/ask_prompt.md)

## 方法論（Skill Graph: 内部でこれに沿って考える・出力は簡潔に合成）
$(cat brain/methodology/lenses.md)
$(cat brain/methodology/source-tiers.md)
$(cat brain/methodology/synthesis-rules.md)

## ユーザーの問い:
$Q"
# --strict-mcp-config 必須(telegram等MCPを起動させない)。read-only(wiki編集しない)。
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
