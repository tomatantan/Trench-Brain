---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=72（dead 46 / tracked 26＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 64%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-45.6%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 36/41 (88%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 2/12 (17%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 42/62 (68%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 36/41 (88%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 2/12 (17%) |

### ⑥ ★交互作用 gate×peak（gate は peak の保護効果を上書きする）
> 仮説「高 peak = 本物の需要 → 生存」は graduated 銘柄では不成立と確認（2026-06-29）。

| peak ≥ $50k の群 | dead | tracked | 死亡率 |
|---|---|---|---|
| graduated | 8 | 3 | **72.7%** |
| non-graduated (mcap門/kol門/user_checked) | 2 | 13 | **13.3%** |

差: **59.4 pt**。同じ peak ≥ $50k でも gate が graduated なら死亡率はほぼ変わらない（overall 88% → 72.7%）。
- graduated-dead 高 peak 例: $TOGI(407k), $SHUPPET(140k), $MOONSEM(87k), $ORANGIE(101k) — 大きく跳ねても全滅
- non-graduated-tracked 高 peak 例: $ZERO(2.9M), $滑る猫(972k), $JOTCHUA(11M)

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 43/63 (68%) |
| AI/agent | 1/2 (50%) |
| animal | 2/7 (29%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 25/25 (100%) |
| 10-50k | 11/19 (58%) |
| 50-200k | 9/23 (39%) |
| 200k-1M | 1/3 (33%) |
| >1M | 0/2 (0%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **gate × peak 交互作用（⑥）**: graduated gate は peak $50k 超でも死亡率 72.7%。non-graduated は同条件で 13.3%。**screening 優先度: gate 種別 > peak 規模**。graduated 銘柄の高 peak は「生存根拠」にならない。
- **peak mcap <10k ＝ 死25/25 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死36/41 (88%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死2/12 (17%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
