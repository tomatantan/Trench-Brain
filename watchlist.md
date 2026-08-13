---
type: config
title: 監視アカウント watchlist
created: 2026-06-22
updated: 2026-06-22
tags: [trench, watchlist, ingest]
---

# 監視アカウント watchlist v3

[[index]] / 収集(貯める仕組み)の入口。**これが収集の"門"**＝ここに載るアカウントの新規投稿"だけ"を取り込む（CLAUDE.md 憲法 指針2）。
**採用基準**: signalが濃いアカウント＝ミームの流れを読む／trench思想を継続発信する／有益情報を落とす。creator/VC/researcher/podcastも対象(trench-brain-vision)。
⚠️ ここでいう「signalを出す」は**無差別firehoseの肯定ではない**。watchlistという門で絞ること自体がキュレーション＝忠実さの担保。門なしフィード(CoinGecko trending/DexScreener boosted等)は憲法で恒久禁止。
weight = 合成優先度の目安(高ほど深いconcept合成に回しやすい / 後の仕分けフィルタ用)。
★**追加の手順（理解→収集の順・本人指示2026-07-06）**: 新アカを本体表に足したら、収集が始まる前に `bash brain/onboard_player.sh <handle>` で **onboarding profile（何者か/保守↔攻撃/立ち位置/発言の型/読み方）** を先に作る＝人物理解なしに投稿だけ取らない。profileはentityのcurated層（機械上書き不可）に入る。✅=fxtwitter実在確認済 / ⚠️=未確認(要再取得)。

## 創業者・ローンチパッド・VC（土台/動線の発端源）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@a1lon9]] | alon | — ✅ | Pump.fun 共同創業。launchpad文化の中心、新規ローンチの源 | 高 |
| [[@a16zcrypto]] | a16z crypto | 724k ✅ | 最大手VCのcrypto部門。セクター/規制/思想の土台 | 高 |
| [[@cdixon]] | Chris Dixon | 928k ✅ | a16z crypto マネージングパートナー | 高 |
| [[@rajgokal]] | raj | 1.09M ✅ | Solana 共同創業。エコシステムの号令 | 高 |
| [[@toly]] | Toly | — ✅ | Solana 共同創業(正ハンドルは @toly) | 高 |
| [[@KyleSamani]] | Kyle Samani | 215k ✅ | 元Multicoin共同創業→Forward Industries会長 | 中 |
| [[@hosseeb]] | Haseeb | 145k ✅ | Dragonfly マネージングパートナー | 中 |
| [[@lmrankhan]] | Imran | 43k ✅ | @alliance(アクセラレータ) | 中 |
| [[@FrankDeGods]] | Frank | 464k ✅ | DeGods創業(dox: @rohunvora) | 中 |
| [[@theunipcs]] | Bonk Guy | 225k ✅ | $BONK 旗振り | 中 |

## マクロ・外部要因クロスオーバー
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@mellometrics]] | Mello | 162k ✅ | GTM @worldlibertyfi(Trump系DeFi)。crypto×政治の外部ノード | 高 |
| [[@CryptoHayes]] | Arthur Hayes | 804k ✅ | BitMEX共同創業/Maelstrom。マクロ×crypto論者 | 高 |
| [[@zhusu]] | Zhu Su | 617k ✅ | 元3AC。マクロ/思想(賛否あるが影響力大) | 中 |

## Podcast・メディア（思想・有益情報の土台）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@Bankless]] | Bankless | 373k ✅ | crypto教育/フロンティアメディア | 高 |
| [[@RyanSAdams]] | Ryan Sean Adams | 278k ✅ | Bankless共同創業 | 中 |
| [[@TrustlessState]] | David Hoffman | 257k ✅ | Bankless共同創業 | 中 |
| [[@theempirepod]] | Empire | 14k ✅ | Blockworksのpodcast(crypto大局) | 中 |
| [[@JasonYanowitz]] | Yano | 128k ✅ | Blockworks共同創業/Empireホスト | 中 |
| [[@santiagoroel]] | Santiago Santos | 134k ✅ | Inversion Capital創業(思想/投資) | 中 |
| [[@TheRollupCo]] | The Rollup | 58k ✅ | 数字資産×金融podcast | 中 |
| [[@Lightspeedpodhq]] | Lightspeed | 12k ✅ | Solana特化podcast(Blockworks) | 高 |
| [[@defi_kay_]] | Danny | 1.7k ✅ | Lightspeed/0xresearch ホスト | 中 |
| [[@laurashin]] | Laura Shin | 289k ✅ | Unchained。crypto記者 | 中 |
| [[@uponlytv]] | Up Only | 128k ✅ | エンタメ寄りpodcast | 低 |
| [[@Cobie]] | Cobie | 1.03M ✅ | Echo/UpOnly。CTの古参・影響力大 | 高 |

## オンチェーン分析・リサーチ
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@lookonchain]] | Lookonchain | 699k ✅ | スマートマネー追跡 | 高 |
| [[@nansen_ai]] | Nansen | 355k ✅ | オンチェーン分析プラットフォーム | 中 |
| [[@arkham]] | Arkham | 1.52M ✅ | オンチェーンインテリジェンス | 中 |
| [[@DefiIgnas]] | Ignas | 162k ✅ | DeFiリサーチ/ナラティブ | 中 |
| [[@thedefiedge]] | The DeFi Edge | 302k ✅ | ナラティブ系統リサーチ | 中 |
| [[@milesdeutscher]] | Miles Deutscher | 671k ✅ | 分析/AI(現@aiedge_寄り) | 中 |

## トレンチKOL・デジェン（中核）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@blknoiz06]] | Ansem | 979k ✅ | トレンチ最大級KOL(@BullpenFi @MarketBubble) | 高 |
| [[@Ministerr]] | Minister 🔮 | 157k ✅ | "making internet money with internet friends" 大口デジェン | 高 |
| [[@notthreadguy]] | notthreadguy | — ✅ | トレンチKOL | 高 |
| [[@badattrading_]] | Nova | 55k ✅ | コイン精査/レビュー系、$SOBAT絡み | 中 |
| [[@spyzer]] | spyzer | 20k ✅ | "Stay delusional" @UN10001 @Labyr1nthhh_ | 中 |
| [[@cookerbruski]] | bruski🦎 | 15k ✅ | "cemetery operator" @coldcapitalclub | 中 |
| [[@TheMisterTurtle]] | Mr. Turtle | 15k ✅ | "too rich to work, too poor to retire" | 中 |
| [[@jotagezin]] | jg | 12k ✅ | "the cage is all I know" | 中 |
| [[@ilyunow]] | Ily | 7k ✅ | "delusional meme economist"(旧垢削除) | 中 |
| [[@ShapeFN_]] | Shape | 1.7k ✅ | "Be the Penguin" 小規模・早期シグナル候補 | 低 |

## 拡張 v3（2026-06-22 追加・有償取得を見据え対象拡大）

### トレンチKOL・トレーダー（追加）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@CryptoKaleo]] | Kaleo | 727k ✅ | 大手caller | 高 |
| [[@HsakaTrades]] | Hsaka | 600k ✅ | 著名トレーダー | 高 |
| [[@inversebrah]] | smolting (wassie) | 512k ✅ | CTデジェン文化の中心 | 中 |
| [[@CredibleCrypto]] | CrediBULL | 482k ✅ | TA/トレーダー | 中 |
| [[@gainzy222]] | gainzy | 329k ✅ | "professional pastry eater" 古参トレンチ | 中 |

### マクロ・外部要因（追加）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@cz_binance]] | CZ | 11.6M ✅ | Binance創業。発言が市場全体を動かす最上位ノード | 高 |
| [[@saylor]] | Michael Saylor | 5.1M ✅ | Strategy/BTC最大級の論者 | 高 |
| [[@pmarca]] | Marc Andreessen | 4.0M ✅ | a16z創業。tech×政治×crypto | 高 |
| [[@balajis]] | Balaji | 1.7M ✅ | Network State。思想/マクロ | 高 |
| [[@RaoulGMI]] | Raoul Pal | 1.4M ✅ | Global Macro/Real Vision | 中 |

### 創業者・VC（追加）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@Rewkang]] | Andrew Kang | 421k ✅ | Mechanism Capital創業/トレーダー | 高 |
| [[@0xngmi]] | 0xngmi | 193k ✅ | DefiLlama創業。データ/DeFi | 中 |

### ニュース・速報（追加）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@WatcherGuru]] | Watcher.Guru | 4.3M ✅ | crypto/金融速報の最大級 | 高 |
| [[@Tree_of_Alpha]] | Tree | 246k ✅ | TreeNewsFeed。超速報/アルファ | 高 |

### ナラティブ源（追加）
| handle | 名前 | followers | メモ | weight |
|---|---|---|---|---|
| [[@shawmakesmagic]] | Shaw | 163k ✅ | ai16z/Eliza。AIエージェント・ナラティブの発生源 | 高 |

## ★対立枠 / anti-echo（2026-07-04・本人directive「情報源が視野狭窄・エコーチェンバー」）
> ここは**合意枠と逆の声を能動的に入れる門**。目的＝矛盾の表面積を最大化する(ENGINE-REDESIGN §0.1・矛盾=KPI)。
> 引用グラフ拡張は却下(同クラスタを濃くするだけ=エコー増幅)。うちのwatchlistが"引用しない側"を名指しで入れる。
> ⚠️ handleは未確認多数＝collectorが fxtwitter で自動検証。存在しないものは収集されず落ちるだけ(fail-safe)。
> ★このセクションは「どっちの声か常に分かる」為に独立管理。合成時 concept で ⚠️矛盾 として両論併記に使う。

### 軸1: オンチェーン検事・構造的懐疑者（熱狂を"どう抜かれるか"で見る）
| handle | 視点 | weight |
|---|---|---|
| [[@zachxbt]] | 詐欺追及の本丸。魔界の裏側(rug/bundle/insider)を暴く | 中 |
| [[@spotonchain]] | 資金フロー実測で言説を裏取り | 中 |
| [[@lookonchain]] | (既存) オンチェーン検証装置 | 中 |

### 軸2: 弱気・froth懐疑（「これはカジノ」と言う側）
| handle | 視点 | weight |
|---|---|---|
| [[@GiganticRebirth]] | GCR。froth/過熱の逆張り・弱気call | 中 |
| [[@Pentosh1]] | マクロ×懐疑。無闇に乗らない型 | 中 |
| [[@Cobie]] | CT過熱への冷笑・構造批判 | 中 |
| [[@loomdart]] | 逆張り・froth警戒 | 中 |

### 軸3: 別チェーン・反pump.fun（魔界を格下と見る視点）
| handle | 視点 | weight |
|---|---|---|
| [[@sassal0x]] | ETH側。Solミーム文化への対立視点 | 中 |
| [[@iamDCinvestor]] | ETH/NFT長期。meme casino批判 | 中 |
| [[@0xngmi]] | DefiLlama。データで殴る・ナラティブ不信 | 中 |

### 軸4: 純TA・quant・perp desk（ナラティブでなくチャート/建玉で語る）
| handle | 視点 | weight |
|---|---|---|
| [[@CryptoCred]] | 純TA。物語でなく価格構造 | 中 |
| [[@0xkyle__]] | quant/リサーチ寄り | 中 |

> 軸5(CN/KR圏)は実handleを確信できない為 保留＝本人/仲間から現地アカを募集中。

## 未確認・保留
- [[@0xMert_]] (Mert/Helius CEO) — fxtwitter 404、要再取得。
- [[@TusharJain_]] (Multicoin共同創業) — fxtwitter 404、要再取得。
- @spotonchain — @hupzy_agent に移行済(要確認)。

## メモ
- 計 約40アカ(v2)。weightは暫定、投稿の質/follow-throughで調整。
- 取得方式: **自動かつ無料**で回す方針(公式API/有料API不使用)。GitHub Actions等の無料cron＋無料取得(nitter/syndication/fxtwitter)でポーリング→ingest→自動commitを想定。脆さは要PoC検証。詳細は[[trench-brain-vision]]。
- 追加候補・新顔はここに追記。

## 拡張 v4（Senshi/CAVEサークル harvest, 2026-06-22）
@SenshiNeo7 のフォローから取り込み。③方針=crypto＋外部要因を採用、スポーツ/格闘技/一般/非cryptoミームは除外。
日本trench層＋[[CAVE]]コミュニティ＋外部要因(elon/WhiteHouse等)を補完。

| handle | 名前 | メモ |
|---|---|---|
| [[@coingecko]] | CoinGecko | The world's largest independent crypto data aggregator. |
| [[@moonshot]] | Moonshot | Buy, Sell, and Create Memes with Apple Pay. Live on App |
| [[@pepecoineth]] | Pepe | $PEPE. The most memeable memecoin in existence. |
| [[@wojakcto]] | Wojak | Wojak, also known as "Feels Guy," the OG Internet Meme |
| [[@WhiteHouse]] | The White House | Welcome to The Golden Age of America.  📱 Text USA to 45 |
| [[@Clutch_FIFA2026]] | CLUTCH | $Clutch - The Eagle Mascot of USA for the World Cup 202 |
| [[@Crypto_Alch]] | The Alchemist (🧪,⚗ | Some people call me Nostradamus's 7th Son. I often miss |
| [[@itspyrored]] | 𝐏𝐲𝐫𝐨 𝐑𝐞𝐝 | Not Financial Advice - I share my opinions,Technical An |
| [[@Punch_on_sol]] | Punch | Ultimately, you have to be brave. $PUNCH on Solana 🐒 |
| [[@iconocl4sm_]] | Idola | Idola(あいどら)a.k.a. Ains/xlo TGac: https://t.co/drq082mgo |
| [[@ametomuchi123]] | 飴と鞭 | 高卒→色々失敗借金沢山→多重債務(29%利率の時)→完全歩合の営業で借金完済→起業。草コインで→億→継続→税金 |
| [[@AdimsSHOGUN]] | Adims SHOGUN アディムス | 雰囲気トレーダー📊労働基準法適用除外の社畜🐽安全保障セクター🌏経済的自由になりたい元SUI MAXI💧魔界Wa |
| [[@810yenshamp]] | 810円ﾌﾟﾚｲｱｯｰ | イクゾ〜ヤルゾ〜ヤジュウコイン  $YAJUcoin |
| [[@Uniswap]] | Uniswap | The largest onchain marketplace. Buy and sell crypto on |
| [[@CoinbaseMarkets]] | Coinbase Markets 🛡 | Building the everything exchange. All markets — all in  |
| [[@brian_armstrong]] | Brian Armstrong | Co-founder & CEO at @Coinbase. Creating more economic f |
| [[@cryptocom]] | Crypto.com | The best place to buy, sell, and pay with crypto #BTC # |
| [[@MEXC]] | MEXC | Your 0-Fee Gateway to Infinite Opportunities Trade Cryp |
| [[@BinanceUS]] | Binance.US 🇺🇸 | Access 200+ cryptocurrencies and explore the world of W |
| [[@golocojp]] | Maru2 | Crypto Investor｜Agentic Coding Learner｜ICM Believer in  |
| [[@NZensin]] | NEO | 忘備録の為の只野日記です 投資歴 株式38年・ゴールド原油29年・BTC9年 まだ47年投資続きます リーダー |
| [[@Plably_coin]] | Plably | Trade less. Play more. A token economy built around gam |
| [[@angorou7]] | アンゴロウ@暗号資産 | 「2025年ブロックチェーン業界で活躍した人物」日本2位受賞🇯🇵🥈 ビットコイン・暗号資産（仮想通貨）・株の爆 |
| [[@xvwmuca]] | kagura | trencher / $url, $kinton dev |
| [[@MurphyBTC]] | まーふぃー＠ビットコイン | Crypto Trader / Investor / Market Analyst / DUMP-PUMP M |
| [[@tomuisan]] | とむい | 専業トレーダー8年目。 |
| [[@coinkeiba]] | ツァビ | $HYPE と馬券を握りしめる男。 |
| [[@Nishi8maru]] | 仮想NISHI | 暗号資産アナリスト / CoinPostアプリ-Terminal開発-BTC Alert @Nishi8mAl |
| [[@coin_post]] | CoinPost（仮想通貨メディア） | Japan's largest crypto news outlet 国内最大の暗号資産（仮想通貨）・Web3 |
| [[@bull_bnb]] | BuLL 牛 | I didn't survive the dark. I studied it. Decoding patte |
| [[@mag_onsol]] | まが (maga) | CAVE's admin https://t.co/VFvM7JhWtt |
| [[@DEG_2020]] | DEG | 2016年からの子育て無職トレーダー。株、為替、商品、不動産、暗号資産なんでもトレードします。資産10億円目指 |
| [[@noritaka_okabe]] | 岡部典孝　JPYC代表取締役 | JPYC株式会社で日本円ステーブルコインJPYCを発行。社会のジレンマを突破する！ 責任あるイノベーションを一 |
| [[@ren_Nevermind]] | ren | れんちょん / ex-VC / what important truth do very few people |
| [[@MemememHen]] | haru (punch/acc) | $punch cto lead/ affiliate with @tradingterminal |
| [[@daisuk_e4]] | Okumo | CAVE's admin. Tweet about crypto topics. |
| [[@kyurukyurutrade]] | しょこら/Shoko | しょこらとかしょことか名乗ってます。かそつーたのしー @cave_jpn の民 |
| [[@uyunicham]] | うゆにちゃん🐰 | ·̩͙. ᘏ▸◂ᘏ .·̩͙ ꒰ ⸝⸝ɞ̴̶̷ ·̮ ɞ̴̶̷ ⸝⸝꒱ *ଘ_(")("）┄┄゛meme系クリ |
| [[@0xFunX]] | 0xFun | 你所相信的，就是你的命运！  全职投机笔记，乐观者，记录分享。 |
| [[@solana]] | Solana | The high performance network powering internet capital  |
| [[@pumpilians_]] | Pumpilians | 2D Pixel Sandbox MMORPG. Play different. Earn different |
| [[@GTCaliber_]] | Caliber | Focus on making the actual GTA 6 before the GTA 6 out!! |
| [[@PumpfunEco]] | Pump.fun Ecosystem | Featuring @Pumpfun’s best traders, creators & communiti |
| [[@Pumpfun]] | Pump.fun | Launch a coin that is instantly tradeable in one click  |
| [[@garrytan]] | Garry Tan | President & CEO @ycombinator —Founder @garryslist—Creat |
| [[@nikitabier]] | Nikita Bier | head of product @x, advisor @solana, venture partner @l |
| [[@RookieXBT]] | RookieXBT 🧲 |  |
| [[@jzbookp9ca]] | 本屋🍆/Stray Ebi | CAVE末席  せんせえ🍆です 大学のなかの人もやってます ごちゃまぜアカウントなので騒がしいです  ▶ il |
| [[@tsuyuto6154]] | 猫太郎_Nekotaro | $YAJUcoin team ／ fulltime degen ／Cave admin |
| [[@SeruDefi]] | Crypto_Serupo🇯🇵 | CAVE |
| [[@JPY_TO_Crypto]] | tomatantan | dev:https://t.co/tjoc5Yyma4 |
| [[@ethereum]] | Ethereum | The universal platform for crypto, blockchain apps, sta |
| [[@MascotAsteroid]] | Asteroid Shiba | Mascot of SpaceX / Official X for the memecoin Asteroid |
| [[@solbrdl]] | Bradley (☄️) | Asteroid maxxing. |
| [[@dogecoin]] | Dogecoin | Dogecoin is an open source peer-to-peer cryptocurrency, |
| [[@coinbase]] | Coinbase 🛡️ | The future of finance is on Coinbase. For support: @Coi |
| [[@Bitcoin]] | Bitcoin | Bitcoin is an open source censorship-resistant peer-to- |
| [[@dxrnell]] | dxrnelljcl | @tagxalpha / @ugcabal / @tradingterminal |
| [[@ofasya_]] | Ogawa (小,川) | Stay poor , Stay Degen CAVE Founder / @cave_jpn |
| [[@YAJUDAIGONGEN]] | 野獣コインに全財産を賭けた男 | 野獣先輩は宇宙の心理 昭和〜平成のレトロゲー、アニメ、映画が好きです コメントや大喜利、適当なボケ大歓迎！ 気 |
| [[@CoinMarketCap]] | CoinMarketCap | #CMC is the world’s most trusted source for crypto data |
| [[@binance]] | Binance | The world’s leading blockchain ecosystem and digital as |
| [[@grok]] | Grok | @grok it |
| [[@MarioNawfal]] | Mario Nawfal | Largest Show on X (Live Daily 10am-8pm ET) / 24x7 Write |
| [[@SpaceX]] | SpaceX | SpaceX designs, manufactures and launches the world’s m |
| [[@elonmusk]] | Elon Musk | https://t.co/dDtDyVssfm |

## 自動拡張→承認（2026-06-24・引用グラフ候補から本人承認・段階追加）
| account | name | 役割/理由 | 優先 |
|---|---|---|---|
| [[@pumpdotfun]] | Pump.fun | launchpad本体・新規ローンチの源（[[launchpad-economics]]） | 高 |
| [[@mert]] | mert | Helius/Solana インフラ・dev動線 | 中 |
| [[@HyperliquidX]] | Hyperliquid | perp dex本体（[[perp-dex-wars]] 直結） | 中 |
| [[@fundstrat]] | Fundstrat | マクロ/BTC cycle 分析（BTC coverage 穴埋め） | 中 |
| [[@VitalikButerin]] | Vitalik | Ethereum 共同創業・思想/影響力 | 中 |
| [[@armaniferrante]] | Armani | Backpack 共同創業・RWA/tokenized株($SPCX系) | 中 |
> ↑ signal_backlog を見ながら段階追加（一括でなく＝合成が追いつくレート維持・芯）。次枠は backlog が bounded を確認してから。

## 自動拡張から承認（2026-07-02・引用グラフ＝"調べる人を増やす"・本人directive）
引用グラフで watchlist の複数アカが繰り返し言及してた実在の人/トレーダー/思考発信者を承認（org/取引所/protocol/政府/メディアは除外＝mind-modelにならない）。強者だけでなく多様な声・別クラスタ・日本trench系も含め、**矛盾の表面積を広げる**（echo-chamber対策）。次サイクルから収集開始。⚠️=未実在確認(収集時fxtwitterで確認)。

| handle | メモ | weight |
|---|---|---|
| [[@naval]] | Naval・思想/first-principles ⚠️ | 中 |
| [[@nic_carter]] | Nic Carter・BTC/データ論客 ⚠️ | 中 |
| [[@ErikVoorhees]] | Erik Voorhees・libertarian/思想 ⚠️ | 中 |
| [[@tayvano_]] | Tay・セキュリティ/on-chain forensics ⚠️ | 中 |
| [[@imperooterxbt]] | imperooter・trader ⚠️ | 中 |
| [[@buffalu__]] | buffalu・trench trader ⚠️ | 中 |
| [[@HardhatChad]] | HardhatChad・on-chain/dev視点 ⚠️ | 中 |
| [[@LarpVonTrier]] | LarpVonTrier・trench ⚠️ | 中 |
| [[@tulipking]] | tulipking・trader ⚠️ | 中 |
| [[@_Shadow36]] | Shadow・trader ⚠️ | 中 |
| [[@vibhu]] | vibhu ⚠️ | 中 |
| [[@minnus]] | minnus・trader ⚠️ | 中 |
| [[@remusofmars]] | remus・trader ⚠️ | 中 |
| [[@Adam_Tehc]] | Adam ⚠️ | 中 |
| [[@SenshiNeo7]] | Senshi・trench ⚠️ | 中 |
| [[@tushar_jain]] | Tushar Jain・Multicoin ⚠️ | 中 |
| [[@ilblackdragon]] | Illia・NEAR創業/AI ⚠️ | 中 |
| [[@adietrichs]] | Ansgar・ETH researcher ⚠️ | 中 |
| [[@vnovakovski]] | trader ⚠️ | 中 |
| [[@seyong]] | seyong ⚠️ | 中 |
| [[@fibonacki]] | fibonacki・trader ⚠️ | 中 |
| [[@poe_real69]] | poe・trench ⚠️ | 中 |
| [[@solangelestv]] | trench ⚠️ | 中 |
| [[@ichikawa_zoo]] | 日本trench ⚠️ | 中 |
| [[@MCGlive]] | trench ⚠️ | 中 |
| [[@PlayKintara]] | 日本trench ⚠️ | 中 |
| [[@the_defi_report]] | DeFi research ⚠️ | 中 |
| [[@aerugoettinea]] | 日本trench ⚠️ | 中 |

<!-- auto-candidates:start -->
## 自動拡張候補（引用グラフ・要承認 / `expand_watchlist.py` 自動生成）
watchlist の **2アカ以上**が言及した未収集アカ＝門に足す候補（指針2: 繰り返し引用＝KOL言及門）。
**承認のしかた**: 良いものを上の watchlist 本体に `[[@handle]]` で足すだけ→次サイクルから収集開始。

| 候補 | 言及したwatchlistアカ数 | 総言及 |
|---|---|---|
| @fomo | 41 | 209 |
| @vladtenev | 35 | 111 |
| @RobinhoodCrypto | 34 | 91 |
| @rasmr_eth | 18 | 48 |
| @mdudas | 18 | 29 |
| @Pattyice | 17 | 24 |
| @Lighter_xyz | 14 | 101 |
| @JohannKerbrat | 14 | 39 |
| @SECGov | 14 | 21 |
| @realDonaldTrump | 13 | 48 |
| @Morpho | 13 | 30 |
| @MeteoraAG | 12 | 123 |
| @MarketBubble | 12 | 57 |
| @jtx_trade | 12 | 36 |
| @CoinDesk | 12 | 27 |
| @daumenxyz | 12 | 26 |
| @wrld_sol | 12 | 24 |
| @OpenAI | 12 | 19 |
| @ponsdotfamily | 11 | 52 |
| @artsch00lreject | 11 | 39 |
| @jessepollak | 11 | 35 |
| @zinceth | 11 | 24 |
| @Cointelegraph | 11 | 22 |
| @krakenfx | 11 | 15 |
| @POTUS | 10 | 150 |
| @AskVenice | 10 | 55 |
| @MINHxDYNASTY | 10 | 45 |
| @json1444 | 10 | 24 |
| @TradingTerminal | 10 | 24 |
| @haydenzadams | 10 | 23 |
| @arbitrum | 10 | 17 |
| @_TJRTrades | 10 | 15 |
| @DegenerateNews | 10 | 15 |
| @sunrise | 9 | 61 |
| @virtuals_io | 9 | 39 |
| @sapijiju | 9 | 39 |
| @PhoenixTrade | 9 | 27 |
| @MEADGod | 9 | 26 |
| @OnlyLJC | 9 | 24 |
| @RebeccaRettig1 | 9 | 22 |
| @OndoFinance | 9 | 21 |
| @jito_sol | 9 | 19 |
| @SolanaFloor | 9 | 19 |
| @solanamobile | 9 | 18 |
| @izebel_eth | 9 | 18 |
| @econoar | 9 | 17 |
| @BNBCHAIN | 9 | 17 |
| @ThinkingUSD | 9 | 16 |
| @AvgJoesCrypto | 9 | 16 |
| @DavidSacks | 9 | 15 |
| @gr3gor14n | 9 | 12 |
| @aibaldking | 8 | 127 |
| @NEARProtocol | 8 | 62 |
| @Collector_Crypt | 8 | 32 |
| @KobeissiLetter | 8 | 27 |
| @justinsuntron | 8 | 23 |
| @heyibinance | 8 | 23 |
| @moonpay | 8 | 22 |
| @SecScottBessent | 8 | 22 |
| @tradexyz | 8 | 21 |
<!-- auto-candidates:end -->

## spyzer情報網（本人承認 2026-07-06・収集ON）
> 出典: [[spyzer-complete-meme-coin-guide-fulltext]] p.112-119。本人「移していいよ」(2026-07-06)。
> まず推し18（spyzerのinner circle 8＋大物10）のみ＝合成が追いつくペースで段階投入（芯: 一括163はしない）。

| handle | 名前/枠 | メモ | weight |
|---|---|---|---|
| [[@Ga__ke]] | inner circle | spyzerガイドのレビュアー(感謝枠)＝彼の情報網の中核 | 中 |
| [[@monke_]] | inner circle | 同上(レビュアー) | 中 |
| [[@C1phervoyager]] | inner circle | 同上(レビュアー) | 中 |
| [[@Just2Addicted]] | inner circle | 同上(レビュアー) | 中 |
| [[@IceSlayerMan]] | inner circle | 同上(レビュアー) | 中 |
| [[@Cypherpunkgod]] | inner circle | 同上(レビュアー) ⚠️垢は生存確認済(2026-07-07 web・NFT/creator経済系の発信)だが twitterapi last_tweetsが0件返す型＝onboarding profile保留・収集は梯子の別経路で試行 | 中 |
| [[@chjokka]] | inner circle | 同上(レビュアー) | 中 |
| [[@au_xbt]] | 訳者 | ガイド中国語訳を無償担当＝CN圏への橋・spyzerが人柄を絶賛 | 中 |
| [[@MustStopMurad]] | Murad | memecoin supercycle論の本人 | 高 |
| [[@SOLBigBrain]] | 大物 | SOL系大口 | 中 |
| [[@aixbt_agent]] | AI agent | AI発の相場観測アカ(独自ソース種) | 中 |
| [[@traderpow]] | 大物 | trencher | 中 |
| [[@orangie]] | 大物 | trencher | 中 |
| [[@Cupseyy]] | 大物 | trencher | 中 |
| [[@KookCapitalLLC]] | 大物 | trencher | 中 |
| [[@wizardofsoho]] | 大物 | trader | 中 |
| [[@trading_axe]] | 大物 | trader | 中 |
| [[@himgajria]] | 大物 | trader/thinker | 中 |


## spyzer情報網（段階投入・自動 staged_intake.py）
> 承認済み候補([[spyzer-complete-meme-coin-guide-fulltext]]の情報網)を**1人/サイクル**で段階投入(本人指示2026-07-07)。健康ゲート=signal_backlog増加中は停止。理解ゲート=onboarding profile必須。

| handle | 枠 | followers(取得時) | weight |
|---|---|---|---|
| [[@trader1sz]] | main | 682016 | 中 |
| [[@shahh]] | main | 402674 | 中 |
| [[@cishanjia]] | cn | 306753 | 中 |
| [[@Jeremybtc]] | main | 282494 | 中 |
| [[@metaversejoji]] | main | 263326 | 中 |
| [[@huahuayjy]] | cn | 300305 | 中 |
| [[@0xSweep]] | main | 249098 | 中 |
| [[@SolportTom]] | main | 209340 | 中 |
| [[@0xcryptowizard]] | cn | 228217 | 中 |
| [[@cozypront]] | main | 205691 | 中 |
| [[@cryptolyxe]] | main | 198601 | 中 |
| [[@0xSunNFT]] | cn | 211374 | 中 |
| [[@patty_fi]] | main | 147730 | 中 |
| [[@CookerFlips]] | main | 135608 | 中 |
| [[@0xAA_Science]] | cn | 180533 | 中 |
| [[@bonkfun]] | main | 106866 | 中 |
| [[@Cbb0fe]] | main | 106625 | 中 |
| [[@connectfarm1]] | cn | 134076 | 中 |
| [[@ResellCalendar]] | main | 102000 | 中 |
| [[@WhiteWhaleLabs]] | main | 98301 | 中 |
| [[@EnHeng456]] | cn | 104880 | 中 |
| [[@fomomofosol]] | main | 94361 | 中 |
| [[@slingoorio]] | main | 84270 | 中 |
| [[@DekuKing1]] | cn | 103979 | 中 |
| [[@SolidTradesz]] | main | 84016 | 中 |
| [[@suganarium]] | main | 82313 | 中 |
| [[@silverfang88]] | cn | 95874 | 中 |
| [[@FlippingProfits]] | main | 73803 | 中 |
| [[@ShockedJS]] | main | 73596 | 中 |

## 本人指名（2026-07-12・理解→収集の門=onboarding profile作成済）
| handle | メモ | weight |
|---|---|---|
| [[@flooroftests]] | 本人指名2026-07-12 | 中 |
| [[@pingucharts]] | 本人指名2026-07-12 | 中 |
| [[@CJWAT5ON]] | 本人指名2026-07-12 | 中 |
| [[@change]] | 本人指名2026-07-12 | 中 |
| [[@_logjam]] | 本人指名2026-07-12 | 中 |
| [[@PoorGoat_]] | 本人指名2026-07-12 | 中 |
| [[@Thokani]] | 本人指名2026-07-12 | 中 |
| [[@airtightfish]] | 本人指名2026-07-12 | 中 |
| [[@OinkersRUs]] | 本人指名2026-07-12 | 中 |
| [[@Farmercharts]] | 本人指名2026-07-12 | 中 |

## spyzer情報網 候補プール（★全量 本人承認済 2026-07-07 → 段階投入queueへ移行済）
> **状態(2026-07-07)**: 残り145は本人承認済。ただし**一気に投入しない**(本人指示「1人ずつ」)＝`brain/state/staged_intake_queue.json` に followers降順×main2:CN1交互で積み、`brain/staged_intake.py`(cron配線済)が**1人/サイクル**だけ上の「段階投入」表へ昇格する。健康ゲート(signal_backlog増加中は停止)+理解ゲート(onboarding profile必須)。下のリストは出典記録として保持（このプール自体は収集対象でない=[[@handle]]リンクにしていない）。
> [[@spyzer]]（Ansem公認KOL）のフォロー推奨170超のうち、既watch 22を除く分。
> ⚠️ spyzer本人が「全員検証済みではない・印象ベース」と明言（実例: 推薦リスト内の @badattrading_ はうち実測で死亡率61%）＝**彼の網の地図であって品質保証ではない**。承認は下から選んで上の本体表へ `[[@handle]]` で移すだけ。無差別一括追加はしない（門）。

**推し18 → 上の承認済みセクションへ移動済（2026-07-06 本人承認）**。元リスト:
- **感謝枠=ガイドのレビュアー（彼のinner circle）**: @Ga__ke @monke_ @C1phervoyager @Just2Addicted @IceSlayerMan @Cypherpunkgod @chjokka／中国語訳者 @au_xbt
- **大物で未watch**: @MustStopMurad（Murad） @SOLBigBrain @aixbt_agent @traderpow @orangie @Cupseyy @KookCapitalLLC @wizardofsoho @trading_axe @himgajria

**残り（main・109）**:
@game_for_one @xydotdot @real_y22 @watchingmarkets @ieatjeets @JW100x @Cryptotrissy @DecentrlizOrDie @cryptoleon @AlphaHunte19762 @miragemunny @0xBossman @fey_xbt @bitbellaa @HopiumPapi @metaversejoji @cozypront @daumenxyz @cryptolyxe @trader1sz @rasmr_eth @wrld_sol @slingoorio @gudmansachs @bonkfun @NewsyJohnson @SolidTradesz @shahh @WazzCrypto @roboPBOC @fomomofosol @ShockedJS @degengambleh @0xSweep @patty_fi @DataC58218 @thokani @suganarium @cryptokillua99 @0xx_Hammy @redemptionarcc @feikuu @leyten @onchainrapist @WhiteWhaleLabs @BernieOnChain @sized_in @ResellCalendar @jackduval @0xSoju @CookerFlips @trenchesborn @goyimpnl @clukz @CryptoCaptic @sippin_icm @AceAgain_ @Fapital3 @RainsRevenge @Bancrypto__ @AxisAce101 @DimitriDotEth @dylansdegens @Jeremybtc @zer0profit_ @crypto_iso @0GAntD @solvenant @ChillTRD @0xHeroSt @winiam4444 @zinceth @0xRenaissance @roxinft @evee0x @jikksol @0xdetweiler @Cbb0fe @icobeast @supercontraa @crypticd22 @MidCurveMortal @FlippingProfits @J_Dood_ @Nic_Wenzel_1 @DineroDom0 @iruletrenches @CryptoTomYT @SolportTom @BeanzzSOL @_logjam @rynzoeth @sonder_crypto @duckingnator @lesabrefomo @Catolicc @amabinvesting @izebel_eth @funcry @gumsays @tryfomo

**中国語圏KOL（44・未開拓の多視点ソース=エコチェンバー対策の別大陸）**:
@hexiecs @0xSunNFT @brc20niubi @0xcryptowizard @0xmagnolia @hellosuoha @connectfarm1 @BitCloutCat @neso @cishanjia @DekuKing1 @silverfang88 @CryptoDevinL @Ed_x0101 @GCsheng @EnHeng456 @BiliSquare @Wolfy_XBT @Michael_Liu93 @Huang2024 @minglaugodel @BroLeonAus @liangfenxiaodao @Mirro7777 @huahuayjy @kaikaibtc @liping007 @bigbottle44 @0xEdwin999 @HtrZac @0xAA_Science @GoldenPepeCabal @SuperL9 @nine_DeFi @Deibajie @3ethtomoon @luge517 @Arya_web3 @Unipioneer @Dincocoin @cryptojiuyi @real_dr_pump @Wmafia6 @0xNoNo_1

（既にwatch済で重なった22: spyzer mert toly zachxbt poe_real69 HsakaTrades rajgokal frankdegods DegenerateNews moonshot Pumpfun dxrnell notthreadguy blknoiz06 MCGlive badattrading_ cz_binance gainzy222 remusofmars a1lon9 OnlyLJC seyong ＝ **spyzer網とうちの門の重なり15.6%**＝独立に組んだ網が2割弱一致・相互裏付け）

## プラットフォーム中枢（Robinhood・上流シグナル / 本人 /add 2026-07-13）
> 型＝[[platform-insider-watching]]。KOL網とは**別レイヤーの縦/上流**シグナル（プラットフォームが次に何を押すか）。原典 [[robinhood-insider-watch]]（@btc2ai）。
> ⚠️ **状態＝候補（要 fxtwitter 実在確認 + `bash brain/onboard_player.sh <handle>` でのonboarding）**。理解→収集の順（指針）を尊重＝実在確認+profile前は能動収集に載せない。監視法＝新規フォロー差分/ミーム・軽口/いいね・RT。

- **意思決定者**: @vladtenev（CEO Vlad Tenev）/ @BaijuBhatt（共同創業）
- **実行層（最も見落とされるalpha）**: @abhishekf96（VP）/ @GrantBradford（CS・ops）/ @SteveQuirk_ / @JBMackenzie_ / @PatDunn / @ShivVerma
- **Crypto/DeFi直轄**: @fern（DeFi lead）/ @RobinhoodCrypto（公式crypto）
- **公式マトリクス（ニュース確認用）**: @RobinhoodComms / @AskRobinhood / @RobinhoodApp_EU
