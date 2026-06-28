---
type: source
platform: image
via: /add-image
captured: 2026-06-28
tags: [trench-brain, ui, ca-check, hot-word, meme, $BTC, $ETH, $SPCX, $HYPE, $SOL]
---

## 観測（写っているもの）

### 画像種別
Trench Brain Web UI のスクリーンショット（ターミナル風ダークテーマ）。

### HOT WORD バー（上部）
| ticker | accounts | カテゴリ |
|--------|----------|---------|
| $BTC   | 18       | MACRO   |
| $ETH   | 18       | MACRO   |
| $SPCX  | 18       | WORLD   |
| $HYPE  | 13       | MACRO   |
| $SOL   | 10       | MACRO   |

### CA check セッション
- 入力CA: `BcHEaaTCvycPwwsJ9yQTXdHP9X2gCLkznDbZ8VySpump`
- 結果: **未収録**。`ui-data.json live[] / signals[]` にこのCAに一致するtoken recordなし。
- システム応答: 「別のHOT WORDへ推測で紐づけません。CA一致がない場合は、根拠なしの関連付けを行いません。」

### ユーザークエリ
「今日流行りのmeme」

### Trench Brain 応答（meme-word候補）
- **$BTC** — 18 accounts / MACRO
- **$ETH** — 18 accounts / MACRO
- **$SPCX** — 18 accounts / WORLD
- **$HYPE** — 13 accounts / MACRO
- **$SOL** — 10 accounts / MACRO
- 指標: 「いいね数ではなく、独立言及及びアカウント数を優先。」

### その他UI要素
- Learning Queue チェックボックス（画面下部）
- 入力プロンプト例: 「今meme化しそうな言葉は？ / このワードの起点は？ / KOL発言から何が見える？」

---

## 推論

### CA `BcHEaaTCvycPwwsJ9yQTXdHP9X2gCLkznDbZ8VySpump` について
- サフィックス `pump` は pump.fun 発行トークンの典型的なCA末尾。
- 未収録＝watchlist経由で一度も入ってきていないトークン。
- ⚠️ 外部から渡されたCAをシステムが根拠なしに既存概念と結びつけることを拒否している点は、**指針6（観測と推論の分離）** の正しい動作。

### HOT WORDランキングの示唆
- 上位5件が全て L1/メジャーチェーン ($BTC/$ETH/$SOL) + Hyperliquid ($HYPE) + $SPCX (Space Coin系?) で占められている。
- memeコイン固有のナラティブよりも**マクロ/インフラ層のワードが支配的**な状態。
- trenchが動く局面というよりは静観/macro観測フェーズの可能性。
- $SPCX が WORLD カテゴリに分類されている点が異質——何らかのグローバルナラティブ（宇宙/国家系?）に紐づいている可能性。要確認。

### このスクリーンショットの文脈的意味
- Trench Brain UI の動作確認・デモとして撮影された可能性が高い。
- システムが「根拠なし紐づけをしない」ことを自ら明示していることは、品質管理機能の証跡。
