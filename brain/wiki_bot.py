#!/usr/bin/env python3
"""
Trench-Brain Q&A bot — グループ会話インターフェース（対話脳 + 取り込み）。

コマンドにだけ反応（privacy mode ON 推奨＝雑談無視）:
  /wiki <問い>   … 対話脳(ask.sh)が wiki横断で答える（§Query）
  /add  <input>  … Twitter URL / 記事URL / テキスト を sources/ に取り込む（人がcurateする門＝指針2/§6）→ commit→ cron の合成engineが料理

設計:
  - **専用 bot トークン**（個人チャンネルと別）＝getUpdates の 1トークン1ポーラー衝突を回避（切断の元を踏まない）。
  - ask.sh は --strict-mcp-config（telegram MCP を起動しない）。bot自身は Bot API を直叩き（MCP不使用）。
  - stdlib のみ（urllib）。

トークン: 環境変数 TG_WIKI_BOT_TOKEN（.env でも可）。
起動: TG_WIKI_BOT_TOKEN=xxxx python3 brain/wiki_bot.py
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = ROOT / ".env"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
TWEET_RE = re.compile(r"https?://(?:www\.)?(?:twitter|x)\.com/([A-Za-z0-9_]+)/status/(\d+)")
URL_RE = re.compile(r"https?://\S+")


def load_token():
    t = os.environ.get("TG_WIKI_BOT_TOKEN", "")
    if not t and ENV.exists():
        for line in ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith("TG_WIKI_BOT_TOKEN="):
                t = line.split("=", 1)[1].strip().strip('"').strip("'")
    return t


TOKEN = load_token()
API = f"https://api.telegram.org/bot{TOKEN}"


def _get(url, data=None, timeout=40):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def send(chat_id, text):
    """4096字制限で分割送信。"""
    for i in range(0, len(text), 3800):
        chunk = text[i:i + 3800]
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": chunk}).encode()
        try:
            _get(f"{API}/sendMessage", data=data, timeout=20)
        except Exception as e:
            print(f"send error: {e}", file=sys.stderr)


def fetch_html(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=20
    ).read().decode("utf-8", "replace")


def git_commit_push(paths, msg):
    """新ソースを commit→pull --rebase --autostash→push（cloud GHA と分岐しても壊れない）。"""
    try:
        subprocess.run(["git", "-C", str(ROOT), "add", *paths], check=False)
        subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-m", msg], check=False)
        subprocess.run(["git", "-C", str(ROOT), "pull", "-q", "--rebase", "--autostash",
                        "origin", "main"], check=False)
        subprocess.run(["git", "-C", str(ROOT), "push", "-q", "origin", "main"], check=False)
    except Exception as e:
        print(f"git error: {e}", file=sys.stderr)


def add_tweet(handle, tid):
    """単一ツイートを oEmbed(無認証) で取得して sources/x へ。"""
    o = _get("https://publish.twitter.com/oembed?" +
             urllib.parse.urlencode({"url": f"https://x.com/{handle}/status/{tid}", "omit_script": "1"}))
    html = o.get("html", "")
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    author = o.get("author_name", handle)
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    p = ROOT / "sources" / "x" / f"{handle}__{tid}.md"
    if p.exists():
        return f"既出（既に sources/x にある）: @{handle}/{tid}"
    fm = ["---", "type: source", "platform: x", f"account: {handle}", "via: /add",
          f'tweet_id: "{tid}"', f"url: https://x.com/{handle}/status/{tid}",
          f"captured: {captured}", "tags: [trench, source, x, manual-add]", "---", "",
          text, ""]
    p.write_text("\n".join(fm), encoding="utf-8")
    git_commit_push([f"sources/x/{handle}__{tid}.md"], f"/add tweet @{handle}/{tid}")
    return f"✅ 取り込んだ: @{author} のツイート → sources/x。次サイクルで合成される。"


def add_url(url):
    """記事URLを取得して sources/news へ。"""
    try:
        html = fetch_html(url)
    except Exception as e:
        return f"⚠️ 取得失敗: {type(e).__name__}"
    tm = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    title = re.sub(r"\s+", " ", (tm.group(1) if tm else url)).strip()[:120]
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body).strip()[:6000]
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    slug = re.sub(r"[^a-z0-9]+", "-", (host + "-" + title.lower()))[:60].strip("-")
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    p = ROOT / "sources" / "news" / f"{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = ["---", "type: source", "platform: web", f"source: {url}", f"title: {title}",
          f"captured: {captured}", "tags: [trench, source, news, manual-add]", "---", "",
          f"# {title}", "", f"> {url}", "", body, ""]
    p.write_text("\n".join(fm), encoding="utf-8")
    git_commit_push([f"sources/news/{slug}.md"], f"/add url {host}")
    return f"✅ 取り込んだ: {title[:50]}… → sources/news。次サイクルで合成される。"


def add_text(text):
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    stamp = captured.replace(":", "").replace("-", "")
    p = ROOT / "sources" / "figures" / f"clip-{stamp}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    fm = ["---", "type: source", "platform: clip", "via: /add",
          f"captured: {captured}", "tags: [trench, source, clip, manual-add]", "---", "",
          text, ""]
    p.write_text("\n".join(fm), encoding="utf-8")
    git_commit_push([f"sources/figures/clip-{stamp}.md"], "/add text clip")
    return "✅ 取り込んだ: テキスト → sources/figures。次サイクルで合成される。"


def handle_add(chat_id, arg):
    arg = arg.strip()
    if not arg:
        send(chat_id, "使い方: /add <Twitter URL / 記事URL / テキスト>"); return
    m = TWEET_RE.search(arg)
    if m:
        send(chat_id, "取り込み中…(tweet)")
        send(chat_id, add_tweet(m.group(1), m.group(2))); return
    um = URL_RE.search(arg)
    if um:
        send(chat_id, "取り込み中…(url)")
        send(chat_id, add_url(um.group(0))); return
    send(chat_id, add_text(arg))


def assetize_query(q, ans):
    """★憲法§Query: 価値ある回答を wiki/queries/ に資産化＋「薄い→要ingest」を ingest-queue へ。
    write-only(git永続はcronに委譲=race回避)。＝問うほど wiki が育つ複利ループ。"""
    if not ans or ans.startswith("⚠️") or ans.startswith("(回答が空"):
        return
    captured = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date = captured[:10]
    slug = re.sub(r"[^a-z0-9ぁ-んァ-ヶ一-龠ー]+", "-", q.lower())[:40].strip("-") or "query"
    p = ROOT / "wiki" / "queries" / f"{date}-{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    body = ["---", "type: query", f"title: {q[:80]}", f"created: {date}",
            f"asked: {captured}", "via: /wiki", "tags: [trench, query]", "---", "",
            "## 問い", q, "", "## 回答（/wiki 6レンズ横断合成）", ans, ""]
    p.write_text("\n".join(body), encoding="utf-8")
    # 「薄い/未カバー/要ingest」gap → ingest-queue(質問が取り込みを駆動)
    gaps = [l.strip("- ").strip() for l in ans.splitlines()
            if any(k in l for k in ("薄い", "要ingest", "未カバー", "未ingest", "未収録"))]
    if gaps:
        iq = ROOT / "wiki" / "actions" / "ingest-queue.md"
        iq.parent.mkdir(parents=True, exist_ok=True)
        new = not iq.exists()
        with open(iq, "a", encoding="utf-8") as f:
            if new:
                f.write("---\ntype: actions\ntitle: ingest-queue（質問が駆動する取り込み待ち）\n"
                        "tags: [actions, ingest]\n---\n\n# 取り込み待ち（/wiki が『薄い』と言った gap）\n\n")
            f.write(f"- [{date}] 問い「{q[:50]}」→ {(' / '.join(gaps))[:200]}\n")


def handle_wiki(chat_id, q):
    q = q.strip()
    if not q:
        send(chat_id, "使い方: /wiki <trench の問い>"); return
    send(chat_id, "🧠 考え中…(wiki横断)")
    try:
        out = subprocess.run(["bash", str(ROOT / "brain" / "ask.sh"), q],
                             capture_output=True, text=True, timeout=300)
        ans = (out.stdout or "").strip() or "(回答が空。質問を変えてみて)"
    except subprocess.TimeoutExpired:
        ans = "⚠️ タイムアウト。質問を絞って再試行を。"
    send(chat_id, ans)
    try:
        assetize_query(q, ans)  # §Query: 資産化(問うほど育つ)
    except Exception as e:
        print(f"assetize err: {type(e).__name__}: {e}", file=sys.stderr, flush=True)


def parse_cmd(text):
    """'/wiki@bot 質問' → ('wiki','質問')。コマンドでなければ (None,None)。"""
    text = text.strip()
    if not text.startswith("/"):
        return None, None
    head, _, rest = text.partition(" ")
    cmd = head[1:].split("@", 1)[0].lower()
    return cmd, rest


def download_file(file_id):
    """Telegram getFile→ローカルDL。sources/media/ に保存しパスを返す。"""
    info = _get(f"{API}/getFile?file_id={file_id}", timeout=20)
    fp = (info.get("result") or {}).get("file_path")
    if not fp:
        return None
    ext = os.path.splitext(fp)[1] or ".jpg"
    dest = ROOT / "sources" / "media" / f"{file_id[:24]}{ext}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://api.telegram.org/file/bot{TOKEN}/{fp}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
        f.write(r.read())
    return str(dest)


def handle_photo(chat_id, file_id, caption):
    """画像ミーム/スクショを vision で取り込む(brainが"見る")。"""
    send(chat_id, "🖼 取り込み中…(画像をvisionで読む)")
    try:
        path = download_file(file_id)
        if not path:
            send(chat_id, "⚠️ 画像DL失敗"); return
        out = subprocess.run(["bash", str(ROOT / "brain" / "ingest_image.sh"), path, caption or ""],
                             capture_output=True, text=True, timeout=300)
        rel = os.path.relpath(path, str(ROOT))
        git_commit_push([rel, "sources/x"], "/add image (vision ingest)")
        msg = (out.stdout or "").strip().splitlines()
        line = next((l for l in reversed(msg) if l.startswith("INGESTED")), (msg[-1] if msg else "取り込んだ"))
        send(chat_id, f"✅ {line}")
    except subprocess.TimeoutExpired:
        send(chat_id, "⚠️ vision合成タイムアウト")
    except Exception as e:
        send(chat_id, f"⚠️ 画像取り込みエラー: {type(e).__name__}")


def main():
    if not TOKEN:
        print("TG_WIKI_BOT_TOKEN 未設定。BotFatherの2個目トークンを環境変数か .env に。", file=sys.stderr)
        return 1
    print("wiki_bot 起動。/wiki /add /画像 に反応。", file=sys.stderr)
    offset = 0
    while True:
        try:
            r = _get(f"{API}/getUpdates?offset={offset}&timeout=30", timeout=40)
        except Exception as e:
            print(f"poll error: {e}", file=sys.stderr); time.sleep(5); continue
        for upd in r.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or upd.get("channel_post") or {}
            chat_id = (msg.get("chat") or {}).get("id")
            if chat_id is None:
                continue
            # 画像(photo or 画像document)→ vision取り込み(bareでも=送った=取り込み意図)
            photo = msg.get("photo") or []
            doc = msg.get("document") or {}
            cap = msg.get("caption", "")
            if photo:
                print(f"recv photo from {chat_id}", file=sys.stderr, flush=True)
                try:
                    handle_photo(chat_id, photo[-1]["file_id"], cap)  # 最大サイズ
                except Exception as e:
                    print(f"photo err: {e}", file=sys.stderr, flush=True)
                continue
            if doc and str(doc.get("mime_type", "")).startswith("image/"):
                try:
                    handle_photo(chat_id, doc["file_id"], cap)
                except Exception as e:
                    print(f"doc img err: {e}", file=sys.stderr, flush=True)
                continue
            text = msg.get("text", "")
            if not text:
                continue
            cmd, arg = parse_cmd(text)
            if cmd in ("wiki", "add", "start", "help"):
                print(f"recv /{cmd} from {chat_id}: {arg[:60]!r}", file=sys.stderr, flush=True)
            try:
                if cmd == "wiki":
                    handle_wiki(chat_id, arg)
                elif cmd == "add":
                    handle_add(chat_id, arg)
                elif cmd == "start" or cmd == "help":
                    send(chat_id, "Trench-Brain bot\n/wiki <問い> = wiki横断で答える\n/add <URL/テキスト> = 取り込む\n画像を送る = ミームをvisionで取り込む")
            except Exception as e:
                print(f"handler error: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
                try:
                    send(chat_id, f"⚠️ エラー: {type(e).__name__}")
                except Exception:
                    pass


if __name__ == "__main__":
    sys.exit(main())
