# gap_prompt.md — headless LLM への指示書（wiki_gaps.json の保守的自動解決）

## タスク概要
`brain/state/wiki_gaps.json` を読み、各 gap を**保守的に**解決する。**1回で最大10件**処理する。

gap は `{"concept": "<target>", "referenced_by": ["<file>.md", ...], "first_seen": "..."}` の形式のリスト。
`concept` は dangling wikilink のターゲット（まだ存在しないページ名）。
`referenced_by` はそのリンクを含むwikiファイルのパス一覧。

## 決定ルール（この順で判定・最初に当たったルールで即決）

### ルール1: 履歴・生成物のみ参照 → leave
`referenced_by` が `log.md` / `index.md` / `*-report.md` などの **append-only 履歴ファイル・生成物のみ** の場合:
- **何もしない**。履歴は書き換えない。生成物は再生成されるもの。
- この gap を `resolved: history-leave` として `wiki_gaps.json` から除く。

### ルール2: live ページ参照 + 既存ページへの別名・case違い → re-point
`referenced_by` に `wiki/concepts/`・`wiki/entities/`・`wiki/summaries/`・`wiki/queries/`・`wiki/watchlist/`・`wiki/canon/`・`wiki/feeds/` 等の **live ページ** が含まれ、
かつ `concept`（dangling target）が既存の wiki ページに **case違い・別名・表記揺れで明らかに対応** している場合:
- 該当 live 参照元ページの `[[concept]]` を正しい `[[既存ページ名]]`（必要なら `[[既存ページ名|表示テキスト]]`）に書き換える。
- **編集対象は参照元の live ページのみ**。新しいファイルは作らない。
- この gap を resolved として `wiki_gaps.json` から除く。

### ルール3: live ページ参照 + wikiページ化すべきでない stray → de-link
`referenced_by` に live ページが含まれ、かつ `concept` が以下のいずれかに該当する stray な場合:
- メモリファイル名のような `trench-brain-*` パターン
- 方針削除対象の `player-*-thinking-pattern` 等のパターン
- 日付付き識別子 `*-YYYYMMDD` や `*-\d{6,8}`
- wikiの概念でない語（ファイル名・設定キー・スクリプト名・URL断片 等）

対応:
- 該当 live 参照元ページの `[[concept]]` を **角括弧を外した平文 `concept`** にする。
  または文脈上不要な短い言及なら自然に除去する。
- **編集対象は参照元の live ページのみ**。
- この gap を resolved として `wiki_gaps.json` から除く。

### ルール4: 判断がつかない / 本物の新概念かもしれない → 何もしない
上記 1〜3 のどれにも当てはまらない、または判断に迷う場合:
- **触らない・queueに残す**。
- ★**新しい concept ページを絶対に作らない**（憲法 指針8: bottom-up・エージェントが独断でページ量産しない）。

## 厳守事項
- 編集できるファイルは **`referenced_by` に挙がった live ページ** と **`brain/state/wiki_gaps.json`** のみ。
- `sources/` は読むだけ（書き込み禁止）。
- `log.md`・`index.md`・`*-report.md` は書き換えない。
- **新しい concept ページ・summary ページ等を新規作成しない**（指針8）。
- 迷ったら触らず残す（保守的）。淡々と処理する。

## 完了処理
- 処理済みの gap（resolved 分）を除いた残りで `brain/state/wiki_gaps.json` を上書きする。
  すべて resolved または history-leave なら空リスト `[]` を書く。
- 最後に必ず以下の1行を出力する:
  ```
  resolved N件(内訳: re-point A / de-link B / history-leave C) / 残 M件
  ```
