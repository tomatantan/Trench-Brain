---
type: entity
kind: token
source: auto-track
title: $FCKED (FCKED)
mint: HaqLMWXMABbAq4DDYhhMMxV9v5dfedofNGLRaSXVpump
status: dead
created: 2026-06-26
updated: 2026-06-26
tags: [token, pumpfun, graduated, traction0, expletive-meme]
---

# $FCKED (FCKED) — HaqLMW

pump.fun 発。bonding curve 卒業済（complete=true）。名前は expletive meme。twitter は @FunkyGuppy44 のツイート。website なし。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | HaqLMWXMABbAq4DDYhhMMxV9v5dfedofNGLRaSXVpump |
| name | FCKED |
| mcap (初観測) | $35,507 |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| kol_ticker | なし |
| twitter | https://x.com/FunkyGuppy44/status/2070276815688794314 |
| website | なし |
| complete | true（graduated） |
| pool | HmJ3tiMAQ7oCBJbwVCyRisMr4paRQXN4eJHcfXQ7LqAU |
| real_sol | 0 |
| tokenized_agent | false |
| 検知日時 | 2026-06-25T22:46Z |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|---|---|---|---|
| 初検知(22:46Z) | $35,507 | — | gate 通過。reply:0・KOLゼロ。 |
| auto(22:47Z) | $51,598 | +45% | 誕生直後の mcap 上昇。traction 変化なし。 |
| synth_queue(23:13Z) | **$12,582** | **-76%**（prev $51,598） | **大幅続落。reply 0・KOL ゼロ変わらず。** |
| 23:36Z | **$18,948** | **+51%**（prev $12,582） | **反発。reply 0・KOL ゼロ継続。dead cat bounce の可能性。** |
| 23:59Z | **$5,759** | **-70%**（prev $18,948） | **死亡確定。peak比-88.8%。traction0全期間。** |

<!-- synthesis:start -->
## 合成メモ

**観測（事実）**:
- mcap $35.5k→$51.6k（+45%・初動）→**$12.6k（-76%・続落）**
- graduated・reply 0・KOL CA なし（全期間）
- twitter に @FunkyGuppy44 のツイートをセット（非著名）・website なし・real_sol 0・tokenized_agent false

**判断（23:13Z 更新）**:
- 誕生直後+45%→続落-76% = BREAKOUT-then-dead 初動と一致。traction（reply/KOL）ゼロのまま mcap 崩壊進行中。
- social 基盤ゼロ（real_sol 0・website なし・非著名 twitter）= graduated-but-empty 型が進んでいる。
- $12.6k は死亡判定水準（tracking floor）に接近。次窓で消滅 or さらに縮退なら [[rug-anatomy]] 死亡台帳行き確実。
- ⚠️ 死亡前兆シグナル全点灯。traction 無し初動 +45% → -76% は traction0 × 出来高先行 BREAKOUT-then-dead の型通り。
- **23:59Z 死亡確定**: dead cat bounce +51%（$12.6k→$18.9k）の後、$5,759（peak比-88.8%）まで崩落。traction ゼロ全期間。
- 死因: mcap枯れ。初動+45%→-76%→dead cat bounce+51%→最終崩壊 = BREAKOUT-then-dead 型の教科書事例。
- outcome: died。[[rug-anatomy]] 死亡台帳 N=132 追加。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty / 初動 mcap 動き）
- [[rug-anatomy]]（traction0 → 死パターン）
