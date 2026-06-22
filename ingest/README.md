# ingest/ — 多層ingestエンジン（無料・鍵不要）

価値あるデータを多層で「たらふく」食わせる自走エンジン。ソースごとの adapter を足すだけで層が増える。
取得 → `sources/<layer>/` に保存（既存ファイル名でdedup＝新規だけ）→ commit。

## 対応ソース（現状・全部 無料/鍵不要）
| layer | 取得元 | 保存先 |
|---|---|---|
| `x` | watchlistの全アカ（`wiki/watchlist.md`の[[@handle]]）→ nitter RSS 優先 / syndication フォールバック | `sources/x/` |
| `news` | RSS：Decrypt / CoinDesk / Cointelegraph / Bankless | `sources/news/` |
| `onchain` | DefiLlama `/protocols`（24h変動の大きい上位＝動いてるプロトコル） | `sources/onchain/` |
| `reddit` | r/CryptoCurrency, r/solana（top/day RSS） | `sources/reddit/` |

## 使い方
```
node ingest/run.mjs --dry            # 取得して件数/サンプルだけ（保存しない）
node ingest/run.mjs --limit=5        # 各ソース上限5件
node ingest/run.mjs --only=news,reddit
node ingest/run.mjs                  # 全部 取得して保存
```

## 自走（無料cron）
`.github/workflows/ingest.yml` が **3時間ごと**に実行→新規を自動commit。
※ワークフローは **mainにmergeされて初めて動く**（ingestブランチ上では休眠）。

## 注意 / 既知
- X(syndication)は**バースト厳禁**＝IPレート制限あり。よって 700ms間隔＋nitter優先。レートに当たったらnitterで拾う。
- The Block / 一部はCloudflareで403＝除外。DefiLlama `/raises` は有料化したので未使用。
- 設計原則（[[CLAUDE]]）：**網羅（除外しない）/ 観測事実は出典付きで保存 / sources は生データ＝レビューはconcept合成側で**。

## これから足せる口（鍵 or 検証が要る）
- CryptoPanic（無料token）・Farcaster（Neynar無料枠）・Podcast全文（YouTube transcript 要検証 / Supadataは課金）。
- 足し方：`run.mjs` に `fetchXxx()` を1個書いて `all` に登録するだけ。
