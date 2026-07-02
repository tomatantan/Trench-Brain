#!/usr/bin/env python3
"""brain/asset_queries.py — 学習の両輪(合成半・原則3/§Query).

ask.sh が捨てずに積んだ Q&A(brain/state/query_log.jsonl)を、門付きで
wiki/queries/ の永続ページに資産化する＝「質問するほど脳が賢くなる」。
資産化された query は BM25(/api/search)で拾われ、以後の回答の材料になる
＝クエリ軸の複利([[trench-brain-world-engine-moat]] の②合成=複利の源)。

門(価値ゲート・firehoseにしない): 失敗/短すぎ/重複 は資産化しない。
これは合成側の仕事＝wiki を書く(読取専用 public backend からは呼ばない)。

冪等: 資産化済みは query_log の assetized=True で二度書きしない。
Usage: python3 brain/asset_queries.py [--dry-run]
"""
import argparse
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "brain", "state", "query_log.jsonl")
QDIR = os.path.join(ROOT, "wiki", "queries")

MIN_ANSWER = 120           # これ未満は資産化に値しない
ERR_MARKERS = ("脳が応答", "内部エラー", "タイムアウト", "GEMINI_API_KEY", "usage:", "bad request")


def norm_q(q):
    return re.sub(r"\s+", "", (q or "").lower())


def slug(q):
    s = re.sub(r"[^\w぀-ヿ一-鿿]+", "-", (q or "").strip().lower())
    return s.strip("-")[:40] or "query"


def load_log():
    if not os.path.exists(LOG):
        return []
    out = []
    with open(LOG, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    pass
    return out


def existing_questions():
    """資産化済み query の正規化問い集合(dedup用)。"""
    seen = set()
    if not os.path.isdir(QDIR):
        return seen
    for fn in os.listdir(QDIR):
        if not fn.endswith(".md"):
            continue
        try:
            with open(os.path.join(QDIR, fn), encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
        if m:
            seen.add(norm_q(m.group(1)))
    return seen


def gate(rec):
    """(通すか, 理由)。門=firehoseにしない価値判定。"""
    q, a = rec.get("question", ""), rec.get("answer", "")
    if not q.strip():
        return False, "empty-question"
    if len(a.strip()) < MIN_ANSWER:
        return False, f"answer-too-short({len(a.strip())})"
    if any(m in a for m in ERR_MARKERS):
        return False, "error-answer"
    return True, "ok"


def write_page(rec):
    date = (rec.get("ts", "") or "")[:10] or datetime.date.today().isoformat()
    q, a = rec["question"].strip(), rec["answer"].strip()
    fn = f"{date}-{slug(q)}.md"
    path = os.path.join(QDIR, fn)
    # 同名衝突は連番回避
    i = 2
    while os.path.exists(path):
        path = os.path.join(QDIR, f"{date}-{slug(q)}-{i}.md")
        i += 1
    title = q.replace("\n", " ")[:120]
    body = (
        f"---\ntype: query\ntitle: {title}\ncreated: {date}\nupdated: {date}\n"
        f"asked: {rec.get('ts', '')}\nvia: ask({rec.get('backend', '')})\n"
        f"tags: [trench, query]\n---\n\n## 問い\n{q}\n\n## 回答\n{a}\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return os.path.relpath(path, ROOT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    log = load_log()
    if not log:
        print(json.dumps({"ok": True, "assetized": 0, "note": "query_log 空(コスト0)"}))
        return

    seen = existing_questions()
    assetized, skipped, changed = [], [], False
    for rec in log:
        if rec.get("assetized"):
            continue
        ok, why = gate(rec)
        nq = norm_q(rec.get("question", ""))
        if ok and nq in seen:
            ok, why = False, "duplicate"
        if not ok:
            skipped.append(why)
            if not args.dry_run:
                rec["assetized"] = True  # 門落ちも再評価しない(署名スキップ=無駄LLM/走査防止)
                rec["skip_reason"] = why
                changed = True
            continue
        if args.dry_run:
            assetized.append(f"[DRY] {rec['question'][:40]}")
            continue
        path = write_page(rec)
        seen.add(nq)
        rec["assetized"] = True
        rec["asset_path"] = path
        changed = True
        assetized.append(path)

    if changed and not args.dry_run:
        with open(LOG, "w", encoding="utf-8") as f:
            for rec in log:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    from collections import Counter
    print(json.dumps({
        "ok": True, "assetized": len([a for a in assetized if not a.startswith("[DRY]")]),
        "assetized_paths": assetized,
        "skipped": dict(Counter(skipped)),
        "note": "資産化済みは BM25(/api/search)で以後の回答材料に=クエリ軸の複利。"
                "深い織り込み(concept更新)は合成ループの次段。",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
