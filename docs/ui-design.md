# Trench-Brain UI 設計図（backend 31機能 → 画面/動線）

> UIチーム向けの **設計青写真**。フロント実装はUIチーム。これは「31個の `/api/*` 機能をどう画面・動線に落とすか」を定義する。
> backend は `brain/ui_server.py`（read-only・$0）。全機能カタログは **`GET /api/index`** が返す（自己ドキュメント）。
> 既存の CRT/terminal 美学（`crt-screen`/`terminal-panel`/login gate）は壊さない＝その中に live API を流し込み、核となる動線を足す。

---

## 0. 前提と北極星

- **核の決定（本人のedge）＝「この launch/token は ape か avoid か」**。UI全体はこの判断に奉仕する。→ **SCAN ビューが hero**。
- **公開は $0**（本気公開）。下記の大半は **クエリ時LLM不要**（合成済みwiki＋state を読むだけ）＝concurrency壁なし。LLMが要るのは `ASK` のみ（別扱い・§7）。
- **案A「検索できるLLM Wiki」**＝合成済みページを検索して読む。クエリ時LLM不要で最も芯に忠実。→ **WIKI ビュー**。
- データは**静的 ui-data.json から live `/api/*` へ移行**（鮮度が上がる）。ui-data.json は fallback に残してよい。

---

## 1. 情報設計（IA）= 6ビュー + ヘッダ

terminal の中に **ビュー切替**（タブ or サイドナビ）を置く。既存の単一ダッシュボードを下記6つに整理:

| ビュー | 役割 | 主要 API |
|---|---|---|
| **PULSE**（home） | 今のtrenchの脈 | `feed` `hot` `themes` `digest` |
| ★**SCAN**（hero） | ape-or-avoid 判定 | `score` `entity` `related` `creator` `autocomplete` |
| **WIKI** | 検索できるLLM Wiki | `search` `page` `related` `concepts` `graph` `similar` `sitemap` |
| **PLAYERS** | KOL信頼 | `kol` `entity`(player) |
| **INTEL** | メタ/地盤 | `base-rate` `death-ledger` `survivors` `stats` `contradictions` `health` |
| **ASK** | 深いQ&A(LLM) | `ask`（§7・別扱い） |

ヘッダ常設: 時計/接続表示(既存)・`autocomplete` 付きグローバル検索ボックス（どのビューからでも SCAN/WIKI に飛べる）・`/api/health` の鮮度インジケータ（**user向けには"鮮度"表現に留め、backlog等の内部語は出さない**）。

---

## 2. PULSE（home）= 今の脈

1リクエスト `GET /api/feed` で大半を描ける（hot+直近launch+最近更新wiki+themes）。補助に `hot` `digest`。

```
┌─ PULSE ─────────────────────────────────────────┐
│ 🔥 今動いてる (hot・変化pct順)                      │
│   $DEADSEM +208%   Hero Dog +122%   ...           │  ← /api/hot or feed.hot
│ 🧭 ナラティブ分布 (themes バーチャート)              │  ← feed.themes
│   animal/pet ███ tech/meme ██ AI/agent ██ ...     │
│ 🆕 直近launch  $X (rc_score) / $Y / ...           │  ← feed.recent_launches → クリックで SCAN
│ 📊 何が変わった (digest)  死亡+4 台帳+4 mints+300  │  ← /api/digest
│ 📝 最近の合成 (recent_wiki) → クリックで WIKI       │  ← feed.recent_wiki
└──────────────────────────────────────────────────┘
```
- hot/launch の各行は **クリックで SCAN へ**（その銘柄を判定）。
- digest は「先週/昨日から何が動いたか」を淡々と（煽らない）。

---

## 3. ★SCAN（hero）= ape か avoid か

**この製品の核**。CA か $ticker を入れたら「張る/避ける」が即出る。

```
┌─ SCAN ──────────────────────────────────────────┐
│ [ CA か $ticker を入力      ] 🔍 (autocomplete)   │  ← /api/autocomplete
├──────────────────────────────────────────────────┤
│  判定: ⛔ AVOID / ⚠️ 要注意 / ◽赤旗なし            │  ← /api/score .verdict
│  赤旗: 保有集中 top58% / mint権限残存 / ...         │  ← score.flags
│  on-chain: mcap $5.6k / rugged:false / insiders   │  ← score.onchain
│  ⚖️ base-rate: 門通過でも約69%が死ぬ＝赤旗無し≠安全 │  ← score.base_rate_note（必ず出す）
├── 文脈（合成知識） ──────────────────────────────│
│  📄 合成ページ(entity.markdown)                    │  ← /api/entity
│  🔗 関連concept: [[rug-anatomy]] [[launchpad-経済]]│  ← entity.related（クリックでWIKI）
│  👤 creator履歴: 3トークン目=連続rugger疑い         │  ← /api/creator (serial_flag)
└──────────────────────────────────────────────────┘
```
**設計原則（核）**:
- **観測事実(on-chain) と 判定(verdict) を視覚的に分ける**（指針6＝事実とLLM/ルール推論の分離）。
- **base_rate_note を必ず表示**＝"赤旗なし"を"安全"と誤読させない（正直）。verdictは断定でなく risk-lean。
- 関連conceptは `[[link]]` で WIKI に繋ぐ＝根拠が辿れる（citations）。

---

## 4. WIKI = 検索できるLLM Wiki（案A）

クエリ時LLM不要・$0。`search`→`page`→`related`/`graph` で「検索→読む→辿る」。

```
┌─ WIKI ──────────────┬───────────────────────────┐
│ [検索ボックス]🔍     │  📄 合成ページ (page.markdown) │  ← /api/page
│ 結果(search):       │     # 型: rug の解剖 ...      │
│  ・型 rug解剖 [score]│     本文(md→HTML)...          │
│  ・$CAFE ...        │  🔗 外向き/内向きリンク(related)│  ← /api/related
│  ・@crediblecrypto  │     [[onchain-verification]]  │  → クリックで再検索
│ 📚 concept目次       │  🕸️ グラフ表示(graph)         │  ← /api/graph (nodes/edges)
│  (/api/concepts)    │  🔎 類似(similar)            │  ← /api/similar
└─────────────────────┴───────────────────────────┘
```
- `[[wikilink]]` クリック → その語で再検索 or その page を開く。
- `/api/graph`（nodes/edges・concept/query/player）で知識グラフを可視化（任意・力指向グラフ）。
- `/api/sitemap` で全ページ一覧（ナビ/サイトマップ）。

---

## 5. PLAYERS = KOL信頼

```
┌─ PLAYERS ───────────────────────────────────────┐
│ KOL信頼ランク (death_rate昇順)                     │  ← /api/kol
│  @badattrading  call116 / dead64 / 生存率36%       │
│  ... (min評価数でフィルタ)                          │
│ → クリックで player の合成ページ (entity)           │  ← /api/entity?name=@x
└──────────────────────────────────────────────────┘
```
- 「語られてる≠良い」を体現＝track-record を前面に（KOL-CA の裏取り思想）。

---

## 6. INTEL = メタ/地盤

```
┌─ INTEL ─────────────────────────────────────────┐
│ 📉 base-rate funnel: mint67k→通過491→grad353/死337 │  ← /api/base-rate
│ ⚰️ death-ledger: 死337 / 生存率 / 死分母           │  ← /api/death-ledger
│ 🏆 survivors: graduated&生存 token (traction先頭)  │  ← /api/survivors
│ ⚠️ 矛盾: ⚠️矛盾旗の立ったページ81件                 │  ← /api/contradictions（矛盾の表面化）
│ 📊 wiki統計: 660ページ/links5594/orphans202        │  ← /api/stats
│ 💚 脳の鮮度（"最新更新N分前"等・内部語は出さない）   │  ← /api/health
└──────────────────────────────────────────────────┘
```

---

## 7. ASK = 深いQ&A（LLM・別扱い）

既存 chat（`chat-form`/`chat-log`）。`POST /api/ask`＝claude が全wiki横断・6レンズ・引用で合成回答。
- ★**唯一 LLM を使う＝公開コスト/同時接続の論点がここだけに集中**。public で $0 を貫くなら: (a) 無料クラウドAPI(Gemini/Groq)に差し替え (b) ローカルLlama (c) BYOK。→ 別途決定（`brain/ui_server.py` の `/api/ask` の backend を差し替えるだけ）。
- 出力規律は既に `ASK_UI=1`（内部jargon禁止・具体先行・"待ち"で終わるな・捏造禁止）。

---

## 8. 全ビュー共通の設計原則（憲法のUI適用）

1. **淡々・煽らない・絵文字過多なし**（指針9）。数字とverdictで語る。
2. **答えは出典に根ざす**＝`[[ページ]]`/関連を必ず辿れる（citations）。
3. **user-facing で内部語を出さない**（corpus/backlog/death_ledger/scam reject率/N窓… は禁止＝"ゴミ"教訓）。APIは生データを返すが、**UIが人間の言葉でラベルする**。
4. **障害を見せない**＝API失敗時は不安にさせない（"取得できません"でなく前回値/控えめ表示）。
5. **観測事実 と LLM/ルール判定 を分離表示**（指針6）。特に SCAN。
6. **base-rate を常に添える**＝"赤旗なし"を"安全"と誤読させない（正直）。

---

## 9. 実装メモ（UIチーム向け）

- backend: `python3 brain/ui_server.py [--port 8000]`。`GET /api/index` で全31機能(path/method/params/desc)。
- 全 GET は read-only・JSON `{ok, ...}`・CORS有。`ok:false` 時は `error`。
- 静的 `wiki/ui-data.json` は fallback に残してよいが、**live は `/api/*` を主に**。
- 既存の `wiki/ui/index.html`/`app.js` を拡張する形でよい（このdocは設計提案・実装の自由度はUIチーム）。
- 参考デモ: `wiki/ui/wiki.html`（俺が作った検索フロントの最小例＝案Aの動く参考）。

---

*この設計は backend 側(Claude)からの提案。優先実装は **SCAN(hero=ape/avoid)** → **PULSE(home)** → **WIKI** の順を推奨（核→脈→知識）。*
