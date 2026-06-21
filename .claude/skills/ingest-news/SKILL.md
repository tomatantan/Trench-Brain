---
name: ingest-news
description: ニュース記事/ブログをTrench-Brainに取り込む。URLを渡すと生ソース保存→要約→関連concept更新。
---

# ingest-news

ニュース・記事・要人エッセイをWikiに取り込む。

## 手順
1. 記事URLから本文を取得（タイトル・媒体・日付・要旨）。
2. `sources/news/<媒体>-<短い識別>.md`（要人の発言なら `sources/figures/`）に保存。
3. `wiki/summaries/` に要約ページ作成（[[_templates/summary]]）。`source:` に元URL。
4. 関連 concept を更新（規制/マクロ/セクター/プレイヤー等）。crypto trench への影響を必ず1行書く。
5. `[[wikilink]]` 接続、`index.md`/`log.md` 更新。

## 注意
- 事実と意見を分ける。誰の主張かを明記。
- trench に無関係なら取り込まない（高シグナルのみ）。
