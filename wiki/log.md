# Log — 操作履歴

ingest / query / lint の記録（新しい順）。

- 2026-06-23 ingest(synthesis cycle 5): 新concept2枚。[[ai-memes]]（型: トークン＝自律エージェントの配布層。$ai16z/$GOAT/[[$FARTCOIN]]、agentic economy物語[[@a1lon9]]/[[@rajgokal]]。⚠️[[@blknoiz06]]「$10B AI memeは来るが勝者不明」・[[@lmrankhan]]自壊論・自律の主張と実体の差・corpus強気一色）と [[perp-dex-wars]]（動線: [[$HYPE]]/Hyperliquid一強 vs Axiom/[[$ASTER]]/Lighter/Phoenix。★⚠️[[@DefiIgnas]]「buyback flywheelの燃料は清算されたretailの手数料」＝productive cryptoの影、Wynn/Tate清算[[onchain-verification]]、CEX(JELLY)攻撃で独立性が的）。entity: [[$FARTCOIN]] [[$ASTER]] [[$HYPE]](追記) / [[@shawmakesmagic]]。これでconcept 11枚＝土台→基盤→マクロ→供給→meme/AI/perpの層構造が一旦埋まった。

- 2026-06-23 ingest(synthesis cycle 4): 新concept2枚。[[l1-substrate-wars]]（動線: Solana vs Ethereum＝memeが乗る地面。Solana陣営[[@rajgokal]]「pivot to solana」/cross-chain流動性 ⇄ Ethereum陣営[[@RyanSAdams]]profit/money layer/RWA。★[[@DefiIgnas]]が軸により両側＝「何の用途で勝つか」が肝。SOL/ETH相対は基盤シェアの代理）と [[vc-founder-thesis-layer]]（型: VC/創業者thesisが下流ナラティブの土台。stablecoin/BTC多層資本[[@saylor]]/規制追い風/AI×crypto[[@cdixon]]/app層。⚠️断層=BTC一極 vs app層optionality、規制楽観 vs [[@balajis]]脱国家）。entity: [[@toly]] [[@rajgokal]] [[@DefiIgnas]] [[@cdixon]] [[@saylor]]。手法=2並列エージェント横断→合成、mark_ingestedで合成分のみ消し込み。

- 2026-06-22 ingest(synthesis cycle 3): 新concept2枚。[[launchpad-economics]]（型: memeの供給工場＝Pump.fun/[[$PUMP]]・$600M/12分完売・revenue→buyback36%焼却・⚠️graduation率1.5%＝98.5%は死ぬ供給過剰＝[[majors-rotation-supercycle]]の供給希釈の蛇口・$LIBRA rug）と [[survivor-memes]]（型: 生き残った少数のblue-chip meme [[$BONK]]/[[$WIF]]/[[$PEPE]]/[[$FARTCOIN]]/[[$PENGU]]・★⚠️生存者バイアス＝語られる超リターンは全て後知恵の早期entry・集中リスク・corpusは強気一色なので懐疑はwikiが供給）。entity合成メモ: [[$PUMP]] [[$BONK]] [[$WIF]] [[$PEPE]] / [[@a1lon9]] [[@blknoiz06]]。手法=2並列エージェントで sources/x 横断→合成。mark_ingested で合成分のみ消し込み。

- 2026-06-22 ingest(synthesis cycle 2): 新concept [[onchain-verification]]（型: 言説をオンチェーン資金移動で裏取り＝憲法 指針6「観測と推論の分離」の運用ツール。[[@lookonchain]]/[[@arkham]]=計器、一致/乖離/休眠覚醒の3類型＋perp-OI先回り[[@theunipcs]]）。entity合成メモ記入: [[$BTC]]（QT→QEマクロ・4年周期・⚠️zhusu逆指標）/ [[@lookonchain]]（観測装置・⚠️移動と意図の分離）/ [[@theunipcs]]（perp-OIシグナル論・$BONK maxi）/ [[@milesdeutscher]]（サイクル慎重派・3AC記録者）。手法=2並列エージェントで sources/x 横断→合成。mark_ingested で合成分のみ消し込み。

- 2026-06-22 ingest(synthesis cycle 1): firehose是正。収集を一旦停止(GitHub `ingest` workflow disable＋ローカルlaunchd unload)し、backlog(未合成4,523)を合成する側へ全振り。新concept2枚: [[majors-rotation-supercycle]](BTC→ETH→altのローテ＋⚠️ supercycle主唱者[[@zhusu]]の崩壊を本人ツイで裏取り＝逆指標)、[[jp-meme-cluster]]([[$KINTON]]×[[$YAJUCOIN]]の相互保有メカニクス=束ねる型)。[[external-event-to-token-pattern]] を $TRUMP/$MELANIA/$VINE/$HARRYBOLZ で補強し「政治/要人meme=grift減衰」サブ型を追加。entity合成メモ記入: [[$ETH]] [[$SOL]] [[$KINTON]] [[$YAJUCOIN]] [[$TRUMP]] [[$HYPE]](追記) / [[@zhusu]] [[@CryptoHayes]]。手法=3並列エージェントで sources/x 横断収集→人手で合成判断(観測と推論を分離)。

- 2026-06-22 brain(mechanism): 整理(判断)を増分自動化する仕組みを実装。ingest_worklist.py(新ソース差分→bounded TODO=wiki/_worklist.md)、mark_ingested.py(消し込み状態)、pipeline.py(collect→digest→entities→worklist の glue)、INGEST.md(エージェント工程の手順)。LLM Wiki概念説明 docs/LLM-WIKI.md。実証として $HYPE を横断合成(Hayes売却発言×lookonchainオンチェーン裏取り)。

- 2026-06-22 brain(faithful): LLM Wiki(Karpathyパターン)準拠に作り直し。背骨=entityページ自動生成(brain/build_entities.py: token40/player120, synthesis保持ブロック付)。合成はentityのsynthesisメモ＋concept(動線/型)に分離、矛盾は両論併記。冗長なtoken-concept3枚をentityに統合。工程をbrain/READMEに明文化(貯める→仕分ける→整理 背骨→整理 判断)。

- 2026-06-22 brain: 仕分け層(brain/digest.py)＋合成デモ。5,086生ツイ→信号4,354に集計([[signal]])、そこからconcept5枚を合成(型: 外部イベント→token / 動線: SpaceX IPO→$SPCX・$ASTEROID / $ASTEROID / $SPCX / $CLUTCH)を相互リンク。LLM Wikiの脳が初稼働。

- 2026-06-22 collect: Senshi(@SenshiNeo7)のフォローからCAVEサークル＋日本trench層を取り込み(watchlist v4, ③方針=crypto＋外部要因, 66アカ追加, +1270ノート)。

- 2026-06-22 collect: 初回backfill完了。3,796ノート/55アカ取得(watchlist 58中)。syndication(無料)で大半＋twitterapi.io(有償)で残り＆詰まり分をクリーン回収。0xMert_/aeyakovenko/TusharJain_の3アカはAPI上0件(ハンドル変更/保護疑い、要確認)。collectorはsyndication/twitterapi両対応。

- 2026-06-22 build: collector v1 実装（syndication無料取得→sources/x/に生ツイ保存、$ticker/@mention自動抽出、ファイル存在で重複判定）。3アカ実走で形式確認(12ノート)。GitHub Actions(毎時)＋ローカルcron手順、graphからsources除外。

- 2026-06-22 config: watchlist v2 へ拡張（VC/Podcast/オンチェーン/マクロ層を追加、計約40アカをfxtwitterで実在確認）。収集方式は「自動かつ無料」で確定。
- 2026-06-21 init: Trench-Brain スキャフォールド作成。
