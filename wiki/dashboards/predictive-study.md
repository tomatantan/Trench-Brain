---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=80（dead 54 / tracked 26＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 68%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-50.9%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 43/47 (91%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 3/14 (21%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 50/70 (71%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 43/47 (91%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 3/14 (21%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 50/71 (70%) |
| AI/agent | 1/2 (50%) |
| animal | 3/7 (43%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 26/26 (100%) |
| 10-50k | 15/21 (71%) |
| 200k-1M | 2/4 (50%) |
| 50-200k | 11/27 (41%) |
| >1M | 0/2 (0%) |

## ⑥ graduated gate 内での peak $100k 閾値（2026-06-30 精密化）
> 先行「$50k超・全gate・不確定」を graduated gate 限定・$100k で再検証。
| 群 | dead | tracked | 生存率 |
|---|---|---|---|
| graduated × peak >$100k | 5 | 3 | **37.5%**（N=8） |
| graduated × peak ≤$100k | 38 | 1 | **2.6%**（N=39） |
判定: **不確定（方向性強・時間バイアス未除去）**
→ graduated 内でも peak $100k 超は"弱い生存傾斜"あり。ただし >$100k 群でも死亡 62.5%＝graduated の呪い（91%）を override できない。実用: graduated を拾うなら peak $100k 超が最低足切り条件、それでも保証はない。

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死26/26 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死43/47 (91%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死3/14 (21%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
