---
type: entity
kind: token
title: $GOOGL
updated: 2026-06-22
tags: [trench, entity, token]
mentions: 4
accounts: 2
---

# $GOOGL

> 自動生成(brain/build_entities.py)。言及 4件 / 2アカ。
事実=この自動集約 / 判断=下の合成メモ＋関連 [[concepts]]。

## 言及アカウント
[[@MEXC]] [[@WatcherGuru]]

## 共起トークン
[[$NVDA]] [[$SPCX]] [[$VZ]]

## 高エンゲージ言及
| likes | account | 抜粋 | source |
|---|---|---|---|
| 1,353 | [[@WatcherGuru]] | JUST IN: Google $GOOGL added to the Dow Jones Industrial Average, replacing Verizon  | [[watcherguru__2069534814773158274]] |
| 984 | [[@WatcherGuru]] | JUST IN: Google $GOOGL added to the Dow Jones Industrial Average, replacing Verizon  | [[WatcherGuru__2069534814773158274]] |
| 107 | [[@MEXC]] | Your next Earn deposit could come with a side of $NVDA.  🎰 Share $1,000,000 in stock | [[mexc__2069269215534883003]] |
| 19 | [[@MEXC]] | Your next Earn deposit could come with a side of $NVDA.  🎰 Share $1,000,000 in stock | [[MEXC__2069269215534883003]] |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 観測（事実）
- **[[@WatcherGuru]]（984♥, 2026-06-23）**: "JUST IN: Google $GOOGL added to the Dow Jones Industrial Average, replacing Verizon $VZ."（[[WatcherGuru__2069534814773158274]]）＝伝統金融指数変更という外部イベント。
- **[[@MEXC]]（107♥, 2026-06-23）**: "$NVDA、$GOOGL、$SPCX 等をEarnプロモーションの賞品として掲載"（[[mexc__2069269215534883003]]）＝CEX が tokenized stock ($GOOGL) をリワードとして配布するプロモーション文脈。
- 共起: [[$NVDA]]（AI/半導体）・[[$SPCX]]（SpaceX tokenized stock）・[[$VZ]]（DJIA入れ替え相手）。

### 判断（推論）
- **動線上の位置（[[external-event-to-token-pattern]] / [[perp-dex-wars]] RWA側）**: DJIA採用という伝統金融の外部イベントが $GOOGL という ticker を trench に流し込む典型パターン。MEXCのEarnプロモ（tokenized stock 配布）と合わさり「TradFi指数変更 → CEX tokenized stock プロモ → trench言及」という動線が見える。
- **[[$SPCX]] との共起の意味**: SpaceX IPO narrative（[[spacex-ipo-narrative]]）の文脈でも tokenized stock の参照点として並んでいる。$GOOGL・$NVDA・$SPCX が同一プロモに乗るのは「TradFi大型株の tokenized stock」が一括りのカテゴリとして扱われている証拠。
- **⚠️ 懐疑**: WatcherGuru は「JUST IN」形式の速報アカウントであり言及自体はニュース転載に近い。trench での買い動線（KOLが推奨・onchainで動く）とは性質が異なる。MEXCプロモはCEXマーケティングであり token 固有のファンダでない。2アカウント・4言及は最小閾値であり、major tokenized stock として流動性は存在するが trench 固有のナラティブは薄い。

### concept接続
- [[external-event-to-token-pattern]]（DJIA採用という外部イベント → tokenized stock 言及の典型型・RWA側）
- [[perp-dex-wars]]（RWA perp / tokenized stock がHyperliquidのHIP-3 40%到達と同時期の流れと接続）
- [[$NVDA]] / [[$SPCX]] / [[$VZ]]（共起・tokenized stock カテゴリ）
<!-- synthesis:end -->
