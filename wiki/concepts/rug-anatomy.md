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
| [[$GTA6Begin]] | traction:graduated(~$168.7k) | ~$168,727 | reply0 / KOL0（twitter=@GTAVI_Countdown association marketing） | 3窓(~12-18h) | mcap枯れ($3,742・peak比-97.8%) | IP借用×association marketing×GTA wave第2波→3窓崩壊（$GTASOLANA 同 wave 後続・[[external-event-to-token-pattern]]） |
| $AT(HzSqzun) | graduated($258) | ~$258 | reply0 / KOL0 | 誕生即死 | mcap枯れ($258) | traction無しの即死（ultra-low mcap・1文字ticker・social基盤ゼロ） |
| [[$ABUSE]] | graduated($245k) | **~$250,488（コホート最高 peak の一つ）** | reply0 / KOL0（twitter/website整備済） | ~5窓(~4日) | mcap枯れ($1,533・peak比-99.4%) | graduated-but-empty高peak版——$250k から reply/KOL ゼロのまま whale pump→分配→1窓崩壊（website/twitter 整備済みでも organic community ゼロは補えなかった） |
| [[$GTA]] | traction:graduated | ~$71k | reply0 / KOL0 | 短期（~2-3サイクル） | mcap枯れ($5,705・peak比-91.9%) | GTA6 IP直接借用×traction0→BREAKOUT+235%→崩壊（$B4GTA6/$GTA6Begin/$GTASOLANA と同 GTA wave コホート・IP借用4例目） |
| [[$GTT]] | traction:graduated | ~$130k | reply0 / KOL0 | 7窓(~42h) | mcap枯れ($1,471・peak比-98.9%) | GTA6便乗×social整備済(twitter+web)×7窓後全崩壊——第53窓意外反転(+36%)は最終出口利用・social整備≠traction代替の実証（[[external-event-to-token-pattern]]） |
| $AT-BHagmz | graduated(complete=true) | ~$60 | reply0 / KOL0 | 誕生即死 | mcap枯れ($60・peak=last) | 1文字ticker squatter $AT 2例目——$AT(HzSqzun)$258 に続く同型の超低 peak 誕生即死（entity 作成スキップ・分母算入のみ） |
| [[$EPSTEIN]] | traction:mcap>=30000 | ~$30k | reply0 / KOL0 | 数サイクル(~1日) | mcap枯れ($5,749・-81%) | 政治meme × prebond 縮退死——Jeffrey Epstein テーマ × traction0 × bonding curve 未突破で自然消滅（$LEGACY 同型：政治/陰謀論 naming × prebond ≠ traction 代替）|
| [[$CLO]] | traction:graduated | ~$28k | reply0 / KOL0（a1lon9 association marketing偽装） | 数サイクル | mcap枯れ($4,137・-85.3%) | graduated-but-empty × association marketing（a1lon9 tweet を deployer が公式twitter欄に設定・kol_ca空・実際の言及なし）——$ANYONE/$TOROS と同 authority 借用型 |
| [[$COMMOTITTY]] | traction:kol(badattrading_・警告) | ~$313 | reply0 / KOL:警告のみ | 誕生即死 | mcap枯れ($313) / bundled scam確定 | KOL警告→即死（$GTASOLANA/$HARU同型）× bundled scam × KobeissiLetter association marketing偽装——観測コホート最低 peak・警告KOL言及は即死加速 |
| [[$LION]] | traction:graduated | ~$8.9k | reply0 / KOL0（NatGeoTV association marketing偽装） | 誕生即死 | mcap枯れ($2,326・-74%) | graduated-but-empty 低 peak 版——NatGeoTV tweet を deployer が公式 twitter に設定（$CLO の a1lon9 借用と同型）× traction0 → 即死 |
| [[$AEGIS]] | traction:graduated | ~$76k | reply0 / KOL0 | 数サイクル(~2日) | mcap枯れ($6,086・-92%) | BREAKOUT-then-dead（privacy テーマ冠・+160%BREAKOUT後 2日で崩壊——$MOONLAKE/$PHONEBLACK と同型・N追加） |
| [[$GOONER]] | traction:graduated | ~$73k | reply0 / KOL0（TRobinsonNewEra association marketing偽装） | 誕生即死 | mcap枯れ($1,475・-98%) | association marketing（Tommy Robinson 極右政治活動家）×銃器事件exploitation命名→即死（$CLO/$LION 同型：authority借用型・政治センセーショナル版） |
| [[$UFO]] | traction:graduated | ~$9.3k | reply0 / KOL0（PumpFun711非公式 association marketing） | 誕生即死 | mcap枯れ($1,577・-83%) | peak$10k未満→死亡率100%帯通り確定（historical 予測通り）×PumpFun711非公式 association marketing で需要補完不能 |
| [[$GRUMBLE]] | traction:graduated | ~$78.9k | reply0 / KOL0 | 複数サイクル(~1日) | mcap枯れ($1,255・peak比-98.4%) | graduated-but-empty（twitter/website整備済×community ゼロ＝$WORLDCRAFT/$ABUSE 同型） |
| [[$BULL]] | traction:graduated | ~$29.2k | reply0 / KOL0（Crypto_Alch⚠️未確認・zankyosol association marketing疑い） | 複数サイクル(~1日) | mcap枯れ($2,288・peak比-92.2%) | graduated-but-empty × association marketing疑い（KOL未確認のまま死亡・$CLO/$LION 同型） |
| [[$EWS]] | traction:graduated | ~$184k | reply0 / KOL0（全14+窓） | ~14窓(数日) | mcap枯れ($1,590・peak比-99.1%) | T1-only long追跡型——Elon/AWS association marketing × $187k resistance 突破不能 × 散発需要消滅（[[external-event-to-token-pattern]]） |
| $BROKEN(8mhAsG) | traction:graduated | ~$1.3k(peak=last) | reply0 / KOL0 | 誕生即死 | mcap枯れ($1,292) | traction無しの即死（generic name・ultra-low peak・entity作成スキップ） |
| $WARDEN(9GmLK9) | traction:graduated | ~$1.2k(peak=last) | reply0 / KOL0 | 誕生即死 | mcap枯れ($1,208) | traction無しの即死（generic name・ultra-low peak・entity作成スキップ） |
| $67NGELES(9WWnY1) | traction:graduated | ~$1.2k(peak=last) | reply0 / KOL0 | 誕生即死 | mcap枯れ($1,214) | traction無しの即死（ultra-low peak・entity作成スキップ） |
| $MONOPOLY(Dm2pvA) | traction:graduated | ~$1.7k(peak=last) | reply0 / KOL0 | 誕生即死 | mcap枯れ($1,718) | traction無しの即死（"Monopoly Money"・ultra-low peak・entity作成スキップ） |
| [[$50-6SYbKV]] | traction:mcap>=30000（未卒業） | ~$37.6k | reply0 / KOL0 | 誕生即死（数窓） | mcap枯れ($953・peak比-97.5%・complete=false） | 数字のみ generic ticker・同名別 mint（$50コホート2本目）・bonding curve 未卒業死（$HI multi-mint 型を補強） |
| [[$MECCHA]] | traction:graduated | ~$43.8k | reply0 / KOL0 | 複数窓(~1日) | mcap枯れ($1,903・peak比-95.7%) | jp-meme命名（「めっちゃ」+Chameleon・anime Japan テーマ）× traction0 → 死亡（[[jp-meme-cluster]] 命名系失敗例・graduated-but-empty 型） |
| [[$SAI]] | traction:graduated | ~$22.4k | reply0 / KOL0 | 誕生即死（1窓・~23分） | mcap枯れ($1,240・peak比-94.5%) | AI 命名（Sensix Ai）×独自ドメイン整備済み× traction0 → 即死（低 peak 帯 AI テーマ命名失敗・entity は作成直後に閉じ） |
| $WEN(6CsMmCz) | traction:graduated | ~$4.4k | reply0 / kol_ticker:badattrading_（ticker言及のみ） | 誕生即死 | mcap枯れ($3,103) | Wendy's Co 命名・BurryJMichael tweet + Reddit WSB リンク association marketing → 即死（entity作成スキップ・ultra-low peak） |
| $LEEKUANYEW(4xKykH) | traction:graduated | ~$3.9k | reply0 / KOL0（Elon Musk tweet association marketing・twitter=elonmusk投稿） | 誕生即死 | mcap枯れ($3,913・peak=last) | Elon Musk tweet を公式 twitter に設定した Lee Kuan Yew association marketing → 即死（$CLO/$LION 型：authority借用型・極低 peak） |
| [[$RELAYNET]] | traction:graduated | ~$95.4k | reply0 / KOL0 | 誕生即死（~27分） | mcap枯れ($1,347・peak比-98.6%) | graduated-but-empty 誕生即死（RelayNet tech/meme・twitter/website整備済×community需要ゼロ＝$GRUMBLE/$MECCHA 同型） |
| [[$PULLIES]] | traction:graduated | ~$24.6k | reply0 / KOL0 | 複数窓 | mcap枯れ($5,956・peak比-75.7%) | gym/crypto スラング命名・social整備済(twitter/website)×traction0→死亡（graduated-but-empty 型・$MECCHA/$SAI/$RELAYNET 同型） |
| $JUAN(9xZuyY) | traction:graduated | ~$1.5k(peak=last) | reply0 / KOL0（twitter/website=他人のtweetリンク） | 誕生即死 | mcap枯れ($1,531) | 他人tweet association marketing × ultra-low peak → 即死（entity作成スキップ） |
| $MOUSER(4S2HkH) | traction:graduated | ~$7.4k(peak) | reply0 / KOL0（twitter=shubgaur tweet） | 誕生即死 | mcap枯れ($5,082) | AI agent命名×association marketing×ultra-low peak → 即死（entity作成スキップ） |
| [[$EC43]] | traction:kol(badattrading_・構造チェック) | ~$128,967 | reply0 / KOL:badattrading_(構造警告・sniper7.4%/KuCoin8%) | 複数サイクル(~1日) | mcap枯れ($12,320・peak比-90.4%) | sniper7.4%×KuCoin8%集中×traction0→whale pump崩壊（badattrading_警告が正しかった・graduated-but-empty高peak版） |
| [[$WIFFY]] | traction:kol(badattrading_・**bundled scam警告**) | ~$2,492 | reply0 / KOL:badattrading_「bundled scam」CA直接警告 | 誕生即死 | mcap枯れ($2,492) | bundled scam × KOL警告即死（$GTASOLANA/$HARU/$COMMOTITTY/$WENMAXX と同型・Wendy's wave 同時発生） |
| $WENDOG(88eXUs) | traction:graduated | ~$1,414 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($1,372) | traction無しの即死（Wendy's Co波の亜種・同時多発・entity作成スキップ） |
| $WENDYGUY(F9Byw) | traction:graduated | ~$1,251 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($1,251) | traction無しの即死（Wendy's Co波・同時多発・entity作成スキップ） |
| $DEATHNOTE(AaBKe) | traction:user_checked | ~$4,418 | reply0 / KOL0（death note anime meme） | 誕生即死(birth=death) | mcap枯れ($4,418) | anime IP借用×traction0→即死（デスノート命名・entity作成スキップ） |
| [[$JALAPEÑO]] | traction:graduated | ~$102,347 | reply0 / KOL0（wallstengine association・Axiom DEX website） | 複数サイクル(~1.5日) | mcap枯れ($9,296・peak比-90.9%) | BREAKOUT-then-dead確定（+102%BREAKOUT→底→反発×3→最終崩壊・跳躍台帳記録済・$AEGIS/$MOONLAKE/$PHONEBLACK/$TOROS 同型・長期死亡経路実証） |
| [[$AT-DsvbjG]] | traction:mcap>=30000 | ~$157,631 | reply0 / KOL0 | 誕生即死（数窓内） | mcap枯れ($266・-99.8%) | 1文字generic ticker × prebond × traction0 → $157k から$266へ即死（$ANYONE/$LEGACY 同型・$ATコホート3本目全滅・peak mcap高低によらず死ぬ確定） |
| $WENJAK(942HA2) | traction:graduated | ~$1,261 | reply0 / KOL0（Wendy's Co wave） | 誕生即死(birth=death) | mcap枯れ($1,261) | traction無しの即死（Wendy's Co wave 同時多発・$WENDOG/$WENDYGUY と同型・entity作成スキップ） |
| [[$MDT]] | traction:user_checked | ~$17,036 | reply0 / KOL0（twitter/website整備済） | 複数サイクル(~1日) | mcap枯れ($1,707・peak比-90%) | graduated-but-empty（Minidiggers命名・social整備済×traction0→自然消滅・$PULLIES/$RELAYNET/$GRUMBLE 同型） |
| [[$EAGLE250]] | traction:graduated | ~**$1,060,656** | reply0 / KOL0（twitter/website完全ゼロ） | 複数サイクル(~1日) | mcap枯れ($96,307・peak比-90.9%) | BREAKOUT-then-dead 最純粋形——social/KOL/reply ゼロのまま peak $1M 超到達後崩壊（$MOONLAKE/$PHONEBLACK/$TOROS/$AEGIS と同型・social 基盤ゼロ最高 peak 例） |
| [[$THEBLOOP]] | traction:graduated | ~$423,907 | reply0 / KOL0（twitter/website整備済・internet meme lore あり） | 複数サイクル(~1日) | mcap枯れ($13,816・peak比-96.7%) | BREAKOUT-then-dead（+208%BREAKOUT後→peak $423k→崩壊・Bloop lore × KOL不在 = traction 未変換・$MOONLAKE/$PHONEBLACK/$AEGIS/$JALAPEÑO と同型） |
| [[$WENBOY]] | traction:mcap>=30000 | ~$311,473 | reply0 / KOL0（全13窓・一貫ゼロ） | 13窓（~3日） | mcap枯れ($1,575・peak比-99.5%) | 13窓最長追跡→peak $311k→0.5%未満まで溶解（KOL不在のまま $170k条件クリア・候補消滅後も最終死亡確定・T3ゼロ高値持続不能の最長実証） |
| $FINLEY(DLJgWQ) | traction:graduated | ~$1,659 | reply0 / KOL0（redacted_noah tweet・GitHub chewingglass） | 誕生即死(birth=death) | mcap枯れ($1,612) | multi-mint競合即死（同バッチで3 mint 同時出現・最弱コピーが流動性ゼロで消滅・entity作成スキップ） |
| $JEWCOIN(HTCC1j) | traction:mcap>=30000 | ~$54,106 | reply0 / KOL0（offensive name・social無し） | 数窓 | mcap枯れ($3,895・peak比-92.8%) | 攻撃的名称×traction0→死亡（entity作成スキップ・log 1行のみ） |
| [[$FINLEY-59JgPz]] | traction:graduated | ~$52,779 | reply0 / KOL0（redacted_noah tweet・GitHub chewingglass） | 数窓 | mcap枯れ($5,011・peak比-90.5%) | multi-mint競合敗北（7rANTZ mint に流動性吸収・graduated後崩壊・$59JgPz は第2位 mint） |
| $MAYHAM(5pP5vo) | traction:graduated | ~$163 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($163) | 誕生即死・別 mint 同銘柄 2 例目（$MAYHAM D5Gqvj が先行して死亡済・entity作成スキップ） |
| $OBSERVED(F5aaF3) | traction:graduated | ~$1,012 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($844) | 誕生即死・社会基盤完全ゼロ・entity作成スキップ |
| $WORLDCHUA(82VSr4) | traction:graduated | ~$1.5k(peak=last) | reply0 / KOL0（twitter/website無し） | 誕生即死(birth=death) | mcap枯れ($1,445) | traction無しの即死（ultra-low peak・entity作成スキップ） |
| [[$WENS]] | traction:graduated | ~$115,467 | reply0 / KOL0（全窓通じゼロ） | 複数窓 | mcap枯れ($1,534・peak比-98.7%) | BREAKOUT-then-dead確定（+89%上昇→peak $115k→崩壊・traction0のまま・$EAGLE250/$MOONLAKE/$THEBLOOP と同型） |
| [[$JONAH]] | traction:graduated | ~$12,530 | reply0 / KOL:@JEET(association marketing疑い・watchlist外) | 数窓 | mcap枯れ($3,923・peak比-68.7%) | graduated-but-empty 低 peak（@JEET tweet association marketing疑い×reply0→死亡・$CLO/$LION/$BULL 同型：authority借用型） |
| $HAMA(2w5nRa7) | traction:graduated | ~$1,547 | reply0 / KOL0（website=hamadog.fun のみ） | 誕生即死(birth=death) | mcap枯れ($1,540) | traction無しの即死（website整備済・social需要ゼロ・entity作成スキップ） |
| $MAYHAM(3vpeyAb) | traction:graduated | ~$107 | reply0 / KOL0（social完全ゼロ） | 誕生即死(birth=death) | mcap枯れ($107) | 4本目の同名mint誕生即死（D5Gqvj:$421→5pP5vo:$163→AWchjc pending と同コホート・観測史上最低mcap候補・entity作成スキップ） |
| [[$WENDYS-AEwbCr]] | traction:mcap>=30000 | ~$98,785 | reply0 / KOL0（twitter/website無し） | 数窓 | mcap枯れ($511・peak比-99.5%) | duplicate-ticker 2本目×traction0→型通り死亡（[[WENDYS]] mint 41Ktmp1K と同名別 mint 競合・social基盤ゼロ・2本とも死亡） |
| [[$PLUTO]] | traction:graduated | ~$76,778（二次pump天井） | reply0 / KOL0（全期間） | 複数窓 | mcap枯れ($1,401・peak比-98.2%) | 二次pump=1窓寿命（$74.7k初観測→-84%底→$76.8k二次pump前ピーク超え→翌窓-98.2%崩壊・KOL/reply全期間ゼロ・T3なし二次pump=演出確定） |
| [[$HAMA-85HFRQa]] | traction:graduated | ~$55,343 | reply0 / KOL0（hamadog.fun整備済・social需要ゼロ） | 数窓 | mcap枯れ($1,578・peak比-97.1%) | 同ブランド再 mint × traction0→死亡（先行 mint(2w5nRa7)即死直後に同ブランド2本目発射・graduated後崩壊・ブランド再利用が traction を呼ばない N=2+1） |
| $AIVEXA(9Sw9MaxE) | traction:graduated | ~$3,141 | reply0 / KOL0（@AiVexaa 整備済） | 誕生即死(birth=death) | mcap枯れ($1,459・peak比-53.6%) | AI-themed ultra-low peak 誕生即死（twitter/website整備・KOL0・entity作成スキップ） |
| $GRQ(DVGerQPf) | traction:graduated | ~$190 | reply0 / KOL0（social完全ゼロ） | 誕生即死(birth=death) | mcap枯れ($190・peak=last≒$190) | ultra-low peak 誕生即死（name="GET RICH QUICK"・social無し・entity作成スキップ） |
| [[$WENMAXX]] | traction:kol(badattrading_・**bundled scam警告**) | ~$165,356（peak） | reply0 / KOL:badattrading_（警告・CA直接指定） | 複数サイクル（~1-2日） | mcap枯れ($1,724・peak比-98.9%) | bundled scam × KOL警告後pump継続→最終崩壊（$HARU/$GTASOLANA/$COMMOTITTY と同型・警告後pump継続は最長クラスも結末同じ・Wendy's Maxxing命名） |
| [[$AURAFARM]] | traction:graduated | ~$52,394 | reply0 / KOL0（twitter/website整備済） | 誕生即死（1〜2サイクル） | mcap枯れ($1,324・peak比-97.5%) | graduated-but-empty（aura farming独自命名・aurafarming.wiki整備済×community需要ゼロ・$GRUMBLE/$MECCHA 同型） |
| [[$DROOLING]] | traction:mcap>=30000（prebond） | ~$60,845（peak・bonding curve 未卒業） | reply0 / KOL:ticker言及あり(Crypto_Alch・別mint可能性) | 数サイクル以内（prebond） | mcap枯れ($4,800・-92%・bonding curve 未卒業） | prebond消滅（cat meme・KOL ticker言及はあったが CA紐付きなし・別mint由来の可能性高——「KOL ticker言及 ≠ CA直接支持」の実証） |
| [[$GMR]] | traction:graduated | ~$56,895 | reply0 / KOL0（@GMRDEV1+greatmemereset.cc整備済） | 2窓(~12h) | mcap枯れ($1,263・peak比-97.8%) | graduated-but-empty（"Great Reset"政治ミーム転用×social整備済×community需要ゼロ・$GRUMBLE/$AURAFARM 同型） |
| $WARRIOR23(3MfXppuB) | traction:graduated | ~$238 | reply0 / KOL0（social無し） | 誕生即死(birth=death) | mcap枯れ($238) | traction無しの即死（LeBron wave・ultra-low peak・entity作成スキップ） |
| $LSSSM23(Hdi8XY9F) | traction:graduated | ~$55 | reply0 / KOL0（social無し） | 誕生即死(birth=death) | mcap枯れ($55) | traction無しの即死（LeBron wave・観測史上最低 peak 候補・entity作成スキップ） |
| $LOR23(5HKC47hc) | traction:graduated | ~$61 | reply0 / KOL0（social無し） | 誕生即死(birth=death) | mcap枯れ($61) | traction無しの即死（LeBron wave・$LSSSM23と同水準超低peak・entity作成スキップ） |
| [[$LEBRON23]] | traction:mcap>=30000（prebond） | ~$62,759 | reply0 / KOL0（social完全ゼロ） | 数窓（~1日） | mcap枯れ($188・peak比-99.7%) | prebond消滅（LeBron引退 event-driven meme × traction0 → bonding curve 未突破・$EPSTEIN/$LEGACY 同型：event naming × prebond ≠ traction 代替；同wave $WARRIOR23/$LSSSM23/$LOR23 と全滅コホート完成） |
| $LEBRON23(8YHxUh) | traction:graduated | ~$69 | reply0 / KOL0（social無し） | 誕生即死(birth=death) | mcap枯れ($69) | LeBron wave 同名2本目 mint 誕生即死（先行 6bKKMiw と同名・peak $69 = コホート最低水準・entity作成スキップ） |
| $RICH23(FSTViL) | traction:graduated | ~$804 | reply0 / KOL0（twitter/website無し） | 誕生即死(birth=death) | mcap枯れ($804) | LeBron Retirement Rich 命名 × traction0 → 即死（LeBron wave 同バッチ・entity作成スキップ） |
| $MOONEXPRES(Dh34vi) | traction:graduated | ~$1,305 | reply0 / KOL0（twitter/website整備済） | 誕生即死(birth=death) | mcap枯れ($1,305) | MOONEXPRESS 命名 × traction0 → 即死（website moonexpress.online・social整備済でも community需要ゼロ・entity作成スキップ） |
| [[$AY YAI YAI]] | traction:graduated | ~$157,788 | reply0 / KOL0（Elon Musk tweet association marketing・real_sol≈56.4SOL） | 数時間（birth→peak→death 同バッチ内） | mcap枯れ($2,300・peak比-98.5%) | Elon tweet association marketing × multi-mint競合($YAI/$AIAIAI-Cbqrm9) × traction0 → -98.5%崩壊（real_sol 56.4SOL が deployer 出口流動性として機能・$LEEKUANYEW/$RO 同型：authority借用型 peak $157k でも需要ゼロ確認） |
| [[$ALICORN]] | traction:graduated | ~$26,417 | reply0 / KOL0（lilbruhfish tweet・CA未確認） | 誕生即死(birth=death) | mcap枯れ($2,533・peak比-90.4%) | low-mcap graduated→即死（fantasy creature命名・tokenized_agent=true⚠️疑・traction皆無・$AIVEXA/$AURAFARM 同型：low-peak graduated-but-empty） |
| $APPI(5gPmFC) | traction:graduated | ~$1,259 | reply0 / KOL0（twitter:@appipumpfun/website:appi.one） | 誕生即死(birth=death) | mcap枯れ($1,259) | traction無しの即死（social整備済・ultra-low peak・entity作成スキップ） |
| [[$AIAIAI-Cbqrm9]] | traction:graduated | ~$111,397 | reply0 / KOL0（Elon Musk tweet association marketing・real_sol≈54.3SOL） | 4窓（~1.5h） | mcap枯れ($1,381・peak比-98.8%) | エバポレーション型——4窓 $100k維持後に崩壊（$AY YAI YAI -98.5%と同型・ay yai yai 3本目 mint も全滅・real_sol deployer出口確認） |
| $SHIROAI(4cU5AG) | traction:graduated | ~$29,066 | reply0 / KOL0（twitter:@shiroaipumpfun/website:shiroai.art） | 誕生即死(birth=death) | mcap枯れ($1,982・peak比-93.2%) | AI命名 × 誕生即死（shiroai.art整備済×traction0・entity作成スキップ） |
| $SOILJIM(26xAefC) | traction:graduated | ~$1,254 | reply0 / KOL0（twitter:@soiljim/website:soiljim.com） | 誕生即死(birth=death) | mcap枯れ($1,254) | traction無しの即死（ultra-low peak・entity作成スキップ） |
| [[$JOB]] | traction:mcap>=30000（prebond） | ~$34.9k | reply0 / KOL0（MooonVaultx tweet association marketing疑い） | 誕生即死(birth=death) | mcap枯れ($458・peak比-98.7%・bonding curve 未卒業) | prebond消滅×Wendy's wave後続×association marketing→即崩壊（$EPSTEIN/$LEGACY/$LEBRON23 同型：prebond ≠ traction 代替；Wendy's wave 後続コホート全滅N追加） |
| [[$HOOT]] | traction:graduated | ~$63,966 | reply0 / KOL0（@nobodydriving association marketing疑い） | 数サイクル(~1日) | mcap枯れ($5,892・peak比-90.8%) | graduated-but-empty × association marketing（@nobodydriving tweet を公式twitter設定・watchlist外・$CLO/$LION/$BULL 同型）× ticker/name乖離(HOOT vs sage) × traction0 → -90.8%崩壊 |
| [[$YAI]] | traction:graduated | ~$110,829 | reply0 / KOL0（full 10窓追跡・multi-mint競合） | 10窓(~1日) | mcap枯れ($1,419・peak比-98.7%) | multi-mint競合の敗者側——$AY YAI YAI(同テーマ/同クラスター)が勝者、YAI は 10窓 oscillation(-25%→回復→-44%→回復→-48%→崩壊)の末 T3ゼロのまま崩壊。需要がクラスター内1本に集中した構図の敗者サイド実証 |
| [[$AIAIAI]] | traction:graduated | ~$87,564 | reply0 / KOL0（@bingusdevss association marketing疑い・tokenized_agent=true） | 数窓(~5h) | mcap枯れ($8,260・peak比-90.6%) | AI命名(AIAssociatedInstituteAmericaINC)×tokenized_agent=true×traction0→崩壊——AI フラグが traction の代替にならない N 追加（$SAI/$AIVEXA/$MOONLAKE 同型。$AIAIAI-Cbqrm9 とは別 mint） |
| $LOM(CV37tc) | traction:graduated | ~$1,332 | reply0 / KOL0（twitter:@leagueofmeme_） | 誕生即死(birth=death) | mcap枯れ($1,316) | traction無しの即死（ultra-low peak・LEAGUE OF MEME・entity作成スキップ） |
| $GAMBLE(CHYuyZ) | traction:graduated | ~$1,286 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($1,270) | traction無しの即死（"Billions must gamble"命名・ultra-low peak・entity作成スキップ） |
| $PEACHY(GwXRfJ) | traction:graduated | ~$4,090 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($4,090) | traction無しの即死（"Airman Peachy" US Air Force mascot命名・tokenized_agent=true も即死・entity作成スキップ） |
| [[$STARBASE]] | traction:graduated | ~$635,928（post-exit deployer pump ATH） | reply0 / KOL0（全期間） | 12窓+post-exit pump | mcap枯れ($3,294・peak比-99.5%) | SpaceX外部event命名×KOL/reply全期間ゼロ×list exit後deployer自己資金pump→ATH→-99.5%崩壊（post-exit deployer pump パターン確定・[[external-event-to-token-pattern]]/[[spacex-ipo-narrative]]接続・peak $635k はコホート最高水準） |
| [[$TOKEN]] | traction:graduated | ~$41,382 | reply0 / KOL0（全期間） | 複数窓（~数時間） | mcap枯れ($4,934・peak比-88.1%) | graduated-but-empty 縮退型——DeFi generic ticker(sTokens)×traction0×3窓連続下落→枯れ（[[launchpad-economics]] 縮退死の典型） |
| $BEAR(2htygu7) | traction:graduated | ~$234 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($234) | "BEAR MARKET"命名×ultra-low peak→即死（entity作成スキップ） |
| [[$FINLEY-7rANTZ]] | traction:graduated | ~$87,634 | reply0 / KOL0（全期間） | 数窓（~11h） | mcap枯れ($6,832・peak比-92.2%) | multi-mint最強版も死亡——redacted_noah association marketing × traction0 × real_sol 82.6SOL ありでも崩壊（high real_sol ≠ 生存保証・multi-mint 3本全滅コホート完成） |
| [[$MYAUR]] | traction:graduated | ~$94,735 | reply0 / KOL0 | 誕生即死（~23分） | mcap枯れ($1,606・peak比-98.3%) | 独自命名×social整備済×traction0→23分死亡（birth 13:34Z・death 13:57Z・同一セッション内崩壊・graduated-but-empty 最短死亡候補） |
| [[$OVERTONWINDO]] | traction:graduated | ~$109,356 | reply0 / KOL0（全期間） | 3窓+突然崩壊（~3h） | mcap枯れ($1,265・peak比-98.8%) | 政治概念命名×traction0×3窓下落鈍化→突然崩壊——「下落率縮小≠底打ち」確認事例（[[external-event-to-token-pattern]]） |
| $PLTA(3PZY1S) | traction:graduated | ~$1,264 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($1,262) | traction無しの即死（ultra-low peak・Paletta命名・entity作成スキップ） |
| $BBL(2S6rEj) | traction:graduated | ~$2,073 | reply0 / KOL0 | 誕生即死(birth=death) | mcap枯れ($1,839) | "Bitcoin bubble"命名×PeterSchiff tweet association marketing×traction0→即死（ultra-low peak・entity作成スキップ） |
| [[$GIRLS]] | traction:graduated | ~$109,093 | reply0 / KOL0（全期間） | ~51分（birth=13:57→death=14:48） | mcap枯れ($1,563・peak比-98.6%) | real_sol 82.9SOL 最高水準でも KOL/traction0→崩壊——⑬「high real_sol ≠ 生存保証」N=2確定（$FINLEY 82.6SOL→-92.2%と並ぶ同サイクル事例）|
| [[$PAWS]] | traction:graduated | ~$174,072（初窓・1窓最高） | reply0 / KOL0（全2窓） | 2窓（初窓+143.8%→翌窓-99.0%） | mcap枯れ($1,675・peak比-99.0%) | 単窓pump→翌窓即崩壊（animal/pet フロー増テーマ初候補×traction0×1窓+143.8%→翌窓-99.0%崩壊・SHAK/GTT 型最速版。フロー量増加 ≠ トークン survival の実証） |
| [[$BUCK]] | traction:graduated | ~$71,802 | reply0 / KOL0（全期間） | 短期(~1日以内) | mcap枯れ($1,313・peak比-98.2%) | graduated-but-empty × real_sol 0——"ONE BUCK"命名×twitter/website整備済×real_sol0→traction0→-98.2%崩壊（$GRUMBLE/$RELAYNET 同型。pool 実流動性ゼロは deployer pump 余地なし=自然枯れ型） |
| [[$HAMA]] | traction:graduated | ~**$2,099,022（コホート最高・全観測最高）** | reply0 / KOL0（全期間・全窓通じゼロ） | 複数窓(~2日) | mcap枯れ($184,059・peak比-91.2%) | BREAKOUT-then-dead 観測史上最大——hamadog.fun 第3 mint×deployer自己pump×peak $2.1M到達×traction0全期間→-91.2%崩壊（$EAGLE250$1.06M/$STARBASE$635k を超えるコホート最高peak traction0崩壊・先行2 mint 全滅でブランド再利用 N=3 全滅確定） |
| $BLANK_USDC(8FgTJN) | traction:mcap>=30000（prebond） | ~$34,338（peak=last） | reply0 / KOL0（twitter=a1lon9 tweet association marketing） | 誕生即死（birth=death 同サイクル） | mcap枯れ($373・peak比-98.9%) | USDC名称偽装×blank ticker×a1lon9 association marketing×prebond死——ticker＝空白文字、name＝"Usdc"のUSDC impersonation scam token。birth同サイクルで死亡。entity作成スキップ |
| [[$SENDY]] | traction:graduated | ~$25,849 | reply0 / KOL0（twitter @sendymission / catsendy.fun） | ~2時間（14:21Z→16:12Z） | mcap枯れ($2,003・peak比-92.3%) | oscillation型 graduated-but-empty（$21k→$25.8k peak→-51%急落→+58%振れ戻し→$2k最終崩壊・cat meme・real_sol 0・$BUCK/$MDT 同型） |
| [[$GOON]] | traction:graduated | ~$391,931（peak・第116窓後） | reply0 / KOL0（全7窓・全期間ゼロ） | 複数窓（~1日） | mcap枯れ($1,361・peak比-99.7%) | 6窓 multi-window T1 momentum 後崩壊（GTT型・鈍化→初下落窓→翌窓-99.6%即崩壊・real_sol 39.9SOL ありでも崩壊・⑬N=3確定追加・"crab rangoooning" food meme × KOL 不在 = traction 未変換の最長追跡例） |
| $SNOWBALL(2G51DJ) | traction:graduated | ~$1,225 | reply0 / KOL0（@tyomateee2 tweet association marketing） | 誕生即死(birth=death) | mcap枯れ($1,225) | association marketing × ultra-low peak → 誕生即死（entity作成スキップ） |
| [[$PBTCSTR]] | traction:graduated | ~$185,843（5窓観測・第115窓天井） | reply0 / KOL0（全5窓） | 5窓（~数時間） | mcap枯れ($1,757・peak比-99.1%) | JOB型確定（横ばい→1窓+67.1%急騰→2窓連続反落→崩壊）× satirical命名("Ponzi BTC Strategy") × Cointelegraph association marketing——「satirical名称 × 外部媒体 association marketing = traction代替にならない」N追加 |
| [[$SLEEPGER]] | traction:graduated | ~$28,084 | reply0 / KOL0（@itsanimalworlds association marketing） | ~数時間 | mcap枯れ($1,307・peak比-95.3%) | graduated-but-empty × association marketing（@itsanimalworlds watchlist外借用）× 命名不明("sleepger") × real_sol 0——$CLO/$LION/$HOOT と同型（watchlist外 association marketing × traction0 → 死亡） |
| [[$REDAWN]] | traction:graduated | ~$9,719 | reply0 / KOL0（twitter/website整備済） | 誕生即死(birth=death) | mcap枯れ($1,838・peak比-81.1%) | low-peak graduated→誕生即死（"redawn"独自命名×social整備済×traction皆無・$AURAFARM/$ALICORN 同型：social整備≠需要） |
| $WENDYGELES(8HELvnM) | traction:graduated | ~$1,190 | reply0 / KOL0（social無し） | 誕生即死(birth=death) | mcap枯れ($1,189・peak比-0.1%) | ultra-low peak誕生即死（peak=last≒コスト圏・entity作成スキップ） |
| [[$GTA-y1Jx8x]] | traction:graduated | ~$458,231（peak・BREAKOUT後） | reply0 / KOL0（全期間・twitter/website無し） | 複数窓（~1日） | mcap枯れ($43,203・peak比-90.6%) | BREAKOUT-then-dead確定（$191k卒業→peak $458k→-90.6%崩壊・acronym転用命名 × social基盤ゼロ × real_sol 72.8SOL ありでも崩壊——⑬ high real_sol ≠ 生存保証 N=4確定追加） |
| [[$SOB]] | traction:graduated | ~$158,060 | reply0 / KOL:badattrading_(wallet分析・sourced) | ~2日（2026-06-24→2026-06-26） | mcap-90%（peak$158k→$15k） | KOL wallet-analysis attention付き BREAKOUT-then-dead——top70=83.2%/Debridge 11.8%⚠️red flag の集中構造が exit 連鎖として表出。KOL分析はリスク可視化ツールであり生存保証でない。association marketing(jncquant tweet team設定) × traction(organic)0 確定 |
| [[$AYAI]] | traction:graduated | ~$216,578（track.py peak） | reply0 / KOL0（全7窓・全期間ゼロ） | 7窓（~2日：2026-06-25→2026-06-26） | mcap枯れ($1,644・peak比-99.2%) | GOON型完全踏襲確認——ay-yai-yai cluster 3本目×near-stale(+8.6%)→初下落(-21.2%)→崩壊(-56%→-99.2%)。real_sol 46.4SOL ありでも traction0→崩壊（⑬N=5追加）。先行2本全滅から誰でも死ぬと読めたクラスター型 |
| [[$ENDRICK]] | traction:graduated（user_checked） | ~$14,576（peak・dead cat bounce複数後） | reply0 / KOL0（全期間） | 複数窓（2026-06-25→2026-06-26） | mcap枯れ($5,981・peak比-59%) | sports-meme × association marketing（matzeraxx tweet 公式設定）× traction0 → dead cat bounce のみで持続不能・枯れ死。Endrick Felipe（ブラジル代表）名義。②「graduated-but-empty」型通り。 |
| [[$MACCA]] | traction:graduated | ~$124,596（多重bounce peak） | reply0 / KOL0（twitter:@ShabbatMonster tweet・GTA VI Macca the Alligator公式IP） | 複数窓・多重dead cat bounce（2026-06-24→2026-06-26） | mcap枯れ($11,742・peak比-90.6%) | GTA VI IP meme（Macca the Alligator公式キャラ）×traction0×多重dead cat bounce（$92k→$37k→$53k→$67k→$124k→$11k）→枯れ死——narrative強度(公式IP)≠crypto traction の実証（[[external-event-to-token-pattern]] GTA wave・$VCSOL/$GTA6Begin/$GTASOLANA 同型N追加） |
| [[$SQUEEZE-9wEUXx]] | traction:graduated | ~$44,755 | reply0 / KOL0（Supermanonchain tweet・finance meme・association marketing） | 複数窓（2026-06-24→2026-06-26） | mcap枯れ($1,181・peak比-97.4%) | duplicate-ticker 2 mint 同時競合（[[SQUEEZE-2Jua7N]]との需要分散）×WSB Short Squeeze finance meme×traction0→資本希薄化崩壊——capital dilution が graduated-but-empty 崩壊を加速した例 |
| [[$DUMPSTR]] | traction:graduated | ~$382,678（raw ATH・多重bounce peak） | reply0 / KOL0（全10+窓・全期間ゼロ） | 10+窓・複数bounce（~3日：2026-06-25→2026-06-26） | mcap -92.8%（peak$382,678→$27,408） | JOB型崩壊→観測史上初V字反転→dead cat bounce DEAD——$130k→raw spike $382k（intra-window）→$125k戻し→第119窓$209k（BREAKOUT）→6h ATH $311k→raw ATH $382k→dead cat bounce（$197k→$89k→$27k）。⑬N=6(real_sol 54.3SOL/-92.8%)。新型「JOB崩壊+V字反転+dead cat bounce→DEAD」実証（[[launchpad-economics]] 跳躍台帳記録済） |
| [[$8 YEARS]] | traction:graduated | ~$106,096 | reply0 / KOL0（twitter:@trondao authority借用） | 誕生即死（birth≒death 同日 2026-06-25） | mcap枯れ($1,736・peak比-98.4%) | authority借用 association marketing（@trondao公式tweet 2本）×real_sol 57.4SOL×traction0→誕生即死（⑬high real_sol ≠ 生存保証N=7追加・TRON 8周年 event meme・$CLO/$LION/$LEEKUANYEW同型：authority借用型N追加） |
| [[$TROLLGELES]] | traction:graduated | ~$45,019 | reply0 / KOL0（twitter/website無し） | 誕生即死（birth=death 同サイクル内） | mcap枯れ($1,334・peak比-97.0%) | traction0 × real_sol 0 × social完全ゼロ × graduated-but-empty → 誕生即死（$REDAWN/$ALICORN/$MYAUR 同型：social基盤ゼロ誕生即死） |
| $GUARDIANS(4xyyYH) | traction:graduated | ~$1,473 | reply0 / KOL0（twitter=WhiteHouse tweet・website=kick.com/ansem 二重 authority borrowing） | 誕生即死(birth=death) | mcap枯れ($1,371・peak比-6.9%) | ultra-low peak × 二重 authority 借用（WhiteHouse + Ansem）→ 即死（entity作成スキップ） |
| $BWICK(2xy2oaG) | traction:graduated | ~$3,385 | reply0 / KOL0（twitter:@bwickdotfun/website:bwick.fun） | 誕生即死(birth=death) | mcap枯れ($2,044・peak比-39.6%) | ultra-low peak 誕生即死（entity作成スキップ） |
| [[$RUSTON]] | traction:graduated | ~$47,111 | reply0 / KOL0（@RustonDev/ruston.fun整備済） | 短期(~1日) | mcap枯れ($1,309・peak比-97.2%) | graduated-but-empty（dev命名×社会需要ゼロ・$FOLK同パターン候補との対比）|
| [[$WEN-66pQgf]] | traction:kol(badattrading_) | ~$1,144,820 | reply0 / KOL:badattrading_(wallet分析・sourced) | 複数日（2026-06-24→2026-06-25） | mcap -90%（peak$1,144,820→last$110,750） | 構造クリーン(top10=15.7%分散×CEX funded 58.5%)×KOL wallet-analysis attention×WSB external-event meme→最終崩壊。有機的traction発生ゼロのまま $1M超到達→死亡——構造クリーン≠生存保証・KOL wallet-analysis attention≠生存保証（$SOBと同結論・構造は異なる N追加）。[[external-event-to-token-pattern]] WSB/株式ネタ型でorganic traction未転換の実証 |
| [[$KOG]] | traction:graduated | ~$1,676,214（raw ATH） | reply0 / KOL0（全14窓・全raw poll ゼロ） | 14窓（2026-06-25・~8h観測）| mcap -98.3%（raw ATH $1,676,214→last$28,070） | **全観測唯一：T3ゼロ14窓×$1.6M+峰→崩壊**——KOL沈黙×4度GOON型逸脱×multi-cycle oscillation→最終崩壊。外部需要源（whale/MM）不明のまま終了。KOL不在でも $1M+到達可能だが同時に KOL不在なら崩壊もする実証（generalize不可の例外事例）。[[launchpad-economics]] 跳躍台帳記録済 |
| $MBGA(AfQtxV) | traction:graduated | ~$8,845 | reply0 / KOL0 | 誕生即死（birth=death 同サイクル内） | mcap枯れ($2,285・peak比-74.2%) | MAGA-derivative meme×traction0×website/twitter低品質→誕生即死（entity作成後即死・ultra-low peak） |
| [[$FCKED]] | traction:graduated | ~$51,598 | reply0 / KOL0（全期間） | 短期(~1日・2026-06-25→26) | mcap枯れ($5,759・peak比-88.8%) | BREAKOUT-then-dead（初動+45%→-76%→dead cat bounce+51%→最終崩壊）×expletive meme×real_sol 0——dead cat bounce 後の最終崩壊まで T3ゼロ継続（$JALAPEÑO/$WENS と同型：bounce後崩壊確定型） |
| [[$PRIME]] | traction:graduated | ~$31,010 | reply0 / KOL0（全期間） | 誕生即死（birth=death 同サイクル内） | mcap枯れ($3,315・peak比-89.3%) | graduated-but-empty 誕生即死（"Prime Rush" gaming命名×twitter/website整備済×traction0→-89.3%即死・$GRUMBLE/$AURAFARM/$RELAYNET 同型：social整備≠需要） |
| [[$MEEP]] | traction:graduated | ~$170,471 | reply0 / KOL0（@tronoffone association marketing疑い） | 数サイクル（~2日） | mcap枯れ($15,378・peak比-91.0%) | BREAKOUT-then-dead確定（+259%BREAKOUT→-91%崩壊・cat meme×association marketing疑い×traction0継続・[[launchpad-economics]]跳躍台帳記録済） |
| [[$RIFICA]] | traction:graduated | ~$26,375 | reply0 / KOL0（twitter/website整備済） | 数サイクル(~1日) | mcap枯れ($1,946・peak比-92.6%) | graduated-but-empty（exchange風命名×rifica.exchange×real_sol 0×traction0→-92.6%崩壊・$RELAYNET/$GRUMBLE 同型） |
| [[$PBB]] | traction:graduated | ~$17,619 | reply0 / KOL0（twitter/website整備済） | 誕生即死（birth=death相当） | mcap枯れ($1,822・peak比-89.7%) | Pokemon IP借用×traction0→即死（PokeBattleBet・pokebb.xyz整備済・IP参照命名≠traction代替・$VCSOL/$LEGACY 同型） |
| [[$CLAY]] | traction:graduated | ~$56,767 | reply0 / KOL0（twitter/website整備済） | 誕生即死（birth=death同サイクル内） | mcap枯れ($1,295・peak比-97.7%) | traction0×real_sol 0→誕生即死（CLAY 汎用命名・social整備済でも community需要ゼロ・$RELAYNET/$MYAUR/$TROLLGELES 同型） |
| [[$ANGIE]] | traction:graduated | ~$22,211 | reply0 / KOL0（creator social only・watchlist外） | 複数サイクル(~2日) | mcap枯れ($4,993・peak比-77.5%) | graduated-but-empty（quirky meme "The Trash Can Bandit"×website=X search placeholder×traction0→縮退死） |
| [[$PEPONK]] | traction:graduated | ~$24,560 | reply0 / KOL0（Telegram整備済） | 誕生即死（birth=death同日） | mcap枯れ($1,311・peak比-94.7%) | graduated-but-empty（PEPONK独自命名×Telegram整備済×real_sol 0×traction0→即死） |
| [[$WEN-5xHMRX]] | traction:graduated+kol_ticker(CA未確認) | ~$206,334 | reply0 / KOL0（CA確認ゼロ・kol_ticker ticker言及のみ） | ~2日(多窓) | mcap -90%($20,342・peak比-90.1%) | BREAKOUT-then-dead（WSB Wendy's Co 後発multi-mint×BREAKOUT×traction0→peak$206k→-90.1%崩壊・[[$WEN-66pQgf]]と同ブランド両mint崩壊確定） |
| [[$BMIND]] | traction:graduated | ~$109,975 | reply0 / KOL0（@blackminddev dev整備済） | 誕生即死(~20分) | mcap枯れ($1,965・peak比-98.2%) | graduated-but-empty超速即死（AI命名×dev twitter整備済×traction0→約20分-98.2%崩壊・コホート最速クラス・$VCSOL/$WORLDCRAFT同型の極端版） |
| [[$KOTON]] | traction:graduated | ~$73,688 | reply0 / KOL0（twitter無し・website koton.fun） | 誕生即死（birth=death 同サイクル内） | mcap枯れ($1,295・peak比-98.2%) | graduated-but-empty誕生即死（独自命名×twitter無し×real_sol 0×traction0→-98.2%崩壊・$TROLLGELES/$MYAUR/$CLAY 同型：social基盤ゼロ誕生即死） |
| [[$背手负鼠]] | traction:graduated | ~$42,555 | reply0 / KOL0（Grok公式tweet association marketing・中国語ticker） | 数窓（2026-06-25→2026-06-26） | mcap枯れ($5,627・peak比-86.8%) | authority借用型 graduated-but-empty（Grok tweet association marketing × traction0 × real_sol 0→縮退死・$AY YAI YAI/$LEEKUANYEW/$CLO 同型：Grok/Elon 権威借用N追加） |
| [[$PENISPUMP-9xP6dK]] | traction:graduated | ~$35,077 | reply0 / KOL0（GoFundMe viral gag・multi-mint下位） | 数窓（2026-06-26・dead cat bounce後） | mcap枯れ($5,924・peak比-83.1%) | multi-mint競合下位→dead cat bounce+101%→最終崩壊（GoFundMe gag残需要が dead cat bounce を生成後に枯れ・real_sol 0・iuv59R mint に需要集中） |
| [[$TRUTH]] | traction:graduated | ~$111,395 | reply0 / KOL0（@thetruthvirus1・thetruth.live整備済） | 誕生即死（~20分・birth=death同セッション内） | mcap枯れ($1,637・peak比-98.5%) | graduated-but-empty超速即死（THE TRUTH conspiracy meme×twitter/website整備済×traction0→~20分-98.5%崩壊・$BMIND同型：超速即死コホートN追加） |
| [[$HODL]] | traction:graduated | ~$354,405（peak） | reply0 / KOL0（@HODLCoinX・hodlsol.life整備済・全11窓） | 11窓（multi-cycle oscillation・数時間） | peak比-97.6%($8,551) | **振動減衰型multi-peak崩壊**（down振幅 -23%→-27%→-32% エスカレート＋up振幅 +67%→+31% 縮小→dead cat bounce+37%→第2波崩壊・$DUMPSTR末期同型・crypto定番ミーム ticker "HODL" × social整備済 × T3ゼロ全11窓 → peak $354k から -97.6%）。⑯**振動減衰型multi-peak崩壊の典型例として台帳追加** |
| [[$FITNESS]] | traction:kol(badattrading_・bundled確認) | ~$885,718（peak・artificial bundled） | reply0 / KOL0（twitter/website無し・badattrading_ 早期警告） | 数日（2026-06-24→06-26） | peak比-92.9%($62,973) | **bundled scam 型崩壊**（badattrading_ が "buy するな" 警告→崩壊継続確認・twitter/website ゼロ × bundled構造 × T3ゼロ = artificial peak → 長期崩壊型。peak $885k はコホート高値級だが artificial mcap の実証）。⑰**bundled scam 警告後の長期崩壊パターン追加** |
| [[$AYAYA]] | traction:graduated | ~$198,709（peak） | reply0 / KOL0（@ayaya_sol整備済・全16窓） | 16窓（dead-cat bounce後崩壊） | mcap枯れ($2,246・peak比-98.8%) | **dead-cat bounce崩壊型**（3窓連続プラス加速→翌窓-98.4%即崩壊・AY系クラスター6/6全DEAD完結・T3ゼロ全16窓：graduated×social整備済×T3ゼロ→崩壊）。⑱AY系クラスター完結（ay yai yai・AIAIAI・AYA・AYY・AYAI・Ayaya 全6本：anime reaction meme × T3ゼロ全滅） |
| [[$STARSHIT-CYZN5P]] | traction:graduated | ~$4,637（peak=last） | reply0 / KOL0（Elon直接URL設定・multi-mint最下位） | 1窓以下（誕生即死） | mcap枯れ($4,637・peak<$10k) | Elon tweet authority借用 × multi-mint最下位 × peak<$10k → 誕生即死（[[$背手负鼠]]/$RO 同型・authority借用型 N追加） |
| [[$POKÉBALL]] | traction:graduated | ~$49,424（peak） | reply0 / KOL0（@PlayPokeball・pokeballgame.online整備済） | 数窓（+61%まで上昇後崩壊） | mcap枯れ($1,325・peak比-97.3%) | Pokemon IP borrowing × traction0 → graduated-but-empty崩壊（$PBB -89.7%/$VCSOL 同型・IP借用型 N追加：Pokemon ブランド借用 ≠ community 需要） |
| [[$STARSHIT-5zzAWB]] | traction:graduated | ~$12,650（peak） | reply0 / KOL0（Elon tweet参照・multi-mint下位） | 数窓（birth→縮退死） | mcap枯れ($2,861・peak比-77.4%) | Elon association marketing × multi-mint下位 → 縮退死（[[$STARSHIT-CYZN5P]] 同セッション死・[[$STARSHIT]] AomWJrRu主力mintへの需要集中で下位mint消滅・multi-mint競合崩壊型） |
| [[$SCOOREX]] | traction:graduated | ~$40,687（BREAKOUT peak） | reply0 / KOL0（twitter無し・website scoorex.lol） | 数窓（birth直後BREAKOUT→崩壊・2026-06-26） | mcap枯れ($1,639・peak比-96%) | birth直後BREAKOUT×traction0 → whale single pump → BREAKOUT-then-dead型（$WENS/$MOONLAKE/$TOROS同型・traction0 BREAKOUT即死 N追加） |
| [[$TRASHCAN]] | traction:exited(post-exit) | ~$1,144,649（post-exit deployer pump ATH・tracking ATH $258k の4.4倍） | reply0 / KOL0（NY Post URL association marketing・T3ゼロ20窓超） | 多窓（traction_candidates 19窓 + post-exit oscillation 数時間・2026-06-25→06-26） | mcap枯れ($6,233・peak比-99.5%) | **post-exit deployer pump 崩壊型最大例**（T3ゼロ19窓→list exit後 deployer pump $1.14M ATH → oscillation（$168k底→反発繰り返し）→最終崩壊-99.5%・$STARBASE⑪同型：post-exit pump 高 peak ほど崩壊落差も大きい）。⑲ post-exit deployer pump コホート最大 peak 更新 |
| [[$arm]] | traction:graduated（mcap>=30k→3窓加速GOON型BREAKOUT） | ~$306,557（ATH・9窓目） | reply0 / KOL0（全12窓・全期間ゼロ） | ~12窓（2026-06-26・大振幅往復後崩壊） | mcap枯れ($4,616・peak比-98.5%) | DUMPSTR型V字ATH更新後最終崩壊——3窓加速→天井$289k→5窓崩壊-67%→2nd BREAKOUT+117%→ATH $306k更新→+3.4%鈍化→-73%→-92.6%→枯れ。KOL不在の大振幅往復型・ARM.exe tech命名。⑬high real_sol ≠ 生存保証は関係なし（real_sol 0）。DUMPSTR型確定追加 |
| [[$MINE]] | traction:graduated | ~$124,651（初検知） | reply0 / KOL0（全7+窓・全期間ゼロ） | ~7窓（2026-06-26） | mcap枯れ($2,057・peak比-98.3%) | dead cat bounce崩壊型——急落(-32.2%)→反発(+23.3%)→鈍化(+3.2%)→停滞(+1.1%)→崩壊再突入(-20.8%)→加速崩壊(-48.2%)→枯れ。MineTown Minecraft連想命名×social整備済(twitter/web)×traction0→dead cat bounce経由消滅（$FCKED/$JALAPEÑO 同型：bounce後崩壊確定型） |
| [[$PURRSUN]] | traction:graduated | ~$1,289（peak=birth） | reply0 / KOL0（@Purrsuncoin・purrsun.top整備済・real_sol 0） | 誕生即死（birth=death同セッション内） | mcap枯れ($1,289) | graduated × peak<$2k 誕生即死（cat/sun meme命名×social整備済×real_sol 0×peak$1,289→birth時点で既DEAD圏・$PEPONK/$KOTON同型：超低peak帯コホートN追加） |
| [[$凪ちゃん]] | traction:graduated | ~$99,005（peak・birth直後+79%急騰） | reply0 / KOL0（livedoor news tweet参照・@Persennt発信点・real_sol 0） | 誕生~20分即死（birth$55k→peak$99k→death$3.8k） | mcap枯れ($3,778・peak比-96.2%) | livedoor news authority借用 × 日本語ticker × traction0 → 急騰後即死（外部メディア記事meme化が crypto community に伝播せず・$背手负鼠 同型：authority借用型N追加。birth+79%急騰は organic でなく deployer pump疑い） |
| [[$STARSHIT]] | traction:graduated | ~$112,441（peak） | reply0 / KOL0（Elon tweet association marketing × multi-mint競合・tokenized_agent=true・全期間ゼロ） | 複数窓（birth→縮退死） | mcap枯れ($11,235・peak比-90.0%) | Elon tweet authority借用 × multi-mint主力mint最終崩壊——[[$STARSHIT-5zzAWB]]・[[$STARSHIT-CYZN5P]] 三兄弟全DEAD完結。tokenized_agent=true ラベルも需要を生めず（authority借用型N追加） |
| [[$SORROW]] | traction:graduated | ~$44,531（peak=birth） | reply0 / KOL0（@sorrowclownsol・sorrowclown.lol整備済・real_sol ~84.622SOL） | 誕生即死（birth$44.5k→death$1.5k・~20分） | mcap枯れ($1,472・peak比-96.7%) | graduated × real_sol高（~84.622SOL） × social整備済でも traction0 → 誕生即死。⑬ high real_sol ≠ 生存保証 N追加（clown meme 命名・real_sol池があっても organic buyer ゼロなら即崩壊） |
| [[$BTC-HZRnhP]] | traction:graduated | ~$125,748 | reply0 / KOL0（kol_ticker=Bitcoin普通言及・kol_ca空） | 数時間（birth=death同日） | mcap枯れ($1,589・peak比-98.7%) | ticker詐称型 graduated-but-empty（"Buy The Cycle"×BTC ticker impersonation×real_sol 0×traction0→-98.7%崩壊。kol_ticker noise ≠ CA support の実証） |
| $SEABORN(Edp7xQ) | traction:graduated | ~$1,360(peak=last) | reply0 / KOL0（@SeabornSolana/seaborn.fun整備済・real_sol 0） | 誕生即死 | mcap枯れ($1,359) | traction無しの即死（social整備済でも organic 需要ゼロ × ultra-low peak × entity作成スキップ） |
| [[$PIXELVILLE]] | graduated(complete=true) | ~$127k(10窓目) | reply0 / KOL0（全13窓） | 13窓(~4h) | mcap枯れ($1,490・-98.6%) | traction0 bubble振動型——social/bonding整備済×13窓oscillation(底→反発→検知時奪還→崩壊)×KOL不在→reflexivity点火失敗実証（[[reflexivity]]）|
| [[$FREEIRAN]] | traction:mcap>=30000（prebond） | ~$133,192（peak=birth） | reply0 / KOL0（PIGGYTOLLAH命名・twitter/website無し） | ~80分（birth 08:42Z→death 10:02Z・prebond消滅） | mcap枯れ($543・peak比-99.6%) | 政治meme × prebond × traction0 → 即死（反イランイスラム共和国 FREEIRAN+PIGGYTOLLAH命名 × social基盤皆無 × bonding curve 未卒業 → 80分で-99.6%崩壊。$LEBRON23/$JOB 同型：外部イベント命名 ≠ traction 代替）|
| [[$CORA]] | traction:graduated | ~$48,642（peak=birth） | reply0 / KOL0（@cora_current/coracurrent.top整備済・real_sol=0） | 誕生即死（birth 10:01Z→death 10:23Z・約22分） | mcap枯れ($1,412・peak比-97.1%) | graduated × real_sol=0 × social整備済 × traction0 → 誕生即死（"Cora Current"独自命名 × KOL不在 × real_sol=0 → 需要ゼロで約22分崩壊。$PURRSUN/$AURAFARM 同型：social整備済でも organic需要ゼロ = 即死）|
| [[$R-MSB]] | traction:graduated | ~$59,202（peak） | reply0 / KOL0 | 1窓（~21分・birth 10:45Z→death 11:06Z） | mcap枯れ($5,691・peak比-90.4%) | WSB/Reddit parody × real_sol 0 × traction0 → 1窓内消滅（r/MemeStreetBets・WSB命名≠traction代替・$CORA同型：real_sol 0 誕生即死型N追加） |
| [[$PUNANI]] | traction:graduated | ~$130,472（V字反転peak） | reply0 / KOL0 | 3窓（~45分・birth 10:01Z→death 10:46Z） | mcap枯れ($1,421・peak比-98.9%) | 初下落→V字反転(+34.6%)→即崩壊——real_sol ~51.4SOL × traction0 × 俗語命名 → 3窓-98.9%崩壊（⑬high real_sol ≠ 生存保証 N追加・「V字反転=survival signal」ならない実証） |
| $BYTEAPE(CJiGAM) | traction:graduated | ~$1,685（peak=birth=death） | reply0 / KOL0（@BYTEAPESOL/byteape.online整備済・real_sol 0） | 誕生即死（birth=death同サイクル） | mcap枯れ($1,610) | ultra-low即死——BYTEAPE命名 × $1.7k peak × social整備済でも organic需要ゼロ（entity作成スキップ・$SEABORN同型） |
| [[$STARS]] | traction:graduated | ~$178,131（ATH・10窓目） | reply0 / KOL0（全15窓・reply:0全期間） | 15窓（~4h+・振動型多サイクル） | mcap枯れ($1,556・ATH比-99.1%) | traction0 bubble振動型DEAD——@SolTrenchStars/playtrenchstars.fun整備済 × real_sol 46.4SOL × 15窓で6度急騰急落繰り返し（$160k→$98k→$178k→$97k→$1.6k）× KOL不在→最終崩壊。[[reflexivity]] 点火条件未達型確定。⑬ real_sol 46.4SOL ≠ 生存保証 N追加・[[PIXELVILLE]] 15窓版 |
<!-- death-ledger: 以降 synthesize.sh が追記。古い順に貯める。 -->

**現時点で浮いている型（N=159 確定死亡・2026-06-26 更新）**: ⑳**誕生即死（~22分）・real_sol=0**（[[$CORA]]）——graduated × social整備済 × real_sol=0 × traction0 → 22分即死。独自命名の community 引力ゼロ確認。⑬**high real_sol ≠ 生存保証**（[[$FINLEY-7rANTZ]] 82.6SOL→-92.2% / [[$GIRLS]] 82.9SOL→-98.6% / [[$GOON]] 39.9SOL→-99.7% / [[$GTA-y1Jx8x]] 72.8SOL→-90.6% / [[$AYAI]] 46.4SOL→-99.2% / [[$DUMPSTR]] 54.3SOL→-92.8% / [[$8 YEARS]] 57.4SOL→-98.4% / [[$STARS]] 46.4SOL→-99.1% ATH比）——pool に大量 SOL が入っていても KOL/traction ゼロなら崩壊・N=8 確定（$STARS は 15窓 traction0 bubble 振動型でも最終崩壊）。⑮**KOL wallet-analysis attention ≠ 生存保証**（[[$SOB]] / [[$WEN-66pQgf]]）——$SOB: top70=83.2%/Debridge⚠️ 集中構造 exit 連鎖→-90%崩壊（集中リスク起因）。$WEN-66pQgf: 構造クリーン(top10=15.7%分散)でも traction(有機的)ゼロのまま $1M超→-90%崩壊。構造クリーン・集中どちらでも「KOL wallet-analysis attention ≠ 生存保証」N=2確定。⑭**誕生~23分死亡**（[[$MYAUR]]）——birth=death 相当の超短命事例（social整備済の independent naming でも traction0 は防げない）。⑪**post-exit deployer pump → 高peak → 崩壊**（[[$STARBASE]] peak $635k -99.5%）——list exit後に deployer 自己資金で pump し ATH を更新しても KOL/community ゼロなら最終崩壊（$ABUSE 同型の高peak版・コホート最高 peak 級）。⑫**DeFi generic ticker縮退死**（[[$TOKEN]] sTokens -88.1%）——generic DeFi ticker + traction0 の多窓縮退死パターン。①**traction(reply/KOL)ゼロ × 出来高先行**で上げた銘柄は死にやすい——**確定死亡 N=53**（N=52 前回 + AYAYA の1件）。⑱**dead-cat bounce崩壊型**（[[$AYAYA]]）——3窓連続プラス加速後に翌窓-98.4%即崩壊・AY系クラスター6/6全DEAD完結（anime reaction meme × T3ゼロ全期間 → dead-cat bounce を「回復」と誤認させて崩壊）。⑦**BREAKOUT-then-dead の association marketing 確定例**（$TOROS）——Toros Finance DeFi ブランド借用 × traction0 で BREAKOUT → 3窓12h で peak比-98.4%崩壊。⑩**BREAKOUT-then-dead 最新例**（[[$WENS]]）——peak $115k まで traction ゼロのまま上昇→peak比-98.7%崩壊（N追加）。⑧**generic name squatter 量産コホート**（$HI×3+$HI-UZWrgk）——generic ticker の多重 mint は高 peak（$46k）でも peak 比 -99.7% で死ぬ実証（peak mcap 高低によらない）。⑨**同ブランド再登場即死**（[[$VORTEX]] 2例）——同一 VortexDeployer.com ブランドが mint を変えて再登場しても community 需要がゼロのまま同水準で死亡；ブランド名の再利用が traction を呼ばない N=2 実証。⑤**KOL 言及あり誕生即死**（$RONALDINU/$BBQ）——KOL gate 通過 ≠ community 追随の実証。⑥**T1-only の上限実証**（$BABYFACE:4窓/$COVER:15窓）——KOL ゼロで到達可能な momentum の天井（$267k〜$289k）を N=2 で可視化。**$MAYHAM コホート全滅**（D5Gqvj $421 / 5pP5vo $163 / 3vpeyAb $107 / AWchjc pending）——4 mint 同名で3本確定死亡・最低 peak $107 は観測史上最低水準候補。他は全件 reply0/KOL0 のまま死亡＝「traction の不在」が死の先行指標として型化（⚠️ 同一コホート・同一時間帯の観測で独立性は限定的）。②graduated でも KOL ピックアップ無し＝「graduated but empty」型（[[launchpad-economics]]）が主流死因。③**traction-less BREAKOUT → 即死**（$MOONLAKE/$PHONEBLACK/$TOROS/$WENS・N=4）——BREAKOUT が社会的需要を生まない実証が N=4 に強化。④誕生即死量産型（$EYEZ/$JAKE/$SLICK/$MAYHAM）は型通りにつき1行記録のみ。

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
