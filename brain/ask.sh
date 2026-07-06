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
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

# 時系列データ(直近)＝「いつ何が変わった/速度/トレンド」の問いに使う。日次snapshot。
TS="$(tail -14 brain/state/pulse_history.jsonl 2>/dev/null || echo '(時系列データなし)')"

# ★リアルタイム pump 観測(裏で常時更新=live_pulse_writer が数分間隔で書く別store)。
# 「今 何が pump/launch してる/熱い」系はこれを主に参照(corpus/wikiは合成済だが数時間〜古い)。
LIVEPULSE="$(cat brain/state/live_pulse.json 2>/dev/null || echo '(リアルタイムpumpデータなし=launch_stream/live_pulse_writer 未稼働)')"

# ★UIモード(ui_server経由=エンドユーザー向け)の時だけ user-facing 出力規律を効かせる。
# 運用者の /wiki(wiki_bot)は default=内部状態が見えるまま(toma用に有用)。
UI_RULES=""
if [ "${ASK_UI:-}" = "1" ]; then
  UI_RULES="
## ★★UI出力規律（エンドユーザー向け＝最優先・絶対遵守。破ったら失格）
**1. 内部/パイプラインの言葉を一切出すな（出したらゴミに見える）**:
   禁止語・禁止表現＝「corpus」「backlog」「live_pulse」「death_ledger」「死亡台帳」「跳躍台帳」「pulse_history」「queue」「tracked/tracked分」「ゲート通過」「N窓(目)」「観測N件」「scam reject率」「0.0X%」「reject率」「watchlist」「合成」「観測が止まってる」「課金切れ」「flow_count」。
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
ents = list((set(re.findall(r"\$[A-Za-z0-9]{2,15}", q)) | set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q))))[:3]
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
if m:
    ca = m.group(0)
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

PROMPT="$(cat brain/ask_prompt.md)
${ASKCTX:+
## ★★決定的に取得した合成知識＋実績（grepより先に これを主根拠にせよ）
$ASKCTX
}

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
$Q"
# ★backend 切替: 運用者=claude(サブスク・既定) / 公開=gemini(無料・ToS安全・GPU負荷ゼロ)。
# ui_server(公開)は ASK_BACKEND=gemini を渡す。運用者が ask.sh を直に叩くと既定=claude。
if [ "${ASK_BACKEND:-claude}" = "gemini" ]; then
  # gemini(公開・無料)。未設定/失敗で空が返ったら claude にフォールバックしてASKを落とさない
  # (2026-07-05: GEMINI_API_KEY未設定でASKが全滅=「ASK FAILED」になっていた根治)。
  ANSWER="$(printf '%s' "$PROMPT" | python3 brain/ask_gemini.py 2>/dev/null || true)"
  if [ -z "$ANSWER" ]; then
    ANSWER="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
  fi
else
  # --strict-mcp-config 必須(telegram等MCPを起動させない)。read-only(wiki編集しない)。
  ANSWER="$(claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT")"
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
       "q_tickers": tick(q), "q_cas": sorted(set(re.findall(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b", q))),
       "a_tickers": tick(a), "a_handles": sorted({h.lower() for h in re.findall(r"@([A-Za-z0-9_]{3,15})", a)})}
with open("brain/state/query_log.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
PY
fi
printf '%s\n' "$ANSWER"
