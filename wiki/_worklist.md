---
type: worklist
title: ingest worklist
updated: 2026-06-26
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **7454件**（基準時刻 2026-06-26T15:30Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**294ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 20 | 10 | 118 | 5655♥ @milesdeutscher: $BTC balance on exchanges just hit a 7-year low.   / 5398♥ @zhusu: If you had invested $1000 in $BTC in 2012, you'd p |
| [[$ETH]] | 17 | 4 | 117 | 4097♥ @CryptoHayes: 1/ Guess who is pumping $BTC and $ETH  / 3864♥ @zhusu: mental math with $eth will be a lot easier when it |
| [[$STRC]] | 12 | 4 | 20 | 148♥ @CryptoKaleo: $STRC down to $71.  Already knocking on the door o / 131♥ @CryptoKaleo: Saylor and Strategy are finally admitting cash is  |
| [[$MU]] | 5 | 3 | 6 | 39♥ @DEG_2020: マイクロンアフターマーケットで+3.4% $MU  / 26♥ @MEXC: 🔥 More USD1-M Futures are now available on MEXC! @ |
| [[$JOTCHUA]] | 5 | 3 | 5 | 66♥ @PumpfunEco: A $Jotchua whale is currently holding a $121,000 b / 42♥ @Crypto_Alch: If the whole timeline could stop vamping and run $ |
| [[$SOL]] | 4 | 3 | 19 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 2022♥ @lookonchain: From a $1M loss (-90%) to a $2.5M profit—this diam |
| [[$SPCX]] | 3 | 3 | 9 | 29♥ @MurphyBTC: $SPCX #株   買い増し前に確認したい「ロックアップ解除リスク」 低フロート相場の次に来る“売 / 26♥ @MEXC: 🔥 More USD1-M Futures are now available on MEXC! @ |
| [[$HYPE]] | 3 | 3 | 8 | 249♥ @lookonchain: A whale is rotating from $ETH into $HYPE.  Two wee / 249♥ @coingecko: Top 20 Trending Coins on CoinGecko 🦎  This week, $ |
| [[$WOJAK]] | 3 | 2 | 7 | 158♥ @BinanceUS: Only one week left to earn your share of ~$100K $W / 139♥ @wojakcto: $wojak but make it @binance colors  |
| [[$CHAMELEON]] | 2 | 2 | 2 | 37♥ @PumpfunEco: This trader refused to sell early & now their $626 / 14♥ @badattrading_: $Chameleon (CA GuSborgzpo6Hc7msoRouQyPJ3psxgAHm4am |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$MSTR]] | 7 | 1 | 10 | 131♥ @CryptoKaleo: Saylor and Strategy are finally admitting cash is  / 87♥ @CryptoKaleo: Once mNAV is definitively below 1 for $MSTR , what |
| [[$PUMPI]] | 6 | 1 | 27 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$MERLIN]] | 4 | 1 | 18 | 1973♥ @ShapeFN_: Nos vemos el jueves. Merlin estará ahí.🦆🏆🇲🇽 $Merli / 1969♥ @ShapeFN_: Nos vemos el jueves. Merlin estará ahí.🦆🏆🇲🇽 $Merli |
| [[$WORLD]] | 3 | 1 | 5 | 205♥ @PumpfunEco: This trader is up $93,000 after buying $136 worth  / 41♥ @PumpfunEco: This trader refused to sell early & now their $​1, |
| [[$HPP]] | 3 | 1 | 4 | 111♥ @cryptocom: 🚨  is supporting the Aergo ($AERGO) token swap and / 47♥ @cryptocom: 🎉 The Aergo (AERGO) token swap and rebrand to Hous |
| [[$GRAM]] | 3 | 1 | 3 | 50♥ @cryptocom: 🎉 The Toncoin (TON) to Gram (GRAM) rebrand has bee / 41♥ @cryptocom: Gram ($GRAM) is now available for trading in the   |
| [[$SOLANGELES]] | 2 | 1 | 4 | 151♥ @PumpfunEco: $SOLANGELES is rallying, up 28% in the past hour 👀 / 133♥ @PumpfunEco: $SOLANGELES is rallying, up 28% in the past hour 👀 |
| [[$KINS]] | 2 | 1 | 3 | 29♥ @Crypto_Alch: Comfy in Kintara $KINS   Fascinating gaming tek th / 17♥ @PumpfunEco: $KINS is rallying, currently up 22% in 24 hours 👀  |
| [[$PAXG]] | 2 | 1 | 2 | 287♥ @solana: BREAKING: $PAXG from @Paxos is now live on Solana  / 103♥ @solana: $PAXG on Solana, live with @ramzyyalii & @whessert |
| [[$AAPL]] | 2 | 1 | 2 | 3508♥ @WatcherGuru: JUST IN: Apple $AAPL raises iPads and Macs prices  / 1805♥ @WatcherGuru: JUST IN: Apple $AAPL falls 5% after announcing pri |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- [[$WOJAK]]（48h 3件/2アカ・総25）まだconcept無し → 動線/型を検討

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 473 |
| [[@badattrading_]] | 217 |
| [[@CoinMarketCap]] | 198 |
| [[@laurashin]] | 175 |
| [[@DEG_2020]] | 149 |
| [[@Lightspeedpodhq]] | 144 |
| [[@Ministerr]] | 140 |
| [[@JasonYanowitz]] | 139 |
| [[@blknoiz06]] | 139 |
| [[@RyanSAdams]] | 138 |
| [[@lookonchain]] | 128 |
| [[@KyleSamani]] | 127 |
| [[@thedefiedge]] | 121 |
| [[@mellometrics]] | 119 |
| [[@milesdeutscher]] | 118 |
