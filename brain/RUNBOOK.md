# Trench-Brain RUNBOOK — LLM Wiki 自動最適化パイプライン運用マニュアル

> 対象: 誰でも・どのモデル(Fable/Opus/Sonnet/ローカルLLM)でも同じ手順で運用できる。
> 失敗が沈黙しない・回復手順が明確 = foolproof を設計の柱とする。

---

## 1. これは何か

**LLM Wiki** とは、LLM が生ソースを読んで構造化・相互リンクされた永続マークダウン知識ベースを
少しずつ構築・維持し続けるパターン（`docs/LLM-WIKI.md` が原典）。
RAGとの根本的な違いは「合成が残る」こと——質問のたびにソースを再索引するのでなく、
取り込み時に合成した知識(概念ページ/entityページ)が複利で積み上がる。

Trench-Brain はこの LLM Wiki に、**自動最適化ループ**（dangling wikilink の機械修復・gap 合成・
合成出力の構造検証・憲法 conformance 検査）を加えた自己改善型パイプライン。
成長の律速は収集量でなく「**合成スループット**」（`brain/state/health.jsonl` の `signal_backlog` が健康指標）。

---

## 2. 1サイクルの全体像

`brain/cron_collect.sh` が1サイクルを定義する。Windows WSL cron が 3h 毎に実行する。

| ステップ | スクリプト / コマンド | 何のために |
|---|---|---|
| **自己修復** | `pgrep` + `nohup` (cron_collect.sh 冒頭) | caffeinate / wiki_bot / launch_stream が死んでたら即起動 |
| **pull rebase** | `git pull -q --rebase --autostash origin main` | cloud GHA の収集 push と分岐しないよう事前 sync |
| **X pipeline** | `python3 brain/pipeline.py` | digest → build_entities → worklist (鮮度ゲート §1a) を既存 `sources/x/` から生成。X 収集は cloud GHA 専任なので collect はしない（書き込みパス分離） |
| **YouTube 収集** | `python3 collector/collect_youtube.py --limit 1` | 長文(transcript) ローカル専任・1本/サイクル・門 `wiki/feeds.md` |
| **watchlist 拡張** | `python3 brain/expand_watchlist.py` | 引用グラフから候補を自動生成（人は承認のみ・指針2） |
| **① 決定的層** | `python3 brain/track.py run` | 全 pump.fun mint 観測 → 篩(traction+KOL) → `synth_queue.json` (LLM 不使用) |
| **② pump.fun 合成** | `bash brain/synthesize.sh` | `synth_queue.json` を headless claude が wiki に合成。空なら claude 未呼出(コスト0) |
| **② X 合成** | `bash brain/synthesize_x.sh` | worklist §1a 通過分を headless claude が合成。空なら skip |
| **player concept 掃除** | `rm -f wiki/concepts/player-*.md` | synthesize_x が量産した player 思考 concept を除去。entity が canonical（指針8） |
| **② 長文合成** | `bash brain/synthesize_longform.sh` | 未合成 transcript を 3本/サイクル deep 合成 |
| **② backfill 合成** | `bash brain/synthesize_backfill.sh` | 高 signal 未合成 stub を 5件/サイクル deep 合成。グラフ密度UP |
| **★ 自動最適化: autofix** | `python3 brain/wiki_autofix.py --apply` | dangling wikilink を3分岐（修復/gap積み/放置）で処理。上限50件・atomic・冪等 |
| **★ 自動最適化: gap 合成** | `bash brain/synthesize_gaps.sh` | `wiki_gaps.json` の concept-gap を headless LLM が保守的解決(最大10件/run)。空なら skip |
| **★ 合成出力門番** | `python3 brain/synth_validate.py` | 合成が触った wiki ページの frontmatter/synthesisブロック/失敗マーカーを機械検証。不正は `brain/state/synth_validate.out` + cron.log に loud 出力 |
| **lint** | `bash brain/synthesize_lint.sh` | wiki 自身の矛盾・孤立・陳腐化を敵対的に検出 → `wiki/lint-report.md` |
| **conformance 検査** | `python3 brain/check_conformance.py` | 憲法 9 指針を機械検査 → `wiki/conformance-report.md` + `brain/state/conformance.log` |
| **snapshot** | `python3 brain/snapshot.py` | 主要 metrics を dated append で蓄積(時系列) |
| **feedback 系** | `brain/feedback.py` / `brain/kol_track_record.py` / `brain/predictive_study.py` | KOL 実績・仮説検証・フィードバック学習 |
| **自律 read** | `bash brain/autonomous_read.sh` | trench を見て genuine notable な時だけ telegram push |
| **自律 research** | `bash brain/autonomous_research.sh` | 脳が自分で仮説立て → tracked data で検証 → corpus が自力で賢くなる |
| **UI export** | `python3 brain/export_ui.py` | entities + track 状態 → `wiki/ui-data.json` |
| **commit / push** | `git add <対象ファイル群>` + `git commit` + `git push` | local 所有物 (youtube/wiki/state) のみ add。`-A` 禁止(書き込みパス分離) |
| **wiki モバイルミラー** | `git subtree split` → force push → `Trench-Brain-wiki` | `wiki/` だけの軽量 repo を iOS Obsidian 用に更新 |

---

## 3. 自動最適化ループ（核心）

dangling wikilink を **沈黙で放置しない** 3ステップの自己修復ループ。

```
[全合成ステップ後]
         │
         ▼
┌─────────────────────────────────────┐
│ wiki_autofix.py --apply             │  ← 決定的3分岐（LLM不使用）
│                                     │
│  dangling wikilink を分類:          │
│  (a) 一意case/表記ゆれ → 自動修復  │  機械的・曖昧ゼロ
│  (b) kebab-case slug で実体なし     │  → wiki_gaps.json に積む
│  (c) $ticker/@handle/曖昧 → 放置   │  良性前方参照
└─────────────────────────────────────┘
         │ (b) concept-gap
         ▼
┌─────────────────────────────────────┐
│ synthesize_gaps.sh                  │  ← LLM が保守的解決（最大10件/run）
│                                     │
│  gap_prompt.md の決定ルール:        │
│  R1: 履歴ファイル参照のみ → leave  │
│  R2: live ページ + case違い → re-point（リンク書換） │
│  R3: live ページ + stray → de-link（平文化）        │
│  R4: 判断不能 → 触らず残す         │  ★新 concept 作成禁止（指針8）
└─────────────────────────────────────┘
         │ 合成出力
         ▼
┌─────────────────────────────────────┐
│ synth_validate.py                   │  ← 合成出力の構造門番
│                                     │
│  wiki/entities/ concepts/ summaries/ queries/ の │
│  変更ページを検査:                  │
│  1. frontmatter (先頭---・必須キー type/title)  │
│  2. synthesis ブロック均衡          │
│  3. 失敗マーカー ("api error"等)    │
│  4. 空ファイル / 未閉じコードフェンス │
│                                     │
│  出力: brain/state/synth_validate.out │
│  ★fail-safe: commit は止めない     │  queue が gitignore = revert でロス危険
│  → 不正を loud にログして沈黙 fail を根絶 │
└─────────────────────────────────────┘
```

**憲法境界**

| 処理 | 担当 | 根拠 |
|---|---|---|
| case/表記ゆれ修復 | 機械（wiki_autofix.py） | 決定的・曖昧ゼロ |
| gap の re-point / de-link | LLM（synthesize_gaps.sh） | 文脈判断が必要 |
| 新 concept ページ作成 | **人間のみ** | 指針8 bottom-up |
| 逸脱疑い・判断不能 | **人間に委ねる（残す）** | 保守的ポリシー |

---

## 4. どう動かすか

### 常駐（通常運用）

Windows WSL cron が 3h 毎に実行:
```cron
0 */3 * * * bash /Users/toma/trench-brain/brain/cron_collect.sh >> /tmp/trench-cron.log 2>&1
```

Mac は `caffeinate` で常時起き続ける（cron_collect.sh が自己修復で再起動）。

### 手動1サイクル実行

```bash
bash brain/cron_collect.sh
```

### 主要環境変数

| 変数 | 効果 | 既定値 |
|---|---|---|
| `SYNTH_MODEL` | 全合成スクリプト(synthesize.sh / synthesize_x.sh / synthesize_gaps.sh 等)が使う claude モデル | `sonnet` |
| `SYNTH_ENABLED` | `0` で pump.fun 合成(synthesize.sh)を無効化（課金を止めたい時） | `1` |
| `X_AUTH_TOKEN` / `X_CT0` | X web 内部 GraphQL API の cookie（無料収集経路） | .env |
| `TWITTERAPI_KEY` | twitterapi.io 有償 API キー（梯子の最終手段・手動 `--source twitterapi` でのみ使用） | .env |
| `TG_WIKI_BOT_TOKEN` / `TG_CHAT_ID` | watchdog.py の telegram 通知 | .env |

### 個別実行例

```bash
# X 収集経路の生死確認
python3 collector/collect.py --probe

# 収集: 梯子で全周（syndication → graphql）
python3 collector/collect.py --source auto

# build_entities 単体
python3 brain/pipeline.py

# autofix dry-run（ファイル書換なし・gap 記録のみ）
python3 brain/wiki_autofix.py

# conformance 検査単体
python3 brain/check_conformance.py

# watchdog 1回だけ実行して状態確認
python3 brain/watchdog.py --once
```

---

## 5. モデル可搬（どのモデルでも運用できる理由）

全合成は headless CLI 呼び出し:
```bash
claude --print --model "$SYNTH_MODEL" --dangerously-skip-permissions --strict-mcp-config \
  "$(cat brain/<prompt>.md)"
```

`SYNTH_MODEL` を書き換えるだけで別モデルに切り替わる。例:
```bash
export SYNTH_MODEL=opus   # Opus に切り替え
export SYNTH_MODEL=haiku  # 安価なモデルに切り替え
```

ローカル LLM に向ける場合でも、`synth_validate.py` が出力の構造を機械検証するため、
弱いモデルが壊れた frontmatter / 不均衡 synthesis ブロック / 失敗マーカーを吐いても
`synth_validate.out` に記録され、cron.log に `★synth_validate: 合成出力に不正検出` と loud に出る。
沈黙で壊れたページが積み上がることはない。

**★絶対に外してはいけないフラグ: `--strict-mcp-config`**

外すと headless claude がグローバル設定の telegram プラグインを起動し、
`getUpdates` は 1 トークン 1 ポーラー仕様のため、本人のチャンネル poller を SIGTERM で乗っ取って切断する。
（2026-06-23 フラッピング原因として特定済み。全合成スクリプトに必須。）

---

## 6. 絶対に失敗しない（foolproof）— 門番一覧

| 門番 | 何を検出するか | 出力先（沈黙しない） |
|---|---|---|
| **conformance R3d** (check_conformance.py) | X 収集の入口が凍結してないか。`brain/state/collect_health.json` の鮮度(12h閾値)を第一級ソースとして確認 | `wiki/conformance-report.md` + `brain/state/conformance.log` + cron.log |
| **conformance R3** (check_conformance.py) | `health.jsonl` の `signal_backlog` が bounded か(>50でWARN)。合成が収集に追いつかず scraper 化してないか | 同上 |
| **conformance S1** (check_conformance.py) | wiki 内の dangling wikilink 件数。wiki_autofix.py との連携で毎サイクル縮小が期待される | 同上 |
| **conformance S2** (check_conformance.py) | summaries/concepts/queries の必須 frontmatter(type/title/created/updated/tags、summaryはsource)の欠落 | 同上 |
| **conformance OP1** (check_conformance.py) | `wiki/entities/players/` の最新 mtime(12h閾値)。build_entities が crash すると古くなる | 同上 |
| **collect_health.json** | 収集 run 毎に `{ts, backend, new, errors, accounts}` を記録。R3d の第一級ソース | `brain/state/collect_health.json` |
| **synth_validate.py** | 合成が触った wiki ページの frontmatter/synthesisブロック均衡/失敗マーカー/空ファイル | `brain/state/synth_validate.out` + cron.log(`★synth_validate: 合成出力に不正検出`) |
| **health.jsonl** | 毎サイクル `signal_backlog`(未合成件数) + `corpus_ts`(最終合成 wall-clock) を append。時系列で backlog 増大を追跡 | `brain/state/health.jsonl` |
| **watchdog.py** | ui_server 応答 / live_pulse 鮮度 / launch_stream 活性 / public tunnel 到達 / 合成 backlog の5項目を2分毎に監視。flip(死↔復活)検知で telegram 通知 | `brain/state/watchdog_status.json` + `brain/state/watchdog.log` + telegram |

---

## 7. 障害と回復

| 症状 | まず確認する場所 | 対処 |
|---|---|---|
| **X 収集が止まった** (新ツイートが来ない) | `wiki/conformance-report.md` の R3d / `brain/state/collect_health.json` の `ok` フィールドと `backend` | `python3 collector/collect.py --probe` で経路生死確認。syndication が 429 常態化なら graphql cookie (`X_AUTH_TOKEN`/`X_CT0`) を .env に投入。有料 `TWITTERAPI_KEY` は手動 `--source twitterapi` でのみ使用 |
| **合成が壊れた出力を吐いた** | `brain/state/synth_validate.out` / cron.log 末尾の `★synth_validate` 行 | 該当ページを確認して手動修正。モデルを変えるか `SYNTH_ENABLED=0` で一時停止 |
| **backlog が増大している** | `brain/state/health.jsonl` の最新行 `signal_backlog` | 収集を絞る（収集 cron の間隔を伸ばす・watchlist を減らす）か、合成を増やす（`synthesize_backfill.sh` を追加 run） |
| **conformance 違反** | `wiki/conformance-report.md` の ❌ FAIL 行 | 各 check の「証拠/違反」列を読んで具体的に修正。R3d なら収集修復、S2 なら frontmatter 補完 |
| **`sources/x/` が大量 modified** (git status が数百件) | macOS 大小文字衝突の既知問題 | `git update-index --skip-worktree sources/x/*.md` で中和済（削除しない・レポジトリは健全）。再調査不要 |
| **build_entities が止まっている** | conformance OP1 が FAIL / `brain/state/cron.log` の pipeline 行 | `python3 brain/pipeline.py` を単体実行してエラーを確認。`wiki/entities/players/` の mtime で稼働確認 |
| **watchdog が死亡通知を出した** | `brain/state/watchdog_status.json` の `checks` 各項目 | 該当項目(ui_server/live_pulse/launch_stream/public_tunnel/synthesis)ごとに対処。watchdog 自体が死んだら cron_collect.sh の自己修復ロジックが起動する（冒頭 pgrep セクション） |
| **gap queue が増え続ける** | `brain/state/wiki_gaps.json` の件数 | `synthesize_gaps.sh` の claude エラーを cron.log で確認。gap が本物の新概念なら人間が判断（指針8・自動では新ページ作らない） |
| **`wiki/` へのpushが失敗し続ける／新規clone環境で `wiki/.git 未初期化` ログが出る** | 2026-07-30〜: `wiki/` は独立private repo(`github.com/tomatantan/Trench-Brain-wiki`)。mainリポ(public)はこのパスを追跡しない(`.gitignore`) | 新環境では `cd wiki && git init && git remote add origin https://github.com/tomatantan/Trench-Brain-wiki.git && git fetch && git checkout main`。認証は private repo への書き込み権限を持つ資格情報(gh/deploy key)が必要。`cron_collect.sh` は main側pushの後に `wiki/` 内で別途add/commit/push する(独立ステップ・失敗してもmain側は無事) |

---

## 8. 運用チェックリスト

定期的に以下を確認する（優先度順）:

1. **`wiki/conformance-report.md`** — ❌ FAIL があれば即修正。⚠️ WARN は傾向を見る。特に R3d(収集入口)・R3(backlog)・OP1(パイプライン) は最重要。

2. **`brain/state/health.jsonl` 末尾** — `signal_backlog` の増加傾向。非増加 = 正常。増え続けるなら収集過多のサイン（指針3: 合成と両輪）。

3. **`brain/state/watchdog_status.json`** — `all_ok` が false なら `checks` を見て原因特定。

4. **`brain/state/cron.log` 末尾** — `★` マーク行（synth_validate 不正・conformance 違反・push 失敗）を確認。

5. **`brain/state/synth_validate.out`** — 合成出力に不正があった場合のページ別詳細。

---

> 憲法原典: `CLAUDE.md`（9指針）/ `docs/LLM-WIKI.md`（LLM Wiki 概念）/ `brain/CORE-CHECK.md`（芯チェック）
> 機械門番の実装: `brain/check_conformance.py` / `brain/synth_validate.py` / `brain/wiki_autofix.py`
