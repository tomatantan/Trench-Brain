---
name: selfheal
description: Trench-Brainの自己修復。合成(synthesis)が止まってないか診断し、止まっていれば原因を特定して直せる範囲は直し、直せない範囲は具体的にTelegramで報告する。.github/workflows/healthcheck.yml(検知・6h毎)の相方＝検知はGHAが無料でやる、実際に直すのはこのskill。
---

# selfheal

Trench-Brainは「収集(cloud GHA)」と「合成(ローカルsubscription、Mac/Windows)」の両輪。
収集は落ちにくいが、合成は**人間が動かしているホストが死ぬと誰も気づかず止まる**（2026-08-06、
Windows cron死亡から3週間超無検知で発覚した実例あり）。このskillはその再発防止＋実際の復旧。

## 手順

1. **診断**：以下を確認する。
   - `git status` で作業ツリーがcleanか。cleanなら `git pull origin main --ff-only` して
     origin/mainからどれだけ遅れてたか確認（遅れてる=このホストでcronが回ってなかった証拠）。
   - `brain/state/health.jsonl` の最終行の `ts` と現在時刻の差（何時間止まってたか）。
   - `git log --oneline -20` で直近commitのパターンを見る：
     `cloud-collect (GHA)` だけが並んでて `auto-collect (cron)` が無ければ、
     ローカル合成(cron_collect.sh)がそのホストで動いてない確定。
   - `brain/state/cron.log` の末尾（ローカルで動いてる形跡があるか）。

2. **直せる範囲は直す**（決定的・LLM不使用・タダの部分）：
   - `python3 brain/pipeline.py` を実行（digest→build_entities→worklist、health.jsonlを更新）。
   - これでhealth.jsonlの鮮度は復旧する。ただし**LLM合成そのもの**(worklistの中身を実際に
     entityページへ書き込む判断作業)は次項の通り人間の判断が要る領域＝このskillだけでは完結しない。

3. **合成本体は`brain/INGEST.md`の手順に従い、このセッション自身が続けて処理してよい**
   （このskillを呼んだセッションがそのままworklistを処理する＝止まってた分を自分の判断で埋める）。
   ただしバックログ全部を一気に飲まない。1サイクル=worklistのHOT分だけ（複利で積む設計）。

4. **直せない範囲**（そのホストで恒久的にcronが死んでる原因＝OS設定/launchd/Windowsタスクスケジューラ
   の話）は、このskillの権限外。診断結果を具体的にTelegramで報告し、人間の対応を仰ぐ。
   「直りました」は言わない——**health.jsonlが実際に更新された事実だけを報告する**。

## 出力フォーマット（Telegram報告）
- 止まっていた時間
- 原因（分かる範囲で：どのホストのcronが死んでいたか／不明なら不明と言う）
- 今回やった具体的な作業（pull何コミット分／pipeline実行／worklist何件処理）
- まだ残ってる問題（例：Windows cronの恒久修正は未着手、など）

## 呼び出しタイミング
- `.github/workflows/healthcheck.yml` がTelegramに警告を送ってきた時（人間が手動でこのskillを起動）。
- 定期的な念のためのセルフチェック（本人が明示的に依頼した時）。
- 自動起動はしない——このskill自体がLLM実行(=課金/サブスク消費)を伴うため、
  起動判断は人間 or 明示的なスケジュール設定に委ねる（GHA healthcheckは無料の検知専任のまま）。
