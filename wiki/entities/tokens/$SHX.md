---
type: entity
kind: token
source: auto-track
status: dead
ticker: $SHX
mint: 86UWvt4HWFAFeqJHe3r8LUJoU9XhrRqq6KWsJXsBpump
created: 2026-06-29
updated: 2026-06-29
tags: [token, pumpfun, prebond, traction0, dog-meme, shiba-derivative]
---

# $SHX — Shibax（86UWvt）

pump.fun 発。bonding curve **未卒業（complete=false）**。名称は Shiba 派生（Shibax）。twitter なし・website なし・KOL なし・reply_count=0。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 86UWvt4HWFAFeqJHe3r8LUJoU9XhrRqq6KWsJXsBpump |
| name | Shibax |
| pool_address | 3wNZoJsZEFycsS9CwebYe21dg1HZx1PdRmQS2zbfsCML |
| 初検知 mcap | $121,878（2026-06-29T10:22Z） |
| gate | safety:ok / traction:mcap>=30000 |
| reply_count | 0 |
| KOL（CA確認） | なし |
| twitter | null |
| website | null |
| tokenized_agent | false |
| real_sol | 4,420,402,259（lamports） |
| complete | false（prebond継続） |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun 産・prebond・$121,878 で検知。
- "Shibax" = Shiba + X 接尾辞。Shiba 系は $SHIB/$SHIBX/$SHIBAINU 系の連想を狙う命名。
- traction 指標全ゼロ（reply/KOL/twitter/website なし）。real_sol 高値（lamports 換算で ~26 SOL 相当）。

**判断**:
- Shiba 派生は crypto trench の最も汎用的な命名カテゴリの一つ。「X」接尾辞は差別化を試みているが、記憶性は低い（[[survivor-memes]] の条件：十分に差別化されていない）。
- traction 全ゼロ × prebond = narrative なし stub。real_sol 数値は high だが lamports 単位で実質 ~26 SOL ——ある程度の bond は入っているが community signal はない。
- [[launchpad-economics]] 標準候補：traction 待ち。signal なければ典型崩壊パス。

**接続概念**: [[launchpad-economics]] 直下（prebond traction0 標準候補）。

---

### 2026-06-29 死亡確定（mcap枯れ）

**観測（事実）**
- peak_mcap: $145,979（2026-06-29T10:22Z観測）
- last mcap: $589（2026-06-29T13:30Z）——peak 比 -99.6%。
- complete=false（prebond のまま死亡）・real_sol=70957031 lamports（~0.07SOL 残存）。
- tokenized_agent=true——prebond tokenized_agent 宣言銘柄として記録。

**死因・型**
- 「prebond 枯れ死」：bonding curve 未卒業のまま mcap が $589 まで枯れた。
- tokenized_agent=true × twitter/website 皆無 × traction0 = AI agent 宣言だけで community 需要が伴わなかった事例。[[ai-memes]] 接続の観点では「tokenized_agent フラグ ≠ traction 保証」の N 追加。
- peak $146k は本バッチ死亡銘柄中最高 peak。高 peak でも prebond × social 皆無 × traction0 なら崩壊パスは変わらない。

**outcome**: died（mcap枯れ・peak比-99.6%）
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（prebond・traction0 標準候補）
- [[survivor-memes]]（Shiba 派生命名 — 汎用カテゴリ・差別化薄）
