#!/usr/bin/env python3
"""
apply_watchlist_approvals.py — UI(/api/approve_watchlist)経由の1タップ承認を
実際にwatchlist.mdへ反映する。LLM不使用・決定的。cron_collect.shから毎サイクル呼ぶ想定。

設計: ui_server.py はローカルに積むだけ(brain/state/watchlist_approvals.jsonl)。
git書き込みはcron側の既存git pull/commit/pushサイクルに乗せる(サーバースレッドから直接gitを叩かない
= COORDINATION.md の書き込みパス分離と同じ発想)。

承認済みhandleは watchlist.md の「UI承認済み(要分類)」節に追記する。カテゴリ/weightは
UI側では分からない(候補は引用グラフから出ただけで人物属性が無い)ので中weightの暫定枠に置き、
人が気が向いたら本体の適切な節へ移動・re-weightできるようにする(嘘の分類をでっち上げない)。
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
WL = ROOT / "watchlist.md"
QUEUE = ROOT / "brain" / "state" / "watchlist_approvals.jsonl"

START = "<!-- ui-approved:start -->"
END = "<!-- ui-approved:end -->"
HANDLE_RE = re.compile(r"\[\[@([A-Za-z0-9_]{2,15})\]\]", re.I)


def load_queue():
    if not QUEUE.exists():
        return []
    items = []
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    return items


def save_queue(items):
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False, separators=(",", ":")) + "\n")


def current_handles(text):
    return {h.lower() for h in HANDLE_RE.findall(text)}


def main():
    items = load_queue()
    pending = [it for it in items if not it.get("processed")]
    if not pending:
        print("apply_watchlist_approvals: 承認待ちなし")
        return

    text = WL.read_text(encoding="utf-8") if WL.exists() else ""
    have = current_handles(text)

    applied = []
    for it in pending:
        h = (it.get("handle") or "").strip().lower()
        if not h or h in have:
            it["processed"] = True  # 既にwatchlist本体にある/handle不正=もう用済み
            continue
        applied.append(h)
        have.add(h)
        it["processed"] = True

    if applied:
        block_re = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        existing = block_re.search(text)
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        rows = []
        if existing:
            # 既存節から行を保持しつつ追記(冪等: 二重追記しない)
            rows = re.findall(r"\|\s*\[\[@[A-Za-z0-9_]+\]\].*", existing.group(0))
        for h in applied:
            rows.append(f"| [[@{h}]] | 中 | UI承認({today})・要分類 |")
        block = "\n".join([
            START,
            "## UI承認済み(要分類・`/api/approve_watchlist` 経由)",
            "expand_watchlist.py の自動拡張候補をUIから1タップ承認したもの。カテゴリ不明のため暫定weight=中。"
            "気が向いたら上の本体節へ移動・再分類してよい。",
            "", "| handle | weight | メモ |", "|---|---|---|",
            *rows, END,
        ])
        if existing:
            text = text[:existing.start()] + block + text[existing.end():]
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
        WL.write_text(text, encoding="utf-8")
        print(f"apply_watchlist_approvals: {len(applied)}件をwatchlist.mdへ追記 ({', '.join('@' + h for h in applied)})")
    else:
        print("apply_watchlist_approvals: 承認待ちはあったが全て処理済み/重複")

    save_queue(items)


if __name__ == "__main__":
    main()
