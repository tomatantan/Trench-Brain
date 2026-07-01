---
type: worklist
title: ingest worklist
updated: 2026-06-26
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **7308件**（基準時刻 2026-06-26T15:30Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**298ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$BTC]] | 10 | 7 | 52 | 738♥ @CredibleCrypto: Not much has changed here, still think most logica / 735♥ @CredibleCrypto: Not much has changed here, still think most logica |
| [[$ETH]] | 4 | 3 | 74 | 3864♥ @zhusu: mental math with $eth will be a lot easier when it / 1896♥ @lookonchain: Machi Big Brother(@machibigbrother) spent ~5.2K $E |
| [[$MU]] | 2 | 2 | 3 | 16♥ @MEXC: Micron doesn’t just need to beat. #WallStreetMonth / 10♥ @DEG_2020: $MU マイクロンアフターマーケットでATHしそう  |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$PUMPI]] | 6 | 1 | 27 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$MERLIN]] | 4 | 1 | 18 | 1973♥ @ShapeFN_: Nos vemos el jueves. Merlin estará ahí.🦆🏆🇲🇽 $Merli / 1969♥ @ShapeFN_: Nos vemos el jueves. Merlin estará ahí.🦆🏆🇲🇽 $Merli |
| [[$WORLD]] | 3 | 1 | 5 | 205♥ @PumpfunEco: This trader is up $93,000 after buying $136 worth  / 41♥ @PumpfunEco: This trader refused to sell early & now their $​1, |
| [[$HPP]] | 3 | 1 | 4 | 111♥ @cryptocom: 🚨  is supporting the Aergo ($AERGO) token swap and / 47♥ @cryptocom: 🎉 The Aergo (AERGO) token swap and rebrand to Hous |
| [[$MSTR]] | 3 | 1 | 4 | 87♥ @CryptoKaleo: Once mNAV is definitively below 1 for $MSTR , what / 80♥ @CryptoKaleo: You can still sell your $MSTR for more than $50.  |
| [[$GRAM]] | 3 | 1 | 3 | 50♥ @cryptocom: 🎉 The Toncoin (TON) to Gram (GRAM) rebrand has bee / 41♥ @cryptocom: Gram ($GRAM) is now available for trading in the   |
| [[$WOJAK]] | 2 | 1 | 5 | 134♥ @wojakcto: t-minus 7 days to get in on the action with @Binan / 134♥ @wojakcto: our heroes @TrustWallet featuring $wojak for the c |
| [[$SOLANGELES]] | 2 | 1 | 4 | 151♥ @PumpfunEco: $SOLANGELES is rallying, up 28% in the past hour 👀 / 133♥ @PumpfunEco: $SOLANGELES is rallying, up 28% in the past hour 👀 |
| [[$KINS]] | 2 | 1 | 3 | 29♥ @Crypto_Alch: Comfy in Kintara $KINS   Fascinating gaming tek th / 17♥ @PumpfunEco: $KINS is rallying, currently up 22% in 24 hours 👀  |
| [[$PAXG]] | 2 | 1 | 2 | 287♥ @solana: BREAKING: $PAXG from @Paxos is now live on Solana  / 103♥ @solana: $PAXG on Solana, live with @ramzyyalii & @whessert |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- （なし）

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 473 |
| [[@badattrading_]] | 217 |
| [[@CoinMarketCap]] | 198 |
| [[@laurashin]] | 175 |
| [[@DEG_2020]] | 146 |
| [[@Lightspeedpodhq]] | 144 |
| [[@Ministerr]] | 140 |
| [[@JasonYanowitz]] | 139 |
| [[@blknoiz06]] | 139 |
| [[@RyanSAdams]] | 138 |
| [[@KyleSamani]] | 127 |
| [[@thedefiedge]] | 120 |
| [[@mellometrics]] | 119 |
| [[@milesdeutscher]] | 115 |
| [[@FrankDeGods]] | 115 |
