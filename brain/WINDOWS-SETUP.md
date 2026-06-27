# Trench-Brain を Windows(WSL2)で常時稼働させる — コピペ用手順

> 目的: 合成の脳を **Mac非依存** にする。Windows を常時ONの合成ホストにする。
> 実行は **お前の Claude サブスク** で動く＝**API従量課金ゼロ**(Macと同じ)。
> 役割分担: **cloud GHA = 収集の腕 / Windows = 合成の脳 / Mac = 解放**。
>
> ★この .md を **Windows の Claude Code に丸ごと貼る** か、ターミナルで手で追ってよい。

---

## ⚠️ 絶対に守る制約(壊さないため)

1. **合成ループ(cron_collect.sh)は1台でだけ回す**。Mac と Windows の両方で回すと
   同じ `wiki/` を別commitで push して **git衝突** する。→ 最後の手順で **Mac側を止める**。
2. **Telegram bot(wiki_bot.py)も1インスタンスだけ**。同じ bot token で2台がpollingすると
   getUpdates が 1token=1poller 仕様で**切断し合う**(既知の実害)。→ この MVP では bot/stream は
   Windowsで起こさない(後述の通り self-heal 行をOFF)。当面 bot は Mac に残す or 後でWindows移管。
3. **公開 `trench-brain` だけ触る**。私的 `brain` repo(Obsidian同期)は**一切触らない**。
4. **secrets は本人が Mac の `.env` からコピペ**(`TWITTERAPI_KEY`, `TG_WIKI_BOT_TOKEN`)。
   このファイルには値を書いてない＝鍵は本人が運ぶ。

---

## 手順

### 1. WSL2 + Ubuntu を入れる(PowerShell を管理者で)
```powershell
wsl --install -d Ubuntu
```
→ 再起動 → Ubuntu の初回起動で username/password を作る。

### 2. 依存を入れる(Ubuntu の中で)
```bash
sudo apt update && sudo apt install -y git python3 python3-pip curl
```

### 3. Claude Code を入れて **サブスクでログイン**(これが"タダ"の肝)
Mac で使ってるのと同じ `claude` CLI を入れる。公式インストーラ、または Node があれば:
```bash
# 入れる(どちらか):
npm install -g @anthropic-ai/claude-code   # Node がある場合
# または公式インストーラ(Macで入れたのと同じ方法)。
claude --version                            # 2.1.x が出ればOK(Macと同系)
# ★サブスクでログイン: `claude` を起動して中で `/login` → ブラウザでお前のアカウント認証
#   (Macと同じ。API key ではなくサブスクログイン。コマンド名が違ったら `claude --help` で確認)
```
※`ANTHROPIC_API_KEY` は **絶対に設定しない**(設定すると従量課金になる)。サブスクログインだけ。

### 4. clone して .env を作る
```bash
git clone https://github.com/tomatantan/trench-brain.git ~/trench-brain
cd ~/trench-brain
# Mac の ~/trench-brain/.env から下の2行の値をコピペして作る:
#   TWITTERAPI_KEY=...
#   TG_WIKI_BOT_TOKEN=...
nano .env
```

### 5. cron_collect.sh を WSL 用に微修正(macOS専用部分をOFF)
`brain/cron_collect.sh` の **19〜21行目**(caffeinate / bot / launch_stream の self-heal)を
コメントアウトする。理由: caffeinate は macOS 専用、bot/stream は制約2で当面Windowsで起こさない。
```bash
sed -i '19,21 s/^/# WSL-disabled: /' brain/cron_collect.sh
# 確認(19-21がコメント化されてるか):
sed -n '19,21p' brain/cron_collect.sh
```
※これで cron_collect.sh は **収集pull→合成(pipeline/synthesize_x/track/synthesize等)→commit/push** の
**同期処理だけ**になる＝常駐デーモン不要＝WSLで素直に回る。

### 6. 3時間ごとに実行(Windows タスクスケジューラ推奨)
WSL内 cron は自動起動しないので、**Windows タスクスケジューラ**で WSL を叩くのが堅い:
- 操作: プログラム `wsl.exe`
- 引数: `-d Ubuntu -- bash -lic "cd ~/trench-brain && bash brain/cron_collect.sh"`
- トリガー: 3時間ごと、PC起動時にも

(代替: WSL内 `crontab -e` に `0 */3 * * * cd ~/trench-brain && /bin/bash brain/cron_collect.sh`
 ＋ `sudo service cron start`。ただし WSL は再起動でcronが止まりがち＝タスクスケジューラの方が確実。)

### 7. Windows を寝かせない
設定 → 電源 → **スリープ「なし」(電源接続時)**。WSL は Windows が寝ると止まる＝合成が飛ぶ。
ノートなら蓋を閉じてもスリープしない設定 or 電源接続運用に。

### 8. 動作確認(手動で1サイクル)
```bash
cd ~/trench-brain && bash brain/cron_collect.sh
tail -30 brain/state/cron.log     # collect/合成/「pushed main」が出るか
git log -3 --oneline              # "auto-collect: ... (cron)" が push されたか
```
ここで `synth-x: done` か `synth-x: §1a empty, skip` がログに出れば **X合成が回ってる**。

---

## 最後: Mac 側の合成を止める(Windowsが回り出したのを確認してから)
二重writer/二重poller を消すため、**Windowsの push を1回確認したら** Mac で:
```bash
launchctl unload ~/Library/LaunchAgents/com.trenchbrain.collect.plist   # 3h合成ループ停止
# (bot を Mac に残すならそのまま。Windowsに移すなら別途。pump stream も同様)
```
※この Mac側停止は、俺(Mac上のClaude)が「Windows稼働確認OK」の合図で代わりにやってもいい。

---

## まとめ(これで達成すること)
- 合成が **Windows上・お前のサブスク・API課金ゼロ** で3h毎に自動。
- Mac を閉じても/切っても 合成が止まらない＝**真のMac非依存**。
- cloud GHA は収集を継続。Windows は合成。きれいな両輪。
