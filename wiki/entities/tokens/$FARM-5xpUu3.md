---
type: entity
kind: token
source: auto-track
title: $FARM — MAYHEM FARM（5xpUu3）
mint: 5xpUu3um2L214UekFPz1d9bEofsPckuXXgBAhCkhpump
status: watch
created: 2026-06-26
updated: 2026-06-26
tags: [token, pumpfun, traction0, low-signal, stub, mayhem-cluster]
---

# $FARM — MAYHEM FARM（5xpUu3）

※ ticker 衝突回避: 既存 [[$FARM]](./\$FARM.md) は FarmTown（Moonshot）系の別トークン。本ファイルは mint 先頭6文字で区別。

pump.fun 発。bonding curve 未卒業（complete=false）。名称「MAYHEM FARM」——同時期の $MAYHEM-EUkmxX と関連した命名か（same deployer / coordinated launch の可能性）。twitter なし・website なし。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 5xpUu3um2L214UekFPz1d9bEofsPckuXXgBAhCkhpump |
| name | MAYHEM FARM |
| mcap (検知時) | ~$119,978 |
| gate | safety:ok / traction:mcap>=30000 |
| reply_count | 0 |
| KOL (CA確認) | なし |
| twitter | なし |
| website | なし |
| complete | false（未卒業） |
| real_sol | ⚠️ 9,352,477（データ異常の疑い・SOL単位なら不可能な値） |
| tokenized_agent | false |
| 検知日時 | 2026-06-25T23:36Z |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- mcap $119,978・complete:false・reply 0・KOL ゼロ・twitter/website なし
- ⚠️ real_sol=9,352,477 は SOL 単位として桁外れ（pool に 935万 SOL は不可能）——ラムポート表示 or データ取得バグの疑い。実際の pool 流動性は不明。

**判断**:
- "MAYHEM FARM" は [[$MAYHEM-EUkmxX]] と同時期登場——coordinated launch（deployer による複数 mint 同時展開）の可能性がある。
- twitter/website ゼロ・traction ゼロ = social 基盤なし。[[launchpad-economics]] graduated-but-empty 候補。
- ⚠️ real_sol データ異常の場合、pool 流動性の実態が評価できない。次窓で再確認必要。
<!-- synthesis:end -->

## 関連
- [[launchpad-economics]]（mcap gate 通過）
- [[rug-anatomy]]（traction0 死パターン）
- [[$MAYHEM-EUkmxX]]（同時期登場・coordinated launch 疑い）
