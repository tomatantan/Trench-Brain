# Log — 操作履歴

ingest / query / lint の記録（新しい順）。

- 2026-06-22 brain: 仕分け層(brain/digest.py)＋合成デモ。5,086生ツイ→信号4,354に集計([[signal]])、そこからconcept5枚を合成(型: 外部イベント→token / 動線: SpaceX IPO→$SPCX・$ASTEROID / $ASTEROID / $SPCX / $CLUTCH)を相互リンク。LLM Wikiの脳が初稼働。

- 2026-06-22 collect: Senshi(@SenshiNeo7)のフォローからCAVEサークル＋日本trench層を取り込み(watchlist v4, ③方針=crypto＋外部要因, 66アカ追加, +1270ノート)。

- 2026-06-22 collect: 初回backfill完了。3,796ノート/55アカ取得(watchlist 58中)。syndication(無料)で大半＋twitterapi.io(有償)で残り＆詰まり分をクリーン回収。0xMert_/aeyakovenko/TusharJain_の3アカはAPI上0件(ハンドル変更/保護疑い、要確認)。collectorはsyndication/twitterapi両対応。

- 2026-06-22 build: collector v1 実装（syndication無料取得→sources/x/に生ツイ保存、$ticker/@mention自動抽出、ファイル存在で重複判定）。3アカ実走で形式確認(12ノート)。GitHub Actions(毎時)＋ローカルcron手順、graphからsources除外。

- 2026-06-22 config: watchlist v2 へ拡張（VC/Podcast/オンチェーン/マクロ層を追加、計約40アカをfxtwitterで実在確認）。収集方式は「自動かつ無料」で確定。
- 2026-06-21 init: Trench-Brain スキャフォールド作成。
