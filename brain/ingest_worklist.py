#!/usr/bin/env python3
"""
Trench-Brain ingest worklist — 「整理(判断)」を増分・自動化するための仕組み。

LLM Wiki の ingest は本来「新ソースが来る度に、関連entityを更新し、必要な所に
conceptをemergeさせる」工程。5,000件を毎回読むのは非現実的なので、
**前回ingest以降の新ソースだけ**を対象に、エージェントが手を入れるべき箇所を
bounded な worklist にして渡す。これでエージェントの合成が「決まった工程」になる。

★鮮度ゲート(2026-06-23, CLAUDE.md 指針2「門=自動フィルタのコード」/ 本人確認):
  worklist は以前「累積の新規言及数」だけで並べていた＝もう冷えたトークン(数日前に
  話題→今は死)が上位に出る構造バグがあった。合成は"生きた知識"を対象にすべき(LLM Wiki)。
  そこで created 時刻で **HOT / 単一ソース / stale** に三分し、合成対象には
  「①直近48h言及 ②複数アカ横断(単一シラー除外) ③エンゲージ」を満たす HOT だけを上位に出す。
  ＝合成対象の選定を決定的コードで正しくする(LLM不使用＝誤らない)。stale は隠さず件数を明記。

出力: wiki/_worklist.md（エージェントが読むTODO）
状態: brain/state/ingested.txt（synthesis済 tweet_id。追記式）

流れ(brain/INGEST.md 参照):
  collect → digest → build_entities → ingest_worklist → [エージェントが worklist を処理] → mark_ingested
"""
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
CONCEPTS = ROOT / "wiki" / "concepts"
STATE = ROOT / "brain" / "state" / "ingested.txt"
OUT = ROOT / "wiki" / "_worklist.md"

TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")
URL_RE = re.compile(r"https?://\S+")
NOISE_RE = re.compile(r"^(gm+|gn+|lfg+|wagmi|ngmi|wen|soon|ser|fr+|lol+|gg+|\.+)$", re.I)
TOP_ENTITIES = 20   # 1サイクルでエージェントに渡す上限
MIN_ACCOUNTS = 2    # concept候補/HOTのticker閾値(複数アカ横断=単一シラー除外)
MIN_NOTES = 3
HOT_WINDOW_H = 48   # 鮮度窓: created がこの時間内の言及を「今ホット」とみなす


def parse(p):
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return None, ""
    _, fm, body = t.split("---", 2)
    m = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            m[k.strip()] = v.strip()
    return m, body.strip()


def is_noise(m, b):
    if str(m.get("is_retweet", "")).lower() == "true":
        return True
    s = re.sub(r"[@#]\w+", "", URL_RE.sub("", b)).strip()
    return len(s) < 12 or bool(NOISE_RE.match(s.replace(" ", "")))


def to_int(s):
    try:
        return int(s)
    except Exception:
        return 0


def parse_dt(s):
    """'2026-06-22T14:53:26Z' -> aware datetime(UTC)。失敗時 None。"""
    s = (s or "").strip().strip('"')
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None


def load_ingested():
    if STATE.exists():
        return set(STATE.read_text(encoding="utf-8").split())
    return set()


def concept_text():
    txt = ""
    if CONCEPTS.exists():
        for p in CONCEPTS.glob("*.md"):
            txt += p.read_text(encoding="utf-8")
    return txt


def main():
    ingested = load_ingested()
    ctext = concept_text()

    new_tweets = 0
    tk_new = Counter()              # ticker -> 新規言及数(全期間の新規)
    tk_accts = defaultdict(set)     # ticker -> accounts(全体)
    tk_notes = defaultdict(int)
    pl_new = Counter()              # player -> 新規投稿数
    tk_top = defaultdict(list)      # ticker -> [(likes, acct, snippet, fname)] 新規のみ
    tk_recent = defaultdict(list)   # 鮮度: ticker -> [(created_dt, acct)] 新規かつ窓内

    rows = []   # 一旦貯めて ref_now 確定後に集計
    max_dt = None
    for p in SRC.glob("*.md"):
        m, b = parse(p)
        if m is None or is_noise(m, b):
            continue
        tid = m.get("tweet_id", "").strip('"')
        acct = m.get("account", "?")
        via = m.get("via", acct)
        dt = parse_dt(m.get("created"))
        tickers = sorted({t.upper() for t in TICKER_RE.findall(b)})
        rows.append((m, b, tid, acct, via, tickers, tid not in ingested, dt, p.stem))
        if dt and (max_dt is None or dt > max_dt):
            max_dt = dt

    # 「今」基準＝コーパス最新ツイ時刻(機械時計のズレ/収集ラグに頑健)。無ければ wall-clock。
    ref_now = max_dt or datetime.now(timezone.utc)
    hot_cut = ref_now - timedelta(hours=HOT_WINDOW_H)

    for m, b, tid, acct, via, tickers, is_new, dt, stem in rows:
        for tk in tickers:
            tk_accts[tk].add(acct)
            tk_notes[tk] += 1
        if is_new:
            new_tweets += 1
            pl_new[via] += 1
            for tk in tickers:
                tk_new[tk] += 1
                snip = URL_RE.sub("", b).replace("\n", " ")[:80]
                tk_top[tk].append((to_int(m.get("likes")), acct, snip, stem))
                if dt and dt >= hot_cut:
                    tk_recent[tk].append((dt, acct))

    def hot_stats(tk):
        """(48h言及数, 48h内の distinct アカ数)。"""
        rec = tk_recent.get(tk, [])
        return len(rec), len({a for _, a in rec})

    # 鮮度ゲートで三分: HOT(合成対象) / 単一ソース注意 / stale(降格)
    hot, single, stale = [], [], 0
    for tk, n in tk_new.items():
        h48, hacc = hot_stats(tk)
        if h48 == 0:
            stale += 1
            continue
        if hacc >= MIN_ACCOUNTS:
            hot.append((tk, n, h48, hacc))
        else:
            single.append((tk, n, h48, hacc))

    # HOT: 鮮度×横断幅 = h48*hacc を主スコア、総新規をタイブレーク
    hot.sort(key=lambda x: (x[2] * x[3], x[1]), reverse=True)
    single.sort(key=lambda x: (x[2], x[1]), reverse=True)

    def ex_for(tk):
        top = sorted(tk_top[tk], reverse=True)[:2]
        return " / ".join(f"{lk}♥ @{ac}: {sn[:50]}" for lk, ac, sn, _ in top)

    hot_rows = [
        f"| [[{tk}]] | {h48} | {hacc} | {n} | {ex_for(tk)} |"
        for tk, n, h48, hacc in hot[:TOP_ENTITIES]
    ]
    single_rows = [
        f"| [[{tk}]] | {h48} | {hacc} | {n} | {ex_for(tk)} |"
        for tk, n, h48, hacc in single[:10]
    ]

    # concept候補: 閾値超え & 鮮度(48h)生存 & まだどのconceptにも未登場
    cand = []
    for tk, _n, h48, hacc in hot:
        if tk_notes[tk] >= MIN_NOTES and hacc >= MIN_ACCOUNTS and tk not in ctext:
            cand.append(f"- [[{tk}]]（48h {h48}件/{hacc}アカ・総{tk_notes[tk]}）まだconcept無し → 動線/型を検討")

    pl_rows = [f"| [[@{h}]] | {n} |" for h, n in pl_new.most_common(15)]
    today = ref_now.strftime("%Y-%m-%d")

    lines = [
        "---", "type: worklist", "title: ingest worklist", f"updated: {today}", "---", "",
        "# ingest worklist（エージェントが処理するTODO）", "",
        f"前回ingest以降の新シグナルツイ **{new_tweets}件**（基準時刻 {ref_now.strftime('%Y-%m-%dT%H:%MZ')}）。手順は brain/INGEST.md。",
        "★**鮮度ゲート適用済**: 合成対象は下記 §1a（直近48h×複数アカで生きてる物）だけ。",
        f"§1b は単一アカ連投＝要警戒。stale（48h言及ゼロ＝冷えた）**{stale}ティッカーは降格**して非表示。",
        "処理したら合成したページを `python3 brain/mark_ingested.py --from-files <pages>` で消し込む。", "",
        "## 1a) 合成対象＝今ホット（直近48h言及×複数KOL横断・優先順）",
        "各 entity の `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。一次ソースを読む。",
        "", "| entity | 48h言及 | 48hアカ | 総新規 | 新規の代表ツイ |", "|---|---|---|---|---|", *hot_rows, "",
        "## 1b) 単一ソース注意（48hは生きてるが1アカ連投＝シラー依存・低優先/慎重に）",
        "", "| entity | 48h言及 | 48hアカ | 総新規 | 代表ツイ |", "|---|---|---|---|---|",
        *(single_rows or ["| （なし） | | | | |"]), "",
        "## 2) concept 候補（鮮度ゲート通過・閾値超え・まだconcept未登場）",
        "複数アカが今まさに言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。",
        "", *(cand or ["- （なし）"]), "",
        "## 3) 活発になった player（合成メモ更新候補）",
        "", "| player | 新規投稿 |", "|---|---|", *pl_rows, "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"worklist: {new_tweets} new tweets / HOT {len(hot)} (top{len(hot_rows)}) / "
          f"single-source {len(single)} / stale-demoted {stale} / "
          f"concept-cand {len(cand)} -> {OUT.relative_to(ROOT)}  [ref_now={ref_now:%Y-%m-%d %H:%MZ}]")


if __name__ == "__main__":
    main()
