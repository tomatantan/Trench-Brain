#!/bin/bash
# Trench-Brain ローカル自動収集＋合成（launchd/cronから叩く）＝両輪を1サイクルで回す。
# 収集(twitterapi)→worklist(鮮度ゲート)→[pump.fun合成 + X合成(headless)]→UI→commit/push。
# 指針3「収集と合成は両輪」: 収集だけでなく合成(判断)まで毎サイクル回す。
#   - pump.fun側: track.py(観測→篩→queue) → synthesize.sh(headless合成)
#   - X側:        pipeline.py が worklist(§1a=鮮度ゲート) → synthesize_x.sh(headless合成 上位3件/複利)
#   どちらも headless claude は --strict-mcp-config(telegram干渉なし) / SYNTH_*_ENABLED で停止可。
set -euo pipefail
cd /Users/toma/trench-brain

export PATH="/usr/bin:/bin:/usr/local/bin:$PATH"
LOG="brain/state/cron.log"
mkdir -p brain/state
echo "=== $(date -u +%Y-%m-%dT%H:%M:%SZ) collect start ===" >> "$LOG"

# ★永続化(本人「永遠に動かせ」)＝自己修復: このcronはRunAtLoad(boot時)+3h毎に発火する唯一の確実なanchor。
#   毎回ここで (1)caffeinate=Mac起こし続ける→3h cronが確実に発火 (2)Q&A bot を常駐 を再確認し、死んでたら起こす。
#   ＝Macが電源ONな限り、collect/合成/bot/起き続け が自己修復で永続する。
pgrep -f "caffeinate -i -m -s" >/dev/null 2>&1 || { nohup caffeinate -i -m -s >/dev/null 2>&1 & echo "self-heal: caffeinate起動" >> "$LOG"; }
pgrep -f "brain/wiki_bot.py" >/dev/null 2>&1 || { nohup /usr/bin/python3 /Users/toma/trench-brain/brain/wiki_bot.py >> brain/state/bot.out 2>&1 & echo "self-heal: bot起動" >> "$LOG"; }
pgrep -f "brain/launch_stream.py" >/dev/null 2>&1 || { nohup /usr/bin/python3 /Users/toma/trench-brain/brain/launch_stream.py >> brain/state/launch_stream.log 2>&1 & echo "self-heal: launch_stream起動" >> "$LOG"; }

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

# auto-synthesis: (1)決定的層=全mint観測→篩→watch→synth_queue(LLM不使用)
python3 brain/track.py run >> "$LOG" 2>&1 || echo "track skipped" >> "$LOG"
# (2)pump.fun合成層=synth_queue を headless claude が wiki に合成(空なら呼ばない=コスト0)
bash brain/synthesize.sh || echo "synth skipped" >> "$LOG"
# (2b)X側合成層=worklist §1a(鮮度ゲート通過)全件 を headless claude が合成(§1a空なら呼ばない=コスト0)
bash brain/synthesize_x.sh || echo "synth-x skipped" >> "$LOG"
# (2c)長文合成層=未合成transcriptを3本/サイクル deep 合成(0本なら呼ばない=コスト0)
bash brain/synthesize_longform.sh || echo "synth-longform skipped" >> "$LOG"
# (2d)backfill層=高signal未合成stubを5件/サイクル deep 合成=グラフ密度UP(対象無で呼ばない=コスト0・自己限定)
bash brain/synthesize_backfill.sh || echo "synth-backfill skipped" >> "$LOG"
# (2e)lint層=第5の輪・自己検証(過学習対策)。wiki自身の小N型/矛盾/陳腐化を敵対的に検出→lint-report(報告のみ)。~日次gate。
bash brain/synthesize_lint.sh || echo "lint skipped" >> "$LOG"
# (2f)★憲法conformance検査(機械・毎サイクル・安価)=芯チェックの構造化。違反は wiki/conformance-report.md+ログに出す。
python3 brain/check_conformance.py >> brain/state/conformance.log 2>&1 && echo "conformance: PASS" >> "$LOG" || echo "★conformance: 違反あり→wiki/conformance-report.md" >> "$LOG"
# (2g)★時系列snapshot=主要metricsをdated appendで貯める(本人「時系列弱い」対処・決定的・安価)。trajectory取得の土台。
python3 brain/snapshot.py >> "$LOG" 2>&1 || echo "snapshot skipped" >> "$LOG"
python3 brain/feedback.py >> "$LOG" 2>&1 || echo "feedback skipped" >> "$LOG"
python3 brain/kol_track_record.py >> "$LOG" 2>&1 || echo "kol-track-record skipped" >> "$LOG"
python3 brain/predictive_study.py >> "$LOG" 2>&1 || echo "predictive-study skipped" >> "$LOG"
python3 brain/scorecard.py >> "$LOG" 2>&1 || echo "scorecard skipped" >> "$LOG"
# (3)UI連携=entities+track状態 → wiki/ui-data.json(UIチームが消費)
python3 brain/export_ui.py >> "$LOG" 2>&1 || echo "export_ui skipped" >> "$LOG"

# ingested.txt も add=合成dedup状態を版管理(でないと次サイクルで再合成対象に出る)
# local は sources/x を add しない(=cloud専任。書き込みパス分離で衝突防止)。local所有=youtube/wiki/state。
git add sources/youtube wiki/dashboards wiki/entities wiki/concepts wiki/summaries wiki/queries wiki/_worklist.md wiki/log.md wiki/index.md wiki/canon.md wiki/feeds.md wiki/ui-data.json wiki/conformance-report.md brain/state/ingested.txt brain/state/health.jsonl brain/state/pulse_history.jsonl brain/state/kol_track_records.json brain/state/risk_weights.json brain/state/brain_calls.jsonl >> "$LOG" 2>&1 || true
if git diff --cached --quiet; then
  echo "no new data" >> "$LOG"
else
  git commit -q -m "auto-collect: $(date -u +%Y-%m-%dT%H:%MZ) (cron)" >> "$LOG" 2>&1
  # push直前にもう一度 rebase: cron実行中に cloud GHA collector が push して分岐した場合に対応。
  git pull -q --rebase --autostash origin main >> "$LOG" 2>&1 || echo "pre-push pull skipped" >> "$LOG"
  git push -q origin main >> "$LOG" 2>&1 && echo "pushed main" >> "$LOG" || echo "push failed(次サイクル再試行)" >> "$LOG"
fi

# スマホ閲覧用 軽量ミラー＝専用 private repo Trench-Brain-wiki(wiki/だけ・213md)を force更新。
# 6000+の sources/x を含む main は重くスマホ同期に不向き→iOS Obsidian はこの軽量repoをclone。
WIKI_SHA="$(git subtree split --prefix=wiki main 2>/dev/null)"
[ -n "$WIKI_SHA" ] && git push https://github.com/tomatantan/Trench-Brain-wiki.git "$WIKI_SHA":main --force >> "$LOG" 2>&1 \
  && echo "wiki mobile-mirror updated" >> "$LOG" || echo "wiki mobile-mirror skipped" >> "$LOG"
echo "=== done ===" >> "$LOG"
