# 憲法 conformance レポート（機械検査・自己採点でない）

PASS 17 / FAIL 0 / WARN 0 / 計17

| id | 指針/節 | 要件 | 判定 | 証拠/違反 |
|---|---|---|---|---|
| Q1 | §Query step3 | /wiki の価値ある回答を wiki/queries/ に資産化する | ✅PASS | assetize_query 定義&呼出あり / queries 1枚 |
| R1 | 指針1 | sources/ は読むだけ＝合成engineは sources/ を編集しない(収集/curationのみ可) | ✅PASS | 合成engineはsources/を編集してない(collect/add/imageのみ=curation) |
| R2 | 指針2 | 収集は門付き(watchlist/traction/KOL)・firehose禁止 | ✅PASS | watchlist門=6 scam門=6 firehose無し |
| R3 | 指針3 | 合成が収集に追いつく＝signal_backlogで健康を測る | ✅PASS | 最新signal_backlog=17（記録あり） |
| R7 | 指針7 | 全ページを wikilink で接続＝孤立ページが無い | ✅PASS | 孤立concept無し |
| L1 | §Lint | lint(健康診断)が稼働＝矛盾/孤立/ギャップを定期検出 | ✅PASS | synthesize_lint.sh + lint-report.md あり |
| OA1 | 指針2/6 観測≠採用 | 全mint観測(篩材料)≠採用(篩通過のみ合成) | ✅PASS | 観測コード=16 採用門コード=9 |
| C4 | 指針4 | 1ソース取込→複数ページに波及(synthesis) | ✅PASS | 波及指示あり・summary2+entity210枚 |
| C5 | 指針5 | 矛盾は消さず⚠️両論で保持する | ✅PASS | concept内 ⚠️/矛盾 60箇所・prompt指示あり |
| C6 | 指針6 | entityで観測(事実)と推論(判断)を分離する | ✅PASS | 観測/判断を分離した entity 75/210枚 |
| C8 | 指針8 | bottom-up＝conceptを独断量産しない(動線/型が立つ時だけ) | ✅PASS | concept15枚(source7026・比0.002)・bottom-up痕17 |
| C9 | 指針9 | 淡々＝煽り/絵文字過多をしない(brainの声のみ・引用ソースは逐語=対象外) | ✅PASS | brain-voiceに煽り/絵文字過多なし(引用は対象外) |
| I1 | §Ingest | index.md/log.md を維持＝取込を記録・カタログ化 | ✅PASS | index=True log=True |
| L2 | §Lint実挙動 | lintが実際に動いてる(stampが新しい＝存在でなく実行) | ✅PASS | last_lint 12h前(実行痕) |
| Q2 | §Query実挙動 | /wiki が実際に queries を蓄積してる(存在でなく稼働痕) | ✅PASS | queries 1枚(0なら未稼働) |
| R3b | 指針2/3 計測鮮度 | 死の分母tracker(base_rate/tracked)が凍結してない=最近更新されてる | ✅PASS | base_rate 最終更新 0.0h前（>6h=凍結=FAIL） |
| R3c | 指針6 矛盾 | base_rateのdiedと死亡台帳が矛盾してない(計測整合) | ✅PASS | died=9 / 死亡台帳4件(整合) |
