# Trench-Brain システム構成（言語化＝構成図の元）

> crypto trench(memecoin) を **収集→観測→合成→判断→公開** する統合システム。
> 単一ソースでは見えない繋がりを **LLM Wiki** に合成し、「この launch は **ape か avoid か**」を出す。
> **全層 $0**（合成=サブスク / on-chain=無料API / 公開=cloudflared無料 / host=自宅Windows）。

---

## データフロー（1本の線・図の背骨）

```
[ソース]                [収集(門)]        [観測(決定的)]      [合成(LLM)]          [資産]              [脳API]                 [公開]
X(watchlist)  ─┐                                                                                                          ┌─→ ユーザー
pump.fun(全mint)┼─→ cloud GHA ──→ sources/ ──→ track.py ────→ Windows ────→ wiki/ ──→ rag.py(BM25索引) ──→ ui_server ──→│  (ブラウザ)
news           ┘   (門付き        (raw不変)    launch_stream  headless    (LLM Wiki  +知識グラフ         /api/* 31機能   cloudflared
on-chain           キュレーション)              live_pulse    claude cron  =合成知識)                    (read-only)     quick tunnel
(rugcheck/pump)                                 → state/                                                     │            → 公開HTTPS URL
                                                (観測事実)                                                   └─ /api/score: CA→on-chain(rugcheck/pump)
                                                                                                                 →LP除外+非LP top3.5%+insider→ape/avoid
```

**別系統（運用者専用）**: `ask.sh` = claude --print が全wiki横断・6レンズ・引用で深いQ&A（本人個人用・サブスク=$0・**公開には使わない**＝ToS/BANリスク）。

---

## レイヤ / コンポーネント（下から上）

**L0. ソース（raw・不変の真実源）**
- X(watchlist単位) / pump.fun(全mint) / news / on-chain(rugcheck・pump API)
- 保存: `sources/x/` 等（**読むだけ・改変しない**＝検証可能性）

**L1. 収集＝門付きキュレーション（firehose禁止）**
- cloud GHA が常時ON・**門**（watchlist門 / traction閾値 / KOL言及門）でraw を `sources/` へ
- 門＝自動フィルタのコード（無差別取得を禁止）

**L2. リアルタイム観測（決定的・LLM不使用・$0）**
- `track.py` / `launch_stream.py`: pump.fun **全mintを安く観測**→篩(scam門=rugcheck)→TRACKED→watch→合成キュー
- `live_pulse_writer.py`: 集約→`live_pulse.json`
- 出力: `brain/state/*`（`launch_queue.jsonl` / `base_rate.json` / `live_pulse.json` / `kol_track_records.json` / `health.jsonl`…）＝**観測事実の層**（gitignore=マシン毎ローカル）
- ★観測≠採用: 篩通過だけが合成に進む（死の分母=生存者バイアス対策）

**L3. 合成＝LLM Wiki化（Windows headless-claude cron）**
- Windows(WSL cron)が headless claude で合成キューを処理→`wiki/` の concept/entity に**永続化された合成知識**
- **両輪**: 収集を入れたら合成まで回す。健康=未合成 backlog 件数（scraper化の防止）

**L4. LLM Wiki（合成済み知識＝真の資産・地盤）**
- `wiki/` markdown: `concepts/`(横断合成) / `entities/tokens・players/` / `queries/` / `summaries/` / `dashboards/`
- 全ページ **[[wikilink]]** で知識グラフ / git同期 / Obsidian閲覧
- 現状: 約709ページ・concept孤立0・backlog3（=synthesisが収集に追いついてる健全状態）

**L5. 脳 / backend API（read-only・$0）**
- `rag.py`: **依存ゼロ Pure Python BM25** で合成wikiを索引（日本語=CJK bigram / $ticker完全一致boost）+ [[link]]知識グラフ。**生RAGでなく合成済みを検索**（芯維持）
- `ui_server.py`: `/api/*` **31機能**（`/api/index` が自己ドキュメント）
  - 知識: search / page / related / concepts / recent / tags / graph / similar / autocomplete / entity / sitemap
  - リアルタイム: live / hot / launches / feed
  - 判断: **score(ape-or-avoid)** / kol / base-rate / death-ledger / digest
  - Lint: contradictions / orphans / gaps / stats
  - intelligence: survivors / watchlist / themes / creator / meta(health/compare)
- **`/api/score`（核）**: rugcheck+pump の on-chain → **LP除外＋非LP top holder 3.5%階層＋insider**（[[@blknoiz06|Ansem]]公認の spyzercrypto guide 由来）→ ape/avoid verdict＋base-rate注記
- **read-only**（書かない＝Windows合成writerと非衝突）

**L6. フロント（UIチーム所有・俺は触らない）**
- `wiki/ui/index.html`(terminal UI) / `wiki/ui/wiki.html`(検索デモ)
- 6ビュー設計（`docs/ui-design.md`）: PULSE / **SCAN(ape-avoid hero)** / WIKI / PLAYERS / INTEL / ASK

**L7. 公開（serve.sh・$0）**
- `brain/serve.sh` = **launch_stream + live_pulse_writer + ui_server + cloudflared quick tunnel** を1本起動→公開HTTPS URL
- 全層(UI+API+realtime)が1コマンドで公開状態。read-only。
- 恒久URL=named tunnel（要Cloudflareアカ+ドメイン）/ 常時ON=service化

---

## マシン構成

| マシン | 役割 |
|---|---|
| **cloud GHA** | 収集（L1・常時ON） |
| **Windows (WSL)** | 合成の脳(L3) + リアルタイム観測(L2) + 公開host(L7)＝**唯一のwriter** |
| **Mac** | 解放済（cutover完了・writer停止） |
| ユーザー端末 | 公開URLを叩く（read-only消費） |

---

## コストモデル（全$0）

| 層 | 手段 | コスト |
|---|---|---|
| 合成 | Claudeサブスク(headless) | $0（定額・個人運用） |
| on-chain判定 | rugcheck / pump.fun 無料API | $0 |
| 検索 | CPU上のBM25 | $0 |
| 公開 | cloudflared quick tunnel | $0（恒久URLはドメイン~$10/年） |
| host | 自宅Windows(RTX4060Ti機) | 電気代のみ |

---

## 芯（憲法・設計原則）

1. **LLM Wiki = 収集と合成の両輪**（合成が収集に追いつく＝scraperでない）
2. **門付きキュレーション**（firehose恒久禁止・門=自動フィルタ）
3. **観測≠採用**（篩通過だけ合成／全mint観測は"篩の材料"）
4. **観測事実(state) と LLM判断(concept/score) の分離**
5. **single-writer**（Windows）/ **read-only serving** / 全ページ [[wikilink]] 接続
6. **矛盾は消さない**（⚠️矛盾旗で両論併記）
7. **公開が壊れても自分で使える**（local Markdown+git＝service非依存の資産）

---

*関連: [[docs/ui-design.md]](UI画面設計) / `/api/index`(API自己ドキュメント) / `CLAUDE.md`(憲法) / `docs/LLM-WIKI.md`(原典).*
