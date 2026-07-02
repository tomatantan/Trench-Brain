#!/usr/bin/env python3
"""
Trench-Brain collector — 「貯める仕組み」($0梯子構造 2026-07-02)

watchlist のアカウントをポーリングし、新規ツイートを
sources/x/<author>__<tweetID>.md に1枚1ノートで保存する。

取得元(--source):
  auto        … ★推奨。無料経路の梯子: syndication → graphql の順に生きてる経路を
                probe で選んで全周する。全滅なら exit 2（=cron/GHA が赤くなり検知できる）。
                有償(twitterapi)には自動では落ちない（$0方針・課金は人間の判断）。
  syndication … X公式 syndication endpoint(認証不要・無料)。標準ライブラリのみ。
                429されやすい（2026-07-02時点: 住宅IPでも429が常態化。probeで生死確認）。
  graphql     … X web内部 GraphQL API(無料)。要 .env: X_AUTH_TOKEN / X_CT0（自分のアカの
                cookie。★捨てアカ推奨=BANリスクあり・メインアカ禁止）。queryId は
                ローテーションで壊れうる→ .env X_QID_USER / X_QID_TWEETS で差し替え可。
  twitterapi  … twitterapi.io(有償・安定・429なし)。要 TWITTERAPI_KEY。梯子の最終手段
                （手動 --source twitterapi でのみ使う。402=クレジット切れは即エラー）。

--tier hot   … watchlist の weight=高 の行だけ回す（負荷/リスクを1/3に。低頻度側は
               別サイクルで --tier all を回す運用）。

毎run後 brain/state/collect_health.json に {ts, backend, new, errors, ...} を記録
＝watchdog / check_conformance が「収集の入口が生きてるか」をここで測る
（2026-06-26〜の twitterapi 402 沈黙が5日半 false-green だった教訓）。

翻訳・要約はしない(後段=summary/concept の仕事)。重複はファイル存在で判定。

使い方:
  python3 collector/collect.py --source auto                 # 梯子で全周(推奨)
  python3 collector/collect.py --probe                       # 各経路の生死だけ確認
  python3 collector/collect.py --source auto --tier hot      # weight=高 だけ
  python3 collector/collect.py --accounts blknoiz06 --limit 5
"""
import argparse
import html
import json
import os
import random
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
STATE_DIR = ROOT / "brain" / "state"
HEALTH_FILE = STATE_DIR / "collect_health.json"
UID_CACHE = STATE_DIR / "x_uid_cache.json"

SYND_URL = "https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}"
TWAPI_URL = "https://api.twitterapi.io/twitter/user/last_tweets"
GQL_URL = "https://x.com/i/api/graphql/{qid}/{op}"
# X web app の公開 bearer（全ブラウザ共通・数年不変）。変わったら .env X_BEARER で上書き。
X_BEARER_DEFAULT = (
    "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs="
    "1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
)
# GraphQL queryId（ローテーションで陳腐化しうる→ .env で差し替え可能にしておく）
QID_USER_DEFAULT = "G3KGOASz96M-Qu0nwmGXNg"     # UserByScreenName
QID_TWEETS_DEFAULT = "V7H0Ap3_Hh2FyS75OCDO3Q"   # UserTweets
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  # 最小UA(余計なヘッダは429を招く)
UA_BROWSER = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
THROTTLE = 4  # アカウント間の待機秒数(free経路向け・実際は±30% jitter)

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


def read_watchlist_handles(path: Path, tier: str = "all"):
    """watchlist.md 内の [[@handle]] を出現順・重複排除で抽出。
    tier='hot' なら weight列(行末セル)に「高」を含むテーブル行だけ＝高signal門。"""
    if not path.exists():
        return []
    seen, out = set(), []
    for line in path.read_text(encoding="utf-8").splitlines():
        if tier == "hot":
            # テーブル行 `| [[@x]] | … | 高 |` のみ対象（プロース中の言及は拾わない）
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or "高" not in cells[-1]:
                continue
        for m in HANDLE_RE.finditer(line):
            h = m.group(1)
            if h.lower() not in seen:
                seen.add(h.lower())
                out.append(h)
    return out


def _get(url: str, headers=None, retries: int = 4, timeout: int = 25):
    """429/5xx は指数バックオフでリトライ。402(Payment)や403は即raise=無駄打ちしない。"""
    headers = {"User-Agent": UA, **(headers or {})}
    delay = 5
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
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


def fetch_syndication(handle: str, retries: int = 4):
    body = _get(SYND_URL.format(handle=handle), retries=retries)
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


# ---------- graphql backend（無料・要cookie・捨てアカ推奨） ----------

def _gql_creds():
    """(auth_token, ct0) を .env/環境変数から。無ければ (None, None)=経路使用不可。"""
    return os.environ.get("X_AUTH_TOKEN") or None, os.environ.get("X_CT0") or None


def _gql_call(op: str, qid: str, variables: dict, features: dict, auth_token: str, ct0: str,
              retries: int = 3):
    """GraphQL GET。400 の 'features cannot be null' は自動補修して再試行
    （queryId/feature はローテーションするので、この自己修復が持続可能性の要）。"""
    feats = dict(features)
    for _ in range(4):  # feature補修ループ(通常1-2周で収束)
        params = urllib.parse.urlencode({
            "variables": json.dumps(variables, separators=(",", ":")),
            "features": json.dumps(feats, separators=(",", ":")),
        })
        url = GQL_URL.format(qid=qid, op=op) + "?" + params
        headers = {
            "User-Agent": UA_BROWSER,
            "Authorization": f"Bearer {os.environ.get('X_BEARER', X_BEARER_DEFAULT)}",
            "Cookie": f"auth_token={auth_token}; ct0={ct0}",
            "x-csrf-token": ct0,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
        }
        try:
            body = _get(url, headers=headers, retries=retries)
            return json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code == 400:
                try:
                    msg = json.loads(e.read().decode("utf-8", "replace"))
                    missing = re.findall(r"Failed to fetch the following features: ([\w, ]+)|"
                                         r"The following features cannot be null: ([\w, ]+)",
                                         json.dumps(msg))
                    names = []
                    for a, b in missing:
                        names += [x.strip() for x in (a or b).split(",") if x.strip()]
                    if names:
                        for n in names:
                            feats[n] = False
                        continue  # 補修して再試行
                except Exception:
                    pass
            raise
    raise ValueError("gql feature auto-repair failed")


def _load_uid_cache():
    try:
        return json.loads(UID_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _gql_user_id(handle: str, auth_token: str, ct0: str, cache: dict):
    if handle.lower() in cache:
        return cache[handle.lower()]
    qid = os.environ.get("X_QID_USER", QID_USER_DEFAULT)
    data = _gql_call("UserByScreenName", qid,
                     {"screen_name": handle, "withSafetyModeUserFields": True},
                     {"hidden_profile_subscriptions_enabled": True,
                      "responsive_web_graphql_exclude_directive_enabled": True,
                      "verified_phone_label_enabled": False,
                      "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                      "responsive_web_graphql_timeline_navigation_enabled": True},
                     auth_token, ct0)
    uid = (((data.get("data") or {}).get("user") or {}).get("result") or {}).get("rest_id")
    if not uid:
        raise ValueError("UserByScreenName: rest_id無し(凍結/改名/queryId陳腐化?)")
    cache[handle.lower()] = uid
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        UID_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return uid


def _scavenge_tweets(node, out):
    """UserTweets応答から legacy tweet を構造非依存で回収（layout drift 耐性）。"""
    if isinstance(node, dict):
        leg = node.get("legacy")
        if (isinstance(leg, dict) and leg.get("full_text") is not None
                and (node.get("rest_id") or leg.get("id_str"))):
            out[str(node.get("rest_id") or leg.get("id_str"))] = leg
        for v in node.values():
            _scavenge_tweets(v, out)
    elif isinstance(node, list):
        for v in node:
            _scavenge_tweets(v, out)


def fetch_graphql(handle: str, auth_token: str, ct0: str, uid_cache: dict):
    uid = _gql_user_id(handle, auth_token, ct0, uid_cache)
    qid = os.environ.get("X_QID_TWEETS", QID_TWEETS_DEFAULT)
    data = _gql_call("UserTweets", qid,
                     {"userId": uid, "count": 40, "includePromotedContent": False,
                      "withQuickPromoteEligibilityTweetFields": False,
                      "withVoice": True, "withV2Timeline": True},
                     {"responsive_web_graphql_exclude_directive_enabled": True,
                      "verified_phone_label_enabled": False,
                      "creator_subscriptions_tweet_preview_api_enabled": True,
                      "responsive_web_graphql_timeline_navigation_enabled": True,
                      "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                      "tweetypie_unmention_optimization_enabled": True,
                      "responsive_web_edit_tweet_api_enabled": True,
                      "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                      "view_counts_everywhere_api_enabled": True,
                      "longform_notetweets_consumption_enabled": True,
                      "responsive_web_twitter_article_tweet_consumption_enabled": False,
                      "tweet_awards_web_tipping_enabled": False,
                      "freedom_of_speech_not_reach_fetch_enabled": True,
                      "standardized_nudges_misinfo": True,
                      "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                      "longform_notetweets_rich_text_read_enabled": True,
                      "longform_notetweets_inline_media_enabled": True,
                      "responsive_web_media_download_video_enabled": False,
                      "responsive_web_enhance_cards_enabled": False},
                     auth_token, ct0)
    found = {}
    _scavenge_tweets(data, found)
    out = []
    for tid, leg in found.items():
        # 他人のツイート(引用先等)が混ざりうる→ user_id_str で自アカ分に絞る
        if str(leg.get("user_id_str") or "") not in ("", str(uid)):
            continue
        out.append({
            "id": tid,
            "author": handle,
            "text": html.unescape(leg.get("full_text") or ""),
            "created": parse_created(leg.get("created_at", "")),
            "likes": leg.get("favorite_count") or 0,
            "rts": leg.get("retweet_count") or 0,
        })
    return out


# ---------- 梯子（$0優先・全滅を隠さない） ----------

FREE_LADDER = ["syndication", "graphql"]


def probe_backends(probe_handle: str, verbose=True):
    """各経路の生死を1アカで確認。{backend: (ok, detail)} を返す。"""
    res = {}
    # syndication: 認証不要。速く諦める(retries=2)
    try:
        n = len(fetch_syndication(probe_handle, retries=2))
        res["syndication"] = (n > 0, f"{n} tweets")
    except Exception as e:
        res["syndication"] = (False, f"{type(e).__name__}: {str(e)[:80]}")
    # graphql: cookie 必須
    at, ct0 = _gql_creds()
    if not at or not ct0:
        res["graphql"] = (False, "cookie未設定(.env X_AUTH_TOKEN/X_CT0)")
    else:
        try:
            n = len(fetch_graphql(probe_handle, at, ct0, _load_uid_cache()))
            res["graphql"] = (n > 0, f"{n} tweets")
        except Exception as e:
            res["graphql"] = (False, f"{type(e).__name__}: {str(e)[:80]}")
    if verbose:
        for k, (ok, d) in res.items():
            print(f"  probe {k}: {'✅' if ok else '✗'} {d}")
    return res


def write_health(backend, new, skipped, errors, accounts):
    """収集の入口の健康を記録＝watchdog/conformance がここで鮮度を測る。"""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        HEALTH_FILE.write_text(json.dumps({
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "backend": backend, "new": new, "skipped": skipped,
            "errors": errors, "accounts": accounts,
            "ok": accounts > 0 and errors < accounts,
        }, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


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
    ap.add_argument("--source", choices=["auto", "syndication", "graphql", "twitterapi"],
                    default="auto")
    ap.add_argument("--tier", choices=["all", "hot"], default="all",
                    help="hot=watchlistのweight高のみ(負荷1/3・高頻度側)")
    ap.add_argument("--accounts", help="カンマ区切りでwatchlistを上書き")
    ap.add_argument("--limit", type=int, default=0, help="1アカ最大保存数(0=無制限)")
    ap.add_argument("--throttle", type=float, default=THROTTLE, help="アカウント間待機秒")
    ap.add_argument("--probe", action="store_true", help="各経路の生死確認のみ(全滅=exit 2)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    load_env()

    handles = (
        [h.strip().lstrip("@") for h in args.accounts.split(",") if h.strip()]
        if args.accounts
        else read_watchlist_handles(WATCHLIST, tier=args.tier)
    )
    if not handles:
        print("no handles found", file=sys.stderr)
        return 1

    if args.probe:
        res = probe_backends(handles[0])
        return 0 if any(ok for ok, _ in res.values()) else 2

    # --- backend 決定（auto=梯子） ---
    source = args.source
    if source == "auto":
        res = probe_backends(handles[0])
        source = next((b for b in FREE_LADDER if res.get(b, (False,))[0]), None)
        if not source:
            # ハイブリッド(C・2026-07-02): 無料が全滅したら、TWITTERAPI_KEY があれば有料に自動fallback
            # ＝定常は$0(free)、無料が死んだ時だけ課金＝実支出最小で収集は止めない(false-green も出さない)。
            if os.environ.get("TWITTERAPI_KEY"):
                source = "twitterapi"
                print("ladder: 無料経路全滅→有料 twitterapi に自動fallback（ハイブリッド保険）", file=sys.stderr)
            else:
                print("★ 無料経路が全滅（syndication/graphql とも死）かつ TWITTERAPI_KEY 無し＝収集不可。\n"
                      "  → graphql は .env X_AUTH_TOKEN/X_CT0(捨てアカcookie) 投入で復活。\n"
                      "  → 有料保険を効かせるなら TWITTERAPI_KEY を設定（残高があれば自動fallback）。",
                      file=sys.stderr)
                write_health("none", 0, 0, len(handles), len(handles))
                return 2
        else:
            print(f"ladder: {source} を使用")

    key = os.environ.get("TWITTERAPI_KEY", "")
    if source == "twitterapi" and not key:
        print("TWITTERAPI_KEY が未設定(.env か環境変数に入れて)", file=sys.stderr)
        return 1
    gql_at, gql_ct0 = _gql_creds()
    if source == "graphql" and (not gql_at or not gql_ct0):
        print("X_AUTH_TOKEN/X_CT0 が未設定(.env に捨てアカのcookieを入れて)", file=sys.stderr)
        return 1
    uid_cache = _load_uid_cache()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_new, total_skip, total_err = 0, 0, 0

    for i, h in enumerate(handles):
        if i > 0:
            # jitter=機械的リズムを崩す(free経路のban/429対策)
            time.sleep(args.throttle * (0.7 + 0.6 * random.random()))
        try:
            if source == "twitterapi":
                tweets = fetch_twitterapi(h, key)
            elif source == "graphql":
                tweets = fetch_graphql(h, gql_at, gql_ct0, uid_cache)
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
        f"\n{'[dry-run] ' if args.dry_run else ''}done [{source}]: "
        f"{total_new} new, {total_skip} skipped, {total_err} fetch-errors "
        f"across {len(handles)} accounts"
    )
    if not args.dry_run:
        write_health(source, total_new, total_skip, total_err, len(handles))
    # 全アカfetch失敗=収集の入口が死んでる→ green を偽装しない(2026-06-26の5日半沈黙の教訓)
    if total_err == len(handles):
        print("★ 全アカウント fetch 失敗＝収集ゼロ。exit 2（silent fail させない）",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
