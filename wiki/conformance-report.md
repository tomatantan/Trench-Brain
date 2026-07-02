# 憲法 conformance レポート（機械検査・自己採点でない）

PASS 22 / FAIL 0 / WARN 1 / 計23

| id | 指針/節 | 要件 | 判定 | 証拠/違反 |
|---|---|---|---|---|
| Q1 | §Query step3 | /wiki の価値ある回答を wiki/queries/ に資産化する | ✅PASS | assetize_query 定義&呼出あり / queries 17枚 |
| R1 | 指針1 | sources/ は読むだけ＝合成engineは sources/ を編集しない(収集/curationのみ可) | ✅PASS | 合成engineはsources/を編集してない(collect/add/imageのみ=curation) |
| R2 | 指針2 | 収集は門付き(watchlist/traction/KOL)・firehose禁止 | ✅PASS | watchlist門=8 scam門=6 firehose無し |
| R3 | 指針3 | 合成が収集に追いつく＝signal_backlogで健康を測る | ✅PASS | 最新signal_backlog=2（記録あり） |
| R3d | 指針2/3 収集入口の鮮度 | X収集の入口が生きてる＝sources/x が凍結してない(2026-06-26 twitterapi 402 が5日半 false-green だった盲点を塞ぐ) | ✅PASS | collect_health 2.3h前 backend=twitterapi new=162 err=0/131 |
| R7 | 指針7 | 全ページを wikilink で接続＝孤立ページが無い | ✅PASS | 孤立concept無し |
| L1 | §Lint | lint(健康診断)が稼働＝矛盾/孤立/ギャップを定期検出 | ✅PASS | synthesize_lint.sh + lint-report.md あり |
| OA1 | 指針2/6 観測≠採用 | 全mint観測(篩材料)≠採用(篩通過のみ合成) | ✅PASS | 観測コード=18 採用門コード=9 |
| C4 | 指針4 | 1ソース取込→複数ページに波及(synthesis) | ✅PASS | 波及指示あり・summary4+entity750枚 |
| C5 | 指針5 | 矛盾は消さず⚠️両論で保持する | ✅PASS | concept内 ⚠️/矛盾 88箇所・prompt指示あり |
| C6 | 指針6 | entityで観測(事実)と推論(判断)を分離する | ✅PASS | 観測/判断を分離した entity 669/750枚 |
| C8 | 指針8 | bottom-up＝conceptを独断量産しない(動線/型が立つ時だけ) | ✅PASS | concept18枚(source12387・比0.001)・bottom-up痕18 |
| C9 | 指針9 | 淡々＝煽り/絵文字過多をしない(brainの声のみ・引用ソースは逐語=対象外) | ✅PASS | brain-voiceに煽り/絵文字過多なし(引用は対象外) |
| I1 | §Ingest | index.md/log.md を維持＝取込を記録・カタログ化 | ✅PASS | index=True log=True |
| L2 | §Lint実挙動 | lintが実際に動いてる(stampが新しい＝存在でなく実行) | ✅PASS | last_lint 0h前(実行痕) |
| Q2 | §Query実挙動 | /wiki が実際に queries を蓄積してる(存在でなく稼働痕) | ✅PASS | queries 17枚(0なら未稼働) |
| R3b | 指針2/3 計測鮮度 | 死の分母tracker(base_rate/tracked)が凍結してない=最近更新されてる | ✅PASS | base_rate 最終更新 0.1h前（>6h=凍結=FAIL） |
| R3c | 指針3/6 死の計測整合 | 死の分母counter(base_rate.died)が実dead数(tracked.json)と一致＝正しく数えてる | ✅PASS | died=131=tracked実dead131(counter整合) / 台帳265型(型集約の学習サンプル=died≧台帳は正常) |
| H1 | 衛生/指針6 | concept が confidence frontmatter を持つ(主張の確信度を明示) | ✅PASS | 全conceptにconfidence有 |
| H2 | 衛生/前のめり防止 | 強い断定(確証/確定/必ず)が裏付け(⚠️/仮説/N)無しに先走ってない=型化バイアス防止 | ✅PASS | 裏付け無き断定なし(前のめり型化なし) |
| OP1 | 運用/パイプライン健全 | build_entities が成功して entity が新鮮(=合成パイプラインが crash してない) | ✅PASS | 最新player entity 0.3h前更新(135件)＝パイプライン稼働 |
| S1 | §Lint/指針7 | 内部 wikilink の切れ(指す先のwikiページが存在しない)を検出 | ⚠️WARN | 内部dangling 288件(上位: ['#$BELIVE（64oYF5U...）', '$$.GIF', '$6/26', '$AAIF', '$AAPL']) |
| S2 | ページ規約 | summaries/concepts/queries が必須frontmatter(type/title/created/updated/tags・summaryはsource)を持つ | ✅PASS | 対象39枚すべて規約準拠 |
