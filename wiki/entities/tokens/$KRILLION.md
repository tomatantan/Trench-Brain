---
type: entity
kind: token
title: $KRILLION
created: 2026-06-23
updated: 2026-06-23
source: auto-track (pump.fun)
tags: [trench, entity, token, auto-track]
status: dead
outcome: died
---

# $KRILLION — Krillion on Sol

> `brain/track.py` が観測→篩(KOL)通過→**死**を検知（auto-synthesis）。mint `8ufh…pump`。

## ライフサイクル（auto-track）
- 初観測→死: 2026-06-23（**誕生と同サイクルで死**）
- 門: kol（[[@badattrading_]] が "$KRILLION" 言及）/ mcap: $2,054（bonding floor）/ reply: 0 / website: 無し
- 死因: **mcap枯れ（$2,054）**＝bonding curve放置 / status: **dead** / outcome: **died**

<!-- synthesis:start -->
## 合成メモ（synthesis / エージェント記述）
- **観測**: Pump.fun mint。bonding floor（~$2k）から動かず・0 reply・website無し＝低エフォート。**誕生と同サイクルで死**＝[[launchpad-economics]] の 98.5%側の生標本。**死の分母**に計上（[[survivor-memes]] の生存者バイアス対策）。
- **★⚠️ 設計発見（KOL門の ticker 衝突）**: [[@badattrading_]] の $KRILLION 分析（CA `DZ9s…ontNk`: snipers 3.8% / insiders 1.2% / no clusters / top70 73.4% / 455 holders avg $90 / "Nfa"）は**別CAの同名トークン**。tracked mint（`8ufh…pump`）≠ badattrading CA＝**ticker衝突**。
  → 改善点: **KOL門は CA で照合すべき**（ticker照合は誤マッチする）＝`brain/track.py` v2。＝この合成（一次ソースを読む規律）が設計バグを検出した実例。
- **rug-anatomy data point**: badattrading の screening 自体は比較的クリーン寄り（snipers/insiders低・クラスタ無し）だが **top70=73.4% 集中・avg bag $90** ＝薄い。そして traction無しで死亡＝「**screening通過 ≠ 生存**」。[[rug-anatomy]] の「勢い門は安全門と別に必須」を実例で補強。
<!-- synthesis:end -->
