---
type: entity
kind: token
source: auto-track
status: dead
ticker: $HAMA
mint: 85HFRQa1wUGLMcVFwtLXxYrcFbqsZL3hgkB62KmRpump
created: 2026-06-25
updated: 2026-06-25
tags: [token, pumpfun, meme, hama, dog]
---

# $HAMA-85HFRQa — Hama（2本目 mint）

## ライフサイクル (auto-track)
| 項目 | 値 |
|---|---|
| mint | 85HFRQa1wUGLMcVFwtLXxYrcFbqsZL3hgkB62KmRpump |
| name | Hama |
| mcap (初観測) | $55,343 |
| gate | safety:ok / traction:graduated |
| status | active (graduated→Raydium) |
| reply_count | 0 |
| twitter | — |
| website | https://hamadog.fun/ |
| tokenized_agent | false |
| 観測時刻 | 2026-06-25T04:42Z |

**同名先行 mint**: $HAMA(2w5nRa7) が同日 04:24 に観測→即死（peak $1,547・mcap枯れ）。本ファイルは同ブランド(hamadog.fun)の2本目。

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- pump.fun graduated（bonding curve 完了→Raydium 移行）・$55.3k mcap
- website: hamadog.fun——先行 mint(2w5nRa7)と同一 URL → 同一 deployer または copycat
- twitter なし・reply 0・KOL 言及なし
- 先行 mint(2w5nRa7)は同日 $1.5k で即死——本 mint はそれよりはるかに高い $55k で graduated

**判断**:
- ⚠️ 同ブランド 2 mint 出現: 先行(2w5nRa7 $1.5k 即死)の直後に本 mint が $55k graduated → 同一 deployer の再 mint 疑い（低流動版で様子見→本投入）か copycat か
- social ゼロ（twitter なし）× reply0 × KOL0 → graduated だが traction なし
- hamadog.fun というドメイン整備がある点は先行 mint と同条件——それでも先行は即死

**DEAD確定（2026-06-25T05:01）**: peak $55,343 → last $1,578（peak比-97.1%）。cause: mcap枯れ。KOL/reply ゼロのまま崩壊——同ブランド2本目も traction ゼロで死亡（先行 mint(2w5nRa7)と同結論）。→ [[rug-anatomy]] 死亡台帳。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated 動線・re-mint 疑い）
- [[rug-anatomy]]（同ブランド再 mint × traction0 → 死亡候補）
