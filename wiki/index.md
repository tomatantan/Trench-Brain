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

## エンティティ（entities）★事実の自動集約層。token は全合成済(質◎)。**player は高signalから順次合成中（多くは未記入stub＝観測のまま・低signalは合成しない＝観測≠採用）**。判断は合成メモ＋concept。
- tokens/ — $ticker毎（50件）。例: [[$SPCX]] [[$ASTEROID]] [[$ARX]] [[$JSON]] / traction 採用(追跡中): [[$PACMON]]（2窓） [[$PUMPBULL]]（10窓） [[$KIDGRIN]]（3窓） [[$IMBACK]]（8窓） [[$TRUMPCUP]]（6窓・Trump系唯一） [[$VIREO]]（8窓） [[$ORBIT]]（2窓） [[$TEXE]]（再入場・⚠️exit不可逆仮説反証） / 脱落(12窓・T3未着火): [[$TRUMPUNC]] / 脱落(11窓・T3未着火): [[$ciarra]] / 脱落(9窓・T3未着火→再入場): [[$TEXE]] / 脱落(10窓・T3未着火): [[$MORPH]] / 脱落(7窓・T3未着火): [[$SHARKCASH]] / 脱落(live price未確認): [[$BRUH]] [[$GLX]] / 縮退確定: [[$CITTA]]
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
- [[manipulation-playbook]] — ★型: 魔界social手口（pumper exit/bot投票campaign/借用ナラ＝/checkが検出する"乗せられ方")
- [[predictive-study]] — ★実証: 死の分母data N=99 で「何が運命を分けるか」（peak<10k=100%死/graduated×tr無70%/traction有18%＝/checkの予測重み）
- [[ape-or-avoid]] — ★capstone: 全概念を「乗るか避けるか」1判断に束ねる決定フレーム（reflexivity→base-rate→予測因子→手口→KOL信頼性→live・/checkの知識側）
- [[early-lowcap-entry]] — ★早期層: 卒業前low-capを「危険一律」でなく評価（mcap velocity/organic traction初動/theme-fit/最初のKOL＝早期の中で生存を分ける・本人指摘から合成）
- [[launch-pulse]] — ★観測: ローンチの流れ合成（pump非scam flow・死の分母・テーマ分布・KOL standout）

## player 思考の型（view-engine 燃料）

## 要約ページ（summaries）
- ツイートは原子的なので source note 自体が summary を兼ねる（sources/x/）。長文ソース(news等)取込時に作成。
- [[bankless-ai-crackdown-internet-2026-06-23]] — Illia Polosukhin (Near Protocol) × Bankless: Fable 輸出規制 / AI 国有化 / 分散型 AI "full sovereign mode"（⚠️ 創業者ポジション最大）（2026-06-23）
- [[bankless-arthur-hayes-ai-crash-bitcoin-1m-2026-06-22]] — [[@CryptoHayes]] AI bubble thesis / ETH setup / perp起源 / BTC $1M causal chain（2026-06-22）
- [[bankless-world-cup-polymarket-2026-06-19]] — W杯チケット × Polymarket IRL ヘッジ事例（2026-06-19）

## クエリ（queries）
- [[where-in-reflexive-cycle-2026-06-23]] — 今 trench は再帰サイクルのどこ＆edgeはどこか（古典×YouTube×X×pump 横断合成・§5実演）
