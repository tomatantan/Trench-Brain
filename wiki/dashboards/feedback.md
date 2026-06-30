---
type: dashboard
title: Feedback — 型の hit-rate（実outcome採点）
updated: auto
tags: [feedback, learning, hit-rate]
---

# Feedback — 脳の型を実outcomeで採点

> `brain/feedback.py` が tracked.json の実死亡/生存から型のhit-rateを計算（報告のみ）。
> 断定はデータが出てから。小N/pending/比較群欠如は正直に出す。

## 母集団: tracked 106件（dead 70 / pending(tracked) 36）

## 型の hit-rate（観測）

| 型(仮説) | 検証 | 判定 |
|---|---|---|
| **traction無し→死ぬ** | 死亡 65/94 (69%)・残り29はpending | 支持(死多) |
| **traction有り→生存** | traction有り母集団 N=12（死5） | 検証可 |
| gate=graduated の死亡率 | 59/67 (88%) | 観測 |
| gate=mcap勢い門 の死亡率 | 3/20 (15%) | 観測 |
| gate=other の死亡率 | 8/19 (42%) | 観測 |

## ⚠️ 計測の限界（正直に）
- pending(tracked)が36件＝まだ生死未決着＝hit-rateは暫定（決着で更新）。
- **traction有り銘柄がほぼゼロ**＝「traction が生存を分ける」仮説の対照群が無い＝今は**反証も確証もできない**。
  → ①watchlist拡張でKOL言及銘柄が tracked に入れば対照群ができ、初めて型が検証可能になる（①と②Feedbackは連動）。
- 全件 同一launchpad/近時間帯＝独立性低い（[[rug-anatomy]]の注記と同じ留保）。

関連: [[rug-anatomy]] 死亡台帳 / [[launchpad-economics]] 跳躍台帳・base rate
