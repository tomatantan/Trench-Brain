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
- tokens/ — $ticker毎（42件）。例: [[$SPCX]] [[$ASTEROID]] [[$ARX]] [[$JSON]]
- players/ — @アカウント毎（120件）。例: [[@solbrdl]] [[@CryptoHayes]]

## 概念ページ（concepts）★横断合成＝判断/動線/型。
- [[reflexivity]] — ★★根本エンジン(古典[[canon]]/Soros): 価格↔ナラティブの自己強化。memecoin=ファンダ無し=reflexivityが裸で全部。pump/death/rotationの下にある共通機械。traction=燃料計
- [[external-event-to-token-pattern]] — ★型: 外部イベント→token（再現プレイブック・政治サブ型あり）
- [[spacex-ipo-narrative]] — ★動線: SpaceX IPO → [[$SPCX]]/[[$ASTEROID]]
- [[majors-rotation-supercycle]] — ★動線: メジャー・ローテ（BTC→ETH→alt）/スーパーサイクル説（⚠️zhusu逆指標）
- [[jp-meme-cluster]] — ★型: 日本コミュ meme クラスタ（[[$KINTON]]×[[$YAJUCOIN]] 相互保有で束ねる）
- [[onchain-verification]] — ★型: オンチェーン裏取り（言説 vs 実際の資金。[[@lookonchain]]＝検証装置／perp OIで先回り）
- [[launchpad-economics]] — ★型: launchpad経済圏（[[$PUMP]]/Pump.fun＝memeの供給工場・⚠️graduation 1.5%）
- [[survivor-memes]] — ★型: 生存者meme（[[$BONK]]/[[$WIF]]/[[$PEPE]]等・⚠️生存者バイアス）
- [[l1-substrate-wars]] — ★動線: L1基盤戦争（Solana vs Ethereum＝memeが乗る地面）
- [[vc-founder-thesis-layer]] — ★型: VC/創業者の思想層（[[@cdixon]]/[[@saylor]]＝ナラティブ最上流の土台）
- [[ai-memes]] — ★型: AI-meme（トークン＝自律エージェントの配布層・[[$FARTCOIN]]・⚠️自律の主張と実体の差）
- [[perp-dex-wars]] — ★動線: perp DEX戦争（[[$HYPE]]一強 vs 群雄・⚠️buyback燃料は清算retail）
- [[regulation-catalyst]] — ★動線: 規制/政策→trench（GENIUS/FIT21・SEC・Trump政策・⚠️発表≠実行）
- [[rug-anatomy]] — ★型: rugの解剖（[[$LIBRA]]・赤旗チェックリスト＝screeningの入力・実用edge寄り）

## 要約ページ（summaries）
- ツイートは原子的なので source note 自体が summary を兼ねる（sources/x/）。長文ソース(news等)取込時に作成。
- [[bankless-arthur-hayes-ai-crash-bitcoin-1m-2026-06-22]] — [[@CryptoHayes]] AI bubble thesis / ETH setup / perp起源 / BTC $1M causal chain（2026-06-22）
- [[bankless-world-cup-polymarket-2026-06-19]] — W杯チケット × Polymarket IRL ヘッジ事例（2026-06-19）

## クエリ（queries）
- （まだ無し）
