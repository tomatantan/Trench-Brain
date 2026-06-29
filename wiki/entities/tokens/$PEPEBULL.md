---
type: entity
kind: token
source: auto-track
status: watch
title: $PEPEBULL（The PEPE Bull）
mint: DVt8WDxWLCUMiyEwCVgbg1PQ1RpQTMKckp2cF8S1pump
pool: CRpYJRUFkQNFeEVoJvGrMCFBiaywdz3FanR1hAdcXk9L
created: 2026-06-29
updated: 2026-06-29
tags: [trench, entity, token, auto-track, watch, breakout]
---

# $PEPEBULL（The PEPE Bull）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | DVt8WDxWLCUMiyEwCVgbg1PQ1RpQTMKckp2cF8S1pump |
| pool | CRpYJRUFkQNFeEVoJvGrMCFBiaywdz3FanR1hAdcXk9L |
| gate | safety:ok / traction:mcap>=30000 |
| mcap(birth観測) | $38,154（2026-06-28T21:35Z） |
| mcap(BREAKOUT観測) | $79,922（2026-06-29T13:30Z、+102%） |
| peak_mcap | $79,922（暫定） |
| real_sol | 5（lamports）——BREAKOUT時点で実質ゼロ |
| reply_count | 0 |
| twitter | null |
| website | null |
| tokenized_agent | false |
| complete | false（prebond継続） |
| status | watch |
| auto-track birth | 2026-06-28T21:35Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-29 初回合成（auto-track birth）

**観測（事実）**
- pump.fun 産・complete=false（bonding curve 未卒業）・2026-06-28T21:35Z 検知。
- mcap $38,154。real_sol ~21 SOL・reply_count=0・kol_ca 空・twitter=null・website=null。

**動線・型**
- [[launchpad-economics]]: "The PEPE Bull" = PEPE（最大 survivor meme）× bull market の複合命名。既存人気 meme への派生乗り型として trench 標準。
- complete=false（prebond継続）= $38k での bonding curve 中途段階。graduation できるかが最初の分岐点。
- real_sol ~21 SOL は中程度（⑬コホート 82SOL+ には遠い）。traction0 との組み合わせでは pump 引力として弱い。
- ⚠️ social 皆無（twitter/website 両方 null）× traction0 = PEPE 命名の引力頼みで独自需要の根拠なし。

**賭け仮説**（confidence=低）
- PEPE brand 派生 × graduation 未達 × traction0 = [[rug-anatomy]] "traction0 × prebond 出来高先行" 候補。graduation 到達すれば [[survivor-memes]] 評価対象、未達なら prebond 圏消滅。

---

### 2026-06-29 BREAKOUT 更新（+102%・$39.5k→$79.9k）

**観測（事実）**
- 2026-06-29T13:30Z: mcap $39,508 → $79,922（+102%）。flags=[BREAKOUT]。
- complete=false 継続（prebond のまま BREAKOUT）。real_sol=5（実質ゼロ lamports）。
- reply_count=0・twitter=null・website=null 変わらず。

**判断**
- traction 全ゼロ × real_sol=5 のまま +102% = organic 需要の証拠ゼロ——whale 単独またはbot pump の可能性が高い。[[rug-anatomy]] ⑦/③ "traction-less BREAKOUT → 即死" パターン候補。
- prebond で $80k 到達は bonding curve の力学上可能だが、bonding curve 未卒業 × real_sol≒0 = organic 需要ゼロ確定候補（[[launchpad-economics]] $PEAK/$AEGIS/$0TT 同型）。
- ⚠️ PEPE brand 派生命名で graduation + KOL 言及が来た場合は [[survivor-memes]] 再評価。ただし現状の根拠は命名のみ。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
- [[survivor-memes]]
