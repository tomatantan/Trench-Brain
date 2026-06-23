---
type: lint
title: Lint Report — 過学習リスク・矛盾・陳腐化 検出
updated: 2026-06-23
---

# Lint Report（2026-06-23）

検出 **10件**。重大度順。**報告のみ・自動修正なし**。

---

## 🔴 重大度 HIGH

### 1. rug-anatomy 死亡台帳: N=1 で "traction0→高死亡率" を主張している
**該当ページ**: [[rug-anatomy]] 死亡台帳  
**証拠**:  
- 正式エントリ: `$KRILLION` 1件のみ（"誕生即死"）  
- 「traction(reply/KOL)ゼロ × 出来高先行で上げた銘柄は死亡率が高い」の具体例として挙がる $AXIOS（peak比-76%）・$TBHR（-86%）は **status:fading**。死亡台帳未記入、`base_rate.json` の `died=0` に対応  
- 「死の最大の先行指標は traction の不在」は1件の正式死亡 + 2件の進行中ケースで支えられている  

**なぜ過学習リスクか**: 死亡を確認していない事例を「死亡率が高い」の根拠に混用している。fading ≠ dead。型が立っているように見えて分母が揃っていない。  
**提案**: 死亡台帳エントリ条件を明文化する（例: "peak比-90%以上を RETIRE と呼ぶ"）。$AXIOS/$TBHR が閾値を超えた時点で台帳に記入し、その時点で型の主張を強化する。現状は "台帳エントリ前の仮説" として括弧書きに格下げを検討。

---

### 2. launchpad-economics の auto-track base rate が base_rate.json と乖離
**該当ページ**: [[launchpad-economics]] "auto-track 実観測コホート" ブロック  
**証拠**:  
- concept 記載: "mints 観測 900 / 門通過 11（1.2%）/ graduated 6 / 死 0"  
- `brain/state/base_rate.json` 現在値: `mints_seen: 1800, gate_passed: 17, died: 0, graduated: 10`  
- 差異: mint数 900→1800（2倍）、gate 11→17（+55%）、grad 6→10（+67%）  

**なぜ過学習リスクか**: 内部数字が整合していない状態で「1.2%」などを引用すると、自前データが持つ信頼性（"外部主張と自前観測が一致"という主張）が崩れる。  
**提案**: launchpad-economics の auto-track ブロックの数値を base_rate.json の現在値に更新（gate_passed/mints_seen 比 = 17/1800 ≒ 0.94%、外部 1.5% との差異は方法論の違いを注記）。

---

### 3. reflexivity "traction無し跳躍＝崩れる" の確証フレームが早い（$MOONLAKE 反証が現存）
**該当ページ**: [[reflexivity]] §★実時間の実証  
**証拠**:  
- 概念は「確証されつつある」と表現  
- $MOONLAKE: traction0、+147%、$1.03M突破、**2026-06-23 現在も崩壊していない**（反証候補として概念内に明記はあり）  
- 完全弧が確認できているのは $PHONEBLACK（1件）のみ。$AEGIS/$RO は "fading" 進行中  

**なぜ過学習リスクか**: ⚠️自体は概念内に書かれているが、上の「実証」節が "確証" トーンで書かれており、⚠️との重みが逆転している。読み手が「もう確定した型」と受け取りやすい。反例 $MOONLAKE が解決していない以上、型の主張は「仮説段階」が正確。  
**提案**: 「確証されつつある」→「仮説支持（完全弧 N=1・$MOONLAKE 未解決）」に書き換える。$MOONLAKE の決着がついた時点で型の状態を更新する。⚠️を先に書き、実証は後に置くよう順序を入れ替える。

---

## 🟠 重大度 MEDIUM

### 4. majors-rotation-supercycle: "AI が crypto の酸素を吸っている" は単一ソース1 podcast
**該当ページ**: [[majors-rotation-supercycle]] §2026-06-23 追記  
**証拠**:  
- 出典: `bankless-arthur-hayes-ai-crash-bitcoin-1m-2026-06-22` のみ（Arthur Hayes × Bankless 対談 1本）  
- 独立した2次確認なし  
- 代替説明（金利水準・サイクルタイミング・規制圧力）は当追記セクションに存在しない  

**なぜ過学習リスクか**: 「今サイクルのalt season の弱さ」という観測は複数の説明が競合できる問題。thedefiedge の供給希釈論を "補強" として並置しているが、因果が独立な2説を「重なる」と表現することで、どちらも独立した検証を受けていない。Hayes 自身も "AI 継続なら crypto 酸素不足のまま" と timing 不明を明言。  
**提案**: 追記セクションの頭に「出典: Hayes 単独、timing 不明」の bracket を付加。供給希釈論（thedefiedge）との関係を "補強" でなく "独立した別仮説" として記述。

---

### 5. regulation-catalyst: "strategic reserve 仕込み投稿" が単一ジャーナリスト報告で断定的に記載
**該当ページ**: [[regulation-catalyst]] ⚠️矛盾・懐疑  
**証拠**:  
- 記述: 「strategic reserve（XRP/SOL/ADA）の Trump 投稿は Ripple 系ロビー会社が仕込んだもの」  
- 出典: `@laurashin` 1件のみ  
- 一次確認（Trump 側・Sacks 側の発言）なし  

**なぜ過学習リスクか**: ジャーナリスト報告を "仕込み確定" として扱うと、政策リスク評価が過大になる。同じ指針6（観測と推論の分離）を policy 言説にも適用するよう regulation-catalyst 自身が示唆しているが、この記述はその規律に反する。  
**提案**: 「仕込んだもの」→「@laurashin が仕込み報道（一次未確認）」に表現を変える。

---

### 6. reflexivity がほぼ全 concept に接続され "何でも説明するハンマー" リスク
**該当ページ**: [[reflexivity]] §既存 concept をこの1原理で束ねる  
**証拠**:  
- 接続先: launchpad-economics / survivor-memes / rug-anatomy / onchain-verification / majors-rotation-supercycle / spacex-ipo-narrative / external-event-to-token-pattern — 13 concept ほぼ全て  
- 「reflexivity の燃料が無い」「reflexive ゆえ突然」「reflexive なローテ」と異なる現象を同一語で説明  

**なぜ過学習リスクか**: 一般理論はどの現象にも貼り付けられる＝反証条件が不明確になる。$MOONLAKE のように反例が出ても「まだ燃料切れ前」で説明できてしまう。Soros の reflexivity は株式の fundamentals に対して機能するが、trench では "fundamentals がない" 点でそもそも応用域が拡張されており、オリジナルの制約が外れている。  
**提案**: "reflexivity で説明できない / reflexivity が当てはまらないケース" を1セクション追加する。反証条件（「何があったら reflexivity を否定できるか」）を明示することで理論の予測力を維持する。

---

### 7. ai-memes: corpus 強気一色・崩壊例ゼロ、懐疑の実例が薄い
**該当ページ**: [[ai-memes]] ⚠️矛盾・懐疑  
**証拠**:  
- 自認: 「corpusは強気一色: 名指しのAI-meme($ai16z/$GOAT/$Fartcoin等)にrug/崩壊の記録が無い」  
- 提示されている懐疑: @blknoiz06「勝者不明」/ @lmrankhan「自壊論」/ @DefiIgnas「上場歪み」の3件のみ  
- $ai16z / $GOAT / $arc の現在価格推移・崩壊例は取り込まれていない（"上昇局面のみ採取" を自認している）  

**なぜ過学習リスクか**: 「桁違いの PnL（6,400x）」を冒頭に置きながら崩壊例をゼロのまま「⚠️」だけで注記する構造は、読み手に強気バイアスを与える。懐疑3件の重みが PnL の印象に見合っていない。  
**提案**: $GOAT / $ai16z の現在値または崩壊例を少なくとも1件 sources に追加し、⚠️に「崩壊実例」として記載する。survivor-memes と同様に "rug/崩壊の記録が無い = 生存者バイアスの典型" を ⚠️ の冒頭に移動。

---

## 🟡 重大度 LOW

### 8. spacex-ipo-narrative: "示唆 / 賭けの仮説" セクションが全騰幅消去後も更新されていない
**該当ページ**: [[spacex-ipo-narrative]] §示唆 / 賭けの仮説  
**証拠**:  
- 示唆テキスト: "perp側=OI/funding/取引所(Hyperliquid/Binance/MEXC・出来高の主流)／spot側=機関フロー・real-share backing(未検証)" — 全騰幅消去前の視点のまま  
- 時系列: 「6/23 全騰幅消去確定 + Hayes thesis 部分実現」が時系列末尾に追記されているが示唆テキストとの整合が取れていない  

**なぜ過学習リスクか**: "現在の示唆" として読むと古い前提のまま。「9月 unlock が Hayes thesis の検証ポイント」という記述（追記 Hayes 節）が示唆セクションに反映されていない。  
**提案**: 示唆セクション冒頭に「(2026-06-23 更新: 全騰幅消去済・Hayes thesis 部分実現。以下の示唆は9月 unlock 前提で読む)」の注記を追加。

---

### 9. external-event-to-token-pattern: 本文「6件超」vs ⚠️「2-3件」の内部矛盾
**該当ページ**: [[external-event-to-token-pattern]] §この型から言える示唆 vs ⚠️未確認  
**証拠**:  
- 本文: 「サンプルが2-3→6件超に増え、型の確度が上がった」  
- ⚠️セクション: 「サンプル数まだ少(2-3件)。型の確度を上げるには...」  

**なぜ過学習リスクか**: 同一ページ内で confidence が矛盾している。後者は前者更新前の記述が残留している。  
**提案**: ⚠️セクションを「6件超に増加した現時点でも、過去の同型事例（選挙/ETF承認等）との比較検証が不足。型の確度は上がったが historical backtest は未実施」に書き換え。

---

### 10. $CLUTCH: external-event-to-token-pattern の表に登場・source も entity ($CLUTCH) も動線ページもなし
**該当ページ**: [[external-event-to-token-pattern]] 実例テーブル  
**証拠**:  
- テーブル: W杯/FIFA発端 → meme側 $CLUTCH と記載  
- `wiki/entities/players/@Clutch_FIFA2026.md` は存在するがトークン entity `$CLUTCH` は未作成  
- 動線ページ: `—`（リンク先なし）  
- sources: ゼロ  

**なぜ過学習リスクか**: テーブルに載っているのに一次ソース・entity・動線がない = 外部主張（誰が言ったか）が消えた素の "型の適用例" になっており検証不可。  
**提案**: $CLUTCH のソースが存在する場合は entity と sources を作成し外部イベント → token の実例として繋げる。ソースが無ければテーブルから「（ソース未取得・参照保留）」の注記を付ける。

---

## 芯チェック（完了節目 ② 確認）

- `health.jsonl` 直近値: `signal_backlog=5`（bounded・非増加）→ 芯 OK
- 自動修正なし・概念削除なし → 指針1・8 OK  
- 全検出に証拠（ページ引用・数字）付き → 断定はデータから（思想5 OK）
- 報告後 git は触らない（cron指定）

---

## 次に人/合成が手を入れるべき TOP 3

1. **rug-anatomy 死亡台帳の記入条件を明文化し、$AXIOS/$TBHR が閾値超えた時点で台帳入り** — 「traction0→死」仮説の N をまず揃える。N=1 で型化するのはリスクが高い。
2. **launchpad-economics の auto-track数値を base_rate.json と揃える** — 内部矛盾の最も簡単な修正。門通過率・graduation率の数値が wiki 内で統一されることで、引用の信頼性が上がる。
3. **reflexivity に "この枠組みが当てはまらない条件" セクションを1つ追加** — ハンマー化を防ぐ最小の修正。$MOONLAKE 決着とセットで、型の適用範囲を明示する。
