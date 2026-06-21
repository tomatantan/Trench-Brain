---
name: ingest-x
description: XのポストをTrench-Brainに取り込む。URLか本文を渡すと、生ソース保存→要約ページ作成→関連concept更新まで行う。
---

# ingest-x

Xのポスト（trenchのKOL/dev/要人）をWikiに取り込む。

## 手順
1. 渡されたXのURL/本文からポスト内容を取得（本文・投稿者・日付・含まれるトークン/CA）。
2. `sources/x/<投稿者>-<短い識別>.md` に生ソースとして保存（原文そのまま）。
3. `wiki/summaries/` に要約ページ作成（[[_templates/summary]] 準拠）。`source:` に元URL。
4. **関連 concept ページを更新**：
   - 言及されたナラティブ/トークン/セクターの concept を探す（無ければ新規）。
   - この投稿が示す パターン/プレイヤー相関/矛盾/変化 を反映。
   - 単なる転記でなく「他ソースとの交差点」を書く（CLAUDE.md の概念ページ指針）。
5. `[[wikilink]]` で summary ↔ concept を接続。
6. `wiki/index.md` と `wiki/log.md` を更新。

## 注意
- `sources/` は今回作る新規ファイルのみ。既存sourceは編集しない。
- 投稿者の立場（VC/KOL/dev/匿名）をメモ（信頼度の文脈になる）。
- スレッドなら全体を取り込む。
