---
type: concept
title: 型 — rugの解剖（繰り返す抽出メカニクスと赤旗チェックリスト）
created: 2026-06-23
updated: 2026-06-23
tags: [trench, concept, pattern, rug, scam, screening, risk]
memetic_potential: —
confidence: 中〜高
---

# 型: rugの解剖（人がrektされる繰り返しの構造）

trench で資金が抜かれる**再現メカニクス**を分類し、**赤旗チェックリスト**に落とす concept。
[[onchain-verification]] の「危険検出」側を体系化し、screening（出口/執行）に渡せる形にする。
worklist で [[$LIBRA]]・[[@lookonchain]]・[[@badattrading_]] が浮上したことから合成。

## 標準ケース: [[$LIBRA]]（Milei系）＝全部入り
1. **インサイダー事前知識**: [[@lookonchain]]「Someone knew in advance that $LIBRA was going to be launched but bought too late, losing 26,577 $SOL($5.34M). However, compensated with 5M $USDC」([[lookonchain__1891340262326346071]])＝**事前共有の証拠**（損失を補填される＝身内）。
2. **LP非対称で抽出**: 「$YZY も $LIBRA 同様、トークンのみをLPに入れ $USDC を入れない→dev が add/remove で売り抜け」([[lookonchain__1958355708010975580]])。
3. **集中キャッシュアウト**: 「$LIBRA team has cashed out $107M! 8 wallets が add/remove liquidity と fee claim で 57.6M $USDC＋249,671 $SOL を取得」([[lookonchain__1890619615883219455]])。
4. **wash で資金洗浄**: 「insider team is laundering... 19,846 $SOL で POPE(<$150K mcap)を買い $24K で売却、$2.73M を意図的損失で funnel」([[lookonchain__1894757929204813828]])。
- [[@a1lon9]]「I'm disgusted by $LIBRA... substantial personal gains at expense of users」＝launchpad運営者自身が rug 認定。

## 繰り返すメカニクス（型の分類）
| 型 | 中身 | 観測例 |
|---|---|---|
| **インサイダー/事前知識** | team・縁故walletがlaunch前に仕込み→pump後dump | $LIBRA / $MELANIA（"LeBron" $8.9M）/ $YZY / MrBeast |
| **LP非対称・低float** | stablecoin非ペアでdevが価格操作、低floatで薄い板を抜く | $LIBRA / $YZY |
| **sniper＋集中** | 上位70walletが供給の74-76%、sniperがlaunch割当を掴む | [[@badattrading_]] が多数tokenで観測 |
| **bundled/honeypot** | コントラクトがretailの売却を阻止、insider/sniperだけ保持 | $LOT / $Jetchua / $CATWIF / $SCF |
| **team dump** | team保有%大・lock短い→解禁で投げ | $SS（team 39.5%・6%だけ71日lock） |
| **influencer pump-dump** | 影響力で煽り→保有をdump | MrBeast（$23M / $SUPER・$ERN） |
| **whale操作** | 大口が清算を誘発して利益 | $JELLY（124.6M で HLP に $12M 損失を強制＝[[perp-dex-wars]] のHyperliquid攻撃） |
| **phishing/なりすまし** | 似アドレス生成で誤送金を誘発 | $WBTC $71M 盗難 |
| **team送金=売り圧偽装** | 「流動性供給」と称し取引所へ大量入金 | [[$TRUMP]] team $455M を Binance |

## ★赤旗チェックリスト（screeningに渡す）
[[@badattrading_]]（devsnightmare等の解析）が分離して見る指標＝そのまま赤旗:
- **sniper%**（9-10%超は注意）/ **insider%** / **top70集中度**（74-76%＝薄い実流動）
- **LPにstablecoinが対で入っているか**（無い＝dev抽出可）
- **team保有%とlock期間**（39.5%・短lock＝時限爆弾／3.4%・1年lock＝相対クリーン）
- **CEXクラスタ%**（高集中＝偏り）/ **bundledフラグ**（exit阻止＝即アウト）

## auto-track 死亡台帳（死の型を貯めて学習する）
`brain/track.py` が死(RETIRE: mcap枯れ or peak比-90%)を検知する度、`brain/synthesize.sh` の合成が
**死亡シグネチャを1行追記**する。観測の蓄積＝「死ぬ前に何が見えていたか」の共通項を浮かせる学習台帳
（観測＝表 / 型の言語化＝下の判断）。型通りの死は1行、番狂わせ(新しい死に方)はentityにフル。

| ticker | entry門 | peak mcap | traction(reply/KOL) | 生存 | cause | 型/signature |
|---|---|---|---|---|---|---|
| [[$KRILLION]] | 勢い門 | 低 | reply0 / KOL0 | 誕生即死(1cy) | mcap枯れ | **traction無しの即死**＝最頻型 |
<!-- death-ledger: 以降 synthesize.sh が追記。古い順に貯める。 -->

**現時点で浮いている型（⚠️仮説段階・N不足／lint 2026-06-23 で格下げ）**: ①**traction(reply/KOL)ゼロ × 出来高先行**で上げた銘柄は死にやすい**かもしれない**——ただし**確定死亡は [[$KRILLION]] の N=1 のみ**で `base_rate.json` の died=0。挙げている [[$AXIOS]](peak比-76%)・[[$TBHR]](-86%) は **fading＝進行中で dead ではない**（fading≠dead）。＝「死亡率が高い」と断定する分母が未だ揃っていない＝**仮説**。②graduated でも KOL ピックアップ無し＝「graduated but empty」候補（[[launchpad-economics]]）。→ 「traction の不在」を**死の先行指標候補**として観測継続（死亡台帳に確定死亡が貯まって初めて型として確立）。それまで前段フィルタに使うなら確度は低く見積もる。

## ⚠️ 境界の論争（何をrugと呼ぶか）
- **インサイダー≠rug?**: 「割当を持つteamが利確しただけ」論 ⇄ [[@a1lon9]] は**害(at expense of users)**で rug 認定。$LIBRA の POPE wash は「意図的抽出」の証拠＝単なる利確と一線。
- **sniper≠rug（MEV）?**: [[@badattrading_]] は sniper(正常だが集中リスク) と bundled(無条件アウト) を**別の赤旗**として区別＝程度問題。
- **lock付きteam保有はOK?**: lock期間と%で判定（[[$LIBRA]]型の即抜き vs 1年lock）。
- ⚠️ corpus に rug を擁護する声は無い＝debateは「擁護」でなく**screening基準の精緻化**として現れる。

## 示唆 / 賭けの仮説
- **これは"地図"でなく"防具"＝実用edge寄り**: 上記チェックリストは買う前の即時スクリーニングに使える＝[[onchain-verification]] を行動に落とす。screening（出口/執行）セクションの中核入力。
- **rugは型が有限＝自動検出可**: sniper%/insider%/LP-pair/lock/集中度は機械で取れる＝[[@badattrading_]] 的解析を自動化すれば**門の一部（指針2のtraction門に"安全門"を追加）**になる。
- **"事前知識"は最強の危険信号**: launch前の仕込み・補填walletが見えたら近づかない（$LIBRA）。
- 監視: 新規launchの sniper/insider/LP構成、team wallet の取引所入金、whaleの清算誘発（perp）。

## 関連
- [[reflexivity]]（**根本エンジン**＝bust は reflexive ゆえ突然・holder集中は反転時 exit の増幅器）/ [[onchain-verification]]（資金移動の検算）/ [[launchpad-economics]]（98.5%が死ぬ母集団＝rugの温床）/ [[perp-dex-wars]]（$JELLY whale操作）/ [[external-event-to-token-pattern]]（政治meme grift）
- [[$LIBRA]] / [[$TRUMP]] / [[@lookonchain]] / [[@badattrading_]] / [[@a1lon9]] / 集計の入口: [[signal|Signal digest]]

## 出典(生ソース)
[[@lookonchain]] $LIBRA/$MELANIA/$YZY/$JELLY/MrBeast/$WBTC, [[@badattrading_]] sniper/insider/bundled解析,
[[@a1lon9]] $LIBRA rug認定。（全て sources/x/ の原ツイに保存済）
