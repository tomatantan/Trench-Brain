---
type: entity
kind: token
source: auto-track
status: dead
title: $ANSEMWHEEL（Ansem Wheel）
mint: 3i3xCsMzmhGwAMZSojGH7uGEaizkGibBWPnZ5bgnpump
pool: DALvBc3qpd7uZmfbeEjaYmSGhHE15J6TNp5FTtMdAb1p
created: 2026-06-28
updated: 2026-06-28
tags: [trench, entity, token, auto-track, dead]
---

# $ANSEMWHEEL-3i3xCs（Ansem Wheel）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | 3i3xCsMzmhGwAMZSojGH7uGEaizkGibBWPnZ5bgnpump |
| pool | DALvBc3qpd7uZmfbeEjaYmSGhHE15J6TNp5FTtMdAb1p |
| gate | safety:ok / traction:graduated |
| mcap推移 | $28,795（birth 2026-06-28T12:05Z）→ $16,091（-44% 2026-06-28T12:06Z）→ $1,351（死亡 2026-06-28T15:12Z） |
| outcome | died |
| cause | mcap枯れ（peak比-95.3%） |
| real_sol | 0 |
| reply_count | 0 |
| twitter | https://x.com/0xSavior/status/2071202952866418954 |
| status | watch |
| auto-track birth | 2026-06-28T12:05Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-28 初回合成（auto-track birth + mcap-44%）

**観測（事実）**
- pump.fun 産・graduated(complete=true)・2026-06-28T12:05Z 検知。
- birth mcap $28,795 → 次窓 $16,091（-44%）。reply_count=0 のまま。
- real_sol=0・kol_ca 空・kol_ticker 空 = KOL の CA 直接支持未確認。
- twitter: https://x.com/0xSavior/status/2071202952866418954（@0xSavior ツイート）。
- tokenized_agent=false。
- **同名 multi-mint**: 同バッチに同 ticker 別 mint（Av5FFK... peak $5,858）が存在→即死確認済（死亡台帳記録）。

**動線・型**
- [[launchpad-economics]]: graduated・"Ansem Wheel" = @blknoiz06（Ansem）の名を冠したルーレット型 association meme。
- ⚠️ **association marketing 疑い**: deployer が @0xSavior ツイートを設定。kol_ca 空＝ Ansem 本人の CA 言及は sources/x に未確認。名前借用型。
- ⚠️ **real_sol=0**: 有機的買い手のみで $28k 維持が必要。deployer exit バッファなし。
- birth 即 -44% = 初期 holder の profit-take が始まっている。[[rug-anatomy]] dead-spiral 入口候補。
- Ansem 関連 meme のマルチ発射（同バッチに $ANSEMWHEEL 別 mint + 同名 "Ansem's Army"→$🐂🀄 も同時存在）= 需要分散リスク。

**賭け仮説**（confidence=低）
- traction0 × real_sol=0 × -44% 急落 = [[rug-anatomy]] "graduated-but-empty" 標準展開。
- Ansem 本人の言及または KOL 独立裏付けがなければ dead-spiral 最有力。[[survivor-memes]] 到達条件未達。

### 2026-06-28 最終合成（dead確定）

- peak $28,795 → 最終 $1,351（-95.3%・2026-06-28T15:12Z）。cause=mcap枯れ。
- 型通り: Ansem brand association × multi-mint下位 × real_sol=0 × traction0 → dead-spiral 完結。同バッチ Ansem meme（$🐂🀄 Ansem's Army・$MOONSEM）の中で最下位 mint として先に枯死。
- [[launchpad-economics]] / [[rug-anatomy]] の "graduated-but-empty" コホートに追加。生存者バイアスの分母として閉じる。
<!-- synthesis:end -->
