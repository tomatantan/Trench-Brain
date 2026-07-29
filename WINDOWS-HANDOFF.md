# WINDOWS-HANDOFF — Mac Claude ⇄ Windows Claude 共有黒板

> 2台のClaude Codeが**git経由で非同期にやりとりする**タスク箱。詳細な役割は [COORDINATION.md](COORDINATION.md)。
> **Mac Claude**: ここに `## TASK` を書いてpush。**Windows Claude**: 起動時/サイクル時に読み、TODOを実行→状態をDONEにし結果を追記→push。
> ルール: 各タスクに ID・状態(TODO/DOING/DONE/BLOCKED)・依頼者・結果欄。完了は必ず結果を書く。BLOCKEDは理由を書き本人に上げる。秘密情報は書かない（gitに乗る）。

---

## 使い方の例（このセクションは消さない・雛形）
```
## TASK-0001
- 状態: TODO
- 依頼: Mac Claude
- 日時: 2026-07-13
- 内容: <Windows Claudeにやってほしいこと・具体的に>
- 結果: <Windows Claudeがここに実行結果・完了時刻を書く>
```

状態の意味: TODO=未着手 / DOING=作業中 / DONE=完了(結果必須) / BLOCKED=詰まり(理由必須・本人へ)

---

## 現在のタスク

## TASK-0001
- 状態: TODO
- 依頼: Mac Claude
- 日時: 2026-07-30
- 内容: **★重要・破壊的操作の予告**。本人承認済みで、Mac Claudeがこのタスク追記の直後に **git履歴の書き換え**(`git filter-repo`で全ブランチから`wiki/`パスを除去=過去commitからも合成データの中身を消す)を実行し、`origin`の全ブランチ(main含む)を**force-push**する。理由: リポジトリをpublic化した際、`wiki/`(合成の資産本体)が過去コミットにも残っていたため完全に消す。
  実行後、**このMac(トレンチブレインのローカルclone)のcommit historyは全部ハッシュが変わる**＝Windows側の既存clone/ローカルhistoryと非互換になる。
  **Windows Claudeがやるべきこと**（次回起動/サイクル時にこれを読んだら即実行）:
  1. `cron_collect.sh`等の自動実行を一時止める(可能なら)。
  2. ローカルの `trench-brain` ディレクトリを**丸ごと再clone**するのが一番安全（例: 既存を`trench-brain.old`に退避 → `git clone https://github.com/tomatantan/Trench-Brain.git` で新規clone → `brain/state/`配下のgitignoreされてるlocal状態ファイル(cron.log等)は古い方から必要なら移植）。
  3. `wiki/` は2026-07-30から独立private repo(`Trench-Brain-wiki`)＝新規clone後に `cd wiki && git init && git remote add origin https://github.com/tomatantan/Trench-Brain-wiki.git && git fetch && git checkout main`。詳細は `brain/RUNBOOK.md` §7 / `COORDINATION.md` §7。
  4. 再clone後、cron_collect.shの自己修復ロジック(冒頭のpgrep起動チェック)は自動で再起動されるはず。念のため `bash brain/cron_collect.sh` を手動で1回叩いて正常終了を確認。
- 結果: <Windows Claudeがここに実行結果・完了時刻を書く>

## TASK-0002
- 状態: TODO
- 依頼: Mac Claude(本人指示2026-07-30「Windowsが少し怠けてる」)
- 日時: 2026-07-30
- 内容: **★TASK-0001より先にこれを診断して**。git履歴を見ると `auto-collect (cron)` commitが**2026-07-12T10:17Z以降ゼロ**＝Windows側のローカル自動収集/合成が**約18日間完全に止まっている**。このHANDOFFファイル自体も07-13の作成以来一度も編集されてない＝Windows Claudeがこの黒板を全く読みに来ていない可能性が高い。
  診断してほしいこと（優先順）:
  1. Windows端末/Windows Claudeセッション自体が起動しているか。
  2. `cron_collect.sh` を駆動しているタスク(Windowsタスクスケジューラ or 常駐プロセス)が生きているか・登録が消えていないか。
  3. `brain/state/cron.log` の末尾を見て、最後に走った時刻と、そこで止まった理由(エラー/例外/該当プロセスのkill跡)を確認。
  4. 止まってた原因を直したら、TASK-0001(履歴書き換え後の再clone)を先に片付けてから通常運転に戻す。
  5. 再開できたら、このタスクに結果(何が原因で・いつ復旧したか)を書いてpush。
- 結果: <Windows Claudeがここに実行結果・完了時刻を書く>
