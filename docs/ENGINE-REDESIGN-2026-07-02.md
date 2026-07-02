# Trench-Brain Engine 再設計 — KOLの脳をモデル化する複利LLM Wiki（モデル非依存）

> 本人mandate(2026-07-02): LLM Wiki**そのもの**を根本から良くする。Fableだからでなく**どのAIでも同じ品質で回せる**設計＋マニュアルに落とす。完璧を追求。
> 権威: `docs/LLM-WIKI.md`(原典) / `CLAUDE.md`(憲法9指針) / この文書は現engineの検証済み解剖(4-agent audit + linchpin実測)の上に立つ。

---

## 0. これは何を作り直すか（目的の確定）

**LLM Wikiの真の目的＝「トークン当て機」でなく「勝ってるトレーダー/KOLの"脳"をモデル化する機械」。**

- 主役は**銘柄でなく人**。Twitter上のKOL・手法/マインドセット発信者から、①意思決定プロセス ②売買動機 ③思考の型 ④KOLへの成長論 を、発言と実行動から合成する。
- 多数のKOLを重ねて **共通点（勝者が共有する思考）と矛盾（誰と誰が割れ・どの相場でどっちが正しいか）** を抽出。
- 出力＝「**この相場で、この型ならこう読み・こう動く**」＝弱小トレーダーが勝者の頭を借りて強くなる。
- 銘柄/オンチェーンは主役でなく**KOLの読みの答え合わせ材料**（当てたか外したか）。
- 共有前提（meme tradeは一人でできない）＝公開する果実。moat＝時短できない積み上げ（[trench-brain-world-engine-moat]）。

### 合格基準（"great"の定義・これで設計をテストする）
> ある問いへの回答が **relay（得た情報の羅列）なら不合格**。**synthesis of winning minds（勝者の頭を貸す）なら合格**。
- ❌ relay例: 「$SEXY +156%、$BULLATLAS +107%、reply0…」＝ダッシュボードでも出せる。脳が考えてない。
- ✅ great例(骨格): 「moversを追うな→[momentum型]は燃料なしで見送り(この型は実績上◯割死)／[narrative型の誰(直近的中率○)]は[この物語]に張る／割れてる所は[X]、この相場なら[こっち]／お前が使う思考の型は[…]」＝**視点＋実績の錨＋なぜそう考えるか（教える）**。

### 0.1 矛盾こそ価値・反echo-chamber・強弱両方・鏡（本人2026-07-02追加・核心）

**echo-chamberは無価値**: 今は最初に登録したKOLしか見てない＝視野狭窄＝一致意見しか集まらない＝**合成する価値がゼロ（矛盾が見つからない）**。**成長は矛盾を見つけてこそ**。だから設計は以下を核に据える:

1. **矛盾＝KPI**: wikiの健康は coverage でなく **surfaced contradictions（意味ある対立を何個表面化し、どの条件で誰が正しいかまで解いたか）**。一致だけ増えるのは劣化。[trench-brain-compounding-meter] の `contradictions_surfaced` を第一級指標に昇格。
2. **反echo-chamber＝ソースを積極拡張**: 登録KOL内に閉じない。**対立する声・別クラスタ・別言語圏を能動的に探して取り込む**（同意を増やすのでなく、矛盾の表面積を最大化する方向に discover を向ける）。多様性が無いと②以降が成立しない。
3. **強者だけでなく弱者もモデル化**: 「良い人の意見」だけ入れない。**弱小/一般トレーダーも第一級の subject**として観測し、**①なぜ強者は強いか ②なぜ弱者は弱いか** を対比で明らかにする（弱さの型が無いと強さは定義できない）。
4. **鏡＝第三者視点の客観評価**: 主観でしか測れない「自分の強さ」を、強弱パターンで**客観的に位置づける**。「自己認識では凄腕でも、filterすると弱小」を機械が突きつける＝主観を第三者視点にする＝ **0→1のoutput**（どのツールも出せない）。
5. **定性＋定量**: 本人の主観insight（例: 「Ansemがトレンドなのに日本の弱者は自分の世界に篭りAnsemを見てすらいない＝その盲点が弱さ」）を、**定性(型の言語化)＋定量(誰がAnsemに言及/行動したか・その後の成績)で裏取り**して矛盾を客観的に引く。主観をwikiの検証可能知識に変える。

この5点は§3(知識モデル)と§4(ループ)の設計制約であり、relay脱却(§5)と並ぶ"great"の必須条件。

---

## 1. 検証済み root（なぜ今ダメか）＝「部品は全部あるが、ループになってない」

4-agent audit + linchpin実測（claude --print --strict-mcp-config は**wikiを読める**＝ask.shはagentic RAG）で確定:

| # | gap | 症状 | 該当 |
|---|---|---|---|
| G1 | queryが合成をcleanに読まずgrep運任せ | 同じ問いで神にもゴミにも | ask.sh(BM25 rag.py未使用・原典§6違反) |
| G2 | 脳が自分のfeedbackを見てない | KOLに触れても実績を知らず喋る | kol_track_records/base_rate/risk_weights が prompt未注入 |
| G3 | KOL信号が壊れてる | kol_standouts=[]→生moverノイズ | launch_stream.py:146(CA文字列一致でticker/物語を拾えない) |
| G4 | 合成が単一パスで自己改訂しない | 48h窓外のconceptが凍結・矛盾データの行き場なし | ingest_worklist §1a / synth_prompt.md固定 |
| G5 | 答え/予測が二度と採点されない | outcome追跡してるのに答えに戻らない | query_log write-only / feedback.mdは人間read-only |
| G6 | concept品質バグ | 論理逆転・壊れリンク・echo-chamber・強気バイアス | manipulation-playbook等 |

**核心**: 良い合成(concept高品質)も outcome採点(kol_track_records)も存在するが、**循環に繋がってない**。人中心の目的に照らすと G2/G3/G5 が致命的（"実績で勝ってる人"を脳が使えてない＝評判で答える＝弱小が間違った頭を借りる）。

---

## 2. 設計原則（不変・どのAIでも守る）

1. **人中心**: 第一級成果物はKOLの mind-model。銘柄は答え合わせの材料。
2. **実績で錨**: "勝者"は評判/フォロワーでなく **track record（検証された成績）** で定義。声のデカさを増幅しない。
3. **query=合成を読む（再導出しない）**: 原典§6。決定的retrieval＋状態注入で、毎回grepしない。
4. **循環を閉じる**: ingest→score→feedback→query→assetize→revise が一周する。outcomeが必ず答えと合成に戻る。
5. **合成は自己改訂する**: 矛盾/予測外れでconcept/mind-modelを再合成・confidence減衰。単一パスにしない。
6. **モデル非依存＝決定的契約で包む**: 各LLM stepは「決定的retrieval＋prompt template＋機械validator＋retry」。弱いモデルでも validator が構造/接地を強制。
7. **relayを禁じ、synthesisを強制**: 回答契約(§5)を機械checkで守らせる。
8. **憲法を守る**: 門付き収集/観測≠推論/矛盾保持/[[wikilink]]/bottom-up/淡々（CLAUDE.md 9指針）。
9. **form非依存＝engineをUI/UX/現仕様に閉じ込めない（本人2026-07-02音声）**: 資産はengine（KOL脳モデル＋複利知識）であって、UI/今の形は"表面(surface)"の1つ。engineとsurfaceを厳密に切り離し、同一engineを chat/dashboard/API/通知/未来の別形 で出せるようにする。今のUI/UXに枠を嵌めない＝「全てに応用/果実は配る」と一致（engineが本体、UIは蛇口の1つ）。回答契約(§5)・決定的契約(§6)は surface非依存に定義する。

---

## 3. 知識モデル（wikiが持つもの・人中心に据え直す）

現状: 615 token entities vs 126 player entities＝**銘柄過多**。重心を人に移す。

### 3.1 KOL mind-model（第一級・`wiki/entities/players/@handle.md`を深化）
seed は既存の「思考の型」ブロック。これを構造化して深める:
```
---
type: entity  kind: player  handle: @x
archetype: forensics|momentum|narrative|contrarian|macro  (主・副)
track_record: {evaluated: N, hit_rate: %, on: [型/銘柄クラス], window: 直近Nd, tier: 実績T1}
confidence: 実績由来の重み(高/中/低)   ← G2で答えに注入
---
## 観測(事実): 実発言・実売買(CA+outcome)・エンゲージ
## 思考モデル(合成):
  - decision_process: どう入り/どう降りるか
  - motivations: なぜその銘柄に動いたか(実例+outcome)
  - tells / biases / epistemic_style
  - reads_market_as: 「相場状態Xならこう読む」(behavioral prediction)
  - ⚠️矛盾: 本人の言と実行動のズレ / 他KOLとの対立
根拠: [[archetype-concept]] [[関連KOL]] [[実銘柄]]
```

### 3.2 archetype / 横断concept（`wiki/concepts/`）
- **勝者の共通マインド**: track record上位だけを母集団に、共有する思考を抽出（評判でなく成績で選別＝G6 echo-chamber対策）。
- **弱者の共通する型（§0.1-3）**: track record下位/一般ユーザーを母集団に、**負けパターン**（篭る・トレンドを見ない・遅い・確証バイアス・型無し）を抽出。強者との**対比**で「なぜ強い/なぜ弱い」を定義。
- **割れる所**: どのKOLが何で対立し、どの相場条件でどっちが正しかったか（矛盾保持・指針5）。矛盾こそ§0.1のKPI。
- **archetype別の読み方**: forensics/momentum/narrative/contrarian/macro が同じ状況をどう weigh するか。
- **KOLへの成長path**: 強者-弱者の差分から「弱小→勝者」の思考/行動の型。

### 3.3b subject拡大（人＝強者∪弱者・反echo-chamber）
`wiki/entities/players/` は登録KOLに閉じない。**弱小/一般トレーダーも第一級subject**（負けの型の観測点）。ソース拡張(§7)が対立する声・別クラスタを能動的に取り込み、矛盾の表面積を最大化する。

### 3.4 鏡output（第三者視点の自己評価・§0.1-4・0→1）
問い「俺は/このトレーダーは強いか弱いか」に対し、強弱パターンでの**客観的位置づけ**を返す新output型: 観測(実発言/実売買/成績) → 強者型/弱者型のどの特徴に一致するか → 「自己認識と第三者評価のズレ」を明示。主観を検証可能知識に変える。回答契約(§5)の判断問いの一種として扱う。

### 3.3 token entity（第二級・答え合わせ材料）
現状維持＋**どのKOLがいつ言及/売買し、outcomeはどうだったか**を必ず記録＝KOL採点の一次データ。

---

## 4. 複利ループ（G1-G5を閉じる・どのAIでも回る）

```
        ┌────────────────────── (収集・門付き) ──────────────────────┐
        │  KOL投稿(X) + pump.fun観測 + on-chain                        │
        └───────────────┬───────────────────────────────────────────┘
                        ▼
 [INGEST] KOL発言→mind-model更新 / 発言中のCA・ticker→そのKOLの"call"として記録(予測)
   └ G3修正: KOL検出を CA文字列一致でなく (a)track.pyのregex CA抽出 (b)ticker→mint解決 で正しく紐付け
                        ▼
 [SCORE] on-chain outcome(生死/mcap)で各callを採点 → kol_track_records更新 → mind-modelのtrack_record/confidenceに反映
   └ G5修正: 採点結果が mind-model と base_rate に必ず戻る(dashboardで止めない)
                        ▼
 [QUERY] 問い→決定的retrieval(BM25 rag.py context())で関連 mind-model/concept を読む
        ＋状態注入(該当KOLのtrack_record・base_rate・risk_weights)＝G1/G2修正
        →回答契約(§5)で synthesis of winning minds を合成→assetize(wiki/queries)
                        ▼
 [REVISE] KOLのcallが外れ続ける/conceptの予測が外れる→再合成・confidence減衰＝G4修正
   └ 48h窓外でも、矛盾データ/予測外れが来たら re-synthesis を trigger
                        │
        └──────────── outcomeが常に上流へ還る（moatフライホイール）─────────┘
```

各stepは§6の決定的契約で実装＝どのモデルでも同じ品質。

---

## 5. 回答契約（"great"を機械で強制する・relay禁止）

ask経路(ask.sh/ask_prompt.md)を、**判断状況の問い**で以下を必須化する。機械validatorで構造を検査し、欠けたら再生成:

| 要素 | 必須 | 機械check（どのAIでも判定可） |
|---|---|---|
| **視点(誰の頭で)** | 判断/状況問いで必須 | archetype名 or KOL[[handle]]が本文に≥1 |
| **実績の錨** | 必須 | 言及KOLに track_record数値 or「実績薄」明示（評判だけで語らせない=G2） |
| **矛盾/割れ** | 該当時 | 対立が存在する時 ⚠️ or 条件分岐が本文に |
| **教える(なぜ)** | 必須 | 結論だけでなく「なぜそう読むか＝思考の型」が本文に |
| **接地(citation)** | 必須 | [[wikilink]] 根拠 ≥1（retrieveした mind-model/concept 由来） |
| **relay検出** | 失格条件 | 本文が「銘柄名+数値の羅列」主体で視点/思考が無い→再生成 |

> 一般知識の問い(用語/歴史)はこの限りでない（既存の分岐を維持）。効かせるのは「判断/状況/成長」の問い。

---

## 6. モデル非依存の実装契約（どのAIでも同品質＝北極星②）

各LLM stepを3層で包む（既存 synth_validate パターンの一般化）:
1. **決定的 retrieval/injection**（LLM前）: rag.py `context(q,k)` で関連ページ＋状態(track_record/base_rate)を**コードで**組み立てて渡す。モデルにgrep探索させない＝弱いモデルでも同じ材料。
2. **prompt template**（`brain/*_prompt.md`）: 役割・手順・出力構造を固定。SYNTH_MODEL/ASK_MODEL 差し替えのみでモデル交換。
3. **機械validator＋retry**（LLM後）: §5契約 と synth_validate（frontmatter/synthesisブロック/失敗マーカー）を検査。不合格→再生成 or loud fail。沈黙failを根絶。

＝「良い答えはモデルの賢さ」でなく「**決定的な材料＋構造強制**」から出す。ローカルLLMでも成立。

---

## 7. 具体修正リスト（現ファイルへの落とし込み）

| gap | 修正 | 対象 |
|---|---|---|
| G1 | ask.shにBM25 retrieval配線（rag.context()を呼びpromptに注入）＋grep依存を減らす | brain/ask.sh, brain/rag.py |
| G2 | 該当KOLの track_record / base_rate / risk_weights を ask prompt に注入 | brain/ask.sh, kol_track_records.json |
| G3 | KOL検出を CA文字列一致→(regex CA抽出＋ticker→mint解決)で正しく紐付け・launch_queueにkol反映 | brain/launch_stream.py:146, track.py:270-308 |
| G4 | 48h窓外でも矛盾/予測外れでconcept・mind-model再合成をtrigger（新stepまたは既存合成の拡張） | ingest_worklist.py, synthesize_x.sh, 新 revise step |
| G5 | 採点結果を mind-model.track_record/confidence と base_rate に書き戻す（dashboard止まりを解消） | feedback.py, kol_track_record.py, build_entities.py |
| G5 | 回答を後から採点（query_logのcall→outcome照合） | asset_queries.py 拡張 or 新 score_answers |
| G6 | 論理逆転/壊れリンク修正＋機械check（claim方向・source独立性） | 該当concept, check_conformance.py |
| 回答 | §5回答契約のvalidator | 新 answer_validate（ask経路） |
| 中心移動 | player mind-model スキーマ(§3.1)へ深化 | build_entities.py, synth_x_prompt.md |
| §0.1-2 | discoverを「矛盾を最大化する方向」に＝対立クラスタ/別言語圏を能動探索・弱者voiceも取り込む | brain/expand_watchlist.py, discover.py |
| §0.1-1 | contradictions_surfaced を第一級健康指標に昇格（compounding meter/conformance） | brain/compounding.py, check_conformance.py |
| §0.1-3/4 | 弱者subject観測＋なぜ強い/弱いconcept＋鏡output | build_entities.py, 新concept, ask経路 |

---

## 8. 段階（安全に・積み上げをリセットしない）

各段は独立に価値を出し、既存を壊さない（憲法の書込みパス分離・門を維持）:
1. **P1 信号を直す(G3)**: KOL検出修正→kol_standouts が実際に埋まる＝relayの原因を根から断つ。
2. **P2 脳に実績を見せる(G1/G2)**: retrieval配線＋track_record注入＋§5回答契約＝great が安定して出る。
3. **P3 人中心の合成(G4一部/中心移動)**: player mind-model深化＋archetype concept。
4. **P4 ループを閉じる(G5)**: outcome→mind-model/答え への還流＋回答採点。
5. **P5 自己改訂(G4)**: 矛盾/外れでの再合成＋confidence減衰。
6. 各段: 敵対的自己批判→機械validator→検証してからcommit（原則2/4）。

---

## 9. 完璧の担保（このドキュメント自身を疑う）

- 各段実装後に**独立agentで敵対反証**（「これはまだrelayか / モデル非依存が崩れる所 / 複利しない所」）。
- 回答は**relay/great の acceptance test**（§0基準）を実データで通す＝主観でなく機械+実問いで判定。
- 「部品はあるがループしてない」を再発させない＝§4ループが一周する事を機械で確認（outcomeがmind-modelに戻ってるか）。

> この設計は「どのAIでも実現できる構成」を意図する。実装は本文の契約(§5/§6)に従えばモデルを問わない。
