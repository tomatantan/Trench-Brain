# INGEST routine — エージェントが回す「整理(判断)」工程

LLM Wiki の ingest の判断パートを**定まった手順**にしたもの。新ソースが入る度（または
定期に）エージェント(Claude)がこれを回す＝conceptは"書きたいから書く"のではなく、
この工程の結果として自然に生成・更新される。

## 前提（決定的パートは先にスクリプトが済ませる）
`python3 brain/pipeline.py` が collect→digest→build_entities→ingest_worklist を実行し、
`wiki/_worklist.md`（処理すべき bounded な TODO）を出力している。

## エージェントの手順
1. **`wiki/_worklist.md` を読む**。今サイクルで触るべき entity / concept候補 / player が出ている。
2. **worklist の §1 entity** を上から処理する。各 entity ページ（`wiki/entities/…`）を開き、
   新規の代表ツイ（と必要なら `[[source]]` 原文）を読み、`<!-- synthesis:start … end -->`
   ブロックを **追記・改訂** する:
   - 物語/役割、動線上の位置、⚠️矛盾（強気/弱気を両論併記）、賭け仮説、スコア感(memetic/confidence)。
   - 既存の合成があれば**上書きでなく更新**（新証拠を反映、矛盾は消さず追加）。
   - 関連 entity / concept へ `[[wikilink]]`。
3. **worklist の §2 concept候補** を判断する。複数アカが言及し始めたのに concept が無いもの。
   - そこに**動線（発端→金になるまで）や型（繰り返すパターン）が立つか**を見る。
   - 立つなら `wiki/concepts/` に concept を**新規作成 or 既存更新**。立たないなら作らない（top-down量産はしない）。
4. **矛盾**は見つけ次第、該当 entity/concept に両論併記で旗を立てる（⚠️）。
5. **`wiki/index.md` と `wiki/log.md` を更新**（新規ページ・主な更新を記録）。
6. 1サイクルは worklist の範囲だけ。全部を一度にやらない（複利で積む）。
7. 完了したら、**実際に合成した分だけ**消し込む（全件マーク禁止＝部分合成を全完了と詐称しない）:
   `python3 brain/mark_ingested.py --from-files <このサイクルで合成/更新した wiki ページ...>`
   （触れた concept / entity ページを渡すと、その中の `[[source]]` link の tweet_id だけが ingested 登録される）
   → その後 commit/push。

## 原則（曲げない）
- 合成の起点は worklist（=新ソース）であって、エージェントの主観ではない。
- 矛盾は消さず両論併記。事実は entity、判断は entity の合成メモ＋concept。
- 概念説明は `docs/LLM-WIKI.md`、スキーマは `CLAUDE.md`。
