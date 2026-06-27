---
type: entity
kind: token
source: auto-track
status: dead
ticker: $GIRLS
mint: 2VHJqiKUeagsTUJM2Ez6W5yNDy28Hp3WpiS8LUgvpump
created: 2026-06-25
updated: 2026-06-25 (DEAD確定)
tags: [token, pumpfun, dead, traction0, generic-name, real-sol, high-real-sol-dead]
---

# $GIRLS — 2VHJqiK・DEAD確定

pump.fun 発。bonding curve 卒業済。real_sol 82.9 SOL は本サイクル最高水準だが KOL/traction ゼロのまま death。⑬「high real_sol ≠ 生存保証」N=2 確定事例（$FINLEY 82.6SOL と同型）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 2VHJqiKUeagsTUJM2Ez6W5yNDy28Hp3WpiS8LUgvpump |
| name | Girls |
| 検知時 mcap | $75,179（2026-06-25T13:57Z） |
| gate | safety:ok / traction:graduated |
| reply_count | 0（全期間） |
| KOL (CA確認) | なし（全期間） |
| twitter | https://x.com/girlspumpfun |
| website | https://girls.reisen/ |
| tokenized_agent | false |
| real_sol | 82.9 SOL（pool 実流動性・本サイクル最高水準） |
| pool_address | YQZHRr2VcZ2nVfjqQSpMZ4sqm3UX5BYwvVuZ3b7Xmd2 |
| peak mcap | $109,093（auto 14:22Z） |
| 最終 mcap | $1,563（2026-06-25T14:48Z） |
| 最終status | **DEAD確定** |

## 追跡ログ

| 観測 | live mcap | 変化（検知時比） | 窓間変化 | 備考 |
|----|-----------|----------------|---------|------|
| 初検知(13:57Z) | $75,179 | — | — | gate 通過。reply:0・KOLゼロ。 |
| auto(14:22Z) | $109,093 | +45.2% | +$33,914（+45.2%） | synth_queue +46%（DB比）。継続上昇。T3ゼロ・reply:0 継続。 |
| auto(14:48Z) | **$1,563** | **-97.9%** | -$107,530（-98.6%） | **DEAD確定。peak比-98.6%崩壊。real_sol 82.9SOL ありでも崩壊。** |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun bonding curve 卒業・初検知 $75k。peak $109,093（14:22Z）→ 最終 $1,563（14:48Z）。birth 13:57Z から約51分で崩壊。
- real_sol **82.9 SOL**——本サイクル最高水準（$FINLEY 82.6SOL とほぼ同水準）。pool に大量 SOL あり。
- reply_count=0・KOL=0（全期間）——有機的 traction ゼロのまま死亡。
- "Girls" は generic naming。crypto narrative との直接接続なし。

**死の学習**:
- **⑬「high real_sol ≠ 生存保証」N=2 確定**: $FINLEY(82.6SOL → -92.2%)に続き、$GIRLS(82.9SOL → -98.6%)が同サイクル内で2例目の確定。pool に本サイクル最大級の SOL が入っていても KOL/traction ゼロなら崩壊は防げない——deployer が自己準備した流動性は最終的に自己利益のために引き出される。
- **「graduated-but-empty」型の典型死**: generic name + traction0 → [[launchpad-economics]] 縮退死パターン。girls.reisen ドメインや twitter 整備も生存に寄与しなかった。
- birth($75k)→peak($109k, +45%)→death($1.5k, -98.6%)——一度の mcap 上昇後の急落。peak での deployer 利確が疑われる。

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty 縮退死）
- [[rug-anatomy]]（high real_sol ≠ 安全・⑬型 N=2 確定・死亡台帳）
- [[survivor-memes]]（候補だったが traction 不在のまま死亡）
