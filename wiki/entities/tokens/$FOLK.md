---
type: entity
kind: token
source: auto-track
title: $FOLK (Folk)
mint: 6zoA5hxRXAYpbe1wPv8KWUuUjHm7dcYrtuxVkTqBcv8S
status: dead
outcome: died
created: 2026-06-26
updated: 2026-06-26 (17:38Z・DEAD・$4.6k・-93.4%・graduated-but-empty確定)
tags: [token, pumpfun, graduated, traction0, dev-theme, dead]
---

# $FOLK (Folk) — 6zoA5h

pump.fun 発。bonding curve 卒業済（complete=true）。twitter は @arlanr のツイート、website は GitHub プロフィール（arlanrakh）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 6zoA5hxRXAYpbe1wPv8KWUuUjHm7dcYrtuxVkTqBcv8S |
| name | Folk |
| mcap (初観測) | $69,861 |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| kol_ticker | なし |
| twitter | https://x.com/arlanr/status/2070268760041410789 |
| website | https://github.com/arlanrakh |
| complete | true（graduated） |
| pool | 96iWaW1e1dwMYCNiGTYh7Trv81Swa356TyrpWKtn6i4Y |
| real_sol | 0 |
| tokenized_agent | false |
| 検知日時 | 2026-06-25T22:19Z |

## 追跡ログ

| 観測 | live mcap | 備考 |
|---|---|---|
| 初検知(22:19Z) | $69,861 | gate 通過。reply:0・KOLゼロ。githubリンク。 |
| 23:36Z | **$21,672** | **-49%**（prev $42,231）。reply 0・KOL ゼロ継続。下落中。 |
| 09:41Z | **$28,560** | **+32%**（$21k底からbounce・ただし検知時$69k比-59%）。reply 0・KOL ゼロ継続。 |
| DEAD(17:38Z) | **$4,586** | **-83.9%**（prev $28,560）・peak比 **-93.4%** | mcap枯れ確定。死亡台帳算入。 |

<!-- synthesis:start -->
## 合成メモ

**観測（事実）**:
- mcap $69,861（初検知）→ $21,672（23:36Z低値）→ $28,560（09:41Z bounce）
- reply 0・KOL CA 言及なし全期間
- twitter に @arlanr のツイートをセット（一次ソース未確認）
- website が GitHub プロフィール（arlanrakh）= 個人 dev ページ
- real_sol 0・tokenized_agent false

**判断（09:41Z更新）**:
- $21k底から$28k (+32%) bounce は dead cat bounce 候補。検知時$69k比-59%の水準であり、構造的下落継続中の一時的反発と見る。
- ⚠️ @arlanr が実際にこのトークンを言及しているか未確認。sources/x に関連ツイートなし。
- reply 0・KOL ゼロ継続。T3 なし全期間。→ graduated-but-empty の縮退死動線。
- real_sol 0 = deployer の出口 SOL なし。bounce の継続性根拠薄い。

**賭け仮説**: T3 シグナルなしの間は自然死確率高。$28k→$40k+維持できなければ次窓で死亡台帳候補。

**17:38Z DEAD確定**: $28,560→$4,586（-83.9%窓間・peak比-93.4%）。
- @arlanr GitHub リンク × traction0 → graduated-but-empty 型死亡確定。
- dev 個人プロジェクトリンクが crypto traction を呼べなかった典型（$CLO/$JONAH と同型：authority/個人リンク型）。
- peak $69.9k → last $4.6k = 死亡コホート算入。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty 動線）
- [[rug-anatomy]]（traction0 → 死パターン）
