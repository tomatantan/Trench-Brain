---
type: entity
kind: token
title: $SNDK
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 7
accounts: 3
---

# $SNDK

> 自動生成(brain/build_entities.py)。言及 7件 / 3アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連 [[concepts]]。

## 言及アカウント
[[@DEG_2020]] [[@MEXC]] [[@solana]]

## 共起トークン
[[$MU]] [[$AMD]] [[$DRAM]] [[$INTC]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 351 | [[@solana]] | BREAKING: $SNDK from @Sandisk via @SunriseDeFi, issued by @Backpack Securities | [[solana__2069776880627310837]] |
| 61 | [[@DEG_2020]] | 恐怖強欲指数はSP500のモメンタム低下で極度の恐怖一歩手前 $MU と $SNDK -13%と暴落もSOXは月初から大きくプラス、今月は四半期末フロー意識 貴金属の下 | [[DEG_2020__2069556912782520704]] |
| 36 | [[@DEG_2020]] | $DRAM $MU $SNDK メモリ系時間外で5%近くのリバ 韓国指数Kospi連動っぽいねぇ | [[deg_2020__2069581256049017112]] |
| 27 | [[@DEG_2020]] | 持ってる $SNDK は爆上げで喜ばしいが本当にメモリしか上がらんな。 日本株もキオクシア1本にした方がいいぐらいだ。 | [[deg_2020__2070270192719184286]] |
| 20 | [[@MEXC]] | AI storage is driving one of the market's biggest moves.   In May: 📊 Stock Futures v | [[mexc__2069986438943559696]] |
| 16 | [[@DEG_2020]] | $MU +13% $SNDK +11% | [[deg_2020__2069880532205490619]] |
| 4 | [[@MEXC]] | The AI trade isn't over.  $MU. $SNDK. $INTC. SK Hynix.  Trade them with 0 fees. Shar | [[mexc__2070454526188863908]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-27 初回合成

#### 観測（事実）
- [[@solana]] 公式（2026-06-24, 351♥）: 「BREAKING: $SNDK from @Sandisk via @SunriseDeFi, issued by @Backpack Securities」([[solana__2069776880627310837]]) = SanDisk 株の **tokenized stock を Solana 上で発行**。[[$SPCX]] → [[$MU]] に続く Backpack/SunriseDeFi tokenized-equity ラインの新銘柄。
- [[@MEXC]]: 「AI storage is driving one of the market's biggest moves。May: Stock Futures volume +105% MoM / $MU +1,002% / $SNDK +757% / $AMD +465%」(20♥, [[mexc__2069986438943559696]]) / 「The AI trade isn't over. $MU. $SNDK. $INTC. SK Hynix. Trade them with 0 fees. Share $1,000,000 in rewards」(4♥, [[mexc__2070454526188863908]]) = MEXC は SNDK を **stock futures（合成/デリバ）** として 0 手数料・賞金プロモ。
- [[@DEG_2020]]（日本株/メモリ系トレーダー）: 「$DRAM $MU $SNDK メモリ系時間外で5%近くのリバ、Kospi連動っぽい」([[deg_2020__2069581256049017112]]) / 「$MU +13% $SNDK +11%」 / 「持ってる $SNDK は爆上げ…本当にメモリしか上がらん、日本株もキオクシア1本にした方がいい」([[deg_2020__2070270192719184286]]) = **実 NASDAQ 株として時間外で売買**している文脈（Kioxia / SK Hynix / Kospi 連動）。

#### 判断（推論）— ⚠️ instrument の峻別が肝（装い≠実体）
SNDK は **3つの別物が同じティッカーに重なる**:
1. **実株（NASDAQ: SNDK = SanDisk）** — [[@DEG_2020]] が時間外で売買。AI/メモリ半導体 supercycle の一角（$MU / SK Hynix / Kioxia / $INTC / $DRAM と連動・Kospi 連動）。**これが価格の母体**。
2. **tokenized spot 株（RWA claim）** — @SunriseDeFi 発行/@Backpack Securities、Solana 上。[[$SPCX]] [[$MU]] と同一インフラの 3 銘柄目。**⚠️ real-share backing は未検証**（SPCX/MU と同じくペッグ/裏付け/カストディがブラックボックス）。「issued by Backpack Securities」は**主張**＝実株保管の独立検証なし。
3. **stock futures / 合成 perp** — [[@MEXC]] の 0 手数料商品。株の裏付けを持たないデリバ。funding/清算/オラクルリスク。

→ trench edge は「meme の物語」ではなく **①AI-storage/メモリ supercycle という実セクターのモメンタム ＋ ②それを onchain/perp で賭けられる新レール（Backpack tokenized equity / MEXC futures）の重なり**。$SNDK 単独でなく **$MU $DRAM $INTC SK Hynix Kioxia のバスケット**で動く（DEG_2020「メモリしか上がらん」）。SPCX のような meme フィーバー/lore ではなく、株式メカニクスとセクターローテで測る。

#### ⚠️ 赤旗
- tokenized 版の backing 未検証（=[[onchain-verification]] / [[$SPCX]] と同じ懸念）。
- [[@MEXC]] の「0 fees」「$1M rewards」は取引所の出来高誘導プロモ＝**独立 signal ではない**。
- @solana の "BREAKING" 演出は RWA ローンチを大事件に見せるが、中身は Backpack tokenized-equity ラインの定型展開（SPCX→MU→SNDK）。別 issuer だが Solana の tokenized-RWA 隣接トレンドに [[$PAXG]]（@Paxos の tokenized gold）。

#### concept 接続
[[spacex-ipo-narrative]]（Backpack/SunriseDeFi tokenized-equity インフラの多段展開＝SPCX→MU→SNDK） / [[external-event-to-token-pattern]]（AI-storage 需要という外部マクロ → onchain instrument） / [[perp-dex-wars]]（MEXC stock futures） / [[onchain-verification]]（backing 未検証 ⚠️） / [[$MU]] [[$SPCX]] [[$DRAM]] [[$INTC]] [[$PAXG]] / [[@solana]] [[@Backpack]] [[@SunriseDeFi]] [[@Sandisk]] [[@MEXC]] [[@DEG_2020]]

#### 賭け仮説
価格母体は**実メモリ supercycle**（機関/Kospi/時間外で動く）＝meme ではない。onchain edge は Backpack tokenized equity / MEXC futures という**レールの早期採用**だが、tokenized 版の backing 未検証ゆえロングは本物 CA/裏付け確認後に限る。セクター basket（$MU $SNDK $DRAM SK Hynix Kioxia）連動を追うのが筋。confidence=中（セクターは強いが tokenized instrument の実体未検証）。
<!-- synthesis:end -->
