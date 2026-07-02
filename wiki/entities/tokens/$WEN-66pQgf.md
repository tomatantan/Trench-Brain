---
type: entity
kind: token
source: auto-track
title: $WEN-66pQgf (Wendy's Co)
created: 2026-06-24
updated: 2026-06-25
tags: [token, pump-fun, solana, dead, kol-checked, wsb-meme, clean-structure, mcap-1m, outcome-died]
status: dead
---

# $WEN-66pQgf (Wendy's Co)

pump.fun 発。名称「Wendy's Co」——WSB（r/wallstreetbets）ミーム起源。mcap $728k。badattrading_ によるホルダー構成確認済みで構造上のクリーン判定。同名の別 mint（CuwbX6y...）が既存エンティティ [[ＷEN]] として別個に存在する。

## ライフサイクル(auto-track)

| 項目 | 値 |
|------|-----|
| Sym | WEN |
| Mint | `66pQgfLHEfbHSBgYSZSrKEdJHHaGiYbgCtNbz48Apump` |
| Pool | `HZyqZRuAUCLdJaHqBfnoFHVBwXmuH3Sm1LyXnWu8Ee15` |
| Gate | safety:ok / traction:kol (badattrading_) |
| MCap 検知時 | ~$728,221 |
| MCap 最新 | ~$599,775（**+62%**・prev $371,012→$599k・2026-06-24T23:00Z）、前peak ~$1.14M |
| Status | watch（graduated / complete:true） |
| Reply | 0 |
| Twitter | https://x.com/BurryJMichael/status/2069595279649558997（WSB 関連） |
| Website | https://www.reddit.com/r/wallstreetbets/comments/1udygxi/ |
| tokenized_agent | false |
| 検知日時 | 2026-06-24T11:24Z |

<!-- synthesis:start -->
## 合成

**観測（全期間）**:
- badattrading_ が mint を直接検証（[[badattrading___2069674616155410617]]）——「snipers/insiders なし、top 70 holders=56.9%（バランス良）、top 10=15.7%、holders 2,150 人・平均 bag $290、CEX funded 58.5%（Binance 20.9%・Coinbase 23.8%）、no major cluster on bubblemap」。ホルダー構成は同時期他銘柄（$PROV top70=84.9%、$EC43 top70=72.4%）と比較して分散度が高い。
- twitter は BurryJMichael の WSB ツイートを参照、reddit WSB スレッドにリンク——Wendy's 株の「救済」ミームを起源とする。
- 全期間を通じて reply 0・KOL ゼロ（traction 有機的発生なし）。
- peak mcap ~$1,144,820 → 最終 $110,750（-90% from peak）。

**判断（死亡確定 2026-06-25T23:13Z）**:
- 構造クリーン（badattrading_ 基準・top10=15.7%分散）でも、traction（reply/KOL有機的）が発生しないまま peak から -90% で死亡。
- WSB external-event meme（「Wendy's を救え」）は SOL meme に変換されたが、WSB コミュニティからの実際の流入はゼロ——narrative 強度がオンチェーン traction に繋がらなかった。
- ⚠️ BurryJMichael の WSB ツイートは token 推薦ではなく team が参照した既存コンテンツ。直接的 KOL 推薦と混同しない。
- **学習点**: 構造クリーン × KOL wallet-analysis attention × $1M超到達でも、有機的 traction ゼロなら最終崩壊——$SOB（top70=83.2% 集中崩壊）とは構造が異なるが「KOL wallet-analysis attention = 生存保証でない」という結論は同じ（N追加）。[[external-event-to-token-pattern]] の WSB/株式ネタ型で organic traction が発生しなかった事例。

**概念接続**: [[launchpad-economics]]（構造クリーン卒業→死亡）/ [[external-event-to-token-pattern]]（WSB/株式ミーム→SOL meme・traction未転換）/ [[rug-anatomy]]（KOL wallet-analysis attention ≠ 生存保証 N追加）

### 2026-07-02T09:27Z POST-MORTEM BOUNCE（+64%・$142,051→$233,080）
**観測（事実）**
- dead 確定後（2026-06-25 peak $1.14M→$110k -90%）に mcap $142k → $233k（+64%）が記録された。queue flags: mcap+64%。
- kol_ca: [] / reply=0 / twitter-website 変化なし。complete=true・pool 継続。
- kol_ticker に theunipcs が記録（queue birth列）——theunipcs が ticker を言及した可能性あり。

**判断**
- dead 判定後に $233k まで V字回復——典型的 dead-cat bounce。entity status は dead のまま（有機的 traction 復活の証拠なし）。
- WSB ミーム（「Wendy's を救え」）が再度話題になった or whale が floor 付近から再 pump した可能性。
- ⚠️ theunipcs の ticker 言及が真にこの CA を指すか未確認——kol_ca ゼロで CA 裏付け不在。言及≠推薦の注意事項は据え置き。
- dead-cat bounce として記録。次窓で $233k を維持できなければ再崩壊確定。
<!-- synthesis:end -->
