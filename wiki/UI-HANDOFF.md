# UI handoff — `wiki/ui-data.json` の契約

UIチーム(ogawa)向け。`wiki/ui-data.json` を fetch して描画する。
**自動更新**: `brain/export_ui.py` が 3h cron で再生成→`main` に push。常に最新が乗る。手で触らない。

## 3セクション

### 1. `signals[]` — concept由来の泡（既存・安定層）
合成済みの concept/entity から生成。**泡＝ナラティブ、click＝SIGNAL TRACE**。
```
{ type: "MACRO"|"WORLD"|"MEME",  title: "$BTC",
  size: 60-130,                  // memetic potential近似(言及×アカ×エンゲージ)
  color: "#hex", glow: 0.0-1.0,  // 発光強度
  mentions, accounts,
  trace: { why, top:[{likes,account,text}], causal:[所属concept名...],
           confidence, synthesized } }   // ドロワー: なぜ浮上+CAUSAL CHAIN+確度
```

### 2. `live[]` — launch lifecycle（新・ライブ層）
pump.fun launch pipeline(`brain/track.py`)の TRACKED トークン。**launch radar / 生死トラッキング**。
```
{ ticker, name, mint, mcap, peak_mcap,
  status: "tracked"|"dead",  outcome: "graduated"|"died"|null,
  color: "#48eca0"(生存) | "#ffb749"(graduated) | "#5a6472"(死),
  gate,                      // どの門を通ったか(safety/traction)
  kol: [CA一致した言及アカ], ai_agent: bool, reply_count,
  first_seen, died_at, link: "pump.fun/coin/<mint>",
  spark: [mcap履歴 直近24点] }   // ミニチャート用
```
※ live は投機tier（生死が激しい・大半は死ぬ）。signals(合成済concept)とは性質が別。用途で使い分け。

### 3. `base_rate` — 生存者バイアスの分母（headline metric）
```
{ mints_seen, gate_passed, died, graduated, pass_rate_pct, note }
```
= 全mint観測のうち篩通過率。`launchpad-economics`(98.5%死ぬ)の**実測値**。
「今日 N mint 観測 / 篩通過 X% / 死 Y」のヘッドラインに使える。

## 注意
- 値が空/0でも壊さない（cron初回前や queue 空の時）。
- 色は上記固定。増減は `signals`/`live` を上から N 件描けばよい（size/mcap降順済）。
- schema は ui-data.json の `schema` フィールドにも自己記述あり。
