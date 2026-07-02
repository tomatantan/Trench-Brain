---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=210（dead 131 / tracked 79＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 62%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-53.0%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 112/127 (88%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 6/28 (21%) |
| mcap勢い門 | 9/46 (20%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 125/182 (69%) |
| traction有 | 6/28 (21%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 112/127 (88%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 6/28 (21%) |
| mcap勢い門 × tr無 | 9/46 (20%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| finance | 3/4 (75%) |
| other | 114/179 (64%) |
| animal | 10/18 (56%) |
| AI/agent | 4/8 (50%) |
| IP/brand | 0/1 (0%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 61/64 (95%) |
| 10-50k | 30/42 (71%) |
| 50-200k | 33/77 (43%) |
| 200k-1M | 5/17 (29%) |
| >1M | 2/10 (20%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死61/64 (95%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死112/127 (88%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死9/46 (20%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
