#!/usr/bin/env python3
"""x_read.py — X(Twitter)のURLを1本読む(2026-08-30)。

■ なぜ
「このツイート読める?」に毎回 curl を組み立てて答えていた。使い捨てにせず道具にする。

■ 読める / 読めない(実測)
  ツイート本文        ○ syndication(cdn.syndication.twimg.com)で全文取れる。認証不要
  引用元・添付の情報  ○ 同上
  x.com/i/article/…   ✕ **ログインの内側**。タイトルと冒頭(preview_text)までしか出ない
                        WebFetch=402 / r.jina.ai=Xのエラーページ、も確認済み
★X APIの読み取りは使わない(「X APIはポスト用途のみ」の方針)。ここは公開の
  syndication エンドポイントだけを叩く。

使い方:
  python3 brain/x_read.py https://x.com/user/status/123...
  python3 brain/x_read.py 123...            # IDだけでも可
  python3 brain/x_read.py <url> --json      # 生のまま
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request

SYND = "https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"
UA = "Mozilla/5.0 (compatible; trench-brain/1.0)"


def tweet_id(s: str) -> str | None:
    s = s.strip()
    if s.isdigit():
        return s
    m = re.search(r"/status(?:es)?/(\d+)", s)
    if m:
        return m.group(1)
    m = re.search(r"/i/article/(\d+)", s)
    if m:
        return m.group(1)  # 記事IDでも一応投げる(本文は返らない)
    return None


def fetch(tid: str) -> dict | None:
    req = urllib.request.Request(SYND.format(id=tid), headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        print(f"取得できなかった: {e}", file=sys.stderr)
        return None


def render(d: dict) -> str:
    u = d.get("user") or {}
    out = [
        f"@{u.get('screen_name')}（{u.get('name')}）{'✔' if u.get('is_blue_verified') else ''}",
        f"{d.get('created_at', '')}  ♥{d.get('favorite_count', 0)} / 返信{d.get('conversation_count', 0)}",
        "",
        (d.get("text") or "").strip(),
    ]
    art = d.get("article") or {}
    if art:
        out += [
            "",
            "── 添付の長文記事 ──",
            f"タイトル: {art.get('title')}",
            f"冒頭: {art.get('preview_text')}",
            "★本文はログインの内側で取得不可(preview_textまで)。読むなら本文をコピペしてもらう。",
        ]
    q = d.get("quoted_tweet") or {}
    if q:
        qu = q.get("user") or {}
        out += ["", f"── 引用元 @{qu.get('screen_name')} ──", (q.get("text") or "").strip()]
    media = [m.get("expanded_url") or m.get("url") for m in (d.get("mediaDetails") or [])]
    if media:
        out += ["", "メディア: " + ", ".join(str(m) for m in media if m)]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    tid = tweet_id(a.url)
    if not tid:
        print("URLからツイートIDが取れない", file=sys.stderr)
        return 2
    d = fetch(tid)
    if not d:
        return 1
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
    else:
        print(render(d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
