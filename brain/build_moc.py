#!/usr/bin/env python3
"""
brain/build_moc.py — wiki/index.md を「自動生成 Master Index / MOC (map of content)」として
毎サイクル再生成する。stdlib のみ・network/LLM不使用・決定的。

CLAUDE.md 指針1(仕様は実際に照合する)への対応: 手書き index.md は必ず腐る
(例: 「tokens 51件/players 120件」と書いてあるが実数は917/154だった)。
被リンク数(inbound wikilink count)を機械的に数え、知識グラフの中心(=概念の背骨)を
自動で並べ直すことで、二度と手書きで腐らない中心ハブにする。

出力: wiki/index.md を上書き。既存の手書き内容は捨てる(腐っているため)。
運用ナビ(watchlist/canon/_worklist)だけは静的節として必ず保持する。
"""
import os
import re
from collections import Counter
from datetime import datetime, timezone

BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BRAIN_DIR)
WIKI_ROOT = os.path.join(REPO_ROOT, "wiki")
INDEX_PATH = os.path.join(WIKI_ROOT, "index.md")

# wiki/ui/ と wiki/_templates/ は走査対象から除外(UI実装物・雛形であり知識ページではない)。
EXCLUDE_DIR_NAMES = {"ui", "_templates"}

# [[stem]] / [[stem|表示]] / [[stem#heading]] の stem を取る(表示名・見出し参照は無視)。
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
# sources/x 由来の生ソース参照 `name__digits` は概念/エンティティページではないので inbound から除外。
SRC_REF_RE = re.compile(r"__\d+$")


def classify(relpath):
    """パスから kind を判定する。"""
    parts = relpath.split(os.sep)
    if "concepts" in parts:
        return "concept"
    if "entities" in parts and "players" in parts:
        return "player"
    if "entities" in parts and "tokens" in parts:
        return "token"
    if "queries" in parts:
        return "query"
    if "dashboards" in parts:
        return "dashboard"
    if "summaries" in parts:
        return "summary"
    return "other"


def parse_title(text, stem):
    """frontmatter の title:(無ければ ticker:)を取り出す。両方無ければ stem を使う。"""
    if not text.startswith("---"):
        return stem
    end = text.find("\n---", 3)
    if end == -1:
        return stem
    fm = text[3:end]
    title = None
    ticker = None
    for line in fm.splitlines():
        line = line.strip()
        m = re.match(r"^title:\s*(.*)$", line)
        if m:
            title = m.group(1).strip()
            continue
        m = re.match(r"^ticker:\s*(.*)$", line)
        if m:
            ticker = m.group(1).strip()
    val = title or ticker or stem
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
        val = val[1:-1]
    return val or stem


def collect_pages():
    pages = []
    for dirpath, dirnames, filenames in os.walk(WIKI_ROOT):
        dirnames[:] = [
            d for d in dirnames
            if d not in EXCLUDE_DIR_NAMES and not d.startswith(".")
        ]
        rel_dir = os.path.relpath(dirpath, WIKI_ROOT)
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            relpath = fn if rel_dir == "." else os.path.join(rel_dir, fn)
            full = os.path.join(dirpath, fn)
            stem = fn[:-3]
            kind = classify(relpath)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                text = ""
            pages.append({
                "stem": stem,
                "kind": kind,
                "title": parse_title(text, stem),
                "relpath": relpath,
                "text": text,
            })
    return pages


def extract_link_targets(text):
    targets = []
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1).strip()
        if "|" in target:
            target = target.split("|", 1)[0].strip()
        target = target.strip()
        if not target or SRC_REF_RE.search(target):
            continue
        targets.append(target)
    return targets


def compute_inbound_counts(pages):
    """全stemについて、小文字照合で被リンク数(=リンクしてくる distinct ページ数)を数える。
    同一ページ内で同じ stem を複数回リンクしても1と数える(重複貼りで水増ししない)。
    """
    lower_to_stem = {}
    for p in pages:
        lower_to_stem.setdefault(p["stem"].lower(), p["stem"])
    counts = Counter()
    for p in pages:
        targets_in_page = {t.lower() for t in extract_link_targets(p["text"])}
        for target_lower in targets_in_page:
            canon = lower_to_stem.get(target_lower)
            if canon is not None:
                counts[canon] += 1
    return counts


def link(stem):
    return "[[%s]]" % stem


def build_index_text(pages, counts):
    concepts = [p for p in pages if p["kind"] == "concept"]
    dashboards = [p for p in pages if p["kind"] == "dashboard"]
    queries = [p for p in pages if p["kind"] == "query"]
    tokens = [p for p in pages if p["kind"] == "token"]
    players = [p for p in pages if p["kind"] == "player"]
    summaries = [p for p in pages if p["kind"] == "summary"]

    by_inbound = lambda p: (-counts.get(p["stem"], 0), p["stem"].lower())
    concepts_sorted = sorted(concepts, key=by_inbound)
    tokens_sorted = sorted(tokens, key=by_inbound)
    players_sorted = sorted(players, key=by_inbound)
    dashboards_sorted = sorted(dashboards, key=lambda p: p["stem"].lower())
    # queries/summaries: ファイル名降順(=新しい順。ファイル名が日付先頭のため)。
    queries_sorted = sorted(queries, key=lambda p: p["stem"], reverse=True)
    summaries_sorted = sorted(summaries, key=lambda p: p["stem"], reverse=True)

    lines = []
    lines.append("---")
    lines.append("type: config")
    lines.append("title: Index — Trench-Brain Master Index (MOC)")
    lines.append("updated: auto")
    lines.append("tags: [trench, index, moc, auto-generated]")
    lines.append("---")
    lines.append("")
    lines.append("> 自動生成(brain/build_moc.py)。手で編集しても次サイクルで上書きされる。")
    lines.append("")
    lines.append("## 運用（config）")
    lines.append("- [[watchlist]] — 監視アカウント watchlist（収集の入口）")
    lines.append("- [[canon]] — 古典 canon（読書リスト＝古典の門）")
    lines.append("- [[_worklist]] — ingest worklist（エージェントが処理する増分TODO）")
    lines.append("")
    lines.append("## ★概念の背骨（MOC・被リンク数順＝知識の中心）")
    for p in concepts_sorted:
        lines.append("- %s （%d被リンク） — %s" % (
            link(p["stem"]), counts.get(p["stem"], 0), p["title"]
        ))
    lines.append("")
    lines.append("## ダッシュボード")
    for p in dashboards_sorted:
        lines.append("- %s — %s" % (link(p["stem"]), p["title"]))
    lines.append("")
    lines.append("## クエリ（資産化された問い）")
    for p in queries_sorted:
        lines.append("- %s — %s" % (link(p["stem"]), p["title"]))
    lines.append("")
    lines.append("## エンティティ（事実の自動集約層）")
    lines.append("- token %d件 / player %d件" % (len(tokens), len(players)))
    lines.append(
        "- token 被リンク上位15: "
        + " ".join(link(p["stem"]) for p in tokens_sorted[:15])
    )
    lines.append(
        "- player 被リンク上位15: "
        + " ".join(link(p["stem"]) for p in players_sorted[:15])
    )
    lines.append("")
    lines.append("## 古典 canon / summaries")
    lines.append("- canon 1件: %s" % link("canon"))
    lines.append(
        "- summaries %d件: " % len(summaries)
        + " ".join(link(p["stem"]) for p in summaries_sorted)
    )
    lines.append("")
    lines.append("---")
    lines.append("生成時刻(UTC): %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    lines.append("")
    return "\n".join(lines)


def main():
    pages = collect_pages()
    counts = compute_inbound_counts(pages)
    content = build_index_text(pages, counts)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(
        "build_moc: wrote %s (%d bytes, %d pages scanned, %d concepts, %d dashboards, "
        "%d queries, %d tokens, %d players, %d summaries)"
        % (
            INDEX_PATH,
            len(content.encode("utf-8")),
            len(pages),
            sum(1 for p in pages if p["kind"] == "concept"),
            sum(1 for p in pages if p["kind"] == "dashboard"),
            sum(1 for p in pages if p["kind"] == "query"),
            sum(1 for p in pages if p["kind"] == "token"),
            sum(1 for p in pages if p["kind"] == "player"),
            sum(1 for p in pages if p["kind"] == "summary"),
        )
    )


if __name__ == "__main__":
    main()
