#!/usr/bin/env python3
"""synthesize_local.py — auto-synthesis の合成工程をローカルLLM(ollama)で回す。

■ なぜ作るか(2026-08-30)
既存の synthesize.sh は `claude --print --model sonnet` に合成ごと任せていたが、
WSL側の claude CLI のトークンが失効し、**20分おきに 401 を出しては黙って再試行**
していた。cron.log には出ていたが誰にも通知しないので気づかれず、
synth_queue が **4,319件** まで積み上がった。
課金・認証・レート制限のどれにも依存しない形に移す = ローカルLLM。

■ 設計: LLMに「ファイル操作」をさせない
claude版はwikiへの書き込みごとエージェントに任せていた。ollamaの素の生成には
ツールが無いのでそのままは動かないが、**分けた方が安全**でもある:
  ・ファイル入出力・キュー管理・台帳追記・skip判定 → このスクリプトが決定的に行う
  ・LLM → 「観測/判断」の文章と、13conceptのどれに刺さるかだけを返す
14bにwiki全体の書き込み権を渡すと何を壊すか分からない。書き込み先はコードで固定する。

■ 深さ∝情報量(brain/synth_prompt.md の方針をそのまま実装)
  A: KOL言及 / tokenized_agent / reply>0 / social整備(tw&web) / real_sol>=20 → LLMで合成
  B: tw か web か real_sol>0 のどれか                                        → 決定的stub
  C: どれも無い                                                              → entityを作らない
実測(2026-08-30のキュー4,328件): A=1,636 / B=880 / C=1,812(42%)。

★最初は peak_mcap で分けようとして**やめた**。キューの peak が信用できないため
  (tier() の注記参照 — DexScreener突合で中央110倍の水増し)。
  mcapの派生値で分けると、一番壊れたレコードを優先して厚く書くことになる。

★Cのlog記録について: 元のプロンプトは「skipは log に1行」だが、それは1回15件想定。
  1,812件を1行ずつ書くとlogがゴミで埋まるので**1回の実行につき集約1行**にする。
  件数と内訳は残すので追跡はできる。

■ 触らない場所
書き込むのは wiki/entities/tokens/ , wiki/concepts の台帳2つ, wiki/log.md ,
brain/state/synth_queue.json のみ。sources/ と本人の領域は読むだけ。

使い方:
  python3 brain/synthesize_local.py            # 既定バッチ
  SYNTH_BATCH=200 python3 brain/synthesize_local.py
  SYNTH_DRY=1 python3 brain/synthesize_local.py   # 書き込まず件数だけ出す
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "brain" / "state" / "synth_queue.json"
TOKENS = ROOT / "wiki" / "entities" / "tokens"
LOG_MD = ROOT / "wiki" / "log.md"
DEATH_LEDGER = ROOT / "wiki" / "concepts" / "rug-anatomy.md"
BREAK_LEDGER = ROOT / "wiki" / "concepts" / "launchpad-economics.md"
STATE_LOG = ROOT / "brain" / "state" / "synth_local.log"

MODEL = os.environ.get("SYNTH_MODEL_LOCAL", "qwen3:14b")
BATCH = int(os.environ.get("SYNTH_BATCH", "40"))
DRY = os.environ.get("SYNTH_DRY") == "1"
TIMEOUT = int(os.environ.get("SYNTH_LLM_TIMEOUT", "120"))
# 厚く合成する線。実測分布(deaths中央値$2,229 / 90%点$657k)から、
# 「ページを作る価値がある」側に寄せてこの値。
THICK_MCAP = float(os.environ.get("SYNTH_THICK_MCAP", "100000"))
STUB_MCAP = float(os.environ.get("SYNTH_STUB_MCAP", "10000"))
# 処理する層。既定は全部。`SYNTH_TIERS=B` のように絞れる。
# ★用途: B層はLLMを使わない(テンプレのみ)ので、良いモデルの準備を待たずに先に流せる。
#   A層を弱いモデルで流してしまうと、キューから消えて後から作り直せない。
TIERS = set((os.environ.get("SYNTH_TIERS") or "ABC").upper())


def ollama_url() -> str:
    """ollama の待受先。WSLからWindows側のollamaを叩くのが既定。

    ★WSL2のホストIPは再起動で変わるので固定しない(default routeから引く)。
    OLLAMA_URL を明示すればそれを使う。
    """
    if os.environ.get("OLLAMA_URL"):
        return os.environ["OLLAMA_URL"].rstrip("/")
    host = "127.0.0.1"
    try:
        out = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=5).stdout
        m = re.search(r"via (\d+\.\d+\.\d+\.\d+)", out)
        if m:
            host = m.group(1)
    except Exception:
        pass
    return f"http://{host}:11434"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def log(msg: str) -> None:
    line = f"{now_iso()} {msg}"
    print(line)
    try:
        STATE_LOG.parent.mkdir(parents=True, exist_ok=True)
        with STATE_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ── 分類 ───────────────────────────────────────────────────────────────
def metrics_of(item: dict) -> dict:
    return item.get("last") or item.get("metrics") or item.get("now") or {}


def peak_of(item: dict) -> float:
    m = metrics_of(item)
    try:
        return float(item.get("peak_mcap") or m.get("mcap_usd") or 0)
    except (TypeError, ValueError):
        return 0.0


def has_kol(item: dict) -> bool:
    return bool(item.get("kol_ca") or item.get("kol_ticker"))


def real_sol_of(item: dict) -> float:
    try:
        return float(metrics_of(item).get("real_sol") or 0)
    except (TypeError, ValueError):
        return 0.0


def tier(item: dict) -> str:
    """A=LLMで厚く / B=決定的stub / C=entityを作らない。

    ★peak_mcap では分けない(2026-08-30に測って捨てた基準)。
    キューの peak_mcap は**信用できない**。DexScreenerと突き合わせた実測:
      キューpeak ÷ 現在MC = 中央110.8倍 / 75%点556倍 / 最大226,430倍
      $USMS peak $236M〜$643M ← 実際にコールした時のMCは $9.78M(65倍以上の水増し)
      $RST $459,652,932 → 今$2,030 / $WOFI $316,431,221 → 今$2,438
    一瞬の異常なmcap読みが peak として保存されている。
    これを基準にすると **一番壊れたレコードを優先して厚く書く**ことになり、
    しかも $643M を事実として wiki に書き込む。

    → 代わりに**mcap計算の派生でない生の属性**で分ける:
      KOL言及 / tokenized_agent / reply(人が反応した) / social整備 / 実SOL流入。
    これらは収集時点にそのまま入っている値なので、mcapの壊れ方に巻き込まれない。
    """
    m = metrics_of(item)
    tw, web = bool(m.get("twitter")), bool(m.get("website"))
    rep = m.get("reply_count") or 0
    # ★A層をさらに絞った(2026-08-30、実際に60件書かせてから)。
    #   最初は「twitterとwebsiteの両方あり」もA(LLMで厚く)に入れていたが、
    #   出てきた文章が全部これだった:
    #     「◯◯はミームコインとして始まったが、マーケットキャップが◯◯ドルにまで
    #       縮小し、活動の停止を示唆している。SNSでの反応も乏しく…」
    #   銘柄が変わっても中身が変わらない。**区別する情報がそもそも無い**からで、
    #   モデルを替えても解決しない(qwen2.5:14bで確認)。おまけに
    #   「マーケットキャピタルIZATION」のような壊れた語も混ざる。
    #   同じことはテンプレのstubが言えるし、そちらは語が壊れない。
    #   → LLMは**事実に差がある物にだけ使う**: KOL言及 / AIエージェント /
    #      人が反応した(reply>0) / 実SOLが入った(>=20)。
    #   実測: 1,648件 → 366件(内訳 real_sol 361 / KOL 7 / reply 0 / agent 0)。
    #   ★「両方SNSあり」がAを1,282件も膨らませていた = 捨てリンクが多い。
    if has_kol(item) or bool(m.get("tokenized_agent")) or rep > 0 or real_sol_of(item) >= 20:
        return "A"
    if tw or web or real_sol_of(item) > 0:
        return "B"
    return "C"


# ── LLM ────────────────────────────────────────────────────────────────
PROMPT = """あなたは Trench-Brain の合成担当。Solanaのミームコインを1件、**与えられた事実だけ**から短く評価する。

出力は**JSONのみ**。前置き・説明・コードフェンス禁止。形式:
{"synthesis": "<日本語2-4文>", "ledger_note": "<日本語1文>", "concepts": ["..."]}

■ 絶対の規則(破ったら無価値)
- **事実欄と矛盾することを書かない。** twitter/website に URL があるなら
  「SNS未整備」「social無し」とは書けない。null の時だけ未整備と書く
- synthesis と ledger_note が**互いに矛盾しない**こと
- 与えられていない数字・出来事・人物を出さない
- **peak_mcap は未検証**(収集側の異常値が混ざる)。断定に使わず、触れるなら「記録上」と書く
- 「今後が注目される」「可能性がある」だけの文は書かない。**事実か、事実から言えることだけ**

■ synthesis(2-4文)
観測(事実の要約)と判断(そこから言えること)を分ける。情報が薄い銘柄は2文でよい。

■ ledger_note(1文)
台帳の「型」列。**この銘柄について**「死ぬ前/跳ぶ前に何が見えていたか」を日本語の文で書く。
★「値をそのまま並べろ」とは言わない — 一度そう指示したら
  `None → None → mcap枯れ($17) → 型不明` という生の値の羅列を出してきた。
  **文章として**書かせ、分類できなければ "型不明(情報不足)" とだけ書かせる方が良い。
無理に型を作らない。

■ concepts(1-3個・該当するものだけ)
launchpad-economics … 発射台の経済。ほぼ全銘柄に該当する土台
rug-anatomy        … rug/死の解剖。死んだ・抜かれた銘柄
survivor-memes     … **実際に生き残った**ミームだけ。新規/死亡銘柄には付けない
ai-memes           … tokenized_agent が true の時だけ
jp-meme-cluster    … 日本語圏の文脈がある時だけ

事実:
"""

def ask_llm(facts: str, url: str) -> dict | None:
    body = json.dumps(
        {
            "model": MODEL,
            "prompt": PROMPT + facts,
            "stream": False,
            "format": "json",
            # think を切る(qwen3は既定で思考を吐く。合成本文に混ざると台無し)
            "think": False,
            "options": {"temperature": 0.3, "num_predict": 400},
        }
    ).encode("utf-8")
    req = urllib.request.Request(f"{url}/api/generate", data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = json.loads(r.read().decode("utf-8")).get("response", "")
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        log(f"  llm error: {e}")
        return None
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        log("  llm returned non-JSON — 破棄(捏造しない)")
        return None
    s = str(obj.get("synthesis") or "").strip()
    if not s:
        return None
    # frontmatter を壊す行頭 --- と、行を跨ぐ制御を落とす
    s = re.sub(r"^\s*---\s*$", "", s, flags=re.M).replace("\r", " ").replace("\n", " ").strip()
    if len(s) > 700:
        s = s[:699] + "…"
    # ★台帳は markdown の表なので、本文中の | が入ると列がずれて表ごと壊れる
    note = str(obj.get("ledger_note") or "").strip().replace("|", "/")
    note = " ".join(note.split())[:300] or "型不明(情報不足)"
    cons = [c for c in (obj.get("concepts") or []) if isinstance(c, str)]
    allowed = {"launchpad-economics", "rug-anatomy", "survivor-memes", "ai-memes", "jp-meme-cluster"}
    cons = [c for c in cons if c in allowed][:3] or ["launchpad-economics"]
    return {"synthesis": s, "ledger_note": note, "concepts": cons}


# ── entity 書き出し ────────────────────────────────────────────────────
def safe_name(ticker: str, mint: str) -> str:
    base = re.sub(r'[\\/:*?"<>|]', "_", ticker) or "UNKNOWN"
    p = TOKENS / f"{base}.md"
    if p.exists():
        head = p.read_text(encoding="utf-8", errors="ignore")[:800]
        if mint and mint in head:
            return p.name  # 同一銘柄 = 更新
        return f"{base}-{mint[:6]}.md"  # 同名別mint = 衝突回避
    return p.name


def facts_block(item: dict, kind: str) -> str:
    m = metrics_of(item)
    peak = peak_of(item)
    rows = [
        f"ticker: {item.get('ticker')}",
        f"name: {m.get('name')}",
        f"種別: {kind}",
        f"peak_mcap_usd(未検証・収集側の値): {peak:,.0f}",
        f"last_mcap_usd: {(m.get('mcap_usd') or 0):,.0f}",
        f"twitter: {m.get('twitter')}",
        f"website: {m.get('website')}",
        f"reply_count: {m.get('reply_count')}",
        f"tokenized_agent: {m.get('tokenized_agent')}",
        f"gate: {item.get('gate')}",
    ]
    if item.get("cause"):
        rows.append(f"死因(決定的判定): {item['cause']}")
    if item.get("flags"):
        rows.append(f"flags: {','.join(item['flags'])}")
    if has_kol(item):
        rows.append(f"KOL言及: ca={item.get('kol_ca')} ticker={item.get('kol_ticker')}")
    return "\n".join(rows)


def status_for(kind: str, item: dict) -> tuple[str, str]:
    if kind == "death":
        cause = str(item.get("cause") or "")
        return "dead", ("rugged" if "rug" in cause.lower() else "died")
    return "watch", "unknown"


def write_entity(item: dict, kind: str, synthesis: str, concepts: list[str]) -> str:
    m = metrics_of(item)
    ticker = str(item.get("ticker") or "?")
    mint = str(item.get("mint") or "")
    status, outcome = status_for(kind, item)
    fname = safe_name(ticker, mint)
    path = TOKENS / fname
    links = " ".join(f"[[{c}]]" for c in concepts)
    peak = peak_of(item)
    tags = ["token", "pumpfun"]
    if (m.get("reply_count") or 0) == 0:
        tags.append("traction0")
    if m.get("tokenized_agent"):
        tags.append("ai-agent")
    tags.append(status)
    body = f"""---
type: entity
kind: token
source: auto-track
status: {status}
outcome: {outcome}
ticker: {ticker}
mint: {mint}
created: {today()}
updated: {today()}
peak_mcap: {peak}
last_mcap: {m.get('mcap_usd') or 0}
tags: [{', '.join(tags)}]
---

# {ticker}（{m.get('name') or ticker}）

pump.fun発。gate: {item.get('gate') or 'n/a'}。twitter={m.get('twitter') or 'null'} / website={m.get('website') or 'null'} / reply={m.get('reply_count')} / tokenized_agent={m.get('tokenized_agent')}。記録上の peak mcap ${peak:,.2f}(**未検証** — 収集側のmcapは実測比で中央110倍の水増しが確認されている)。

<!-- synthesis:start -->
**観測/判断**: {synthesis}

{links}
<!-- synthesis:end -->

## 関連
{chr(10).join('- [[' + c + ']]' for c in concepts)}
"""
    if not DRY:
        TOKENS.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return fname


def stub_synthesis(item: dict, kind: str) -> str:
    """LLMを呼ばない層の文章。**事実の言い換えだけ**にする(判断を捏造しない)。"""
    m = metrics_of(item)
    peak = peak_of(item)
    social = "SNS未整備" if not (m.get("twitter") or m.get("website")) else "SNSあり"
    trac = "traction(reply)ゼロ" if (m.get("reply_count") or 0) == 0 else f"reply={m.get('reply_count')}"
    # ★peakは断定しない。収集側の値は実測比で中央110倍ずれている(tier()の注記)。
    if kind == "death":
        return f"{social}・{trac}のまま終了({item.get('cause') or '死因未記録'})。記録上のpeakは${peak:,.0f}だが未検証。型通りの死として台帳に1行残す。"
    return f"{social}・{trac}。記録上のpeakは${peak:,.0f}(未検証)。厚く書くだけの情報が無いので薄stubで維持。"


# ── 台帳 ───────────────────────────────────────────────────────────────
def append_ledger(path: Path, marker: str, row: str) -> bool:
    """台帳に1行足す。`<!-- marker -->` があればその直前、無ければ**末尾に追記**。

    ★実物を見てから決めた(2026-08-30): synth_prompt.md は
      「`<!-- death-ledger -->` コメントの直前へ」と書いているが、
      rug-anatomy.md(12,266行)にも launchpad-economics.md にも**そのマーカーは無い**。
      実際の行はファイル末尾に積まれている。仕様の文言ではなく実物に合わせる。
      ★勝手に表やマーカーを新設はしない — 本人の構成を作り変えないため。
    """
    if DRY or not path.exists():
        return False
    txt = path.read_text(encoding="utf-8")
    tag = f"<!-- {marker} -->"
    if tag not in txt:
        sep = "" if txt.endswith("\n") else "\n"
        path.write_text(txt + sep + row.rstrip() + "\n", encoding="utf-8")
        return True
    i = txt.index(tag)
    path.write_text(txt[:i] + row.rstrip() + "\n" + txt[i:], encoding="utf-8")
    return True


def traction_cell(item: dict) -> str:
    """既存台帳の traction 列と同じ書式(reply/KOL/real_sol/social)。"""
    m = metrics_of(item)
    kol = len(item.get("kol_ca") or []) + len(item.get("kol_ticker") or [])
    parts = [f"reply{m.get('reply_count') or 0}", f"KOL{kol}"]
    parts.append(f"real_sol={m.get('real_sol')}" if m.get("real_sol") is not None else "real_sol=?")
    tw, web = m.get("twitter"), m.get("website")
    parts.append("twitter/website null" if not tw and not web else f"twitter={tw or 'null'}・website={web or 'null'}")
    return "・".join(parts)


def death_row(item: dict, note: str) -> str:
    """★既存の死亡台帳と同じ7列に揃える(2026-08-30に実物を読んで合わせた)。
    | [[$TICKER]]（名前） | entry門 | peak | traction | 生存 | cause | 型 |
    最後の「型」列が学習の中身なので、A層ではここもLLMに書かせる。"""
    m = metrics_of(item)
    peak = peak_of(item)
    last = m.get("mcap_usd") or 0
    ratio = f"・peak比{(last / peak - 1) * 100:.1f}%" if peak > 0 else ""
    return "| [[{}]]（{}） | {} | ${:,.2f}（記録上peak・未検証） | {} | auto-track | {}{} | {} |".format(
        item.get("ticker"), m.get("name") or item.get("ticker"), item.get("gate") or "n/a",
        peak, traction_cell(item), item.get("cause") or "?", ratio, note,
    )


def breakout_row(item: dict, note: str) -> str:
    m = metrics_of(item)
    prev = item.get("prev_mcap") or 0
    now = m.get("mcap_usd") or 0
    jump = f"{(now / prev - 1) * 100:+.0f}%" if prev else "?"
    return "| [[{}]]（{}） | {} | ${:,.0f}→${:,.0f} | {} | {} | {} |".format(
        item.get("ticker"), m.get("name") or item.get("ticker"), jump, prev, now,
        traction_cell(item), ",".join(item.get("flags") or []) or "n/a", note,
    )


# ── 本体 ───────────────────────────────────────────────────────────────
LOCK = ROOT / "brain" / "state" / "synth_local.lock"


def acquire_lock() -> bool:
    """多重起動を構造的に拒否する(2026-08-30、実際に踏んでから足した)。

    実障害: 前のバッチが走っている最中に次を起動してしまい、**同じ台帳と同じキューに
    2プロセスが read-modify-write** した。片方の読み込みが書き込み途中のファイルに当たり
    `UnicodeDecodeError: unexpected end of data`。今回は無事だったが、
    条件次第で台帳の行が消え、キューが巻き戻る(= 処理済みが復活する/未処理が消える)。
    ★ファイル1本を丸ごと書き戻す設計なので、同時実行は必ず壊す。
    """
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            pid = int(LOCK.read_text().strip() or 0)
        except (ValueError, OSError):
            pid = 0
        alive = False
        if pid:
            try:
                os.kill(pid, 0)
                alive = True
            except (ProcessLookupError, PermissionError):
                alive = pid and False
        if alive:
            log(f"既に別の合成が走っている(pid={pid}) — 何もしない")
            return False
        log(f"古いロックを掃除して続行(pid={pid} は居ない)")
        try:
            LOCK.unlink()
        except OSError:
            pass
        return acquire_lock()
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    return True


def release_lock() -> None:
    try:
        LOCK.unlink()
    except OSError:
        pass


def main() -> int:
    if not acquire_lock():
        return 0
    if not QUEUE.exists():
        log("queue無し")
        release_lock()
        return 0
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    kinds = [("deaths", "death"), ("changes", "change"), ("births", "birth")]

    counts = {"A": 0, "B": 0, "C": 0}
    for key, _ in kinds:
        for it in q.get(key, []):
            counts[tier(it)] += 1
    log(f"queue: deaths={len(q.get('deaths', []))} changes={len(q.get('changes', []))} births={len(q.get('births', []))} / A={counts['A']} B={counts['B']} C={counts['C']}")

    url = ollama_url()
    done = {"A": 0, "B": 0, "C": 0}
    ledger_hits = 0
    llm_fail = 0
    budget = BATCH

    for key, kind in kinds:
        items = q.get(key, [])
        if not items:
            continue
        # C は LLM を使わないので先に全部さばく(バッチ予算を食わせない)
        keep = []
        for it in items:
            t0 = tier(it)
            if t0 not in TIERS:
                keep.append(it)   # 対象外の層はキューに残す(消さない)
            elif t0 == "C":
                done["C"] += 1
            else:
                keep.append(it)
        # 残りは peak の大きい順 = 情報量の多い順に処理する
        keep.sort(key=peak_of, reverse=True)
        rest = []
        for it in keep:
            if budget <= 0:
                rest.append(it)
                continue
            t = tier(it)
            if t not in TIERS:
                rest.append(it)
                continue
            if t == "A":
                res = ask_llm(facts_block(it, kind), url)
                if res is None:
                    llm_fail += 1
                    # ★失敗を握り潰さない。捏造もしない — stubに落として次サイクルで厚くしない
                    res = {"synthesis": stub_synthesis(it, kind), "ledger_note": "型不明(LLM失敗)", "concepts": ["launchpad-economics"]}
                write_entity(it, kind, res["synthesis"], res["concepts"])
                note = res["ledger_note"]
                done["A"] += 1
            else:
                write_entity(it, kind, stub_synthesis(it, kind), ["launchpad-economics"])
                # B層は型を推定しない(事実だけ)。ここで無理に型を書くと台帳が薄まる
                note = "型通り(薄stub・LLM未使用)"
                done["B"] += 1
            if kind == "death":
                if append_ledger(DEATH_LEDGER, "death-ledger", death_row(it, note)):
                    ledger_hits += 1
            elif kind == "change" and any(f in (it.get("flags") or []) for f in ("BREAKOUT", "GRADUATED")):
                if append_ledger(BREAK_LEDGER, "breakout-ledger", breakout_row(it, note)):
                    ledger_hits += 1
            budget -= 1
        q[key] = rest

    total = done["A"] + done["B"] + done["C"]
    summary = (
        f"- {today()} auto-synthesis(local {MODEL}): 合成{done['A']}件 / stub{done['B']}件 / "
        f"低signalでentity化せず{done['C']}件 / 台帳追記{ledger_hits}行"
        + (f" / LLM失敗{llm_fail}件はstubに降格" if llm_fail else "")
    )
    if not DRY:
        if LOG_MD.exists():
            txt = LOG_MD.read_text(encoding="utf-8")
            lines = txt.split("\n")
            at = 1 if lines and lines[0].startswith("#") else 0
            lines.insert(at, summary)
            LOG_MD.write_text("\n".join(lines), encoding="utf-8")
        tmp = QUEUE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(q, ensure_ascii=False), encoding="utf-8")
        tmp.replace(QUEUE)

    log(f"done: {summary}  (残り deaths={len(q.get('deaths', []))} changes={len(q.get('changes', []))} births={len(q.get('births', []))})")
    release_lock()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        # ★中断(Ctrl-C / kill)でもロックを残さない。残すと次回が永久に止まる。
        release_lock()
