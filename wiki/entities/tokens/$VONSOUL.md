---
type: entity
kind: token
source: auto-track
status: watch
title: $VONSOUL（The Artist）
mint: A1oXmM78zn6PVm2XkkAY8Eh8vNzGuzrbEeZcLLBppump
pool: Hcyh1yu6dSaJ1AFFkbt9Q3msC3PuTEymxb1hWGzMchNX
created: 2026-06-29
updated: 2026-06-29
tags: [trench, entity, token, auto-track, watch]
---

# $VONSOUL（The Artist）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | A1oXmM78zn6PVm2XkkAY8Eh8vNzGuzrbEeZcLLBppump |
| pool | Hcyh1yu6dSaJ1AFFkbt9Q3msC3PuTEymxb1hWGzMchNX |
| gate | safety:ok / traction:graduated |
| mcap(birth観測) | $24,102（2026-06-28T18:18Z） |
| peak_mcap | $24,102（暫定） |
| real_sol | 0 |
| reply_count | 0 |
| twitter | https://x.com/vonsoulart/status/2071294670164971763 |
| website | （空） |
| tokenized_agent | false |
| status | watch |
| auto-track birth | 2026-06-28T18:18Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-29 初回合成（auto-track birth）

**観測（事実）**
- pump.fun 産・graduated(complete=true)・2026-06-28T18:18Z 検知。
- mcap $24,102。real_sol=0・reply_count=0・kol_ca 空。
- twitter: @vonsoulart（ticker VONSOUL と一致する account 名）。tokenized_agent=false。

**動線・型**
- [[launchpad-economics]]: ticker "VONSOUL" と twitter account @vonsoulart が一致 = 実在するアーティストアカウントが自ら発行した可能性、または deployer が @vonsoulart を詐称している可能性の両義。一次裏取り未済（sources/x に @vonsoulart ファイルなし）。
- ⚠️ **creator token 疑い**: account 名と ticker の一致は "artist の自己トークン化" パターン。real_sol=0 × traction0 の場合、creator の初期 pull risk が残る。
- real_sol=0 × reply=0 = [[rug-anatomy]] "graduated-but-empty" 標準候補。

**賭け仮説**（confidence=低）
- @vonsoulart が genuine クリエイターであれば creator-token 型の需要が期待できるが、kol_ca 空 × traction0 の現状では証拠不十分。次サイクルで @vonsoulart の独立発信や reply 増加があれば格上げ候補。
<!-- synthesis:end -->
