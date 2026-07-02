---
type: entity
kind: token
title: $SPCX
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 40
accounts: 18
---

# $SPCX

> 自動生成(brain/build_entities.py)。言及 40件 / 18アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連する concept ページ。

## 言及アカウント
[[@0xFunX]] [[@AdimsSHOGUN]] [[@CryptoHayes]] [[@DEG_2020]] [[@DefiIgnas]] [[@MEXC]] [[@MurphyBTC]] [[@WatcherGuru]] [[@coingecko]] [[@coinkeiba]] [[@cryptocom]] [[@dxrnell]] [[@lookonchain]] [[@nansen_ai]] [[@solbrdl]] [[@spyzer]] [[@thedefiedge]] [[@theunipcs]]

## 共起トークン
[[$MU]] [[$NVDA]] [[$SPCS]] [[$GOOGL]] [[$TSLA]] [[$DOGE]] [[$USELESS]] [[$ASTEROID]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 6,182 | [[@WatcherGuru]] | JUST IN: Elon Musk's SpaceX $SPCX falls 10.5%, erasing over $250 billion from its ma | [[WatcherGuru__2069071268905701414]] |
| 779 | [[@WatcherGuru]] | JUST IN: Elon Musk is down $150 billion from his net worth today after SpaceX $SPCX  | [[WatcherGuru__2069188912619081898]] |
| 458 | [[@coingecko]] | NEWS: $SPCX falls 17.8%, erasing most of its gains since its market debut. | [[coingecko__2069288716133425284]] |
| 390 | [[@theunipcs]] | i haven't tweeted about any other memecoin except $USELESS in ages  but $DOGE feels  | [[theunipcs__2066818467639017607]] |
| 278 | [[@CryptoHayes]] | $SPCX IPO pop indicating +17%, is that enough to keep the AI dream alive? | [[cryptohayes__2064196537908085090]] |
| 278 | [[@CryptoHayes]] | $SPCX IPO pop indicating +17%, is that enough to keep the AI dream alive? | [[CryptoHayes__2064196537908085090]] |
| 259 | [[@CryptoHayes]] | Happy Friday the $SPCX  IPO edition. Can Barron von Elon save the market? | [[CryptoHayes__2065237665440804899]] |
| 258 | [[@CryptoHayes]] | Happy Friday the $SPCX  IPO edition. Can Barron von Elon save the market? | [[cryptohayes__2065237665440804899]] |
| 228 | [[@DefiIgnas]] | Crypto PTSD tells me $SPCX will end up as crypto hyped low-float/high-FDV token laun | [[DefiIgnas__2065716814169202728]] |
| 222 | [[@DefiIgnas]] | Crypto PTSD tells me $SPCX will end up as crypto hyped low-float/high-FDV token laun | [[defiignas__2065716814169202728]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）
- **⚠️カテゴリ（正確に。"RWA"単独は誤り）**: $SPCX は単一資産でなく **SpaceX株エクスポージャーを束ねた傘ティッカー**で、中身は**別リスクの2 instrument**:
  - **(1) 合成 perp / 先物**＝株の裏付けを持たない**デリバティブ（RWAではない）**。[[@thedefiedge]]「#1 Synthetic perps＝レバ/ショート用」([[thedefiedge__2067291214614089780]]) / [[@nansen_ai]]「Perps powered by [[@HyperliquidX]]」([[nansen_ai__2067598994675827014]]) / [[@MEXC]] Futures / [[@DefiIgnas]] のOI。**trench の出来高・KOL言及の主流はこちら**。リスク＝funding / 清算 / オラクル価格。型は [[perp-dex-wars]]。
  - **(2) tokenized spot 株**＝**こちらが RWA**（real-share-backed を称する）。[[@cryptocom]]「tokenized stock」4%利回り([[cryptocom__2067548618341384397]]) / [[@Backpack]]・@sunrisedefi が Solana で発行([[AdimsSHOGUN__2068599540115202320]]) / [[$BP]] が listing後 Solana の spot equities 出来高50%超([[golocojp__2067815287840448859]]) / [[@MEXC]]「real share ownership」。リスク＝ペッグ / 裏付け / カストディ（**backing は未検証**＝[[@DefiIgnas]] の low-float/high-FDV 懐疑の核）。型は [[external-event-to-token-pattern]] の RWA 側 [[spacex-ipo-narrative]]。
  - 共通: memecoin ではない＝**meme virality（lore/拡散）でなく株式メカニクス（float/lockup/valuation）と板で測る**。姉妹の純memecoinは別物の [[$ASTEROID]]。SpaceX はこの世界線で **IPO 済**（[[@theunipcs]]「successful SpaceX IPO」/ [[@thedefiedge]]「hottest listing」）＝未上場ではないが、上記2 instrument の別は残る。
- **板/フロー(数字で追う層)**: OI Binance$312.8M / Hyperliquid$309M([[@DefiIgnas]])、[[@MEXC]]先物日次800M $USDT、[[$BP]] が listing後 Solana の spot equities 出来高50%超捕捉。Tesla-run類推([[@solbrdl]])。
- **⚠️両論(未決)**:
  - 懐疑: [[@DefiIgnas]]「crypto流の低float/高FDVローンチに終わる」/ [[@theunipcs]]「$2.6T評価は高すぎ?」/ [[@coinkeiba]]「$SPCX買わず$TSLA集める・SpaceXは陰謀論でショート」
  - 強気: [[@0xFunX]]「初値割れ予想を覆した(150→176→161)」/ 取引所([[@MEXC]] [[@cryptocom]])の商品化
  - [[@CryptoHayes]]「AIの夢を保つに十分か / Barron von Elonが市場救うか」=マクロ皮肉
- **⚠️偽物ticker乱立**: [[$SPCXON]] [[$SPCXX]] [[$SPCS]] 等の類似が共起＝便乗/詐称の温床。CA確認必須(rug注意)。
- **賭け仮説**: 物語より板(OI/出来高/取引所採用)で追う。ショート勢も厚く一方向でない。confidence=中。

### 更新(2026-06-23): IPO pop 退潮→**ダンプ局面入り・ショート側が勝ちつつある**
- **事実**: [[@WatcherGuru]]「$SPCX -10.5%・1日で時価総額$250B超が蒸発」([[WatcherGuru__2069071268905701414]])。[[@lookonchain]]「long の whale 0x519c が -$1.2M で含み損」([[lookonchain__2069075414069428266]])。[[@MurphyBTC]]「急落中・ナンピン前に確認」([[MurphyBTC__2069072373333311840]])。
- **ショート勝者の出現**: [[@arkham]]「Trader VBVIT が crypto最大の SpaceX ショート。取引開始前に$6.3Mショート→avg$193で$28.9Mへ増し、7日で+$2.5M。generational trade になるか」([[arkham__2067721424148758536]])。[[@coinkeiba]] もショート利確([[coinkeiba__2067582673678409857]])。
- **機序が判明（DefiIgnas懐疑の裏付け）**: [[@MurphyBTC]]「IPO直後の低フロート相場＝買いたい人多・売れる株少→**ロックアップ解除で売り圧フェーズが来る**」([[MurphyBTC__2068891750563995653]])。＝上の[[@DefiIgnas]]「低float/高FDV」懐疑に**具体的な売り圧トリガ(lockup unlock)**が付いた。両論の弱気側が現実化しつつある。
- **perp 横断 ＋ ⚠️名称の混同に注意**: [[@frankdegods]] が「SPCX on HL vs Asteroid on ETH」「leveraged Asteroid (SPCX on Hyperliquid)」([[frankdegods__2066661633804448150]] / [[frankdegods__2066692613986553977]]) と書くが、**[[$ASTEROID]] は本来 SpaceX マスコット発の"別個の純memecoin"**（[[spacex-ipo-narrative]] の峻別）。frankdegods は両者を口語的に混同している可能性が高く、$ASTEROID=$SPCX のperp版と断定しない（CA未確認）。確実なのは $SPCX の板が [[perp-dex-wars]]（Hyperliquid/Binance のOI）に跨ること。[[@nansen_ai]] が SPCX 分析ツール提供([[nansen_ai__2067598994675827014]])＝tooling も追従。
- **示唆**: 「物語(IPO の夢) < 板(売り圧/lockup/OI)」がより鮮明に。**現時点の edge はショート/様子見側**。lockup 解除スケジュールが次の触媒。偽ticker乱立(下記)と合わせ、ロングは取引所RWA本物CAのみ・売り圧イベント前提で。confidence=中→やや弱気バイアス。

### 2026-06-23 更新②（同日 2 サイクル目）
- **観測（ダンプ続報）**: [[@WatcherGuru]]（2026-06-22）: 「JUST IN: Elon Musk is down $150 billion from his net worth today after SpaceX $SPCX falls **16%**. He is now worth $1.1 trillion」([[WatcherGuru__2069188912619081898]] 779♥)。前回観測（WatcherGuru 6,182♥ の -10.5%）から**さらに続落して -16% まで拡大**。1 日の時価総額蒸発額を Buffett の純資産（$145B）と比較する演出 = メディア・バイラル演出は残るが中身はダンプ継続。
- **強気 analogy（古信号）**: [[@solbrdl]]（2026-06-16）: 「$SPCX が Tesla の株式分割前の $200→$1,200 run を辿ったら？$ASTEROID は Shiba Inu レベルの 10 billion も」([[solbrdl__2066784174246117740]] 107♥) = Tesla-run 類比の楽観シナリオ。ただしこれは 6/16 = IPO 初期の強気言説。現在（-16%）の事実とは乖離。
- **⚠️ 示唆**: -10.5% → -16% の続落 ＋ long whale 含み損 -$1.2M（前回更新参照）= 弱気側がさらに優勢。WatcherGuru の数字はメディア計算（"Elon net worth" = $SPCX ではない）に注意するが、$SPCX の株価下落事実は確認。confidence=やや弱気（変化なし・強化）。

### 2026-06-23 更新③（同日 3 サイクル目）
- **観測（実世界イベント → meme 再燃）**: [[@dxrnell]]（2026-06-23T01:23）: 「The booster has safely landed $SPCX」([[dxrnell__2069229769166872837]] 35♥/8RT）。実際の SpaceX Falcon 9 ブースター着陸成功イベントをトークンのティッカーと絡めた投稿 = **リアルイベント → ミームキャタリスト型の拡散**（[[spacex-ipo-narrative]]のパターン通り）。likes は薄いが RT 比（8RT/35♥）はやや高く、拡散ベクトルは残る。
- **観測（coinkeiba の TSLA 優先、2026-06-17）**: [[@coinkeiba]]「$SPCX 買わずに淡々と $TSLA 集めてる」([[coinkeiba__2067223580837106022]] 107♥) = 「$SPCX を買わずに原資産である $TSLA を直接集める」という**equity-first の合理化戦略**。既存の coinkeiba ショート利確（ショートで稼ぐ）とは別の立場: "underlying を集める方が賢い" という判断。この立場は**「合成 perp/tokenized spot よりも本物の株を」**という最も真っ当な反論。
- **示唆**: ダンプ継続（-16%）の中で、①実世界イベントによる meme 再燃試み（dxrnell）と②原資産回帰の合理化（coinkeiba/TSLA 優先）という 2 つの対応が並行。meme 再燃は短命の可能性が高い（板/売り圧に対抗できるほどの likes ではない）。confidence=やや弱気（変化なし）。

### 2026-06-23 更新④（同日 4 サイクル目）
- **観測（価格マイルストーン：全騰幅消去）**: [[@coingecko]]（2026-06-23T05:12Z）: 「NEWS: $SPCX falls 17.8%, erasing all of its gains since its market debut.」([[coingecko__2069287524254482595]] 14♥)。前回観測（WatcherGuru -16%）からさらに続落し、**上場初日からの全上昇幅を消去**。-10.5% → -16% → -17.8% の連続下落が CoinGecko ニュース feed で確認された。
- **[[@MEXC]]（2026-06-23T05:00Z）**: $SPACEX(PRE) の 0-Fee キャンペーン広告（[[MEXC__2069284313808646519]]）= 取引所プロモ継続だが、$SPCX 本体ではなく PRE 商品。信号として独立性なし。
- **示唆（判断）**: [[@CryptoHayes]]「9月 unlock = low float high FDV shitcoin」（2026-06-22）の thesis が **unlock 前の現在時点で既に全騰幅消去**として実現しつつある。DefiIgnas の「低 float / 高 FDV」懐疑 + MurphyBTC の「lockup 解除で売り圧フェーズ」という論理の前半が今証明された。残るのは 9 月 unlock 以降の売り圧が追加でどれほどか。既存の強気サイド（「初値割れ予想を覆した」[[0xFunX]]・Tesla-run 類比 [[solbrdl]]）は全騰幅消去で根拠消失。
- **⚠️ MEXC の $SPACEX(PRE) とは分けて考える**: MEXC 広告は先物（perp）商品ラインの継続。$SPCX 本体の株価が -17.8% でもデリバティブ取引所は存続する（[[perp-dex-wars]]の観点では板・流動性が生き続ける可能性）。ただし underlying が全騰幅消去なら perp の強気 funding は剥落方向。
- **confidence = 弱気（更に強化）**。[[spacex-ipo-narrative]] の「外部イベント→フィーバー→ダンプで全消し」完結パターン確定へ近づいている。

### 2026-06-24 確認（新 beat なし）
- worklist 代表ツイ「$SPCX falls 17.8%」([[@coingecko]] 458♥) は更新④で既合成済。[[@MEXC]]「Every pullback creates a new question」(37♥) は取引所プロモ = 独立信号なし。本サイクルの新 beat なし。既存合成（全騰幅消去・弱気強化）に変化なし。

### 2026-06-27 確認（新 beat なし・instrument 分類再確認）
- worklist 代表の [[@MEXC]] 2件＝「Every pullback creates a new question（$SPCX is down from its post-IPO highs）」(134♥, [[MEXC__2069348737064026145]]) と「Earn deposit/spin で $NVDA $GOOGL $SPCX が当たる」(107♥, [[MEXC__2069269215534883003]]) は **いずれも取引所プロモ＝独立 signal なし**。前者は post-IPO 高値からの下落を認める設問形だが新情報なし。
- **instrument 分類は不変（再確認済）**: $SPCX = 傘ティッカー[合成 perp/futures（非RWA, MEXC/Hyperliquid/Binance）＋ tokenized spot 株（RWA claim, Backpack/SunriseDeFi/cryptocom, **backing 未検証**）]。[[spacex-ipo-narrative]] の2系統対比と整合。新規 instrument の登場なし。
- 既存合成（全騰幅消去・lockup 売り圧・弱気バイアス）に変化なし。confidence=弱気（維持）。

### 2026-06-28 更新（新 beat: MurphyBTC のロックアップ解除スケジュール・数字で追う）
出典: [[MurphyBTC__2068114102682038366]]（25♥・2026-06-19T23:30Z）

**観測（ロックアップ解除スケジュール・SEC資料ベース）**
[[@MurphyBTC]] が SEC 資料に基づいた詳細な解除スケジュールを整理（前回合成で「lockup 解除で売り圧フェーズが来る」と抽象的に記録していた内容の具体化）:
- 2026年8月頃: Q2 決算後 **最大 20% 解除**（Public Offering Date Shares の最大 20%・条件次第で追加 10% の余地）
- 2026-08-21: +7%
- 2026-09-10: +7%
- 2026-09-25: +7%
- 2026-10-10: +7%
- 2026-10-25: +7%
- 2026年11月頃: Q3 決算後 **+28% 解除**
- 2026-12-09: **残り全株解除**
- 2027-06-13: **Elon Musk および主要株主**のロックアップ解除

**試算（MurphyBTC の計算）**:
- 現在の $SPCX 売買代金: 約 $50.3B（約8.1兆円）
- 20% 解除分を全部吸収するために必要な需要: $354B〜$524B（現在売買代金の **7〜10 倍**）
- これは「解除分が全部売られる」という極端な前提だが、需給のオーダー感を示す。

**⚠️ 判断（更新）**:
- 前回合成「9月 unlock = low float high FDV 論の前半が既に証明」（全騰幅消去）に続き、今後の弾は **2026-08/09（+20%+7%+7%）** に集中。夏場の供給増加フェーズが近い。
- $SPCX 株価が現在「全騰幅消去」水準（[[coingecko__2069288716133425284]] 458♥ = -17.8%）であっても、ロックアップ解除後の **7〜10 倍の需要** を必要とする計算は、現在の板では到底吸収できない規模感。
- 既存合成の弱気バイアスを**更に具体的日程で裏付け**。confidence=弱気（維持・スケジュール追加で確度↑）。
- 接続: [[spacex-ipo-narrative]]（IPO → ロックアップ → 売り圧フェーズのライフサイクル）/ [[external-event-to-token-pattern]]（解除日=カタリスト）。

### 2026-06-28 確認（新 beat なし・MEXC USD1-M futures 継続確認）
- [[@MEXC]] (2026-06-26): USD1-M Futures に $SPCX を追加（$MU / $SP500 / $NAS100 / $ARM と併列、[[mexc__2070416779948568669]] 26♥）= 取引所プロモ・独立信号なし。ただし perp 取引所が **$SPCX を株式系 futures ライン**として継続提供している事実 = 株価が全騰幅消去済みでも perp 板は生存（[[perp-dex-wars]]上の plate 継続）。
- [[@spyzer]] (2026-06-12T15:55Z): 「$SPCX gonna be an interesting study case considering launch dynamics」([[spyzer__2065462914383859910]] 21♥) = IPO 直後（6/12）の薄い観察。launch dynamics への着目のみ = 本サイクルで既合成の「DefiIgnas の低 float/高 FDV」「MurphyBTC の lockup 売り圧」に対し新情報なし。likes 21♥・thin。
- 既存合成（全騰幅消去・lockup 解除スケジュール 2026年8月〜12月・弱気バイアス）に変化なし。confidence=弱気（維持）。

### 2026-06-28 確認②（worklist 代表ツイ確認・DEG_2020「値固め？」・nansen_ai promo）
出典: [[deg_2020__2070086212967440890]]（8♥・2026-06-25T10:06Z）/ [[nansen_ai__2068950016430072308]]（11♥・2026-06-22T06:51Z）

**観測（事実）**:
- [[@DEG_2020]]（2026-06-25T10:06Z）: 「$SPCX 値固めに入った？」（8♥）= チャートリンク付きで「値固め（consolidation）に入ったか？」という疑問形の観測。全騰幅消去（-17.8%）後の価格動向への JP KOL の着目。内容は問いかけのみ = 独立の強気/弱気 signal としての強度は低い。
- [[@nansen_ai]]（2026-06-22T06:51Z）: 「Trading $SPCX? Perps on Nansen are powered by @HyperliquidX and @tradexyz. 🎟️ Every $10,000 in perps volume = 1 raffle ticket. 💎 100 winners every week, $1,000 USDC each.」（11♥）= perp 取引所プロモ（raffle キャンペーン）= 独立信号なし。ただし perp ツーリングが SPCX に特化した raffle を組んでいる事実 = 板・出来高ベースのエンゲージが一定存在することの傍証。

**⚠️ 判断（light-touch）**:
- DEG_2020「値固め？」は全騰幅消去後の横ばいに対する JP KOL の観察。8♥ = 極小エンゲージ・signal 強度低。lockup スケジュール（2026年8月〜）が迫る中での「値固め」は、むしろ lockup 前の一時的な需給均衡（強気サインでなく静止状態）の可能性が高い。
- 既存合成（全騰幅消去・lockup スケジュール・弱気バイアス）に変化なし。confidence=弱気（維持）。

### 2026-07-02 更新（新 beat: Nasdaq-100 組み入れ Jul 7 / DefiIgnas マクロ回帰論）
出典: [[mexc__2072243817516769510]]（101♥・2026-07-01T09:00Z）/ [[defiignas__2072618892610945190]]（30♥・2026-07-02T09:50Z）

**観測（事実）**:
- [[@MEXC]]（2026-07-01）: 「Not all buying is driven by investors. Some follows an index. $SPCX joins the Nasdaq-100 on Jul 7, which means index funds are expected to rebalance. Do you hold a Nasdaq-100 ETF?」= **$SPCX が 2026-07-07 に Nasdaq-100 へ組み入れ予定**。指数連動ファンドの強制的なリバランス買い需要が発生する見込み。
- [[@DefiIgnas]]（2026-07-02）: 「For crypto to pump again, retail needs to stop making money elsewhere. It's happening: KOSPI dumped 7.9% today, -18% from ATH(+85% YTD でまだ余地あり) / Gold -27% and silver -50% from records / $NVDA -16%, $MU -18%, and **$SPCX can't even manage a disbelief rally** / Korean retail, historically crypto's most degen crowd, rotated into KOSPI this cycle. That trade is breaking now. / Sidelined money has to go somewhere. Or this is one big risk-off and everything dumps together.」= SPCX の不振をマクロ文脈で位置付けるフレーミング。

**判断**:
- **Nasdaq-100 組み入れ（Jul 7）**: 既合成「全騰幅消去（-17.8%）・lockup 解除スケジュール（2026 年 8 月〜）・弱気バイアス」の中で、**一時的な買い需要の触媒**。パッシブ運用（ETF・インデックスファンド）は銘柄組み入れ時にルール上 $SPCX を購入せざるを得ない＝**需要の質は "指数への強制リバランス"** であり投資判断に基づく需要ではない。MEXC の演出は取引所プロモ（「あなたは Nasdaq-100 ETF を持っているか？」= 既 $SPCX 保有ルートの暗示）。ただし組み入れ直前の需給的な価格押し上げ効果は存在しうる（典型的な「組み入れ前買い・後売り」）。
- ⚠️ **「強制リバランス≠ファンダ改善」**: 既合成「lockup 解除（2026-08〜）が 7〜10 倍の需要を必要」という計算の前で、Nasdaq-100 組み入れによるパッシブ買いが吸収バッファになるかは規模次第。DefiIgnas が「disbelief rally すら起きない」と評する通り、$SPCX は全騰幅消去後もモメンタムが立っていない状態。
- **DefiIgnas マクロ論**: 「KOSPI/Gold/NVDA/MU が同時に崩れ、Korean retail の alternative trade が崩壊しつつある → crypto に戻る条件が整いつつある」。その文脈で $SPCX を「反発すら起きない」と評する = $SPCX を **crypto 内の弱い輪（macro recovery に乗れない銘柄）** と位置付け。「全部まとめてリスクオフで沈む」可能性も明示。
- **既存合成との接続**: DefiIgnas の「SPCX can't manage a disbelief rally」は既合成「全騰幅消去・弱気バイアス（confidence=弱気）」の最新確認として整合。Nasdaq-100 組み入れ（Jul 7）の前後で一時的な反発が起きるかを監視ポイントとして追加。それ以降は lockup スケジュールに戻る（既合成）。confidence=弱気（維持・Jul 7 周辺の需給イベントを注視）。
- 接続: [[spacex-ipo-narrative]]（組み入れ後の需給パターンは「外部イベント→一時的資金流入→剥落」の変種）/ [[majors-rotation-supercycle]]（DefiIgnas: KOSPI/Gold 崩壊 → crypto rotation 条件形成の文脈で $SPCX が「乗れない」銘柄として位置付け）/ [[perp-dex-wars]]（MEXC は組み入れを perp 取引促進のネタに転用）。
<!-- synthesis:end -->
