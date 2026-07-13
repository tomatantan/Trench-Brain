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
（まだ無し。Mac Claudeが必要時にここへ `## TASK-NNNN` を追記する）
