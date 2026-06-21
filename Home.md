---
type: home
title: Home — Trench-Brain
tags: [trench]
---

# 🧠⛏️ Trench-Brain

crypto trench の X発言・ニュース・要人発言を取り込み、単一ソースでは見えない繋がりを概念ページに合成し続ける LLM Wiki。

## 入口
- 📇 [[index]] — 全ページのカタログ
- 🗒️ [[log]] — 操作履歴（ingest / query / lint）

## フォルダの役割
| フォルダ | 中身 | 編集 |
| --- | --- | --- |
| `sources/` | X・ニュース・要人発言の生クリップ（x / news / figures） | 人間が追加。**LLMは読むだけ** |
| `wiki/summaries/` | 1ソース=1要約ページ | LLM |
| `wiki/concepts/` | ★横断合成の概念ページ（肝） | LLM |
| `wiki/queries/` | 質問と回答の資産 | LLM |
| `wiki/_templates/` | ページ雛形（summary / concept） | — |

## 操作（Claude Code / Codex のスキル）
- **ingest-x** … XのポストURL/本文を渡す → 要約＋関連 concept 更新
- **ingest-news** … ニュース/記事URLを渡す → 同上
- **query** … Wikiに質問 → 横断回答 → `wiki/queries/` に保存
- **lint** … 矛盾・孤立ページ・知識ギャップ・古さを検出（報告のみ）

## グラフの見方
ノードの色：**concept=オレンジ（主役）** / summary=青 / query=緑 / source=グレー。
オレンジに線が集まるほど、横断合成が育っている合図。

> 運用規約は `CLAUDE.md`。`sources/` は読むだけ、編集は `wiki/` 配下のみ。
