---
type: entity
kind: token
source: auto-track
status: dead
title: $FOMO-Em4TPX（Fearless Of Missing Out）
mint: Em4TPXE3P5zCWz31mDre8siqUp4DbJxzYEoWvdbtZhE5
pool: 9dQWGcwVAExD1Ju4JMf6g6PVTVy57Aspci7d4X6v9ngJ
created: 2026-06-29
updated: 2026-06-29
tags: [trench, entity, token, auto-track, watch]
---

# $FOMO-Em4TPX（Fearless Of Missing Out）

mint 先頭6文字 Em4TPX で識別（同名 ticker $FOMO が同バッチ3mint同時発射のため）。

## ライフサイクル(auto-track)
| 項目 | 値 |
|---|---|
| mint | Em4TPXE3P5zCWz31mDre8siqUp4DbJxzYEoWvdbtZhE5 |
| pool | 9dQWGcwVAExD1Ju4JMf6g6PVTVy57Aspci7d4X6v9ngJ |
| gate | safety:ok / traction:graduated |
| mcap(birth観測) | $17,574（2026-06-28T21:35Z） |
| peak_mcap | $17,574（暫定） |
| real_sol | 0 |
| reply_count | 0 |
| twitter | https://x.com/TrollFootball2/status/2071344581443264571 |
| website | null |
| tokenized_agent | false |
| complete | true（graduated） |
| status | watch |
| auto-track birth | 2026-06-28T21:35Z |

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）

### 2026-06-29 初回合成（auto-track birth）

**観測（事実）**
- pump.fun 産・complete=true（graduated）・2026-06-28T21:35Z 検知。
- mcap $17,574。real_sol=0・reply_count=0・kol_ca 空。
- twitter: @TrollFootball2（サッカー系 meme アカウント）。tokenized_agent=false。
- **同名 3mint 同時発射**: 同バッチに $FOMO(DB2Pb1) $1,267 / $FOMO(3o1GSQ) $2,286 / 本 mint $17,574 が同時検知。DB2P と 3o1G は同バッチ内で誕生即死確定（死亡台帳入り）。本 mint が 3 mint 中の最高 mcap 生存者。

**動線・型**
- [[launchpad-economics]]: "Fearless Of Missing Out" = FOMO の逆説的命名（FOMOを恐れない者/恐れながらも突っ込む者）。crypto trench の感情的コア「FOMO」を ticker 化。
- multi-mint wave: 同名 3 mint が同時発射 = deployer 競争 or 同一 deployer の自己分散の可能性。下位 2 mint の即死で需要が本 mint に集中した可能性。
- @TrollFootball2（サッカー fan × troll 系）は FOMO 命名との接続が不明確。deployer 設定の可能性。
- real_sol=0 × reply=0 × kol_ca 空 = traction なし状態での $17k 生存。

**賭け仮説**（confidence=低）
- multi-mint で上位 mint が生き残るパターンは過去に確認（$FOMO 系での需要集中）。ただし T3ゼロ × real_sol=0 継続なら [[rug-anatomy]] "graduated-but-empty" 型崩壊デフォルト。@TrollFootball2 の独立 KOL 言及があれば格上げ候補。

### 2026-06-29 死亡確定

**観測（事実）**
- 最終 mcap $3,703（2026-06-29T00:52Z）。peak $17,574 → last $3,703（-78.9%）。
- outcome: **died**。cause: mcap枯れ（$3,703）。3 mint 中の最高位 mint も最終的に枯死。
- multi-mint 需要集中も traction0 × real_sol=0 の前では無効——「同名最上位 mint 生き残り」は一時的優位にすぎず生存保証にならない N=1 追加。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]
- [[rug-anatomy]]
