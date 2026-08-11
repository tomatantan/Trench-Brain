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
