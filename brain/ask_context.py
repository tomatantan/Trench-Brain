#!/usr/bin/env python3
"""ask_context.py — 決定的 retrieval + 実績注入（G1/G2・回答を接地する）.

ask.sh の脳を「grep運任せ」から「合成済みwikiを決定的に読む＋自分のfeedback(KOL実績/
base-rate)を見る」に変える。BM25(rag.py)で関連ページを取り、問い/文脈に出るKOLの
track record と base-rate を添える。モデル非依存（材料をコードで組む＝弱いモデルでも同じ）。

出力は prompt に注入する markdown ブロック（stdout）。失敗しても空を返し ask を壊さない。
Usage: python3 brain/ask_context.py "<question>"
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "brain"))


def _load(name, default):
    try:
        with open(os.path.join(ROOT, "brain", "state", name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return default


def main():
    q = sys.argv[1] if len(sys.argv) > 1 else ""
    if not q.strip():
        return

    # G1: 決定的 retrieval（合成済みwikiの関連ページ＝grepさせない）
    ctx = ""
    try:
        from rag import Retriever
        ctx = Retriever().context(q, k=6, max_chars=1000)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"[ask_context] retrieval失敗: {type(e).__name__} {e}\n")

    # G2: 言及KOLの実績（評判でなく成績で"勝者"を判断させる）
    ktr = _load("kol_track_records.json", {})
    base = _load("base_rate.json", {})
    # 問い＋retrieved context に出る handle を拾う
    hay = q + "\n" + ctx
    handles = {h.lower() for h in re.findall(r"@([A-Za-z0-9_]{3,15})", hay)}
    handles |= {h.lower() for h in re.findall(r"\b([A-Za-z0-9_]{4,15})\b", q)}
    recs = []
    for k, v in ktr.items():
        if not isinstance(v, dict):
            continue
        hd = (v.get("handle") or k)
        if (k.lower() in handles or hd.lower() in handles) and v.get("evaluated"):
            recs.append(f"- @{hd}: 直近{v['evaluated']}件評価中 **death {v.get('death_rate')}%**"
                        f"（母集団は大半死＝相対で読む・小N注意）")

    # base-rate の錨
    gp, di, gr = base.get("gate_passed"), base.get("died"), base.get("graduated")
    base_line = ""
    if gp:
        base_line = (f"門通過 {gp}銘柄中 死{di}/卒業{gr}＝**門を通っても大半が死ぬ**のが基準線。"
                     f"個別銘柄はこの事前確率の上で読む。")

    out = []
    if ctx:
        out.append("### 合成済みwiki（決定的に取得＝これを根拠に横断合成せよ。[[..]]で引用）\n" + ctx)
    if recs:
        out.append("### 言及KOLの実績（track record＝評判/フォロワーでなく"
                   "**成績**で『勝者』を判断せよ・声のデカさで語るな）\n" + "\n".join(recs))
    if base_line:
        out.append("### base-rate（錨）\n" + base_line)
    if out:
        print("\n\n".join(out))


if __name__ == "__main__":
    main()
