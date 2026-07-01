---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=119（dead 81 / tracked 38＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 68%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-54.5%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 67/76 (88%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 4/10 (40%) |
| mcap勢い門 | 6/24 (25%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 77/109 (71%) |
| traction有 | 4/10 (40%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 67/76 (88%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 4/10 (40%) |
| mcap勢い門 × tr無 | 6/24 (25%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| finance | 3/3 (100%) |
| other | 70/103 (68%) |
| AI/agent | 2/3 (67%) |
| animal | 6/10 (60%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 37/37 (100%) |
| 10-50k | 21/30 (70%) |
| 200k-1M | 3/5 (60%) |
| 50-200k | 19/42 (45%) |
| >1M | 1/5 (20%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死37/37 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死67/76 (88%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死6/24 (25%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

## ★死の形とgate種別（2026-07-01 研究）

> 仮説: gate種別が dead 銘柄の「死に方」を決定する。N小（user_checked=4, mcap_gate=3）のため確証傾向。

| gate | dead N | ghost死（残存率>80%） | pump-dump死（残存率<10%） |
|---|---|---|---|
| user_checked | 4 | 4/4 (100%) | 0/4 (0%) |
| kol | 4 | 3/4 (75%) | 0/4 (0%) |
| mcap>=30000 | 3 | 0/3 (0%) | 3/3 (100%) |
| graduated | ~46 | 17/46 (37%) | 26/46 (57%) |

**構造的説明:**
- user_checked・kol = pump前エントリ → pump来なければ流動性枯渇 → cur≈peakのままghost死
- mcap>=30000 = pump確認後エントリ（$30k到達を捕捉条件とする） → 定義上、常に高点近辺で記録 → cur/peak残存率が低いのは観測の構造的バイアス

**⚠️ 解釈の罠（要注意）:**
mcap_gate dead の残存率が低い＝「崩落した証拠」と早計してはならない。「入場時点が既に高点に近い」という観測バイアスかもしれない。
mcap_gate の生存率が高いこと（25%死）には「$30k超まで到達＝実需がある」という正の選択効果と上記バイアスが混在する——分離できていない。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
