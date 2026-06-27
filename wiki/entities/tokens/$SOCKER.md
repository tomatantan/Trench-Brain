---
type: entity
kind: token
source: auto-track
status: watch
ticker: $SOCKER
mint: 22FoEF2zsmQ1nxt9PkqVsxsX2RwR5CbtPkdkqgWJpump
created: 2026-06-26
updated: 2026-06-26
tags: [token, pumpfun, prebond, traction0, association-marketing]
---

# $SOCKER — SOCKER（22FoEF2）

pump.fun 発。bonding curve 未卒業（complete=false）。名称「SOCKER」。twitter に @updatecultura のツイートリンク（association marketing・watchlist 外）。website なし。⚠️ real_sol フィールドに異常値（23,670,948 = lamports 換算で ~0.024 SOL と推定・データ精度要確認）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 22FoEF2zsmQ1nxt9PkqVsxsX2RwR5CbtPkdkqgWJpump |
| name | SOCKER |
| 初検知 mcap | $32,566（2026-06-26T02:31Z） |
| gate | safety:ok / traction:mcap>=30000 |
| reply_count | 0 |
| KOL（CA確認） | なし |
| twitter | https://x.com/@updatecultura/status/2070333186584846629（association marketing） |
| website | なし |
| tokenized_agent | false |
| real_sol | ⚠️ 23,670,948（データ異常・lamports 換算 ~0.024 SOL と思われる） |
| complete | false（bonding curve 未卒業） |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|---|-----------|------|------|
| 初検知(02:31Z) | $32,566 | — | prebond（未卒業）。reply:0・KOLゼロ。@updatecultura association marketing。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- bonding curve 未卒業（complete=false）。$32,566（初検知）。reply 0・KOL なし。website ゼロ。
- twitter フィールドに @updatecultura のツイートリンク——watchlist 外のアカウント。association marketing 手法（$CLO/$LION 型）。
- ⚠️ real_sol フィールド値が 23,670,948 と異常値。SOL 建てなら約$4.3B で不可能。lamports 建てと仮定すると ~0.024 SOL（実質ゼロ）。track.py データ精度問題の可能性。

**判断**:
- prebond × twitter association marketing（watchlist外）× traction0 = [[rug-anatomy]] prebond 消滅型候補（$EPSTEIN/$LEGACY 型）。
- real_sol 異常値は採用判断に使えない（データ信頼性低）。実質 real_sol 0 として扱う。
- social 基盤ゼロ（website なし・watchlist外 association marketing のみ）——graduated できないまま消滅する可能性が高い。

**概念接続**:
- [[launchpad-economics]]: prebond 監視（association marketing 型）
- [[rug-anatomy]]: prebond 消滅型候補

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（prebond・$33k・association marketing）
- [[rug-anatomy]]（prebond消滅型候補・watchlist外 association marketing）
