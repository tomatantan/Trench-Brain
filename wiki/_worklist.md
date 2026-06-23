---
type: worklist
title: ingest worklist
updated: 2026-06-23
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **4843件**（基準時刻 2026-06-23T10:45Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**203ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 13 | 5 | 85 | 5655♥ @milesdeutscher: $BTC balance on exchanges just hit a 7-year low.   / 5398♥ @zhusu: If you had invested $1000 in $BTC in 2012, you'd p |
| [[$ETH]] | 10 | 5 | 86 | 4097♥ @CryptoHayes: 1/ Guess who is pumping $BTC and $ETH  / 3864♥ @zhusu: mental math with $eth will be a lot easier when it |
| [[$SPCX]] | 5 | 3 | 8 | 458♥ @coingecko: NEWS: $SPCX falls 17.8%, erasing most of its gains / 37♥ @MEXC: Every pullback creates a new question. 🚀  $SPCX is |
| [[$SOL]] | 4 | 2 | 16 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 2022♥ @lookonchain: From a $1M loss (-90%) to a $2.5M profit—this diam |
| [[$JOTCHUA]] | 2 | 2 | 2 | 51♥ @PumpfunEco: A $Jotchua whale is currently holding a $114,000 b / 1♥ @Crypto_Alch: My Nigerian quant thinks the $Jotchua bottom is in |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$PUMPI]] | 10 | 1 | 15 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$USDC]] | 3 | 1 | 18 | 3000♥ @lookonchain: Trump's World Liberty(@worldlibertyfi) just spent  / 2801♥ @lookonchain: North Korean hackers went long $ETH on #Hyperliqui |
| [[$ASTEROID]] | 3 | 1 | 17 | 248♥ @Crypto_Alch: $ASTEROID just 2x in a single fvcking candle   Did / 220♥ @solbrdl: Do people realize $ASTEROID was ACTUALLY on stage  |
| [[$AGI]] | 3 | 1 | 3 | 13♥ @badattrading_: Wow some guy has 18.6% of $AGI supply, that's some / 10♥ @badattrading_: Snipers have 2% of $AGI (CA 4VKS1SjqeGGVHAAg1eJyR9 |
| [[$TRIPLET]] | 3 | 1 | 3 | 76♥ @PumpfunEco: $TripleT has pumped 44% today! 🔥  / 72♥ @PumpfunEco: This trader bought $430 worth of $TripleT at $61K  |
| [[$STRC]] | 2 | 1 | 7 | 245♥ @CryptoKaleo: There’s a much higher chance $STRC never returns t / 201♥ @CryptoKaleo: $STRC   If you like STRC at $89, you’ll love it at |
| [[$USDT]] | 2 | 1 | 6 | 1772♥ @lookonchain: MrBeast (@MrBeast) just deposited 114,483 $USDT in / 1648♥ @lookonchain: It seems that #Bybit spent 100M $USDT to buy 36,89 |
| [[$USELESS]] | 2 | 1 | 4 | 1083♥ @theunipcs: i'm seeing a lot of similarities between $USELESS  / 252♥ @theunipcs: $SOL continues to outperform $BTC, $ETH, and the o |
| [[$DROOLING]] | 2 | 1 | 3 | 85♥ @PumpfunEco: $drooling has pumped 43% today! 🔥  / 69♥ @itspyrored: You know a meme is good when you don’t have to con |
| [[$GNO]] | 2 | 1 | 2 | 22♥ @DefiIgnas: Gnosis DAO voting on one-time, pro-rata treasury r / 13♥ @DefiIgnas: In theory, this could end the DAO:  You can't mark |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- （なし）

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@laurashin]] | 132 |
| [[@MarioNawfal]] | 131 |
| [[@Lightspeedpodhq]] | 120 |
| [[@JasonYanowitz]] | 119 |
| [[@RyanSAdams]] | 118 |
| [[@thedefiedge]] | 117 |
| [[@mellometrics]] | 117 |
| [[@Ministerr]] | 116 |
| [[@santiagoroel]] | 113 |
| [[@spyzer]] | 111 |
| [[@defi_kay_]] | 110 |
| [[@hosseeb]] | 107 |
| [[@KyleSamani]] | 106 |
| [[@cookerbruski]] | 104 |
| [[@cdixon]] | 102 |
