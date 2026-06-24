---
type: lint
title: Lint Report — 過学習・矛盾・知識ギャップ検出
updated: 2026-06-24
---

# Lint Report（2026-06-24）

> 目的: wikiが"過学習"していないか・矛盾があるか・型のN不足はないかを敵対的に検出。自動修正しない。
> スコープ: wiki/concepts/ 全16ページ + rug-anatomy 死亡台帳 + launchpad-economics 跳躍台帳 + brain/state/base_rate.json + wiki/log.md。
> 検出件数: **10件（HIGH 3 / MEDIUM 4 / LOW 3）**。

---

## HIGH — 即手当て推奨

---

### H1: launchpad-economics.md の base_rate 数値が "同期済" を主張しながら乖離

**該当**: `wiki/concepts/launchpad-economics.md` auto-track 実観測コホートセクション

**証拠（数字）**:

| 指標 | launchpad-economics.md（本文） | brain/state/base_rate.json（現値） | 差分 |
|------|------|------|------|
| mints_seen | 11,717 | **12,017** | +300 |
| gate_passed | 92 | **95** | +3 |
| graduated | 70 | **73** | +3 |
| died | 42 | **45** | +3 |

本文には「`brain/state/base_rate.json` と同期」と明記されているが、現時点で偽。

**なぜ過学習リスクか**: Feedback セクション（75%/13%/12%/55% の型 hit-rate）の計算根拠となる N が「died=42/gate=92」時点のもの。現在 died=45, gate=95 で3件増えており、3件の型分布が未確認。"定量的に確定した型"という印象が実際より先行している。

**提案**: base_rate 現値（mints=12,017 / gate=95 / graduated=73 / died=45）に更新。Feedback N=95 時点の数値を feedback.py で再採点し、変化があれば上書き。

---

### H2: Feedback セクション N=92 の内訳に 3 件の不明分（分母不整合）

**該当**: `wiki/concepts/launchpad-economics.md` Feedback セクション + `wiki/concepts/survivor-memes.md`（同数値を転記）

**証拠（内訳の検算）**:

```
門分類: 49（graduated） + 22（mcap勢い） + 18（other） = 89 ≠ 92
traction分類: 17（有り） + 72（無し）                 = 89 ≠ 92
```

どちらの分類軸でも 3 件が未分類のまま。本文は「N=92 に育ち」と書いているが分母が 89 で計算されている可能性がある。

**なぜ過学習リスクか**: 75%（37/49）・55%（40/72）という具体的な死亡率が 3 件の分類漏れを内包している。これらの 3 件が traction 有りだった場合、12% というシグナルが変動する。survivor-memes.md は同じ数値を「最強の early signal」としてそのままコピーしているため影響範囲が広い。

**提案**: feedback.py 出力ログから 3 件の所在（mint CA）を確認し、門分類・traction 分類を明示。その上で % を再計算して launchpad-economics.md / survivor-memes.md 双方を更新。

---

### H3: manipulation-playbook の「traction有=生存は未支持」が実データと逆方向

**該当**: `wiki/concepts/manipulation-playbook.md` "横断" セクション

**証拠（引用と実数の対照）**:

- manipulation-playbook.md: 「[[feedback]] の「**traction有=生存は未支持**」と整合」
- launchpad-economics.md Feedback: 「traction有り **死12%（2/17）** vs traction無し **死55%（40/72）**」
- survivor-memes.md: 「tractionが**最強の早期生存signal**」

死亡率 12% = 生存率 88%。これを「生存は未支持」と表現するのは **逆方向のフレーミング**。データは「traction があっても生存を保証しない」を示しているが、それは「未支持」ではなく「有意に生存を助けるが非十分条件」。

**なぜ過学習リスクか**: manipulation-playbook は「traction を見ても信頼するな」という結論方向で使われる文脈だが、「未支持」という語は「traction=無価値」の読み方を生じさせ、launchpad-economics の「最強のシグナル」と真逆の印象になる。screening ロジックに矛盾を埋め込む。

**提案（⚠️旗のみ・主張書き換えなし）**: 「traction有=生存は未支持」の行に
`⚠️ 表現注意: データは死亡率12%(traction有) vs 55%(無)→ tractionは有意に生存を助けるが保証しない。「未支持」でなく「非十分条件」が正確。` を1行追記。

---

## MEDIUM — 次のサイクルで対処推奨

---

### M1: traction=survival signal が 4 ページで参照されるが全て同一 N=92 コホート（偽独立）

**該当**: `reflexivity.md` / `launchpad-economics.md` / `survivor-memes.md` / `rug-anatomy.md`（各ページの traction→生存言及）

**証拠**: 4 ページが参照するデータの起源は全て同一——brain/track.py が同一時間帯・同一 launchpad（Pump.fun）で観測した N=92 のコホート。ページが分かれているだけで独立した複数ソースによる確認ではない。

**なぜ過学習リスクか**: 同一コホートを 4 ページが引用すると、読み手には「4 回独立確認」に見える。特定の市場環境・時間帯・launchpad 固有の状態が型として固着するリスク。「KOL がいない相場環境」では traction シグナル自体が弱まるが、それが検出されにくくなる。

**caveat の現状**: launchpad-economics の「同一launchpad・近時間帯で独立性低」は記述済。reflexivity / rug-anatomy / survivor-memes には同等の留保が無い。

**提案**: reflexivity・rug-anatomy・survivor-memes の traction signal 言及箇所に「（N=92 / 同一 Pump.fun コホート・単一時間帯、launchpad-economics の独立性留保参照）」を短く添える。

---

### M2: broken link 3 種（[[kol-track-records|KOL track-record]] / [[feedback]] / /check）

**該当**:
- `manipulation-playbook.md`: `[[kol-track-records|KOL track-record]]` × 2 箇所、`[[feedback]]` × 1、`/check` × 1
- `survivor-memes.md`: `/check` × 1

**証拠**: wiki/concepts/ に [[kol-track-records|KOL track-record]] は存在しない。[[feedback]] は launchpad-economics.md のセクション名であり独立ページではない。/check も独立ページ不在。

**なぜ過学習リスクか**: manipulation-playbook の型1（pumper exit 検出）は「[[kol-track-records|KOL track-record]]で過去callの生存率を照合」を処理の核に置いているが、そのページが存在しない。防御ロジックの核心部分が宙に浮いている。型が機能している体裁だが、照合先が無いため型1は今のところ半完成。

**提案 top-1**: [[kol-track-records|KOL track-record]] concept を新設。players/ にある KOL entity（@CryptoHayes/@blknoiz06/@theunipcs 等）の call 実績・PnL・逆指標歴を横断合成したページ。manipulation-playbook の「勝ち自慢→call 信頼性」文脈に直結。

---

### M3: external-event-to-token-pattern が最古更新（2026-06-22）で多数の新例未反映

**該当**: `wiki/concepts/external-event-to-token-pattern.md`（全16 concept 中唯一 2026-06-22 のまま）

**証拠（log から抽出した未反映の新例）**:
- GTA-VI wave: $MACCA / $GTASOLANA / $GTA / $B4GTA6（launch-pulse 第9窓以降 IP/brand +45% 急増）
- 欧州イベント借用型: $VINTEDGATE（Vinted 論争→欧州ミーム型・死亡確定）
- association marketing 確定例: $TOROS（Toros Finance 借用×BREAKOUT-then-dead 3窓12h完結）
- $ANYONE（@jup_studio 借用・1サイクル完全崩壊 -99.7%）

ページ末尾には「サンプル数まだ少(2-3件)」の注記が残存。本文中には「6件超」とあり内部矛盾もある。

**なぜ過学習リスクか**: 「政治/要人 meme = grift サブ型」のみが例証されており「IP 借用/イベント便乗→即死サブ型」が未反映。GTA-VI wave の IP 便乗は2窓連続で IP/brand 急増として観測済で型の再現を確認したが、型の知識として焼かれていない。次の同型 wave（FIFA後、著名IPリリース等）で予測精度が低いまま判断が走る。

**提案**: 2026-06-22 以降の新例（GTA-VI IP wave, $VINTEDGATE, $TOROS/$ANYONE）を追記し「IP 便乗→即死サブ型」として分類。「サンプル数まだ少」注記を削除。rug-anatomy との逆リンクも追加。

---

### M4: launch-pulse KOL 真空「定常化疑い」が null observation からの過推論

**該当**: `wiki/concepts/launch-pulse.md` 直近観測セクション末尾「低エネルギー相の定常化疑い」

**証拠**: 48 窓連続 KOL ゼロは観測事実。ただし「定常化」という推論は1窓で KOL が出現すれば即座に反証される。「12日間出ていない」は持続する null であって構造変化の証拠ではない。

**なぜ過学習リスクか**: 「定常化」というフレームが判断前提に入ると、次に KOL が出現した時に「例外的1窓」として過小評価するリスクがある。KOL シグナルが出た時の感度が下がる方向の過学習。「疑い」はついているが「低エネルギー相」というカテゴリラベルに引きずられる。

**提案**: "定常化疑い" → "本観測期間内最長記録（前例なし）" に表現を変更。「KOL が出現した瞬間が仮説の反証トリガー → その時点の KOL の質・フォロワー数・波及速度を重点観測」の一文を追記。

---

## LOW — 長期的に対処

---

### L1: rug-anatomy 死亡台帳 N=28 vs base_rate died=45 の残差 17 件が型分析に未反映

**該当**: `wiki/concepts/rug-anatomy.md` 死亡台帳

**証拠**: base_rate.json died=45。台帳掲載は 28 件（62%）。差分 17 件の型（traction 有無・entry 門・死因）が分析対象外。

**なぜ過学習リスクか**: 台帳が curated sample である設計は正しい。ただし 17 件（38%）が無記録であることは末尾の「型の言語化」で明示されていない。もし 17 件に traction 有りの死亡例が含まれるなら「traction 無し → 死亡が頻繁」の型強度が過大評価される可能性がゼロでない。

**提案**: 台帳末尾「現時点で浮いている型」冒頭に「台帳は gate_passed 95 のうち記録済 28 件（残 17 件は型分類未実施、独立性留保と同根）」を一文追記。次回合成で残差 17 件を簡易分類（traction 有無だけ）できれば型の頑健性が上がる。

---

### L2: majors-rotation-supercycle「4 枯渇」合成の watchlist echo chamber（反論収集ゼロ）

**該当**: `wiki/concepts/majors-rotation-supercycle.md` 横断合成セクション（2026-06-23 追記）

**証拠**: 4 系統の "独立した" 枯渇説明:
1. Hayes「AI が酸素を吸う」← Bankless × Hayes（単一 podcast。⚠️ 既記）
2. thedefiedge「供給希釈」← watchlist の1アカウント
3. STRC/MSTR overhang ← Bankless（1と同一メディア圏）
4. reflexivity 低エネ ← 自wiki合成（自己参照）

1+3 が同 Bankless ecosystem、4 が自己参照。「4 本の独立説明が収束」だが独立性が薄い。「bull が強い根拠」の対立論が収集されていない（watchlist が bulls-on-crypto bias を持つ可能性）。

**提案**: 合成セクションに「⚠️ 4 系統は全て bearish-on-near-term-bull な corpus から抽出。watchlist の強気側（theunipcs の melt-up 煽り等）との対照を明示的に確認する必要あり」を一文追記。

---

### L3: regulation-catalyst AI 輸出規制セクション — Illia thesis の「断片化前例」が一次未検証

**該当**: `wiki/concepts/regulation-catalyst.md` AI 輸出規制セクション

**証拠**: 「Fable 5 export control = インターネット断片化の前例」という Illia thesis は引用済み。⚠️ が4箇所立っており旗管理は適切。ただし export control の実際の法的スコープ（誰がどこで制限されるか）の一次情報が未格納。

**なぜ過学習リスクか**: 軽度。⚠️旗の質は適切。ただし「イランとの同列化は修辞的飛躍」という反証の具体事実がない状態で thesis が引用されている。将来の AI ナラティブの判断に使う際、飛躍の程度が不明なまま前提に入る可能性。

**提案**: 優先度低。Fable 5 export control の実際の禁止対象（federal register 等の一次情報）が取得できた場合に限り当セクションに追記。

---

## 次に人/合成が手を入れるべき Top 3

1. **H3 → manipulation-playbook への ⚠️ 1行追記**（最速対応・1行修正）: 「traction有=生存は未支持」は screening ロジックの逆方向フレーミング。誤読が実際の判断に影響するため最優先。

2. **M2 → [[kol-track-records|KOL track-record]] concept 新設**（合成エージェントで対応）: manipulation-playbook の型1の照合先。players/ の KOL entity の call 実績を横断合成し「KOL 信頼性マトリクス」として立てる。[[kol-track-records|KOL track-record]] は既に players/AdimsSHOGUN.md 等で実測ベースの track-record 合成が始まっているため、それを束ねる concept として位置づけ可能。

3. **M3 → external-event-to-token-pattern 更新合成**（合成エージェントで対応）: 全 concept 中唯一の最古更新ページ（2026-06-22）。GTA-VI IP 波・association marketing 確定例・$VINTEDGATE 欧州イベント型の3サブ型を追加。「IP 借用→即死」の死亡例 N を明示し、rug-anatomy との接続を強化。
