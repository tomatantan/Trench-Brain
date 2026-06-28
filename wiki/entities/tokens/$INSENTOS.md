---
type: entity
kind: token
source: auto-track
status: dead
title: $INSENTOS（The Onboarder）
mint: 7JynQAvMuBwkxo6oW2dbAjemXmUJh7juqKjpv7pxpump
pool: GmkKuCUe475nEcvs3kNHf2MTawnpZ19fZugqTgfmYfHa
created: 2026-06-29
updated: 2026-06-29
tags: [trench, entity, token, auto-track, watch]
---

# $INSENTOS（The Onboarder）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | 7JynQAvMuBwkxo6oW2dbAjemXmUJh7juqKjpv7pxpump |
| pool | GmkKuCUe475nEcvs3kNHf2MTawnpZ19fZugqTgfmYfHa |
| gate | safety:ok / traction:graduated |
| mcap(birth観測) | $52,036（2026-06-28T18:18Z） |
| peak_mcap | $52,036（暫定） |
| real_sol | 0 |
| reply_count | 0 |
| twitter | https://x.com/KOLDestroyer/status/2071296151295324634 |
| website | https://www.instagram.com/p/DaIpuKwx2bk/ |
| tokenized_agent | false |
| status | watch |
| auto-track birth | 2026-06-28T18:18Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-29 初回合成（auto-track birth）

**観測（事実）**
- pump.fun 産・graduated(complete=true)・2026-06-28T18:18Z 検知。
- mcap $52,036。real_sol=0・reply_count=0・kol_ca 空。
- twitter: @KOLDestroyer ツイートリンク。website: Instagram リンク。tokenized_agent=false。

**動線・型**
- [[launchpad-economics]]: "The Onboarder" = 新規参入促進 narrative を標榜。symbol は "Insentos"（大文字小文字混在）。
- ⚠️ **@KOLDestroyer という account 名**: "KOL Destroyer" = KOL 批判/風刺アカウントの可能性。deployer 設定ツイートとの相性は不明（一次裏取り未済）。皮肉的 marketing か genuine か不明。
- Instagram website = trench では珍しいソーシャルリンク先。コミュニティ基盤がInstagram側にあれば新規性があるが、sources/x 未確認。
- real_sol=0 × traction0 = [[rug-anatomy]] "graduated-but-empty" 標準候補。

**賭け仮説**（confidence=低）
- @KOLDestroyer のアカウント性質（批判系 vs genuine）が確認できれば signal 質が変わる。現状 traction0 × real_sol=0 = 崩壊デフォルト想定。

### 2026-06-29 死亡確定（auto-track death）
**観測（事実）**
- last mcap $1,724（2026-06-28T21:35Z）・peak $57,584 比 **-97.0%**。cause: "mcap枯れ"。

**死因の型**
- "The Onboarder" × @KOLDestroyer × Instagram website = 新規性ある組み合わせも traction0 → [[rug-anatomy]] "graduated-but-empty" 標準崩壊。
- Twitter の風刺アカウント名（KOL Destroyer）× kol_ca 空 = 仮に genuine でも KOL 波及ゼロ。outcome: dead。
<!-- synthesis:end -->
