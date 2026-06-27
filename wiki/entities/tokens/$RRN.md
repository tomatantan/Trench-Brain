---
type: entity
kind: token
source: auto-track
status: watch
ticker: $RRN
mint: EKrearCNKwan2PhR6KwMWyEXcmDzST6HH7Kr2BFnpump
created: 2026-06-26
updated: 2026-06-26
tags: [token, pumpfun, prebond, traction0, ironic-naming]
---

# $RRN — buy = rich right now（EKrear）

pump.fun 発。名称「buy = rich right now」——get-rich-quick 系 ironic 命名（$GRQ と同コホート・同日）。twitter/website 未設定。bonding curve 未卒業（complete=false）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | EKrearCNKwan2PhR6KwMWyEXcmDzST6HH7Kr2BFnpump |
| name | buy = rich right now |
| 初検知 mcap | $55,157（2026-06-26T03:10Z） |
| gate | safety:ok / traction:mcap>=30000 |
| reply_count | 0 |
| KOL（CA確認） | なし |
| twitter | 未設定 |
| website | 未設定 |
| tokenized_agent | false |
| complete | false（未graduated） |
| real_sol | 6,711,454（bonding curve 内） |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|---|-----------|------|------|
| birth（03:10Z） | $55,157 | — | mcap>=$30k 勢い門通過。prebond。reply:0・KOL なし。 |
| BREAKOUT（10:23Z） | $134,871 | +137% | BREAKOUT 検知（$56.9k→$134.9k）。traction0継続・prebond継続。reply:0・KOL なし変わらず。 |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- 初検知 $55,157（03:10Z）→ BREAKOUT $134,871（10:23Z）= +137%。約7時間後の急騰。
- prebond 継続（complete=false）——bonding curve 未卒業のまま $134k 到達。
- reply:0・KOL CA 確認ゼロ・twitter/website なし——traction 完全ゼロのまま急騰。
- 「buy = rich right now」= get-rich-quick 系 ironic 命名。
- real_sol 84,577,510 lamports（~0.085 SOL）——bonding curve 資金量は相対的に低。

**判断**:
- traction0 × 出来高先行 BREAKOUT＝[[rug-anatomy]] の whale/bot 単独 pump 疑い。social 基盤なし・organic 需要の証拠なし。[[launchpad-economics]] 跳躍台帳追記（→BREAKOUT-then-dead 候補）。
- prebond のまま $134k は「出来高だけ先行して社会的需要が伴わない」パターンの典型——$AEGIS/$JALAPEÑO/$JOKER と同型シグネチャ。
- ⚠️ ironic 命名（「今すぐ買えば金持ちになれる」）が逆に bot pump に見えるシグナル——exit dump への布石の可能性。

**概念接続**: [[launchpad-economics]]（prebond・BREAKOUT・traction0） / [[rug-anatomy]]（traction0×出来高先行BREAKOUT・BREAKOUT-then-dead候補）
<!-- synthesis:end -->
