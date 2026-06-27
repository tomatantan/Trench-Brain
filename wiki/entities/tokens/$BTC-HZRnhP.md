---
type: entity
kind: token
source: auto-track
status: dead
outcome: died
ticker: $BTC
mint: HZRnhPrEoddCir4thWEaSn1u6As3nxJ3QKB6rHPppump
created: 2026-06-26
updated: 2026-06-26 (death・mcap枯れ$1,589・peak$125,748比-98.7%・ticker詐称型確定)
tags: [token, pumpfun, graduated, traction0, ticker-impersonation, dead]
---

# $BTC — Buy The Cycle（HZRnhP）

pump.fun 発。ティッカー "BTC" に "Buy The Cycle" という名称——Bitcoin(BTC)のティッカーを意図的に流用した ticker 詐称型。twitter: @BuyTheCycle / website: buythecycle.fun 整備済。kol_ticker に CoinMarketCap/lookonchain/theunipcs が入っているが **kol_ca は空**（= これらのアカは「BTC」という文字を言及したが、この pump.fun ミントの CA を明示してはいない = Bitcoin 言及が大半）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | HZRnhPrEoddCir4thWEaSn1u6As3nxJ3QKB6rHPppump |
| Pool | 5bVBfqeBRyp6mk2xdyKcxsducMvUFxVygTVZwVceE9M6 |
| Gate | safety:ok / traction:graduated |
| MCap | $125,748 |
| reply_count | 0 |
| kol_ticker（ticker言及・CA未確認） | CoinMarketCap / lookonchain / theunipcs |
| kol_ca（CA明示・裏取り確認） | なし |
| Twitter | @BuyTheCycle |
| Website | buythecycle.fun |
| complete | true（graduated） |
| real_sol | 0 |
| tokenized_agent | false |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- peak mcap $125,748。last $1,589（peak比 -98.7%）。graduated（complete=true）、real_sol 0。reply:0。
- kol_ticker に CoinMarketCap/lookonchain/theunipcs——ただし kol_ca は空。Bitcoin(BTC)への言及がこの mint の CA を拾った誤検知。
- twitter @BuyTheCycle + website buythecycle.fun は整備済。

**判断（確定・死亡）**:
- ticker 詐称型 × real_sol 0 × traction0 → -98.7%崩壊。予測通り。
- "Buy The Cycle" ナラティブは Bitcoin 強気論との共鳴に失敗、crypto community へ伝播せず。
- kol_ticker ノイズ（Bitcoin 普通言及）が KOL support と誤認されるリスクを実証——kol_ca ゼロが本当の支持指標。
- 型: [[rug-anatomy]] graduated-but-empty × ticker 詐称型の合成死（$LEGACY/$VCSOL の IP/名称借用型と同根）。

**概念接続**: [[launchpad-economics]]（graduated・real_sol 0） / [[rug-anatomy]]（ticker 詐称 × traction0） / [[manipulation-playbook]]（ticker impersonation 手法）

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
- [[manipulation-playbook]]
