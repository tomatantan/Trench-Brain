---
type: worklist
title: ingest worklist
updated: 2026-07-02
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **7648件**（基準時刻 2026-07-02T06:10Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**358ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 14 | 6 | 67 | 990♥ @fundstrat: Crypto is a hyper volatile asset and some macro he / 723♥ @CredibleCrypto: I have a feeling our macro $ETH bottom at $1,500 i |
| [[$ETH]] | 13 | 6 | 84 | 3864♥ @zhusu: mental math with $eth will be a lot easier when it / 1870♥ @lookonchain: After $ETH broke above $4,200, trader 0xcB92 was f |
| [[$ANSEM]] | 10 | 7 | 17 | 774♥ @arkham: Ansem is up $75M on $ANSEM.  The pumpfun account “ / 716♥ @moonshot: The Black Bull ($ANSEM) is now verified on Moonsho |
| [[$TRIPLET]] | 7 | 3 | 7 | 179♥ @dxrnell: The “I’ve never seen $TripleT it’s a terrible coin / 177♥ @dxrnell: The $TripleT chart is simply lovely  |
| [[$SOL]] | 5 | 3 | 20 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 1568♥ @lookonchain: Someone created a new wallet and spent 7,156 $SOL( |
| [[$KINS]] | 6 | 2 | 9 | 214♥ @PumpfunEco: 24h volume leaders on pump fun 👀  $ANSEM $44.4M $F / 206♥ @Crypto_Alch: $KINS curling up for an onchain gaming season   CT |
| [[$DROOLING]] | 5 | 2 | 12 | 178♥ @Crypto_Alch: Last cycle we had a dog   This cycle the trenches  / 165♥ @Crypto_Alch: My Nigerian quant sent me this $drooling TA   That |
| [[$STRC]] | 4 | 2 | 10 | 11667♥ @saylor: Strategy announces a Digital Credit Capital Framew / 10724♥ @saylor: Income. Twice a month. $STRC  |
| [[$FARTCOIN]] | 4 | 2 | 4 | 306♥ @theunipcs: i actually care about other coins  i've been most  / 305♥ @theunipcs: $USELESS is up 15% today while $BTC makes fresh 22 |
| [[$MSTR]] | 3 | 2 | 11 | 11667♥ @saylor: Strategy announces a Digital Credit Capital Framew / 389♥ @CredibleCrypto: With today's move the can has been kicked down the |
| [[$WOJAK]] | 2 | 2 | 8 | 330♥ @wojakcto: feeling like @HTX_Global knows real meme culture   / 212♥ @BinanceUS: It's the last 24 hours to get your share of ~$100K |
| [[$SYN]] | 2 | 2 | 6 | 493♥ @CryptoHayes: I still want to be long the Hyperliquid ecosystem  / 254♥ @coingecko: $SYN’s market cap jumped over 5x from $9M to ~$60M |
| [[$THREE]] | 2 | 2 | 4 | 216♥ @Crypto_Alch: Moment of truth for the $three tech   What if they / 128♥ @Crypto_Alch: Pay attention to the projects that hold levels whe |
| [[$TJR]] | 2 | 2 | 3 | 442♥ @moonshot: The Top Floor Boss ($TJR) is now verified on Moons / 279♥ @lookonchain: Don't #FOMO into celebrity coins.  Trader CCv4xA s |
| [[$TSLA]] | 2 | 2 | 3 | 9613♥ @nikitabier: We heard you guys like charts, so we made them big / 299♥ @theunipcs: $USELESS has now consolidated in its current range |
| [[$NEET]] | 2 | 2 | 3 | 243♥ @cookerbruski: similar to the way that $troll ranged for months,  / 165♥ @dxrnell: The $20M floor holding extremely well on $neet  Wo |
| [[$NVDA]] | 2 | 2 | 3 | 299♥ @theunipcs: $USELESS has now consolidated in its current range / 103♥ @milesdeutscher: Robotics investments just hit a new all-time high  |
| [[$TRUMP]] | 2 | 2 | 3 | 324♥ @arkham: TRUMP MADE OVER $1.4 BILLION FROM CRYPTO  Biggest  / 306♥ @theunipcs: i actually care about other coins  i've been most  |
| [[$HOOD]] | 2 | 2 | 2 | 80♥ @coingecko: INSIGHT: $HOOD rose 8.1% after Robinhood successfu / 5♥ @defi_kay_: $HOOD event  -Hood chain live, tokenized stock tra |
| [[$TESTIBULL]] | 2 | 2 | 2 | 305♥ @moonshot: testibull ($TESTIBULL) is now verified on Moonshot / 153♥ @dxrnell: So what’s the plan here  Rotate $testibull profits |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$USELESS]] | 5 | 1 | 8 | 413♥ @theunipcs: one memecoin remains strong and unfazed. it's up d / 306♥ @theunipcs: i actually care about other coins  i've been most  |
| [[$WIF]] | 4 | 1 | 6 | 362♥ @theunipcs: i have always liked and supported Ansem  i've neve / 306♥ @theunipcs: i actually care about other coins  i've been most  |
| [[$USDT]] | 3 | 1 | 11 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |
| [[$PEPE]] | 3 | 1 | 7 | 1742♥ @lookonchain: James Wynn(@JamesWynnReal) just deposited another  / 1516♥ @lookonchain: Who made the most money on $PEPE?  Here is a leade |
| [[$USDC]] | 2 | 1 | 14 | 2349♥ @rajgokal: absolutely thrilled that @visa has chosen @solana  / 1826♥ @DefiIgnas: We learned that $USDC is backed by cash held in ba |
| [[$PUNCH]] | 2 | 1 | 8 | 28♥ @daisuk_e4: The team is working tirelessly, sacrificing sleep. / 18♥ @daisuk_e4: 上場まだでしょうか、、？  $punch |
| [[$WORLD]] | 2 | 1 | 7 | 518♥ @PumpfunEco: JUST IN: $world hits a new all-time high of $10.7M / 205♥ @PumpfunEco: This trader is up $93,000 after buying $136 worth  |
| [[$HYPE]] | 2 | 1 | 6 | 347♥ @lookonchain: The #a16z-linked whale that previously accumulated / 195♥ @DefiIgnas: How does one prepare for the next bull if you are  |
| [[$BONK]] | 2 | 1 | 5 | 1604♥ @theunipcs: $BONK has the highest mindshare of any memecoin ov / 1354♥ @rajgokal: so $bonk is the next billion dollar community on @ |
| [[$LAB]] | 2 | 1 | 3 | 174♥ @bull_bnb: It doesn't matter how they're pumping $ANSEM. What / 24♥ @MurphyBTC: 🚨 $LAB に珍しいサインが出現‼️  これは暴走モードの準備段階に出現する演出で、前回暴走モード |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- [[$TRIPLET]]（48h 7件/3アカ・総14）まだconcept無し → 動線/型を検討
- [[$WOJAK]]（48h 2件/2アカ・総23）まだconcept無し → 動線/型を検討
- [[$SYN]]（48h 2件/2アカ・総6）まだconcept無し → 動線/型を検討
- [[$THREE]]（48h 2件/2アカ・総12）まだconcept無し → 動線/型を検討
- [[$TJR]]（48h 2件/2アカ・総3）まだconcept無し → 動線/型を検討
- [[$TSLA]]（48h 2件/2アカ・総4）まだconcept無し → 動線/型を検討
- [[$NEET]]（48h 2件/2アカ・総5）まだconcept無し → 動線/型を検討
- [[$NVDA]]（48h 2件/2アカ・総4）まだconcept無し → 動線/型を検討

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 493 |
| [[@badattrading_]] | 219 |
| [[@CoinMarketCap]] | 201 |
| [[@laurashin]] | 193 |
| [[@DEG_2020]] | 158 |
| [[@blknoiz06]] | 143 |
| [[@Ministerr]] | 141 |
| [[@milesdeutscher]] | 133 |
| [[@Lightspeedpodhq]] | 127 |
| [[@coin_post]] | 126 |
| [[@FrankDeGods]] | 126 |
| [[@JasonYanowitz]] | 125 |
| [[@spyzer]] | 124 |
| [[@thedefiedge]] | 122 |
| [[@RyanSAdams]] | 119 |
