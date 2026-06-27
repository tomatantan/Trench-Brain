---
type: worklist
title: ingest worklist
updated: 2026-06-26
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **6859件**（基準時刻 2026-06-26T15:30Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**293ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 24 | 11 | 121 | 18413♥ @saylor: Strategy has acquired 1,587 BTC for $100 million t / 5655♥ @milesdeutscher: $BTC balance on exchanges just hit a 7-year low.   |
| [[$ETH]] | 18 | 5 | 115 | 4097♥ @CryptoHayes: 1/ Guess who is pumping $BTC and $ETH  / 3864♥ @zhusu: mental math with $eth will be a lot easier when it |
| [[$STRC]] | 14 | 5 | 27 | 18413♥ @saylor: Strategy has acquired 1,587 BTC for $100 million t / 4368♥ @saylor: Bitcoin Capitalism — my keynote from @BTCPrague 20 |
| [[$MU]] | 12 | 5 | 16 | 1188♥ @WatcherGuru: JUST IN: Micron $MU reports $41.5 billion in reven / 685♥ @blknoiz06: think $MU beats on ER makes a fresh new all time h |
| [[$MSTR]] | 10 | 3 | 18 | 18413♥ @saylor: Strategy has acquired 1,587 BTC for $100 million t / 5597♥ @saylor: Volatility tests every capital structure. Strategy |
| [[$SOL]] | 6 | 4 | 21 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 2022♥ @lookonchain: From a $1M loss (-90%) to a $2.5M profit—this diam |
| [[$JOTCHUA]] | 8 | 3 | 8 | 124♥ @Crypto_Alch: All my stables on the cute dog and I’m not even bo / 119♥ @PumpfunEco: $Jotchua has pumped 58% today! 🔥  |
| [[$HYPE]] | 5 | 4 | 11 | 334♥ @blknoiz06: $VVV & $HYPE strongest bounces on low timeframes s / 313♥ @blknoiz06: MERT'S 5 MAIN HOLDINGS: - $ZEC - solana:So11111111 |
| [[$MERLIN]] | 5 | 2 | 14 | 1973♥ @ShapeFN_: Nos vemos el jueves. Merlin estará ahí.🦆🏆🇲🇽 $Merli / 406♥ @ShapeFN_: People compare $Merlin to $Penguin because both we |
| [[$SPCX]] | 3 | 3 | 9 | 134♥ @MEXC: Every pullback creates a new question. 🚀  $SPCX is / 107♥ @MEXC: Your next Earn deposit could come with a side of $ |
| [[$WEN]] | 3 | 3 | 4 | 62♥ @PumpfunEco: Top traded pump fun coins by volume in the last 24 / 26♥ @itspyrored: Call me retarted but I blasted $Wen here  |
| [[$USELESS]] | 4 | 2 | 8 | 366♥ @theunipcs: $USELESS is now the second most-traded memecoin on / 305♥ @theunipcs: one metric that almost nobody is talking about:  $ |
| [[$SNDK]] | 4 | 2 | 6 | 351♥ @solana: BREAKING: $SNDK from @Sandisk via @SunriseDeFi, is / 36♥ @DEG_2020: $DRAM $MU $SNDK メモリ系時間外で5%近くのリバ 韓国指数Kospi連動っぽいねぇ |
| [[$DOGE]] | 3 | 2 | 10 | 4726♥ @milesdeutscher: AI will be one of the biggest bubbles in financial / 1518♥ @lookonchain: On Apr 4, @elonmusk changed the Bluebird to dog, t |
| [[$WOJAK]] | 3 | 2 | 8 | 158♥ @BinanceUS: Only one week left to earn your share of ~$100K $W / 150♥ @wojakcto: all wojaks are welcome. come feel something with t |
| [[$KINS]] | 3 | 2 | 7 | 171♥ @Crypto_Alch: Entry on $KINS IMO  $50-$100M to to bring gaming t / 104♥ @PumpfunEco: A $KINS whale is currently holding a $135,000 bag  |
| [[$SHIB]] | 2 | 2 | 6 | 2772♥ @lookonchain: A whale spent 4,806 $ETH($21.25M) to buy 938,489 $ / 2514♥ @lookonchain: Never seen such smart addresses!  - Made $4.14M by |
| [[$FARTCOIN]] | 2 | 2 | 5 | 366♥ @theunipcs: $USELESS is now the second most-traded memecoin on / 305♥ @theunipcs: one metric that almost nobody is talking about:  $ |
| [[$PENGU]] | 2 | 2 | 5 | 1794♥ @theunipcs: make no mistake:  the $PENGU pump should absolutel / 366♥ @theunipcs: $USELESS is now the second most-traded memecoin on |
| [[$TRIPLET]] | 2 | 2 | 2 | 105♥ @Crypto_Alch: $TripleT prediction coming to light   There’s only / 22♥ @PumpfunEco: $TripleT has pumped 21% today! 🔥  |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$PUMPI]] | 6 | 1 | 27 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$WORLD]] | 4 | 1 | 7 | 205♥ @PumpfunEco: This trader is up $93,000 after buying $136 worth  / 96♥ @PumpfunEco: Top traded pump fun coins by volume in the last 24 |
| [[$HPP]] | 3 | 1 | 4 | 111♥ @cryptocom: 🚨  is supporting the Aergo ($AERGO) token swap and / 47♥ @cryptocom: 🎉 The Aergo (AERGO) token swap and rebrand to Hous |
| [[$GRAM]] | 3 | 1 | 3 | 50♥ @cryptocom: 🎉 The Toncoin (TON) to Gram (GRAM) rebrand has bee / 41♥ @cryptocom: Gram ($GRAM) is now available for trading in the   |
| [[$SOLANGELES]] | 2 | 1 | 3 | 151♥ @PumpfunEco: $SOLANGELES is rallying, up 28% in the past hour 👀 / 77♥ @PumpfunEco: A $SOLANGELES whale is currently holding a $55,000 |
| [[$PAXG]] | 2 | 1 | 2 | 287♥ @solana: BREAKING: $PAXG from @Paxos is now live on Solana  / 103♥ @solana: $PAXG on Solana, live with @ramzyyalii & @whessert |
| [[$AAPL]] | 2 | 1 | 2 | 3508♥ @WatcherGuru: JUST IN: Apple $AAPL raises iPads and Macs prices  / 1805♥ @WatcherGuru: JUST IN: Apple $AAPL falls 5% after announcing pri |
| [[$DROOLING]] | 1 | 1 | 7 | 137♥ @Crypto_Alch: Here’s a screenshot taken from the future   $drool / 133♥ @Crypto_Alch: I’m hearing a cat will run to multimillions and br |
| [[$XRP]] | 1 | 1 | 7 | 906♥ @DefiIgnas: $XRP is 21% away from flipping $ETH in FDV.  $XRP  / 735♥ @CredibleCrypto: Not much has changed here, still think most logica |
| [[$USDT]] | 1 | 1 | 7 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- [[$MERLIN]]（48h 5件/2アカ・総14）まだconcept無し → 動線/型を検討
- [[$SNDK]]（48h 4件/2アカ・総7）まだconcept無し → 動線/型を検討
- [[$WOJAK]]（48h 3件/2アカ・総19）まだconcept無し → 動線/型を検討
- [[$TRIPLET]]（48h 2件/2アカ・総7）まだconcept無し → 動線/型を検討

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 473 |
| [[@badattrading_]] | 217 |
| [[@CoinMarketCap]] | 182 |
| [[@laurashin]] | 175 |
| [[@DEG_2020]] | 146 |
| [[@blknoiz06]] | 144 |
| [[@lookonchain]] | 130 |
| [[@Lightspeedpodhq]] | 125 |
| [[@Ministerr]] | 122 |
| [[@thedefiedge]] | 121 |
| [[@RyanSAdams]] | 119 |
| [[@JasonYanowitz]] | 119 |
| [[@mellometrics]] | 119 |
| [[@milesdeutscher]] | 118 |
| [[@FrankDeGods]] | 115 |
