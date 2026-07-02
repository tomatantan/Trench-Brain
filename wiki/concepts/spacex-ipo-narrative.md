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
- 6/22 [[@CryptoHayes]] 「9月 unlock = low float high FDV shitcoin」/ [[@WatcherGuru]] -10.5% → -16%
- **6/23 [[@coingecko]]「$SPCX falls 17.8%, erasing all of its gains since its market debut」**([[coingecko__2069287524254482595]])。**IPO初日からの全騰幅消去**が確定。Hayes thesis が 9 月 unlock 前に部分実現。

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

### 2026-06-23 追記: Hayes 「SpaceX IPO = low float high FDV shitcoin」

出典: [[bankless-arthur-hayes-ai-crash-bitcoin-1m-2026-06-22]] / [[@CryptoHayes]] × [[@Bankless]] / 2026-06-22

**Hayes 評価（観測）**:
- 「SpaceX IPO は最初の2日は好調。だが**low float / high FDV のshitcoin**で、9月にunlockが来る。我々はそれがどうなるか知っている。」
- Anthropic + OpenAI の IPO も「高バリュエーションで控える」 = AI IPO パイプラインへの一括懸疑。

**既存との接続**:
- 既存: [[@0xFunX]]「初日150→高値176→終値161」= Hayes の skepticism に対して初値割れ不発で強気側が反論。
- 今回の Hayes 発言はそのあと（2日後 = 2026-06-22）= **「初値は良かったが long-term = shitcoin パターン」**への再フレーム。9月 unlock が Hayes thesis の検証ポイント。
- 「how those go when you start having unlocks」= trench での low float IPO の典型パターン（[[rug-anatomy]] の外部市場版）と重なる見方。

**⚠️ 含意**:
- Hayes が SpaceX IPO の AI bubble の「exit ベクター」と見ている = AI 資金が SpaceX/Anthropic/OpenAI の unlock 売り圧力に直面する 2026Q3〜Q4 のリスク意識。
- これは [[majors-rotation-supercycle]] の「AI が crypto の酸素を吸っている」に対する反転トリガー候補の一つ。

### 2026-06-19 追記: Hyperliquid が SpaceX IPO を「完璧に」プライシング（Bankless 確認）
出典: Bankless 週次ロールアップ / David Hoffman + Tom Schmidt / sources/youtube/UCAl9Ld79qaZxp9JzEOwd3aA__F8njppzDIxY.md

**観測**:
- Hoffman: 「HIP-3 の Trade XYZ が SpaceX IPO を160で priced → 取引終了時点でぴったり到達。今もなお SpaceX で 数百億円/日の volume」（2026-06-19）。
- Schmidt（VC 視点）: 「これは Cerebrus IPO が shot across the bow だった。Cerebrus の時に TradFi の trading floor で Hyperliquid を Hyperliquid（赤いバナー=管轄外で banned）の画面を参照しているスクリーンショットが出回った。Wall Street が実際に取引していたかどうかより、**価格発見ツールとして Hyperliquid が認識された**ことが重要」。
- 「SpaceX は今まで最大の IPO。これが game time だった。Hyperliquid は打ち出の小槌を当てた」。
- 次の大型 IPO: OpenAI・Anthropic = さらにスケールが大きいステージが来る。Hoffman: 「これは展開中のストーリー」。

**示唆（判断）**:
- Hyperliquid HIP-3 の価格発見機能は「crypto の TradFi に対する勝利」= crypto が先行情報発信源になったポリマーケット × 2024 選挙と同じ構図の再現。
- ⚠️ 赤旗: IPO pricing の正確さは「流動性と参加者の質」に依存。SpaceX が完璧だった = 次も完璧とは限らない（Hoffman 自身も「次で機能するか」を問い open）。
- 既存の Hayes 評価（「SpaceX = low float high FDV shitcoin / 9月 unlock が本当の試練」）と組み合わせると: **Hyperliquid は IPO を正確に priced したが、9月 unlock 後の下落も "正確に" 反映する可能性**。

## 出典(生ソース)
[[@solbrdl]]×$ASTEROID連投, [[@DefiIgnas]] OI内訳, [[@CryptoHayes]] IPO初値, [[@MEXC]] 先物出来高,
[[@coinkeiba]] ショート, [[@0xFunX]] 初値割れ反論, [[@AdimsSHOGUN]]/[[@DegenerateNews]] Solana 157x。
[[@CryptoHayes]] Bankless 対談 2026-06-22（SpaceX = low float high FDV shitcoin・9月 unlock リスク）。
[[@Bankless]] 週次ロールアップ 2026-06-19（HIP-3 SpaceX IPO 完璧プライシング / Cerebrus precedent / OpenAI・Anthropic 次ステージ）。
(全て sources/x/ / sources/youtube/ の原文に保存済)

### 2026-07-02 更新: Nasdaq-100 組み入れ（Jul 7）= 強制リバランス需要フェーズ
出典: [[mexc__2072243817516769510]]（101♥・2026-07-01）

**観測**: $SPCX が **2026-07-07（月）に Nasdaq-100 に正式組み入れ**予定。指数連動 ETF・インデックスファンドが自動的に $SPCX を組み入れる強制リバランス。MEXC が「Not all buying is driven by investors. Some follows an index.」と演出。

**時系列への追加** (既存の 6/23「全騰幅消去」以降):
- 2026-07-01: MEXC が Nasdaq-100 組み入れ（Jul 7）を告知
- 2026-07-02: DefiIgnas が「$SPCX can't even manage a disbelief rally」= 組み入れ前の底値圏で反発すら起きていないことを確認

**型への示唆**: 「外部イベント（IPO）→ フィーバー → 全騰幅消去（-17.8%）→ lockup 解除待ち」の途中に、**指数組み入れという第二の外部イベント**が挿入される。この「指数組み入れ前の駆け込み需要 → 後の売り（sell-the-news）」は TradFi では繰り返し観測されるパターン。crypto-stock クロスオーバーの [[$SPCX]] でも同パターンが出るか = **Jul 7 組み入れ後の price action が本 concept の「外部イベント→一時的買い→剥落」仮説の検証ポイント**。lockup 解除（2026-08〜）との二重の売り圧イベントが重なる 8 月が次の節目。
