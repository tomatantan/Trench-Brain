---
type: entity
kind: token
source: auto-track
status: dead
outcome: died
ticker: $AMERICA250
mint: USA6S93wdRDc8gUuNbWYH17vWWY6pcxLbWu3bdQ3q6X
created: 2026-06-26
updated: 2026-06-27 (DEAD確定・peak $104k→$1,707・-98.4%・mcap枯れ)
tags: [token, pumpfun, graduated, traction0, event-driven, usa-narrative, dead]
---

# $AMERICA250 — America250（USA6S93）

pump.fun 発。bonding curve 卒業済（complete=true）。"America250" は米国建国250周年（2026年7月4日・Semiquincentennial）に連動する外部イベント命名。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | USA6S93wdRDc8gUuNbWYH17vWWY6pcxLbWu3bdQ3q6X |
| name | America250 |
| 初検知 mcap | $84,493（2026-06-25T17:04Z） |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| twitter | なし |
| website | なし |
| tokenized_agent | false |
| real_sol | ~67.7 SOL（pool 実流動性あり） |
| pool_address | 4Gx3bgU9sCM4i2yVbnxSE6iMhhB7KvgPWajKzmAHPh6N |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|----|-----------|------|------|
| 初検知(17:04Z) | $84,493 | — | gate 通過。reply:0・KOLゼロ。real_sol ~67.7SOL。 |
| 死亡確定(20:27Z) | $1,707 | peak比-98.4% | mcap枯れ。peak $104,473。T3ゼロ全期間。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun bonding curve 卒業・$84,493。real_sol ~67.7 SOL——コホート内では比較的高い流動性（$FINLEY 82.6SOL/$GIRLS 82.9SOL クラス）。
- twitter/website なし——social 基盤ゼロ。
- 命名: "America250"——2026年7月4日・米国建国250周年（Semiquincentennial）に連動する外部イベント命名。
- reply_count=0・KOL なし——T3 signal ゼロ。

**判断（初観測）**:
- [[external-event-to-token-pattern]] の典型入口——外部イベント（米国250周年）を借用、twitter/website 完全ゼロ × traction0。
- real_sol ~67.7 SOL は deployer が自己資金を pool に注入した可能性（[[rug-anatomy]] ⑬型候補——$FINLEY/$GIRLS と同水準）。高 real_sol が生存保証にならないことは N=2 実証済（$FINLEY 82.6SOL→-92.2% / $GIRLS 82.9SOL→-98.6%）。
- $LEBRON23/$EPSTEIN/$LEGACY 等の event-driven コホートと比較すると $84k は larger peak 圏に入るが、social 基盤ゼロは同型パターン。
- ⚠️ twitter/website ゼロ + traction0 は [[rug-anatomy]] 赤旗フル一致。real_sol 存在が唯一の differentiator——deployer exit 流動性として機能するリスク。

**死亡確定（2026-06-27・auto-track）**: peak $104,473→last $1,707（peak比-98.4%）。cause: mcap枯れ。status→dead。
- [[external-event-to-token-pattern]] の典型死亡——外部イベント命名（米国250周年・Semiquincentennial）× twitter/website 完全ゼロ × traction0 → 縮退死。real_sol ~67.7SOL でも deployer exit 需要を超える有機的買い皆無。→[[rug-anatomy]]死亡台帳追記。

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated・$84k・実流動性あり）
- [[external-event-to-token-pattern]]（米国250周年イベント命名）
- [[rug-anatomy]]（traction0・real_sol deployer exit候補・⑬型）
