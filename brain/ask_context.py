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
    # ★alias解決(2026-07-11 本人「猫太郎とかのシグナル使えてなくない？」): 日本語名/表示名で聞かれても
    #   handleに解決できる様、watchlist.md の |[[@handle]]|名前| 列から alias辞書を組む(決定的・毎回~1ms)。
    #   例: 「猫太郎」→ tsuyuto6154。名前は「猫太郎_Nekotaro」の様な複合形→ _/／/空白 で分割して各tokenも引く。
    alias_hits = []  # 質問文中の表示名ヒット=名指しされた本人(G4の注入優先順で最上位に置く)
    try:
        wl = open(os.path.join(ROOT, "wiki", "watchlist.md"), encoding="utf-8").read()
        for h, name in re.findall(r"^\|\s*\[\[@([A-Za-z0-9_]+)\]\]\s*\|\s*([^|]+?)\s*\|", wl, re.M):
            for alias in re.split(r"[_/／\s@]+", name):
                alias = alias.strip()
                if len(alias) >= 2 and alias in q:
                    handles.add(h.lower())
                    if h.lower() not in alias_hits:
                        alias_hits.append(h.lower())
    except Exception:  # noqa: BLE001
        pass
    recs = []
    # ★N門(本人指摘2026-07-13「死亡率とかどうでもいい・正しいのかもわからんゴミ指標」):
    #   N=3〜6の"死亡率0%"は偶然=統計的にゴミ・生存≠強さ・検証不能な精度が信頼を壊す。
    #   → N<MIN_N は率を出さない(サンプル不足と正直に)。出す時も"生存率であって収益でない弱い補助"に降格。
    MIN_N = 20
    for k, v in ktr.items():
        if not isinstance(v, dict):
            continue
        hd = (v.get("handle") or k)
        n = v.get("evaluated") or 0
        if not ((k.lower() in handles or hd.lower() in handles) and n):
            continue
        if n < MIN_N:
            recs.append(f"- @{hd}: 評価{n}件のみ＝**実績を語るにはサンプル不足**"
                        f"（生存率は出さない・強さの根拠にするな）")
        else:
            recs.append(f"- @{hd}: 参考=直近{n}件の**生存率**の粗い目安 death {v.get('death_rate')}%"
                        f"（※生存であって収益/edgeでない・母集団は大半死＝弱い補助信号・これで強者を順位づけするな）")

    # base-rate の錨
    gp, di, gr = base.get("gate_passed"), base.get("died"), base.get("graduated")
    base_line = ""
    if gp:
        base_line = (f"門通過 {gp}銘柄中 死{di}/卒業{gr}＝**門を通っても大半が死ぬ**のが基準線。"
                     f"個別銘柄はこの事前確率の上で読む。")
    # ★チェーン別base-rate(Phase2-lite 2026-07-12): KOL言及コホートの0x CA現生死。母集団が違う事を明示。
    cb = _load("chain_base_rate.json", {})
    ch_lines = [f"{ch}: {v['n']}件中 死{v['death_rate']}%"
                for ch, v in sorted((cb.get("chains") or {}).items()) if v.get("n", 0) >= 3]
    if ch_lines:
        base_line += ("\nEVM各チェーン(KOL言及コホート・全mint観測でない=Solanaのbase-rateと母集団が違う): "
                      + " / ".join(ch_lines))

    # G5b: 過去の自分の回答のその後（自己校正＝答えっぱなしにしない）
    sc = _load("answer_scorecard.json", {})
    self_lines = []
    summ = sc.get("summary") or {}
    if summ.get("tokens_mentioned"):
        dp = summ.get("dead_pct_of_resolved")
        self_lines.append(
            f"過去{summ['answers']}回答の言及銘柄{summ['tokens_mentioned']}件: "
            f"現在 dead {summ['dead_now']} / alive {summ['alive_now']}"
            + (f"（決着分の死{dp}%）" if dp is not None else ""))
        for aid in sorted((sc.get("answers") or {}), reverse=True)[:3]:
            v = sc["answers"][aid]
            toks = " ".join(f"{k}:{t.get('status')}" for k, t in list(v.get("tokens", {}).items())[:4])
            if toks:
                self_lines.append(f"- {v.get('ts')}「{v.get('question','')[:50]}」→ {toks}")

    out = []
    if ctx:
        out.append("### 合成済みwiki（決定的に取得＝これを根拠に横断合成せよ。[[..]]で引用）\n" + ctx)
    if recs:
        out.append("### 言及KOLの参考実績（★強さの順位づけに使うな）\n"
                   "track recordは**生存率であって収益/edgeではない**・小Nは偶然。"
                   "『強者/勝者』を死亡率で並べるな＝**型・考え方・タイミング・待てるか・立ち回り**で語れ"
                   "（指針10＝判断でなく思考を渡す）。数字は弱い補助にとどめ、N不足なら実績を語らない。\n"
                   + "\n".join(recs))
    if base_line:
        out.append("### base-rate（錨）\n" + base_line)
    if self_lines:
        out.append("### 過去の自分の回答のその後（自己校正＝同じ外し方を繰り返すな）\n"
                   "言及した銘柄の多くが死んでいるなら、その型の推し方自体を疑って答えよ"
                   "（観測であり正誤ではない＝avoid警告が的中して死んだ可能性もある。文脈で読む）。\n"
                   + "\n".join(self_lines))

    # G3: 銘柄のKOL立場マップ注入（brain/build_entities.py が token entity に焼いた多視点テーブルを
    # そのまま見せる＝1視点のKOLコールを鵜呑みにさせない）。失敗しても ask を絶対に壊さない。
    try:
        STANCE_HDR = "## KOL立場マップ（多視点・自動）"
        tickers_in_q, seen = [], set()
        for m in re.findall(r"\$[A-Za-z][A-Za-z0-9]{1,9}", q):
            tk = m.upper()
            if tk not in seen:
                seen.add(tk)
                tickers_in_q.append(tk)
            if len(tickers_in_q) >= 2:
                break
        stance_blocks = []
        for tk in tickers_in_q:
            path = os.path.join(ROOT, "wiki", "entities", "tokens", f"{tk}.md")
            if not os.path.isfile(path):
                continue
            with open(path, encoding="utf-8") as f:
                txt = f.read()
            i = txt.find(STANCE_HDR)
            if i == -1:
                continue
            after = txt[i + len(STANCE_HDR):]
            ends = [p for p in (after.find("\n## "), after.find("<!--")) if p != -1]
            section = STANCE_HDR + (after[:min(ends)] if ends else after)
            stance_blocks.append(section.strip())
        if stance_blocks:
            out.append(
                "### 銘柄のKOL立場マップ（多視点＝**共通点と矛盾**を軸に答えよ・1視点の買い推奨はゴミ）\n"
                + "\n\n".join(stance_blocks))
    except Exception:  # noqa: BLE001
        pass

    # G4: 言及KOLの深堀りprofile注入（curated profile:start ブロックの「視点エンジンでの使い方」＋
    # 「⚠️矛盾」を渡し、その人の思考の型で答えさせる）。失敗してもask を絶対に壊さない。
    try:
        PROF_START, PROF_END = "<!-- profile:start -->", "<!-- profile:end -->"
        HDR_RE = re.compile(r"^### .*$", re.MULTILINE)
        prof_blocks = []
        # 質問文に直接出るhandle＋表示名(alias)で名指しされた本人を優先
        # (cap=2でretrieval由来のアルファベット先行handleに主役が押し出されるのを防ぐ)
        in_q = [h.lower() for h in re.findall(r"@([A-Za-z0-9_]{3,15})", q)]
        named = in_q + [h for h in alias_hits if h not in in_q]
        ordered_handles = named + sorted(h for h in handles if h not in named)
        for h in ordered_handles:
            if len(prof_blocks) >= 2:
                break
            path = os.path.join(ROOT, "wiki", "entities", "players", f"@{h}.md")
            if not os.path.isfile(path):
                continue
            with open(path, encoding="utf-8") as f:
                txt = f.read()
            i, j = txt.find(PROF_START), txt.find(PROF_END)
            if i != -1 and j != -1:
                inner = txt[i + len(PROF_START):j]
                subs, ms = [], list(HDR_RE.finditer(inner))
                for idx, m in enumerate(ms):
                    s = m.start()
                    e = ms[idx + 1].start() if idx + 1 < len(ms) else len(inner)
                    subs.append(inner[s:e].strip())
                persp = next((s for s in subs if s.split("\n", 1)[0].startswith("### 視点エンジンでの使い方")), None)
                contra = next((s for s in subs if s.split("\n", 1)[0].startswith("### ⚠️矛盾")), None)
                parts = [s for s in (persp, contra) if s]
                excerpt = ("\n\n".join(parts) if parts else inner.strip())[:900]
            else:
                # ★fallback(2026-07-11): curated profile未整備でも、自動合成の「思考の型」(synthesisブロック)が
                #   あればそれを注入＝JP trench勢等(猫太郎=tsuyuto6154)の脳が回答に届かない穴を塞ぐ。
                si, sj = txt.find("<!-- synthesis:start -->"), txt.find("<!-- synthesis:end -->")
                if si == -1 or sj == -1:
                    continue
                syn = txt[si + len("<!-- synthesis:start -->"):sj].strip()
                if "思考の型" not in syn:
                    continue
                excerpt = syn[:900]
            prof_blocks.append(f"**@{h}**:\n{excerpt}")
        if prof_blocks:
            out.append("### 言及KOLの深堀りprofile（思考の型＝この人ならこう読む）\n"
                       + "\n\n".join(prof_blocks))
    except Exception:  # noqa: BLE001
        pass

    if out:
        print("\n\n".join(out))


if __name__ == "__main__":
    main()
