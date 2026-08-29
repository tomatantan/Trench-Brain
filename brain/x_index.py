#!/usr/bin/env python3
"""x_index.py — sources/x に貯まったツイートを**読める**ようにする索引(2026-08-30)。

■ なぜ作るか
`sources/x` に **93,374件**のツイートが .md で貯まっているのに、
retrieval(brain/rag.py)は `wiki/` しか見ていない。
= 集めているだけで、検索も閲覧も一切できない状態だった。

■ 方式: SQLite FTS5(依存ゼロ)
93k件・約370MB を毎回grepするのは重いので全文検索索引を作る。
Python標準の sqlite3 に FTS5 が入っている(検証済み)ので**新しい依存を足さない**。
mtimeで差分更新するので、2回目以降は数秒。

■ 触らないもの
`sources/x` は**読むだけ**。索引は brain/state/x_index.db に作る(生成物)。
本文はファイルが正、索引は複製。壊れたら消して作り直せばいい。

使い方:
  python3 brain/x_index.py build          差分更新(初回は全件)
  python3 brain/x_index.py build --full   作り直し
  python3 brain/x_index.py search "みたい語" [-n 20] [--account xxx]
  python3 brain/x_index.py stats
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
DB = ROOT / "brain" / "state" / "x_index.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS docs(
  path TEXT PRIMARY KEY,
  account TEXT, tweet_id TEXT, url TEXT,
  created TEXT, captured TEXT,
  likes INTEGER DEFAULT 0, retweets INTEGER DEFAULT 0,
  is_retweet INTEGER DEFAULT 0,
  tickers TEXT DEFAULT '', mentions TEXT DEFAULT '',
  body TEXT, mtime REAL
);
CREATE INDEX IF NOT EXISTS idx_docs_created ON docs(created DESC);
CREATE INDEX IF NOT EXISTS idx_docs_account ON docs(account);
CREATE INDEX IF NOT EXISTS idx_docs_likes ON docs(likes DESC);
CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(
  body, account, tickers, content='docs', content_rowid='rowid', tokenize='unicode61'
);
"""

FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)


def parse(p: Path) -> dict | None:
    """frontmatter + 本文。壊れたファイルは None(捏造しない・件数には出す)。"""
    try:
        raw = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = FM.match(raw)
    if not m:
        return None
    meta: dict[str, str] = {}
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")

    def lst(key: str) -> str:
        v = meta.get(key, "")
        return " ".join(re.findall(r"[A-Za-z0-9_$]+", v))

    def num(key: str) -> int:
        try:
            return int(float(meta.get(key, "0") or 0))
        except ValueError:
            return 0

    return {
        "path": str(p.relative_to(ROOT)),
        "account": meta.get("account", ""),
        "tweet_id": meta.get("tweet_id", ""),
        "url": meta.get("url", ""),
        "created": meta.get("created", ""),
        "captured": meta.get("captured", ""),
        "likes": num("likes"),
        "retweets": num("retweets"),
        "is_retweet": 1 if meta.get("is_retweet", "").lower() == "true" else 0,
        "tickers": lst("tickers"),
        "mentions": lst("mentions"),
        "body": m.group(2).strip(),
        "mtime": p.stat().st_mtime,
    }


def connect() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB)
    c.executescript(SCHEMA)
    return c


def build(full: bool = False) -> None:
    c = connect()
    if full:
        c.executescript("DROP TABLE IF EXISTS fts; DROP TABLE IF EXISTS docs;")
        c.executescript(SCHEMA)
    known = {r[0]: r[1] for r in c.execute("SELECT path, mtime FROM docs")}
    added = updated = broken = 0
    batch: list[dict] = []

    def flush() -> None:
        if not batch:
            return
        c.executemany(
            """INSERT INTO docs(path,account,tweet_id,url,created,captured,likes,retweets,is_retweet,tickers,mentions,body,mtime)
               VALUES(:path,:account,:tweet_id,:url,:created,:captured,:likes,:retweets,:is_retweet,:tickers,:mentions,:body,:mtime)
               ON CONFLICT(path) DO UPDATE SET
                 account=excluded.account, likes=excluded.likes, retweets=excluded.retweets,
                 body=excluded.body, mtime=excluded.mtime""",
            batch,
        )
        c.commit()
        batch.clear()

    for p in SRC.glob("*.md"):
        rel = str(p.relative_to(ROOT))
        try:
            mt = p.stat().st_mtime
        except OSError:
            continue
        if rel in known:
            if known[rel] and abs(known[rel] - mt) < 1e-6:
                continue
            updated += 1
        else:
            added += 1
        d = parse(p)
        if d is None:
            broken += 1
            continue
        batch.append(d)
        if len(batch) >= 2000:
            flush()
    flush()
    # FTSは content= 連動なので作り直しが一番安全(93k件で数秒)
    c.executescript("INSERT INTO fts(fts) VALUES('rebuild');")
    c.commit()
    n = c.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    print(f"index: {n}件 (新規{added} / 更新{updated} / 壊れて読めない{broken})")
    c.close()


def search(q: str, n: int = 20, account: str | None = None, ticker: str | None = None) -> list[dict]:
    c = connect()
    out: list[dict] = []
    where, args = [], []
    if account:
        where.append("d.account = ?")
        args.append(account)
    if ticker:
        where.append("d.tickers LIKE ?")
        args.append(f"%{ticker.lstrip('$')}%")
    cond = (" AND " + " AND ".join(where)) if where else ""
    if q:
        # FTS5の演算子文字は落とす(ユーザーの入力をクエリ構文として解釈させない)
        safe = re.sub(r'["\*\(\)\:\^]', " ", q).strip()
        if not safe:
            return []
        sql = f"""SELECT d.path,d.account,d.url,d.created,d.likes,d.retweets,d.tickers,d.body
                  FROM fts JOIN docs d ON d.rowid = fts.rowid
                  WHERE fts MATCH ?{cond}
                  ORDER BY bm25(fts) LIMIT ?"""
        rows = c.execute(sql, [safe, *args, n]).fetchall()
    else:
        sql = f"""SELECT d.path,d.account,d.url,d.created,d.likes,d.retweets,d.tickers,d.body
                  FROM docs d WHERE 1=1{cond} ORDER BY d.created DESC LIMIT ?"""
        rows = c.execute(sql, [*args, n]).fetchall()
    for r in rows:
        out.append({
            "path": r[0], "account": r[1], "url": r[2], "created": r[3],
            "likes": r[4], "retweets": r[5], "tickers": r[6],
            "body": r[7][:1200],
        })
    c.close()
    return out


def stats() -> dict:
    c = connect()
    n = c.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    accounts = c.execute("SELECT COUNT(DISTINCT account) FROM docs").fetchone()[0]
    newest = c.execute("SELECT MAX(created) FROM docs").fetchone()[0]
    oldest = c.execute("SELECT MIN(created) FROM docs WHERE created != ''").fetchone()[0]
    top = c.execute("SELECT account, COUNT(*) n FROM docs GROUP BY account ORDER BY n DESC LIMIT 10").fetchall()
    c.close()
    return {"tweets": n, "accounts": accounts, "newest": newest, "oldest": oldest,
            "top_accounts": [{"account": a, "n": k} for a, k in top]}


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--full", action="store_true")
    s = sub.add_parser("search"); s.add_argument("q"); s.add_argument("-n", type=int, default=20)
    s.add_argument("--account"); s.add_argument("--ticker")
    sub.add_parser("stats")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.full)
    elif a.cmd == "search":
        for r in search(a.q, a.n, a.account, a.ticker):
            print(f"[{r['created'][:10]}] @{r['account']} ♥{r['likes']}  {r['url']}")
            print("   " + r["body"][:180].replace("\n", " "))
    else:
        print(json.dumps(stats(), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
