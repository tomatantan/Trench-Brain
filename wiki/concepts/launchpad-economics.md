---
type: concept
title: 型 — launchpad 経済圏（Pump.fun / $PUMP＝memeの供給工場）
created: 2026-06-22
updated: 2026-06-22
tags: [trench, concept, pattern, launchpad, pumpfun, supply, solana]
memetic_potential: 中
confidence: 中〜高
---

# 型: launchpad 経済圏（memeはどこで生まれるか＝供給側）

trench の **供給源/工場**を扱う concept。ナラティブ（需要側）の手前に、memeを物理的に生む
**launchpad** がある。worklist で [[$PUMP]]・[[@a1lon9]]・[[@PumpfunEco]] が浮上したことから合成。
他の concept（[[jp-meme-cluster]] / [[external-event-to-token-pattern]] の meme側）が扱う個々のトークンは、
**すべてこの launchpad 層から発射されている**＝供給の構造を押さえると個別ナラティブの見え方が変わる。

## Pump.fun の動線（工場→自己トークン化→価値捕捉）
```
誰でも token を bonding curve で発射（"anyone can be early" を商品化）
   → 一部が graduate して DEX に流動性（大半は死ぬ＝下記⚠️）
   → launchpad 自身を $PUMP でトークン化（$600M public sale が12分で完売）
   → revenue を buyback/burn に回し $PUMP に価値を還流
```
- [[@a1lon9]]（Pump.fun共同創業）「pump fun invented a completely new way to launch tokens」([[a1lon9__1942948097237172509]])、
  「selling out the $600m public sale in 12 minutes, pump fun is inevitable」([[a1lon9__1944140985539473557]])。
- 価値捕捉: 「100% of revenue went into buybacks. ~36% of circulating supply removed, forever」([[a1lon9__2049233387328565548]])。
  プレマーケットは [[@defi_kay_]]「PUMP priced at $5B, 25% above ICO」→「$6.5B (63% premium), 24h vol over $600M」([[defi_kay___1944358396288712778]])。
- 思想: 「the reason pump fun is controversial is that it allows anyone to be early, something that used to be reserved for the few」
  ＝**早期参加の民主化**を旗印に。理想形として a1lon9 は「fartcoin never had a centralized team, never relied on KOLs—just a ticker & lore」([[a1lon9__1952866820748144795]]) を掲げる。

## ⚠️ 致命的事実：量産される大半は死ぬ（供給過剰）
- **graduation率は低い**: [[@defi_kay_]]「pump fun launched 41k tokens with 1.5% graduation rate (vs Raydium 2.4%)」([[defi_kay___1913218855750476000]])
  ＝発射された**98.5%は graduate できず消える**。「launch数が多い＝健全」ではない。
- 活況の体温計: 「daily # of graduated tokens down ~80% from Trump top」＝trench全体の熱量の減衰指標。
- これは [[majors-rotation-supercycle]] の [[@thedefiedge]]「トークン供給の希釈で alt season が効かない」の**供給側メカニズム**＝launchpad が希釈の蛇口。
- rug の温床: [[@a1lon9]] 自身「disgusted by events surrounding $LIBRA. People made personal gains at expense of users」([[a1lon9__1891593196439790005]])。
  openness は bad actor も呼ぶ＝[[onchain-verification]]（[[@lookonchain]] が $LIBRA の $107M exit を追跡）と直結。

## auto-track 実観測コホート（`brain/track.py` の死の分母）
外部主張だけでなく、自前の観測でも同じ型が出る。base rate（2026-06-23 時点・累計）= **mints 観測 900 / 門通過 11（1.2%）/ graduated 6 / 死 0**。
- **「graduated but empty」型が観測の主流**: 通過銘柄の大半が *graduation 済みなのに reply 0・KOL 言及ゼロ*。出来高だけ先行し社会的 traction が伴わない。
  実例コホート（同一バッチ）: [[$MOONLAKE]]（AI・$274k）/ [[$MOTION]]（$187k）/ [[$VCSOL]]（GTA参照・$119k）/ [[$AEGIS]]（privacy・$27k）/ 既出 [[$RO]] / [[$AXIOS]]。
- **追跡で型が裏付く**: [[$AXIOS]] は graduation 直後 $53k→**-52%** で fading。「KOL pickup なし＝短命」仮説が観測で確証されつつある＝98.5%死亡母集団の動態をリアルタイムで捉えている。
- **prebond 観測（未 graduation・勢い門 mcap で通過）**: [[$MEW2]]（Pokemon IP・$47k）/ [[$GOOSE]]（animal・$90k）＝bonding curve 上で出来高だけ立った初期銘柄。graduation か死かを watch＝分母の入口側。
- **含意**: graduation は生存の十分条件ではない。**graduation × (reply/KOL traction)** が [[survivor-memes]] の足切り。traction を欠く graduate は死の分母に算入する前提で見る（これが生存者バイアス対策の実装）。

## auto-track 跳躍台帳（大きく跳ねた型を貯めて学習する）
死(→[[rug-anatomy]] 死亡台帳)と対。`brain/track.py` が **BREAKOUT(mcap前回比+100%超) / GRADUATED** を検知する度、
`brain/synthesize.sh` の合成が**跳躍シグネチャを1行追記**する。「跳ねる前に何が見えていたか」の共通項を貯める学習台帳。

| ticker | 跳躍 | mcap 前→後 | traction(reply/KOL) | 前兆/きっかけ | 型/signature |
|---|---|---|---|---|---|
| [[$RO]] | +138% | $5.8k→$13.8k | reply0 / KOL0 | ⚠️ twitterがElon tweetリンク(association marketing偽装) | **traction無し×出来高driven**＝持続性疑問 |
| [[$AEGIS]] | +160% | $29k→$76k | reply0 / KOL0 | 不明(privacyテーマ便乗 or bot買い) | traction0で急騰＝⚠️[[rug-anatomy]] のつり上げ候補 |
| [[$PHONEBLACK]] | +138% | $89.8k→$214.3k | reply0 / KOL0 | 不明(phone-01black.com整備済だが言及ゼロ) | traction0×出来高先行＝$AEGIS/$RO と同型・whale/bot pump疑い |
<!-- breakout-ledger: 以降 synthesize.sh が追記。古い順に貯める。 -->

**現時点で浮いている型（判断）**: 観測中の跳躍はほぼ **traction(reply/KOL)ゼロ × mcap先行**＝「whale仕込み or pump初動」の両義。
**KOL/reply を伴う跳躍**（=本物の社会的需要）と **traction無しの出来高跳躍**（=操作/bot疑い）を分けて貯めれば、
「[[survivor-memes]] に化ける跳躍」と「rug前のつり上げ」を**事前に弁別**する型が立つ見込み。現状サンプルは後者寄り。

## 競争（launchpad wars）
- Pump.fun（$PUMP）vs **BonkFun**（[[$BONK]] eco、[[@theunipcs]] が straddle: 「$PUMP TGE and what it means for $BONK and BonkFun eco」）
  vs Moonshot / Axiom / Raydium LaunchLab / Zora。Pump.fun が「40%+ of bonding curve volume originating on-platform」([[defi_kay___1932801391694692718]]) で支配的。
- ⚠️ 懐疑: [[@cobie]]「They're not making new commodities on pumpfun every few seconds」＝皮肉な距離感。a1lon9 は「streaming is not sustainable」批判に防御的反論([[a1lon9__1967316708835872941]])＝外部の持続性懸念が存在。

## 示唆 / 賭けの仮説
- **$PUMP は trench の"インデックス"**: 個別memeでなく launchpad に張る＝trench全体のβ＋buyback需給。trench が回れば手数料が増え buyback が効く。
- **供給の体温計を最上位指標に**: launch数・graduation率・graduated tokensの日次推移＝ナラティブより先に「trench全体が熱いか冷えてるか」を示す。個別meme判断の前にここを見る。
- **個別memeは"工場の出荷"の一つ**: [[jp-meme-cluster]] も [[external-event-to-token-pattern]] の meme側も、ここから出荷された在庫。98.5%が死ぬ母集団からの生存を見ているという前提を忘れない（→[[survivor-memes]]）。
- 監視: [[@a1lon9]] の buyback/burn 実績、graduation率、BonkFun との市場シェア争い。

## 関連
- [[reflexivity]]（**根本エンジン**＝98.5%死は reflexive bust が常態・graduation×traction はループ燃料の有無）/ [[survivor-memes]]（工場から生き残った稀な graduate）/ [[majors-rotation-supercycle]]（供給希釈）/ [[onchain-verification]]（$LIBRA rug）
- [[$PUMP]] / [[$BONK]] / [[@a1lon9]] / [[@theunipcs]] / 集計の入口: [[signal|Signal digest]]

## 出典(生ソース)
[[@a1lon9]] $PUMP発射/buyback/$LIBRA disgust/fartcoin理想, [[@defi_kay_]] 評価額・graduation率・出来高,
[[@theunipcs]] $PUMP↔$BONK/BonkFun, [[@cobie]] 皮肉。（全て sources/x/ の原ツイに保存済）
