# collector — 「貯める仕組み」

Trench-Brain の収集エンジン。[[wiki/watchlist]] の監視アカウントを
X 公式 **syndication endpoint(認証不要・無料)** でポーリングし、新規ツイートを
`sources/x/<author>__<tweetID>.md` に1枚1ノートで保存する。

## 特徴
- 外部API・キー不要。Python 標準ライブラリのみ(GitHub Actions でも `pip install` 不要)。
- 重複判定は**ファイル存在**で行う(状態ファイル不要)。
- 翻訳・要約はしない（それは後段=summary/concept の仕事。翻訳は後付けの別バッチ）。
- 取得した本文の `$ticker` と `@mention` を frontmatter に自動抽出（言語中立なリンク材料）。

## 手動実行
```bash
python3 collector/collect.py                              # watchlist 全周
python3 collector/collect.py --accounts blknoiz06,DefiIgnas --limit 5
python3 collector/collect.py --dry-run                    # 書き込まず件数だけ
```

## ノート形式
```
---
type: source
platform: x
account: <author>        # 実際の投稿者(RTなら元投稿者)
via: <polled handle>     # watchlist 上の誰経由で拾ったか
tweet_id: "..."
url: https://x.com/<author>/status/<id>
created: <ISO8601 UTC>
captured: <取得時刻>
likes: N
retweets: N
is_retweet: true|false
tickers: [$X, ...]
mentions: [@y, ...]
tags: [trench, source, x]
---
<原文そのまま>
```

## 自動化（取得はこまめに）
2通り。用途で選ぶ。

### A. GitHub Actions（クラウド・常時）
`.github/workflows/collect.yml` が毎時実行→新規を Wiki ブランチへ自動 commit。
- ⚠️ **private リポは Actions 無料枠が月2000分**。毎時×全アカだと枠を超え得る→頻度を下げるか、リポを public にする(public は無制限)。
- ⚠️ データセンターIPは syndication に 429 される場合あり。詰まるなら B を使う。

### B. ローカル cron / launchd（推奨・完全無料・自宅IP）
Mac が起きている前提だが、IP制限を受けにくく Actions 枠も食わない。
例: 30分ごと（crontab）
```
*/30 * * * * cd /Users/toma/trench-brain && /usr/bin/python3 collector/collect.py && git add sources/x && git commit -q -m "collect" && git push -q origin Wiki
```

## 既知の注意
- syndication は1アカ**直近~98件**しか返さない。超高頻度アカは取得間隔が空くと取りこぼす→こまめに回す。
- リクエストヘッダは最小(短いUA)で投げること。余計なヘッダを足すと 429 になる。
- 仕様変更で `__NEXT_DATA__` 構造が変わると壊れ得る(無料経路の宿命)。その時はパーサ修正。
