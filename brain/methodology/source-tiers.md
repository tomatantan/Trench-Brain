# ソース/証拠 5段階ティア（trench版）— 証拠の信頼度を格付けする

出典: makeai_ceo記事のティアシステム ＋ **本人拡張(2026-06-23)「tier系はトークン取る時もできる」**。
＝ソース評価だけでなく、**トークンの証拠も格付け**する。観測≠推論(指針6)の数値化。
「ゴミを入れたらゴミが出る」→ 答え/判断に必ず「これはtier何の証拠か」を明示する。

## ティア定義（trench）
| tier | 内容 | trench での例 | 使い方 |
|---|---|---|---|
| **T1 最高** | 一次・改ざん不能データ | **on-chain**: RugCheck(authority/LP/holders/insider)・mint事実・実取引・mcap・base_rate・死亡/跳躍台帳の実数 | ほぼそのまま使う。結論の土台 |
| **T2** | 専門家の分析 | 実績ある分析者の検証可能な解析([[@lookonchain]]のwallet追跡・[[@badattrading_]]のbundle解析) | 因果/解釈の主張に |
| **T3** | informed commentary | watchlist KOL の言及・見解(資金源/ポジ要確認) | 仮説生成・narrative検知 |
| **T4** | 一般メディア | ニュース・まとめ | 初期オリエンテーション |
| **T5** | SNS/hype/体験談 | reply数・"バズってる"・無名の煽り | **シグナル検知のみ**。"多数が言う=事実"ではない |

## レッドフラグ（証拠の信頼度を1段下げる）
- 引用元/CAが不明 ・ 発信者が結論に金銭利害(自分がdump済で強気＝逆シグナル[[onchain-verification]])
- 都合の良い期間/データだけ切り取り ・ 相関と因果の混同 ・ association marketing(Elon等を勝手に紐付け＝$RO型)

## ★トークン評価への適用（本人拡張）
あるトークンを語る/採用する時、証拠を tier で分ける:
- **T1(on-chain)だけ強くてT3(KOL)が無い** → 「出来高はあるがnarrative燃料ゼロ＝死亡台帳の型」(traction無し噴き)
- **T5(hype)だけでT1裏付け無し** → 「⚠️ hypeのみ・on-chain未確認＝つり上げ/bot疑い」([[rug-anatomy]])
- **T1(安全)×T3(複数KOL)×narrative有機** → survivor候補([[survivor-memes]])＝採用門(指針2 traction+KOL)を満たす
＝**採用(合成/個別page化)は T3以上のsignalが要る**。T5だけは観測どまり(死の分母)。

> 答え/合成には必ず tier ラベルを：「これはT1 on-chain／これはT3 KOL主張(未T1裏付け)」。断定を tier で律する。
