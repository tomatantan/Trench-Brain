---
type: entity
kind: token
source: auto-track
status: watch
ticker: $AURUM+
mint: 5AkPFPnjuJvg7fqSTnJL7Qr6RVYa3fr8Sfix4fwepump
created: 2026-06-29
updated: 2026-06-29
tags: [token, pumpfun, prebond, traction0, duplicate-brand, stub]
---

# $AURUM+ (3rd mint) — Aurum +（5AkPFP）

pump.fun 発。bonding curve 未完（complete=false・prebond）。"Aurum +" 同名の 3rd mint——先行する [[$AURUM+]]（7Bis8dfy）と [[$AURUM+-FAuihE]]（FAuihEJ・2nd mint）がすでに存在。twitter/website なし。KOL なし・traction0。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 5AkPFPnjuJvg7fqSTnJL7Qr6RVYa3fr8Sfix4fwepump |
| name | Aurum + |
| pool_address | G9Ti413dPHG54xYbTCEkr6AjdiACwjNn5Fsqj7LBKFYV |
| 初検知 mcap | $43,834（2026-06-29T04:01Z） |
| gate | safety:ok / traction:mcap>=30000 |
| reply_count | 0 |
| KOL（CA確認） | なし |
| twitter | なし |
| website | なし |
| tokenized_agent | false |
| real_sol | 8,724,745 |
| complete | false（prebond） |

<!-- synthesis:start -->
## 合成

**観測（事実）**:
- 同名 mint が既に 2 本存在する中で出た 3rd mint（1st: 7Bis8dfy $32k、2nd: FAuihEJ $54k、本件: 5AkPFP $43k）。
- prebond × twitter/website なし × reply0 × KOL なし。traction0 × real_sol=8.7M（lamport 換算 ~0.009 SOL）。

**判断**:
- 同名 3rd mint の反復出現——1st/2nd がともに traction を築けないまま別 deployer が参入し続けるパターン。共倒れ確率は上昇するのみ。
- [[rug-anatomy]] ⑨同ブランド再登場型の多重発射版（3本）。いずれも community ゼロなら全滅確定。
- prebond × traction0 × social 皆無 = 合成の起点がなく stub で留まる。

**概念接続**: [[launchpad-economics]]（prebond・traction0・同名多重mint） / [[rug-anatomy]]（⑨同ブランド再登場・3rd mint共倒れ）
<!-- synthesis:end -->

## 関連
- [[$AURUM+]]（1st mint・7Bis8dfy）
- [[$AURUM+-FAuihE]]（2nd mint・FAuihEJ）
- [[launchpad-economics]]
- [[rug-anatomy]]
