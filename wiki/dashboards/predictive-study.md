---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=207（dead 127 / tracked 80＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 61%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: dead銘柄の平均drawdown **-52.3%**（peak比）＝死は「フェード」でなく「崩落」

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 109/124 (88%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 6/28 (21%) |
| mcap勢い門 | 8/46 (17%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 121/179 (68%) |
| traction有 | 6/28 (21%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 109/124 (88%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 6/28 (21%) |
| mcap勢い門 × tr無 | 8/46 (17%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| finance | 3/4 (75%) |
| other | 110/177 (62%) |
| animal | 10/17 (59%) |
| AI/agent | 4/8 (50%) |
| IP/brand | 0/1 (0%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 60/63 (95%) |
| 10-50k | 30/41 (73%) |
| 50-200k | 30/77 (39%) |
| 200k-1M | 5/16 (31%) |
| >1M | 2/10 (20%) |

## ⑥ KOL×peak 交互作用（2026-07-02 研究）

> kol=true 全 15 件を peak で分割。

| 群 | dead | tracked | 死亡率 |
|---|---|---|---|
| kol=true + peak >= $40k | 0 | 9 | **0%** |
| kol=true + peak < $40k | 4 | 2 | 67% |
| 全体 50-200k 帯（参考） | — | — | 39% |

- kol=true + peak >= $40k: $MEEP/$YAJUCOIN/$ARENA/$GLUE/$TJR/$JOTCHUA/$USELESS/$SPX/$MUTUMBO — 全員生存（N=9）
- kol=true + peak < $40k dead 例: $BALDI(11.5k)/$SAMPAIO(2.1k)/$DEATHNOTE(2.9k)/$MUTUMBO(1.8k)
- **逆転異常**: $URL(peak 7.5k, tracked) < $BALDI(peak 11.5k, dead) — peak 単独では KOL 銘柄の全順序はつかない
- **解釈**: KOL 言及は「保険」ではなく「一定規模まで伸びた後に死を回避する触媒」。小 peak に貼られた KOL ラベルは免除にならない
- **前向き検証**: $URL・$$TUPID(16.7k) が今後 dead になるか否かが "$40k 境界の普遍性" を決める

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死60/63 (95%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死109/124 (88%)＝最強のavoid。
- **最良の gate×traction**: mcap勢い門 × tr無＝死8/46 (17%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
