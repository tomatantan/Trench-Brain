# Trench-Brain 🧠⛏️

crypto trench（memecoin最前線）の集合知を、LLMが**繋ぎ続ける**ナレッジWiki。
全TrenchのX発言・ニュース・要人の発言を取り込み、単一ソースでは見えない「交差点の気づき（ナラティブ/プレイヤー/パターン）」を合成する。Andrej Karpathy式 LLM Wiki の crypto特化版。

> 思想：RAGは「質問のたびにゼロから再発見」。LLM Wikiは「持続的に蓄積・接続される成果物」。

## 3層構造
1. **Sources（生ソース）** `sources/` — X投稿・ニュース・要人発言のクリップ。人間/取り込みが追加、**LLMは読むだけ・編集しない**。
2. **Wiki** `wiki/` — LLMが管理するmarkdown。要約・**概念ページ（肝）**・query・index・log。
3. **Schema** `CLAUDE.md` / `AGENTS.md` — 運用規約。人間が定義、エージェントが従う。

## 3つの操作（エージェントが実行）
- **Ingest**：新ソース投入 → 要約ページ作成 → 関連する概念ページを更新（1ソースで複数ページに波及）。
- **Query**：Wikiに質問 → 横断で回答 → 価値ある回答は `wiki/queries/` に保存して資産化。
- **Lint**：定期ヘルスチェック → 矛盾・孤立ページ・知識ギャップを検出して報告。

## 使い方（Claude Code / Codex）
リポジトリで `claude`（or codex）を起動してスキルを呼ぶ：
- `ingest-x` … XのポストURL/本文を渡す
- `ingest-news` … 記事URLを渡す
- `query` … 質問する
- `lint` … 健康診断

規約の詳細は **[CLAUDE.md](./CLAUDE.md)**（エージェントは作業前に必ず読む）。

## セットアップ（各メンバー）
1. `git clone <repo>` → `cd Trench-Brain`
2. **Obsidianでこのフォルダを vault として開く**（グラフビューで繋がりが見える）
3. `claude` 起動 → スキルで ingest / query / lint

## 同期 = Git（チーム）
- GitHubリポが唯一の正。Obsidian Syncは使わない（個人用なので）。
- 作業後：`git add -A && git commit -m "..." && git push` ／ 作業前：`git pull`
- 秘密（APIキー等）は `.env`（gitに乗せない）。

## 共同開発フロー
ブランチ切る → 作業 → push → Pull Request → レビュー/merge → 各自 `git pull`。
