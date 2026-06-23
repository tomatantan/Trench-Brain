---
type: entity
kind: token
title: $USDC
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 25
accounts: 4
---

# $USDC

> 自動生成(brain/build_entities.py)。言及 25件 / 4アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連 [[concepts]]。

## 言及アカウント
[[@BinanceUS]] [[@DefiIgnas]] [[@lookonchain]] [[@rajgokal]]

## 共起トークン
[[$ETH]] [[$SOL]] [[$USDT]] [[$LIBRA]] [[$BTC]] [[$USD1]] [[$WOJAK]] [[$LINK]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 4,455 | [[@lookonchain]] | A wallet named Ansem(@blknoiz06) sold 194,799 $TRUMP($6.83M) 2 hours ago, losing $2. | [[lookonchain__1881528883079709134]] |
| 3,764 | [[@lookonchain]] | Arthur Hayes(@CryptoHayes) sold 2,373 $ETH($8.32M) a week ago when the $ETH price wa | [[lookonchain__1954132632423588028]] |
| 3,000 | [[@lookonchain]] | Trump's World Liberty(@worldlibertyfi) just spent 20M $USDC to buy 6,041 $ETH at $3, | [[lookonchain__1880992881164623958]] |
| 2,801 | [[@lookonchain]] | North Korean hackers went long $ETH on #Hyperliquid, turning $476,489 into $18,187 — | [[lookonchain__1871138914226057482]] |
| 2,772 | [[@lookonchain]] | A whale spent 4,806 $ETH($21.25M) to buy 938,489 $LINK across 5 wallets 8 hours ago. | [[lookonchain__1956920547692122563]] |
| 2,558 | [[@lookonchain]] | Someone knew in advance that $LIBRA was going to be launched but bought too late, lo | [[lookonchain__1891340262326346071]] |
| 2,514 | [[@lookonchain]] | Never seen such smart addresses!  - Made $4.14M by trading $ETH during $USDC depeggi | [[lookonchain__1635179044475121665]] |
| 2,411 | [[@lookonchain]] | The $LIBRA team has cashed out $107M!😱  8 wallets related to the $LIBRA team have ob | [[lookonchain__1890619615883219455]] |
| 2,396 | [[@lookonchain]] | Trump's World Liberty(@worldlibertyfi) is buying $ETH, $LINK and $AAVE!  In the past | [[lookonchain__1867036708983935325]] |
| 2,349 | [[@rajgokal]] | absolutely thrilled that @visa has chosen @solana for high-performance blockchain se | [[rajgokal__1699030958580625452]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 観測（事実）
- trench における $USDC の登場パターンは「whale 行動の計量単位」に集中。直接 trade される観測はほぼなく、lookonchain が「誰が何をいくらで買ったか」を示す際の denomination として機能している（高エンゲージ言及10件中9件がこのパターン）。
- 具体的フロー: Trump の [[World Liberty Finance]] が 20M $USDC → $ETH 購入（3,000♥）、$LIBRA team が $107M キャッシュアウト（$USDC建て計上）。
- stablecoin depeg 事件: 「$USDC depegging 中にスマートアドレスが $4.14M 益」（2,514♥）= 過去の depeg をアーカイブとして保持。
- Visa × Solana: [[rajgokal]] が「@visa が @solana を high-performance blockchain settlement に採用」（2,349♥）= $USDC が ETH/SOL 基盤戦争の**得点板**になった瞬間。
- 共起トークン: [[$USD1]]（Trump系stablecoin）が存在する = 政治的競合 stablecoin との同一文脈が発生している。

### 判断（推論）
- $USDC は trench において**賭けの対象ではなく、資金フロー検証ツール**。[[onchain-verification]] の中核素材。lookonchain の言及数が多い理由は「whale 追跡コストが低い透明な通貨」だから。
- [[regulation-catalyst]] への直撃: GENIUS Act（stablecoin 制度化）が成立すれば $USDC のような USD-backed stablecoin が法的地位を得る最有力候補。ただし [[regulation-catalyst]] の「promises vs delivery」緊張が残る。
- [[l1-substrate-wars]]: Visa × Solana 採用は ETH の「settlement 基盤」主張（RyanSAdams「banks will issue stablecoins on Ethereum」）への**反例**。stablecoin settlement の覇権争いが L1 戦争の一戦線になっている。
- ⚠️ [[$USD1]]（Trump系）との競合: 同一 corpus に共起している = 政治的選好が stablecoin 選択に影響する可能性。「$USDC = 中立的 USD」の地位が政治化するリスク。
- 賭け仮説: GENIUS Act 成立 → stablecoin 制度化 → $USDC の機関採用拡大 → SOL/ETH どちらのチェーンで settlement が主流になるかが次の分岐点。

### concept 接続
[[regulation-catalyst]]（GENIUS Act・stablecoin制度化） / [[l1-substrate-wars]]（Visa×Solana の settlement 争い） / [[onchain-verification]]（whale追跡の計量単位） / [[$USD1]] / [[$ETH]] / [[$SOL]] / [[@lookonchain]] / [[@rajgokal]]
<!-- synthesis:end -->
