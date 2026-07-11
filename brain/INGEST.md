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

## auto-synthesis（launchpad ライフサイクル＝即時tier）
`brain/track.py` が**決定的(安い)層**を回す＝全mint観測(pump.fun launch feed)→篩(安全門+勢い門)→TRACKED登録→毎時watch(数値diffのみ・LLM不使用)→誕生/変化/死を `brain/state/synth_queue.json` に積む。
エージェント(Claude)の仕事＝**synth_queue を読んで合成する**（worklistと同じ"判断"工程の即時版）:
- **births**(門通過の新規): これは何か(name/twitter/links/tokenized_agent)、**既存13 conceptのどこに刺さるか**（[[launchpad-economics]] 直下、[[survivor-memes]]/[[ai-memes]]/[[jp-meme-cluster]] 等）、⚠️([[rug-anatomy]] の赤旗)。→ token entity の synthesis を起こす/更新。
  - ★**token entity のファイル名は必ず大文字ticker** `wiki/entities/tokens/$<UPPERCASE-TICKER>.md`(同ticker別mintは `$<UPPER>-<mint先頭6>.md`)。case違い($Foo/$FOO)の双子は macOS の pull 詰まり源＝機械normalizer(entity_paths.py)が事後に潰すが、**最初から大文字で書け**(normalizerの仕事を減らす)。

- **changes**(GRADUATED / mcap急変 / 話題化): 該当 entity を更新＝動線の進展を追記。
- **deaths**: **最終合成**＝死因(cause)を記録し outcome=died/rugged を確定→ entity を閉じる。**これが生存者バイアスの分母**（死を記録して初めて死は資産になる）。
- **深さ∝情報量**: 型通りの死＝1行で型を補強。番狂わせ(生存/新しい死に方)＝フル合成。千件の同じ死を深掘りしない。
- 状態管理は track.py（mark_ingested 不要）。entity更新を commit/push。
- **観測(全mint) ≠ 採用(wiki入り)**: wikiに入る(=合成される)のは門通過分だけ＝firehoseでない。観測は安くカウントするだけ(base_rate＝死の分母)。

## 原則（曲げない）
- 合成の起点は worklist（=新ソース）であって、エージェントの主観ではない。
- 矛盾は消さず両論併記。事実は entity、判断は entity の合成メモ＋concept。
- 概念説明は `docs/LLM-WIKI.md`、スキーマは `CLAUDE.md`。
