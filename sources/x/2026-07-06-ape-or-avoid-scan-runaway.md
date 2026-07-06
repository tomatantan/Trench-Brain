---
type: source
platform: image
via: /add-image
captured: 2026-07-06
tags: [ape-or-avoid, smart-detect, pumpfun, scan, system-health]
---

## 観測（写っているもの）

Trench-Brain 自身の SCAN UI スクリーンショット。

- ヘッダー: "**Ready**" / "Enter a ticker or CA. If backend is live, `/api/score` will return ape-or-avoid intelligence."
- ラベル "**SMART DETECT**" が付いたカードが12枚以上連続表示（2列）。
- 各カードの内容（ticker / name / score / mcap / signal種別）:

| ticker | name | score | mcap | signal |
|--------|------|-------|------|--------|
| BIF | bullwifhat | 41 | $755K | pumpfunbot |
| G | G | 30 | $17K | pumpfunbot |
| G | G | 30 | $17K | pumpfunbot |
| SKYE | SkyeSharkie | 29 | $14K | pumpfunbot |
| SKYE | SkyeSharkie | 29 | $14K | pumpfunbot |
| SKYE | SkyeSharkie | 29 | $13K | pumpfunbot |
| SKYE | SkyeSharkie | 29 | $12K | pumpfunbot |
| G | G | 29 | $16K | pumpfunbot |
| G | G | 29 | $13K | pumpfunbot |
| G | G | 29 | $13K | pumpfunbot |
| G | G | 29 | $14K | pumpfunbot |
| Nigirikobushi | The Crashout Frog | 28 | $10K | pumpfunbot |

- 全カードのシグナル源: `pumpfunbot`
- スコア範囲: 28〜41（BIFが突出、残りは29〜30で均質）

## caption（ユーザー文脈）

「アカン暴走してるｗｗｗｗｗ」→ SMART DETECT が連続大量発火している状態を指す。

## 推論（ナラティブ・型・tier）

**T3推論（システム挙動観察）**: Trench-Brain の ape-or-avoid scan エンジンが pumpfunbot シグナルを大量にフィードしている。同一ticker（SKYE、G）が複数回重複検出されており、デduplication が効いていないか、pumpfunbot 側が同トークンを繰り返し通知している可能性。

**T4推論（健康診断視点）**: CLAUDE.md 指針2・3 の観点で見ると、`pumpfunbot` 由来のシグナルが「門」として機能しているか要確認。score が29〜30に密集しているのは閾値付近のノイズが通過しているサイン。BIF (score 41, $755K) は突出しており信号として明確。小mcap帯（$10K〜$17K）の量産カードは backlog を増やすだけのリスク。

**関連concept**: [[ape-or-avoid]] / [[launch-pulse]] / [[rug-anatomy]]（低mcap帯の大量検出=rug候補密度の指標にもなりうる）
