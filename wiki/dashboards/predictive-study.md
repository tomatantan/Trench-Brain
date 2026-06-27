---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=21（dead 7 / tracked 14＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 33%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-14.2%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| mcap勢い門 | 1/3 (33%) |
| KOL言及 | 3/9 (33%) |
| user_checked | 3/9 (33%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 4/12 (33%) |
| traction有 | 3/9 (33%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| mcap勢い門 × tr無 | 1/3 (33%) |
| KOL言及 × tr有 | 3/9 (33%) |
| user_checked × tr無 | 3/9 (33%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| AI/agent | 1/1 (100%) |
| animal | 1/3 (33%) |
| other | 5/17 (29%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 6/7 (86%) |
| 50-200k | 1/6 (17%) |
| 10-50k | 0/6 (0%) |
| 200k-1M | 0/1 (0%) |
| >1M | 0/1 (0%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死6/7 (86%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: KOL言及 × tr有＝死3/9 (33%)＝最強のavoid。
- **最良の gate×traction**: KOL言及 × tr有＝死3/9 (33%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
