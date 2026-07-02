---
type: entity
kind: token
source: auto-track
status: suspicious
title: $PEPEBULL-52hneK（PEPEBULL / bundled scam）
mint: 52hneKeDvX3QMpysYXERquicq3QXxfVChqsEtYaLpump
pool: 3Yx9Q1FvhVXH4Vv8mLWWFDbLPZW4fXKgA3FAkbLQHVS6
created: 2026-07-02
updated: 2026-07-02
tags: [trench, entity, token, auto-track, suspicious, bundled-scam, pepebull, ticker-collision]
---

# $PEPEBULL-52hneK（PEPEBULL / bundled scam）

> ⚠️ ticker 衝突。既存 [[$PEPEBULL]]（mint: DVt8WDxWL...・2026-06-28）と別 deployer の同名 mint。mint 先頭6文字で区別。

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | `52hneKeDvX3QMpysYXERquicq3QXxfVChqsEtYaLpump` |
| name | PEPEBULL |
| gate | safety:ok / traction:kol |
| kol_ca | @badattrading_（⚠️ 警告ツイート） |
| kol_ticker | @badattrading_ |
| mcap(birth観測) | ~$108,017（2026-07-02T11:40Z） |
| reply_count | 0 |
| complete | true（bonding curve 卒業済） |
| real_sol | 0 |
| twitter | null |
| website | null |
| pool | 3Yx9Q1FvhVXH4Vv8mLWWFDbLPZW4fXKgA3FAkbLQHVS6 |
| status | suspicious（bundled scam） |
| auto-track birth | 2026-07-02T11:40Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-07-02 初回合成（auto-track birth）

**観測（事実）**  
一次ソース裏取り済（sources/x badattrading___2072575347795599852）:
> 「$PEPEBULL (CA 52hneKeDvX3QMpysYXERquicq3QXxfVChqsEtYaLpump) doesn't have insiders and snipers per devsnightmare. Team holds 17.6%. It's actually a bundled scam, don't buy, stay away.」（2026-07-02T06:57:24Z, likes:9, RT:1）

- badattrading_ が **明示的に「bundled scam」と警告**し CA を確認。
- complete=true（卒業済）。reply_count=0。twitter/website ともに null。mcap $108k。
- team holds 17.6%（高い team 保有）。snipers/insiders=0 だが bundled = 協調 wallet による人工買い。

**動線・型**  
- [[rug-anatomy]]: **bundled scam の典型**。bundles = 複数 wallet が協調して bonding curve を買い上げる手法。snipers/insiders=0（devsnightmare チェック）をクリアしながら、チームが協調 wallet 群（bundle）で価格を人工的に吊り上げる。
- 既存 [[$PEPEBULL]]（DVt8WDxWL...・別 deployer）に便乗した同名 launch である可能性も高い。人気 ticker の二番煎じ＋bundled scam の組み合わせ。
- **kol gate が「警告 KOL」として機能した事例**: badattrading_ の言及が avoid シグナルとして gate を通ったケース。gate は shill だけでなく警告でも反応する（情報の質は別途判断要）。

**⚠️ 評価**  
KOL 明示警告（「don't buy, stay away」）× bundled scam 確認 × team 17.6% 保有 × traction0 = 保有・参入はリスク最大。[[rug-anatomy]] 分類確定。

**賭け仮説**（confidence=該当なし）  
投資対象として検討しない（KOL 明示 avoid）。死の分母として観測継続、死亡台帳に登録予定。
<!-- synthesis:end -->

## 関連
- [[rug-anatomy]]
- [[launchpad-economics]]
- [[$PEPEBULL]]（既存・別 mint）
- [[@badattrading_]]
