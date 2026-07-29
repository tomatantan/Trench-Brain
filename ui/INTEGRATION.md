# UI ↔ LLM Wiki 接続契約

## 読み取り

UIは次の順で1時間ごとの実データを読む。

1. `../ui-data.json`
2. `https://raw.githubusercontent.com/tomatantan/Trench-Brain/main/wiki/ui-data.json`

- 成功時: `Wiki: LIVE DATA`
- 失敗時: 内蔵モックへフォールバック
- `file://` ではブラウザ制約により取得できないため、HTTP配信が必要

## ユーザー入力

Brain Terminalの入力は、明示的な同意がある場合だけ学習候補へ追加する。
現在はブラウザ内に保存し、`Export Inbox`から以下のJSONを出力する。

```json
{
  "schema": "trench-brain-ui-inbox/v1",
  "exported_at": "ISO-8601",
  "status": "pending_agent_review",
  "items": [
    {
      "kind": "question | hypothesis | observation | correction",
      "text": "...",
      "time": "...",
      "context": "...",
      "source": "ui-brain-terminal"
    }
  ]
}
```

LLM側はInboxをレビューし、`query`または`ingest`対象として処理する。
UIから `sources/` や `wiki/` を直接変更しない。

## 未実装

- LLMへ質問を送るHTTP API
- 回答ストリーム
- Inboxのサーバー保存
- 人間承認後のWiki反映

## Brain Terminal 応答規約

1. 質問へ正面から回答する。
2. `concepts` と `sources` を横断合成する。
3. 各主張へ `[[出典リンク]]` を付ける。
4. Wikiに無い事実は「未収録」と明示する。
5. 回答本文と `⚠️要検証` を分離する。
6. 矛盾は両論併記し、消さない。
7. Hot判定の第一指標は独立した「言及アカ数」。いいね数は補助指標。
8. FTは思考様式・文体、事実取得はRAGとして分離する。
