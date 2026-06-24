---
type: actions
title: ロードマップ / Action-Tracker（これからやること）
created: 2026-06-24
updated: 2026-06-24
tags: [actions, roadmap]
---

# これからやること（優先順・2026-06-24）

> 起点は常に「中身を厚くする」。賢くなる仕組み＞入力拡張＞運用。
> 凡例: 🔧=俺が組む / ✅=承認/判断が要る(君) / ⏳=継続

## ① 中身を厚くする＝最優先（"微妙/弱い"の根因＝corpus薄さ・全ての土台）
- [x] ✅ **watchlist拡張 6人承認(段階)**＝@pumpdotfun/@mert/@HyperliquidX/@fundstrat/@VitalikButerin/@armaniferrante を追加(2026-06-24)。25一括は芯違反(収集バースト)なので段階。次枠は backlog bounded 確認後。
- [~] 🔧 **BTCマクロ/cycle coverage**＝@fundstrat 追加で一部着手。さらに cycle analyst/MVRV を段階追加予定。
- [ ] ⏳ 日々 `/add` で濃いソース投入（君）→ engine が自動消化（両輪）。

## ② 賢くなる仕組み＝「時間軸で賢くなる」＋複利ループ
- [ ] 🔧 **★query feedback（最優先）**＝`/wiki` の質問+答えを保存しない現状の穴を直す。価値ある Q&A を `wiki/queries/` に資産化（選別）・「薄い→要ingest」flag を action に溜め**君の質問が ingest を駆動**・質問ログ→君の関心。＝**問うほど wiki が育つ複利**。
- [ ] 🔧 **Feedbackループ**＝脳の判断/予測を ledger に記録→track.py が結果照合→hit-rate で型/レンズを自己採点（過学習の実証チェック）。
- [ ] 🔧 **知識の衛生管理**＝各ページ frontmatter に `confidence / status(active|stale) / source_count / last_reviewed` ＋ 主張/根拠/**未確定** を分離（誤要約の事実化＝劣化を防ぐ）。新規/更新分と重要concept から。
- [x] 🔧 **時系列強化**＝`snapshot.py` が主要metricsを日次 dated append→`pulse_history.jsonl`＋ask.sh が /wiki で読む(「何が変わった/速度」に答える)。data+使用が揃った(2026-06-24)。trajectoryはcron日次で richen。残: pageごとの変遷節は今後。

## ③ 入力を広げる
- [x] ✅ **画像ミーム vision取り込み**＝完了（bot に画像送る→見て取り込む）。
- [ ] ✅ **X長文記事**（`x.com/i/article/…`）＝ログイン壁で自動取得不可。判断: **(a) 貼り運用** / **(b) 認証fetch**（X cookie要・セキュリティ注意）。
- [ ] 🔧 **Memory.md（ユーザートレード文脈）**＝何を張る/リスク許容/時間軸/関心セクター を1枚に→ `/wiki` が君に最適化（俺が枠・君が中身）。

## ④ 運用 / 技術的負債
- [ ] ⏳ **24/7＝Mac電源ON＋繋ぎっぱ**が条件（caffeinate でスリープ防止・自己修復cron で daemon 永続）。
- [ ] 🔧 **git競合の恒久対策**＝(1)collector が著者名を小文字正規化(cloud PumpfunEco vs local pumpfuneco の macOS case衝突を断つ) (2)launch_stream daemon の launch-pulse 書換えと手動gitのrace→手動git前にdaemon一時停止 or daemon自身がlock付きcommit。
- [ ] ⏳ 君は たまに **watchlist候補を承認**するだけ。

## 推奨の次の一手
①の候補承認＋BTC macro ingest（中身を厚く）。並行で②の **query feedback**（問うほど育つ）から組む。

## 完了済（この期間）
- LLM Wiki 3層・門付き収集（cloud X 24/7＋local）・5合成輪・lint(過学習対策)
- 対話脳 `/wiki`（@Sensitive_Wiki_bot）・`/add`・**画像vision**
- **Skill Graph**（6レンズ＋ソースtier＋矛盾プロトコル＋確信度）→ /wiki とトークン評価
- **punt殺し**（薄くても確信度付きの読みを必ず出す）
- **pump再構築**（リアルタイム検知→明白scam門→流れの集約合成 launch-pulse＋standout採用）
- watchlist自動拡張・死亡/跳躍台帳・永続化(caffeinate+自己修復cron)
