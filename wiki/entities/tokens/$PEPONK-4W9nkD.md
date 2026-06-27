---
type: entity
kind: token
source: auto-track
status: watch
ticker: $PEPONK
mint: 4W9nkDkmhVokuv84yeNkSMHQxh1Ta35GMkYMsACbpump
created: 2026-06-26
updated: 2026-06-26 (BREAKOUT継続+40%・peak $192k・traction0継続)
tags: [token, pumpfun, graduated, traction0, multi-mint, breakout]
---

# $PEPONK — PEPONK（4W9nkD）※2nd mint

pump.fun 発。bonding curve 卒業済（complete=true）。名称「PEPONK」——先行 mint（2LAk8gf）が -94.7% 即死（N=139・[[rug-anatomy]]）後の 2 本目 mint。今回は twitter @peponkwtf（正規アカウント）・website peponk.io が正しく設定されている（先行 mint はフィールド混同あり）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 4W9nkDkmhVokuv84yeNkSMHQxh1Ta35GMkYMsACbpump |
| name | PEPONK |
| 初検知 mcap | $37,861（2026-06-26T02:12Z） |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL（CA確認） | なし |
| twitter | https://x.com/peponkwtf |
| website | https://peponk.io |
| tokenized_agent | false |
| real_sol | 0 |
| 先行 mint | [[$PEPONK]]（2LAk8gf・dead・-94.7%） |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|---|-----------|------|------|
| 初検知(02:12Z) | $37,861 | — | graduated。reply:0・KOLゼロ。real_sol 0。@peponkwtf・peponk.io 整備済（先行 mint より整合性高い）。 |
| BREAKOUT(02:52Z) | $129,693 | prev $41,568 → **+212%** | BREAKOUT 確定。reply:0・KOL ゼロ継続。traction0 × 出来高先行。 |
| mcap+40%(05:27Z) | $192,393 | prev $137,285 → **+40%** | BREAKOUT 継続。peak更新。reply:0・KOL ゼロ変わらず。traction0 で $192k まで伸長。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- graduated・$37,861（初検知）。real_sol 0。reply 0・KOL なし——全追跡窓を通じて traction0 継続。
- 先行 mint（2LAk8gf）は -94.7% 即死（[[rug-anatomy]] N=139）。今回は 2 本目で再挑戦。
- twitter @peponkwtf・website peponk.io が整合した形で設定（先行 mint はフィールド混同）。
- **BREAKOUT（02:52Z）**: $41,568 → $129,693（+212%）。traction なし × 出来高先行。
- **BREAKOUT 継続（05:27Z）**: $137,285 → $192,393（+40%）。peak $192k 更新。traction0 のまま。

**判断**:
- $37k → $192k（+407%）を traction 0 で達成——pure 出来高先行型 BREAKOUT の延長。同ブランド 2nd mint でも community が戻らない状態でここまで上昇する事例。
- traction なき上昇が続くほど、[[launchpad-economics]] BREAKOUT-then-dead 崩壊リスクは蓄積。reply 0 の新規参入者は「動いてるから買う」系——需要の薄さが崩壊を急激にする典型。
- ⚠️ ただし $192k はこのブランドの先行 mint peak（$24,560）の 7.8x——同ブランド 2nd mint が 1st mint を完全に超えた。traction がついてくれば持続可能性が出る。⚠️両論。
- 次窓分岐: traction 0 継続 → BREAKOUT-then-dead 崩壊（先行 mint再現）。reply/KOL 流入 → 持続上昇（新事例）。

**概念接続**:
- [[launchpad-economics]]: 同ブランド 2nd mint × traction0 BREAKOUT $192k（跳躍台帳追記済）
- [[rug-anatomy]]: real_sol 0 × traction0 × 高値滞在——崩壊前の典型局面候補

<!-- synthesis:end -->

## 関連
- [[$PEPONK]]（先行 mint・2LAk8gf・dead・N=139）
- [[launchpad-economics]]（graduated・$38k・multi-mint）
- [[rug-anatomy]]（同ブランド再登場型候補）
