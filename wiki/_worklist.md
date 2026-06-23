---
type: worklist
title: ingest worklist
updated: 2026-06-23
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **4652件**（基準時刻 2026-06-23T00:39Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**204ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$ETH]] | 12 | 5 | 87 | 4097♥ @CryptoHayes: 1/ Guess who is pumping $BTC and $ETH  / 3864♥ @zhusu: mental math with $eth will be a lot easier when it |
| [[$BTC]] | 12 | 5 | 84 | 5655♥ @milesdeutscher: $BTC balance on exchanges just hit a 7-year low.   / 5398♥ @zhusu: If you had invested $1000 in $BTC in 2012, you'd p |
| [[$SOL]] | 4 | 3 | 18 | 2296♥ @lookonchain: Davido(@davido) launched a token named $DAVIDO and / 2284♥ @theunipcs: $SOL to $1,000 is one of those targets that sound  |
| [[$MU]] | 4 | 3 | 4 | 400♥ @solana: NEW: $MU (@MicronTech) via @SunriseDeFi. issued by / 351♥ @blknoiz06: airmass might be the greatest to ever do it with t |
| [[$WOJAK]] | 3 | 3 | 13 | 1423♥ @lookonchain: We noticed an early buyer of $SHIB also bought $PE / 683♥ @BinanceUS: Deposits for $WOJAK are now open on @BinanceUS!  T |
| [[$FARM]] | 4 | 2 | 5 | 277♥ @moonshot: FarmTown ($FARM) is now verified on Moonshot.  / 157♥ @Crypto_Alch: What is $FARM and why is it going parabolic?  |
| [[$HYPE]] | 3 | 2 | 4 | 15♥ @coinkeiba: $SOL 最近雰囲気良いな。 $HYPE が夏枯れして $SOL なのかもしれない。 / 5♥ @MurphyBTC: Hyperliquid TOP10鯨が $ETH 約133億円分のショートポジションをクローズしまし |
| [[$SPCX]] | 2 | 2 | 7 | 779♥ @WatcherGuru: JUST IN: Elon Musk is down $150 billion from his n / 107♥ @solbrdl: Imagine if $SPCX goes on a Tesla run. Before stock |
| [[$BP]] | 2 | 2 | 4 | 742♥ @coingecko: INSIGHT: $BP is up 27.4% following the debut of it / 251♥ @DefiIgnas: Every bull cycle has a new CEX in town:  • 2010: M |
| [[$THREE]] | 2 | 2 | 3 | 116♥ @Crypto_Alch: It’s $three O’clock   I hope you tailed   They’re  / 112♥ @Crypto_Alch: 99.998877% of CT sleeping on $three while it’s loo |
| [[$ARX]] | 2 | 2 | 2 | 537♥ @solana: BREAKING: $ARX from @Arcium is now live on Solana  / 169♥ @coingecko: $ARX just launched its TGE today and is currently  |
| [[$JSON]] | 2 | 2 | 2 | 41♥ @bull_bnb: On a serious note Who is $Json? / 4♥ @badattrading_: $json (CA 3HVEvoduJ4NKyLk4jUE3sjDX2L6sSDNHmcoJzUTi |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$PUMPI]] | 7 | 1 | 12 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$USDC]] | 4 | 1 | 20 | 3000♥ @lookonchain: Trump's World Liberty(@worldlibertyfi) just spent  / 2801♥ @lookonchain: North Korean hackers went long $ETH on #Hyperliqui |
| [[$ASTEROID]] | 3 | 1 | 18 | 248♥ @Crypto_Alch: $ASTEROID just 2x in a single fvcking candle   Did / 220♥ @solbrdl: Do people realize $ASTEROID was ACTUALLY on stage  |
| [[$TRIPLET]] | 3 | 1 | 3 | 76♥ @PumpfunEco: $TripleT has pumped 44% today! 🔥  / 72♥ @PumpfunEco: This trader bought $430 worth of $TripleT at $61K  |
| [[$STRC]] | 2 | 1 | 7 | 245♥ @CryptoKaleo: There’s a much higher chance $STRC never returns t / 201♥ @CryptoKaleo: $STRC   If you like STRC at $89, you’ll love it at |
| [[$USELESS]] | 2 | 1 | 4 | 1083♥ @theunipcs: i'm seeing a lot of similarities between $USELESS  / 252♥ @theunipcs: $SOL continues to outperform $BTC, $ETH, and the o |
| [[$UNC]] | 2 | 1 | 2 | 89♥ @PumpfunEco: $unc has pumped 48% today! 🔥  / 61♥ @PumpfunEco: $unc has pumped 44% today! 🔥  |
| [[$MSTR]] | 2 | 1 | 2 | 331♥ @CryptoKaleo: You can still sell your $MSTR for more than $100.  / 131♥ @CryptoKaleo: Saylor and Strategy are finally admitting cash is  |
| [[$TCG]] | 2 | 1 | 2 | 57♥ @PumpfunEco: $TCG has pumped 28% today! 🔥  / 33♥ @PumpfunEco: $TCG has pumped 83% today! 🔥  |
| [[$USDT]] | 1 | 1 | 6 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- [[$MU]]（48h 4件/3アカ・総4）まだconcept無し → 動線/型を検討
- [[$WOJAK]]（48h 3件/3アカ・総14）まだconcept無し → 動線/型を検討
- [[$FARM]]（48h 4件/2アカ・総5）まだconcept無し → 動線/型を検討
- [[$THREE]]（48h 2件/2アカ・総3）まだconcept無し → 動線/型を検討

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@laurashin]] | 132 |
| [[@JasonYanowitz]] | 120 |
| [[@Lightspeedpodhq]] | 120 |
| [[@RyanSAdams]] | 118 |
| [[@thedefiedge]] | 117 |
| [[@mellometrics]] | 117 |
| [[@Ministerr]] | 113 |
| [[@santiagoroel]] | 111 |
| [[@spyzer]] | 111 |
| [[@defi_kay_]] | 110 |
| [[@hosseeb]] | 107 |
| [[@KyleSamani]] | 106 |
| [[@cookerbruski]] | 104 |
| [[@cdixon]] | 102 |
| [[@FrankDeGods]] | 101 |
