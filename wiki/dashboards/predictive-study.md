---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=90（dead 59 / tracked 31＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 66%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-52.1%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 48/54 (89%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 3/17 (18%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 55/80 (69%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 48/54 (89%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 3/17 (18%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 54/80 (68%) |
| AI/agent | 1/2 (50%) |
| animal | 4/8 (50%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 28/28 (100%) |
| 10-50k | 17/23 (74%) |
| 200k-1M | 2/5 (40%) |
| 50-200k | 12/31 (39%) |
| >1M | 0/3 (0%) |

## ★KOL × peak tier 交互作用（研究: 2026-06-30）
| KOL=true × peak tier | 死亡率 |
|---|---|
| peak < $12k | 4/4 (100%) |
| peak >= $12k | 0/6 (0%) |

完全分離（N=10）。境界は $11,512（最高 dead = $BALDI）と $16,713（最低 tracked = $$TUPID）の間。
**既存仮説「$5k未満で全滅」を更新**: $BALDI（peak $11.5k）が dead → 境界は ~$12k が正確。
$5k-$12k を「KOL付きで安全」と読むのは誤り——KOL効果は peak $12k 超えで初めて実績として立つ。

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死28/28 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死48/54 (89%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死3/17 (18%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
