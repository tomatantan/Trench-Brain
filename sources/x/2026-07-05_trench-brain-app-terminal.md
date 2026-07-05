---
type: source
platform: image
via: /add-image
captured: 2026-07-05
tags: [trench-brain, app, ui, terminal]
---

## 観測（写っているもの）

- アプリ名: **TRENCH BRAIN**（緑の脳+ハットロゴ）
- ステータス: **API LIVE**（赤い点灯インジケータ）
- タブ: **TRENCH BRAIN TOOLS** → `LLM TERMINAL`（選択中・緑）/ `BRAIN CALL`（右側、一部切れ）
- **HOT WORD** セクション（▲ S と表示、残りは切れている）
- ターミナル表示テキスト（等幅フォント・緑）:
  > Trench Brain
  > Connection request from Trench
  > >>>> Authorized. Knowledge channel is open.
- 入力欄プレースホルダー:
  > 例：今meme化しそうな言葉は？ / このワードの起点は？ / KOL発言から何が見える？
- UIパーツ: `Learning Queue`チェックボックス（チェック済）、`Question`ドロップダウン、`TRANSMIT`ボタン（緑）
- ボトムナビ: 脳アイコン「脳」/ 波アイコン「サーフ」
- 端末ステータス: 時刻 15:22、バッテリー83%、iOSスタイル

ticker/CA: なし

## 推論（ナラティブ/型）

- Trench Brain の**モバイルフロントエンド**のスクリーンショット。このリポジトリ自体のUI層と推察（T3推論）。
- 「Connection request from Trench >>>> Authorized. Knowledge channel is open.」はターミナル演出的なオンボーディングメッセージ。ユーザー体験として"接続認証"の感触を与える設計。
- `LLM TERMINAL`タブ＝[[query]]操作の入力UI。`BRAIN CALL`タブは別機能（内容不明）。
- 入力例がwikiの[[query]]フローに直結:「meme化しそうな言葉」「ワードの起点」「KOL発言から見える」= 典型的なnarrative tracing クエリ。
- `Learning Queue`チェック済み＝バックグラウンド学習キューとの連携機能があるとみられる（T4推論）。
- ハッカー/ターミナル審美（黒背景・緑等幅フォント・ドット点灯）は[[survivor-memes]]文脈のサイバーパンク演出ではなくツール的UI選択。
