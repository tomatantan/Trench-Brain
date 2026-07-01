---
type: concept
title: 型 — launchpad 経済圏（Pump.fun / $PUMP＝memeの供給工場）
created: 2026-06-22
updated: 2026-07-01
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
外部主張だけでなく、自前の観測でも同じ型が出る。base rate（2026-06-24 時点・累計、`brain/state/base_rate.json` と同期）= **mints 観測 11,717 / 門通過 92（0.78%）/ graduated 70 / 死 42**（外部 1.5% との差は方法論差＝注記）。
- **「graduated but empty」型が観測の主流**: 通過銘柄の大半が *graduation 済みなのに reply 0・KOL 言及ゼロ*。出来高だけ先行し社会的 traction が伴わない。
  実例コホート（同一バッチ）: [[$MOONLAKE]]（AI・dead -96.8%）/ [[$VCSOL]]（GTA参照・dead -99%）/ [[$AXIOS]]（DeFi冠・dead -96%）/ [[$MOTION]]（$187k・watch中）/ [[$AEGIS]]（privacy・$27k）/ [[$RO]]。
- **追跡で型が裏付いた（2026-06-23 確定）**: [[$AXIOS]]/[[$VCSOL]]/[[$MOONLAKE]] が同コホートで -96%〜-99% に達し**dead 確定**。「KOL pickup なし＝短命」仮説が **N=3** の観測で強化（[[rug-anatomy]] 死亡台帳を参照）。98.5%死亡母集団の動態をリアルタイムで捉えている。
- **prebond 観測（未 graduation・勢い門 mcap で通過）**: [[$MEW2]]（Pokemon IP・$47k）/ [[$GOOSE]]（animal・$90k）＝bonding curve 上で出来高だけ立った初期銘柄。graduation か死かを watch＝分母の入口側。
- **含意**: graduation は生存の十分条件ではない。**graduation × (reply/KOL traction)** が [[survivor-memes]] の足切り。traction を欠く graduate は死の分母に算入する前提で見る（これが生存者バイアス対策の実装）。

## ★Feedback 実測（型の hit-rate・2026-06-24・[[feedback]] `brain/feedback.py`）
観測コホート＝門通過 92件（うち gate/traction 分類済 89件、残は分類待ち）に育ち、型が**数字で**裏付いた（[[feedback]] が tracked.json の実 outcome を採点。以下 N は分類済 89 基準）：
- **gate別 死亡率に明確な差**: **graduated門 75%（37/49）死** vs **mcap勢い門 13%（3/22）** vs other 11%（2/18）。
  ＝**"graduated-but-empty" が最も死ぬ**（卒業≠生存を数字が強く支持）。勢い門通過(社会的traction/mcap勢い)は相対的に生存。
- **traction が生存を分ける（N増で反転・確定寄り）**: **traction有り 死12%（2/17）** vs **traction無し 死55%（40/72）**。
  ＝初期(N=4)は「差なし」だったが、対照群が育ち **traction(KOL/reply)有りは死亡率が約1/4** に。[[survivor-memes]] の「traction足切り」を実測が支持。
- ⚠️ 留保: 母集団は同一launchpad・近時間帯で独立性低・現mcap近似。だが gate差(75% vs 13%)は大きく型として頑健。
- 含意（賭け）: **"graduated・traction無し" は最強の死signal**（/check が avoid に振る根拠）。逆に **mcap勢い門通過 × KOL/reply traction** が相対的 survivor 候補＝[[manipulation-playbook]] で手口を除外した上で見る。

### gate の late-entry バイアス（upside 天井の研究・2026-07-01・N=20 vs 86）
- **仮説**: `traction:mcap>=30000` gate（客観 MCAP 閾値で捕捉）で入った銘柄は peak mcap $200k 未満に収まる。早期 gate（KOL/graduated/user_checked）には $200k+ が複数存在する。
- **検証**: mcap>=30000 群 N=20（dead 3 / tracked 17）、早期 gate 群 N≈86（dead 67 / tracked 19）
  - mcap>=30000 群: **$200k+ = 0/20 件**。最大 $MBAPEPE/$CHIBUL 各 $154k。
  - 早期 gate 群: $200k+ 複数確認——dead では $TOGI(407k)/$BECKER(327k)/$DOGPLANE(300k)/$$SUNBULL(119k) など、tracked では $JOTCHUA(11.1M)/$TESTIBULL(2.5M)/$BELMAR(2.2M)/$ZERO(3.1M)/$滑る猫(972k)/$BITBOY(488k)/$WEN(235k)。
- **判定**: **確証**（0/20 vs 多数、完全分離）
- **含意（gate 設計への示唆）**: mcap>=30000 gate は「$30k 到達後に初めて捕捉」＝その時点が既に peak 近傍になりやすく、以後の upside 余地が小さい構造的 late-entry バイアスを持つ。**「大きく跳ねる（$200k+）」銘柄は KOL/graduated/user_checked いずれかで早期に捕捉されている**。mcap>=30000 gate の役割は「見落とし防止（安全ネット）」であり、主力 upside 発掘には使えない。

### dead floor 構造（2026-07-02・N=16）
- **仮説**: dead 銘柄（pump-dump 型：peak >= $50k）の floor（cur 値）は peak mcap の大きさと無相関。peak $60k の死も peak $400k の死も dead 後の cur 中央値は同じ $1.5k 前後に収束する。
- **検証**: dead かつ peak >= $50k の銘柄 N=16 を2グループ（$50k-$150k: N=13, $150k+: N=3）に分け cur 中央値を比較。
  - Group A（$50k-$150k）中央値: **$1,686**（$FLARO $1,503 / $MOONSEM $1,498 / $RICHES $1,686 / $SUNBULL $2,230 等）
  - Group B（$150k+）中央値: **$1,485**（$DOGPLANE $1,485 / $BECKER $1,462、外れ値 $TOGI $32,421 を除くと $1,473）
  - 全 N=16 中央値: **$1,596**。peak 6x 差（$60k vs $400k）があっても floor 中央値は誤差レベルで一致。
  - $1.3k-$3k 帯への収束: 16 件中 10 件（62.5%）が floor 帯に落ち着く。外れ値（$TOGI/$DEADSEM/$ORANGIE2/$🐂🀄）は半死状態か別流動性源の可能性。
- **判定**: **不確定（方向あり・N 小）** — 中央値の一致は仮説を支持するが N=16・外れ値複数で確証不十分。
- **含意（early-dead 判断への活用）**: platform floor が $1.5k 付近に構造的に存在するなら、「cur $3k 以下かつ前回比下落継続」＝floor フェーズ入り＝実質 dead の早期判断シグナルになりうる。pump 幅（peak）でなく platform の最低 LP 残留・bonding curve 清算後の構造が floor を決めている仮説と整合。N 増で再検証。

### peak mcap 規模の予測力（[[predictive-study]] N=99）
- **peak mcap <10k ＝ 死亡率 100%（24/24）**＝最も clean な死signal。小peakは mcap勢いが立たず事実上全滅＝/check は「peak/現mcap が極小」を強い avoid に。
- 10-50k 42% → 50k超は概ね 23-25%＝**規模が立つほど(=社会的需要の代理)生存率上昇**。但し >1M でも 25%死＝大型でも安全でない。
- **死は崩落**: dead 銘柄の平均 drawdown **-47.8%**（多くは-90%超）＝"fading だから様子見"は通用せず**早期判定**が要る。
- 経験的重みは `brain/state/risk_weights.json`＝/check が単純照合でなく **lift付き予測** に使う。詳細 [[predictive-study]]。

## auto-track 跳躍台帳（大きく跳ねた型を貯めて学習する）
死(→[[rug-anatomy]] 死亡台帳)と対。`brain/track.py` が **BREAKOUT(mcap前回比+100%超) / GRADUATED** を検知する度、
`brain/synthesize.sh` の合成が**跳躍シグネチャを1行追記**する。「跳ねる前に何が見えていたか」の共通項を貯める学習台帳。

| ticker | 跳躍 | mcap 前→後 | traction(reply/KOL) | 前兆/きっかけ | 型/signature |
|---|---|---|---|---|---|
| [[$RO]] | +138% | $5.8k→$13.8k | reply0 / KOL0 | ⚠️ twitterがElon tweetリンク(association marketing偽装) | **traction無し×出来高driven**＝持続性疑問 |
| [[$AEGIS]] | +160% | $29k→$76k | reply0 / KOL0 | 不明(privacyテーマ便乗 or bot買い) | traction0で急騰＝⚠️[[rug-anatomy]] のつり上げ候補 |
| [[$PHONEBLACK]] | +138% | $89.8k→$214.3k | reply0 / KOL0 | 不明(phone-01black.com整備済だが言及ゼロ) | traction0×出来高先行＝$AEGIS/$RO と同型・whale/bot pump疑い |
| [[$MOONLAKE]] | +147% | $415.6k→$1.03M | reply0 / KOL0 | 不明(AI テーマ "Moonlake AI" + moonlake.design 整備済だが有機的言及ゼロ) | traction0×出来高先行＝$AEGIS/$RO/$PHONEBLACK と同型・コホート初 $1M 突破 |
| [[$JOKER]] | +134% | $34k→$80k | reply0 / KOL0 | 不明(JOKER名・twitter/web無し・social起点ゼロ) | traction0×出来高先行＝$AEGIS/$PHONEBLACK/$MOONLAKE と同型・BREAKOUT-then-dead 候補 |
| [[$TOROS]] | +124%（→ピーク+452.5%） | $52.7k→$118k（ピーク$125.6k） | reply0 / KOL0（全3窓） | Toros Finance DeFi ブランド借用（association marketing）・whale 計画的買い | **BREAKOUT-then-dead確定**（association marketing×traction0・3窓12h完結・peak比-98.4%崩壊）—— $MOONLAKE/$PHONEBLACK と同型・association marketing 借用での whale pump が今サイクル初確定 |
| [[$JALAPEÑO]] | +102% | $50.8k→$102.3k | reply0 / KOL0 | 不明(wallstengine trading tweet・website=Axiom DEX pulse) | traction0×出来高先行＝$AEGIS/$PHONEBLACK/$JOKER/$TOROS と同型・BREAKOUT-then-dead 候補 |
| [[$SOB]] | +157% | $13.5k→$34.7k | reply0 / KOL:badattrading_(wallet分析・sourced) | jncquant tweet link(team設定・association marketing疑い)＋badattrading_分析 | KOL attention付き跳躍——top70=83.2%/Debridge⚠️red flag／traction(organic)ゼロ×出来高先行の側面あり・持続性要watch |
| [[$THEBLOOP]] | +208% | $74.8k→$230.2k | reply0 / KOL0 | 不明（深海Bloop meme・twitter整備済・有機的言及ゼロ） | traction0×出来高先行＝$AEGIS/$JOKER/$JALAPEÑO と同型・BREAKOUT-then-dead 候補 |
| [[$WEN-5xHMRX]] | +104% | $61.4k→$125.5k | reply0 / KOL0（badattrading_ ticker言及のみ・CA未確認） | Wendy's Co 後発 multi-mint・WSB ミーム便乗 | KOL CA未確認×後発 multi-mint BREAKOUT → BREAKOUT-then-dead 候補（[[$WEN-66pQgf]] との需要混同） |
| [[$MEEP]] | +259% | $47.4k→$170.5k | reply0 / KOL0（@tronoffone association marketing疑い） | @tronoffone ツイートを公式 twitter に設定・cat meme 命名 | traction0×association marketing疑い×出来高先行 BREAKOUT＝$AEGIS/$JOKER/$JALAPEÑO と同型・BREAKOUT-then-dead 候補 |
| [[$KELL]] | +172% | $26.3k→$71.6k | reply0 / KOL0 | 不明（Kell Phage独自命名・kellphage.com整備済・有機的言及ゼロ） | traction0×出来高先行＝$AEGIS/$JOKER/$JALAPEÑO と同型・BREAKOUT-then-dead 候補 |
| [[$SUPAIAIAI]] | +128% | $55.5k→$126.3k | reply0 / KOL0 | 不明（"aiaiai"=AI命名便乗・twitter/website未整備・有機的言及ゼロ・tokenized_agent=false） | traction0×出来高先行×誕生窓内即BREAKOUT＝$AEGIS/$JALAPEÑO/$THEBLOOP と同型・BREAKOUT-then-dead 候補 |
| [[$KOG]] | +113%（窓間+189.5%） | $75.6k→$161.3k | reply0 / KOL0 | 不明（前窓-33.6%下落から完全逆転・animal meme テーマ・real_sol 0・T3ゼロ2窓） | traction0×下落後逆転BREAKOUT＝⚠️deployer exit pump疑い（real_sol 0 × T3ゼロ2窓継続・$AEGIS/$JALAPEÑO 同型候補。次窓結果待ち） |
| [[$DUMPSTR]] | +214%（raw poll $122k→$382k）/ 6h窓 +60.4%（$130k→$209k） | raw: $122k→$382k / 6h: $130k→$209k | reply0 / KOL0（全期間） | 不明（"Dump Strategy" ironic finance meme・real_sol 54.3SOL・@DumpStrategy整備済・organic言及ゼロ） | **raw poll BREAKOUT＋6h窓BREAKOUT 二重記録——raw poll +214%（第117-118窓 intra-window spike・即戻し $125k）+ 6h窓 +60.4%（第119窓）。real_sol 54.3SOL あり。JOB型「stale→崩壊」後 V字反転（観測史上初）→ raw ATH $382k / 6h ATH $311k（T3ゼロ8窓継続）。whale初期spike + 後続多主体建て直し + 崩壊 + V字反転 の前例なし複合型。** |
| [[$PENISPUMP-iuv59R]] | +126% | $66.4k→$175.0k | reply0 / KOL0（DatDev2026 association marketing・multi-mint競合上位） | GoFundMe viral gag（micropenis enlargement crowdfunding）× traction0（organic） | traction0×multi-mint BREAKOUT——viral meme potential あるも KOL CA未確認・real_sol 0・dead cat bounce候補（$AEGIS/$JALAPEÑO 同型シグネチャ） |
| [[$WETTER]] | +261% | $35.3k→$127.5k | reply0 / KOL0 | 不明（"donner wetter"=ドイツ語感嘆詞・twitter/website無し・有機的言及ゼロ） | traction0×出来高先行×未graduated BREAKOUT＝$AEGIS/$JALAPEÑO 同型・BREAKOUT-then-dead 候補 |
| [[$PENISPUMP-9xP6dK]] | +101%（dead cat bounce） | $6.4k→$12.8k | reply0 / KOL0（GoFundMe gag・multi-mint下位） | dying状態からの反発 | GoFundMe viral gag残需要 or 偶発的buy | dead cat bounce型BREAKOUT（dying状態から+101%・絶対mcap低水準・traction0不変・real_sol 0・上位mint死後の下位mint bounce） |
| [[$PEPONK-4W9nkD]] | +212% | $41.6k→$129.7k | reply0 / KOL0（全期間） | 先行 mint（2LAk8gf）-94.7%即死後の 2nd mint 再発射・同ブランド再登場 | traction0 × 同ブランド 2nd mint BREAKOUT——先行 mint 失敗後でも出来高先行+212% は発生する実証。先行 mint の community 知名度が traction に転化しなかった（reply/KOL ゼロ継続）＝同ブランド再登場 ≠ organic 需要復活。BREAKOUT-then-dead 候補（[[rug-anatomy]] 同型） |
| [[$arm]] | +118%（BREAKOUT） | $138.2k→$301.1k | reply0 / KOL0（全3窓） | 不明（ARM.exe tech命名・armsol.top整備済・traction0全期間・3窓連続加速後） | traction0×出来高先行×GOON型継続——3窓連続加速(+37.6%→+47.8%→+81.3%)後の BREAKOUT検知（$289k→$301k）。KOLゼロの GOON 型はいずれ天井→即崩壊候補（[[$GOON]]-99.7%/$TMB 同型進行中） |
| [[$SCOOREX]] | +336%（BREAKOUT） | $9.3k→$40.7k | reply0 / KOL0 | 不明（SCOOREX独自命名・twitter無し・scoorex.lol のみ・birth直後即BREAKOUT） | birth直後即BREAKOUT×traction0×twitter無し＝whale単独 pump疑い（$AEGIS/$RO 同型）。極短時間4倍は organic 需要ゼロ × 操作/bot買いの典型シグネチャ。BREAKOUT-then-dead 候補最有力 |
| [[$arm]] 2nd BREAKOUT | +117% | $111.6k→$241.9k | reply0 / KOL0（全期間） | dying→$99k nadir→微回復後の 2nd BREAKOUT（5窓崩壊フェーズ中の反発） | **dying後 2nd BREAKOUT**×traction0 → dead cat bounce疑い最有力（1st天井$301kの約80%まで反発・KOLゼロ全期間・GOON型崩壊フェーズ中の whale再買い or 自然bounce）。1st天井超えなら新局面・失速なら崩壊継続確定 |
| [[$RRN]] | +137% | $56.9k→$134.9k | reply0 / KOL0（全期間） | 不明（"buy = rich right now" ironic命名・twitter/web無し・prebond継続・7h後の遅延急騰） | traction0×出来高先行×prebond継続 BREAKOUT＝$AEGIS/$JALAPEÑO 同型・BREAKOUT-then-dead 候補最有力（ironic命名 × social皆無 × prebond継続での$134k到達 = whale単独 pump疑い）|
| [[$MOXIE]] | +120%（BREAKOUT） | $67.5k→$148.7k | reply0 / KOL0（全期間） | 不明（generic sentiment meme "MOXIE"(意欲/勇気)・moxiecoin.top整備済・有機的言及ゼロ・real_sol=0） | traction0×出来高先行BREAKOUT＝$AEGIS/$JOKER/$JALAPEÑO/$THEBLOOP と同型・BREAKOUT-then-dead 候補（birth同キュー内+61%→+120%で2段跳ね・traction伴わず） |
| [[$TURTLE]] | +160%（nadir反転） | $27.5k→$71.5k | reply0 / KOL0（全期間） | 死亡圏($27k nadir)からの V字反転・animal meme "Freaky Turtle"・real_sol=0全期間 | **nadir→BREAKOUT 型**（死亡圏から+160% V字——whale再買い or dead cat bounce疑い最有力。traction0×出来高先行の$MOXIE/$AEGIS 同型。「底打ち偽シグナル」初確定候補） |
| [[$SOL-BUphiK]] | +153% | $25.7k→$65.1k | reply0 / kol_ticker:RookieXBT（⚠️$SOL=Solana本体ティッカー noise・kol_ca未確認） | OpenAI GPT-5.6 Sol発表便乗・multi-mint wave 2nd mint・birth後~1分以内BREAKOUT | **external-event multi-mint BREAKOUT**（traction0×kol_ticker noise×出来高先行——H4CFQn主体mintと同波の下位mint BREAKOUT。BREAKOUT-then-dead 候補（$AEGIS/$JALAPEÑO 同型）） |
| [[$SOL-BUphiK]] 2nd BREAKOUT | +702% | $65.1k→$521.8k | reply0 / KOL CA未確認（kol_ticker noise継続） | H4CFQn主体mint -49%（$258k→$131k）と逆行——波内需要が BUphiK に移行。T3ゼロ継続 | **multi-mint需要逆転 BREAKOUT**（T3ゼロのまま $500k+ 到達。H4CFQnとの需要逆転は deployer 操作 or organic 移行の両義——$arm 2nd BREAKOUT/$KOG 型。peak $522k は[[external-event-to-token-pattern]] wave 最大。BREAKOUT-then-dead 最有力（$EAGLE250/$HAMA 同型水準）） |
| [[$BOO]] | +137%（BREAKOUT） | $137k→$324k | reply0 / KOL0（全期間）・real_sol ~82.7SOL | BooBeat music/EDM 命名・twitter @Boobeat_pump / boobeat.fun 整備済・T3ゼロ全期間 | **real_sol ⑬コホート BREAKOUT**（T3ゼロ継続のまま $324k 到達。real_sol ~82.7SOL = [[rug-anatomy]] ⑬コホート最近似（$FLYRO ~84.4SOL→-98.5% / $GIRLS ~82.9SOL→-98.6%）。deployer pool SOL による人工 pump 疑い最有力。BREAKOUT-then-dead 最有力候補） |
| [[$DNT]] | +156%（BREAKOUT） | $183k→$469k | reply0 / KOL0（全期間）・real_sol=0 | "Death and Taxes" phrase meme・twitter/website 未設定・T3ゼロ全期間・birth $93k→+403% | **traction0 phrase-meme BREAKOUT**（real_sol=0 × social 未設定のまま $469k 到達。T3 ゼロ全期間＝whale/bot pump の可能性高。BREAKOUT-then-dead 最有力候補） |
| [[$BOO]] 2nd BREAKOUT | +119%（2nd BREAKOUT） | $324k→$709k | reply0 / KOL0（全期間）・real_sol ~82.7SOL | BooBeat ⑬コホート 2段 pump——1st $324k 後も deployer SOL 継続・T3ゼロ不変 | **⑬コホート 2段 BREAKOUT**（1st $324k→2nd $709k と 2 波連続。$FLYRO/$GIRLS はこの水準前に崩壊——$700k+ は⑬コホート新高値。T3ゼロ全期間継続中・deployer SOL 消費後の崩壊が焦点） |
| [[$PISS]] | +102%（BREAKOUT） | $161.3k→$326.4k | reply0 / KOL0（全期間）・real_sol=0 | pisscoin vulgar-humor × X community 設定（独立twitter無し）× badattrading_ KOL CA確認済(birth時)・traction0 | **vulgar meme traction0 BREAKOUT**（top10=17.3%・cluster3.4%の構造分散最良クラス × reply:0全期間のまま $326k 到達。deployer pump vs organic vulgar community 両義——次窓の reply/KOL CA 確認が分岐点。BREAKOUT-then-dead 候補（$MOXIE/-92.1%同型）） |
| [[$PEAK]] | +150% | $54.2k→$135.6k | reply0 / KOL0 | 不明（generic 到達感 ticker "PEAK"・twitter/website 両方皆無・prebond 継続・birth 直後~1分以内 BREAKOUT） | birth直後即BREAKOUT×traction0×social皆無×prebond継続＝whale単独 pump 疑い最有力（$AEGIS/$SCOOREX/$RRN 同型。bonding curve 未卒業での $135k は organic 需要ゼロ確定候補） |
| [[$0TT]] | +114% | $40.3k→$86.2k | reply0 / KOL0 | 不明（otter animal meme・@natureunedited 自然映像リンク・prebond継続・real_sol 32M→7.8M と売り圧あり） | traction0 × 出来高先行 × prebond BREAKOUT＝association marketing + real_sol 減少中の whale pump 疑い。$AEGIS/$JALAPEÑO/$SCOOREX 同型・BREAKOUT-then-dead 候補 |
| [[$PEPEBULL]]（The PEPE Bull） | +102%（BREAKOUT） | $39.5k→$79.9k | reply0 / KOL0（twitter/website 両方 null・全期間）・real_sol=5（実質ゼロ） | PEPE×bull 複合命名・prebond 継続・BREAKOUT 時も real_sol≒0 = organic 需要ゼロ確定候補 | prebond traction0 即BREAKOUT×real_sol≒0（whale/bot 単独 pump 最有力。bonding curve 未卒業 × PEPE brand 派生 × real_sol 5 lamports での $80k 到達は $PEAK/$AEGIS 同型——BREAKOUT-then-dead 最有力候補） |
| [[$GUTCHU-GzfBEf]]（GUTCHU 2nd mint） | +106% | $49.3k→$101.3k | reply0 / KOL0（全期間）・real_sol 3.26SOL | birth→BREAKOUT が同一観測バッチ内（超短時間）。prebond 継続。先行同名 mint（DJjg...）が+81% BREAKOUT-then-dead 前例あり | **同名2nd attempt 即BREAKOUT**（先行 mint 死亡後に同名で再 launch → 同バッチで BREAKOUT。traction0 × social 皆無 × real_sol 低値 = whale 単独 pump 最有力。BREAKOUT-then-dead 最有力——先行 mint が同型で死亡済で 2nd attempt でも traction が生まれない場合、3rd 以降も同パスと推定） |
| [[$DEADSEM]] | +301% | $29.8k→$119.4k | reply0 / KOL0（全期間） | 不明（ironic "dead bull" 命名 × X community リンク × real_sol=0 × graduated） | traction0×出来高先行 BREAKOUT×real_sol=0＝$AEGIS/$JOKER/$JALAPEÑO 同型・BREAKOUT-then-dead 候補 |
| [[$TESTIBULL-C6kWVd]] | +2014% | $118.8k→$2.51M | reply0 / KOL0（全期間） | 不明（"testibull" bull cluster 命名 × twitter:DipWheeler × real_sol=0 × graduated × multi-mint 主 mint） | traction0×出来高先行 BREAKOUT×real_sol=0＝$DEADSEM/$JALAPEÑO/$AEGIS 同型・multi-mint 主 mint 需要集中 × whale/bot pump 最有力・BREAKOUT-then-dead 最有力 |
| [[$BELMAR]]（I STUDIED） | +829%（BREAKOUT） | $238k→$2.2M | reply0 / KOL0（全期間）・twitter/website null・real_sol=0 | 不明（social 窓口ゼロ全期間・graduated・$212k birth後さらに上昇） | traction0×出来高先行 BREAKOUT×real_sol=0 = $TESTIBULL/$MOONLAKE 同型・$2M+ 到達も whale/bot pump 最有力・**→dead確定(-98.6%)** |
| [[$TESTIBULL-C6kWVd]] 2nd BREAKOUT | +123%（2nd BREAKOUT） | $1.99M→$4.42M | reply0 / KOL0（全期間）・real_sol=0・DipWheeler twitter | 不明（1st +2014% 後も traction ゼロ継続・multi-mint sibling 即死済・2段連続 pump） | **traction0×2段連続 BREAKOUT×$4.4M**（コホート最高 peak 更新。1st $2.51M→2nd $4.42M。whale/bot ポジション継続の最終 pump 疑い最有力。BREAKOUT-then-dead 最有力——$BOO 2段型の規模拡大版） |
| [[$BITBOY]]（The White Bull） | +265%（BREAKOUT） | $489k→$1.78M | reply0 / KOL0（全期間）・real_sol=0・@BitBoy_TWB / bitboy.meme 整備済 | BitBoy Crypto 名借用（実 @Bitboy_Crypto とは別 CA・⚠️ 非公式）・social 整備あり | **KOL名借用 × social整備 × traction0 BREAKOUT**（website+twitter あっても reply0 全期間のまま $1.78M 到達。$BELMAR（→dead -98.6%）/$TESTIBULL（継続中）と同型水準——BREAKOUT-then-dead 最有力候補） |
| [[$TBB]]（THE BLACKIST BULL） | +323%（BREAKOUT） | $33.6k→$141.9k | reply0 / KOL0（全期間）・real_sol ~9.5SOL・CMC website authority借用 | CMC 他プロジェクトページを website に流用する authority 借用型 × bull-theme × prebond | prebond traction0 BREAKOUT×authority借用×bull-cluster（$TESTIBULL/$BELMAR/$DEADSEM 同型——BREAKOUT-then-dead 最有力） |
| [[$MC]]（Merica Coin） | +118%（BREAKOUT） | $37.6k→$82.1k | reply0 / KOL0（全期間）・real_sol~0・twitter/website 皆無 | 不明（"Merica"=America ironic愛国命名・prebond継続・social 皆無・real_sol=0） | traction0×social皆無×prebond BREAKOUT＝$AEGIS/$JALAPEÑO/$PEAK 同型・BREAKOUT-then-dead 候補 |
| [[$MC]] 2nd BREAKOUT（Merica Coin） | +101%（2nd BREAKOUT） | $82.1k→$165.0k | reply0 / KOL0（全期間・2段全期間ゼロ）・real_sol~0・prebond継続 | 不明（1st BREAKOUT後も traction ゼロのまま whale pump 継続・$arm 2nd BREAKOUT/$BOO 2段 型） | traction0×2段 BREAKOUT×prebond継続——$165k 到達も traction ゼロ不変・BREAKOUT-then-dead 最有力（愛国命名 × social 皆無 × prebond：[[$AMERICA250]] 同クラスタ全滅参照） |
| [[$LR]]（Ledger Realms） | +304% | $139k→$563k | reply0 / KOL0（全期間） | 不明（DeFi/gaming "Ledger Realms"・@ledgerealms/ledgerealms.com 整備済・traction0全期間） | traction0×出来高先行 BREAKOUT×social整備済——$AEGIS/$PHONEBLACK/$MOONLAKE 同型・BREAKOUT-then-dead 候補 |
| [[$LR]]（Ledger Realms）2nd BREAKOUT | +107% | $563k→$1,166k | reply0 / KOL0（全期間） | 不明（1st BREAKOUT後も traction ゼロ継続・social整備済×出来高先行2段） | traction0×2段連続 BREAKOUT×$1.16M——$BOO 2段型/$TESTIBULL 2段型と同シグネチャ・DeFi generic 命名での $1M 突破・BREAKOUT-then-dead 最有力 |
| [[$BELIVE]]（belive） | +123%（BREAKOUT） | $40.2k→$89.8k | reply0 / KOL0（twitter/website null 全期間）・real_sol~1.7SOL | 不明（"belive" generic命名・social 窓口ゼロ・prebond 継続） | traction0×social皆無×prebond BREAKOUT＝$MC/$AEGIS/$JALAPEÑO 同型・BREAKOUT-then-dead 候補 |
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
- **全層を1判断に束ねる capstone**: [[ape-or-avoid]]（乗るか避けるかの統合フレーム）
- [[reflexivity]]（**根本エンジン**＝98.5%死は reflexive bust が常態・graduation×traction はループ燃料の有無）/ [[survivor-memes]]（工場から生き残った稀な graduate）/ [[majors-rotation-supercycle]]（供給希釈）/ [[onchain-verification]]（$LIBRA rug）
- [[$PUMP]] / [[$BONK]] / [[@a1lon9]] / [[@theunipcs]] / 集計の入口: [[signal|Signal digest]]

## 出典(生ソース)
[[@a1lon9]] $PUMP発射/buyback/$LIBRA disgust/fartcoin理想, [[@defi_kay_]] 評価額・graduation率・出来高,
[[@theunipcs]] $PUMP↔$BONK/BonkFun, [[@cobie]] 皮肉。（全て sources/x/ の原ツイに保存済）
