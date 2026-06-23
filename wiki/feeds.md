---
type: config
title: 動画/podcast feeds（YouTube transcript の門）
created: 2026-06-23
updated: 2026-06-23
tags: [trench, feeds, watchlist, ingest, youtube, podcast]
---

# 動画/podcast feeds（YouTube transcript 収集の"門"）

[[index]] / 長文ソース(transcript)収集の入口。**これが門**＝ここに載るチャンネルの新規動画"だけ"を取り込む（CLAUDE.md 憲法 指針2／原典 docs/LLM-WIKI.md §6「人がソースをcurate」）。
crypto podcast の大半は YouTube にも上がる＝**YouTube collector で podcast も大半カバー**（音声onlyのみ別途whisper要・保留）。
収集＝`collector/collect_youtube.py`（RSSで動画発見＋youtube-transcript-apiで字幕）。合成＝`brain/synthesize_longform.sh` が新規transcriptを N本/サイクルで deep 合成。

**芯（volume制御）**: transcriptは長い＝合成を追い越しやすい。**1チャンネル少数/回＋合成 N/サイクル**で signal_backlog を見ながら段階導入（[[CORE-CHECK|芯チェック]]）。無差別禁止。
**採用基準**: 長尺で trench思想/KOL/VC theses を継続発信。多くは [[watchlist]] と重複(同じKOLの長文版＝既存 entity/concept を深める)。**curate は人間**（本人承認）。

## 取り込み対象（active＝collector が巡回）
- [[@Bankless]]（UCAl9Ld79qaZxp9JzEOwd3aA）✅ transcript取得実証済(2026-06-23)

## 候補（本人 curate 待ち＝承認したら上へ）
- @TheRollupCo / @Lightspeedpodhq / @theempirepod / @uponlytv / @blockworks_（既に [[watchlist]] にXあり＝長文版）
- @RealVisionFinance / @ThinkingCryptoYT / @CoinBureau（解説系・signal濃淡を見て）
- ※ 音声only podcast(YouTube無し)は whisper 要＝現環境未対応、保留。YouTubeにある番組を優先。

> 入れたいチャンネルがあれば言ってくれれば「取り込み対象」に上げて回す。無差別には増やさない（門）。
