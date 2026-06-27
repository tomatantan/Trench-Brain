---
type: entity
kind: token
source: auto-track
status: watch
ticker: $MIDAS
mint: D5HEmWz9B1TQ95dVntCjMQcKnGA82EVyRvX7M9C8pump
created: 2026-06-27
updated: 2026-06-27 (birth stub・$99.4k・prebond・real_sol=2)
tags: [token, pumpfun, prebond, traction0, mythology-meme, serial-mint]
---

# $MIDAS-D5HEmW — hand of Midas（D5HEmWz）

pump.fun 発。"hand of Midas"——ギリシャ神話の黄金の手ミーム命名。prebond（complete=false）。twitter/website ゼロ。reply:0・KOL なし。**real_sol=2（bonding curve 残量ほぼゼロ）・mcap $99,456**。同日同名 mint が他に 2 本確認（FzWueSL $62k / AfrovPt $37k）——⑨型 serial mint。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | D5HEmWz9B1TQ95dVntCjMQcKnGA82EVyRvX7M9C8pump |
| Pool | 5CvhdmAVE8fjo1RQ2VsYH6xheuQR7gp93MUhneY32NxN |
| name | hand of Midas |
| Gate | safety:ok / traction:mcap>=30000 |
| 初検知 mcap | $99,456（2026-06-27T08:24Z） |
| reply_count | 0 |
| KOL | なし |
| Twitter | null |
| Website | null |
| complete | false（bonding curve 未卒業） |
| real_sol | 2（ほぼゼロ） |
| tokenized_agent | false |
| 同名他 mint | FzWueSL（$62k・07:48Z）/ AfrovPt（$37k・08:24Z） |

<!-- synthesis:start -->
## 合成

**観測**: $99.4k mcap・prebond（complete=false）・real_sol=2・twitter/website ゼロ・reply:0・KOL なし・traction0。

**⚠️ 最大赤旗**: real_sol=2 はほぼゼロ。prebond（bonding curve 未卒業）でこの数値は**curve 残量が枯渇寸前か空**を示す。$99k のプライスアクションに対して bonding curve の SOL 裏付けが事実上存在しない——人工的な価格水準の可能性が高い。

**⑨型 serial mint 確定**: 同日同名 "hand of Midas" mint が 3 本同時存在（FzWueSL $62k・本 mint $99k・AfrovPt $37k）。時刻差約 8 分（AfrovPt 08:30Z → 本 mint 08:38Z）でほぼ同時ローンチ。同一アクター（またはコピー屋）が複数 mint を並行投下——ブランドを共有しつつ liquidity を分散させる典型パターン。

**判断**:
- real_sol≈0 + traction0 + serial mint = [[rug-anatomy]] 即死候補の最高赤旗構造
- 3 mint 競合 → 1 本が勝者（mcap 最高は本 mint）・残り 2 本は流動性喪失
- ただし「勝者」でも traction なき $99k = BREAKOUT-then-dead の初動と同型——KOL/reply 出現なければ graduated 後即崩壊
- prebond 消滅（curve 空）なら graduated にすら至らず死亡も想定内

**概念接続**: [[launchpad-economics]]（prebond traction0・real_sol≈0）/ [[rug-anatomy]]（⑨同ブランド serial mint・curve枯渇型）

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
- [[$MIDAS]](FzWueSL・同名先行 mint)
- [[$MIDAS-AfrovP]](AfrovPt・同名並行 mint)
