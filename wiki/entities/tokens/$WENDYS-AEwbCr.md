---
type: entity
kind: token
title: $WENDYS-AEwbCr (Wendy's Co・2nd mint)
created: 2026-06-25
updated: 2026-06-25
source: auto-track (pump.fun)
tags: [trench, entity, token, auto-track, duplicate-ticker]
status: dead
---

# $WENDYS-AEwbCr — Wendy's Co（同名2本目 mint）

> `brain/track.py` が観測→篩通過で TRACKED 登録（auto-synthesis）。mint `AEwbCrFTM9ySiWh9mPPzy7Hv9NywJa8LQGpCDEwapump`。
> 同名 [[WENDYS]] (mint 41Ktmp1K...) が既存——別 mint の2本目。
> 事実=下のライフサイクル(自動) / 判断=合成メモ＋関連 [[concepts]]。

## ライフサイクル（auto-track）
- 初観測: 2026-06-25 / 門: **traction:mcap>=30000**（bonding curve 未卒業・complete=false）
- mcap: $98,141 / reply: 0 / tokenized_agent: no / real_sol: 170,770,694（⚠️lamports疑い）
- links: twitter なし / website なし
- pool: `ETfRDYKJLrmKvhnAbXEZhruQrfE747aUHV5unXdqDJcA`
- status: **watch**

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）
- **観測**: 既存 [[WENDYS]](mint 41Ktmp1K・"SIR THIS IS A") と同じ ticker で別 mint が発射。名前は「Wendy's Co」——前者の internet meme 文脈（"Sir This Is A Wendy's"）と異なり、企業名そのまま。mcap $98k（前者 $97k とほぼ同水準）。twitter/website ゼロ・reply 0・KOL 0。
- **判断**: duplicate-ticker の典型。[[SQUEEZE-2Jua7N]]/[[SQUEEZE-9wEUXx]] と同型（同名別 mint が競合発射）。どちらも social 基盤ゼロ・KOL 不在で[[rug-anatomy]]「traction-less 出来高先行」。2本のうち1本が先に出来高を消費すれば、もう1本への資本移動は起きにくい。
- ⚠️: real_sol=170,770,694 は前回 [[WENDYS]] の 4,882,049 より更に大きく lamports 換算疑い（データ異常）。mcap $98k × social ゼロ × 2本目 mint。

**DEAD確定（2026-06-25T05:00）**: peak $98,785 → last $511（peak比-99.5%）。cause: mcap枯れ。duplicate-ticker × traction0 → 型通り崩壊。→ [[rug-anatomy]] 死亡台帳。
<!-- synthesis:end -->

## 関連
[[launchpad-economics]] / [[WENDYS]] / [[rug-anatomy]] / [[external-event-to-token-pattern]]
