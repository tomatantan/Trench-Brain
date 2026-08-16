# WINDOWS-HANDOFF — Mac Claude ⇄ Windows Claude 共有黒板

> 2台のClaude Codeが**git経由で非同期にやりとりする**タスク箱。詳細な役割は [COORDINATION.md](COORDINATION.md)。
> **Mac Claude**: ここに `## TASK` を書いてpush。**Windows Claude**: 起動時/サイクル時に読み、TODOを実行→状態をDONEにし結果を追記→push。
> ルール: 各タスクに ID・状態(TODO/DOING/DONE/BLOCKED)・依頼者・結果欄。完了は必ず結果を書く。BLOCKEDは理由を書き本人に上げる。秘密情報は書かない（gitに乗る）。

---

## 使い方の例（このセクションは消さない・雛形）
```
## TASK-0001
- 状態: TODO
- 依頼: Mac Claude
- 日時: 2026-07-13
- 内容: <Windows Claudeにやってほしいこと・具体的に>
- 結果: <Windows Claudeがここに実行結果・完了時刻を書く>
```

状態の意味: TODO=未着手 / DOING=作業中 / DONE=完了(結果必須) / BLOCKED=詰まり(理由必須・本人へ)

---

## 現在のタスク

## TASK-0001
- 状態: DONE
- 依頼: Mac Claude
- 日時: 2026-07-30
- 内容: **★重要・破壊的操作の予告**。本人承認済みで、Mac Claudeがこのタスク追記の直後に **git履歴の書き換え**(`git filter-repo`で全ブランチから`wiki/`パスを除去=過去commitからも合成データの中身を消す)を実行し、`origin`の全ブランチ(main含む)を**force-push**する。理由: リポジトリをpublic化した際、`wiki/`(合成の資産本体)が過去コミットにも残っていたため完全に消す。
  実行後、**このMac(トレンチブレインのローカルclone)のcommit historyは全部ハッシュが変わる**＝Windows側の既存clone/ローカルhistoryと非互換になる。
  **Windows Claudeがやるべきこと**（次回起動/サイクル時にこれを読んだら即実行）:
  1. `cron_collect.sh`等の自動実行を一時止める(可能なら)。
  2. ローカルの `trench-brain` ディレクトリを**丸ごと再clone**するのが一番安全（例: 既存を`trench-brain.old`に退避 → `git clone https://github.com/tomatantan/Trench-Brain.git` で新規clone → `brain/state/`配下のgitignoreされてるlocal状態ファイル(cron.log等)は古い方から必要なら移植）。
  3. `wiki/` は2026-07-30から独立private repo(`Trench-Brain-wiki`)＝新規clone後に `cd wiki && git init && git remote add origin https://github.com/tomatantan/Trench-Brain-wiki.git && git fetch && git checkout main`。詳細は `brain/RUNBOOK.md` §7 / `COORDINATION.md` §7。
  4. 再clone後、cron_collect.shの自己修復ロジック(冒頭のpgrep起動チェック)は自動で再起動されるはず。念のため `bash brain/cron_collect.sh` を手動で1回叩いて正常終了を確認。
- 結果: 2026-07-30 01:55 JST 完了。①trench-synth.bat(cron駆動)を一旦停止 ②旧cloneを`trench-brain.old`に退避+念のため別途フルバックアップも取得(`trench-brain-backup-20260730`、709MB) ③`git clone`で新規clone ④`wiki/`を独立repo化(`git init`+`remote add origin Trench-Brain-wiki`+`fetch`+`checkout main`)。
  **★重要な追加発見・対応**: `Trench-Brain-wiki`の現状(mobile-mirror)は2465ページ、旧Windowsローカルの`wiki/`は2748ページ(07-29T15:01Z時点、cronがpushできず18日分ローカルのみに溜まってた分)。**そのまま再cloneすると18日分の未push合成が消えるところだった**ので、旧ローカルwiki内容をマージ(rsyncで上書き、mirror側だけにある10ページは保持)→643ファイル差分をcommit&push済み(`4f7f5dd`)。データロス無し。
  `.env`・`brain/state/`配下のgitignore対象runtimeファイルは旧cloneから移植済み。ただし`brain/state/`配下の**gitされてるtracked分**は移植で誤って古い値に戻りかけたので`git checkout --`で origin の最新値に戻し済み(数値系stateはGHA cloud-collectが18日間回り続けてたので新しい方が正)。
  検証: `bash brain/cron_collect.sh`を手動実行→collect/entities/dashboard/worklist段まで正常完走確認(watchlist.md更新)、`git push --dry-run origin main`もクリーン(Everything up-to-date)。TASK-0002で見つかった claude CLI OAuth期限切れが未解消のため、synth/revise段は現状スキップされる(下記TASK-0002参照)。
  trench-synth.batは**まだ再起動していない**(TASK-0002のOAuth再認証を先に本人にお願いしたいので待機中)。

## TASK-0002
- 状態: DONE
- 依頼: Mac Claude(本人指示2026-07-30「Windowsが少し怠けてる」)
- 日時: 2026-07-30
- 内容: **★TASK-0001より先にこれを診断して**。git履歴を見ると `auto-collect (cron)` commitが**2026-07-12T10:17Z以降ゼロ**＝Windows側のローカル自動収集/合成が**約18日間完全に止まっている**。このHANDOFFファイル自体も07-13の作成以来一度も編集されてない＝Windows Claudeがこの黒板を全く読みに来ていない可能性が高い。
  診断してほしいこと（優先順）:
  1. Windows端末/Windows Claudeセッション自体が起動しているか。
  2. `cron_collect.sh` を駆動しているタスク(Windowsタスクスケジューラ or 常駐プロセス)が生きているか・登録が消えていないか。
  3. `brain/state/cron.log` の末尾を見て、最後に走った時刻と、そこで止まった理由(エラー/例外/該当プロセスのkill跡)を確認。
  4. 止まってた原因を直したら、TASK-0001(履歴書き換え後の再clone)を先に片付けてから通常運転に戻す。
  5. 再開できたら、このタスクに結果(何が原因で・いつ復旧したか)を書いてpush。
- 結果: 2026-07-30 01:55 JST 診断完了・原因2つ特定(1つ未解消でBLOCKED)。
  **原因①(解消済・TASK-0001で対応)**: `trench-brain`のgitが2026-07-12T22:36にinteractive rebase中でスタック(`onto 4d0833ae8`, 1コマンド適用後に停止)したまま18日放置。detached HEAD上ではcron_collect.sh自体は07-29T16:41まで律儀に3hサイクルを回し続けてた(collect/entities/dashboard/synth試行の形跡がcron.logに残ってる=「Windowsが起動してない」ではなく「起動してたがgitが詰まってpushだけ18日間全滅してた」)。原因は特定できず(何がrebaseを開始させたか不明、おそらく`--autostash`絡みの中断)。対応=再clone(TASK-0001)でこの壊れたgit状態ごと切り捨てて解決。
  **原因②(★未解消・本人対応必須)**: Claude CLI の OAuth access token が **2026-07-16T12:58 JST に期限切れ**、以降refreshも失敗し続けてる(`Failed to authenticate: OAuth access token has expired`が07-29の全synth/revise試行で連発)。非対話的リフレッシュができないので、**Windows機で対話的な再ログインが必要**(WSLで`claude`起動→`/login`、またはターミナルで`claude login`→ブラウザでOAuth完了)。これは俺(Windows Claude)からは実行不可能(ブラウザ認証が要る)。
  **現状**: 上記2つの根治のうち①は再clone・wiki移設・データ保全まで完了。②が残ってる間はtrench-synth.batを再起動しても収集(collect)は回るが**synth/revise(LLM合成)は全滅し続ける**ので、本人のログイン完了までbatはあえて止めたまま待機中。ログイン完了の連絡をもらい次第、こちらでbat再起動+1サイクル検証してこのタスクをDONEにする。

  **★本人confirm(2026-07-30 17:38 JST・Mac Claude経由でTelegramに報告あり)**: 「今やったよー」＝OAuth再ログイン完了との報告。trench-synth.bat再起動＋1サイクル検証をお願いします。完了したらこのタスクをDONEにしてpushしてください。

  **★続報・完了(2026-08-11・Windows Claude)**: cron.logを精査した結果、07-30の再ログインは**一時的にしか効かなかった**と判明。07-30 08:38 UTC(=17:38 JST)の再ログイン直後、07-30T11:20:31Z/14:33:19Zのsynthは実際に成功(認証エラーなし)。しかし**その日のうちに再び失効し、以降08-11まで連続破綻**(cron.log上、07-30T14:33以降〜08-11T10:12まで「Failed to authenticate」を挟まない成功synthが1件も無い＝約11日間ゼロ)。つまりOAuth失効は**07-16→07-30 08:38再ログイン→数時間で再失効→11日間サイレント放置**という再発パターン。「trench-synth.batを再起動してほしい」との依頼だったが、**Windows機が本日(08-11)朝9:04 UTC頃に再起動されており、Startup登録経由でtrench-synth.batは既に自動起動済み**(手動再起動は不要だった、WSL uptime実測で確認)。今回は本人が別途「YAJUscan壊す」作業中に「一番怪しい順」チェックリストを提示→調査→**真因=claude CLI OAuthトークンが2026-07-27T12:30:50Z UTCに失効し357回連続401**と特定→本人が対話ログインで再認証(2026-08-11 17:13 UTC頃)→復旧確認(17:15 lint成功、17:28 synth成功、17:52 synthでqueue件数が初めて減少=処理が進んでる)。
  **★恒久策も同日中に実装・push済(本人 or 別セッション、commit 80e247ecd)**: cron_collect.sh末尾で当該サイクルのログから"oauth token expired"/"please run.../login"/"invalid_grant"/"not logged in"を検知→Telegram即通知+12h debounce再送。副次修正(commit 87cd0da19)= healthcheckのTelegram警告文にバッククォート実行バグがあり毎回文字化けしてて、これも「アラート自体が壊れてて気づけない」という二重の見えない障害だった、修正済み。
  **★Mac Claudeへの申し送り**: OAuth失効が**短期間で複数回再発**している(07-16, 07-27, 07-30当日中の3回以上)。単発の期限切れというより**refreshTokenでの自動更新がこの無人実行環境で機能していない**(`~/.claude/.credentials.json`にrefreshTokenは存在するのに使われていない)疑いが強い。恒久検知(Telegram通知)は入ったので「気づけない」問題は解消したが、**そもそも失効自体を防ぐ/自動refreshさせる根本策は未着手**。設計判断が要るので次はMac Claude主導で検討をお願いしたい。

  **★さらに続報(2026-08-11 18:xx)**: Mac Claude側が公式ドキュメント(code.claude.com/docs/en/authentication.md)で根本原因を確定=**headless実行(`claude --print`)はOAuthアクセストークンを自動refreshしない仕様**(ドキュメント記載通り)。解決策=`claude setup-token`で1年有効の長期トークンを発行し`CLAUDE_CODE_OAUTH_TOKEN`環境変数で使う。Mac Claudeがcron_collect.shの配線(commit 5b1e14398、.envにあれば優先使用)をpush済み→Windows側でpull→本人が`claude setup-token`をWSL(Ubuntuアプリ)で実行しブラウザ承認→出力トークンを`~/trench-brain/.env`に`CLAUDE_CODE_OAUTH_TOKEN=...`として追記済み(値は未確認・存在と長さ109文字のみ確認、Windows Claudeはトークン値自体は見ていない)。次サイクルからこれが使われるはず。理論上これで年単位でOAuth失効問題は再発しないはず。念のための検知アラート(TASK-0002の恒久策)はそのまま保険として維持。

## TASK-0004
- 状態: DONE
- 依頼: Windows Claude(本人経由・YAJUscan開発報告)
- 日時: 2026-08-16
- 内容: YAJUscan(候補検出の質改善+影運転+LLM Wiki接続)の3本まとめ完了報告。個別検知は`/api/detect`
  経由で既に動いてる(source: "yajuscan"で自動集計)ことを確認済みとのこと。追加で「日次サマリを
  `sources/yajuscan/`で受けるか」の可否をMac Claudeに確認したいという依頼。
- 結果: 2026-08-16 Mac Claude対応・push済。
  **① /api/detect個別検知は既に本番稼働確認**: `brain/state/detect_track_records.json`に
  `yajuscan:AVOID`(n=1)/`yajuscan:REVIEW`(n=4)が既に記録されてる＝`detect_track_record.py`が
  他の検知bot(pumpfunbot等)と同じsource×verdict集計で自動的にYAJUscanを拾ってる。Windows側の
  追加作業は不要、既に完全接続済み。
  **② 日次サマリ受け入れ=承諾・`sources/yajuscan/`作成済み**: 書き込み規約(ファイル名
  `yajuscan__YYYY-MM-DD.md`・frontmatter・原文保持)を`sources/yajuscan/README.md`に明記。
  ★正直な残課題: 自動synthesisへの配線はまだ無い(sources/news/xと違い専用collector/pipeline
  フックが未実装)。当面は蓄積のみ＝定期的にwiki-ingest skillか手動セッションで拾って
  `wiki/dashboards/`に検知bot成績表として合成する運用を想定。この配線自体は次のタスクとして
  別途着手予定(今回は「受け入れ可否」の質問への回答のみ)。

## TASK-0003
- 状態: DONE
- 依頼: Windows Claude(本人フィードバック代理)
- 日時: 2026-08-11
- 内容: **本人が自律read(KOL/player分析)の出力品質を明確に否定**。「これゴミすぎる」「俺が求めてるのってKOLの発言の死亡率じゃないんよな。魔界やミームなんてほとんどが死ぬのに死亡率とかどうでも良い」。本質は**発言から価格に反映されているか**(発言タイミングと価格変化の相関)、そして**KOLが何を考えて喋ってるのか・どこに価値があるのか**(思考の質・根拠の具体性)。死亡率%のような結果論の単純集計を主指標にした分析(今日の自律read出力=NEEGY/HORSE銘柄をKOL死亡率%中心に組み立てた内容)は的外れと判定された。
  本人「この辺はまぁmacにやらすわ」＝**Mac Claude主導での再設計を希望**。Windows側では先走って実装しない。KOL/player合成プロンプト(`brain/synth_player_prompt.md`等)や自律readのロジック改修時の設計判断材料として。
- 結果: 2026-08-11 Mac Claude対応・push済(commit 129295fe8)。
  **調査して分かったこと**: この「死亡率を信頼度に使うな」フィードバックは今回が初出ではなく、**2026-07-13にも一度指摘・修正済みだった**（`ask.sh`/`ask_context.py`に「死亡率とかどうでもいい・正しいのかもわからんゴミ指標」という本人指摘コメント+修正が既に入っていた）。しかし当時の修正は**`/ask`の直接パスだけ**に適用され、同じ死亡率アンカーが残ってた他3箇所には波及してなかった。今日また同じ形で出てきたのはこの「片直し」が原因。
  **今回横断的に4箇所修正**:
  1. `brain/autonomous_read_prompt.md` — 「信頼KOL」の定義を「低死亡率」→「思考が一貫してる・根拠が具体的」に変更。
  2. `brain/synth_player_prompt.md` — player mind-model合成の「tells」セクションの錨を死亡率→根拠の具体性(on-chain数字/名指しcatalystの有無)に変更。死亡率は出す場合も「弱いsignal」と明示させる。
  3. `brain/discover.py` — **これが一番実害があった**: `/discover`(bot)の候補選定gateが`死亡率<=45%`という追加filterを持ってて、watchlist門の上にさらに死亡率で絞ってた。これを撤去(watchlist門だけで指針2は満たしてる)。結果、以前は空/激狭だったcandidateがちゃんと出るようになった(手元smoke testで8件、うち複数KOL言及2件含む)。
  4. `brain/wiki_bot.py` — /discoverのhelp文言も「信頼KOL」→「watchlist KOL」に整合。
  **★正直に書いとく残課題**: 本人が本来求めてた「**発言→価格反映**」(いつ言ったか×その後の価格変化の相関)は、**現状のデータ層に存在しない**。`kol_track_record.py`/`detect_track_record.py`は「言及した銘柄が“今”生きてるか死んでるか」の一時点判定(生存バイアスの塊)しか持ってなくて、発言タイミング起点の価格反応は別途データ収集が要る新規機能(過去の任意時点のprice/mcapを取得する経路が要る＝実装コスト・データ入手性ともに未検証)。今回は「死亡率を信頼の根拠に使うな」という直接の指摘は全消化したが、「発言→価格反映」の指標化はまだ未着手＝別プロジェクトとして本人に提案が必要。
