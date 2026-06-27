---
type: entity
kind: token
source: auto-track
status: watch
ticker: $CDK
mint: CRYPEyLQdFCivwHpKJULAGPM8MUdnzeTQ8ivmdLGpump
created: 2026-06-26
updated: 2026-06-26 (birth・prebond・$45,553・traction0)
tags: [token, pumpfun, prebond, traction0, pulse-watch]
---

# $CDK — Chill Dancing Kid（CRYPEy）

pump.fun 発。"Chill Dancing Kid" 命名——viral dance meme テーマと推測。bonding curve 未卒業（complete=false）。twitter: null・website: null——social 基盤ゼロ。reply:0・KOL なし。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| Mint | CRYPEyLQdFCivwHpKJULAGPM8MUdnzeTQ8ivmdLGpump |
| Pool | EeEFW7YJmdqiFmJTKjFWM6JCUJvMZAJp1b2UnYAQ4QcK |
| Gate | safety:ok / traction:mcap>=30000 |
| MCap 初検知 | ~$45,553 |
| Reply | 0 |
| KOL | なし |
| Twitter | null（整備なし） |
| Website | null（整備なし） |
| tokenized_agent | false |
| real_sol | 9,352,703 lamports（~9.35 SOL・bonding curve残存） |
| Complete | false（prebond） |
| 作成日（mint） | 2026-06-26（ts: 1782454304） |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|---|-----------|------|------|
| birth 06:22Z | $45,553 | — | prebond・social ゼロ。real_sol ~9.35 SOL。 |
| change 06:42Z | $27,190 | -41.4% | real_sol 5 lamports（≒ゼロ）に急減。bonding curve 実質崩壊。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- 初検知 $45,553 → change $27,190（-41.4%）。
- complete=false（prebond 継続）。reply:0・KOL なし。
- real_sol: 9,352,703 lamports（~9.35 SOL・birth時）→ 5 lamports（≒ゼロ・change時）——bonding curve から SOL がほぼ消失。
- twitter/website ともに null——social 基盤ゼロ。

**判断**:
- -41.4% かつ real_sol が ~9.35 SOL → 5 lamports（実質ゼロ）への急減は bonding curve 資金の消失を意味する。prebond のまま SOL 流出 = 自然崩壊（売り圧 or 流動性離散）が進行中。
- prebond × social ゼロ × traction0 × real_sol 消失 = [[rug-anatomy]] 死亡型への直行シグネチャ。次窓での DEAD 圏（<$1.5k）突入確率が高い。
- ⚠️ 型通り死亡進行中。KOL/reply が出現しない限り転換なし。

**概念接続**: [[launchpad-economics]]（prebond・real_sol 消失型崩壊）/ [[rug-anatomy]]（prebond × traction0 × real_sol 消失 → 死亡直行型）

<!-- synthesis:end -->
