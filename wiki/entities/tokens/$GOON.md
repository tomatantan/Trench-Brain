---
type: entity
kind: token
source: auto-track
status: dead
ticker: $GOON
mint: 192yaGfSk3TSW8bp3wZ7ZXyEjRsWiyiaPswpXLppump
created: 2026-06-25
updated: 2026-06-26 (第125窓・list exit確定)
tags: [token, pumpfun, graduated, traction0, internet-meme, food-meme, real-sol, dead]
---

# $GOON (crab rangoooning) — 192yaGf

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 192yaGfSk3TSW8bp3wZ7ZXyEjRsWiyiaPswpXLppump |
| name | crab rangoooning |
| 初検知 mcap | $100,983（第111窓） |
| gate通過 mcap | $107,098（2026-06-25T13:57Z） |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| twitter | https://x.com/joincrabrangoon |
| website | https://rangooning.vercel.app/ |
| tokenized_agent | false |
| real_sol | 39.9 SOL（pool 実流動性あり） |
| pool_address | EcSWuLDMPQvTyTud4YUoxSo8eFTuAPhHCD4WuWgDnD39 |

## 追跡ログ

| 窓 | live mcap | 変化（検知時比） | 窓間変化 | 備考 |
|----|-----------|----------------|---------|------|
| 第111窓 | $107,290 | +6.2% | — | 初登場。8候補中唯一正方向。T3ゼロ・reply:0。 |
| 第112窓 | $151,719 | +50.2% | +$44,429（+41.4%） | 2窓目。2窓連続正方向・上昇率加速。T3ゼロ・reply:0 継続。 |
| 第113窓 | **$245,388** | **+143.0%** | +$93,669（+61.7%） | **3窓目。3窓連続正方向・上昇率加速継続（+6.2%→+50.2%→+143.0%）。T3ゼロ・reply:0 継続。過去全縮退記録の最長反転（2窓）を超えた。** |
| 第114窓 | **$308,968** | **+206.0%** | +$63,580（+26.0%）| **4窓目。4窓連続正方向継続。上昇率は+143.0%→+26.0%と鈍化。T3ゼロ・reply:0 継続。** |
| 第115窓 | **$332,979** | **+229.7%** | +$24,011（+7.8%・さらに鈍化）| **5窓目。5窓連続正方向継続。窓間+7.8%まで急鈍化（前窓+26.0%）。T3ゼロ・reply:0 継続。** |
| 第116窓 | **$303,524** | **+200.6%** | -$29,455（-8.8%・初の窓間下落）| 6窓目。5窓連続上昇後、初の窓間マイナス。T3ゼロ・reply:0 継続。 |
| 第117窓 | **$1,361** | **-98.7%** | -$302,163（**-99.6%窓間・DEAD確定**）| **7窓目・崩壊確定。died +1 計上。GTT型完全踏襲。T3ゼロ・reply:0。** |
| 第117-124窓 | $1,295-$1,361 | -98.7%水準 | — | **DEAD残存 8窓。$1,295-$1,361 水準で継続残存。T3ゼロ・reply:0。** |
| 第125窓 | — | — | — | **candidates消滅・list exit確定（8窓DEAD残存後消滅）。** |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun bonding curve 卒業・検知時 $100,983。第111窓 +6.2%→第112窓 +50.2%→第113窓 +143.0%→第114窓 +206.0%→第115窓 +229.7%（天井 $332,979）→第116窓 +200.6%（初の下落・-8.8%窓間）→**第117窓 -98.7%（$1,361・崩壊確定）**。
- 窓間変化: +$44k→+$94k→+$63k→+$24k→-$29k→**-$302k（崩壊）**。
- real_sol 39.9 SOL（検知時）。reply_count=0・T3 signal ゼロ 全7窓。
- died +1 計上（第117窓）。

**判断（第117窓・DEAD確定）**:
- 第116窓「初の下落窓→GTT型崩壊の可能性最大」の仮説が第117窓で的中。「初の下落窓後に持ち直した前例なし」が再び成立。
- 窓間変化率の推移: +41.4%→+61.7%→+26.0%→+7.8%→-8.8%→**-99.6%**。鈍化→初の下落→翌窓即崩壊のパターンが確定。
- T3ゼロ 7窓全期間——$332k 天井まで上昇しながら KOL 1件も出なかった。deployer が 39.9 SOL の流動性を活用して段階的 exit pump を実行し、6窓かけて完了させた構造と解釈できる。
- ⚠️ 教訓: 「real_sol あり × T3ゼロ × 多窓連続上昇」は deployer の staged exit の温床。KOL が出るまで organic 判定は禁物。[[rug-anatomy]] [[reflexivity]]

**縮退パターン分類**: GTT型（鈍化→初下落→翌窓即崩壊）。ただし GTT（7窓）より1窓多い6窓上昇の実績あり——「最長 GTT 型」として記録。
**第125窓 list exit確定**: DEAD確定（第117窓）後、8窓 DEAD残存（$1,295-$1,361 水準）→第125窓 candidates 消滅。縮退記録へ移行。

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty × real_sol保有）
- [[rug-anatomy]]（real_sol + traction0 = deployer pump リスク）
- [[survivor-memes]]（internet food meme が organic traction を呼んだ場合）
- [[reflexivity]]（KOL言及→点火条件）
- [[launch-pulse]]（第111-113窓 traction 候補・3窓連続正方向・上昇率加速）
