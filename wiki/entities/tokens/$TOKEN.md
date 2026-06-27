---
type: entity
kind: token
title: $TOKEN (sTokens) — generic ticker / DeFi命名
mint: 5YpuodfzRtxVWu17qcLLmk4MhBd7bL7tj5zKYmwTpump
source: auto-track
status: dead
outcome: died
peak_mcap: 41382
created: 2026-06-25
updated: 2026-06-25 (final)
tags: [token, pumpfun, graduated, traction0, generic-name, defi]
---

# $TOKEN (sTokens) — 5Ypuod

pump.fun 発。bonding curve 卒業済（graduated）。website=stokens.fun / twitter=@sTokensfun。generic ticker だが「sTokens」は DeFi プロダクト名風の命名。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 5YpuodfzRtxVWu17qcLLmk4MhBd7bL7tj5zKYmwTpump |
| name | sTokens |
| mcap (初観測→直近) | $21,680 → **$7,182（-42%・2026-06-25T13:06Z）** |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| kol_ticker | なし |
| twitter | https://x.com/sTokensfun |
| website | https://stokens.fun/ |
| complete | true（graduated） |
| pool | HhDNcqnS5KSmmz7YtCfvZJ9YfHoMKdpPxFx9oh79cqEZ |
| real_sol | 0 |
| tokenized_agent | false |
| 検知日時 | 2026-06-25T10:06Z |

<!-- synthesis:start -->
## 合成メモ

**観測（事実）**:
- mcap $21k（低水準）・graduated・reply 0・KOL なし
- website/twitter は整備済（stokens.fun/@sTokensfun）

**判断**:
- mcap $21k は低位。social 基盤（twitter/website）はあるが traction ゼロ。
- generic ticker "TOKEN" は他の同名 mint との混同リスクあり。
- graduated-but-empty の最も軽いケース。low mcap × social整備済 × traction0 = [[launchpad-economics]] 死亡コホートの典型。

**賭け仮説**: signal 最小。KOL/reply なければ消滅確定候補。

**2026-06-25T10:50Z 更新（+60%・$41.4k）**:
- $25,877 → **$41,382（+60%）**。reply=0・KOL なし継続。
- mcap 上昇だが traction ゼロのまま。BREAKOUT 未満（+100%閾値未達）。graduated-but-empty の範囲内。

**2026-06-25T12:17Z 更新（-60%急落・$10.0k）**:
- $25,046 → **$10,003（-60%）**。前回更新の $41.4k から更に下落——2窓で上昇分を全消しし検知時比でも下回った。
- peak $41.4k 比で -75.8%。reply=0・KOL なし全期間継続。縮退加速中。
- traction ゼロのまま2窓連続下落——graduated-but-empty 型の死亡フェーズ入り候補。

**2026-06-25T13:06Z 更新（-42%・$7.2k）**:
- $12,352 → **$7,182（-42%）**。peak $41.4k 比で -82.6%。reply=0・KOL なし全期間継続。
- 3窓連続下落。縮退が加速しており dead 確定候補。-90% 到達で RETIRE 圏入り。

**2026-06-25T13:35Z 最終合成（死亡確定）**:
- last mcap **$4,934**（peak $41,382 比 **-88.1%**）。cause: mcap枯れ。
- $7.2k → $4.9k——縮退継続で枯れ確定。全期間 reply=0・KOL=0。
- **型の確定**: DeFi generic ticker（sTokens）× graduated × traction ゼロ × 複数窓連続下落→枯れ。$PASSINHO と同一サイクル・同型。[[launchpad-economics]] 「graduated-but-empty 縮退型」の典型。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（low-mcap graduated-but-empty 動線）
- [[rug-anatomy]]（traction0→死パターン）
