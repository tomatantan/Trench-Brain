---
type: entity
kind: token
source: auto-track
status: dying
title: $ORANGIE
mint: DuBrjnHaC8BMP6EZ2md38oSERYU1msh8VumPoG2Gpump
pool: 5e8xaAzjXFzPxqe5LF9h4jreveRXKkNzXx23nCXvfxaF
created: 2026-06-28
updated: 2026-06-28
tags: [trench, entity, token, auto-track, dying]
---

# $ORANGIE（The Italian Stallion）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint(主体) | DuBrjnHaC8BMP6EZ2md38oSERYU1msh8VumPoG2Gpump |
| pool | 5e8xaAzjXFzPxqe5LF9h4jreveRXKkNzXx23nCXvfxaF |
| gate | safety:ok / traction:graduated |
| mcap(birth観測) | $101,831 → $97,398 → $12,371（-87% 2026-06-28T08:52Z） |
| real_sol | 0 |
| reply_count | 0 |
| twitter | https://x.com/orangie/status/2071102988970590458 |
| status | watch |
| auto-track birth | 2026-06-28T05:38Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-28 初回合成（auto-track birth）

**観測（事実）**
- pump.fun 産・graduated(complete=true)・2026-06-28 検知。
- mcap $101,831（birth時）・real_sol=0・reply_count=0。
- twitter: https://x.com/orangie/status/2071102988970590458（@orangie のツイート）。
- **multi-mint**: 同名同 twitter の下位 mint（CAq43a67...・$1,453）が同バッチに存在→即死確認済。本 mint (DuBrjnHa) が主体。
- kol_ca 空・kol_ticker 空 = KOL の CA 直接支持未確認。tokenized_agent=false。

**動線・型**
- [[launchpad-economics]]: graduated・multi-mint 同時発射。"The Italian Stallion" = Rocky/Stallone 映画の別名。meme フックとして cultural 認知はあるが crypto community への伝播は未確認。
- ⚠️ **multi-mint 同時発射**: deployer が 2 mint 同時発射→下位 mint 即死($1,453)・本 mint が主体（$STARSHIT/$KOTON/$BOLEX 同型）。
- ⚠️ **real_sol=0**: pool 自己積みなし→有機的買い手のみで $101k 維持が必要。deployer exit バッファなし。
- ⚠️ **association marketing 疑い**: kol_ca 空 = @orangie ツイートは deployer 設定の可能性あり。一次裏取り未確認（sources/x に @orangie ファイルなし）。

**賭け仮説**（confidence=低）
- traction0 × real_sol=0 × graduated = [[rug-anatomy]] "graduated-but-empty" 最頻パターン。
- 独立 KOL の CA 言及が確認されなければ dead-spiral 候補。[[survivor-memes]] 到達条件未達。

### 2026-06-28 update（mcap-87%）
**観測**: mcap $97,398 → $12,371（-87%）。reply_count 0 のまま。status: dying に更新。
**判断**: 初回合成で指摘した「traction0 × real_sol=0 = graduated-but-empty」パターンが的中。-87% = [[rug-anatomy]] dead-spiral 進行中。KOL 支持の裏取り未確認のまま dump。次サイクルで死亡確認されれば台帳記録。
<!-- synthesis:end -->
