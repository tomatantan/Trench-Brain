---
type: entity
kind: token
source: auto-track
status: watch
title: $CHIBUL（Chill Bullok）
mint: 6ANdVaAHJY43ZBGGHr1nj7K5m1FWcFexzMrQLC5Rpump
pool: 92xjAR46usmN16nZuqvnbmdwd4ApnXUCtm7TJcXnksFj
created: 2026-06-29
updated: 2026-06-30
tags: [trench, entity, token, auto-track, prebond, bull-narrative, traction0]
---

# $CHIBUL（Chill Bullok）

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | 6ANdVaAHJY43ZBGGHr1nj7K5m1FWcFexzMrQLC5Rpump |
| pool | 92xjAR46usmN16nZuqvnbmdwd4ApnXUCtm7TJcXnksFj |
| gate | safety:ok / traction:mcap>=30000 |
| mcap(birth観測) | $85,172（2026-06-29T13:29Z） |
| mcap(変化 +76%) | $149,550（2026-06-29T16:37Z） |
| peak_mcap | $149,550（暫定） |
| real_sol | ~0.27 SOL（271103274 lamports） |
| reply_count | 0 |
| twitter | https://x.com/marshmello82088?s=11 |
| website | https://x.com/marshmello82088?s=11 |
| tokenized_agent | false |
| complete | false（prebond継続） |
| status | watch |
| auto-track birth | 2026-06-29T13:29Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-29 初回合成（auto-track birth）

**観測（事実）**
- pump.fun 産・prebond（complete=false）・$85k で検知。
- twitter / website = @marshmello82088（個人アカウント）——DJのMarshmelloではなく一般ユーザーのアカウントとみられる。
- real_sol ~0.27 SOL（極めて低い）・reply_count=0・kol_ca 空。
- "Chill Bullok" = chill（緩い・クール）× bull / bullok（去勢牛）の合成造語。本バッチ bull 命名クラスターの一員。
- mcap $85k は prebond でこの水準 = bonding curve への資金流入が進んでいる。ただし real_sol 0.27SOL との乖離は注目。

**判断**
- [[launchpad-economics]] 直下：prebond × reply0 × real_sol 極低 = mcap 数値が pool SOL 量と乖離——bonding curve の仕組み上、少量 SOL でも高 mcap を示せる初期段階。
- real_sol 0.27SOL × mcap $85k の乖離は prebond 序盤の正常範囲内だが、graduation に向けた追加資金流入の根拠なし。
- traction 全ゼロ × bull vibes 命名 = 本バッチ bull クラスター内で最も thin な social 接続。

**2026-06-29 変化 mcap+76%**: $85k→$149k（prebond 継続）。real_sol ~9.84SOL（9835976 lamports）に増加——bonding curve への継続資金流入が確認できる。ただし reply0・KOL なし・traction0 全継続。prebond での $150k 到達は graduation 圧力が高まっているが、organic 需要の証拠はない。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（prebond・mcap>=30000 gate・real_sol 極低 × traction0）
- [[rug-anatomy]]（traction0 × prebond 出来高先行——graduation 未達リスク）
