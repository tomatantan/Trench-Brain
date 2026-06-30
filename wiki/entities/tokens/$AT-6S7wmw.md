---
type: entity
kind: token
source: auto-track
status: watch
title: $AT（at）
mint: 6S7wmwnCkbckJFqdQXH72vNmDZbtU2ZvPNjqroSYpump
created: 2026-06-30
updated: 2026-06-30
tags: [trench, entity, token, auto-track, prebond, stub]
---

# $AT（at）

> 同名 ticker 衝突あり（$AT-3UMgXH / $AT-2dgmTy / $AT-DsvbjG）。mint 先頭6文字でファイル区別。

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | 6S7wmwnCkbckJFqdQXH72vNmDZbtU2ZvPNjqroSYpump |
| pool | BkvBG5ddPyasE1H3y1rCuMVBjaULgJsekyLYtpcM58c6 |
| gate | safety:ok / traction:mcap>=30000 |
| mcap(birth観測) | $137,984（2026-06-30T11:39Z） |
| peak_mcap | $137,984（暫定） |
| real_sol | 8,441,976（prebond 蓄積中） |
| reply_count | 0 |
| twitter | null |
| website | null |
| tokenized_agent | false |
| complete | false（prebond） |
| status | watch |
| auto-track birth | 2026-06-30T11:39Z |

<!-- synthesis:start -->
**観測（事実）**
- pump.fun 産・prebond（未graduated）・$138k で mcap≥30k 門通過。real_sol=8,441,976（bonding curve 蓄積中）。
- 名称 "at"（@記号相当）。twitter/website 皆無。reply=0・kol 皆無。

**判断**
- 極小ティッカー命名（"at"）は attention-grab 意図が見えるが social 基盤ゼロ。
- real_sol 非ゼロ（8.4M lamport 相当の prebond 資金）：graduated に進む可能性を残している。ただし twitter/website 皆無で community 形成は不明。
- [[launchpad-economics]] の prebond-watch パターン（cf. [[$SPX69]]/$BOWL 同型＝prebond × traction0）。graduate できなければ消滅。
- ⚠️ 同名 ticker が既に複数存在：この mint の独自性を維持するため本ファイル（$AT-6S7wmw）で追跡。

**接続概念**: [[launchpad-economics]]（prebond × traction0 × real_sol 蓄積中）
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
