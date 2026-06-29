---
type: entity
kind: token
source: auto-track
status: watch
title: $GUTCHU-GzfBEf（GUTCHU）
mint: GzfBEfLVzNUgAnPHacitJhoQ8VQgNT94kqinTGEDpump
created: 2026-06-30
updated: 2026-06-30
tags: [trench, entity, token, auto-track, prebond, breakout, traction0, same-name-2nd]
---

# $GUTCHU-GzfBEf（GUTCHU）

同名先行 mint（DJjg...）は死亡済 → [[$GUTCHU]]。本 mint は2代目。

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | GzfBEfLVzNUgAnPHacitJhoQ8VQgNT94kqinTGEDpump |
| pool | AZdBx1YQddxdu5oxcEs8D8HKiEtrmqKW8NhJgnZwjkog |
| gate | safety:ok / traction:mcap>=30000 |
| mcap(birth観測) | $49,274（2026-06-29T16:37Z） |
| mcap(BREAKOUT +106%) | $101,316（2026-06-29T16:37Z・同バッチ内） |
| peak_mcap | $101,316（暫定） |
| real_sol | ~3.26 SOL（3262869501 lamports・BREAKOUT時点） |
| reply_count | 0（全観測） |
| twitter | null |
| website | null |
| tokenized_agent | false |
| complete | false（prebond継続） |
| status | watch |
| auto-track birth | 2026-06-29T16:37Z |

<!-- synthesis:start -->
**観測（事実）**
- pump.fun 産・prebond（complete=false）・$49k で検知→同観測バッチ内で +106% BREAKOUT → $101k。
- twitter/website 未設定・reply_count=0・KOL なし。real_sol 3.26SOL（BREAKOUT時）。
- 先行同名 mint（DJjg...）は $46k birth → +81% BREAKOUT 後 $510 枯死。名称を再利用した 2nd attempt。

**判断**
- birth → BREAKOUT が同一観測バッチ内で完結 = whale 単独 pump の典型シグネチャ（[[launchpad-economics]] traction0 × 出来高先行）。social 皆無 × real_sol 3.26SOL での $100k 到達 = organic 需要ゼロ確定候補。
- 先行 mint（DJjg...）が同型 BREAKOUT 後 $510 枯死——2nd attempt でも同パス最有力。
- ⚠️ real_sol 3.26SOL（prebond）× mcap $100k の乖離は deployer 自転車 pump の可能性。bonding curve 未卒業での $100k 超は外部需要が先行するか whale pump のどちらか——traction0 の現状では後者。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（prebond BREAKOUT × traction0 × 同名 2nd attempt）
- [[rug-anatomy]]（social 皆無 × real_sol 低値 × whale pump 疑い）
- [[$GUTCHU]]（先行死亡 mint・同型 BREAKOUT-then-dead 前例）
