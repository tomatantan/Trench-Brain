---
type: dashboard
title: 脳スコアカード（判定の的中＝良くなってるかの物差し）
updated: auto
tags: [scorecard, accuracy, feedback, edge]
---

# 脳スコアカード — /check 判定 vs 実outcome

> 脳の判定そのものの的中率（[[ape-or-avoid]] の実力）。総判定 4件。
> ★base 死亡率 50%＝**avoid的中はこれを超えて初めて価値**。ape的中こそ難しいテスト。直近18h未満はpending除外・小N。

## 判定種別の的中

| 判定 | 的中 | pending | 読み |
|---|---|---|---|
| **AVOID→死んだか** | 1/1 (100%) | 3 | base50%超で価値 |
| **APE→生存したか** | 未決着 | 0 | ★勝ちを当てる難テスト |

## 確信度 calibration（高確信ほど当たるべき）

| 確信度 | 的中 |
|---|---|
| 高 | 未決着 |
| 中 | 1/1 (100%) |
| 低 | 未決着 |

## 読み方（本人）
- **avoid的中 > base死亡率** なら「死を避ける」で価値が出てる。同水準なら無情報（base-rateと同じ）。
- **ape的中** が高いほど「勝ちを見つける」力＝魔界で稼ぐ本体。ここが上がるのが「良くなってる」の核。
- 高確信の的中 > 低確信 なら calibration が効いてる（自信の正しさ）。
- **時系列で上記が上がれば脳は良くなってる**。判定が溜まるほど信頼できる（今は小N＝/checkを使うほど鮮明に）。

関連: [[ape-or-avoid]] [[predictive-study]] [[feedback]] [[kol-track-records]]
