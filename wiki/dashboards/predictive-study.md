---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=62（dead 41 / tracked 21＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 66%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-41.7%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 32/34 (94%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 1/9 (11%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 37/52 (71%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 32/34 (94%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 1/9 (11%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| other | 39/56 (70%) |
| AI/agent | 1/2 (50%) |
| animal | 1/4 (25%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 24/24 (100%) |
| 10-50k | 9/18 (50%) |
| 200k-1M | 1/2 (50%) |
| 50-200k | 7/16 (44%) |
| >1M | 0/2 (0%) |

## ★gate × peak 交互作用（2026-06-29 研究追加）

> 仮説: 「peak mcap の予測力は gate の種類に条件付きである」— 検証済み（KOL N=10, graduated N=34）

| gate | peak閾値 | 死亡率 | 解釈 |
|---|---|---|---|
| KOL + peak < $15k | 4件 | **4/4 (100%)** | KOL言及が「実買い」に届いていない |
| KOL + peak ≥ $15k | 6件 | **0/6 (0%)** | 実買い転換済み → 生存 |
| graduated + peak ≥ $50k | 8件 | **7/8 (88%)** | peak 大でも死 |
| graduated + peak < $50k | 26件 | **25/26 (96%)** | peak 小でも同率で死 |

**結論**: KOL gate では peak $15k が生死を明確に分離する。graduated gate では peak 大小にかかわらず ~90% 死——peak は graduated の生死を予測しない。  
理由: KOL peak = 実買い転換の証拠 / graduated peak = ボンカーブ突破の人工 pump であり卒業後のサポートが消える。  
「graduated 銘柄が大きく跳ねたから本物」は誤り。gate=graduated は peak にかかわらず avoid。  
★時間バイアス留意（KOL tracked 6件はまだ死にうる）。

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死24/24 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死32/34 (94%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死1/9 (11%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
