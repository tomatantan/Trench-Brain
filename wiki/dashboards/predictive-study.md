---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=83（dead 55 / tracked 28＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 66%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-51.5%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 44/48 (92%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 3/16 (19%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 51/73 (70%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 44/48 (92%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 3/16 (19%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 51/74 (69%) |
| AI/agent | 1/2 (50%) |
| animal | 3/7 (43%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 26/26 (100%) |
| 10-50k | 16/22 (73%) |
| 200k-1M | 2/4 (50%) |
| 50-200k | 11/28 (39%) |
| >1M | 0/3 (0%) |

### ⑥ ★gate × peak 交差項（2026-06-30 実証）
> ⑤の「50-200k = 39%死」は gate mix の平均値。gate 別に分解すると最大 75pt 差。

| gate + peak帯 | dead | tracked | 死亡率 |
|---|---|---|---|
| graduated + $50k-$200k | 9 | 3 | **75%** |
| mcap>=30k + $50k-$200k | 2 | 8 | 20% |
| KOL + $50k-$200k | 0 | 4 | **0%** |
| 全体（ベースライン⑤） | 11 | 15 | 39% |

→ **peak 規模は gate を条件として初めて意味を持つ。peak $80k でも gate=graduated なら死亡率75%、gate=KOL なら0%。**
/check 判定に「graduated + peak <$200k = 高peakでも要警戒」ラベル追加を推奨。
★時間バイアス留意: graduated は古め/mcap>=30k は新着多い可能性あり → 前向き追跡で確認。

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **gate × peak は独立でなく交差する**: peak 50-200k 帯でも gate=graduated は75%死、gate=KOL は0%死（N=26, ⑥）。peak 単独の予測力は gate mix 平均であり過小/過大評価を同時に生む。
- **peak mcap <10k ＝ 死26/26 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死44/48 (92%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死3/16 (19%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
