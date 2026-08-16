---
type: config
title: sources/yajuscan — 受け入れ規約
---

# sources/yajuscan/

YAJUscan(Windows側で開発中の検知bot・pre-bondカーブ加速検出+コールアウトAPI+影運転)の**日次サマリ**を受け入れるsource。

個別検知(candidate単位)は既に `/api/detect` webhook 経由で `brain/state/detections.jsonl`(local/gitignore)に入り、
`brain/detect_track_record.py` が `source: "yajuscan"` として自動でsource×verdict集計に乗っている(2026-08-16時点で
稼働確認済み・`yajuscan:AVOID` n=1 / `yajuscan:REVIEW` n=4を`brain/state/detect_track_records.json`で確認)。
このディレクトリは**それとは別の、日次サマリ(検問成績・影運転の当日結果等のまとまった報告)**を受ける場所。

## 書き込み規約(CLAUDE.md 指針1準拠 — sourcesはraw・書いたら不変)
- ファイル名: `yajuscan__YYYY-MM-DD.md`(1日1ファイル)
- frontmatter:
  ```
  ---
  type: source
  platform: bot
  outlet: yajuscan
  captured: <UTC ISO timestamp>
  tags: [trench, source, yajuscan, detect-bot, auto-collect]
  ---
  ```
- 本文: その日の検知件数・影運転($1,000バンクロール想定の当日成績)・候補の質の変化など、Windows側が
  自然文/箇条書きで書いたものをそのまま保存(原文保持。要約はwiki側=synthesisの仕事)。

## ここに置いた後どうなるか(現状・正直に)
書き込み自体は受け入れる(このREADME設置=承諾)。**ただし自動synthesisへの配線はまだ無い**——
sources/news・sources/xは専用collector+pipeline.pyが拾って合成に回してるが、sources/yajuscan/は
今のところそのフックが無い。当面は蓄積されるだけ。定期的に(または溜まってきたら)`wiki-ingest`skill
または手動セッションで拾って `wiki/dashboards/` に検知bot成績表(kol-track-records.mdのbot版)として
合成するのが妥当な形——★これは次のタスクとして別途着手する。
