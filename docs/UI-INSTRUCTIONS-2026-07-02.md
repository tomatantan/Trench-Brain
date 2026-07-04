# UIチームへ全指示 — chatを「本物の脳」に繋ぐ (2026-07-02)

宛先: UI担当（`wiki/ui/` オーナー）。作成: backend担当(Fable)。
これ1枚で自己完結。backend側は**完了済み**。UIに残るのは**chatの配線1本**だけ。

---

## 0. TL;DR（これだけ読めば動ける）
- **今のchatはゴミ**。理由＝サーバーの脳を叩かず、**クライアント側のモック関数**(`ui-data.json` を読んで文字を組むだけ)で"それっぽい嘘"を返している。
- **backendの本物の脳は完成・稼働確認済み**。`POST /api/ask` を叩けば全wiki横断の合成回答が返る（下に実物）。
- **UIがやること = 1つ**: chat送信を、モック関数から `fetch('/api/ask', {method:'POST', body:{question}})` に差し替える。これでゴミが本物になる。
- それ以外のAPI（検索・スコア・ページ）は既に動いている。触らなくていい。

---

## 1. 何がゴミか（診断・証拠つき）
ユーザーが見た chat 出力:
```
$PEPE / 25件の言及 / 5アカウント
Inference: [観測と一字一句同じ文字列のコピペ]
```
**tell（決定的証拠）**: 「Inference（推論）」欄が「Observation（観測）」欄の**完全コピー**。
これは合成ではなく、クライアント側で `signals` 配列を数えて並べ替えただけ。LLMを一度も呼んでいない。
＝`app.js` の `answer()` 系ローカル関数が `ui-data.json` を読んで組み立てている。**これを消す/バイパスするのが仕事**。

---

## 2. 本物の脳は動く（backend完了の証拠）
同じ問い「今トレンチで一番熱いナラティブを一つ」を **`/api/ask`（実脳）** に投げた実結果:

> $ANSEM（"The Black Bull"、Ansem本人がpump.fun発行）が今一番熱い。
> ・本人が供給58.7%を保持したまま急騰、24h出来高でpump.fun全体トップ級($44M+)・Moonshot verified済み。
> ・読みが真っ二つ：CredibleCryptoは「人為的低float・新cycle到来ではない」と否定、bull_bnbは$MYX/$COAI等と同型の「MM execution」として容認・敬意、DefiIgnasは「attentionのトークン化」＝一過性casinoでtokenized stocksを本命視。
> ・便乗コピー群($ANSEMTRENCH/$ANSEMHOUSE/$ANSEMWHEEL等)は軒並み即死＝本家とコピーの生死が明確に分岐。
> ⚠️ 強気物語の発信源自体が供給の過半を握る本人＝利益相反構造は残ったまま。
> 根拠: [[$ANSEM]] [[rug-anatomy]] [[launchpad-economics]] [[manipulation-playbook]]

＝複数KOLの対立を両論併記・便乗コピーの生死・利益相反フラグ・引用[[wikilink]]付き。
**これが本物のLLM Wiki**。UIがこの文字列を表示するだけで、chatは一気に一級品になる。

---

## 3. やること（唯一の変更）

### 3-1. API contract（backendが保証する形）
```
POST /api/ask
  Content-Type: application/json
  body: {"question": "ユーザーの問い(string)"}

成功: 200 {"ok": true, "answer": "……合成回答(markdown/日本語, [[wikilink]]含む)……"}
失敗:
  400 {"ok": false, "error": "empty question" / "bad request"}
  429 {"ok": false, "error": "rate limit(ask) — 少し待って"}   ← askは重いので厳しめ(短window5回)
  500 {"ok": false, "error": "脳が応答を返せませんでした" / "内部エラー"}
  504 {"ok": false, "error": "脳の応答タイムアウト(>240s)"}
```

### 3-2. 実装（app.js — モックを捨ててこれに）
```js
async function askBrain(question) {
  const res = await fetch('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  const data = await res.json().catch(() => ({ ok: false, error: '応答が読めません' }));
  if (!res.ok || !data.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data.answer;               // ← これをそのまま chat バブルに描画
}
```
- chatの送信ハンドラを `answer()`（ローカルモック）から `askBrain()` に差し替える。
- `answer` は markdown。`[[wikilink]]` は残す（トレーダーの引用元＝価値。リンク化できるなら `/ui/#/page/<slug>` へ、無理なら文字のまま表示でOK）。

### 3-3. UX（脳は遅い・落ちる前提で組む）
1. **loading必須**: `/api/ask` は headless LLM＝**30〜240秒**かかる。送信直後に入力欄をdisable＋「脳が全wikiを横断中…（最大数分）」のスピナー。返ってきたら解除。
2. **timeout**: fetchに `AbortController`（例 250秒）を付け、504/中断時は「脳が時間内に返せませんでした。問いを短く・具体的に」と表示。
3. **429**: 「連投しすぎ。少し待って」を出してボタン一時disable。
4. **エラーは正直に**: モックにフォールバックして"嘘"を返すのは**禁止**（それが今のゴミの正体）。失敗は失敗と表示する。
5. 空`answer`(500)も同様にエラー表示。

---

## 4. backend側は完了済み（UIは前提にしてよい）
- `brain/ui_server.py`＝read-only backend、**31 API稼働**。`/api/ask`(脳)・`/api/search`(全文BM25)・`/api/score`・`/api/page` 等。
- `/api/ask` は `brain/ask.sh`（実脳）を叩く。**稼働確認済み**（§2が実結果）。
- read-onlyなのでWindowsの合成writerと衝突しない（wikiを読むだけ）。
- **ホスティングはWindows（常時ON機）の仕事**。Macでは serve しない（Mac依存に逆戻りするから）。UIは同一オリジンの `/api/*` を叩けばよい＝**APIのURLをハードコードするな**（相対パス `/api/ask` のまま）。

### ★backend担当への確認事項（1つだけ・toma経由でOK）
`/api/ask` の**既定backendは Gemini**（無料・公開ToS安全）で、これは `GEMINI_API_KEY` を要求する。
- 公開運用で Gemini を使うなら → Windows の serve 環境に `GEMINI_API_KEY` を設定（.envではなく環境変数）。未設定だと `/api/ask` が500を返す。
- キー無しで即動かすなら → serve時に `ASK_BACKEND=claude` で起動（運用者のclaude購読を使う。§2のテストはこれ）。
- **どちらにするかは運用判断**。UIコードは同じ（`/api/ask`を叩くだけ）＝この選択でUI実装は変わらない。

---

## 5. やってはいけない
- モックへのフォールバックを残す（=ゴミが再発）。失敗は正直にエラー表示。
- APIのURLをハードコード（`http://localhost:8000` 等）。相対 `/api/*` を使う＝Windows公開でそのまま動く。
- backendファイル（`brain/`）を触る。UIは `wiki/ui/` だけ。API仕様の疑問はtoma経由でbackend担当へ。

---

## 6. 完了の定義（これが満たせたら本物）
1. chatに「今何が熱い」と打つ → §2のような**横断合成＋引用付き**回答が出る（$PEPEコピペのゴミが消える）。
2. loading中はスピナー、失敗時は正直なエラー（嘘を返さない）。
3. `[[wikilink]]` が回答に残っている（＝合成の証拠）。
