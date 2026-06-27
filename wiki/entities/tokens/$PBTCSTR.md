---
type: entity
kind: token
source: auto-track
status: dead
ticker: $PBTCSTR
mint: 58fGUikmrBkzPm4ez2RQwvvJWLQDhw4HoSm4Rr2Zpump
created: 2026-06-26
updated: 2026-06-26 (第118窓・DEAD確定)
tags: [token, pumpfun, traction0, btc-meme, association-marketing, satire, dead, job-type]
---

# $PBTCSTR — Ponzi BTC Strategy（58fGUik）

pump.fun 発。bonding curve 卒業済（complete=true）。"Ponzi BTC Strategy" は MicroStrategy/Bitcoin Treasury Strategy の satirical 命名。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 58fGUikmrBkzPm4ez2RQwvvJWLQDhw4HoSm4Rr2Zpump |
| name | Ponzi BTC Strategy |
| 初検知 mcap | $104,468（第114窓推定） / live $98,730 |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| twitter | https://x.com/Cointelegraph/status/2070150150337470952（Cointelegraph公式ツイートへのリンク） |
| website | https://www.youtube.com/watch?v=ml8d1GkegO4（YouTubeリンク・非トークンサイト） |
| tokenized_agent | false |
| pool_address | GMs8URj2y4AoKcSTMRKoFHLWLicrmnALKaB6M9iQ5tNW |

## 追跡ログ

| 窓 | live mcap | 変化（検知時比） | 窓間変化 | 備考 |
|----|-----------|----------------|---------|------|
| 第114窓 | $98,730 | -5.5% | — | 初登場。ほぼ横ばい。T3ゼロ・reply:0。 |
| 第115窓 | **$164,957** | **+57.9%** | +$66,227（+67.1%）| **2窓目。前窓横ばいから急転換。T3ゼロ・reply:0 継続。price discovery 発動の可能性。** |
| 第116窓 | **$128,885** | **+23.4%** | -$36,072（-21.9%・前窓サージから反落） | 3窓目。前窓+67.1%窓間から反落。T3ゼロ・reply:0 継続。 |
| 第117窓 | **$113,792** | **+8.9%** | -$15,093（-11.7%窓間・2窓連続下落） | **4窓目。2窓連続下落継続。検知時比+8.9%まで縮小。T3ゼロ・reply:0 継続。** |
| 第118窓 | **$1,761** | **-98.3%（DEAD確定）** | -$112,031（-98.5%窓間・崩壊） | **5窓目・DEAD確定。JOB型崩壊完全踏襲。前窓「次窓崩壊」予告的中。T3ゼロ・reply:0。** |

<!-- synthesis:start -->
## 合成（確定・DEAD）

**観測（事実）**:
- pump.fun bonding curve 卒業済。第114窓 $98,730（-5.5%）→第115窓 $164,957（+67.1%・天井）→第116窓 $128,885（-21.9%窓間）→第117窓 $113,792（-11.7%窓間）→**第118窓 $1,761（-98.5%窓間・DEAD確定）**。
- 検知時比: -5.5% → +57.9% → +23.4% → +8.9% → **-98.3%（崩壊）**。
- T3 signal ゼロ 全5窓・reply:0 全期間。
- 命名: "Ponzi BTC Strategy"（satirical）・Cointelegraph association marketing。

**判断（確定）**:
- JOB 型（横ばい→急騰→反落→崩壊）の完全踏襲が確定。
- 第117窓「次窓でフラット以下なら崩壊直前」「JOB型崩壊フェーズ入り」の予測が第118窓で的中。
- satirical 命名 × association marketing × T3ゼロ全期間 → deployer exit 構造の事後確認。「Cointelegraphツイートをwebsiteに貼る」手口はナラティブを借用しながら organic 流入を生まない典型。
- 天井 $164,957（第115窓・検知時比+57.9%）から5窓目崩壊——JOB 原型より1窓多め（JOB本体は2窓目stale→5窓目DEAD）。

**パターン寄与**: JOB型 N=2（JOB本体 + PBTCSTR）。「横ばい/下落スタート→1窓急騰→反落→崩壊」の動線が2例で成立。[[rug-anatomy]] [[external-event-to-token-pattern]]

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty 候補動線）
- [[rug-anatomy]]（association marketing × traction0 パターン）
- [[external-event-to-token-pattern]]（BTC Treasury / MicroStrategy narrative 便乗）
- [[launch-pulse]]（第114窓 traction 候補・初窓）
