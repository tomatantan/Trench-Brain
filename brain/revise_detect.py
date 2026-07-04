#!/usr/bin/env python3
"""
revise_detect.py — G4自己改訂の検出器（決定的・LLM不使用・報告でなくキュー化）。

問題(設計書 ENGINE-REDESIGN §1 G4): 実測(feedback/predictive)は毎サイクル更新されるのに、
concept本文に書かれた統計数値は書いた時点で凍結する＝非対称freshness。
実例: manipulation-playbook が「traction有り死12% vs 無し55%」(6/24時点)のまま、実測が44%/68%に動いていた。

方式(wiki_autofix→synthesize_gaps と同じ2段):
  この検出器(決定的)が concept本文の既知メトリクス数値と機械可読の実測正典
  (brain/state/feedback_stats.json = feedback.py が emit)を突き合わせ、
  乖離(>TOL pp)を brain/state/revise_queue.json に積む。
  消費は synthesize_revise.sh(LLM・revise_prompt.md)が行い、推移を保持したまま数値と主張強度を再合成する。

矛盾は消さない(指針5): 検出はキュー化だけ。書き換え時も旧値は推移として残す(promptで強制)。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATS = ROOT / "brain" / "state" / "feedback_stats.json"
QUEUE = ROOT / "brain" / "state" / "revise_queue.json"
CONCEPTS = ROOT / "wiki" / "concepts"
TOL = 5  # percent-point。実測は生き物＝小さな揺れで毎サイクル書き換えない(churn防止)。超えたら再合成。

# 死亡率の形の%だけを拾う（死12% / 12%死 / 無し55% / 有り12%）。
# 価格変動(+147%)・base rate(98.5%死は別メトリクス扱いで数値のみ拾う)等の誤爆を避けるため、
# 裸の "NN%" は対象にしない。台帳/表の行(| 始まり)は個別トークン観測＝集計claimでないので行ごと除外。
# 数値の前に -/+/± が付く物(価格変動 -92.9% 等)は死亡率でない＝拾わない。
NUM = r"(?<![\d.+\-±])(\d{1,3}(?:\.\d+)?)\s*%"
# ラベル付き抽出: 「有り…12%」「無し…55%」のように、ラベルから40字以内に現れる最初の%を
# そのラベルの死亡率として読む。any-vs-any比較だと「旧無し55% ≒ 現有り60%」の偶然一致で
# stale が素通りする(実際に起きた)ため、ラベル↔現在値を意味的に対応させて比較する。
WITH_RE = re.compile(r"有り[^%]{0,40}?" + NUM)
WITHOUT_RE = re.compile(r"無し[^%]{0,40}?" + NUM)


def near_kw(line, kw, window=30):
    """keyword の直後 window 字以内に現れる最初の死亡率%を全出現分拾う。"""
    out = []
    for m in re.finditer(re.escape(kw), line):
        seg = line[m.end():m.end() + window + 8]
        n = re.search(NUM, seg)
        if n and len(seg[:n.start()]) <= window:
            out.append(float(n.group(1)))
    return out


def bucket_str(b, label):
    if not b or b.get("pct") is None:
        return None
    return f"{label} 死{b['pct']}%（{b['dead']}/{b['n']}）"


def main():
    if not STATS.exists():
        print("revise_detect: feedback_stats.json 無し(feedback.py 未実行) → skip")
        return
    try:
        s = json.loads(STATS.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        print("revise_detect: feedback_stats.json 読めず → skip")
        return

    def pct(key):
        b = s.get(key) or {}
        return b.get("pct")

    # メトリクス台帳: conceptに現れる既知の実測claim ⇔ 正典の現在値。
    # line_filter は「この行はこのメトリクスの claim か」の決定的判定。
    metrics = []
    if pct("traction_with") is not None and pct("traction_without") is not None:
        metrics.append({
            "id": "traction_split", "mode": "labeled",
            "filter": lambda l: "traction" in l and "死" in l and "%" in l
                                and ("有り" in l or "無し" in l),
            "expected": {"with": pct("traction_with"), "without": pct("traction_without")},
            "truth": f"{bucket_str(s['traction_with'],'traction有り')} vs {bucket_str(s['traction_without'],'traction無し')}",
        })
    if pct("graduated_no_traction") is not None:
        metrics.append({
            "id": "graduated_but_empty", "mode": "kw", "kw": "graduated-but-empty",
            "filter": lambda l: "graduated-but-empty" in l and "%" in l,
            "expected": [pct("graduated_no_traction")],
            "truth": bucket_str(s["graduated_no_traction"], "graduated-but-empty(=graduated×traction無)"),
        })
    if pct("gate_mcap") is not None:
        metrics.append({
            "id": "mcap_gate", "mode": "kw", "kw": "mcap勢い門",
            "filter": lambda l: "mcap勢い門" in l and "死" in l and "%" in l,
            "expected": [pct("gate_mcap")],
            "truth": bucket_str(s["gate_mcap"], "mcap勢い門"),
        })
    if pct("gate_graduated") is not None:
        # 敵対検証C1(2026-07-04)の教訓: 台帳に無いメトリクスはループの外に恒久的に残る。
        # feedback_stats に bucket を足したら、ここに metric を必ず対で足す(SSOT=stats側)。
        metrics.append({
            "id": "gate_graduated", "mode": "kw", "kw": "graduated門",
            "filter": lambda l: "graduated門" in l and "死" in l and "%" in l,
            "expected": [pct("gate_graduated")],
            "truth": bucket_str(s["gate_graduated"], "graduated門(全graduated)"),
        })
    if pct("peak_below_10k") is not None:
        metrics.append({
            "id": "peak_below_10k", "mode": "kw", "kw": "10k",
            "filter": lambda l: "10k" in l and "死" in l and "%" in l and ("未満" in l or "<10k" in l),
            "expected": [pct("peak_below_10k")],
            "truth": bucket_str(s["peak_below_10k"], "peak<10k"),
        })

    queue = []
    for cf in sorted(CONCEPTS.glob("*.md")):
        try:
            lines = cf.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith("|"):
                continue  # 台帳/表の行=個別トークン観測。集計claimではない(rug-anatomy死亡台帳の誤爆防止)
            for m in metrics:
                if not m["filter"](line):
                    continue
                stale, written = False, []
                if m["mode"] == "labeled":
                    # ラベル↔現在値を意味的に対応させて比較(with は with と、without は without と)
                    w = [float(x) for x in WITH_RE.findall(line)]
                    wo = [float(x) for x in WITHOUT_RE.findall(line)]
                    if not w and not wo:
                        continue
                    written = {"with": w, "without": wo}
                    if w and not any(abs(v - m["expected"]["with"]) <= TOL for v in w):
                        stale = True
                    if wo and not any(abs(v - m["expected"]["without"]) <= TOL for v in wo):
                        stale = True
                else:
                    written = near_kw(line, m["kw"])
                    if not written:
                        continue
                    stale = not any(abs(v - e) <= TOL for v in written for e in m["expected"])
                if stale:
                    queue.append({
                        "page": f"wiki/concepts/{cf.name}",
                        "line_no": i,
                        "metric": m["id"],
                        "line": line.strip()[:300],
                        "written_pct": written,
                        "current": m["truth"],
                        "stats_ts": s.get("ts"),
                    })

    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    pages = sorted({q["page"] for q in queue})
    print(f"revise_detect: {len(queue)}件のstale数値を検出 → revise_queue.json（{len(pages)}ページ: "
          + ", ".join(p.split('/')[-1] for p in pages) + ")" if queue else
          f"revise_detect: 登録{len(metrics)}メトリクスの範囲で乖離なし（台帳外の数値は保証しない＝拡充はfeedback_statsとペアで）")


if __name__ == "__main__":
    main()
