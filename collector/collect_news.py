#!/usr/bin/env python3
"""
Trench-Brain news collector — 「無差別収集+ワンクッション(篩)」($0・決定的・2026-07-30)

★経緯(必読): 2026-06-22 に一度「門なしニュース収集エンジン」を作って firehose だからという
理由で本人指示により削除した(CLAUDE.md 指針1 例外条項に記録あり)。今回は同じ轍を踏まないため、
**収集元は無差別に広く(本人指示2026-07-30「無差別でいいよ」)だが、sources/news に採用する前に
必ず1段階のフィルタ(=ワンクッション)を通す**。フィルタを通らなかった分は保存すらしない
(観測≠採用・brain/track.py の pump.fun全mint観測と同じ設計)。

取得元: 主要crypto媒体のRSS(認証不要・無料・stdlibのみ)を横断的にポーリング。
  CoinDesk / Cointelegraph / Decrypt / The Block / CryptoSlate / BeInCrypto /
  U.Today / NewsBTC / Blockworks / DailyHodl

ワンクッション(フィルタ・全て決定的・LLM不使用):
  1. 既出URL/guidは除外(brain/state/news_seen.json)
  2. タイトルが短すぎる/宣伝っぽいパターン(sponsored/advertorial/promoted/press release等)は除外
  3. 同一runで既に採った記事とタイトルが酷似(複数媒体が同じ通信社ネタを転載)なら1本に間引く

採用された分だけ sources/news/<outlet>__<hash>.md に保存(1記事1ファイル・sources/x と同じ設計)。
本文は記事URLから実際に fetch した全文(タグ除去・~6000字)＝RSSのdescriptionだけでなく
brain/wiki_bot.py の /add url と同じ質のテキストを保存する。

使い方:
  python3 collector/collect_news.py                 # 全feed巡回・採用分を保存
  python3 collector/collect_news.py --probe          # 各feedの生死だけ確認(保存しない)
  python3 collector/collect_news.py --limit 30       # 1回の採用上限(既定30)
"""
import argparse
import difflib
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sources" / "news"
SEEN = ROOT / "brain" / "state" / "news_seen.json"
HEALTH = ROOT / "brain" / "state" / "collect_health_news.json"

UA = "Mozilla/5.0 (compatible; trench-brain-collector/1.0)"

FEEDS = [
    ("coindesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("cointelegraph", "https://cointelegraph.com/rss"),
    ("decrypt", "https://decrypt.co/feed"),
    ("theblock", "https://www.theblock.co/rss.xml"),
    ("cryptoslate", "https://cryptoslate.com/feed/"),
    ("beincrypto", "https://beincrypto.com/feed/"),
    ("utoday", "https://u.today/rss"),
    ("newsbtc", "https://www.newsbtc.com/feed/"),
    ("blockworks", "https://blockworks.co/feed"),
    ("dailyhodl", "https://dailyhodl.com/feed/"),
]

JUNK_TITLE_RE = re.compile(
    r"\b(sponsored|advertorial|promoted|press release|partner content|paid content)\b", re.I
)


def fetch(url, timeout=15, _redirected=False):
    """一部媒体(coindesk/blockworks)が307/308で恒久リダイレクトする(urllib既定では未追従)ので
    Location を1回だけ手動で追う。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        return urllib.request.urlopen(req, timeout=timeout).read()
    except urllib.error.HTTPError as e:
        if e.code in (307, 308) and not _redirected and e.headers.get("Location"):
            loc = urllib.parse.urljoin(url, e.headers["Location"])
            return fetch(loc, timeout=timeout, _redirected=True)
        raise


def load_seen():
    if SEEN.exists():
        return set(json.loads(SEEN.read_text(encoding="utf-8")))
    return set()


def save_seen(seen):
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    SEEN.write_text(json.dumps(sorted(seen)), encoding="utf-8")


ATOM_NS = "{http://www.w3.org/2005/Atom}"


def parse_feed(xml_bytes):
    """RSS 2.0 <item> と Atom <entry> の両方に対応。壊れたXMLは空リストで継続。"""
    items = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return items
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link).strip()
        pub = (item.findtext("pubDate") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "guid": guid, "pub": pub})
    for entry in root.iter(f"{ATOM_NS}entry"):
        title = (entry.findtext(f"{ATOM_NS}title") or "").strip()
        link = ""
        for l in entry.findall(f"{ATOM_NS}link"):
            if l.get("rel") in (None, "alternate") and l.get("href"):
                link = l.get("href")
                break
        guid = (entry.findtext(f"{ATOM_NS}id") or link).strip()
        pub = (entry.findtext(f"{ATOM_NS}updated") or entry.findtext(f"{ATOM_NS}published") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "guid": guid, "pub": pub})
    return items


def is_junk_title(title):
    return bool(JUNK_TITLE_RE.search(title)) or len(title) < 12


def norm_title(title):
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


def too_similar(a, b, threshold=0.86):
    return difflib.SequenceMatcher(None, a, b).ratio() >= threshold


def article_text(url, max_chars=6000):
    html = fetch(url).decode("utf-8", "replace")
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body).strip()
    return body[:max_chars]


def slug_for(outlet, link):
    h = hashlib.sha1(link.encode("utf-8")).hexdigest()[:12]
    return f"{outlet}__{h}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--limit", type=int, default=30)
    args = ap.parse_args()

    if args.probe:
        ok = 0
        for name, url in FEEDS:
            try:
                items = parse_feed(fetch(url))
                print(f"  probe {name}: ✅ {len(items)} items")
                ok += 1
            except Exception as e:
                print(f"  probe {name}: ✗ {type(e).__name__}")
        sys.exit(0 if ok else 2)

    seen = load_seen()
    kept_titles = []  # このrunで採用したタイトル(酷似間引き用)
    saved = 0
    fetched_total = 0
    errors = 0

    for name, feed_url in FEEDS:
        try:
            items = parse_feed(fetch(feed_url))
        except Exception:
            errors += 1
            continue
        fetched_total += len(items)
        for it in items:
            if saved >= args.limit:
                break
            if it["guid"] in seen or it["link"] in seen:
                continue
            if is_junk_title(it["title"]):
                seen.add(it["guid"])
                continue
            nt = norm_title(it["title"])
            if any(too_similar(nt, kt) for kt in kept_titles):
                seen.add(it["guid"])  # 他媒体の重複ネタ=間引き(既出扱いにして再チェックしない)
                continue
            try:
                body = article_text(it["link"])
            except Exception:
                errors += 1
                continue
            if len(body) < 200:  # 本文が薄すぎる(paywall/取得失敗)は不採用
                seen.add(it["guid"])
                continue
            slug = slug_for(name, it["link"])
            p = OUT / f"{slug}.md"
            if p.exists():
                seen.add(it["guid"])
                continue
            captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            fm = ["---", "type: source", "platform: web", f"outlet: {name}",
                  f"source: {it['link']}", f"title: {it['title'][:200]}",
                  f"published: {it['pub']}", f"captured: {captured}",
                  "tags: [trench, source, news, auto-collect]", "---", "",
                  f"# {it['title']}", "", f"> {it['link']}", "", body, ""]
            OUT.mkdir(parents=True, exist_ok=True)
            p.write_text("\n".join(fm), encoding="utf-8")
            seen.add(it["guid"])
            kept_titles.append(nt)
            saved += 1
            time.sleep(0.3)  # 各媒体への負荷配慮

    save_seen(seen)
    HEALTH.parent.mkdir(parents=True, exist_ok=True)
    HEALTH.write_text(json.dumps({
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetched": fetched_total, "saved": saved, "errors": errors,
    }), encoding="utf-8")
    print(f"news collect: fetched {fetched_total} / saved {saved} (filtered {fetched_total - saved}) / errors {errors}")


if __name__ == "__main__":
    main()
