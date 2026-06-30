---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=85（dead 57 / tracked 28＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 67%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-52.9%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 46/50 (92%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 3/16 (19%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 53/75 (71%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 46/50 (92%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 3/16 (19%) |

### ④-b ★KOL内 peak規模交互作用（2026-06-30 研究）
| 群 | 死亡率 | 備考 |
|---|---|---|
| KOL × peak < $12k | 4/4 (100%) | 全滅・完全分離 |
| KOL × peak $12-30k | 0/1 (0%) | $$TUPID のみ・灰色ゾーン |
| KOL × peak >= $30k | 0/5 (0%) | 全生存・N=5 |

> **観察**: KOL 言及銘柄の中で peak $30k を超えた群は現時点で全員生存。$30k = mcap>=30000 ゲート閾値と同値であり、「KOL + mcap壁突破の両立」が生存の合流点の可能性。mcap>=30000 gate との共線性が強く、独立因子としての確証は要追跡（N=5・時間バイアス未除去）。

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 52/75 (69%) |
| AI/agent | 1/2 (50%) |
| animal | 4/8 (50%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 26/27 (96%) |
| 10-50k | 17/23 (74%) |
| 200k-1M | 2/4 (50%) |
| 50-200k | 12/28 (43%) |
| >1M | 0/3 (0%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死26/27 (96%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死46/50 (92%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死3/16 (19%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
