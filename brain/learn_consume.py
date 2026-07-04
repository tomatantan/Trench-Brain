#!/usr/bin/env python3
"""
learn_consume.py — サーフィンの1タップ学習(brain/state/learn_queue.jsonl)を脳に取り込む(決定的・LLM不使用)。

本人directive(2026-07-04): サーフィン中「これ学習しろ」を1タップ→人が門を通した最強のキュレーション。
ここは軽い決定的層＝キューを消費して以下に振り分ける(重い合成は既存のsynthesize系cronが後で拾う):
  - KOL(@handle) → watchlist.md の「★1タップ学習で追加」節に昇格(=収集の門に入る・人が承認済)。
  - 銘柄(ticker/CA) → brain/state/learn_flags.json に優先フラグ(track.py/合成が優先度に使える)。
  - tweet本文/URL → sources/x に人手ソースとして保存(合成の材料)。
冪等: processed 済みは飛ばす。憲法: 人が明示的に選んだ物だけ=門付き(指針2)。公開に個人閲覧履歴は出さない。
"""
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "brain" / "state" / "learn_queue.jsonl"
FLAGS = ROOT / "brain" / "state" / "learn_flags.json"
WL = ROOT / "wiki" / "watchlist.md"
SRC = ROOT / "sources" / "x"
WL_START = "<!-- learn-added:start -->"
WL_END = "<!-- learn-added:end -->"
HANDLE_RE = re.compile(r"^[a-z0-9_]{2,30}$")


def _load_queue():
    if not QUEUE.exists():
        return []
    out = []
    for ln in QUEUE.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(ln))
        except ValueError:
            continue
    return out


def _existing_watchlist_handles():
    if not WL.exists():
        return set()
    return {h.lower() for h in re.findall(r"\[\[@([A-Za-z0-9_]{2,30})\]\]", WL.read_text(encoding="utf-8"))}


def main():
    items = _load_queue()
    if not items:
        print("learn_consume: キュー空")
        return
    pending = [it for it in items if not it.get("processed")]
    if not pending:
        print("learn_consume: 新規なし")
        return

    flags = {}
    try:
        flags = json.loads(FLAGS.read_text(encoding="utf-8")) if FLAGS.exists() else {}
    except (ValueError, OSError):
        flags = {}

    known = _existing_watchlist_handles()
    new_handles, new_flags, new_src = [], 0, 0
    for it in pending:
        h = (it.get("handle") or "").lower()
        if h and HANDLE_RE.match(h) and h not in known:
            new_handles.append(h)
            known.add(h)
        for tk in filter(None, [it.get("ticker"), it.get("ca")]):
            key = tk.lstrip("$").upper()
            flags[key] = {"flagged_at": it.get("ts"), "via": "surf-learn",
                          "count": (flags.get(key, {}).get("count", 0) + 1)}
            new_flags += 1
        # tweet本文があれば人手ソースとして保存(合成の材料・門は人=このタップ)
        txt = it.get("text") or ""
        if txt and h:
            SRC.mkdir(parents=True, exist_ok=True)
            fn = SRC / f"{h}__learn{it['id'].split('_')[-1]}.md"
            if not fn.exists():
                fn.write_text(
                    f"---\naccount: {h}\nvia: surf-learn\nlikes: 0\nsource: {it.get('url','')}\n---\n{txt}\n",
                    encoding="utf-8")
                new_src += 1
        it["processed"] = True

    # watchlist に「1タップ学習で追加」節を冪等再生成
    if new_handles:
        content = WL.read_text(encoding="utf-8") if WL.exists() else ""
        block_lines = [WL_START,
                       "## ★1タップ学習で追加（サーフィン中に本人が『学習』した＝人が門を通した）",
                       "> 本人がアプリで明示的に選んだアカウント。収集の門に入る。expand_watchlist と別管理で由来が分かる。"]
        # 既存 learn-added 節の handle も保持(冪等)
        prev = []
        if WL_START in content and WL_END in content:
            seg = content.split(WL_START, 1)[1].split(WL_END, 1)[0]
            prev = re.findall(r"\[\[@([A-Za-z0-9_]{2,30})\]\]", seg)
        allh = list(dict.fromkeys([p.lower() for p in prev] + new_handles))
        for h in allh:
            block_lines.append(f"- [[@{h}]] — surf-learn")
        block_lines.append(WL_END)
        block = "\n".join(block_lines)
        if WL_START in content and WL_END in content:
            content = re.sub(re.escape(WL_START) + r".*?" + re.escape(WL_END), block, content, flags=re.S)
        else:
            content = content.rstrip() + "\n\n" + block + "\n"
        WL.write_text(content, encoding="utf-8")

    FLAGS.write_text(json.dumps(flags, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # キュー全体を processed 反映で書き戻し(冪等)
    QUEUE.write_text("\n".join(json.dumps(it, ensure_ascii=False) for it in items) + "\n", encoding="utf-8")
    print(f"learn_consume: 処理{len(pending)}件 → KOL新規{len(new_handles)}(watchlist昇格) / "
          f"銘柄フラグ{new_flags} / ソース保存{new_src}")


if __name__ == "__main__":
    main()
