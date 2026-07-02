---
type: worklist
title: ingest worklist
updated: 2026-07-02
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **8217件**（基準時刻 2026-07-02T06:10Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**370ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 10 | 4 | 63 | 690♥ @lookonchain: BlackRock just deposited another 4,984.56 $BTC($29 / 617♥ @coingecko: JUST IN: Strategy purchases another 520 Bitcoin fo |
| [[$ETH]] | 9 | 3 | 80 | 3864♥ @zhusu: mental math with $eth will be a lot easier when it / 1865♥ @lookonchain: Karma hit fast.  Hacker steals 2,930 $ETH($5.4M) f |
| [[$ANSEM]] | 3 | 2 | 6 | 174♥ @bull_bnb: It doesn't matter how they're pumping $ANSEM. What / 119♥ @Ministerr: The $Ansem coin got all the grifters coming back t |
| [[$NEET]] | 2 | 2 | 3 | 243♥ @cookerbruski: similar to the way that $troll ranged for months,  / 165♥ @dxrnell: The $20M floor holding extremely well on $neet  Wo |
| [[$HOOD]] | 2 | 2 | 2 | 80♥ @coingecko: INSIGHT: $HOOD rose 8.1% after Robinhood successfu / 5♥ @defi_kay_: $HOOD event  -Hood chain live, tokenized stock tra |
| [[$BP]] | 2 | 2 | 2 | 449♥ @coingecko: $BP pumps 18.7% after Backpack EU secures MiCa and / 195♥ @DefiIgnas: How does one prepare for the next bull if you are  |
| [[$TESTIBULL]] | 2 | 2 | 2 | 305♥ @moonshot: testibull ($TESTIBULL) is now verified on Moonshot / 153♥ @dxrnell: So what’s the plan here  Rotate $testibull profits |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$USDT]] | 3 | 1 | 12 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |
| [[$PUNCH]] | 2 | 1 | 8 | 28♥ @daisuk_e4: The team is working tirelessly, sacrificing sleep. / 18♥ @daisuk_e4: 上場まだでしょうか、、？  $punch |
| [[$WORLD]] | 2 | 1 | 7 | 518♥ @PumpfunEco: JUST IN: $world hits a new all-time high of $10.7M / 205♥ @PumpfunEco: This trader is up $93,000 after buying $136 worth  |
| [[$HYPE]] | 2 | 1 | 6 | 347♥ @lookonchain: The #a16z-linked whale that previously accumulated / 195♥ @DefiIgnas: How does one prepare for the next bull if you are  |
| [[$LAB]] | 2 | 1 | 3 | 174♥ @bull_bnb: It doesn't matter how they're pumping $ANSEM. What / 24♥ @MurphyBTC: 🚨 $LAB に珍しいサインが出現‼️  これは暴走モードの準備段階に出現する演出で、前回暴走モード |
| [[$SOL]] | 1 | 1 | 15 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 1568♥ @lookonchain: Someone created a new wallet and spent 7,156 $SOL( |
| [[$ASTEROID]] | 1 | 1 | 13 | 140♥ @solbrdl: Happy international $ASTEROID day  Also noticed so / 132♥ @solbrdl: One day we will watch back at these prices and lau |
| [[$USDC]] | 1 | 1 | 13 | 2349♥ @rajgokal: absolutely thrilled that @visa has chosen @solana  / 1826♥ @DefiIgnas: We learned that $USDC is backed by cash held in ba |
| [[$GYM]] | 1 | 1 | 11 | 171♥ @PumpfunEco: Ansem (@blknoiz06) just bought $1,000 of $CLAW & $ / 90♥ @PumpfunEco: Ansem (@blknoiz06) just bought $1,000 of $CLAW & $ |
| [[$MITCH]] | 1 | 1 | 9 | 373♥ @PumpfunEco: $MITCH surges 679% after Ansem's post calling for  / 51♥ @ShapeFN_: When she doesn’t believe $MITCH will 100x, but you |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- [[$NEET]]（48h 2件/2アカ・総7）まだconcept無し → 動線/型を検討

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 493 |
| [[@badattrading_]] | 219 |
| [[@CoinMarketCap]] | 217 |
| [[@laurashin]] | 193 |
| [[@DEG_2020]] | 164 |
| [[@Ministerr]] | 159 |
| [[@Lightspeedpodhq]] | 146 |
| [[@JasonYanowitz]] | 145 |
| [[@blknoiz06]] | 143 |
| [[@RyanSAdams]] | 138 |
| [[@milesdeutscher]] | 132 |
| [[@KyleSamani]] | 132 |
| [[@FrankDeGods]] | 126 |
| [[@coin_post]] | 126 |
| [[@DefiIgnas]] | 125 |
