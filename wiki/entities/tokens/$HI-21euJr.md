---
type: entity
kind: token
source: auto-track
title: $HI-21euJr (hi)
created: 2026-06-24
updated: 2026-06-24
tags: [token, pump-fun, solana, watch, kol-absent, prebond, hi-squatter-cohort]
status: watch
---

# $HI-21euJr (hi)

pump.fun 発。名称「hi」。mint `21euJrv...`。mcap $95k で gate 通過後、+70% の上昇で $162k 到達。bonding curve 未卒業（complete:false）。同名 ticker "$HI" が同サイクルで複数 mint 並立——うち 3件は $84〜$146 mcap で即死確認済み（$HI squatter コホート）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|------|-----|
| Sym | HI |
| Mint | `21euJrvmZDG5Y5VeDNvTJL8GVxNrdbgysa2tW8iMpump` |
| Pool | `D4RgUfkuvVEM9BKKhb7aGRpZRdJcdrsmVxVUGqamrcUD` |
| Gate | safety:ok / traction:mcap>=30000 |
| MCap 検知時 | ~$95,465 |
| MCap peak観測 | ~$161,872（+70%・2026-06-24T11:24Z） |
| Status | watch（prebond / complete:false） |
| Reply | 0 |
| Twitter | — |
| Website | — |
| tokenized_agent | false |
| 検知日時 | 2026-06-24T11:24Z |

<!-- synthesis:start -->
## 合成

**観測**: 検知時 $95k → 70%上昇で $162k。bonding curve 上（complete:false）。reply 0・KOL ゼロ・twitter/web なし。「hi」という極めて generic な名称——同名別 mint が同サイクルで複数生成されており、うち 3件が $84〜$146 mcap で即死（squatter コホート）。kol_ca/kol_ticker 空。

**判断**: traction シグナルゼロのまま prebond 上で mcap +70%。同名コホートの squatter 3件が即死している中での異質な価格動作——insider/whale の集中買いか、偶発的な出来高集中か。bonding curve 卒業まで到達するかが最初の判定点。KOL/reply が伴わずに graduation しても「graduated-but-empty」パスが既定路線（[[launchpad-economics]]）。

⚠️ $HI ticker は同サイクルで squatter 量産が確認されており、「名前の信頼性ゼロ」コホート。本 mint は他より高い mcap を示しているが、理由の外部シグナルなし。

**概念接続**: [[launchpad-economics]]（prebond 勢い門通過・squatter コホート）/ [[rug-anatomy]]（traction0 赤旗）
<!-- synthesis:end -->
