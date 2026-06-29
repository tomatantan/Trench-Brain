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
                self.docs.append({
                    "path": str(p.relative_to(ROOT)), "title": title,
                    "body": body, "tf": tf, "len": sum(tf.values()),
                    "stem": p.stem.lower(),  # "$cafe" / "@crediblecrypto" 等
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
