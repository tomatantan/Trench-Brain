---
type: entity
kind: token
source: auto-track
status: dead
ticker: $MOONO
mint: APpg3oiSp3PD2sJUhVpZ5Lv7oRaMFvcGMwAEgfCroJRC
created: 2026-06-26
updated: 2026-06-26 (第129窓・re-detection list exit再確定)
tags: [token, traction0, graduated, other-theme, dead]
---

# $MOONO — APpg3oi

pump.fun 形式外のmint（末尾 JRC）——Raydium 等の別 launchpad の可能性あり。theme: other（未分類）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | APpg3oiSp3PD2sJUhVpZ5Lv7oRaMFvcGMwAEgfCroJRC |
| name | — (JSON に name フィールドなし) |
| 初検知 mcap | $71,049（第116窓） |
| gate | safety:ok / traction:graduated（推定） |
| reply_count | 0 |
| KOL (CA確認) | なし |

## 追跡ログ

| 窓 | live mcap | 変化（検知時比） | 窓間変化 | 備考 |
|----|-----------|----------------|---------|------|
| 第116窓 | $79,686 | +12.2% | — | 初登場。modest positive。T3ゼロ・reply:0。 |
| 第117窓 | — | — | — | **list exit確定（candidates から消滅）。** |
| 第125窓 | $2,551 | -96.4% | — | **DEAD残存 re-detection（第117窓 list exit以来、第125窓に再検知）。PAWS・GOOOOOOLD同型——bonding curve 最低流動性残存。** |
| 第128窓 | $2,549 | -96.4% | — | DEAD残存 re-detection 継続。 |
| 第129窓 | candidates消滅 | — | — | **re-detection list exit再確定（第129窓 traction_candidates から消滅）。** |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- 検知時 $71,049 → 第116窓 $79,686（+12.2%）→ **第117窓 candidates 消滅（list exit確定）**。
- 1窓で消滅——traction_candidates 最短追跡記録の一つ。

**判断（第117窓・list exit確定）**:
- +12.2% の modest positive から翌窓で即消滅。追跡内容なし→崩壊か急速な mcap 低下の可能性。
- pump.fun 形式外 mint（末尾 JRC）——別 launchpad の tracking 精度が pump.fun より低く、candidates に入るのが難しい可能性。
- T3ゼロ・reply:0。organic 支持なしで1窓消滅——観測記録としての価値のみ。

**第125窓 re-detection（-96.4%・$2,551）**:
- 第117窓 list exit後、第125窓に $2,551（検知時 $71,049比 -96.4%）で再検知。PAWS・GOOOOOOLD と同型——bonding curve 最低流動性残存による一時的な再浮上。
- DEAD残存 re-detection として観測継続。再採用なし。

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
- [[launch-pulse]]（第116窓 traction 候補・初窓）
