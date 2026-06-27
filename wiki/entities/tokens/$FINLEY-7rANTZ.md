---
type: entity
kind: token
source: auto-track
status: dead
outcome: died
peak_mcap: 87634
ticker: $FINLEY
mint: 7rANTZbuUSfYzEtNkPJfptfEyuFccFdb69FraVy5JoaT
created: 2026-06-25
updated: 2026-06-25 (final)
tags: [token, pumpfun, meme, finley]
---

# $FINLEY (7rANTZ)

## ライフサイクル (auto-track)
| 項目 | 値 |
|---|---|
| mint | 7rANTZbuUSfYzEtNkPJfptfEyuFccFdb69FraVy5JoaT |
| name | finley |
| mcap (初観測) | $87,634 |
| mcap (最終観測) | $28,389（-67.6% from peak） |
| gate | safety:ok / traction:graduated |
| status | active (graduated→Raydium) |
| reply_count | 0 |
| twitter | https://x.com/redacted_noah/status/2069974350724563037 |
| website | — |
| tokenized_agent | false |
| 観測時刻 | 2026-06-25T02:49Z → 最終 2026-06-25T03:48Z |

**同名競合**: 同一バッチで $FINLEY が3 mint 同時出現（7rANTZ/$87.6k・59JgPz/$39k・DLJgWQ/$1.6k→即死）。本ファイルは最大 mcap 版。

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun graduated（bonding curve 完了→Raydium 移行）・$87.6k mcap
- twitter に @redacted_noah のツイートを設定——redacted_noah は Drift Protocol exploit の post-mortem を書いた開発者（[[toly__2069513813486153978]] にて toly が RT）
- reply 0・KOL CA 言及なし・website なし
- 同時刻に同名が3 mint 出現 → multi-mint squatter パターン

**判断**:
- traction ゼロのまま graduated → [[launchpad-economics]] 「graduated but empty」候補
- Drift dev の名前借用 association marketing ⚠️: 実際に redacted_noah 本人が関与しているかは未確認（一次ソース tweet 未取得）
- KOL/reply 不在のまま $87k → [[rug-anatomy]] つり上げ候補。持続には organic 需要が必要
- ⚠️ 同名 multi-mint 競合 → どの mint に流動性が集中するかでどれが「本物」か決まる

**賭け仮説**: reply/KOL が付かなければ [[rug-anatomy]] 死亡台帳入り（graduated-but-empty 型）が支配的。

**更新（2026-06-25T03:48）**:
- mcap $87.6k → $50.3k → $28.4k と一貫して下落中（-67.6% from peak）
- reply/KOL/twitter 変化なし——decline は traction 不在を裏付け
- [[rug-anatomy]] 死亡候補の確度上昇。反転には KOL pickup が必要だが根拠なし
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（门・graduated 動線）
- [[rug-anatomy]]（traction0 × graduated → 死亡確定）

**2026-06-25T13:57Z 最終合成（死亡確定）**:
- last mcap **$6,832**（peak $87,634 比 **-92.2%**）。cause: mcap -90% from peak。
- $28.4k（前回更新）から更に崩壊——KOL/reply 全期間ゼロのまま枯れ確定。real_sol 82.6 SOL が存在したにもかかわらず最終崩壊（high real_sol ≠ 生存保証の N 追加）。
- multi-mint 競合（7rANTZ $87.6k・59JgPz $39k・DLJgWQ $1.6k）の「最強 mint」だったが全滅コホートの一つ。
- **型の確定**: redacted_noah association marketing × traction0 × multi-mint 競合 → graduated-but-empty 死亡（[[launchpad-economics]]）。
