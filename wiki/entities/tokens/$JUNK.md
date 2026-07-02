---
type: entity
kind: token
source: auto-track
status: tracked
title: $JUNK (JUNKBOT)
created: 2026-07-02
updated: 2026-07-02
tags: [trench, entity, token, auto-track, high-real-sol, breakout]
---

# $JUNK（JUNKBOT）

> auto-track entity。gate通過（graduated）。real_sol=81.6SOL で⑬コホート候補。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | `EpfoYfZLxU42XJ92Yj1DWT9DCCX85pNop4NsJyuipump` |
| name | JUNKBOT |
| mcap（初観測） | ~$83,442 → **+98%→$132,164**（2026-07-02T11:40Z） |
| gate | safety:ok / traction:graduated（complete:true） |
| status | tracked |
| reply_count | 0 |
| real_sol | **81.64 SOL**（⑬コホート水準） |
| twitter | https://x.com/junkbotsol |
| website | https://junkbot.my/ |
| pool | DE7DwPg4r8MHkWerUz1bp8WTLpwTrEr3U374D9RnZ8CP |

<!-- synthesis:start -->
## 合成メモ（synthesis）

- **正体**: "JUNKBOT" というbot/ゴミ系のmeme名。twitter @junkbotsol + website junkbot.my/ と social体裁は整備済み。
- **signal**: reply0 / KOL0。ただし **real_sol=81.64SOL** は [[$FLYRO]] (84.4SOL)・[[$VELA]] (84.47SOL) と同水準。⑬コホート（high real_sol ≠ 生存保証）に分類される水準——「poolに大量SOLが入っていてもKOL/tractionゼロなら崩壊」型の観測候補。
- **⚠️**: real_sol 高値は初期 deployer/whale の流動性供給を示す可能性 or 集中保有の証。birth後即+98%の mcap上昇（$83k→$132k）も traction ゼロのまま＝出来高先行 whale pump の疑い強。traction が伴わなければ[[rug-anatomy]] ⑬型パターンに沿って崩壊する最有力候補（BREAKOUT-then-dead or ⑬高real_sol崩壊）。
- **概念接続**: [[launchpad-economics]]（⑬コホート監視）/ [[rug-anatomy]]（high real_sol × traction0 赤旗）。

---

### 2026-07-02 BREAKOUT 更新（+152%・$132k→$333k）

**観測（事実）**
- 2026-07-02T11:56Z: mcap $132,164 → $333,104（+152%）。flags=[BREAKOUT, mcap+152%]。
- complete=true 継続。reply_count=0 不変。real_sol ~81.6SOL（81,644,054,091 lamports）— 初観測から変化なし。
- twitter/website 変わらず。KOL言及なし。

**判断**
- birth後+98%に続く 2段目 BREAKOUT。traction ゼロ全期間。real_sol 不変のまま価格上昇 = deployer pool SOL の継続供給または whale 買い継続。
- ⑬コホート（real_sol ~81-84SOL）の先例: $FLYRO(84.4SOL→-98.5% dead)/$VELA(84.47SOL→-97.6% dead) は1段で崩壊。$BOO(82.7SOL)は2段 BREAKOUT 後 $709k まで到達——$JUNK は $BOO 型の 2段ルートに入った可能性。
- ⚠️ $BOO が崩壊前に 2段 BREAKOUT を見せたことを踏まえると、$333k が崩壊前の最終つり上げである可能性が最大。traction が伴わない限り BREAKOUT-then-dead 最有力。
- [[launchpad-economics]] 跳躍台帳追記済。
<!-- synthesis:end -->
