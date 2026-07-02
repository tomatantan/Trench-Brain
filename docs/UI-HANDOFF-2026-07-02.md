# UIチーム向け 引き継ぎレポート — 2026-07-02

作成: backend/audit 側（Fable）。**このレポートは提案です。UIファイル（`wiki/ui/` 配下）は backend 側で編集していません**。
独立監査で `wiki/ui/{index.html, app.js, wiki.html, styles.css, INTEGRATION.md}` の各 `fetch` を backend の
`brain/ui_server.py` のルート定義と1個ずつ照合しました。全て実コードで検証済みです。

backend 側は**すでに全API（31機能・`/api/ask` 含む）が実装・稼働可能**な状態です。表側を繋ぐだけで芯が出ます。

---

## 🔴 最重要 — メインUIのチャットが実脳に繋がっていない

**症状**: 公開URLの `/` → `/ui/index.html` に来たユーザーがチャットに打つ質問は、本物の脳に届きません。
`wiki/ui/app.js` に `/api` を叩く箇所が**1つもありません**（grep確認）。チャット送信は `answer()`（app.js:212〜）を
呼ぶだけで、これは `ui-data.json` の signals に対する**クライアント側キーワードマッチ**で定型文を返すモックです
（`setTimeout(…,300)` で"考えているフリ"も入っています）。

**なぜこうなっているか（根本原因）**: `wiki/ui/INTEGRATION.md:39` の「## 未実装」に
「LLMへ質問を送るHTTP API」と書かれていますが、**これは既に実装済みです**（`brain/ui_server.py:625`）。
ドキュメントの記述が実装に追いついておらず、その誤契約を信じてチャットがモックのまま据え置かれています。

**直し方（バックエンドは準備済み・フロントの差し替えだけ）**:
```js
// app.js の answer(question) を実脳呼び出しに置換するイメージ
async function answer(question) {
  const res = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  const data = await res.json();        // { ok, answer, ... }
  if (!data.ok) throw new Error(data.error || 'ask failed');
  return data.answer;
}
```
**注意点（UX必須）**:
- `/api/ask` は headless の合成（6レンズ横断＋引用）を回すため**最大240秒**かかります。→ 送信直後に
  ローディング表示＋送信ボタン disable が必須（今の300msフェイクとは体感が別物）。
- レート制限 429 が返ることがあります（`{ ok:false, error:"rate limit…" }`）。429時のリトライ/待機メッセージを。
- 公開の既定バックエンドは Gemini です（安全）。`/api/ask` はそのまま叩けます。

**契約の真実源**: `GET /api/index`（`ui_server.py:66〜`）が全エンドポイントを自己ドキュメントしています。
`INTEGRATION.md` の「未実装」節はこれに合わせて更新してください（`/api/ask` は実装済みへ）。

---

## 🟠 唯一動く検索UI(wiki.html)がどこからも辿り着けない

`wiki/ui/wiki.html` は `/api/search?q=…&k=12` に正しく配線され、ヒットをクリックすると静的Markdownを
取得して表示します（backend と完全整合・**ここは動作OK**）。ところが `index.html`/`app.js` から wiki.html への
**リンクが1つもありません**（grep: 0件）。`serve.sh` は「検索デモ = /ui/wiki.html」と案内しているのに、
`/` に来たユーザーは導線ゼロで、唯一機能している検索UIに到達できません。
→ index.html に wiki.html への動線（ナビ/ボタン）追加を推奨。

---

## 🟡 取得データの大半が非表示divに書き捨てられている

`app.js` の `renderMetrics/renderSignals/renderIntel/renderLaunches` と post-ticker は、40 signals・60 launches・
base_rate funnel を取得・整形した上で、`index.html:94〜105` の `<div class="hidden-support" aria-hidden="true">`
（`styles.css:685` で `display:none!important`）に書き込んでいます。可視なのは hot-ticker とチャットのみ。
＝**表示している情報 < 取得している情報**。v1/v2/v3 の名残 scaffold と思われます。見せる意図があるなら unhide、
隠す意図なら fetch も止める、のどちらかに寄せると綺麗です。

---

## ⚪ 軽微（時間がある時に）

- `wiki.html:59,84` の `fetch` に timeout/AbortController がありません。トンネルが遅い/詰まると「検索中…」の
  まま無言で固着します（`app.js` の `connectData` は 3s abort を持っているので非対称）。→ AbortController 追加推奨。
- `wiki.html:52` の `esc()` は `& < >` のみで**引用符を無エスケープ**。`mdToHtml` が属性値 `data-t="${esc(t)}"` に
  wikilink target を入れるため、`[[a"onmouseover=…]]` 形の本文があると属性を抜けて注入余地（wiki本文は準信頼なので低）。
  公開する以上、`app.js` の `escapeHtml`（quote もエスケープ）と同等に揃えるのを推奨。
- `assets/login-room-source-v1.png`（1.6MB）を login gate で即時ロード＝モバイル/低速で初回描画が重い（lazy/webp化余地）。
- `assets/trenching-brain-hero.png`（2.1MB）は現行UIから**未参照**（archive のみ）＝デッド資産。`wiki/ui/archive/`（v1/v2/v3・計2.2MB）も現行外。整理候補（削除は人間確認で）。
- `app.js:209` に文字化け（`繝ｻ`＝壊れた中黒）。出力先が現状不可視なので今は見えませんが、unhide すると露出。
- `index.html:48〜55` のカテゴリフィルタに `FIGURE`/`X BUZZ` がありますが、`app.js` の `inferType` が生成する type に
  該当が無く、選ぶと必ず "No signals" になります。

---

## ✅ 問題なしと確認した点（誤解防止）
- `app.js:1` の GitHub raw URL は実 remote と一致（バグではない）。
- `../ui-data.json` は実在し、読み取りキー（`signals/live/base_rate/generated_at`）は実データと一致。
- wiki.html → `/api/search` のパス・パラメータ・レスポンスキー・静的MD配信パスは全て backend と整合。
- **localhost:8000 の決め打ちは live 4ファイルに無し**＝相対/正しい絶対URLのみ＝cloudflare 公開で壊れません。CORS も同一オリジンで問題なし。

---

## まとめ（優先度）
1. **chat → `/api/ask` を繋ぐ**（+ローディング/429対応）＝芯の「対話できるLLM Wiki」が表に出る。最優先。
2. **INTEGRATION.md の「未実装」を実装済みへ更新**（1の誤契約の解消）。
3. **index.html から wiki.html への動線**を追加（唯一動く検索UIを見せる）。
4. 非表示divの方針決め（見せる/fetch止める）。
5. 軽微（timeout・quoteエスケープ・画像最適化・archive整理）。

backend 側の追加作業は不要です（`/api/ask` 含め全て稼働可能）。不明点は `GET /api/index` が真実源です。
