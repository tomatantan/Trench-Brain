#!/usr/bin/env python3
"""
Trench-Brain collector — 「貯める仕組み」v1

watchlist のアカウントを X 公式 syndication endpoint(認証不要・無料)でポーリングし、
新規ツイートを sources/x/<author>__<tweetID>.md に1枚1ノートで保存する。

- 外部API・キー不要。標準ライブラリのみ(GitHub Actions でも pip install 不要)。
- 重複判定はファイル存在で行う(状態ファイル不要)。
- 翻訳・要約はしない(それは後段のエージェント=summary/concept の仕事)。

使い方:
  python3 collector/collect.py                 # watchlist 全周
  python3 collector/collect.py --accounts blknoiz06,Ministerr --limit 5
  python3 collector/collect.py --dry-run
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCHLIST = ROOT / "wiki" / "watchlist.md"
OUT_DIR = ROOT / "sources" / "x"

SYND_URL = "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
THROTTLE = 4  # アカウント間の待機秒数

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S
)
HANDLE_RE = re.compile(r"\[\[@([A-Za-z0-9_]{1,15})\]\]")
TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")
MENTION_RE = re.compile(r"@([A-Za-z0-9_]{1,15})\b")


def read_watchlist_handles(path: Path):
    """watchlist.md 内の [[@handle]] を出現順・重複排除で抽出。"""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    seen, out = set(), []
    for m in HANDLE_RE.finditer(text):
        h = m.group(1)
        if h.lower() not in seen:
            seen.add(h.lower())
            out.append(h)
    return out


def _get(url: str, retries: int = 4):
    """429/5xx は指数バックオフでリトライ。"""
    headers = {"User-Agent": UA}
    delay = 5
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise urllib.error.URLError("retries exhausted")


def fetch_timeline(handle: str):
    """syndication から1アカ分の生tweetオブジェクト列を返す。失敗時は例外。"""
    body = _get(SYND_URL.format(handle=handle))
    m = NEXT_DATA_RE.search(body)
    if not m:
        raise ValueError("no __NEXT_DATA__ blob (layout changed?)")
    data = json.loads(m.group(1))
    entries = data["props"]["pageProps"]["timeline"]["entries"]
    tweets = []
    for e in entries:
        t = (e.get("content") or {}).get("tweet")
        if t and t.get("id_str"):
            tweets.append(t)
    return tweets


def parse_created(s: str):
    """'Wed Apr 29 19:04:56 +0000 2026' -> ISO8601(UTC)."""
    try:
        dt = datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return s or ""


def yaml_list(items):
    return "[" + ", ".join(items) + "]" if items else "[]"


def build_note(t: dict, via: str) -> tuple:
    """tweetオブジェクト -> (author, id, markdown文字列)。"""
    tid = t["id_str"]
    author = (t.get("user") or {}).get("screen_name") or via
    text = html.unescape(t.get("full_text") or "")
    created = parse_created(t.get("created_at", ""))
    likes = t.get("favorite_count", 0)
    rts = t.get("retweet_count", 0)
    url = f"https://x.com/{author}/status/{tid}"
    is_rt = text.startswith("RT @")

    tickers = sorted(set(TICKER_RE.findall(text)), key=str.lower)
    mentions = sorted({"@" + h for h in MENTION_RE.findall(text)}, key=str.lower)
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    fm = [
        "---",
        "type: source",
        "platform: x",
        f"account: {author}",
        f"via: {via}",
        f'tweet_id: "{tid}"',
        f"url: {url}",
        f"created: {created}",
        f"captured: {captured}",
        f"likes: {likes}",
        f"retweets: {rts}",
        f"is_retweet: {str(is_rt).lower()}",
        f"tickers: {yaml_list(tickers)}",
        f"mentions: {yaml_list(mentions)}",
        "tags: [trench, source, x]",
        "---",
        "",
        text.strip(),
        "",
    ]
    return author, tid, "\n".join(fm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--accounts", help="カンマ区切りでwatchlistを上書き")
    ap.add_argument("--limit", type=int, default=0, help="1アカ最大保存数(0=無制限)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    handles = (
        [h.strip().lstrip("@") for h in args.accounts.split(",") if h.strip()]
        if args.accounts
        else read_watchlist_handles(WATCHLIST)
    )
    if not handles:
        print("no handles found", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_new, total_skip, total_err = 0, 0, 0

    for i, h in enumerate(handles):
        if i > 0:
            time.sleep(THROTTLE)  # IP単位レート制限を避ける
        try:
            tweets = fetch_timeline(h)
        except (urllib.error.URLError, ValueError, KeyError) as e:
            total_err += 1
            print(f"  ! {h}: fetch failed ({e})")
            continue
        new_here = 0
        for t in tweets:
            author, tid, note = build_note(t, via=h)
            path = OUT_DIR / f"{author}__{tid}.md"
            if path.exists():
                total_skip += 1
                continue
            if args.dry_run:
                new_here += 1
                total_new += 1
                continue
            path.write_text(note, encoding="utf-8")
            new_here += 1
            total_new += 1
            if args.limit and new_here >= args.limit:
                break
        print(f"  - @{h}: {new_here} new ({len(tweets)} seen)")

    print(
        f"\n{'[dry-run] ' if args.dry_run else ''}done: "
        f"{total_new} new, {total_skip} skipped, {total_err} fetch-errors "
        f"across {len(handles)} accounts"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
