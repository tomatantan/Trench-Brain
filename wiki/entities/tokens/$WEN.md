---
type: entity
kind: token
title: $WEN
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 4
accounts: 3
---

# $WEN

> 自動生成(brain/build_entities.py)。言及 4件 / 3アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連する concept ページ。

## 言及アカウント
[[@PumpfunEco]] [[@badattrading_]] [[@itspyrored]]

## 共起トークン
[[$FARTCOIN]] [[$JOTCHUA]] [[$KINS]] [[$WORLD]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 62 | [[@PumpfunEco]] | Top traded pump fun coins by volume in the last 24 hours 👀  $Fartcoin $14.8M $WEN $6 | [[pumpfuneco__2070119982063870255]] |
| 26 | [[@itspyrored]] | Call me retarted but I blasted $Wen here | [[itspyrored__2069873540321386927]] |
| 22 | [[@badattrading_]] | $WEN (CA 66pQgfLHEfbHSBgYSZSrKEdJHHaGiYbgCtNbz48Apump) doesn't have snipers and insi | [[badattrading___2069674616155410617]] |
| 5 | [[@badattrading_]] | $WEN (CA 5xHMRXNcrsipK89EGPN8whB38DWCwLSmPdwG6TQ8pump) doesn't have snipers, insider | [[badattrading___2070041600630141011]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-27 初回合成
**観測（事実・2026-06-24〜25）**
- **出来高は本物（pump.fun 24h ボリューム #2）**: [[@PumpfunEco]]「直近24h の pump.fun 出来高 top: $Fartcoin $14.8M / **$WEN $6.30M** / $world $5.02M / $KINS $2.56M / $Jotchua $2.31M」（[[pumpfuneco__2070119982063870255]] 62♥・2026-06-25）。[[$FARTCOIN]] に次ぐ2位＝薄い meme ではなく、実際に板に資金が回っている。
- **⚠️ ティッカー衝突（最重要赤旗）**: 同じ "$WEN" で**別CAが複数走っている**。[[@badattrading_]] が2つの異なるCAを別々に分析:
  - **CA `66pQgf…pump`**: snipers/insiders なし（devsnightmare 判定）、bubblemap に大クラスタなし、CEX クラスタ 58.5%、top70=56.9% / top10=15.7%、2.15k holders・平均$290 ＝**比較的クリーン**（[[badattrading___2069674616155410617]] 22♥）。
  - **CA `5xHMRX…pump`**: insiders 2.8% / team 3.4%、複数クラスタ（4.2/3.7/2.8%）、CEX クラスタ 72.3%、**Bybit 資金 16.5%＝本人が red flag 明記**、top70=79.2% / top10=23%、540 holders・平均$260 ＝**集中度高く危険寄り**（[[badattrading___2070041600630141011]] 5♥）。
- **degen エントリーコール（低シグナル）**: [[@itspyrored]]「retarded と呼んでくれ、でも $Wen をここでブチ込んだ」（[[itspyrored__2069873540321386927]] 26♥）。論拠ゼロの感覚エントリー。
- CA はいずれも末尾 `pump`＝pump.fun bonding 由来の新規ローンチ（2024年の Jupiter 系オリジナル $WEN とは別物。原典が同一かは一次ソースから未確定）。

**動線・型**
- [[launchpad-economics]]: pump.fun 産で 24h $6.3M 出来高＝ローンチ→トレンド→出来高上位の典型動線に乗っている。
- [[rug-anatomy]]: **ティッカー衝突は混乱/誤購入の常套ベクトル**。複数CAが同名で走ると、プロモが指す "$WEN" がどのCAか曖昧化＝買い手が意図しないCAを掴むリスク。`5xHMRX` 側の top10=23%＋Bybit 16.5% は配布偏りの赤旗。
- [[onchain-verification]]: badattrading の holder forensics（devsnightmare 経由）が、出来高の華やかさの裏でCA間の質の差を可視化＝観測≠採用の好例。`66pQgf` と `5xHMRX` で安全性が逆。

**⚠️ 矛盾・赤旗**
- **どのCAが "本命" か未確定**: 出来高 $6.3M がどちらのCA（or 合算）か一次ソース不明。エンティティ別ファイル（[[$WEN-66pQgf]] / [[$WEN-5xHMRX]]）が分かれて存在＝システム上も衝突を認識。
- **シラー構成が薄い**: 独立 KOL の物語的支持は無く、PumpfunEco の出来高 feed（プラットフォーム自身）＋ badattrading の中立 forensics ＋ itspyrored の感覚コール。ナラティブの芯が無い＝出来高先行・物語後付け型。
- `5xHMRX` の集中＋Bybit 偏りは distribution 赤旗。

**賭け仮説（confidence=低）**
- 出来高は実在するが、ティッカー衝突＋物語不在＝「出来高は回るが誰のどのCAか」が不明瞭な投機回転。追うなら**CAを必ず固定**し、`66pQgf`（クリーン側）と `5xHMRX`（集中側）を混同しないことが前提。
- **監視トリガー**: 独立 KOL がCAを明示して物語付きで言及し始めるか／2つのCAのどちらに流動が集約するか。集約せず両建てのまま出来高が割れるなら confusion トラップとして避ける。
<!-- synthesis:end -->
