---
type: worklist
title: ingest worklist
updated: 2026-06-23
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **4707件**（基準時刻 2026-06-23T05:19Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**203ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 13 | 5 | 85 | 5655♥ @milesdeutscher: $BTC balance on exchanges just hit a 7-year low.   / 5398♥ @zhusu: If you had invested $1000 in $BTC in 2012, you'd p |
| [[$ETH]] | 9 | 5 | 85 | 4097♥ @CryptoHayes: 1/ Guess who is pumping $BTC and $ETH  / 3864♥ @zhusu: mental math with $eth will be a lot easier when it |
| [[$SPCX]] | 3 | 3 | 7 | 107♥ @coinkeiba: $SPCX 買わずに淡々と $TSLA 集めてる🚘 / 35♥ @dxrnell: The booster has safely landed $SPCX  |
| [[$SOL]] | 3 | 2 | 15 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 2022♥ @lookonchain: From a $1M loss (-90%) to a $2.5M profit—this diam |
| [[$HYPE]] | 2 | 2 | 3 | 90♥ @lookonchain: The wallet(0xf7A4) linked to Arthur Hayes(@CryptoH / 5♥ @MurphyBTC: Hyperliquid TOP10鯨が $ETH 約133億円分のショートポジションをクローズしまし |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$PUMPI]] | 8 | 1 | 13 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$USDC]] | 3 | 1 | 18 | 3000♥ @lookonchain: Trump's World Liberty(@worldlibertyfi) just spent  / 2801♥ @lookonchain: North Korean hackers went long $ETH on #Hyperliqui |
| [[$ASTEROID]] | 3 | 1 | 17 | 248♥ @Crypto_Alch: $ASTEROID just 2x in a single fvcking candle   Did / 220♥ @solbrdl: Do people realize $ASTEROID was ACTUALLY on stage  |
| [[$TRIPLET]] | 3 | 1 | 3 | 76♥ @PumpfunEco: $TripleT has pumped 44% today! 🔥  / 72♥ @PumpfunEco: This trader bought $430 worth of $TripleT at $61K  |
| [[$STRC]] | 2 | 1 | 7 | 245♥ @CryptoKaleo: There’s a much higher chance $STRC never returns t / 201♥ @CryptoKaleo: $STRC   If you like STRC at $89, you’ll love it at |
| [[$USELESS]] | 2 | 1 | 4 | 1083♥ @theunipcs: i'm seeing a lot of similarities between $USELESS  / 252♥ @theunipcs: $SOL continues to outperform $BTC, $ETH, and the o |
| [[$UNC]] | 2 | 1 | 2 | 89♥ @PumpfunEco: $unc has pumped 48% today! 🔥  / 61♥ @PumpfunEco: $unc has pumped 44% today! 🔥  |
| [[$MSTR]] | 2 | 1 | 2 | 331♥ @CryptoKaleo: You can still sell your $MSTR for more than $100.  / 131♥ @CryptoKaleo: Saylor and Strategy are finally admitting cash is  |
| [[$TCG]] | 2 | 1 | 2 | 57♥ @PumpfunEco: $TCG has pumped 28% today! 🔥  / 33♥ @PumpfunEco: $TCG has pumped 83% today! 🔥  |
| [[$USDT]] | 1 | 1 | 5 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- （なし）

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@laurashin]] | 132 |
| [[@Lightspeedpodhq]] | 120 |
| [[@JasonYanowitz]] | 119 |
| [[@RyanSAdams]] | 118 |
| [[@thedefiedge]] | 117 |
| [[@mellometrics]] | 117 |
| [[@Ministerr]] | 116 |
| [[@santiagoroel]] | 111 |
| [[@spyzer]] | 111 |
| [[@MarioNawfal]] | 111 |
| [[@defi_kay_]] | 110 |
| [[@hosseeb]] | 107 |
| [[@KyleSamani]] | 106 |
| [[@cookerbruski]] | 104 |
| [[@cdixon]] | 102 |
