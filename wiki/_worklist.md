---
type: worklist
title: ingest worklist
updated: 2026-06-23
---

# ingest worklist（エージェントが処理するTODO）

前回ingest以降の新シグナルツイ **5194件**（基準時刻 2026-06-23T23:32Z）。手順は brain/INGEST.md。
★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。
§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**212ティッカーは降格**して非表示。
処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。

## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）
各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。

| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |
|---|---|---|---|---|
| [[$ETH]] | 12 | 5 | 89 | 4097♥ @CryptoHayes: 1/ Guess who is pumping $BTC and $ETH  / 3864♥ @zhusu: mental math with $eth will be a lot easier when it |
| [[$BTC]] | 15 | 4 | 87 | 5655♥ @milesdeutscher: $BTC balance on exchanges just hit a 7-year low.   / 5398♥ @zhusu: If you had invested $1000 in $BTC in 2012, you'd p |
| [[$SPCX]] | 3 | 2 | 6 | 37♥ @MEXC: Every pullback creates a new question. 🚀  $SPCX is / 25♥ @MurphyBTC: $SPCX #株   買い増し前に確認したい「ロックアップ解除リスク」 低フロート相場の次に来る“売 |
| [[$SOL]] | 2 | 2 | 13 | 2270♥ @lookonchain: This guy spent only 6 $SOL($815) to buy 30.1M $MOO / 2022♥ @lookonchain: From a $1M loss (-90%) to a $2.5M profit—this diam |
| [[$MANIFEST]] | 2 | 2 | 2 | 165♥ @moonshot: Manifesting ($MANIFEST) is now verified on Moonsho / 66♥ @PumpfunEco: One of the top holders of $MANIFEST is sitting on  |
| [[$GOOGL]] | 2 | 2 | 2 | 984♥ @WatcherGuru: JUST IN: Google $GOOGL added to the Dow Jones Indu / 19♥ @MEXC: Your next Earn deposit could come with a side of $ |

## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）

| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |
|---|---|---|---|---|
| [[$PUMPI]] | 13 | 1 | 20 | 66♥ @pumpilians_: New players can now understand the game much easie / 53♥ @pumpilians_: Clan system is now live!  - Create a clan for 500, |
| [[$AGI]] | 3 | 1 | 3 | 13♥ @badattrading_: Wow some guy has 18.6% of $AGI supply, that's some / 10♥ @badattrading_: Snipers have 2% of $AGI (CA 4VKS1SjqeGGVHAAg1eJyR9 |
| [[$MSTR]] | 3 | 1 | 3 | 331♥ @CryptoKaleo: You can still sell your $MSTR for more than $100.  / 131♥ @CryptoKaleo: Saylor and Strategy are finally admitting cash is  |
| [[$USDC]] | 2 | 1 | 18 | 3000♥ @lookonchain: Trump's World Liberty(@worldlibertyfi) just spent  / 2801♥ @lookonchain: North Korean hackers went long $ETH on #Hyperliqui |
| [[$ASTEROID]] | 2 | 1 | 9 | 120♥ @solbrdl: Pepe had a slow bleed before it went to billions.  / 115♥ @solbrdl: Seems like the second scenario is in the play for  |
| [[$STRC]] | 2 | 1 | 7 | 245♥ @CryptoKaleo: There’s a much higher chance $STRC never returns t / 201♥ @CryptoKaleo: $STRC   If you like STRC at $89, you’ll love it at |
| [[$GYM]] | 2 | 1 | 6 | 90♥ @PumpfunEco: Ansem (@blknoiz06) just bought $1,000 of $CLAW & $ / 72♥ @cookerbruski: if you like $gym at 2m you’re gonna love it at 20m |
| [[$DROOLING]] | 2 | 1 | 3 | 85♥ @PumpfunEco: $drooling has pumped 43% today! 🔥  / 69♥ @itspyrored: You know a meme is good when you don’t have to con |
| [[$CLAW]] | 2 | 1 | 2 | 90♥ @PumpfunEco: Ansem (@blknoiz06) just bought $1,000 of $CLAW & $ / 23♥ @PumpfunEco: $CLAW has pumped 30% today! 🔥  |
| [[$CONDOR]] | 2 | 1 | 2 | 18♥ @badattrading_: $CONDOR (CA BQnsQ7LrcKVUqB33cqkVmbN1GNvqCCVYqGLLG5 / 15♥ @badattrading_: 1H chart opportunity here for $CONDOR, hitting rsi |

## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）
複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。

- （なし）

## 3) 活発になった player（合成メモ更新候補）

| player | 新規投稿 |
|---|---|
| [[@MarioNawfal]] | 208 |
| [[@laurashin]] | 133 |
| [[@Lightspeedpodhq]] | 120 |
| [[@JasonYanowitz]] | 119 |
| [[@RyanSAdams]] | 118 |
| [[@mellometrics]] | 118 |
| [[@Ministerr]] | 118 |
| [[@thedefiedge]] | 117 |
| [[@santiagoroel]] | 113 |
| [[@spyzer]] | 112 |
| [[@defi_kay_]] | 111 |
| [[@KyleSamani]] | 109 |
| [[@hosseeb]] | 108 |
| [[@cookerbruski]] | 104 |
| [[@cdixon]] | 102 |
