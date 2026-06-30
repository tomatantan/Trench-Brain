---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=102（dead 65 / tracked 37＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 64%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-51.8%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 54/64 (84%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 3/19 (16%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 61/92 (66%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 54/64 (84%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 3/19 (16%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 59/91 (65%) |
| animal | 5/9 (56%) |
| AI/agent | 1/2 (50%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 31/31 (100%) |
| 10-50k | 17/27 (63%) |
| 200k-1M | 3/6 (50%) |
| 50-200k | 14/35 (40%) |
| >1M | 0/3 (0%) |

## ★ KOL gate 限定: peak $12–16k が生死分水嶺（2026-07-01 研究）

KOL=true 全10件を peak で分割すると dead 側と tracked 側が完全分離する。

| peak 帯 | 結果 |
|---|---|
| < $12k（dead最大=$11.5k） | 4/4 dead（100%） |
| > $16k（tracked最小=$16.7k） | 6/6 tracked（100%） |

- $12–16k gap 内に該当銘柄なし＝自然な分離境界。
- 解釈：KOL 言及後に $12k 未満で天井を打った = 「KOL が買い圧に変換されなかった」early-warning。
- 比較：全gate 先行研究では $50k が境界（不確定 N小）。KOL gate 限定では $16k という低いラインで完全分離 → KOL タグ自体が実質的な mcap 閾値を引き下げる効果がある可能性。
- **実用**: KOL銘柄が $12k を超えなければ「KOL空振り・撤退候補」。N=10 小なので要継続追跡。

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死31/31 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死54/64 (84%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死3/19 (16%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
