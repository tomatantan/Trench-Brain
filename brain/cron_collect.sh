#!/bin/bash
# Trench-Brain ローカル自動収集＋合成（launchd/cronから叩く）＝両輪を1サイクルで回す。
# 収集(twitterapi)→worklist(鮮度ゲート)→[pump.fun合成 + X合成(headless)]→UI→commit/push。
# 指針3「収集と合成は両輪」: 収集だけでなく合成(判断)まで毎サイクル回す。
#   - pump.fun側: track.py(観測→篩→queue) → synthesize.sh(headless合成)
#   - X側:        pipeline.py が worklist(§1a=鮮度ゲート) → synthesize_x.sh(headless合成 上位3件/複利)
#   どちらも headless claude は --strict-mcp-config(telegram干渉なし) / SYNTH_*_ENABLED で停止可。
set -euo pipefail
cd "$(dirname "$0")/.."

export PATH="/usr/bin:/bin:/usr/local/bin:$PATH"
LOG="brain/state/cron.log"
mkdir -p brain/state
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) collect start ===" >> "$LOG"

# ★headless claude 認証の恒久策(2026-08-11発覚: OAuth /login の access token は無人headless実行
#   では自動refreshされない=公式ドキュメント確認済の仕様。11〜15日で毎回手動re-login地獄だった)。
#   `claude setup-token`(要ブラウザ承認・1回だけ)で発行される1年有効トークンを.envに置けば
#   claude CLIが認証precedenceで自動的にこちらを使う(サブスク課金のまま・API従量課金にはならない)。
#   .envに無ければ何もしない=既存の/loginセッションにfallback(後方互換・無害)。
if [ -f .env ]; then
  _OAUTH_TOKEN="$(grep '^CLAUDE_CODE_OAUTH_TOKEN=' .env 2>/dev/null | head -1 | cut -d= -f2-)"
  [ -n "$_OAUTH_TOKEN" ] && export CLAUDE_CODE_OAUTH_TOKEN="$_OAUTH_TOKEN"
fi

# ★永続化(本人「永遠に動かせ」)＝自己修復: このcronはRunAtLoad(boot時)+3h毎に発火する唯一の確実なanchor。
#   毎回ここで (1)caffeinate=Mac起こし続ける→3h cronが確実に発火 (2)Q&A bot を常駐 を再確認し、死んでたら起こす。
#   ＝Macが電源ONな限り、collect/合成/bot/起き続け が自己修復で永続する。
[ "$(uname)" = "Darwin" ] && { pgrep -f "caffeinate -i -m -s" >/dev/null 2>&1 || { nohup caffeinate -i -m -s >/dev/null 2>&1 & echo "self-heal: caffeinate起動(mac)" >> "$LOG"; }; }
pgrep -f "brain/wiki_bot.py" >/dev/null 2>&1 || { nohup python3 brain/wiki_bot.py >> brain/state/bot.out 2>&1 & echo "self-heal: bot起動" >> "$LOG"; }
pgrep -f "brain/launch_stream.py" >/dev/null 2>&1 || { nohup python3 brain/launch_stream.py >> brain/state/launch_stream.log 2>&1 & echo "self-heal: launch_stream起動" >> "$LOG"; }

# 単一枝 main に一本化(2026-06-22 unify)。collect=門付き(watchlist)＝憲法 指針2準拠。
# --autostash: .obsidian 等の未staged変更があっても rebase を通す(無いと pull skip→cloud GHA
# の push と分岐した時に末尾 push が non-fast-forward で失敗する。2026-06-23 cloud冗長化で必須化)。
git pull -q --rebase --autostash origin main >> "$LOG" 2>&1 || echo "pull skipped" >> "$LOG"
# ★X収集は cloud GHA(collect-cloud) 専任＝ここでは collect しない(2026-06-23 修正)。
#   理由: cloud と local が両方 X を collect すると、同一ツイートを別commitで add/add →
#   rebase で衝突して push が詰まりループがjamる(実害発生)。書き込みパスを分離=衝突を原理的に消す。
#   設計「cloud=収集の腕 / local=合成の脳」に一致。local は pull で cloud の sources/x を取得し合成に使う。
#   pipeline.py(--collect無し)= digest→build_entities→worklist(鮮度ゲート)を既存 sources/x から生成。
python3 brain/pipeline.py >> "$LOG" 2>&1 || echo "pipeline failed(継続)" >> "$LOG"
# 長文収集(YouTube/podcast transcript)=local専任(cloudは収集しない=書き込みパス分離)。門 feeds.md・1ch少数/回。
python3 collector/collect_youtube.py --limit 1 >> "$LOG" 2>&1 || echo "yt-collect skipped(継続)" >> "$LOG"
# ★自動で賢くなる: watchlist(門)を引用グラフから自動拡張(候補化→人は承認だけ・指針2)。決定的層=LLM不要。
python3 brain/expand_watchlist.py >> "$LOG" 2>&1 || echo "expand-watchlist skipped" >> "$LOG"
# ★UIからの1タップ承認(/api/approve_watchlist)をwatchlist.mdへ反映(2026-08-06新設)。
#   サーバー側はローカルqueueに積むだけ＝実際の書き込みとgit commit/pushはここでまとめて行う。
python3 brain/apply_watchlist_approvals.py >> "$LOG" 2>&1 || echo "apply-watchlist-approvals skipped" >> "$LOG"
# ★段階投入: 承認済み候補queueを1人/サイクルだけ門へ(本人指示2026-07-07「一気でなく1人ずつ」)。
#   健康ゲート(signal_backlog増加中は停止)+理解ゲート(onboarding profile必須)。決定的・queue空ならno-op。
python3 brain/staged_intake.py >> "$LOG" 2>&1 || echo "staged-intake skipped" >> "$LOG"
# ★onboarding自動化(2026-07-12): queue内でprofile未作成の先頭1人を毎サイクルonboard(理解→収集の門の自動運転)。
#   従来onboardはcron未配線=実ツイ取得不可だった12人が永久に待つ構造だった。データが取れ次第自動で通る。
ONBOARD_TARGET="$(python3 - <<'PYEOF'
import json, os
try:
    q = json.load(open("brain/state/staged_intake_queue.json")).get("queue") or []
except Exception:
    q = []
for it in q:
    h = (it.get("handle") or "").lower()
    ent = f"wiki/entities/players/@{h}.md"
    if h and not (os.path.exists(ent) and "profile:start" in open(ent, encoding="utf-8", errors="replace").read()):
        print(h)
        break
PYEOF
)"
[ -n "$ONBOARD_TARGET" ] && { bash brain/onboard_player.sh "$ONBOARD_TARGET" >> "$LOG" 2>&1 || echo "onboard($ONBOARD_TARGET) skipped" >> "$LOG"; }

# ★節約モード(本人指示2026-07-07「サブスク上限・クレジット消費中=節約して」・既定ON):
#   維持系のheadless合成を haiku に落とし件数も絞る。品質は synth_validate(門番)+北極星設計
#   「弱いモデルでも運用できる」が担保。★ユーザー向け /api/ask は対象外(公開=gemini無料・fallbackのみclaude)。
#   戻す時: ECONOMY=0 をwrapper/環境で渡す。個別上書き(SYNTH_MODEL等)は常に優先される。
# Telegram /model で書かれた engine_model.txt を反映(優先順: env明示 > file > ECONOMY既定)。
# 未設定なら現状維持(何も変わらない)。cwdは冒頭のcdでrepo root。
if [ -f brain/state/engine_model.txt ]; then
  _EM="$(tr -dc 'a-z0-9.-' < brain/state/engine_model.txt 2>/dev/null)"; _EM="${_EM:0:40}"
  if [ -n "$_EM" ]; then
    export ASK_MODEL="${ASK_MODEL:-$_EM}"
    export SYNTH_MODEL="${SYNTH_MODEL:-$_EM}"
    export SYNTH_PLAYER_MODEL="${SYNTH_PLAYER_MODEL:-$_EM}"
    echo "engine_model.txt→model=$_EM (env未指定の合成/askに適用)" >> "$LOG"
  fi
fi
ECONOMY="${ECONOMY:-1}"
if [ "$ECONOMY" = "1" ]; then
  export SYNTH_MODEL="${SYNTH_MODEL:-haiku}"
  export SYNTH_PLAYER_MODEL="${SYNTH_PLAYER_MODEL:-haiku}"
  # ONBOARD_MODEL は economy 対象外(2026-07-12 本人「発言を取る前に人物理解が要る」=人物理解の質は節約しない→sonnet既定)
  export PLAYER_SYNTH_MAX="${PLAYER_SYNTH_MAX:-1}"
  export BACKFILL_TOPN="${BACKFILL_TOPN:-2}"
  echo "economy mode ON (維持合成=haiku・player 1/巡・backfill 2/巡)" >> "$LOG"
fi

# auto-synthesis: (1)決定的層=全mint観測→篩→watch→synth_queue(LLM不使用)
python3 brain/track.py run >> "$LOG" 2>&1 || echo "track skipped" >> "$LOG"
# ★能動的通知(2026-08-06新設): 合成(次項)を待たず、強い門(KOL CA一致)通過を即Telegram通知。
#   LLM不使用・$0。監査で見つけた穴「gate通過してもsynth_queueに積まれるだけで誰も気づかない」の修正。
python3 brain/scout_alert.py >> "$LOG" 2>&1 || echo "scout_alert skipped" >> "$LOG"
# (2)pump.fun合成層=synth_queue を headless claude が wiki に合成(空なら呼ばない=コスト0)
bash brain/synthesize.sh || echo "synth skipped" >> "$LOG"
# (2b)X側合成層=worklist §1a(鮮度ゲート通過)全件 を headless claude が合成(§1a空なら呼ばない=コスト0)
bash brain/synthesize_x.sh || echo "synth-x skipped" >> "$LOG"
# ★単一player思考conceptの濫造防止(指針8): synthesize_xが作っても掃除=player思考はentity(synthesize_player)がcanonical
rm -f wiki/concepts/player-*.md 2>/dev/null || true
# (2d.47)★核心成果物の自動維持: player mind-model(KOLの"脳"=思考の型)を毎サイクル自動合成。
# 従来 synthesize_player は手動のみで cron未配線＝KOLの脳が自動更新されてなかった(engine再設計の核gap)。
# 直近活動+stale順に上限3人/サイクル。空ならclaude未呼出=$0。視点エンジン(ask.sh)が読む燃料を厚くする。
bash brain/synthesize_players.sh >> "$LOG" 2>&1 || echo "synthesize_players skipped" >> "$LOG"
# (2c)長文合成層=未合成transcriptを3本/サイクル deep 合成(0本なら呼ばない=コスト0)
bash brain/synthesize_longform.sh || echo "synth-longform skipped" >> "$LOG"
# (2d)backfill層=高signal未合成stubを5件/サイクル deep 合成=グラフ密度UP(対象無で呼ばない=コスト0・自己限定)
bash brain/synthesize_backfill.sh || echo "synth-backfill skipped" >> "$LOG"
# (2d.4)★自動最適化ループ(step2): 内部danglingを決定的3分岐＝一意case/表記ゆれのconcept-slugは自動修復・
#   本物のconcept-gapは brain/state/wiki_gaps.json に積む(consumerが判断)・閾値未満の$ticker/@handleは放置。
#   機械的で曖昧ゼロの修正のみ自動(憲法境界)・上限50・atomic・冪等。--apply で実適用(現repairable=0で安全)。
python3 brain/wiki_autofix.py --apply >> "$LOG" 2>&1 || echo "autofix skipped" >> "$LOG"
# (2d.45)★gap-consumer: wiki_autofix が積んだ concept-gap を headless LLM が保守的に自動解決
#   (履歴leave / 既存へre-point / stray de-link / 判断不能は残す・新規conceptは作らない=指針8)。空queueなら呼ばない=コスト0。
bash brain/synthesize_gaps.sh || echo "synth-gaps skipped" >> "$LOG"
# (2d.46)★学習の両輪(合成半・§Query/原則3): ask.sh が積んだ Q&A(query_log)を門付きで wiki/queries に
# 資産化＝質問するほど脳が賢くなる(以後 BM25/api/search で回答材料に=クエリ軸の複利)。空queue=コスト0。
python3 brain/asset_queries.py >> "$LOG" 2>&1 || echo "asset_queries skipped" >> "$LOG"
# (2d.48)★1タップ学習を消費(サーフィンの「学習」ボタン→KOL watchlist昇格/銘柄フラグ/ソース保存・人が門)
python3 brain/learn_consume.py >> "$LOG" 2>&1 || echo "learn_consume skipped" >> "$LOG"
# (2d.5)★合成出力の門番(step3・foolproof): この周期の合成が壊れたページ(frontmatter破損/synthesisブロック不均衡/失敗マーカー)を吐いてないか機械検証。fail-safe=commitは止めない(queueがgitignore=revertでqueue-loss危険)が不正をloudにログ+記録し沈黙failを根絶。
python3 brain/synth_validate.py > brain/state/synth_validate.out 2>&1 && echo "synth_validate: OK" >> "$LOG" || echo "★synth_validate: 合成出力に不正検出→brain/state/synth_validate.out 要確認" >> "$LOG"
# (2e)lint層=第5の輪・自己検証(過学習対策)。wiki自身の小N型/矛盾/陳腐化を敵対的に検出→lint-report(報告のみ)。~日次gate。
bash brain/synthesize_lint.sh || echo "lint skipped" >> "$LOG"
# (2f)★憲法conformance検査(機械・毎サイクル・安価)=芯チェックの構造化。違反は wiki/conformance-report.md+ログに出す。
python3 brain/check_conformance.py >> brain/state/conformance.log 2>&1 && echo "conformance: PASS" >> "$LOG" || echo "★conformance: 違反あり→wiki/conformance-report.md" >> "$LOG"
# (2g0)★KOL網の流れ計測(2026-07-12 本人「KOLは市場の流れを捉えるため」)=話題重心の移動を決定的に。$0
python3 brain/flow_pulse.py >> "$LOG" 2>&1 || echo "flow-pulse skipped" >> "$LOG"
# (2g)★時系列snapshot=主要metricsをdated appendで貯める(本人「時系列弱い」対処・決定的・安価)。trajectory取得の土台。
python3 brain/snapshot.py >> "$LOG" 2>&1 || echo "snapshot skipped" >> "$LOG"
# (2g1)★複利計=矛盾KPI(§0.1-1): contradictions_surfaced 含む複利metricsを毎サイクル記録(K1がechochamber監視)。
python3 brain/compounding.py >> "$LOG" 2>&1 || echo "compounding skipped" >> "$LOG"
python3 brain/feedback.py >> "$LOG" 2>&1 || echo "feedback skipped" >> "$LOG"
python3 brain/kol_track_record.py >> "$LOG" 2>&1 || echo "kol-track-record skipped" >> "$LOG"
# (2g4)★検知bot成績表: 外部検知(猫太郎bot等)のCAをoutcome照合し source×verdict で採点(cache共有・bounded)
python3 brain/detect_track_record.py >> "$LOG" 2>&1 || echo "detect-track-record skipped" >> "$LOG"
# (2g3)★G5b答え採点: 過去回答の言及銘柄/KOLを実outcomeと照合(ca_outcome_cache更新直後)→ask_context第4注入で自己校正。
python3 brain/score_queries.py >> "$LOG" 2>&1 || echo "score_queries skipped" >> "$LOG"
python3 brain/predictive_study.py >> "$LOG" 2>&1 || echo "predictive-study skipped" >> "$LOG"
# (2g2)★G4自己改訂: 実測(feedback_stats)とconcept本文の数値乖離を決定的検出→LLMが推移保持で再合成→門番で再検証。
#   実測系(feedback/predictive)の直後に置く=最新実測との比較。queueが空/同一署名なら consumer はコスト0。
python3 brain/revise_detect.py >> "$LOG" 2>&1 || echo "revise_detect skipped" >> "$LOG"
bash brain/synthesize_revise.sh || echo "synth-revise skipped" >> "$LOG"
python3 brain/synth_validate.py >> brain/state/synth_validate.out 2>&1 || echo "★synth_validate(revise後): 不正検出→brain/state/synth_validate.out" >> "$LOG"
# (2g5)★ショーケース回答=UIの「今日の読み」を毎サイクル1本生成(haiku・閲覧は静的=コスト0)
bash brain/showcase.sh >> "$LOG" 2>&1 || echo "showcase skipped" >> "$LOG"
# (2h)★自律read=trenchを見てgenuine notableな時だけ本人にpush(大半沈黙・spam無)
bash brain/autonomous_read.sh >> "$LOG" 2>&1 || echo "auto-read skipped" >> "$LOG"
# (2i)★自律research=脳が自分で仮説立て→tracked dataで検証→確証/反証を学ぶ(試行錯誤で corpus が賢くなる)
bash brain/autonomous_research.sh >> "$LOG" 2>&1 || echo "auto-research skipped" >> "$LOG"
# (3)UI連携=entities+track状態 → wiki/ui-data.json(UIチームが消費)
python3 brain/export_ui.py >> "$LOG" 2>&1 || echo "export_ui skipped" >> "$LOG"
# (3a)★Master Index/MOC自動再生成: 被リンク数(inbound)から知識の中心を機械算出し wiki/index.md を
#   上書き(原則1=手書きindexは腐る対策)。build_entities/synthesisが全部済んだ後・git add の直前に置く。
# ★entity_paths normalizer(2026-07-11): LLMが書いたtokenページのcasefold衝突を機械的に潰す
#   (macOS case-insensitive FSのpull/rebase詰まり根治)。synthesis全済み後・git add前・writer非依存の安全層。
python3 brain/entity_paths.py --fix >> "$LOG" 2>&1 || echo "entity_paths normalizer error" >> "$LOG"
python3 brain/build_moc.py >> "$LOG" 2>&1 || echo "build_moc skipped" >> "$LOG"

# ★claude CLI 認証切れ検知(2026-08-11実インシデント再発防止):
#   OAuth失効でheadless claude(synthesize*.sh)が全滅しても、git pushはclaude非依存で
#   成功し続ける設計＝「動いてるように見えたまま合成だけ15日死ぬ」が実際に起きた
#   (2026-07-27失効→8/11発覚、357回連続失敗、queue 819→3650件)。
#   このサイクルの新規ログだけを見て認証切れの痕跡があれば即Telegram通知(12h debounce)。
THIS_RUN_LOG="$(awk '/=== .* collect start ===/{buf=""} {buf=buf $0 "\n"} END{print buf}' "$LOG" 2>/dev/null || true)"
if printf '%s' "$THIS_RUN_LOG" | grep -qiE "oauth (access )?token (has )?expired|please run.*(/login|claude login)|invalid_grant|not logged in"; then
  ALERT_FILE="brain/state/auth_alert_last.txt"
  NOW_E=$(date +%s); LAST_E=$(cat "$ALERT_FILE" 2>/dev/null || echo 0)
  if [ $(( NOW_E - LAST_E )) -gt 43200 ]; then
    echo "$NOW_E" > "$ALERT_FILE"
    TOKEN="$(grep '^TG_WIKI_BOT_TOKEN=' .env 2>/dev/null | cut -d= -f2)"
    if [ -n "$TOKEN" ]; then
      python3 - "$TOKEN" "7563521418" <<'PY' >> "$LOG" 2>&1 || true
import sys, urllib.request, urllib.parse
token, chat = sys.argv[1], sys.argv[2]
msg = "⚠️ [trench] このホストの claude CLI 認証(OAuth)が切れてます。合成が止まってます。ターミナルで `claude` を起動して再ログインしてください。"
data = urllib.parse.urlencode({"chat_id": chat, "text": msg}).encode()
try:
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=data, timeout=20)
    print("auth-alert: pushed")
except Exception as e:
    print(f"auth-alert push err: {e}")
PY
    fi
    echo "★auth-alert: claude CLI認証切れを検知しTelegram通知" >> "$LOG"
  fi
fi

# ingested.txt も add=合成dedup状態を版管理(でないと次サイクルで再合成対象に出る)
# local は sources/x を add しない(=cloud専任。書き込みパス分離で衝突防止)。local所有=youtube/wiki/state。
# ★per-path add(2026-07-10 恒久修正): 一括addだと1個の欠損pathspec(例: learn_consumeが消した
#   learn_queue.jsonl)で git add が丸ごとfatal→**有効な変更が1件もstageされずcommit/pushが数日死ぬ**
#   (7/4-7/10の実事故・synthは正常なのに公開面が凍った真因)。1 pathずつaddし欠損は握り潰す。
for _p in sources/youtube ui-data.json watchlist.md \
          brain/user_context.md brain/state/hypotheses.jsonl \
          brain/state/research_log.jsonl brain/state/ingested.txt brain/state/health.jsonl \
          brain/state/pulse_history.jsonl brain/state/kol_track_records.json brain/state/risk_weights.json \
          brain/state/feedback_stats.json brain/state/answer_scorecard.json \
          brain/state/compounding_history.jsonl brain/state/learn_queue.jsonl brain/state/learn_flags.json \
          brain/state/detect_history.json brain/state/detect_track_records.json brain/state/chain_base_rate.json brain/state/flow_pulse.json brain/state/showcase.json; do
  git add "$_p" >> "$LOG" 2>&1 || true
done
if git diff --cached --quiet; then
  echo "no new data" >> "$LOG"
else
  git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "$LOG" 2>&1
  # push直前にもう一度 rebase: cron実行中に cloud GHA collector が push して分岐した場合に対応。
  git pull -q --rebase --autostash origin main >> "$LOG" 2>&1 || echo "pre-push pull skipped" >> "$LOG"
  git push -q origin main >> "$LOG" 2>&1 && echo "pushed main" >> "$LOG" || echo "push failed(次サイクル再試行)" >> "$LOG"
fi

# ★wiki/ 本体(entities/concepts/summaries/queries=合成の資産そのもの)は2026-07-30から
#   main(public)には一切コミットしない＝wiki/ 自体が独立repo(private Trench-Brain-wiki)。
#   ここで別途 add/commit/push する(main側のpushとは独立・失敗してもmain側は影響されない)。
if [ -d wiki/.git ]; then
  ( cd wiki \
    && git add -A >> "../$LOG" 2>&1 \
    && if git diff --cached --quiet; then
         echo "wiki(private): no new data" >> "../$LOG"
       else
         git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "../$LOG" 2>&1
         git pull -q --rebase --autostash origin main >> "../$LOG" 2>&1 || echo "wiki(private) pull skipped" >> "../$LOG"
         git push -q origin main >> "../$LOG" 2>&1 && echo "wiki(private) pushed" >> "../$LOG" \
           || echo "wiki(private) push failed(次サイクル再試行)" >> "../$LOG"
       fi )
else
  echo "★wiki/.git 未初期化＝private repoのclone/git initが必要(brain/RUNBOOK.md参照)" >> "$LOG"
fi
echo "=== done ===" >> "$LOG"
