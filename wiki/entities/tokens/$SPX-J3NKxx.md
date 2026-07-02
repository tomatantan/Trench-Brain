---
type: entity
kind: token
source: auto-track
status: watch
ticker: $SPX
mint: J3NKxxXZcnNiMjKw9hYb2K4LUxgwB6t1FtPtQVsv3KFr
created: 2026-07-02
updated: 2026-07-02 (birth stub・$339M・KOL theunipcs/crypto_alch・既存曖昧[[$SPX]]と別実体を確認)
tags: [token, pumpfun, kol-ca, theunipcs, majors, wormhole-bridge, high-mcap]
---

# $SPX — SPX6900 (Wormhole)（J3NKxx）

Solana 上の SPX6900（[[$SPX]]／SPX6900 本体はマルチチェーン、これは Wormhole ブリッジ経由の Solana 表現）。mint 作成は 2023-12-19（古参・fresh launchでない）。twitter/website とも公式（@spx6900 / spx6900.com）。

**既存 [[$SPX]] entity との関係**: 既存ページは @CryptoHayes が S&P500 **株式指数**の意味で "$SPX" を使った文脈（TradFiマクロのボトム論法）を集約したもので、entity 自体が「crypto token か株式指数か曖昧」と自己申告で⚠️を立てていた。本ページの mint (J3NKxx) は crypto_alch/theunipcs のツイートで明示的に CA 言及されている**実在の SPX6900トークン**——既存ページの曖昧さを解消する別実体として分離。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | J3NKxxXZcnNiMjKw9hYb2K4LUxgwB6t1FtPtQVsv3KFr |
| pool | 9t1H1uDJ558iMPNkEPSN1fqkpC4XSPQ6cqSf6uEsTfTR |
| gate | safety:ok / traction:kol |
| 検知 mcap | $339,040,991.37（2026-07-02T07:32:58Z） |
| reply_count | 140 |
| KOL（CA確認） | [[@crypto_alch]] / [[@theunipcs]] |
| twitter | https://x.com/spx6900（公式） |
| website | https://www.spx6900.com（公式） |
| tokenized_agent | false |
| complete | false（bonding curve完了フラグは該当せず・確立資産） |
| created | 2023-12-19（古参mint） |
| real_sol | 0 |

## KOL裏取り

- [crypto_alch__2070158134681694252](../../sources/x/crypto_alch__2070158134681694252.md)——「We ran solana:J3NKxx... from sub $10M to $2,000,000,000 United States dollars」（自己言及的な"we ran"表現・具体的なピーク時期の明示なし）。
- [theunipcs__2072305809296437545](../../sources/x/theunipcs__2072305809296437545.md)——2026-07-02、$USELESS の相対強度比較スレッド内で「up 124% vs solana:J3NKxx...」——majors/meme横断の relative performance list の一項目として言及（$PEPE +324%・$PENGU +207%・$WIF +199%・$FARTCOIN +254% と並列）。

<!-- synthesis:start -->
**観測（事実）**:
- 検知時 mcap $339M——本キュー中最大。twitter/website とも公式整備済の確立ブランド。
- crypto_alch は「sub $10M → $2B」という巨大な run を主張するが、検知時点の実 mcap（$339M）とは大きな乖離——ピーク時期不明・誇張・別集計軸（トークン全体時価総額 vs この Solana ブリッジ pool 単体）のいずれかは本ソースからは特定不能。
- theunipcs の言及は独立した強気thesisでなく、$USELESS 中心の相対強度比較の一項目——SPX単体への深い分析ではない。

**判断**:
- ⚠️ crypto_alch の「$2B」claim は要検算——[[onchain-verification]]。SPX6900はマルチチェーン資産のため、この Solana/Wormhole pool 単体の mcap と、ネットワーク全体の time-of-claim 時価総額を混同している可能性がある（誇張と断定はできない）。
- [[majors-rotation-supercycle]]: 確立ブランドが meme相対強度比較の参照点として使われている＝[[survivor-memes]]を超えて "major格" 扱いされている実例。
- 既存 [[$SPX]] の "entity名が曖昧" という⚠️は本ページの分離で一部解消——ただし wiki横断で "$SPX" 表記を見る際は依然両実体（S&P500指数言及 vs 本token）の混同に注意。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[majors-rotation-supercycle]]
- [[onchain-verification]] — crypto_alchの"$2B"claim要検算
- 同ticker既存entity: [[$SPX]]（CryptoHayesのTradFi指数言及と混同注意）
