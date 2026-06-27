---
type: entity
kind: token
source: auto-track
status: watch
ticker: $VENEZUELA
mint: 6eSzwRMLjK24g1NAYWUABAq9qDCDT2MW4hsbt513pump
created: 2026-06-27
updated: 2026-06-27 (auto-track synth_queue 05:41Z: prev$78k→$44k -44%・birth$147k比-70%・崩壊フェーズ移行・dead候補)
tags: [token, pumpfun, graduated, charity-meme, real-world-event, watch]
---

# $VENEZUELA — Venezuela Relief Fund（6eSzwR）

pump.fun 発。"Venezuela Relief Fund" = 実世界の人道的イベント（ベネズエラ支援）命名の charity meme。graduated（complete=true）。$147k。twitter メタデータは `https://x.com/toly/status/2070708342880899405`（Solana 創業者 @toly のツイート URL）だが **kol_ca=[]**＝tracker が当該ツイート内でこの CA を確認できず。⚠️ association marketing 疑い。

## ライフサイクル(auto-track)

| 項目 | 値 |
|---|---|
| mint | 6eSzwRMLjK24g1NAYWUABAq9qDCDT2MW4hsbt513pump |
| Pool | 3QLHQX5UzbvQNE5mFbQd2ciiWZpTJTn4tABwYVakbJbX |
| Gate | safety:ok / traction:graduated |
| 初検知 mcap | ~$147,079（2026-06-27T03:23Z） |
| reply_count | 0 |
| kol_ca | なし（kol_ticker もなし） |
| Twitter (メタ) | https://x.com/toly/status/2070708342880899405 ⚠️ CA未確認 |
| Website | なし |
| complete | true（graduated） |
| real_sol | 0 |
| tokenized_agent | false |

## 追跡ログ

| 観測 | live mcap | 変化 | 備考 |
|----|-----------|------|------|
| birth(03:23Z) | ~$147,079 | — | graduated・real_sol=0。reply:0・KOLゼロ。toly tweet URL をメタに設定（CA未確認）。同名 $FUND mint も同時出現・$2k即死対比。 |

<!-- synthesis:start -->
## 合成

- "Venezuela Relief Fund" = 実世界イベント連動の charity meme——[[external-event-to-token-pattern]] の典型分岐。
- **toly ツイート URL をメタデータに設定**——kol_ca=[] のため tracker は当該ツイート内で CA を確認できていない。Solana 創業者名を利用した association marketing 偽装が最有力（⚠️ [[rug-anatomy]] 赤旗：association marketing 疑い）。
- real_sol=0 × reply=0 × KOL0 = graduated でも traction ゼロ——有機的買い需要の確認なし。
- 同時出現の同名 mint $FUND（AvJede・$2k 即死）と対比すると、$VENEZUELA は相対 winner だが同名コホートの勝ち馬パターン（$arm 2nd mint 型）。ただし T3 ゼロのまま。
- [[external-event-to-token-pattern]] 視点では "支援/charity meme" は KOL による物語拡散があって初めて持続する——toly CA 未確認 × traction0 のまま $147k 維持は難しい。

⚠️ 接近条件: toly の実際の CA 言及確認前・reply>0 or KOL CA 確認前は距離を置く（association marketing 偽装リスク）。

**概念接続**: [[external-event-to-token-pattern]] / [[launchpad-economics]] / [[rug-anatomy]]

**change (synth_queue 05:41Z・-44%)**: prev **$78,669** → now **$44,034**。birth $147k 比 -70%。
- traction0・reply:0・KOLゼロ継続。real_sol=0 不変。twitter メタデータ（toly tweet URL）の CA 未確認状態変わらず。
- $44k は gate 閾値（$30k）まで残り $14k——このまま traction が付かなければ dead 圏に向けて縮退。
- association marketing 疑い × graduated-but-empty × -70% drawdown = [[rug-anatomy]] 崩壊フェーズ確定候補。
- ⚠️ 次窓で $30k 割れ or 枯渇確認なら dead 処理へ。

<!-- synthesis:end -->

## 関連
- [[external-event-to-token-pattern]]
- [[launchpad-economics]]
- [[rug-anatomy]]
