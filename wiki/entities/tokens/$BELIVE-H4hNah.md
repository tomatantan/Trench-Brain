---
type: entity
kind: token
source: auto-track
status: dead
outcome: died
title: $BELIVE-H4hNah（belive 2nd mint）
mint: H4hNahdT297cjC3pZKizAkfGGZrtF2kcuwTUHFwtpump
created: 2026-07-02
updated: 2026-07-02
tags: [token, auto-track, prebond, traction0, social-null, multi-mint, dead-denominator]
---

# $BELIVE-H4hNah（belive 2nd mint）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | H4hNahdT297cjC3pZKizAkfGGZrtF2kcuwTUHFwtpump |
| pool | BzoGELPP4qtD1A6EDrV3NeRbDtcvWCs2ZVKdGBQsYW77 |
| gate | safety:ok / traction:mcap>=30000 |
| mcap(birth) | $50,597（2026-07-01T22:15Z） |
| real_sol | ~1.364 SOL（1,364,033,075 lamports） |
| reply_count | 0 |
| twitter | null |
| website | null |
| tokenized_agent | false |
| complete | false（prebond継続） |
| status | watch |

<!-- synthesis:start -->
**観測（事実）**
- pump.fun 産・prebond 継続（complete=false）・$50k で traction:mcap>=30000 門通過。
- twitter/website ともに null——social 窓口ゼロ全期間。
- reply=0・T3 KOL 皆無（kol_ca=[]）。real_sol ~1.36 SOL（低値）。
- "belive" という命名——同名の別 mint [[#$BELIVE（64oYF5U...）]] が既存で BREAKOUT→$153k まで到達中。
- **multi-mint**: 同名同スペル（"belive"）で 2 本が並走中。

**判断**
- 64oYF5U mint（メイン）が +123% BREAKOUT 後さらに +71% で $153k 到達中なのに対し、本 mint（H4hNah）は $50k prebond でまだ bonding curve 未卒業。
- same-name multi-mint でメイン mint が先行している構造——本 mint は「乗り遅れ」か「便乗 mint」の可能性。メイン mint の BREAKOUT を見て追随 mint を発行するパターン（[[rug-anatomy]] 参照）。
- traction0 × social 皆無 × prebond で $50k は bonding curve 後半——whale pump で gradudate すれば即縮退候補。
- ⚠️ 同名 2 本並走：需要があるなら両方 pump されるが、片方に集中して他は消滅する型（$LIVEWORK 2nd mint が先に死亡した例参照）。

### 2026-07-01T22:43Z DEAD確定（peak $60,733→$459）
**観測（最終）**
- mcap $459（cause: mcap枯れ $459）。peak $60,733 から **-99.2%**。
- 同名メイン mint（64oYF5U...）が $153k で継続中のまま本 mint は消滅——multi-mint 便乗 mint の典型的即死。
- prebond のまま $459 で死亡（bonding curve 未卒業）。

**判断（最終）**
- メイン mint が BREAKOUT 中に便乗発行された 2nd mint が先に死亡——needs の分散ではなく「吸収されて消える」型。
- [[rug-anatomy]] 便乗 mint パターン確定（$LIVEWORK-5faKbh 同型）。

**接続概念**: [[launchpad-economics]]（same-name multi-mint → 2nd 即死）/ [[rug-anatomy]]（便乗 mint 即死型）
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
- [[$BELIVE]] — 同名メイン mint（64oYF5U...）
