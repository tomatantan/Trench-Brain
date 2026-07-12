#!/bin/bash
# ask.sh — 対話脳。trench の問いに wiki横断で答える(§Query)。会話インターフェースの中身。
# 使い方: bash brain/ask.sh "今 trench で一番張る価値のある非対称はどこ?"
# headless claude が wiki を読んで横断回答(読むだけ=wiki編集しない・--strict-mcp-config=telegram干渉なし)。
# 将来この出力を Q&A bot(別トークン)が telegram に返す。中身=このスクリプト。
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${ASK_MODEL:-sonnet}"

Q="${*:-}"
[ -n "$Q" ] || { echo "問いを渡して: bash brain/ask.sh \"...\"" >&2; exit 1; }
# claude CLI はbackend=claude か geminiのfallback時のみ必要。クラウドserving VM(gemini専・claude無し)でも
# 動ける様に必須チェックを外す(2026-07-08 serving層の家出し)。実呼び出し箇所で有無を見る。
HAS_CLAUDE=0; command -v claude >/dev/null 2>&1 && HAS_CLAUDE=1
if [ "${ASK_BACKEND:-claude}" != "gemini" ] && [ "$HAS_CLAUDE" = "0" ]; then
  echo "claude CLI なし(ASK_BACKEND=gemini なら動く)" >&2; exit 1
fi

# 時系列データ(直近)＝「いつ何が変わった/速度/トレンド」の問いに使う。日次snapshot。
TS="$(tail -14 brain/state/pulse_history.jsonl 2>/dev/null || echo '(時系列データなし)')"

# ★リアルタイム pump 観測(裏で常時更新=live_pulse_writer が数分間隔で書く別store)。
# 「今 何が pump/launch してる/熱い」系はこれを主に参照(corpus/wikiは合成済だが数時間〜古い)。
LIVEPULSE="$(cat brain/state/live_pulse.json 2>/dev/null || echo '(リアルタイムpumpデータなし=launch_stream/live_pulse_writer 未稼働)')"

# ★KOL網の流れ(2026-07-12 本人「KOLを取るのは市場の流れを捉えるため・銘柄の温度じゃない」):
# watchlist全発言(ティッカー無し含む)の話題重心とその移動(7日vs前7日)＝地合いダイヤルの入力。
FLOWPULSE="$(cat brain/state/flow_pulse.json 2>/dev/null || true)"

# ★外部検知botのライブCALL(2026-07-11 本人「猫太郎とかのシグナル使えてなくない？」の根治①):
# /api/detect に着弾した検知(brain/state/detections.jsonl=serving機ローカル)を回答材料に注入。
# 従来はUIのCALL欄表示のみ=脳が一切使ってなかった。鮮度gate=直近24h・最新15件・AVOID含む(避け材料も価値)。
DETECTS="$(python3 - <<'PY' 2>/dev/null || true
import json, datetime
now = datetime.datetime.now(datetime.timezone.utc)
rows = []
try:
    for ln in open("brain/state/detections.jsonl", encoding="utf-8"):
        try:
            d = json.loads(ln)
        except Exception:
            continue
        ts = d.get("ts") or d.get("time") or ""
        try:
            t = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
            if (now - t).total_seconds() > 24 * 3600:
                continue
        except Exception:
            pass  # ts不明は捨てない(直近ファイル末尾なら新しい)
        rows.append(d)
except Exception:
    pass
# 検知botの成績表(detect_track_record.py)＝「出た」でなく「当たるのか」の重み。あれば先頭に1行。
try:
    tr = json.load(open("brain/state/detect_track_records.json", encoding="utf-8"))
    lines = [f"{k}: {v['evaluated']}件評価中 死{v['death_rate']}%"
             for k, v in sorted((tr.get("records") or {}).items()) if v.get("evaluated")]
    if lines:
        print("★この検知網の実績(AVOIDは死%高=避けが的中/REVIEW系は死%低=拾いが良い・現時点スナップショット): "
              + " / ".join(lines))
except Exception:
    pass
for d in rows[-15:]:
    sym = d.get("symbol") or "?"
    print(f"- [{d.get('ts','?')}] ${sym} verdict={d.get('verdict','?')} ca={str(d.get('ca') or '')[:10]}… src={d.get('source','?')}")
PY
)"

# ★UIモード(ui_server経由=エンドユーザー向け)の時だけ user-facing 出力規律を効かせる。
# 運用者の /wiki(wiki_bot)は default=内部状態が見えるまま(toma用に有用)。
UI_RULES=""
if [ "${ASK_UI:-}" = "1" ]; then
  UI_RULES="
## ★★UI出力規律（エンドユーザー向け＝最優先・絶対遵守。破ったら失格）
**1. 内部/パイプラインの言葉を一切出すな（出したらゴミに見える）**:
   禁止語・禁止表現＝「corpus」「backlog」「live_pulse」「death_ledger」「死亡台帳」「跳躍台帳」「pulse_history」「queue」「tracked/tracked分」「ゲート通過」「N窓(目)」「観測N件」「scam reject率」「0.0X%」「reject率」「watchlist」「合成」「観測が止まってる」「課金切れ」「flow_count」「kol_standouts」「stance_map」「ask_context」「traction_candidates」「kol_ca」「synth_queue」。queries/内部ファイルパスをそのまま [[queries/...md]] と引用するな（内容は使ってよい・出典表記は概念/銘柄/人物ページのみ）。
   データの**出所名・パイプライン指標・window数・生の観測カウント・通過率%を書くな**。根拠は人間の言葉で（例『複数の大型KOLが同時に言及』『過去の同型は崩壊した』）か、簡潔な [[概念名]] リンクのみ（[[rug-anatomy]] 等はOK・live_pulse/death_ledger等の内部名はNG）。
**2. 具体を先に・メタ/統計を後に**: 「トレンド/今何が」系は**実際に今 動いてる/launchしてる銘柄を名前で**挙げよ（\$X, \$Y…＋一言ずつ何者か）。死亡率/通過率/件数みたいなメタ統計から始めるな。
**3. 静かでも『待ち』で終わるな**: signalが薄くても (a)今流れてる実銘柄を数個 (b)テーマの偏り (c)**何が出たら入るか=具体的watch条件** を出せ。「待ちが正解」だけの非回答は禁止＝ユーザーは『で、何見ればいいの』となる。
**4. 捏造はしない**: 持ってない具体数値(「\$Xが+Y%」)は作るな。但し 銘柄名/テーマ/構造の読みは出せる。
**5. 結論先行・トレーダーが3秒で使える・パンチ**。冗長なmeta説明・前置き禁止。"
fi

# 問いに $TICKER / CA があれば live X検索(今の熱・watchlist外含む)。無ければ空=スキップ(一般問いはcorpusのみ)。
LIVEX="$(python3 - "$Q" <<'PY'
import sys, re, json, urllib.request, urllib.parse
q = sys.argv[1]
ents = list((set(re.findall(r"\$[A-Za-z0-9]{2,15}", q)) | set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q)) | set(re.findall(r"\b0x[a-fA-F0-9]{40}\b", q))))[:3]  # 2026-07-12 EVM対応
if not ents: sys.exit(0)
key = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="): key = ln.strip().split("=", 1)[1]
except Exception: pass
if not key: sys.exit(0)
out = []
for e in ents:
    u = f"https://api.twitterapi.io/twitter/tweet/advanced_search?query={urllib.parse.quote(e)}&queryType=Latest"
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'X-API-Key': key}), timeout=12)
        tw = (json.loads(r.read()).get('tweets') or [])[:8]
    except Exception:
        continue
    seen = {}
    for t in tw:
        a = t.get('author') or {}; un = a.get('userName')
        if un and un not in seen:
            seen[un] = {'by': un, 'followers': a.get('followers'), 'text': (t.get('text') or '')[:120]}
    if seen:
        out.append({'entity': e, 'live': sorted(seen.values(), key=lambda x: -(x.get('followers') or 0))[:6]})
if out: print(json.dumps(out, ensure_ascii=False, indent=1))
PY
)"

# ★A3統合: 問いに CA→on-chain / accountリンク/@→そのツイ を gather＝1つの頭で全部読む(道具選ばせない)
ENTDATA="$(python3 - "$Q" <<'PY'
import sys, re, json, urllib.request, urllib.parse
q = sys.argv[1]; UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
key = ""
try:
    for ln in open(".env", encoding="utf-8"):
        if ln.startswith("TWITTERAPI_KEY="): key = ln.strip().split("=", 1)[1]
except Exception: pass
out = {}
m = re.search(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q)
m_evm = re.search(r"\b0x[a-fA-F0-9]{40}\b", q)  # 2026-07-12 EVM対応: CA検出にEVMも追加
ca = (m_evm.group(0) if m_evm else None) or (m.group(0) if m else None)
if ca and not ca.startswith("0x"):  # pump.fun/rugcheckはSolana専用＝EVMはgracefully skip(空のまま・エラーにしない)
    try:
        c = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://frontend-api-v3.pump.fun/coins/{ca}", headers={"User-Agent": UA}), timeout=10).read())
        out["token"] = {"sym": c.get("symbol"), "name": c.get("name"), "mcap": c.get("usd_market_cap"), "reply": c.get("reply_count"), "complete": c.get("complete"), "twitter": c.get("twitter")}
    except Exception: pass
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://api.rugcheck.xyz/v1/tokens/{ca}/report", headers={"User-Agent": UA}), timeout=12).read())
        th = d.get("topHolders") or []
        out["token_onchain"] = {"mint_auth": d.get("mintAuthority"), "rugged": d.get("rugged"), "top_pct": round(max((h.get("pct") or 0) for h in th), 1) if th else None, "insiders": bool(d.get("insiderNetworks")), "danger": [r.get("name") for r in (d.get("risks") or []) if r.get("level") == "danger"]}
    except Exception: pass
a = re.search(r"(?:x\.com|twitter\.com)/([A-Za-z0-9_]+)", q) or re.search(r"@([A-Za-z0-9_]{2,15})", q)
if a and key:
    h = a.group(1)
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://api.twitterapi.io/twitter/user/last_tweets?" + urllib.parse.urlencode({"userName": h}), headers={"X-API-Key": key}), timeout=15)
        arr = (json.loads(r.read()).get("tweets") or [])[:15]
        out["account"] = {"handle": h, "recent_tweets": [(t.get("text") or "")[:150] for t in arr]}
    except Exception: pass
if out: print(json.dumps(out, ensure_ascii=False, indent=1))
PY
)"

# ★G1/G2: 決定的retrieval(合成済みwikiをBM25で取得)＋実績注入(KOL track record/base-rate)。
# grep運任せをやめ、脳に「読むべき合成知識」と「誰が本当に当ててるか」をコードで渡す。失敗しても空。
ASKCTX="$(python3 brain/ask_context.py "$Q" 2>/dev/null)"

# ★ライブmacro価格(BTC/ETH/SOL)＝「今の相場/majors/BTCどう」系の土台。
# これが無くて$80-95k等の嘘価格を出してた根治(2026-07-06 本人指摘)。取得失敗時は価格を語らせない。
MACRO="$(python3 - <<'PY'
import json, urllib.request
try:
    u="https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
    d=json.loads(urllib.request.urlopen(u, timeout=10).read())
    def f(k):
        x=d.get(k,{}); return "${:,.0f} ({:+.1f}%/24h)".format(x.get("usd",0), x.get("usd_24h_change",0))
    print("BTC {} / ETH {} / SOL {}".format(f("bitcoin"), f("ethereum"), f("solana")))
except Exception:
    print("(macro価格 取得失敗＝価格を数字で語るな)")
PY
)"

PROMPT="$(cat brain/ask_prompt.md)
${ASKCTX:+
## ★★決定的に取得した合成知識＋実績（grepより先に これを主根拠にせよ）
$ASKCTX
}

## ★今のmajors実価格（ライブ・最優先の事実）
BTC/ETH/SOL や「今の相場/macro/majors/どう動く」系は**必ずこの実価格を根拠にせよ**。記憶や幻の数字で価格レンジを語るな（過去に 8万〜9.5万ドル台 等の捏造で失格した）。この値が「今」。
$MACRO

## ★この人(本人)の文脈＝これを前提に「この人のために」考える(A6)
$(cat brain/user_context.md 2>/dev/null)

## 方法論（Skill Graph: 内部でこれに沿って考える・出力は簡潔に合成）
$(cat brain/methodology/lenses.md)
$(cat brain/methodology/source-tiers.md)
$(cat brain/methodology/synthesis-rules.md)

## 時系列データ（直近14日の日次snapshot＝pulse_history）
「先週から何が変わった/トレンド/速度」系の問いは**このデータで答える**（死/backlog/テーマ分布/台帳/watchlistの推移）。スナップショットの差分を読め。死亡/跳躍台帳(append式)も時系列の根拠に使える。
$TS

## ★リアルタイム pump 観測（裏で常時更新＝今の生の流れ・最重要の鮮度層）
「今 何が pump/launch してる/盛り上がってる/熱い meme は」系はこれを参照。**ただし門を守れ＝"熱い"の先頭は必ず KOL裏付けのある物(kol_standouts＝複数の目立つアカウントが実際に言及)。reply=0 で KOL言及なしの traction候補は"熱い"ではなく『動いてるだけの未確認ノイズ』＝先頭に出すな・"熱い"と呼ぶな。**触れるとしても「板は動いてるが誰も話してない＝噴きの噴きで大半が死ぬ」と型で添えるだけ(観測≠採用)。**kol_standouts が空＝今 KOL裏付けの熱い物は無い、が正しい答え＝正直にそう言い、reply0 の死にかけ micro-cap を"熱い"に仕立てるな**（それが今の質の悪さの元）。live が無い/古い(flow=0 等)時は live を語らず合成知識(型・base-rate)で答えよ。持っていない具体 live 数値は捏造禁止。
$LIVEPULSE
${FLOWPULSE:+

## ★KOL網の流れ（話題の重心と移動・7日vs前7日＝市場の流れの一次入力）
「相場どう/地合い/どう動く/何が来る」系は**銘柄の温度でなくまずこれ**＝網全体の頭がどっちを向き始めたか(delta_pp=話題シェアの移動)。地合いダイヤル(攻める/守る/待つ)の入力・ローテーションの先行指標として読む。銘柄言及はこの流れの下の証拠層。
$FLOWPULSE}
${DETECTS:+

## ★外部検知botのライブCALL（直近24h・信頼するチームの検知網＝生きたsignal層）
コミュニティの検知bot（pump検知・門判定つき）が今日拾ったもの。「今シグナル出てる？/何か検知した？」系はまずここ。verdict=AVOIDは**避け側の材料として**使う（推奨に化けさせない）。検知=注目であって安全ではない＝scam門/base-rateと必ずクロス。
$DETECTS}
${LIVEX:+

## live X（問いの \$ticker/CA を今 誰が語ってるか・watchlist外含む・follower重み）
新規/今の熱はこれで読む（大follower数人がCA投げてる=traction兆候／無風=誰も乗ってない）。⚠️語られてる≠良い(bot/pumper疑い)→corpusのKOL track-recordとクロス。
$LIVEX}
${ENTDATA:+

## ★この問いに含まれる銘柄/アカウントの実データ（1つの頭で全部読め＝道具を選ばせない）
問いに CA/アカウントがあれば下に on-chain/ツイを gather 済。これと corpus・合成知識・liveを**統合して1つの読み**にせよ（/check だの /who だの分けない）。
$ENTDATA}
$UI_RULES

## ユーザーの問い:
$Q

★最後に確認: まず問いのタイプ(上の「出力の型」)。**型A(対象の判断)**なら『複数KOLレンズ/共通点/⚠️矛盾/今すぐ見る1つ』の4見出し。**型B(この人がどう動くかの相談=「どう動けば」「分からん」系)**なら『今のあなたの正しいモード/今日やる3つ/勝者ならこうする/⚠️今のあなたの罠』＝**相場解説で終わったらQとA不一致で失格**。1視点の買い/避け推奨だけも失格。一般知識の問いなら短く直答でよい。"
# ★backend 切替: 運用者=claude(サブスク・既定) / 公開=gemini(無料・ToS安全・GPU負荷ゼロ)。
# ui_server(公開)は ASK_BACKEND=gemini を渡す。運用者が ask.sh を直に叩くと既定=claude。
if [ "${ASK_BACKEND:-claude}" = "gemini" ]; then
  # gemini(公開・無料)。未設定/失敗で空が返ったら claude にフォールバックしてASKを落とさない
  # (2026-07-05: GEMINI_API_KEY未設定でASKが全滅=「ASK FAILED」になっていた根治)。
  ANSWER=""
  # ① まずローカル(Windows)のサブスク Haiku 窓口(ask.trenchbrain.fun)を試す。
  #   起動してれば頭いい回答、落ちてれば Cloudflare が即エラー→空→②Geminiへ自動fallback(2026-07-10)。
  if [ -n "${ASK_WINDOW_URL:-}" ]; then
    ANSWER="$(printf '%s' "$PROMPT" | python3 brain/ask_window_client.py 2>/dev/null || true)"
  fi
  # ② 空なら Gemini(VM完結・常時稼働)へ
  if [ -z "$ANSWER" ]; then
    ANSWER="$(printf '%s' "$PROMPT" | python3 brain/ask_gemini.py 2>/dev/null || true)"
  fi
  if [ -z "$ANSWER" ] && [ "$HAS_CLAUDE" = "1" ]; then
    ANSWER="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
  fi
else
  # --strict-mcp-config 必須(telegram等MCPを起動させない)。read-only(wiki編集しない)。
  ANSWER="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
fi

# ★内部語の機械置換(2026-07-12): 禁止語プロンプトでも弱モデルが漏らす(backlog/kol_standouts等の実漏れ2回目)
# ＝イタチごっこ終了・出力後に決定的に潰す。対象は snake_case の内部識別子のみ(曖昧な日本語語は
# 置換事故が怖いのでプロンプト規律に残す)。ASK_UI=1(エンドユーザー向け)のみ。
if [ "${ASK_UI:-}" = "1" ] && [ -n "$ANSWER" ]; then
  # ★渡し方はenv経由必須: `printf|python3 - <<PY` はheredocがstdinを奪いsys.stdinが空=回答を空に上書きする
  #   (2026-07-12 本番askを数十分落とした実害バグ)。python失敗時も原文維持(fail-safe)。
  FILTERED="$(ASK_RAW="$ANSWER" python3 - <<'PY' 2>/dev/null || true
import os
import sys
t = os.environ.get("ASK_RAW", "")
REPL = {
    "kol_standouts": "複数の目立つアカの言及", "traction_candidates": "板が動いてる候補群",
    "live_pulse": "リアルタイム観測", "pulse_history": "時系列記録", "death_ledger": "過去の死亡記録",
    "ask_context": "参照知識", "synth_queue": "処理待ち", "flow_count": "観測量",
    "signal_backlog": "未消化の新規シグナル", "backlog": "未消化の新規",
    "stance_map": "立場マップ", "chain_base_rate": "チェーン別の実測死亡率",
    "flow_pulse": "網の話題重心",
}
for k, v in REPL.items():
    for var in (k, k.replace("_", "-")):  # ハイフン変種も潰す(実漏れ: kol-standouts 2026-07-12)
        t = t.replace(f"[[{var}]]", v).replace(var, v)
sys.stdout.write(t)
PY
)"
  [ -n "$FILTERED" ] && ANSWER="$FILTERED"
fi

# ★学習の両輪(収集半・原則3): 有効なQ&Aを query_log に capture。
# wikiは書かない(読取専用維持)=state queueに積むだけ。資産化(合成半)は brain/asset_queries.sh が
# 門付きで wiki/queries に落とす=「質問するほど脳が賢くなる」。失敗しても答えは壊さない(|| true)。
if [ -n "$ANSWER" ]; then
  ASK_Q="$Q" ASK_A="$ANSWER" ASK_B="${ASK_BACKEND:-claude}" python3 - <<'PY' 2>/dev/null || true
import json, os, datetime, re
q = os.environ.get("ASK_Q", ""); a = os.environ.get("ASK_A", "")
# ★G5b: 呼んだ銘柄/KOLを回答時点で構造化保存＝後からの採点(score_queries.py)を精密にする。
money = re.compile(r"\d+(?:[.,]\d+)?[kKmMbB]?$")
tick = lambda t: sorted({x.upper() for x in re.findall(r"\$([A-Za-z0-9]{2,15})\b", t) if not money.fullmatch(x)})
rec = {"ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
       "question": q, "answer": a,
       "backend": os.environ.get("ASK_B", ""), "assetized": False,
       "q_tickers": tick(q), "q_cas": sorted(set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q)) | set(re.findall(r"\b0x[a-fA-F0-9]{40}\b", q))),  # 2026-07-12 EVM対応
       "a_tickers": tick(a), "a_handles": sorted({h.lower() for h in re.findall(r"@([A-Za-z0-9_]{3,15})", a)})}
with open("brain/state/query_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
PY
fi
printf '%s\n' "$ANSWER"
