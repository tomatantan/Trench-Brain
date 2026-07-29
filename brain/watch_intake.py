#!/usr/bin/env python3
"""
watch_intake — チーム向け「監視アカウント/ソース投稿口」（承認キュー方式）。

チームが wiki_bot に投げると承認待ちキューに貯まり、運営(OWNER)が承認したものだけ
本監視(watchlist.md=収集の門)に入る。CLAUDE.md 憲法 指針2「門は人が承認」に沿う。

  /watch  @handle [メモ]   … Xアカウントを提案（誰でも可）
  /source <URL>  [メモ]    … ニュース/情報ソースを提案（誰でも可）
  /pending                 … 承認待ち一覧（OWNERのみ）
  /approve <番号|all>      … 承認→本監視入り（OWNERのみ）
  /reject  <番号>          … 却下（OWNERのみ）

キュー: brain/state/watchlist_queue.jsonl（1行1提案・追記のみ・git永続）。
承認された X アカは watchlist.md の「チーム提案（承認済み）」節に行追加＝次サイクルで収集開始。
承認された source は wiki/actions/ingest-queue.md に入れて取り込みパイプラインに乗せる。
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HANDLE_RE = re.compile(r"(?:twitter|x)\.com/([A-Za-z0-9_]{1,15})", re.I)
BARE_HANDLE_RE = re.compile(r"^@?([A-Za-z0-9_]{1,15})$")
URL_RE = re.compile(r"https?://\S+")

WATCHLIST_TEAM_SECTION = "## チーム提案（承認済み・自動追記）"


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _queue_path(root):
    return Path(root) / "brain" / "state" / "watchlist_queue.jsonl"


def _read_queue(root):
    p = _queue_path(root)
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def _write_queue(root, items):
    p = _queue_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in items) + "\n",
                 encoding="utf-8")


def _norm_handle(arg):
    """arg 先頭トークンから @handle を抽出。'@x'・'x'・Xリンク いずれも可。残りはメモ。"""
    arg = arg.strip()
    if not arg:
        return None, ""
    first, _, rest = arg.partition(" ")
    m = HANDLE_RE.search(first)
    if m:
        return m.group(1), rest.strip()
    m = BARE_HANDLE_RE.match(first)
    if m:
        return m.group(1), rest.strip()
    return None, arg  # handle 取れず＝全部メモ扱い(呼び側で弾く)


# ── 提案の追加（誰でも） ─────────────────────────────────────────────

def add_watch(root, arg, sender):
    handle, note = _norm_handle(arg)
    if not handle:
        return "使い方: /watch @handle [メモ]\n例: /watch @blknoiz06 空気読むのが速い", None
    items = _read_queue(root)
    # 既に監視中 or 提案済みの重複を弾く（正直に返す）
    for it in items:
        if it.get("kind") == "x_account" and it.get("value", "").lower() == handle.lower() \
                and it.get("status") == "pending":
            return f"@{handle} は既に承認待ちキューにある（提案者: {it.get('sender','?')}）。", None
    item = {"id": _now().replace(":", "").replace("-", "")[:15], "kind": "x_account",
            "value": handle, "note": note, "sender": sender, "ts": _now(), "status": "pending"}
    items.append(item)
    _write_queue(root, items)
    return (f"✅ @{handle} を承認待ちキューに入れた（提案者: {sender}）。\n"
            f"運営が /approve したら次サイクルから監視開始。"), ["brain/state/watchlist_queue.jsonl"]


def add_source(root, arg, sender):
    m = URL_RE.search(arg or "")
    if not m:
        return "使い方: /source <URL> [メモ]\n例: /source https://example.com/feed RSS", None
    url = m.group(0)
    note = (arg.replace(url, "").strip())
    items = _read_queue(root)
    for it in items:
        if it.get("kind") == "source" and it.get("value") == url and it.get("status") == "pending":
            return f"そのソースは既に承認待ちキューにある（提案者: {it.get('sender','?')}）。", None
    item = {"id": _now().replace(":", "").replace("-", "")[:15], "kind": "source",
            "value": url, "note": note, "sender": sender, "ts": _now(), "status": "pending"}
    items.append(item)
    _write_queue(root, items)
    return (f"✅ ソースを承認待ちキューに入れた（提案者: {sender}）:\n{url}\n"
            f"運営が /approve したら取り込み口に乗る。"), ["brain/state/watchlist_queue.jsonl"]


# ── 承認・却下（OWNERのみ） ──────────────────────────────────────────

def _pending(items):
    return [x for x in items if x.get("status") == "pending"]


def list_pending(root):
    pend = _pending(_read_queue(root))
    if not pend:
        return "承認待ちは無い。"
    lines = ["承認待ち（/approve <番号> か /approve all で承認）:"]
    for i, it in enumerate(pend, 1):
        tag = "X" if it["kind"] == "x_account" else "src"
        val = ("@" + it["value"]) if it["kind"] == "x_account" else it["value"]
        note = f" — {it['note']}" if it.get("note") else ""
        lines.append(f"{i}. [{tag}] {val}{note}（提案: {it.get('sender','?')}）")
    return "\n".join(lines)


def _append_watchlist_row(root, handle, sender, note):
    wl = Path(root) / "watchlist.md"
    text = wl.read_text(encoding="utf-8") if wl.exists() else ""
    if f"[[@{handle}]]" in text:
        return False  # 既に門にいる
    memo = f"提案:{sender}" + (f" / {note}" if note else "")
    row = f"| [[@{handle}]] | — | — | {memo} | 中 |\n"
    if WATCHLIST_TEAM_SECTION in text:
        # 既存のチーム節の末尾（次の見出し直前 or ファイル末尾）に行を差し込む
        idx = text.index(WATCHLIST_TEAM_SECTION)
        after = text[idx:]
        nxt = after.find("\n## ", len(WATCHLIST_TEAM_SECTION))
        if nxt == -1:
            text = text.rstrip() + "\n" + row
        else:
            cut = idx + nxt
            text = text[:cut].rstrip() + "\n" + row + text[cut:]
    else:
        block = (f"\n\n{WATCHLIST_TEAM_SECTION}\n"
                 f"チームが /watch で提案→運営承認で追加。\n"
                 f"| handle | 名前 | followers | メモ | weight |\n"
                 f"|---|---|---|---|---|\n{row}")
        text = text.rstrip() + block + "\n"
    wl.write_text(text, encoding="utf-8")
    return True


def _append_ingest_queue(root, url, sender, note):
    iq = Path(root) / "wiki" / "actions" / "ingest-queue.md"
    iq.parent.mkdir(parents=True, exist_ok=True)
    new = not iq.exists()
    with open(iq, "a", encoding="utf-8") as f:
        if new:
            f.write("---\ntype: actions\ntitle: ingest-queue（質問が駆動する取り込み待ち）\n"
                    "tags: [actions, ingest]\n---\n\n# 取り込み待ち\n\n")
        memo = f" — {note}" if note else ""
        f.write(f"- [{_now()[:10]}] ソース提案（{sender}）: {url}{memo}\n")


def approve(root, arg):
    items = _read_queue(root)
    pend = _pending(items)
    if not pend:
        return "承認待ちは無い。", None
    arg = (arg or "").strip().lower()
    targets = pend if arg == "all" else []
    if not targets:
        if not arg.isdigit():
            return "使い方: /approve <番号> または /approve all（番号は /pending 参照）", None
        n = int(arg)
        if n < 1 or n > len(pend):
            return f"番号は 1〜{len(pend)}。/pending で確認して。", None
        targets = [pend[n - 1]]
    paths = ["brain/state/watchlist_queue.jsonl"]
    msgs = []
    for it in targets:
        if it["kind"] == "x_account":
            added = _append_watchlist_row(root, it["value"], it.get("sender", "?"), it.get("note", ""))
            it["status"] = "approved"
            it["approved_at"] = _now()
            msgs.append(f"✅ @{it['value']} → 監視入り" + ("" if added else "（既に門にいた）"))
            if "watchlist.md" not in paths:
                paths.append("watchlist.md")
        else:
            _append_ingest_queue(root, it["value"], it.get("sender", "?"), it.get("note", ""))
            it["status"] = "approved"
            it["approved_at"] = _now()
            msgs.append(f"✅ ソース → 取り込み口: {it['value']}")
            if "wiki/actions/ingest-queue.md" not in paths:
                paths.append("wiki/actions/ingest-queue.md")
    _write_queue(root, items)
    msgs.append("次サイクルで反映される。")
    return "\n".join(msgs), paths


def reject(root, arg):
    items = _read_queue(root)
    pend = _pending(items)
    arg = (arg or "").strip()
    if not arg.isdigit():
        return "使い方: /reject <番号>（/pending 参照）", None
    n = int(arg)
    if n < 1 or n > len(pend):
        return f"番号は 1〜{len(pend)}。", None
    it = pend[n - 1]
    it["status"] = "rejected"
    it["rejected_at"] = _now()
    _write_queue(root, items)
    val = ("@" + it["value"]) if it["kind"] == "x_account" else it["value"]
    return f"却下した: {val}", ["brain/state/watchlist_queue.jsonl"]
