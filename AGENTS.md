# AGENTS.md

このリポの運用規約（憲法）は **[CLAUDE.md](./CLAUDE.md)** に集約。
Codex / その他エージェントも、作業前に CLAUDE.md を読んでそれに従うこと。
概念の根拠は [docs/LLM-WIKI.md](./docs/LLM-WIKI.md)。

## 絶対に守る指針（要約・詳細と出典/理由は CLAUDE.md「憲法」節）
1. `sources/` は読むだけ。編集は `wiki/` のみ。
2. 収集は**門付きキュレーション**（X=watchlist単位 / 新規=traction+KOL単位）。**firehose（無差別全取得）は恒久禁止**（CoinGecko trending・DexScreener boosted 等）。鮮度は門付き収集で担保＝firehose不要。
3. **収集と合成は両輪**。raw を入れたら必ず合成（entity synthesis＋concept）まで回す。**raw放置は LLM Wiki ではない＝ただのスクレイパー**。健康の物差しは未合成 backlog 件数。
4. 1ソースで複数ページに波及させ、`[[wikilink]]` で繋ぐ。
5. 矛盾は消さず両論併記で `⚠️` 旗。
6. 観測事実とLLM推論を分離。
7. 全ページ `[[wikilink]]` 接続。
8. bottom-up。エージェントが独断でページ量産しない（concept は動線/型が立つ時だけ）。
9. 淡々と。煽り・絵文字過多をしない。

## 操作
ingest / query / lint（`.claude/skills/` 参照）。合成工程の手順は [brain/INGEST.md](./brain/INGEST.md)。
同期は Git（作業前 pull・作業後 commit/push）。
