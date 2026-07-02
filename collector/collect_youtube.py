#!/usr/bin/env python3
"""
Trench-Brain YouTube/Podcast collector — 長文ソース(transcript)の「貯める仕組み」。

門 [[feeds]](wiki/feeds.md の [[@handle]] か channel_id)を巡回し、各チャンネルの新規動画の
**字幕(transcript)** を sources/youtube/<channel>__<videoId>.md に1本1ノートで保存する。
crypto podcast の大半は YouTube にも上がる＝これで podcast も大半カバー(音声onlyのみ別途)。

設計(芯=LLM Wikiの実現を保つ):
- **門付き**(指針2): feeds.md に載るチャンネルだけ。無差別取得しない。
- **volume制御**: 1チャンネル最大 --limit 本/回(既定2)。transcriptは長い＝合成が追い越されない様に絞る。
  合成は brain/synthesize_longform.sh が新規transcriptを N本/サイクルで deep 合成(別工程)。
- 重複はファイル存在で判定。翻訳/要約はしない(後段=合成の仕事)。

依存: 標準ライブラリ(RSS/handle解決) + youtube-transcript-api(字幕)。
  ※ yt-dlp/whisper は不要。YouTube ASR字幕は timedtext 直叩き/yt-dlp では PO token で弾かれるが、
    youtube-transcript-api は取得できる(2026-06-23 実証)。壊れたら此処を差し替える。

使い方:
  python3 collector/collect_youtube.py                 # feeds.md 全チャンネル巡回
  python3 collector/collect_youtube.py --limit 1        # 各1本だけ
  python3 collector/collect_youtube.py --channels @Bankless
  python3 collector/collect_youtube.py --dry-run
"""
import argparse
import html
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEEDS = ROOT / "wiki" / "feeds.md"
OUT_DIR = ROOT / "sources" / "youtube"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
THROTTLE = 3

HANDLE_RE = re.compile(r"\[\[@([A-Za-z0-9_.-]+)\]\]")
CHANNELID_RE = re.compile(r"\b(UC[\w-]{20,})\b")
EXTID_RE = re.compile(r'"externalId":"(UC[\w-]+)"')
VID_RE = re.compile(r"<yt:videoId>([\w-]+)</yt:videoId>")
ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.S)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
PUB_RE = re.compile(r"<published>(.*?)</published>")
TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")
NAME_RE = re.compile(r'"name":"(.*?)"')


def _get(url, retries=3):
    headers = {"User-Agent": UA}
    delay = 4
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(delay); delay *= 2; continue
            raise
    raise urllib.error.URLError("retries exhausted")


def read_feeds(path):
    """feeds.md から [[@handle]] と channel_id(UC...) を出現順・重複排除で。"""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    # コメント/候補節は除外したい場合もあるが、ここでは「## 取り込み対象」以降のみ採用
    if "## 取り込み対象" in text:
        text = text.split("## 取り込み対象", 1)[1].split("## ", 1)[0]
    seen, out = set(), []
    for m in HANDLE_RE.finditer(text):
        h = "@" + m.group(1)
        if h.lower() not in seen:
            seen.add(h.lower()); out.append(h)
    for m in CHANNELID_RE.finditer(text):
        if m.group(1) not in seen:
            seen.add(m.group(1)); out.append(m.group(1))
    return out


def resolve_channel(ref):
    """@handle or UC... -> (channel_id, channel_name)。"""
    if ref.startswith("UC"):
        return ref, ref
    handle = ref.lstrip("@")
    page = _get(f"https://www.youtube.com/@{handle}/videos")
    cid = EXTID_RE.search(page)
    name = NAME_RE.search(page)
    return (cid.group(1) if cid else None,
            html.unescape(name.group(1)) if name else handle)


def fetch_transcript(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    t = api.fetch(video_id)
    return " ".join(s.text for s in t)


def build_note(channel, ch_handle, vid, title, published, transcript):
    url = f"https://www.youtube.com/watch?v={vid}"
    tickers = sorted(set(TICKER_RE.findall(transcript)), key=str.lower)
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    words = len(transcript.split())
    fm = [
        "---", "type: source", "platform: youtube", "kind: transcript",
        f"channel: {channel}", f"channel_handle: {ch_handle}",
        f'video_id: "{vid}"', f"url: {url}",
        f"title: {title}", f"published: {published}", f"captured: {captured}",
        f"words: {words}", f"tickers: [{', '.join(tickers)}]",
        "synthesized: false",   # synthesize_longform が true にする(消し込み)
        "tags: [trench, source, youtube, transcript]", "---", "",
        f"# {title}", "", f"> {url} / {channel} / {published} / {words}語", "",
        transcript.strip(), "",
    ]
    return "\n".join(fm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channels", help="カンマ区切りで feeds を上書き(@handle/UC...)")
    ap.add_argument("--limit", type=int, default=2, help="1チャンネル最大保存数(volume門)")
    ap.add_argument("--throttle", type=float, default=THROTTLE)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    refs = ([c.strip() for c in args.channels.split(",") if c.strip()]
            if args.channels else read_feeds(FEEDS))
    if not refs:
        print("no feeds (wiki/feeds.md の ## 取り込み対象 に [[@handle]] を)", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_new = total_skip = total_err = 0
    done_cids = set()   # 同一チャンネルを @handle と UC で二重に処理しない

    for i, ref in enumerate(refs):
        if i > 0:
            time.sleep(args.throttle)
        try:
            cid, cname = resolve_channel(ref)
            if not cid:
                print(f"  ! {ref}: channel_id 解決失敗"); total_err += 1; continue
            if cid in done_cids:
                continue
            done_cids.add(cid)
            rss = _get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")
        except Exception as e:
            print(f"  ! {ref}: feed失敗 ({type(e).__name__})"); total_err += 1; continue

        new_here = 0
        for entry in ENTRY_RE.findall(rss):
            vm = VID_RE.search(entry)
            if not vm:
                continue
            vid = vm.group(1)
            path = OUT_DIR / f"{cid}__{vid}.md"
            if path.exists():
                total_skip += 1; continue
            tm = TITLE_RE.search(entry); pm = PUB_RE.search(entry)
            title = html.unescape(tm.group(1).strip()) if tm else vid
            published = pm.group(1)[:10] if pm else ""
            try:
                transcript = fetch_transcript(vid)
            except Exception as e:
                print(f"  - {ref} {vid}: transcript無し/失敗 ({type(e).__name__})")
                total_err += 1; continue
            if len(transcript.split()) < 50:
                continue
            if not args.dry_run:
                path.write_text(build_note(cname, ref, vid, title, published, transcript),
                                encoding="utf-8")
            new_here += 1; total_new += 1
            if new_here >= args.limit:
                break
            time.sleep(1)
        print(f"  - {ref} ({cname}): {new_here} new transcript")

    print(f"\n{'[dry-run] ' if args.dry_run else ''}done [youtube]: "
          f"{total_new} new, {total_skip} skipped, {total_err} errors / {len(refs)} channels")
    # 全channel失敗=収集の入口が死んでる→緑を偽装しない(2026-07-02 M3・collect.py と同教訓)
    if refs and total_err == len(refs):
        print("★ 全channel fetch失敗＝収集ゼロ。exit 2", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
