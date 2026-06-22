# Index — Trench-Brain カタログ

全ページの目次。ingest/lint時にエージェントが更新する。

## 運用（config）
- [[watchlist]] — 監視アカウント watchlist（収集の入口）
- collector/ — 「貯める仕組み」。syndication/twitterapiでwatchlistをポーリング→ sources/x/ に生ツイ保存
- brain/digest.py — 「仕分ける仕組み」。生ツイのノイズ除外＋信号集計

## ダッシュボード（dashboards）
- [[signal]] — Signal digest（ホットticker/活発アカ/高エンゲージ抜粋）

## 取り込みTODO
- [[_worklist]] — ingest worklist（エージェントが処理する増分TODO）

## エンティティ（entities）★LLM Wikiの背骨＝事実の集約。brain/build_entities.py が自動生成・更新。判断は各ページの合成メモ＋concept。
- tokens/ — $ticker毎（40件）。例: [[$SPCX]] [[$ASTEROID]]
- players/ — @アカウント毎（120件）。例: [[@solbrdl]] [[@CryptoHayes]]

## 概念ページ（concepts）★横断合成＝判断/動線/型。
- [[external-event-to-token-pattern]] — ★型: 外部イベント→token（再現プレイブック）
- [[spacex-ipo-narrative]] — ★動線: SpaceX IPO → [[$SPCX]]/[[$ASTEROID]]

## 要約ページ（summaries）
- ツイートは原子的なので source note 自体が summary を兼ねる（sources/x/）。長文ソース(news等)取込時に作成。

## クエリ（queries）
- （まだ無し）
