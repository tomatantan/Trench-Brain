---
type: entity
kind: token
source: auto-track
status: dead
ticker: $BULLARMY
mint: FtWD7st7o5fp6sJ5NTp1jLY1qaRjibzYDTe3xSYpump
created: 2026-07-01
updated: 2026-07-02
outcome: died
tags: [token, pumpfun, graduated, traction0, bull-cluster, community-meme, dead-denominator]
---

# $BULLARMY — Bull Army（FtWD7s）

pump.fun 発。"Bull Army" 命名——bull 集団・軍団 community テーマ。mint: FtWD7st7o5fp6sJ5NTp1jLY1qaRjibzYDTe3xSYpump。twitter @bullarmysolx、website https://bullarmy.fun。graduated（complete:true）。reply=0・KOL なし。real_sol=51,358,024,684（lamports・ ~51 SOL 相当の非ゼロ値）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | FtWD7st7o5fp6sJ5NTp1jLY1qaRjibzYDTe3xSYpump |
| pool | Fj27fEPSgAaeUQxE26v6habcamfCMk15neKZTFYma57u |
| gate | safety:ok / traction:graduated |
| 初検知 mcap | $104,799（2026-07-01T12:47Z） |
| peak_mcap | $104,799（暫定） |
| real_sol | 51,358,024,684 lamports（~51 SOL） |
| reply_count | 0 |
| twitter | https://x.com/bullarmysolx |
| website | https://bullarmy.fun |
| tokenized_agent | false |
| complete | true（graduated） |
| status | watch |
| auto-track birth | 2026-07-01T12:47Z |

<!-- synthesis:start -->
## 合成

**観測（事実）**
- pump.fun 産・graduated・$104k で検知。real_sol ~51 SOL（非ゼロ）・reply=0・KOL なし。
- twitter @bullarmysolx（専用アカウント）・website bullarmy.fun（専用ドメイン）——identity は整備済み。

**シグナル分析**
- real_sol ~51 SOL は [[rug-anatomy]] ⑬コホート（$FLYRO ~84SOL→-98.5% / $GIRLS ~83SOL→-98.6% / $BOO ~83SOL→-98.6%相当）の中間域。deployer が pool に初期流動性として SOL を入れているケースと近似——⚠️ deployer pool pump 疑いの参照ポイント。
- twitter/website 整備済みでも reply=0 全期間 = identity コストはかかっているが social 伝播ゼロ。
- bull cluster 命名（$TESTIBULL / $BELMAR / $DEADSEM / $TBB 等の同期コホート）の一角——bull テーマ飽和環境下での個別優位性なし。
- $104k は [[launchpad-economics]] 50k-200k 帯 = 死亡率 23-25% 域。

**⚠️ real_sol 監視**: 次窓での real_sol 減少 = deployer SOL 引き出し候補 → rug 直前シグナル。$BOO は real_sol 一定でも崩壊。

**概念接続**: [[launchpad-economics]]（graduated × bull cluster 競合環境）/ [[rug-anatomy]]（real_sol ~51SOL × traction0 → ⑬コホート候補）

### 2026-07-01T15:51Z mcap +68%（$103,011→$173,341）
**観測（事実）**
- mcap $103,011→$173,341（flags: mcap+68%）。reply=0・real_sol=51,358,024,684 lamports 変化なし。complete=true。

**判断**
- $103k→$173k まで上昇継続。traction0 全期間のまま $173k 到達。
- real_sol 51 SOL が変化していない = deployer がまだ SOL を引き出していない状態継続。
- [[rug-anatomy]] ⑬コホート（high real_sol × traction0）として監視継続——real_sol 減少が始まった時が警戒水準。
- bull cluster 内での $173k は $TESTIBULL/$BELMAR に比べると低水準だが、traction ゼロのまま上昇継続は BREAKOUT-then-dead パスの前段。
### 2026-07-01T17:25Z DEAD — mcap枯れ（peak$173,341→$1,633・-99.1%）
**観測（事実）**
- 最終 mcap $1,633。peak $173,341 → -99.1%。cause: mcap枯れ。
- reply=0・real_sol=51,358,024,684 lamports（~51 SOL）全期間変化なし。complete=true。twitter @bullarmysolx / website bullarmy.fun 不変。

**死因**
- traction0 全期間のまま peak $173k → -99.1%崩壊。⑬コホート（high real_sol ~51SOL × traction0）の型通り確定死。real_sol ~51 SOL が deployer pool にあっても organic buyer ゼロでは持続不能。
- [[rug-anatomy]] 死亡台帳記録（⑬N追加）。[[launchpad-economics]] graduated × bull cluster × social整備済でも KOL 皆無 = 分母として記録。
<!-- synthesis:end -->

## 関連
[[launchpad-economics]] / [[rug-anatomy]]
