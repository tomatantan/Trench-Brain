#!/usr/bin/env python3
"""
Trench-Brain collector — 「貯める仕組み」

watchlist のアカウントをポーリングし、新規ツイートを
sources/x/<author>__<tweetID>.md に1枚1ノートで保存する。

取得元(--source):
  syndication … X公式 syndication endpoint(認証不要・無料)。標準ライブラリのみ。
                429されやすいので throttle 必須。
  twitterapi  … twitterapi.io(有償・安定・429なし)。要 TWITTERAPI_KEY(.env or 環境変数)。

翻訳・要約はしない(後段=summary/concept の仕事)。重複はファイル存在で判定。

使い方:
  python3 collector/collect.py                               # syndication 全周
  python3 collector/collect.py --source twitterapi           # twitterapi.io 全周
  python3 collector/collect.py --accounts blknoiz06 --limit 5
  python3 collector/collect.py --dry-run
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WATCHLIST = ROOT / "wiki" / "watchlist.md"
OUT_DIR = ROOT / "sources" / "x"
ENV_FILE = ROOT / ".env"

SYND_URL = "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"
TWAPI_URL = "https://api.twitterapi.io/twitter/user/last_tweets"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  # 最小UA(余計なヘッダは429を招く)
THROTTLE = 4  # アカウント間の待機秒数(syndication向け)

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', re.S
)
HANDLE_RE = re.compile(r"\[\[@([A-Za-z0-9_]{1,15})\]\]")
TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")
MENTION_RE = re.compile(r"@([A-Za-z0-9_]{1,15})\b")


def load_env():
    """.env を環境変数に読み込む(KEY=VALUE 形式、簡易)。"""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


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


def _get(url: str, headers=None, retries: int = 4):
    """429/5xx は指数バックオフでリトライ。"""
    headers = {"User-Agent": UA, **(headers or {})}
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


def parse_created(s: str):
    """'Wed Apr 29 19:04:56 +0000 2026' -> ISO8601(UTC)。"""
    try:
        dt = datetime.strptime(s, "%a %b %d %H:%M:%S %z %Y")
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return s or ""


def normalize_syndication(t: dict):
    return {
        "id": t.get("id_str"),
        "author": (t.get("user") or {}).get("screen_name"),
        "text": html.unescape(t.get("full_text") or ""),
        "created": parse_created(t.get("created_at", "")),
        "likes": t.get("favorite_count") or 0,
        "rts": t.get("retweet_count") or 0,
    }


def normalize_twitterapi(t: dict):
    return {
        "id": t.get("id") or t.get("id_str"),
        "author": (t.get("author") or {}).get("userName"),
        "text": html.unescape(t.get("text") or t.get("full_text") or ""),
        "created": parse_created(t.get("createdAt") or t.get("created_at") or ""),
        "likes": t.get("likeCount") or t.get("favorite_count") or 0,
        "rts": t.get("retweetCount") or t.get("retweet_count") or 0,
    }


def fetch_syndication(handle: str):
    body = _get(SYND_URL.format(handle=handle))
    m = NEXT_DATA_RE.search(body)
    if not m:
        raise ValueError("no __NEXT_DATA__ blob (layout changed?)")
    data = json.loads(m.group(1))
    entries = data["props"]["pageProps"]["timeline"]["entries"]
    out = []
    for e in entries:
        t = (e.get("content") or {}).get("tweet")
        if t and t.get("id_str"):
            out.append(normalize_syndication(t))
    return out


def fetch_twitterapi(handle: str, key: str):
    url = TWAPI_URL + "?" + urllib.parse.urlencode({"userName": handle})
    body = _get(url, headers={"X-API-Key": key})
    data = json.loads(body)
    if data.get("status") == "error":
        raise ValueError(data.get("msg") or data.get("message") or "twitterapi error")
    payload = data.get("data") or {}
    raw = []
    if payload.get("pin_tweet"):
        raw.append(payload["pin_tweet"])
    raw.extend(payload.get("tweets") or [])
    out = []
    for t in raw:
        nt = normalize_twitterapi(t)
        if nt["id"]:
            out.append(nt)
    return out


def yaml_list(items):
    return "[" + ", ".join(items) + "]" if items else "[]"


def build_note(nt: dict, via: str):
    """正規化済みtweet -> (author, id, markdown)。"""
    tid = str(nt["id"])
    author = nt.get("author") or via
    text = nt.get("text") or ""
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
        f"created: {nt.get('created', '')}",
        f"captured: {captured}",
        f"likes: {nt.get('likes', 0)}",
        f"retweets: {nt.get('rts', 0)}",
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
    ap.add_argument("--source", choices=["syndication", "twitterapi"], default="syndication")
    ap.add_argument("--accounts", help="カンマ区切りでwatchlistを上書き")
    ap.add_argument("--limit", type=int, default=0, help="1アカ最大保存数(0=無制限)")
    ap.add_argument("--throttle", type=float, default=THROTTLE, help="アカウント間待機秒")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_env()
    key = os.environ.get("TWITTERAPI_KEY", "")
    if args.source == "twitterapi" and not key:
        print("TWITTERAPI_KEY が未設定(.env か環境変数に入れて)", file=sys.stderr)
        return 1

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
            time.sleep(args.throttle)
        try:
            if args.source == "twitterapi":
                tweets = fetch_twitterapi(h, key)
            else:
                tweets = fetch_syndication(h)
        except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError) as e:
            total_err += 1
            print(f"  ! {h}: fetch failed ({e})")
            continue
        new_here = 0
        for nt in tweets:
            author, tid, note = build_note(nt, via=h)
            path = OUT_DIR / f"{author.lower()}__{tid}.md"
            if path.exists():
                total_skip += 1
                continue
            if not args.dry_run:
                path.write_text(note, encoding="utf-8")
            new_here += 1
            total_new += 1
            if args.limit and new_here >= args.limit:
                break
        print(f"  - @{h}: {new_here} new ({len(tweets)} seen)")

    print(
        f"\n{'[dry-run] ' if args.dry_run else ''}done [{args.source}]: "
        f"{total_new} new, {total_skip} skipped, {total_err} fetch-errors "
        f"across {len(handles)} accounts"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
