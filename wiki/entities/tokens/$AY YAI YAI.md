---
type: entity
kind: token
title: $AY YAI YAI (ay yai yai) — Elon tweet association marketing
mint: 72T6RQLFc7TVn9EGEyR5iZqPFFpGAiZqov5QkzKypump
source: auto-track
status: dead
created: 2026-06-25
updated: 2026-06-25 (第99窓)
tags: [token, pumpfun, graduated, traction0, association-marketing, multi-mint, meme, dead]
---

# $AY YAI YAI (ay yai yai) — 72T6RQ

pump.fun 発。bonding curve 卒業済。twitter=Elon Musk ツイートリンク（association marketing）。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 72T6RQLFc7TVn9EGEyR5iZqPFFpGAiZqov5QkzKypump |
| name | ay yai yai |
| mcap (birth→直近) | ~$108k（2026-06-25T08:42Z）→ **$157.7k（2026-06-25T09:03Z・+44%）** |
| gate | safety:ok / traction:graduated |
| reply_count | 0 |
| KOL (CA確認) | なし |
| twitter | https://x.com/elonmusk/status/2070042592012570970（Elon Musk ツイートリンク） |
| website | なし |
| real_sol | ~56.4 SOL（56,395,061,722 lamports） |
| tokenized_agent | false |
| 検知日時 | 2026-06-25T08:42Z |

<!-- synthesis:start -->
## 合成メモ

**観測（事実）**:
- "ay yai yai" テーマ・Elon Musk のツイート URL を公式 twitter 欄に設定（association marketing）
- reply 0・KOL CA 言及なし
- real_sol ≈ 56.4 SOL — 同テーマ競合 `$YAI`（real_sol=0）よりプール流動性が実際に存在
- 同時刻に `$YAI`（mint=3cYFJEDn）が同テーマで並走中 → multi-mint 競合

**⚠️ 一次ソース未確認**:
- Elon Musk ツイート(2070042592012570970)の内容は sources/x 未収録。"ay yai yai" meme との連関は未検証。

**判断**:
- Elon Musk ツイート link = [[rug-anatomy]] 「authority 借用型 association marketing」（$CLO の a1lon9/$LION の NatGeoTV 同型）
- real_sol=56.4 SOL は流動性的に差別化されているが、traction（KOL/reply）ゼロのままでは social demand が存在しない
- `$YAI` との 2 mint 競合：$108k vs $110k で拮抗 = 需要分散・両倒れリスク
- ⚠️ association marketing × traction0 × multi-mint 競合 = [[rug-anatomy]] 典型シグネチャ

**賭け仮説**: Elon tweet 借用でも有機的 community が追随しない限り graduated-but-empty 死亡パターン。real_sol の存在が出口流動性として deployer に有利に働く可能性。

**2026-06-25T09:03Z 更新（+44%・$109.6k→$157.7k）**:
- **観測**: prev_mcap=$109,680 → $157,788（+44%）。reply_count=0・KOL 変化なし。complete=true・real_sol=56,395,061,722（56.4 SOL）継続。
- 出来高があり mcap は伸長しているが、traction（KOL/reply）は依然ゼロ。
- Elon Musk association marketing × real_sol 56.4 SOL の流動性バックアップが pull として機能している可能性（$YAI との 2 mint 競合がある中で $AY YAI YAI 側に資金集中している示唆）。
- ⚠️ traction0 継続 × association marketing = [[rug-anatomy]] シグネチャ変わらず。$157k まで達してもコミュニティ需要が存在しない構造。deployer 出口のための mcap 上昇 or 短期投機と判断。
- 次の確認ポイント：①KOL/reply が付くか ②$YAI との競合が収束するか ③real_sol が引き出されるか

**2026-06-25T09:26Z 死亡確定（$157.7k → $2,300・-98.5%）**:
- **観測**: peak_mcap=$157,788 → last=$2,300（peak比 **-98.5%**）。cause: mcap枯れ($2300)。
- Elon Musk association marketing × multi-mint競合（$YAI / $AIAIAI-Cbqrm9 ← 同バッチで3本目出現）× traction0 → 崩壊確定。
- real_sol=56.4 SOL が deployer 出口流動性として機能した可能性。$157k で売り抜けた構造。
- ⚠️ 同バッチで TICKER="AIAIAI" の3本目 mint（Cbqrm9）が $111k で観測中——同じ Elon tweet 借用・同パターン継続中。
- **outcome: died**。→ [[rug-anatomy]] 死亡台帳 N=87 に算入。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（graduated-but-empty コホート）
- [[rug-anatomy]]（association marketing 型・multi-mint 競合型）
- [[$YAI]]（同テーマ競合 mint）
