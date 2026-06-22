#!/usr/bin/env python3
"""
Trench-Brain ingest worklist — 「整理(判断)」を増分・自動化するための仕組み。

LLM Wiki の ingest は本来「新ソースが来る度に、関連entityを更新し、必要な所に
conceptをemergeさせる」工程。5,000件を毎回読むのは非現実的なので、
**前回ingest以降の新ソースだけ**を対象に、エージェントが手を入れるべき箇所を
bounded な worklist にして渡す。これでエージェントの合成が「決まった工程」になる。

出力: wiki/_worklist.md（エージェントが読むTODO）
状態: brain/state/ingested.txt（synthesis済 tweet_id。追記式）

流れ(brain/INGEST.md 参照):
  collect → digest → build_entities → ingest_worklist → [エージェントが worklist を処理] → mark_ingested
"""
import re
from collections import Counter, defaultdict
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
MIN_ACCOUNTS = 2    # concept候補のticker閾値
MIN_NOTES = 3


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
    tk_new = Counter()              # ticker -> 新規言及数
    tk_accts = defaultdict(set)     # ticker -> accounts(全体)
    tk_notes = defaultdict(int)
    pl_new = Counter()              # player -> 新規投稿数
    tk_top = defaultdict(list)      # ticker -> [(likes, acct, snippet, fname)] 新規のみ

    for p in SRC.glob("*.md"):
        m, b = parse(p)
        if m is None or is_noise(m, b):
            continue
        tid = m.get("tweet_id", "").strip('"')
        acct = m.get("account", "?")
        via = m.get("via", acct)
        tickers = sorted({t.upper() for t in TICKER_RE.findall(b)})
        for tk in tickers:
            tk_accts[tk].add(acct)
            tk_notes[tk] += 1
        is_new = tid not in ingested
        if is_new:
            new_tweets += 1
            pl_new[via] += 1
            for tk in tickers:
                tk_new[tk] += 1
                snip = URL_RE.sub("", b).replace("\n", " ")[:80]
                tk_top[tk].append((to_int(m.get("likes")), acct, snip, p.stem))

    # entity worklist: 新規シグナルが付いたentityを優先度順
    ent_rows = []
    for tk, n in tk_new.most_common(TOP_ENTITIES):
        top = sorted(tk_top[tk], reverse=True)[:2]
        ex = " / ".join(f"{lk}♥ @{ac}: {sn[:50]}" for lk, ac, sn, _ in top)
        ent_rows.append(f"| [[{tk}]] | {n} | {len(tk_accts[tk])} | {ex} |")

    # concept候補: 閾値超え & まだどのconceptにも出てこないticker
    cand = []
    for tk in sorted(tk_new, key=lambda t: -tk_new[t]):
        if tk_notes[tk] >= MIN_NOTES and len(tk_accts[tk]) >= MIN_ACCOUNTS:
            if tk not in ctext:  # 既存conceptに未登場
                cand.append(f"- [[{tk}]]（{tk_notes[tk]}件/{len(tk_accts[tk])}アカ）まだconcept無し → 動線/型を検討")

    pl_rows = [f"| [[@{h}]] | {n} |" for h, n in pl_new.most_common(15)]

    lines = [
        "---", "type: worklist", "title: ingest worklist", "updated: 2026-06-22", "---", "",
        "# ingest worklist（エージェントが処理するTODO）", "",
        f"前回ingest以降の新シグナルツイ **{new_tweets}件**。手順は brain/INGEST.md。",
        "処理したら `python3 brain/mark_ingested.py` で消し込む。", "",
        "## 1) 合成メモを更新すべき entity（新シグナル順 top20）",
        "各 entity ページを開き `<!-- synthesis -->` に物語/動線/⚠️矛盾/賭け仮説を追記・改訂。",
        "", "| entity | 新規言及 | 総アカ | 新規の代表ツイ |", "|---|---|---|---|", *ent_rows, "",
        "## 2) concept 候補（閾値超え・まだconcept未登場）",
        "下記は複数アカが言及し始めたのにconceptが無い＝emerge候補。動線/型が立つか判断し、立つなら concept を新規/更新。",
        "", *(cand or ["- （なし）"]), "",
        "## 3) 活発になった player（合成メモ更新候補）",
        "", "| player | 新規投稿 |", "|---|---|", *pl_rows, "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"worklist: {new_tweets} new tweets, "
          f"{len(ent_rows)} entities, {len(cand)} concept candidates -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
