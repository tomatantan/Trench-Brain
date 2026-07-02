---
type: entity
kind: token
source: auto-track
status: watch
ticker: $TOM
mint: BWu8AcV5j9ksCBFcRYHoQLJU5StdLToYxegCpovRbonk
created: 2026-07-02
updated: 2026-07-02
tags: [token, pumpfun, prebond, kol, auto-track, watch, creator-token]
---

# $TOM（SolportTom）

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | `BWu8AcV5j9ksCBFcRYHoQLJU5StdLToYxegCpovRbonk` |
| name | SolportTom |
| mcap（観測時） | ~$156,510 |
| gate | safety:ok / traction:kol |
| kol_ca | badattrading_ |
| kol_ticker | badattrading_ |
| complete | false (prebond) |
| reply_count | 0 |
| real_sol | 0 |
| twitter | https://x.com/SolportTom/status/1916871460334850181 |
| website | null |
| pool | 3G1LvNY8jZf9BM3xrML4hTDtVDgGSzqpfqj87dRpTunb |
| tokenized_agent | false |
| created（on-chain） | 2026-07-01T20:37Z |

<!-- synthesis:start -->
## 合成メモ（synthesis）

**観測（事実）**
- "SolportTom" — @SolportTom という実在 Solana インフルエンサーの名を ticker 化したもの。twitter リンクは SolportTom 本人のツイート（status/1916871460334850181）を指す。
- kol_ca = badattrading_（CA を言及）/ kol_ticker = badattrading_。complete=false（prebond）。reply=0・real_sol=0。
- $156K mcap で prebond 継続中。

**判断**
- SolportTom 本人のツイートが twitter フィールドに設定されている——これが本人公認 token か、または deployer が本人ツイートを借用した association marketing かは要確認。本人が自分のトークンを deploy した場合は KOL 自己トークン化（=[[launchpad-economics]] の creator economy 型）。deployer が無断借用なら[[rug-anatomy]] association marketing 型。
- ⚠️ badattrading_ の CA 言及のみで独立需要の証拠なし。reply0 × real_sol0 × prebond = traction0誕生即死候補。
- prebond × $156K は bonding curve 途中での一時的 mcap。graduation 未達なら prebond 圏で消滅。
- 一次ソース（SolportTom の当該ツイート）を確認できれば本人公認 vs 無断借用の判定が可能——判定次第で[[survivor-memes]]か[[rug-anatomy]]かが分岐。

**概念接続**: [[launchpad-economics]]（creator token候補 / prebond $156K） / [[rug-anatomy]]（association marketing疑惑 / traction0）
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
