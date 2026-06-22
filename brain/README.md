# brain — 「仕分ける/整理する仕組み」（LLM Wiki 準拠）

Trench-Brain は **Andrej Karpathy の LLM Wiki パターン**（2026/4）の crypto trench 実装。
RAGのように毎回生データを検索し直すのではなく、LLMが生ソースを読んで
**構造化・相互リンクされた wiki に合成して書き込み、知識を複利で積む**。

## 3層（Karpathy準拠）
- **raw**（不変）: `sources/x/` の生ツイ。読むだけ・改変しない。
- **wiki**（LLMが全所有）: `wiki/` の md 群。entity / concept / dashboard / index / log。
- **schema**（規約）: `CLAUDE.md`。LLMを"wiki管理者"に躾ける。

## ページ型
- **entity**（`wiki/entities/`）= 事実の集約。token($ticker)・player(@handle)毎。
  `brain/build_entities.py` が**自動生成・冪等更新**。各ページの `synthesis:start/end`
  ブロックにエージェントが判断(物語/動線/⚠️矛盾/賭け仮説)を書き、再生成でも保持される。
- **concept**（`wiki/concepts/`）= 横断合成。ナラティブ・型・動線。entityを束ねる上位層。
- **dashboard**（`wiki/dashboards/`）= 集計ビュー（[[signal]]）。
- **index.md / log.md** = 目録 / 追記ログ。

## パイプライン（"貯める→仕分ける→整理する" を工程化）
```
1. 貯める   collector/collect.py        watchlist→ sources/x/ に生ツイ(冪等)
2. 仕分ける brain/digest.py             ノイズ除外＋信号集計 → wiki/dashboards/signal.md
3. 整理(背骨) brain/build_entities.py   entity(token/player)を自動生成・更新（synthesis保持）
4. 整理(判断) ★エージェント工程         digest+entityを読み、concept を新規/更新。
              矛盾はingest時に両論併記、スコア更新、[[link]]張り、index/log更新。
```
1–3 はスクリプト（決定的）。4 は判断が要るのでエージェント(Claude)が回す＝これが
「定期的にエージェントが回す深い合成」。**手作業の一回こっきりではなく、再実行で複利**。

> ⚠️ **4は省略不可（CLAUDE.md 憲法 指針3）**。1–3だけ自動で回して4を放置すると、これは
> LLM Wikiではなく**ただのスクレイパー**になる。収集(1)と合成(4)は両輪。
> **健康の物差し＝未合成 backlog 件数**（`wiki/_worklist.md` の残り）。増え続けるなら収集過多のサイン
> ＝収集を間引いて合成を回す。intake量で測らない。

## faithful の要点（プロダクトに合わせてパターンを曲げない）
- **収集は門付き（watchlist）＝firehose禁止。収集と合成は両輪**（CLAUDE.md 憲法 指針2・3）。
- 合成は一度きり→以後維持（毎クエリ再導出のRAGとは違う）。
- 矛盾は消さず**取り込み時**に両論併記（例: [[$SPCX]] の強気/ショート両論）。
- entityは"参照される度に更新"＝新ツイ取込後に 2→3 を再実行すれば波及する。
- crypto固有(ticker/動線/6軸思想)は"中身"として正しい構造の中に置く。構造はKarpathy準拠。

## 運用
```bash
python3 collector/collect.py --source twitterapi   # 1. 収集
python3 brain/digest.py                             # 2. 仕分け
python3 brain/build_entities.py                     # 3. entity背骨(synthesis保持)
# 4. エージェントが digest/entity を読んで concept を合成・更新 → commit
```
