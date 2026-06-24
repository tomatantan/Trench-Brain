---
type: concept
title: 型 — rugの解剖（繰り返す抽出メカニクスと赤旗チェックリスト）
created: 2026-06-23
updated: 2026-06-24
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
| [[$AXIOS]] | graduated | ~$53k | reply0 / KOL0 | 複数サイクル(~1.5日) | 出来高消費後・買い手不在 | **graduated-but-empty**＝KOL無し卒業型の自然死 |
| [[$VCSOL]] | graduated | ~$192k | reply0 / KOL0 | ~1日 | IP参照命名もtraction取れず・興味消滅 | graduated-but-empty（IP借用≠KOL代替） |
| [[$MOONLAKE]] | graduated | $1.03M | reply0 / KOL0 | ~1日(BREAKOUT後即死) | AIテーマ冠・有機的需要ゼロ | **BREAKOUT-then-dead**＝traction無しBREAKOUTは持続しない |
| [[$PHONEBLACK]] | graduated | ~$214k | reply0 / KOL0 | ~1日(BREAKOUT後崩壊) | traction無しBREAKOUT→全損 | BREAKOUT-then-dead（$MOONLAKEと同型・崩壊深度最大-98.7%） |
| [[$TBHR]] | graduated | ~$19k | reply0 / KOL0 | ~1日 | gaming/Steam命名もtraction伝播ゼロ | graduated-but-empty（実在リンク≠traction代替） |
| [[$EYEZ]] | graduated | ~$1.4k | reply0 / KOL0 | 誕生即死 | mcap枯れ（初観測≒最終） | traction無しの即死 |
| [[$JAKE]] | graduated | ~$1.4k | reply0 / KOL0(twitter無し) | 誕生即死 | mcap枯れ | traction無しの即死（social基盤ゼロ） |
| [[$SLICK]] | graduated | ~$1.5k | reply0 / KOL0 | 誕生即死 | mcap枯れ | traction無しの即死 |
| [[$MAYHAM]] | graduated | ~$421 | reply0 / KOL0(twitter/web無し) | 誕生即死(peak=last) | mcap枯れ（コホート最低） | traction無しの即死（social基盤ゼロ最低mcap） |
| [[$NUERS]] | 勢い門(T1) | ~$33,800 | reply0 / KOL0 | 数サイクル(~1日) | mcap枯れ(peak比-90.2%) | graduated-but-empty（KOL無し→出来高消費後・自然死） |
| [[$WORLDCRAFT]] | graduated | ~$112k | reply0 / KOL0 | 短期 | mcap枯れ($1,383、-98.8%) | graduated-but-empty（twitter/web整備済・社会需要ゼロ） |
| [[$BABYFACE]] | T1(4窓) | ~$267k | reply0 / KOL0 | 4窓(~24h) | mcap枯れ($3,389、-98.7%) | T1-only4窓survivor候補→mcap枯れ（KOL不在の上限）|
| [[$RONALDINU]] | traction:kol(SeruDefi) | ~$1.4k | reply0 / KOL:SeruDefi(10likes) | 誕生即死 | mcap枯れ($1,407) | KOL言及あり誕生即死（KOL engagement低・community不追随） |
| [[$BBQ]] | traction:kol(SeruDefi) | ~$2.2k | reply68 / KOL:SeruDefi(28likes) | 誕生即死 | mcap枯れ($2,186) | rug後revival・KOL強推薦も誕生即死（revival≠生存保証） |
| [[$COVER]] | T1(15窓) | ~$289k | reply0 / KOL0 | 15窓(~3.75日) | mcap枯れ($2,364、-99.2%) | T1-only最長15窓→mcap枯れ（KOLゼロの天井・BABYFACE4窓と同死因） |
| [[$TAG]] | graduated | ~$6k | reply0 / KOL0 | 誕生即死 | mcap枯れ($5,790) | traction無しの即死（low-signal $6kコホート・social有り需要ゼロ） |
| [[$VORTEX]] | graduated | ~$1,259 | reply0 / KOL0 | 誕生即死 | mcap枯れ($1,259) | traction無しの即死（deployer toolブランド名でも community ゼロ） |
| [[$ADTX]] | graduated | ~$12k | reply0 / KOL0 | 短期(1〜2サイクル) | mcap枯れ($3,675・peak比-70%) | graduated-but-empty（実株ティッカー借用・reddit link・社会需要ゼロ） |
| [[$ANYONE]] | traction:mcap>=30000 | ~$134k | reply0 / KOL0 | 即死(1サイクル) | mcap枯れ($465・peak比-99.7%) | association marketing偽装(@jup_studio 借用)×traction0→1サイクル完全崩壊（-99.7%は観測最速級） |
| [[$TOROS]] | graduated | ~$125.6k | reply0 / KOL0（全3窓） | 3窓（~12h） | mcap枯れ($1,963・peak比-98.4%) | BREAKOUT-then-dead（Toros Finance association marketing × whale pump・$MOONLAKE/$PHONEBLACK と同型・12h完結） |
| $HI×3(squatter) | graduated/prebond | ~$84〜$146 | reply0 / KOL0 | 誕生即死 | mcap枯れ($84〜$146) | $HIコピー量産squatter誕生即死（generic name ticker の多重 mint・同名コホート同時多発型） |
| [[$VORTEX-4YLTUY]] | graduated | ~$1,326 | reply0 / KOL0 | 誕生即死 | mcap枯れ($1,324) | 同ブランド再登場の即死（VortexDeployer.com 2nd mint・前回$1,259と同水準で同じ死・ブランド再利用≠traction） |
| [[$HI-UZWrgk]] | graduated | ~$46,542 | reply0 / KOL0 | 誕生即死 | mcap枯れ($120・-99.7%) | squatter コホート高 peak 版——$46k まで立ったが peak 比 -99.7% 崩壊（$ANYONE と同崩壊率・generic name は peak mcap 高低によらず死ぬ実証） |
| [[$VINTEDGATE]] | graduated | ~$49,212 | reply0 / KOL0 | 短期(1サイクル以内) | mcap枯れ($3,505・-92.9%) | [[external-event-to-token-pattern]] 欧州イベント借用型——Vinted 論争 × X/TikTok social 有り × crypto traction 未伝播で死（イベント名×social整備≠crypto need） |
| [[$LEGACY]] | prebond(mcap>=30k) | ~$31,597 | reply0 / KOL0 | 誕生即死(bonding curve未卒業) | mcap枯れ($911・-97.1%) | Pokemon IP借用（Legacy Pikachu）× traction0 → prebond で消滅（$VCSOL と同型：IP参照命名≠traction代替・N 追加） |
| [[$GTASOLANA]] | traction:kol(badattrading_・警告) | ~$89k | reply0 / KOL:警告のみ | 短期（数時間） | mcap枯れ($2,094・-97.7%) | bundled scam×GTA6便乗×KOL「buy するな」警告後崩壊——KOL traction が「ネガティブ警告」だった初例。警告KOL言及は有機的需要でなく即死加速シグナル |
| [[$HARU]] | traction:kol(badattrading_・警告) | **~$1,044,616（コホート最高）** | reply0 / KOL:警告のみ | 短期（数時間） | mcap枯れ($6,759・**-99.4%**) | bundled scam×KOL警告後崩壊＝$GTASOLANA同型・peak $1M超でも-99.4%崩壊（peak mcap高さ≠生存の実証強化） |
<!-- death-ledger: 以降 synthesize.sh が追記。古い順に貯める。 -->

**現時点で浮いている型（N=28 確定死亡・2026-06-24 更新）**: ①**traction(reply/KOL)ゼロ × 出来高先行**で上げた銘柄は死にやすい——**確定死亡 N=28**（N=26 前回 + [[$VINTEDGATE]]×1 + [[$LEGACY]]×1）。⑦**BREAKOUT-then-dead の association marketing 確定例**（$TOROS）——Toros Finance DeFi ブランド借用 × traction0 で BREAKOUT → 3窓12h で peak比-98.4%崩壊。⑧**generic name squatter 量産コホート**（$HI×3+$HI-UZWrgk）——generic ticker の多重 mint は高 peak（$46k）でも peak 比 -99.7% で死ぬ実証（peak mcap 高低によらない）。⑨**同ブランド再登場即死**（[[$VORTEX]] 2例）——同一 VortexDeployer.com ブランドが mint を変えて再登場しても community 需要がゼロのまま同水準で死亡；ブランド名の再利用が traction を呼ばない N=2 実証。⑤**KOL 言及あり誕生即死**（$RONALDINU/$BBQ）——KOL gate 通過 ≠ community 追随の実証。⑥**T1-only の上限実証**（$BABYFACE:4窓/$COVER:15窓）——KOL ゼロで到達可能な momentum の天井（$267k〜$289k）を N=2 で可視化。他は全件 reply0/KOL0 のまま死亡＝「traction の不在」が死の先行指標として型化（⚠️ 同一コホート・同一時間帯の観測で独立性は限定的）。②graduated でも KOL ピックアップ無し＝「graduated but empty」型（[[launchpad-economics]]）が主流死因。③**traction-less BREAKOUT → 即死**（$MOONLAKE/$PHONEBLACK/$TOROS・N=3）——BREAKOUT が社会的需要を生まない実証が N=3 に強化。④誕生即死量産型（$EYEZ/$JAKE/$SLICK/$MAYHAM）は型通りにつき1行記録のみ。

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
- **全層を1判断に束ねる capstone**: [[ape-or-avoid]]（乗るか避けるかの統合フレーム）
- **on-chainの死(本ページ)に対し social手口は [[manipulation-playbook]]**（pumper exit誘導/協調bot投票/借用ナラ＝出口工作フェーズで多発・両輪で読む）
- [[reflexivity]]（**根本エンジン**＝bust は reflexive ゆえ突然・holder集中は反転時 exit の増幅器）/ [[onchain-verification]]（資金移動の検算）/ [[launchpad-economics]]（98.5%が死ぬ母集団＝rugの温床）/ [[perp-dex-wars]]（$JELLY whale操作）/ [[external-event-to-token-pattern]]（政治meme grift）
- [[$LIBRA]] / [[$TRUMP]] / [[@lookonchain]] / [[@badattrading_]] / [[@a1lon9]] / 集計の入口: [[signal|Signal digest]]

## 出典(生ソース)
[[@lookonchain]] $LIBRA/$MELANIA/$YZY/$JELLY/MrBeast/$WBTC, [[@badattrading_]] sniper/insider/bundled解析,
[[@a1lon9]] $LIBRA rug認定。（全て sources/x/ の原ツイに保存済）
