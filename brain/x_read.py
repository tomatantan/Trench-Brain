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
import os
import re
import sys
import urllib.parse
import urllib.error
import urllib.request

NL = chr(10)

SYND = "https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"
UA = "Mozilla/5.0 (compatible; trench-brain/1.0)"
UA_BROWSER = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
# X web が使っている公開 Bearer(ゲスト用と同じ・秘密ではない)
X_BEARER = os.environ.get("X_BEARER") or (
    "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D"
    "1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA")
# 記事本文は TweetResultByRestId のツイート内に埋まって返る。
# queryId はローテーションするので env で差し替え可能にする(collector/collect.py と同じ思想)。
QID_TWEET = os.environ.get("X_QID_TWEET", "sCU4VpNFPtLj9Cv4GLfYlw")
GQL = "https://x.com/i/api/graphql/{qid}/TweetResultByRestId"


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


def _creds() -> tuple[str | None, str | None]:
    """自分のXアカのcookie。collector/collect.py の graphql 経路と同じものを使う。
    ★捨てアカ推奨(BANリスク) — .env の X_AUTH_TOKEN / X_CT0。"""
    return os.environ.get("X_AUTH_TOKEN") or None, os.environ.get("X_CT0") or None


def _blocks_to_text(content_state: dict) -> str:
    """記事本文(Draft.js風の content_state)を素のテキストに戻す。
    見出しは行頭に # を足して構造を残す。"""
    out: list[str] = []
    for b in content_state.get("blocks") or []:
        t = (b.get("text") or "").rstrip()
        ty = b.get("type") or ""
        if ty.startswith("header"):
            out.append(NL + "## " + t)
        elif ty in ("unordered-list-item", "ordered-list-item"):
            out.append("- " + t)
        else:
            out.append(t)
    return NL.join(out).strip()


def fetch_article(tid: str) -> str | None:
    """ツイートに添付された長文記事の**本文**を取る。要cookie。

    ★cookie無しでは取れないことを実測で確認済み(2026-08-30):
      WebFetch=402 / syndicationはpreview_textまで / Googlebot UA=403 /
      guest token=404 / archive.ph=CAPTCHA。
      X articleは公開クロールに出していない。ログインの内側にしか本文が無い。
    """
    auth, ct0 = _creds()
    if not auth or not ct0:
        return None
    feats = {
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "tweetypie_unmention_optimization_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "responsive_web_enhance_cards_enabled": False,
    }
    variables = {"tweetId": tid, "withCommunity": False,
                 "includePromotedContent": False, "withVoice": False}
    for _ in range(4):  # feature自動補修(collect.py と同じ — queryId/featureは腐る)
        q = urllib.parse.urlencode({
            "variables": json.dumps(variables, separators=(",", ":")),
            "features": json.dumps(feats, separators=(",", ":")),
        })
        req = urllib.request.Request(GQL.format(qid=QID_TWEET) + "?" + q, headers={
            "User-Agent": UA_BROWSER,
            "Authorization": f"Bearer {X_BEARER}",
            "Cookie": f"auth_token={auth}; ct0={ct0}",
            "x-csrf-token": ct0,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
        })
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 400:
                try:
                    msg = e.read().decode("utf-8", "replace")
                    names = re.findall(r"following features cannot be null: ([\w, ]+)", msg)
                    names += re.findall(r"Failed to fetch the following features: ([\w, ]+)", msg)
                    got = [x.strip() for n in names for x in n.split(",") if x.strip()]
                    if got:
                        for n in got:
                            feats[n] = False
                        continue
                except Exception:
                    pass
            print(f"記事の取得に失敗: HTTP {e.code}", file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
            print(f"記事の取得に失敗: {e}", file=sys.stderr)
            return None
        # article は tweet_results.result.article.article_results.result に入る
        node = d
        for k in ("data", "tweetResult", "result"):
            node = (node or {}).get(k) or {}
        art = ((node.get("article") or {}).get("article_results") or {}).get("result") or {}
        cs = art.get("content_state")
        if isinstance(cs, str):
            try:
                cs = json.loads(cs)
            except json.JSONDecodeError:
                cs = None
        if isinstance(cs, dict):
            title = art.get("title") or ""
            body = _blocks_to_text(cs)
            return ((f"# {title}" + NL + NL + body) if title else body) or None
        return None
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
        out += ["", "── 添付の長文記事 ──", f"タイトル: {art.get('title')}"]
        full = fetch_article(str(d.get("id_str") or ""))
        if full:
            out += ["", full]
        else:
            auth, ct0 = _creds()
            out += [
                f"冒頭: {art.get('preview_text')}",
                "",
                ("★本文が取れなかった(cookieはあるが応答に本文が無い。queryIdが腐った可能性 → X_QID_TWEET を差し替え)"
                 if (auth and ct0) else
                 "★本文はログインの内側。.env に X_AUTH_TOKEN / X_CT0(捨てアカのcookie)を入れれば本文まで取れる。"),
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
