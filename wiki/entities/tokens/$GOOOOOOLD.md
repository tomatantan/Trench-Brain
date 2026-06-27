---
type: entity
kind: token
source: auto-track
status: dead
ticker: $GOOOOOOLD
mint: DdrAWJx9ccmXDowswU1cpJmZ7bkasmpUQMZUomV6pump
created: 2026-06-26
updated: 2026-06-26 (第125窓・DEAD残存 re-detection)
tags: [token, pumpfun, traction0, dead, thebloop-type, scats-type, initial-collapse]
---

# $GOOOOOOLD（DdrAWJ）

pump.fun 発。"GOOOOOOLD"（O多重・gold パロディ命名）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | DdrAWJx9ccmXDowswU1cpJmZ7bkasmpUQMZUomV6pump |
| 初検知 mcap | $76,739（traction gate 検知） |
| gate | traction:passed |
| reply_count | 0 |
| KOL (CA確認) | なし |

## 追跡ログ

| 窓 | live mcap | 変化（検知時比） | 窓間変化 | 備考 |
|----|-----------|----------------|---------|------|
| 第123窓 | **$18,966** | **-75.3%** | — | **1窓目(初登場)。traction 検知時点で既に-75.3%——THEBLOOP/SCATS型(初登場時既崩壊)の疑い。stale:false = 下落方向に動意あり。T3ゼロ・reply:0。** |
| 第124窓 | **$1,355** | **-98.2%** | **-$17,611（-92.9%窓間・DEAD確定）** | **2窓目。DEAD確定。THEBLOOP/SCATS型予測的中。2窓でライフサイクル完結。T3ゼロ・reply:0。** |
| 第125窓 | $1,347 | -98.2% | — | **DEAD残存 re-detection（DEAD確定第124窓後、第125窓に再検知）。PAWS同型——bonding curve 最低流動性残存による一時浮上。観測のみ。** |

<!-- synthesis:start -->
## 合成

**観測（事実・T1)**:
- traction 検知時 $76,739 → 第123窓 live $18,966（-75.3%）。
- reply_count=0・KOL なし——T3 signal ゼロ。
- stale:false（価格が動いている = 下落方向）。

**判断（第124窓・DEAD確定）**:
- $18,966（第123窓）→ $1,355（第124窓）。-92.9%窓間・-98.2%検知時比。DEAD確定。
- THEBLOOP/SCATS型「初登場時点で既崩壊→次窓DEAD」の予測が的中。2窓でライフサイクル完結。
- traction gate = mcap の一時点スナップショットで通過する構造を改めて確認。gate通過後急落済みの残滓は生存性ゼロ。

**確定記録**: 縮退パターン記録へ移行。第125窓に $1,347 で re-detection——PAWS同型の bonding curve 残存。died +1 は第125窓カウント（第124窓 DEAD確定分）。

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]（initial-collapse型 = bonding卒業→即崩壊残滓）
- [[launch-pulse]]（第123窓 traction 候補・初窓）
