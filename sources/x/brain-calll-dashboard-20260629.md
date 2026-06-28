---
type: source
platform: image
via: /add-image
captured: 2026-06-29
tags: [brain-calll, meme-monitor, dashboard, tool]
---

## 観測（写っているもの）

**ダッシュボード名**: BRAIN CALLL — meme launch call monitor  
**ツール**: TRENCH BRAIN TOOLS（LLM TERMINAL / BRAIN CALLL タブ）  
**サマリ統計（左下）**: 60 calls / 56 smart / 4 high tire

---

### HOT WORD（上部ティッカー帯）
| ticker | accounts | category |
|--------|----------|----------|
| $TRUMP | 6 | WORLD |
| $DOGE | 6 | MACRO |
| $PEPE | 5 | WORLD |
| $WOJAK | 5 | MEME |
| $WIF | 5 | WORLD |
| $ZEC | 5 | MEME |
| $CARDS | 5 | MEME |
| $BTC | 10 | MACRO |
| $ETH | 10 | (画面端切れ) |

---

### HIGH TIRE DETECT（スコア上位）
| ticker | name | score | mcap |
|--------|------|-------|------|
| $SOL | Solana | 90 | $40,799.65M |
| $PUMPCADE | PUMPCADE | 79 | $23.19M |
| $TCG | The Collector Group | 73 | $7.51M |
| $ZERO | c0mpute | 46 | $3.01M |

---

### SMART DETECT（スコア37–46、一部）
| ticker | name | score | mcap |
|--------|------|-------|------|
| $CATWIF | catwifhat | 46 | $496K |
| $CHAMELEON | Meccha Chameleon | 45 | $393K |
| $PISS | pisscoin | 43 | $200K |
| $VALORA | Valora | 43 | $172K |
| $滑る猫 | Sliding Cat | 42 | $834K |
| $GATO | el gato | 42 | $183K |
| $HEISTED | Heisted | 42 | $133K |
| $PROV | Prova | 42 | $130K |
| $POINT | The Point | 41 | $101K |
| $DNT | Death and Taxes | 40 | $467K |
| $TMB | trust me, bro | 40 | $385K |
| $PONDEER | Pondering Deer | 40 | $371K |
| $WENDU | SIR WENDY'S | 39 | $352K |
| $AAIF | American AI Fund | 39 | $327K |
| $PEPONK | PEPONE | 39 | $318K |
| $XGIFT | (不明) | 39 | $160K |
| $JUSTICE | Mrs McAfee | 38 | $244K |
| $GOLDEN23 | Lebron Golden Jersey | 38 | $237K |
| $MOTION | MOTION | 38 | $204K |
| $SOL | GPT-5.6 Sol | 38 | $203K |
| $TRADER | TRADER | 37 | $208K |
| $BOLEX | BOLEX | 37 | $172K |
| $HI | hi | 37 | $170K |

---

### 詳細展開カード（$ZERO）
- name: c0mpute
- CALL reason: `safety:ok / traction:user_checked`
- mcap: $3.01M / peak: $3.74M
- reply count: 8 / score: 46

---

## 推論（ナラティブ/型）

- **これはTrench-Brain自身のBRAIN CALLLツールのスクリーンショット**（UI上部に "TRENCH BRAIN TOOLS" ロゴあり）。外部ソースではなく、**自分のシステムの動作確認画像**の可能性が高い。(T3推論)
- スコア体系: HIGH TIRE（高スコア=大型既存コイン含む）/ SMART DETECT（新興meme候補）に2段階分類。
- HIGH TIRE 上位に $SOL(score 90)・$PUMPCADE(79)・$TCG(73)が並ぶ → 既存大型+新興の混在検出。
- $ZERO/c0mpute: mcap $3.01M、peak $3.74Mで下落中、reply count 8 → エンゲージ薄め、call reason に `user_checked` が含まれ人手確認済みを示す。
- $滑る猫（Sliding Cat）: 日本語ミームticker、score 42 / $834K → ジャンル混在の様子。
- $NIGGERTEAM という⚠️不適切名のtickerも検出されていることが観測される（フィルタリング議論の材料になりうる）。
- HOT WORDとして $BTC・$ETH が10 accountsでトップ → macro/world sentiment が強い日。

**関連concept候補**: [[brain-calll]] / [[meme-monitor]] / [[traction-scoring]]
