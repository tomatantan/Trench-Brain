---
type: concept
title: 型 — オンチェーン裏取り（言説 vs 実際の資金）
created: 2026-06-22
updated: 2026-06-22
tags: [trench, concept, pattern, on-chain, verification, discipline]
memetic_potential: —
confidence: 中〜高
---

# 型: オンチェーン裏取り（数字で言説を検証する）

trench の言説（KOLの強気・物語・「スマートマネー」ラベル）を、**オンチェーンの実際の資金移動で
裏取り/否定する**型。これは本wikiの中核規律＝[[CLAUDE.md|憲法]] 指針6「観測事実とLLM推論の分離」の
**運用ツール**そのもの。worklist で [[@lookonchain]](121) [[@arkham]] が活発化したことから合成。
「誰が言ったか」ではなく「**誰が実際にどう動いたか**」を一次に置く。

## 一致 / 乖離の3類型
**A. 一致 → 確信度↑（言葉と金が揃う）**
- [[@lookonchain]]: 「Arthur Hayes sold 2,373 $ETH($8.32M) a week ago at ~$3,507. 4 hours ago moved 10.5M $USDC to buy back at higher price」([[lookonchain__1954132632423588028]])＝[[@CryptoHayes]] の ETH 強気が実ポジで裏取りできる。
- 「James Wynn took 70 days 0→$87M, lost almost all in 5 days」([[lookonchain__1927726941710250013]])→「liquidated for 949 $BTC($99.3M)」([[lookonchain__1928259143120630038]])＝破滅の物語がオンチェーンで確認。

**B. 乖離 → grift/インサイダー検出（最強の危険警告）**
- **Trump World Liberty**: 「bought 67,498 $ETH at avg $3,259（~$210M）」→「sold 5,471 $ETH at $1,465」([[lookonchain__1909782070618210423]])＝「スマートマネー」物語と裏腹に**高値掴み→安値投げ**。
- **$TRUMP team**: 「team wallet deposited 10.13M $TRUMP($455M) into Binance in 24h」([[lookonchain__1880881930809508088]])＝「流動性供給」と語られるが実態は取引所への大量送金＝売り圧。([[$TRUMP]] の政治meme grift と接続)
- **MrBeast**: 「engaged in insider trading... made over $23M: $11.45M from $SUPER, $4.65M from $ERN」([[lookonchain__1851672470924988755]])。
- **$LIBRA/$MELANIA インサイダー**: 「laundering funds. Spent 19,846 $SOL($2.76M) to buy POPE(<$150K mcap), sold for $24K, funneled to other wallets」([[lookonchain__1894757929204813828]])＝意図的な loss-making wash。
- **W杯賭けリング**: 「3 wallets won all #WorldCup bets, all sent profits to same Binance address—likely same person」([[lookonchain__2068581320197021801]])＝独立を装った協調。

**C. 休眠の覚醒 → 供給の警告**
- 「Bitcoin OG holding 80,009 $BTC($8.69B) woke up after 14+ years dormancy」([[lookonchain__1941126810961653780]] / [[lookonchain__1941152575514198214]])＝潜在売り圧。
- 「$PEPE whale dormant 600 days transferred all 2.1T $PEPE($52M)... 1,900,000x return」([[lookonchain__1867760241070514287]])。

## 派生: 板（perp OI）で"物語の前に数字"を取る
[[@theunipcs]] の **perp open-interest シグナル論**＝言説でなく板で先回りする変種。
- 「[[$USELESS]] has higher OI-to-market-cap ratio than every other memecoin」([[theunipcs__2067625941585494256]])、
  「OI exceeds $DOGE/$SHIB/$PEPE/$BONK/$PENGU/$WIF on Binance perpetuals」([[theunipcs__2067854742701646135]])＝2023 $PEPE型パラの前兆と主張。
- ⚠️ **OI単独の限界**: [[@thedefiedge]] は perp OI を venue 比較で相対化（Hyperliquid $8.7B vs Phoenix $3.6M）＝OIは場所次第で予測力に差。板シグナルも"数字なら正しい"ではない。

## プレイヤー相関
- **観測装置**: [[@lookonchain]] [[@arkham]]（資金移動を時刻付きで報告）。
- **被検証側**: [[@CryptoHayes]]（言とポジが概ね一致）/ [[@blknoiz06]]（$TRUMP $6.83M損切り）/ Trump World Liberty（乖離）。
- **板シグナル派**: [[@theunipcs]]（OIで先回り）。

## ⚠️ この型自体の限界（観測と断定の線引き）
- [[@lookonchain]] の「insider」「laundering」認定は**wallet紐付けに基づく推定**を含む＝**移動（観測）**と**意図（断定）**は別物。本wikiでは移動を事実、意図ラベルは判断として分離して引用する。
- corpus には被検証KOL**本人の反論ツイが無い**＝一方の観測のみ。「乖離」は強い示唆だが一次の言い分も探す。

## 示唆 / 賭けの仮説
- **言説↔資金の"乖離"が最も信頼できる危険/売りシグナル**（team売り・インサイダー・grift）。逆に一致は確信度を上げる。
- 物語に乗る前に「発信者・team・whale の実際の資金フロー」を1枚噛ませる＝[[majors-rotation-supercycle]] のKOL強気も、[[external-event-to-token-pattern]] の meme も、この層で検算してから張る。
- これは [[external-event-to-token-pattern]] の「RWA側=板/数字で追う ／ meme側=物語で追う」の二分と同根。**数字で追う規律**を全concept共通の検算層に据える。
- 監視: [[@lookonchain]]/[[@arkham]] の team-deposit・dormancy覚醒・insider認定、主要memeの perp OI。

## 関連
- [[external-event-to-token-pattern]] / [[majors-rotation-supercycle]] / [[$BTC]] / [[$TRUMP]] / [[@lookonchain]] / [[@theunipcs]]
- 規律の出典: [[CLAUDE.md|憲法]] 指針6（観測と推論の分離）。集計の入口: [[signal|Signal digest]]

## 出典(生ソース)
[[@lookonchain]] Hayes ETH裏取り/World Liberty乖離/$TRUMP team $455M/MrBeastインサイダー/$LIBRA洗浄/W杯リング/BTC OG覚醒,
[[@arkham]] Andrew Tate清算連発, [[@theunipcs]] $USELESS perp OI, [[@thedefiedge]] OIのvenue差。
（全て sources/x/ の原ツイに保存済）
