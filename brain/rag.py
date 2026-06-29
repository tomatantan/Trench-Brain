#!/usr/bin/env python3
"""
rag.py — wiki から関連ページを安く拾う retrieval（LLM不要・依存ゼロ・$0）。

公開Q&A脳の"索引"層: 質問 → BM25 で Top-K wiki チャンクを返す → 上の合成LLMに渡す。
本人指摘「索引にAIいらない」の実装＝検索はCPUで十分・LLMは最後の合成1回だけ。

日本語/英語/$ticker 混在を**依存ゼロ**で扱う＝CJKは文字bigram・ASCIIは単語/ticker/handle。
（形態素解析器を入れずに日本語検索が効く標準テク）

使い方:
  python3 brain/rag.py "graduatedしたのに死ぬ型は?"     # Top-K 表示
  from rag import Retriever; r = Retriever(); r.context(q, k=6)  # 合成LLM用の文脈
"""
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
# 索引対象(.obsidian / ui / _templates は除外)
SUBDIRS = ["concepts", "entities/tokens", "entities/players", "queries", "dashboards", "summaries"]

ASCII_TOK = re.compile(r"\$[A-Za-z0-9]{1,15}|@[A-Za-z0-9_]{1,30}|[a-z0-9_]{2,}")
CJK_RUN = re.compile(r"[぀-ヿ㐀-鿿豈-﫿]+")
FM = re.compile(r"\A---\n.*?\n---\n", re.S)
LINK = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")  # [[target]] / [[target|display]]


def tokenize(text):
    text = text.lower()
    toks = ASCII_TOK.findall(text)
    # CJK の連続を文字bigram(1文字なら単体)に分解
    for run in CJK_RUN.findall(text):
        if len(run) == 1:
            toks.append(run)
        else:
            toks.extend(run[i:i + 2] for i in range(len(run) - 1))
    return toks


def title_of(raw, path):
    m = re.search(r"^title:\s*(.+)$", raw, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", raw, re.M)
    if m:
        return m.group(1).strip()
    return path.stem


class Retriever:
    def __init__(self):
        self.docs = []      # {path, title, body, tf, len}
        self.df = Counter()
        self._load()
        self.N = len(self.docs)
        self.avgdl = sum(d["len"] for d in self.docs) / max(1, self.N)
        # 知識グラフ index: path/stem 引き + 内向きリンク(誰がこのページを[[link]]してるか)
        self.by_path = {d["path"]: d for d in self.docs}
        self.by_stem = {d["stem"]: d for d in self.docs}
        self.inbound = {}
        for d in self.docs:
            for tgt in d["links"]:
                self.inbound.setdefault(tgt, []).append(d)

    def page(self, path):
        """1ページの合成内容を返す(UIの表示用)。path は 'wiki/...md' でも stem でも可。"""
        if path in self.by_path:
            return self.by_path[path]
        s = str(path).lower()
        return (self.by_stem.get(s) or self.by_stem.get(s.lstrip("$@"))
                or self.by_stem.get("$" + s) or self.by_stem.get("@" + s))

    @staticmethod
    def _prio(p):
        """知識グラフの意味的優先: concept > query/dashboard > player > token。"""
        if "/concepts/" in p:
            return 0
        if "/queries/" in p or "/dashboards/" in p:
            return 1
        if "/players/" in p:
            return 2
        if "/tokens/" in p:
            return 3
        return 4

    def related(self, path, k=40):
        """そのページの外向き[[link]]先 と 内向き(被リンク)を返す＝知識グラフ navigation。
        例token spam に埋もれないよう concept/player を優先順に。"""
        d = self.page(path)
        if not d:
            return {"outbound": [], "inbound": [], "outbound_total": 0, "inbound_total": 0}
        out = []
        for tgt in d["links"]:
            t = self.by_stem.get(tgt) or self.by_stem.get(tgt.lstrip("$@"))
            if t and t["path"] != d["path"]:
                out.append({"title": t["title"], "path": t["path"]})
        out.sort(key=lambda x: (self._prio(x["path"]), x["title"]))
        inb = [{"title": s["title"], "path": s["path"]}
               for s in self.inbound.get(d["stem"], []) if s["path"] != d["path"]]
        inb.sort(key=lambda x: (self._prio(x["path"]), x["title"]))
        return {"outbound": out[:k], "inbound": inb[:k],
                "outbound_total": len(out), "inbound_total": len(inb)}

    def _load(self):
        for sub in SUBDIRS:
            for p in sorted((WIKI / sub).glob("*.md")):
                try:
                    raw = p.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                title = title_of(raw, p)
                body = FM.sub("", raw)
                tf = Counter(tokenize(title + " " + body))
                links = {t.strip().lower() for t in LINK.findall(body)}  # 外向き[[link]]先(正規化)
                self.docs.append({
                    "path": str(p.relative_to(ROOT)), "title": title,
                    "body": body, "tf": tf, "len": sum(tf.values()),
                    "stem": p.stem.lower(),  # "$cafe" / "@crediblecrypto" 等
                    "links": links,
                })
                for t in tf:
                    self.df[t] += 1

    def search(self, query, k=6):
        qtoks = set(tokenize(query))
        # クエリ中の完全エンティティ($ticker / @handle / 名前)を抽出＝自分のページを強boost
        ents = set()
        for m in re.findall(r"\$[A-Za-z0-9]{1,15}", query):
            ents.add(m.lower())
        for m in re.findall(r"@?([A-Za-z][A-Za-z0-9_]{2,})", query):
            ents.add(m.lower())
            ents.add("@" + m.lower())
        k1, b = 1.5, 0.75
        scored = []
        for d in self.docs:
            s = 0.0
            for t in qtoks:
                f = d["tf"].get(t, 0)
                if not f:
                    continue
                idf = math.log(1 + (self.N - self.df[t] + 0.5) / (self.df[t] + 0.5))
                s += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * d["len"] / self.avgdl))
            # ★完全一致boost: doc の filename がクエリのエンティティそのものなら大幅加点
            if d["stem"] in ents or d["stem"].lstrip("$@") in ents:
                s += 25.0
            if s > 0:
                scored.append((s, d))
        scored.sort(key=lambda x: -x[0])
        return scored[:k]

    def context(self, query, k=6, max_chars=1200):
        """合成LLMに渡す文脈＝Top-K の title + 本文抜粋。"""
        out = []
        for _s, d in self.search(query, k):
            excerpt = d["body"].strip()[:max_chars]
            out.append(f"## {d['title']}  ({d['path']})\n{excerpt}")
        return "\n\n".join(out)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "今 trench で死にやすい型は?"
    r = Retriever()
    print(f"索引: {r.N} docs / 平均長 {r.avgdl:.0f}tok\n問い: {q}\n")
    for s, d in r.search(q, 8):
        print(f"  {s:6.2f}  {d['title'][:48]:48}  [{d['path']}]")
