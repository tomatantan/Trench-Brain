# 憲法 conformance レポート（機械検査・自己採点でない）

PASS 7 / FAIL 0 / WARN 0 / 計7

| id | 指針/節 | 要件 | 判定 | 証拠/違反 |
|---|---|---|---|---|
| Q1 | §Query step3 | /wiki の価値ある回答を wiki/queries/ に資産化する | ✅PASS | assetize_query 定義&呼出あり / queries 1枚 |
| R1 | 指針1 | sources/ は読むだけ＝合成engineは sources/ を編集しない(収集/curationのみ可) | ✅PASS | 合成engineはsources/を編集してない(collect/add/imageのみ=curation) |
| R2 | 指針2 | 収集は門付き(watchlist/traction/KOL)・firehose禁止 | ✅PASS | watchlist門=6 scam門=6 firehose無し |
| R3 | 指針3 | 合成が収集に追いつく＝signal_backlogで健康を測る | ✅PASS | 最新signal_backlog=5（記録あり） |
| R7 | 指針7 | 全ページを wikilink で接続＝孤立ページが無い | ✅PASS | 孤立concept無し |
| L1 | §Lint | lint(健康診断)が稼働＝矛盾/孤立/ギャップを定期検出 | ✅PASS | synthesize_lint.sh + lint-report.md あり |
| OA1 | 指針2/6 観測≠採用 | 全mint観測(篩材料)≠採用(篩通過のみ合成) | ✅PASS | 観測コード=16 採用門コード=9 |
