---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=49（dead 26 / tracked 23＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 53%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-30.4%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 18/26 (69%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 3/10 (30%) |
| mcap勢い門 | 1/4 (25%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 23/39 (59%) |
| traction有 | 3/10 (30%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 18/26 (69%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 3/10 (30%) |
| mcap勢い門 × tr無 | 1/4 (25%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| AI/agent | 1/1 (100%) |
| other | 24/45 (53%) |
| animal | 1/3 (33%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 18/20 (90%) |
| 10-50k | 4/12 (33%) |
| 50-200k | 4/13 (31%) |
| 200k-1M | 0/2 (0%) |
| >1M | 0/2 (0%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死18/20 (90%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死18/26 (69%)＝最強のavoid。
- **最良の gate×traction**: KOL言及 × tr有＝死3/10 (30%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
