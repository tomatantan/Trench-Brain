# COORDINATION — 2台のClaude Code協調規約

> **両方のClaude Codeが作業前に読む共有規約**（Mac Claude=自動で読む / Windows Claude=起動時・サイクル時に読む）。
> 目的: trench-brain を **Claude起点で自律運用**する。本人(tomatantan)が「離席・任せた」と言ったら、下記の役割分担と越えない線に従い、確認なしで完遂する。
> 作成: 2026-07-13（本人「それぞれのできることを明確にしたい・Claude起点で全部やってほしい」）。

## 0. 大前提
- **trench-brainは2台のClaude Codeで運用される**: Mac Claude と Windows Claude。両方とも同じClaude Code＝コード実装/独立検証/git/調査/多視点合成は**どちらもできる**。違いは**環境・持ち場・アクセスできるもの**だけ。
- 本人=決定者。窓口は Mac Claude(Telegram)。本人が離席宣言したら、hard-no以外は確認せず完遂し、結果をTelegramに残す。

## 1. Mac Claude（俺・このセッション）
**持ち場**: MacBook Air（本人が開いている時に稼働・閉じると止まる）
**専任（Macだけが持つ）**:
- 本人とのTelegram対話窓口（このチャンネルはMac Claudeが握る）
  - ★**窓口は常に1セッションだけ**（2026-07-28実障害から）: Telegramは1トークン1受信ポーラー。`claude --channels plugin:telegram` を2セッションで起動するとトークンの取り合いで**両方の受信が死ぬ**（メッセージ未達で滞留）。新セッションを窓口にする時は旧窓口を先に閉じる。診断と復旧手順は memory `telegram-single-poller-conflict`。送信だけなら `~/.claude/channels/telegram/.env` のトークンでBot API直叩きが常に効く（受信死亡時も沈黙しない保険）。
- 私的brain `~/brain` への書き込み（Macローカル+Obsidian Sync）
- memory（セッション引き継ぎの記憶）
**主導する役割**: 全体設計・複雑な実装・独立検証（敵対的に自分の緑を疑う）・深い調査・多視点合成・本人との相談・私的brain運用

## 2. Windows Claude
**持ち場**: Windows端末（24時間常駐・本番の番人）
**専任（Windowsだけが持つ）**:
- 24時間常駐（cron_collect.sh の3hサイクル駆動）
- 公開wiki合成エンジンの実行（headless claude合成→push）
- VM (Oracle) の SSH/管理（serving層 trenchbrain.fun）
- ローカルGPU＝llama（$0合成の可能性・北極星「弱モデルでも運用」の受け皿）
- Windows端末の物理操作（プロセス再起動/kill・batサイクル管理）
**主導する役割**: 常駐運用・本番実行・VM管理・その場の物理判断

## 3. 作業の振り分けルール
- **設計・本人対話・私的brain** → Mac Claude
- **常駐運用・本番実行・VM操作・物理操作** → Windows Claude
- **エンジン改修（コード）** → 設計はMac Claudeが書いてpush → **Windows Claudeが次サイクルで自動pull&実行**（既にこのフロー）
- **実装作業一般** → 適材適所（手が空いてる方 or アクセス的に自然な方）

## 4. 連携方法＝WINDOWS-HANDOFF.md（git共有黒板）
- 2台はリアルタイム直接チャット不可（別マシン）。だが**共有gitリポ経由で非同期に会話**する。
- **手順**:
  1. Mac Claude が `WINDOWS-HANDOFF.md` にタスクを書いてpush（`## TASK` セクション・状態=TODO）
  2. Windows Claude が起動時/サイクル時にこれを読む → 実行 → 状態を DONE に更新し結果を追記してpush
  3. Mac Claude が次に見て確認 or 次タスク
- **ルール**: 各タスクに一意ID・状態(TODO/DOING/DONE/BLOCKED)・依頼者・結果欄。完了は必ず結果を書く（沈黙マージ禁止）。BLOCKEDは理由を書き本人に上げる。
- 秘密情報（鍵/token/個人情報）はHANDOFFに書かない（gitに乗るため）。

## 5. hard-no（両方が守る・離席モードでも越えない線）
本人の明示ルール。離席中でも**やらずに残して報告**する:
1. **資金移動**（swap/送金/署名はhuman-gate）
2. **鍵・秘密の露出**（.env/token/seedをgit/ログ/回答に出さない）
3. **外部への公開・送信**（未確認の外部投稿・課金）
4. **不可逆な削除**（削除は隔離→様子見→再確認。2026-07-13 Trench隔離が手本）
これ以外は離席中でも最善判断で完遂・止まらない（原則9）。

## 6. 芯（両方が従う）
- 公開trench-brain: `trench-brain/CLAUDE.md`（門付き収集・矛盾は消さない・合成が収集に追いつく）
- 全プロジェクト共通: `~/.claude/CLAUDE.md`（運用憲法）+ `~/.claude/PLAYBOOK/`
- 指針10「AIは思考するが判断しない」＝出力は視点・決定は本人。

## 7. ★リポジトリ構成変更（2026-07-30・本人承認済）
- **`Trench-Brain`(main) が private→public化**: GitHub Actions課金失敗(2026-07-27〜)の根本原因＝privateリポはActions分課金・publicなら無料無制限。本人承認の上でpublic化、GHA復旧確認済み。
- **同時に `wiki/` を独立private repo(`github.com/tomatantan/Trench-Brain-wiki`)に分離**: publicになったmainに合成データ本体(entities/concepts/summaries/queries=蓄積した知性そのもの)が丸見えになるのを防ぐ。rawソースは憲法通り「合成されないソースは価値ゼロ」なので公開のままでよい。
- **具体的な変更**:
  - `wiki/` は main の `.gitignore` 対象＝main からは一切追跡しない。ディスク上には存在し続けるが、**そのパス自体が別のnested git repo**（`wiki/.git` が独立に存在、remote=Trench-Brain-wiki）。
  - 運用に必要だった `wiki/ui`・`wiki/watchlist.md`・`wiki/_templates`・`wiki/ui-data.json` はrepoルート直下(`ui/`・`watchlist.md`・`_templates/`・`ui-data.json`)に移設し、参照コードのパスを全て更新済み。
  - `cron_collect.sh`: main への `git add` ループから wiki/* を除去。main側push後に**別ステップ**で `wiki/` 内独立repoへadd/commit/push（失敗してもmain側は無事）。
  - `ui_server.py`: 静的配信ルートを`wiki/`→repoルートに変更（`/ui/*`パス解決の為）。ただし配信許可を`/ui/*`と`/ui-data.json`だけに絞るガードを追加＝`wiki/`(private)が誤って配信されないようにした。
- **Windows Claude側で必要な作業**: 初回サイクル前に `wiki/.git` が無ければ `cd wiki && git init && git remote add origin https://github.com/tomatantan/Trench-Brain-wiki.git && git fetch && git checkout main` を一度実行(private repoへの書き込み権限=gh認証/deploy keyが必要)。詳細は `brain/RUNBOOK.md` §7の追加行。
- 判断根拠・詳細は memory参照（Mac Claude側）。
