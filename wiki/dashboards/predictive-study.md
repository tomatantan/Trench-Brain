---
type: dashboard
title: 魔界 predictive study（何が運命を分けるか・実証）
updated: auto
tags: [feedback, predictive, study, edge]
---

# 魔界 predictive study — 死の分母dataで「何が運命を分けるか」

> `brain/predictive_study.py`。母集団 N=27（dead 13 / tracked 14＝**pendingでまだ死にうる=death率は下限**）。
> baseline 死亡率 48%。各因子はこれとの比較で読む。★現mcap近似・N小cell留意・同一launchpad/近時間で独立性限定。

## 死の深さ: 「平均 -23.6%」は虚数——死は peak mcap で二類型に分岐する

> research 2026-06-28: dead 13件を peak $10k 境界で分割検証。N=13 / 例外ゼロ。

| 類型 | peak mcap | drawdown 中央値 | 挙動 |
|---|---|---|---|
| **即死型** (N=10) | < $10k | **≈ 0%** | cur ≈ peak のまま枯れる。崩落を待つ必要なし。 |
| **崩落型** (N=3) | ≥ $10k | **≈ 97%** | 跳ねた後 1 サイクル以内に -90%超急落 |

★**平均 -23.6% は二極の混合値 = 単体では監視基準にならない**。
- 低 peak 銘柄: 追跡開始時に「小 peak = 実質終了」と即判定する（崩落シグナル待ち不要）
- 高 peak 銘柄: cur/peak が急落し始めたら 1 サイクル以内に早期判定が必要

## 次元別 死亡率（高い順）

### ① entry門別
| 因子 | 死亡率 |
|---|---|
| graduated | 5/5 (100%) |
| user_checked | 4/9 (44%) |
| KOL言及 | 3/9 (33%) |
| mcap勢い門 | 1/4 (25%) |

### ② traction(KOL/reply)有無
| 因子 | 死亡率 |
|---|---|
| traction無 | 10/18 (56%) |
| traction有 | 3/9 (33%) |

### ③ ★交互作用 gate×traction（最も効く組合せ）
| 因子 | 死亡率 |
|---|---|
| graduated × tr無 | 5/5 (100%) |
| user_checked × tr無 | 4/9 (44%) |
| KOL言及 × tr有 | 3/9 (33%) |
| mcap勢い門 × tr無 | 1/4 (25%) |

### ④ テーマ別
| 因子 | 死亡率 |
|---|---|
| AI/agent | 1/1 (100%) |
| other | 11/23 (48%) |
| animal | 1/3 (33%) |

### ⑤ peak mcap規模別
| 因子 | 死亡率 |
|---|---|
| <10k | 10/10 (100%) |
| 10-50k | 2/7 (29%) |
| 50-200k | 1/8 (12%) |
| 200k-1M | 0/1 (0%) |
| >1M | 0/1 (0%) |

## ★結論（/check の予測根拠・N>=5のcellのみ）
- **peak mcap <10k ＝ 死10/10 (100%)**＝最も clean な死signal（小peakは事実上全滅・mcap勢いが立たない銘柄は乗らない）。
- **最悪の gate×traction**: graduated × tr無＝死5/5 (100%)＝最強のavoid。
- **最良の gate×traction**: KOL言及 × tr有＝死3/9 (33%)＝相対的に生存（[[manipulation-playbook]]で偽traction除外が前提）。
- traction(KOL/reply)と mcap勢い門が生存方向、graduated-but-empty が死方向＝[[launchpad-economics]]/[[survivor-memes]]と整合。
- 死は崩落型（平均drawdown 上記）＝「fadingだから様子見」は通用しない＝早期判定が要。
- 重みは `brain/state/risk_weights.json` に出力＝[[/check]] が単純照合でなく**経験的重み付き予測**に使える。

関連: [[launchpad-economics]] [[survivor-memes]] [[rug-anatomy]] [[manipulation-playbook]] [[feedback]] [[kol-track-records]]
