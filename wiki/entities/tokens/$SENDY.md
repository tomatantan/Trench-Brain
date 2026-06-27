---
type: entity
kind: token
source: auto-track
status: dead
ticker: $SENDY
mint: 3MUrFjQgPrLZHH8Y7CwssV99dZosGBxYZaAzZwR5pump
created: 2026-06-25
updated: 2026-06-26
tags: [token, pumpfun, graduated, traction0, cat-meme, outcome:died]
---

# $SENDY (Sendy) — 3MUrFj

pump.fun 発。bonding curve 卒業済。mcap $21k・real_sol 0。cat themed（catsendy.fun）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 3MUrFjQgPrLZHH8Y7CwssV99dZosGBxYZaAzZwR5pump |
| name | Sendy |
| 検知時 mcap | $21,593（2026-06-25T14:21Z） |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| twitter | https://x.com/sendymission |
| website | https://catsendy.fun/ |
| tokenized_agent | false |
| real_sol | 0（pool 実流動性なし） |
| pool_address | 6MQYJpeKrcoxcJ7j4cBoGKtfBw3jfrMvcjj6GEc6qBc3 |

## 追跡ログ

| 観測 | live mcap | 変化（検知時比） | 窓間変化 | 備考 |
|----|-----------|----------------|---------|------|
| 初検知(14:21Z) | $21,593 | — | — | gate 通過。reply:0・KOLゼロ。 |
| DB peak(不明) | ~$25,849 | +19.7% | — | track.py DB 記録値（実観測時刻未確認）。 |
| auto(14:48Z) | **$12,650** | **-41.4%** | -$13,199（-51.0%）from DB peak | -51%急落（DB比）。T3ゼロ継続。死亡圏内。 |
| auto(15:43Z) | $21,068 | -2.4% | +$8,418（+66.6%）from 14:48Z | oscillation。初検知水準戻し（回復でなく振れ戻し）。T3ゼロ継続。 |
| auto(16:12Z) | **$2,003** | **-92.3%（peak比）** | -$19,065（-90.5%）from DB peak | **死亡確定**。oscillation後最終崩壊。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun bonding curve 卒業・$21,593。real_sol 0——pool 実流動性なし。
- twitter @sendymission / website catsendy.fun（cat themed）——社会基盤あり。
- reply_count=0・KOL なし——有機的 traction ゼロ。
- "Sendy" は cat meme 命名。generic 寄り。

**判断（auto 14:48Z・更新）**:
- $21k 初検知 → ~$25.8k peak → $12.6k（-51%急落）。real_sol 0 + traction0 の急落は [[launchpad-economics]] 「graduated-but-empty」縮退の典型経路。
- ⚠️ $12.6k は死亡閾値圏内。reply:0・KOLゼロが続く限り回復要因なし。

**2026-06-25T15:43Z 更新（+58%・$21.1k）**:
- prev **$13,366 → $21,068（+58%）**。reply=0・KOL なし継続。
- $12.6k 死亡圏内から $21.1k に部分回復。ただし検知時 $21.6k 比でほぼ同水準——回復でなく oscillation（初検知値に戻っただけ）。real_sol 0 のまま。
- traction ゼロでの oscillation は deployer 自己資金か小口 bot の出し入れ。持続的需要の証拠なし。次窓で再び下落するなら [[rug-anatomy]] 死亡台帳入り確定。

**2026-06-25T16:12Z 死亡確定（最終）**:
- $21,068（15:43Z）→ **$2,003**（-90.5%・peak比-92.3%）。死亡確定。
- oscillation で initial 水準に戻した後、immediate final collapse。real_sol 0 × traction0 × reply0 の「振れ戻し→最終崩壊」経路——$BUCK/$MDT と同型の graduated-but-empty 縮退死。
- cat meme 命名（catsendy.fun・@sendymission）× social 基盤ありでも community 需要ゼロ = 死の先行指標が揃っていた。
- **生存: ~2時間（14:21Z検知→16:12Z死亡）**。型通り。

<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty・低 mcap）
- [[rug-anatomy]]（traction0 × real_sol 0）
