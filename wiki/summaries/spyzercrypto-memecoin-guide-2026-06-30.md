---
type: summary
title: spyzercrypto「A Complete Meme Coin Guide」(132p・強KOLの実戦framework)
source: https://medium.com/@spyzercrypto/a-complete-meme-coin-guide-8d1c6ffac7c0
created: 2026-06-30
updated: 2026-06-30
tags: [trench, summary, kol, framework, rug, screening, onchain, psychology, spyzercrypto]
---

# spyzercrypto「A Complete Meme Coin Guide」要約

**強KOL** [[@spyzercrypto]] の132ページ無料ガイド（PDF・英/中）。著者は2019年に€2kスタート・anti-guru（「guru course seller が嫌い」）。
★**世界最強級KOL [[@ansem]](blknoiz06)が"最強手法"として紹介**＝「強KOLの意見」→**トップKOL Ansem 公認の標準framework**に格上げ（本人確認2026-07-01）。
ただし framework は採用しても**検証層は置き換えない**＝Ansem公認は prior を上げるが heuristicsが効くのは on-chain で検算できるから（[[ape-or-avoid]] の芯＝「語られてる≠良い」。奇しくもガイド自身が同じことを言う＝§KOL「don't borrow conviction」）。権威×検証の両方。

構成: PART I Foundation / II Trading / III Psychology / IV Safety / V Getting Started。

## §Scam/Rug 判定（gold・[[rug-anatomy]] / [[onchain-verification]] に直結）
- **LP Locked 必須**: 作成者がLPのアクセス鍵を burn していないと SOL 全抜き可能。
- **Mint Authority Disabled 必須**: 有効だと増刷→LPに売り→SOL枯渇。
- ★**非LP top holder は 3.5% 超えたら赤旗**（trenching の目安）。1wallet の100%売りで板が急落。
  **注意: top holder一覧の最上位はほぼ LP＝trader でない**（除外して測れ）。
- **Bundle 検出**（最重要・「99%のon-chainトレーダーはbundleで負ける」）:
  - Bubblemaps: wallet cluster（作成時刻/同一CEX資金元/相互送金で同一人物判定）。full bundle＝1人が50-80%支配。
  - Holding %（速い代替）: 上記3.5%ルール。
  - bundler は floor を作り、いつでも crash 可能。「farm」＝徐々に売って chart を活きて見せる。
- **Fresh Wallet アイコン**（緑の葉＝新規wallet）＝大きな赤旗、特に New Pairs。複数あれば回避。
- **Botted chart**: 同サイズ連続candle / 巨大candleのみ＝供給需要の法則で起きない＝bot。
- **Honeypot**: 美しい up-only chart ＋（LP未lock or mint/freeze未無効 or bundle）。
- **VOL/MC 比** で異常検知。「up-only × 低volume × 少holder ＝3赤旗」。
- rugcheck.xyz で LP-lock/mint-auth/リスクを確認。

## §Find Good Trades
- **情報網（group chat）＝information asymmetry のedge**。20人が篩→良い1本を共有→自分でDYOR。dev の rug 履歴/X垢hack を他人の情報で回避した実話。
- **独立思考**: 「followerは必ずパーティに遅れて来る」。call channel/copy-trade でなく**自分のthesis**。crypto外を読め（円キャリー→cryptoのdump時間、luxuryの人工希少性→memeのplaybook）。

## §KOL / Trust（[[@spyzercrypto]] 自身の主張・本ブレインと完全一致）
- ★**「follower数は実力をほぼ何も語らない。track record が語る」**＝[[kol-track-records]] / KOL-CA思想そのもの。
- follower獲得は 1)lottery-ticket（1発当てて自慢）2)bot engagement でも起きる＝多follower≠上手い。
- ★**「don't borrow conviction（借り物の確信で張るな）」**＝KOLが公開で確信を示す頃には手遅れ（followerは遅れて来る）。
- 良KOLの見分け: なぜ良いか paragraph で書く/良い悪い両方 update/外れたら正直/一貫winrate。悪KOL: nuke後に投稿削除→block。

## §Charts / Execution / Psychology
- market structure（support break→downtrend / lower-low→lower-high→base）。「early である必要はない・"ok to buy" を待て」。
- 0.618（golden ratio）fib。
- ★**利確ルール**: 「lifechanging な額まで上がったら利確。lifechanging でなくても**段階的に利確**」。
- FOMO/patience/独立の確信。

## §Safety
- seed phrase は絶対オンラインに置かない/共有しない（紙/金属）。rugcheck 常用。

## ⚠️矛盾/バイアス（迎合しない・正直に）
- **referral収益バイアス**: 取引プラットフォーム「fomo」を推奨し **referral link (fomo.family/r/spyzer) で稼ぐ**と明言。platform推奨は割り引いて読む。
- 3.5%閾値は**文脈依存**: launch直後は集中が常態＝graduated/成熟とは別基準。数字は目安。
- 1トレーダーのframework＝強KOLでも**検証層は残す**（[[ape-or-avoid]] / [[onchain-verification]] で裏取り）。

## ★本ブレインへの含意（source→edge のループを閉じた）
- **`/api/score` を実際に sharpen 済（commit d250d6b・2026-06-30）**: このガイドの ①**LP除外** ②**非LP top holder 3.5%階層閾値** ③insider holder数 を反映。
  例: VaelaQueen 旧"top58%集中"(実はLP誤読) → 新"非LP top 4.79%"(本物) を3.5%基準で拾う。
- 追加候補（未実装）: fresh-wallet検出 / bundle(Bubblemaps cluster) / botted-chart / VOL-MC比。
- KOL-trust framework は [[kol-track-records]] の「follower≠実力・track recordで測る」を**外部強KOLが裏付け**。

関連: [[rug-anatomy]] [[onchain-verification]] [[ape-or-avoid]] [[manipulation-playbook]] [[@spyzercrypto]] [[kol-track-records]]
