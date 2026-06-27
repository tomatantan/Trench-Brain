---
type: entity
kind: token
title: $USDT
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 11
accounts: 3
---

# $USDT

> 自動生成(brain/build_entities.py)。言及 11件 / 3アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連 [[concepts]]。

## 言及アカウント
[[@BinanceUS]] [[@MEXC]] [[@lookonchain]]

## 共起トークン
[[$USDC]] [[$ETH]] [[$USD1]] [[$WOJAK]] [[$SPACEX]] [[$SPCX]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 1,772 | [[@lookonchain]] | MrBeast (@MrBeast) just deposited 114,483 $USDT into #Aster.  @MrBeast profited over | [[lookonchain__1969565658204815822]] |
| 1,648 | [[@lookonchain]] | It seems that #Bybit spent 100M $USDT to buy 36,893 $ETH at $2,711 from Galaxy Digit | [[lookonchain__1893323016865751514]] |
| 1,363 | [[@lookonchain]] | Before the #SEC sued #Binance news reported, @FBGCapital withdrew 35M $USDT from #Bi | [[lookonchain__1665913473753288704]] |
| 494 | [[@MEXC]] | Got rewarded in the $SPACEX(PRE) 0-Fee Gala yet?   🎁 20 winners × 15 $USDT. To enter | [[MEXC__2069284313808646519]] |
| 388 | [[@MEXC]] | The game lasts 90 minutes. The fit lasts forever. ⚽♾️  Show us your ultimate match-d | [[MEXC__2069314511450919395]] |
| 339 | [[@BinanceUS]] | The @BinanceUS x @wojakcto BOOST event is live!  🇺🇸  Earn your share of ~$100K $WOJA | [[BinanceUS__2067638719750811781]] |
| 230 | [[@lookonchain]] | The MEV bot jaredfromsubway was exploited for $7.7M!  Including:  1,583.5 $ETH($2.75 | [[lookonchain__2068527251440963941]] |
| 230 | [[@BinanceUS]] | The Boost × @wojakcto event lands on @BinanceUS tomorrow, June 18 @ 12 p.m. EDT!  🎁  | [[BinanceUS__2067281907528925448]] |
| 215 | [[@MEXC]] | New look. Same infinite opportunities. ♾️  What do you think of MEXC's brand upgrade | [[mexc__2069692004196597941]] |
| 176 | [[@MEXC]] | 🚀 SpaceX fever is real.  $SPCX Futures daily trading volume on MEXC just topped 800M | [[MEXC__2067963107084046668]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 観測（事実）
- $USDC 同様、trench での登場は「大口フローの計量単位」が主。高エンゲージ言及上位4件がこのパターン。
- 機関フロー: Bybit が 100M $USDT → $ETH 購入（1,648♥）= 大口の ETH 仕込み証跡。
- MrBeast が 114,483 $USDT を Aster に入金してプロフィット（1,772♥）= インフルエンサー × DeFi という構図の証跡。
- 規制シグナル: SEC vs Binance 訴訟報道前に [[FBGCapital]] が 35M $USDT を Binance から引き出し（1,363♥）= **情報漏洩疑い**を示す on-chain 行動。
- MEV bot jaredfromsubway が $7.7M 搾取（$ETH 2.75M + $USDT 含む複数資産）（230♥）= $USDT が MEV ターゲットとしても使われている。
- MEXC: SPCX 先物の 1日出来高 800M $USDT（176♥）= [[spacex-ipo-narrative]] の volume 証跡。

### 判断（推論）
- $USDT の trench 内 役割は $USDC と重なるが、**規制摩擦の色が強い**。FBG / SEC 文脈・Binance 文脈で登場する = 規制リスクが高い取引所経由で流れるドルとして観測されている。
- [[regulation-catalyst]]: SEC の BUSD「unregistered security」認定と同じ文脈で FBG が引き出しを行った = 規制シグナルが大口の on-chain 行動を先行して動かす実例。「政策が地合いを決める」の具体ケース。
- ⚠️ $USDC vs $USDT: corpus 内で $USD1（Trump系）も共起 → stablecoin 三つ巴（Tether系 / Circle系 / 政治系）が形成されつつある。規制環境次第で地位が組み替わる。
- [[onchain-verification]]: lookonchain が FBG の引き出しタイミングを SEC 訴訟報道と照合して報告 = on-chain データが「情報優位」の検証装置として機能した事例。

### concept 接続
[[regulation-catalyst]]（FBG × SEC 情報漏洩疑い・BUSD認定） / [[onchain-verification]]（whale / 機関フロー追跡） / [[spacex-ipo-narrative]]（MEXC SPCX volume） / [[$USDC]] / [[$ETH]] / [[$SPCX]] / [[$WOJAK]] / [[@lookonchain]] / [[@BinanceUS]]
<!-- synthesis:end -->
