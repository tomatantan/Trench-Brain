---
type: concept
title: SpaceX IPO 動線 — 外部イベントが meme と tokenized stock を生む
created: 2026-06-22
updated: 2026-06-23
tags: [trench, concept, narrative, causal-chain, external-factor, solana]
memetic_potential: 高
confidence: 中〜高
---

# SpaceX IPO 動線（発端→金になるまで）

2026年6月の **SpaceX IPO**(数年来で最も注目の上場)が発端となり、crypto trench に
2系統の派生を生んだ典型的な「外部イベント→meme化→金」動線。[[signal|Signal digest]] で
$SPCX(14)・$ASTEROID(17) が同時上位に来たことから合成。

## 動線（causal chain）
```
SpaceX IPO（外部/TradFiイベント）
   ├─▶ [[$SPCX]]  … SpaceX株エクスポージャー＝合成perp(非RWA)＋tokenized spot株(RWA)の2経路(24/7・レバ・ショート可)
   └─▶ [[$ASTEROID]]    … IPOステージに登場したマスコットの memecoin 化
        → 両者が相互参照しながら投機フィーバー（先物・OI・派生ローンチ）
```
**発端は完全に外部(crypto外の上場イベント)**。これは「trenchの境界を閉じない＝発端は外部にある」
という本wikiの中核仮説の実例。単一ソースでは "$SPCXが伸びてる"
"$ASTEROIDが面白い" としか見えないが、横断すると**同じ発端から二股に分岐した1本の動線**だと分かる。

## 2系統の対比
| | [[$SPCX]] | [[$ASTEROID]] |
|---|---|---|
| 正体 | **傘ティッカー**: 合成perp/先物(株の裏付けなし=**非RWA**)＋tokenized spot株(**RWA**, Backpack/sunrisedefi/cryptocom発)。詳細[[$SPCX]] | SpaceXマスコット発の純memecoin |
| 駆動 | perp側=OI/funding/取引所(Hyperliquid/Binance/MEXC・出来高の主流)／spot側=機関フロー・real-share backing(未検証) | コミュニティ・物語(「IPOステージに実在した」) |
| 主な論者 | [[@thedefiedge]] [[@DefiIgnas]] [[@CryptoHayes]] [[@MEXC]] [[@nansen_ai]] [[$BP]] | [[@solbrdl]](Asteroid maxxing) [[@MascotAsteroid]] |
| リスク | perp=funding/清算/オラクル ／ spot=ペッグ/裏付け未検証/カストディ・lockup解除の売り圧 | 物語が剥がれると無価値・rug型 |

## プレイヤー相関
- [[@solbrdl]] = $ASTEROID の旗振り。「SpaceX IPOステージに$ASTEROIDが実在」「URLに spacex-asteroid-mascot と入ってる」を根拠に蓄積を主張。100m mcap以下なら積み増し対象、と賭け仮説を明言。
- [[@thedefiedge]] / [[@DefiIgnas]] / [[@CryptoHayes]] = $SPCX をTradFi×onchainのクロスオーバーとして解説。DefiIgnasはOI内訳(Binance $312.8M / Hyperliquid $309.0M)を提示。
- [[@MEXC]] = $SPCX 先物の日次出来高800M USDTを宣伝＝取引所が煽りに参加(資金フローの兆候)。
- [[@AdimsSHOGUN]] が [[@DegenerateNews]] の「Solanaの tokenized $SPCX(by Backpack/sunrisedefi)が spot の24h出来高で157x」を拡散＝Solanaエコへの波及。

## 反例・⚠️矛盾
- [[@coinkeiba]]: 「月も火星も存在しない。SpaceXは陰謀論。ショート利確」= $SPCX を**ショート側**で見る逆張り。物語に乗らない層の存在。
- [[@0xFunX]]: 「初日に必ず破発(初値割れ)と言われたが、開盘150→高値176→終値161」= 弱気予想が外れたと反論。**強気/弱気が同一ティッカーで衝突**している＝まだ決着していない。
- [[@DefiIgnas]]: 「$SPCX も結局 crypto流の低float/高FDVローンチに終わる」/ [[@theunipcs]]: 「$2.6T評価は高すぎ?」= 強気フィーバーの中の冷静な懐疑。
- ⚠️ $ASTEROID の「IPOステージに実在/Elon示唆」は [[@solbrdl]] の主張ベース。一次裏取り未確認＝物語の真偽がそのまま価格リスク。
- ⚠️ $SPCX 周辺に [[$SPCXON]] [[$SPCXX]] [[$SPCS]] 等の類似ティッカー乱立＝便乗/詐称の温床。
- （各トークンの両論フル版は entity [[$SPCX]] / [[$ASTEROID]] の合成メモ参照）

## 時系列
- 6/09 [[@CryptoHayes]]: $SPCX IPO初値+17%、「AIの夢を保つに十分か?」
- 6/12 $SPCX 上場、OI急拡大・初値割れ予想を覆す
- 6/13–6/19 [[@solbrdl]] が $ASTEROID 蓄積論を連投(SpaceX IPO後のシナリオ2＝capitulation→20-30m→新ATH)
- 6/19–6/21 Solana の tokenized $SPCX が出来高157x、MEXC先物800M＝フィーバー加速

## 示唆 / 賭けの仮説
- **型**: 「crypto外のビッグイベント → ①RWA/tokenized で機関フロー ②マスコット/固有名で meme」の二股は再現性がある(W杯→[[$CLUTCH]]、elon→[[$ASTEROID]] 等)。**次の大型IPO/世界イベントで同じ二股を先回り**できる。
- **$ASTEROID**: 物語駆動。100m mcap以下での蓄積は[[@solbrdl]]の賭け。物語の一次裏取りが取れれば確度↑、剥がれれば即死。ハイβ。
- **$SPCX**: 物語より板(OI/出来高/取引所採用)で追うべき。ショート勢([[@coinkeiba]])もいるので一方向ではない。
- 監視ポイント: 次のtokenized-stock候補・SpaceXの実ニュース・$ASTEROIDの一次裏取り。

### 2026-06-23 更新: Backpack tokenized equities が $SPCX → $MU へ拡張
- **観測**: [[@solana]] 公式（2026-06-22）: 「$MU (@MicronTech) via @SunriseDeFi, issued by @Backpack Securities」([[solana__2069058195038032064]] 400♥)。$SPCX に続き Micron（半導体/AI インフラ）の tokenized stock を Solana 上で発行。
- **示唆（判断）**: Backpack Securities + SunriseDeFi は**単発の SpaceX 案件ではなく、tokenized equity ライン（複数銘柄）を構築している**。$SPCX → $MU = 2 銘柄目。この動線は「SpaceX IPO 動線」から「**Backpack tokenized equities プラットフォーム化**」へと拡張しつつある。
- **概念の像の変化**: "SpaceX IPO" はあくまで最初の発端。2 銘柄目が出た時点で、このページの本質は「外部イベント 1 件」から「**tokenized equity インフラの多段展開**」に変わる。[[external-event-to-token-pattern]] の実例が複数になった＝型の確度↑。
- **⚠️ 赤旗**: $MU の backing（実際の Micron 株式裏付け）は未検証（[[onchain-verification]]）。$SPCX も backing 未検証のまま。複数銘柄が出ることでリスクが希薄化されて見えるが、backing の確認は各銘柄で必要。
- **[[$BP]] との接続**: $BP（Backpack トークン）がこのインフラの株。tokenized equity が増えるほど $BP の moat（= "Nasdaq onchain"）が強化される構造。

## 出典(生ソース)
[[@solbrdl]]×$ASTEROID連投, [[@DefiIgnas]] OI内訳, [[@CryptoHayes]] IPO初値, [[@MEXC]] 先物出来高,
[[@coinkeiba]] ショート, [[@0xFunX]] 初値割れ反論, [[@AdimsSHOGUN]]/[[@DegenerateNews]] Solana 157x。
(全て sources/x/ の原ツイに保存済)
