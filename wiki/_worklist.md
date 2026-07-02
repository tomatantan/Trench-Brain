---
type: worklist
title: ingest worklist
updated: 2026-07-02
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **8313件**（基準時刻 2026-07-02T10:16Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**360ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 12 | 7 | 64 | 1913♥ @WatcherGuru: JUST IN: 🇯🇵 Metaplanet buys 2,823 Bitcoin worth $1 / 574♥ @blknoiz06: OK you got me. i'm long $BTC right now  new quarte |
| [[$ETH]] | 11 | 3 | 81 | 3864♥ @zhusu: mental math with $eth will be a lot easier when it / 1820♥ @lookonchain: Update: #Bybit bought another  34,743 $ETH($97.7M) |
| [[$SPCX]] | 2 | 2 | 6 | 101♥ @MEXC: Not all buying is driven by investors.  Some follo / 30♥ @DefiIgnas: For crypto to pump again, retail needs to stop mak |
| [[$GRAM]] | 2 | 2 | 5 | 189♥ @HyperliquidX: By community request, you can now long or short $G / 108♥ @cryptocom: A brand new event has launched in Airdrop Arena!   |
| [[$ANSEM]] | 2 | 2 | 4 | 83♥ @Ministerr: Grifting KOLs will use this opportunity to try to  / 62♥ @DefiIgnas: $ANSEM is a fascinating example of tokenized atten |
| [[$TRIPLET]] | 2 | 2 | 2 | 117♥ @Crypto_Alch: How $TripleT looking this morning   Gas it  / 26♥ @PumpfunEco: $TripleT is rallying, up 23% past 6 hours 👀  |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$USDT]] | 3 | 1 | 12 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |
| [[$PUNCH]] | 2 | 1 | 8 | 28♥ @daisuk_e4: The team is working tirelessly, sacrificing sleep. / 18♥ @daisuk_e4: 上場まだでしょうか、、？  $punch |
| [[$WORLD]] | 2 | 1 | 7 | 518♥ @PumpfunEco: JUST IN: $world hits a new all-time high of $10.7M / 205♥ @PumpfunEco: This trader is up $93,000 after buying $136 worth  |
| [[$LAB]] | 2 | 1 | 2 | 24♥ @MurphyBTC: 🚨 $LAB に珍しいサインが出現‼️  これは暴走モードの準備段階に出現する演出で、前回暴走モード / 19♥ @MurphyBTC: #仮想通貨   急騰・急落AI検知システム #MAGU   $LAB に珍しいサインが出現してから2 |
| [[$UWU]] | 2 | 1 | 2 | 111♥ @dxrnell: The deeper I go down the $UwU rabbit hole  The har / 28♥ @dxrnell: The $UwU chart is undeniably strong, especially wh |
| [[$SOL]] | 1 | 1 | 15 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 1568♥ @lookonchain: Someone created a new wallet and spent 7,156 $SOL( |
| [[$ASTEROID]] | 1 | 1 | 13 | 140♥ @solbrdl: Happy international $ASTEROID day  Also noticed so / 132♥ @solbrdl: One day we will watch back at these prices and lau |
| [[$USDC]] | 1 | 1 | 13 | 2349♥ @rajgokal: absolutely thrilled that @visa has chosen @solana  / 1826♥ @DefiIgnas: We learned that $USDC is backed by cash held in ba |
| [[$GYM]] | 1 | 1 | 11 | 171♥ @PumpfunEco: Ansem (@blknoiz06) just bought $1,000 of $CLAW & $ / 90♥ @PumpfunEco: Ansem (@blknoiz06) just bought $1,000 of $CLAW & $ |
| [[$MITCH]] | 1 | 1 | 9 | 373♥ @PumpfunEco: $MITCH surges 679% after Ansem's post calling for  / 51♥ @ShapeFN_: When she doesn’t believe $MITCH will 100x, but you |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- [[$GRAM]]（48h 2件/2アカ・総5）まだconcept無し → 動線/型を検討
- [[$TRIPLET]]（48h 2件/2アカ・総17）まだconcept無し → 動線/型を検討

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 511 |
| [[@badattrading_]] | 238 |
| [[@CoinMarketCap]] | 227 |
| [[@laurashin]] | 193 |
| [[@DEG_2020]] | 171 |
| [[@Ministerr]] | 159 |
| [[@Lightspeedpodhq]] | 146 |
| [[@blknoiz06]] | 146 |
| [[@JasonYanowitz]] | 145 |
| [[@RyanSAdams]] | 138 |
| [[@milesdeutscher]] | 133 |
| [[@KyleSamani]] | 132 |
| [[@coin_post]] | 131 |
| [[@FrankDeGods]] | 126 |
| [[@DefiIgnas]] | 125 |
