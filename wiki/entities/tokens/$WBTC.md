---
type: entity
kind: token
title: $WBTC
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 3
accounts: 2
---

# $WBTC

> 自動生成(brain/build_entities.py)。言及 3件 / 2アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連 [[concepts]]。

## 言及アカウント
[[@CryptoHayes]] [[@lookonchain]]

## 共起トークン
[[$ETH]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 3,312 | [[@CryptoHayes]] | Here we go ...   1/  Looking at onchain data for $wBTC and $ETH, the liquidations ha | [[CryptoHayes__1536530712752697344]] |
| 2,701 | [[@lookonchain]] | Crazy!  Someone lost 1,155 $WBTC($71M) due to a phishing attack.  How did it happen? | [[lookonchain__1786424681253540337]] |
| 1,770 | [[@lookonchain]] | A whale lost 1,155 $WBTC($71M) due to a phishing attack on May 3.  A week later, the | [[lookonchain__1789699903041700023]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

**観測（事実）**
- 2022-06-14: [[@CryptoHayes]] が wBTC/$ETH のオンチェーン清算データを確認 → 「清算はほぼ完了」と判断 ([[CryptoHayes__1536530712752697344]])。ベアマーケット中のボトム確認文脈。
- 2024-05-03: 1,155 $WBTC($71M) が「address poisoning」型フィッシングで被害 ([[lookonchain__1786424681253540337]])。手口: 同一 prefix の偽アドレスへ誤送金。
- 2024-05-12: 攻撃者が**全額返金** ([[lookonchain__1789699903041700023]])。

**判断（推論）**
- corpus 上の $WBTC 言及は「マクロ清算の確認ツール」と「フィッシング事例」の 2 本のみ。$WBTC 自体へのナラティブ（強気/弱気）は存在しない。
- Hayes の使い方 = wBTC を「[[$ETH]] と並ぶマクロ清算の体温計」として使用 → [[majors-rotation-supercycle]] の底打ち確認に現れる指標。wBTC 単体の thesis ではなく ETH/BTC マクロの観察点。
- フィッシング事件: [[onchain-verification]] の教訓事例。「移動（観測）」は確定、「全額返金」という異常解決は珍しい（ホワイトハット行動 or 法執行圧力の可能性）。意図は不明、observation のみ記録。
- ⚠️ $WBTC ≠ trench の alpha 源: 言及が両方とも 2022-2024 の過去データ。現在の trench での直接的役割は薄い。

接続: [[majors-rotation-supercycle]]（マクロ清算の観察点）/ [[onchain-verification]]（フィッシング事例・資金移動追跡）
<!-- synthesis:end -->
