#!/usr/bin/env python3
"""flow_pulse.py — KOL網の「市場の流れ」計測 (2026-07-12 本人「KOLを取るのは市場の流れを捉えるため。銘柄の温度じゃない」).

銘柄言及(ティッカー温度計)でなく、watchlist全発言(ティッカー無し含む)の**話題の重心とその移動**を
毎サイクル決定的に計測する。直近7日 vs その前7日の話題分布の変化＝「網の頭がどっちを向き始めたか」。
- LLM不使用・$0・bounded。深い解釈は既存のconcept合成とask(地合いダイヤルの入力)が担う。
- 出力: brain/state/flow_pulse.json（ask.shが「相場/どう動く」系の問いに注入）。
"""
import glob
import json
import os
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
OUT = ROOT / "brain" / "state" / "flow_pulse.json"
WINDOW = 7 * 24 * 3600

# 話題バケツ(EN+JP・小文字比較)。単語追加はここだけ=閾値/分類の恒久チューニング口。
BUCKETS = {
    "macro/金利":       r"\bfed\b|rate cut|rate hike|\bcpi\b|inflation|treasury|\bdxy\b|liquidity|金利|マクロ|雇用統計|利下げ|利上げ",
    "regime/転換警戒":  r"\bbear\b|\bbull\b|crash|correction|risk.?off|risk.?on|\bbottom\b|top is in|capitulat|暴落|底打ち|天井|調整",
    "meme/trench":      r"\bmeme|pump\.fun|trench|degen|魔界|bonding curve|launchpad|\bcult\b",
    "rotation/資金移動": r"rotat|資金が|flow(?:s|ing)? (?:in|out|to)|回転|次のメタ|新しいメタ|money mov",
    "perps/defi":       r"\bperp|hyperliquid|funding rate|leverage|\blending\b|\byield\b|\bdefi\b",
    "AI":               r"\bai\b|\bagent(?:ic|s)?\b|\bllm\b|openai|anthropic",
    "規制/政治":         r"\bsec\b|\betf\b|regulat|tariff|senate|congress|規制|法案|関税|大統領",
    "警告/scam":        r"\bscam|\brug|hack(?:ed|er)?|exploit|drain(?:ed|er)?|honeypot|phishing|詐欺|注意喚起",
    "stocks/RWA":       r"tokenized|\brwa\b|\bstocks?\b|equit(?:y|ies)|robinhood|nasdaq|treasur",
    "majors":           r"\bbtc\b|bitcoin|\beth\b|ethereum|\bsol\b|solana(?! meme)",
}


def _post_iter():
    """(epoch, handle, body小文字) を全watchlist発言からyield。createdはfrontmatter優先・無ければmtime。"""
    for p in glob.glob(str(SRC / "*.md")):
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        m = re.search(r"^created:\s*(\S+)", t, re.M)
        ts = None
        if m:
            try:
                from datetime import datetime
                ts = datetime.fromisoformat(m.group(1).replace("Z", "+00:00")).timestamp()
            except Exception:
                ts = None
        if ts is None:
            try:
                ts = os.path.getmtime(p)
            except OSError:
                continue
        body = t.split("---", 2)[-1].lower()
        h = os.path.basename(p).rsplit("__", 1)[0].lower() if "__" in os.path.basename(p) else "?"
        yield ts, h, body


def main():
    now = time.time()
    cur = {k: {"posts": 0, "accounts": set()} for k in BUCKETS}
    prev = {k: 0 for k in BUCKETS}
    n_cur = n_prev = 0
    examples = {k: [] for k in BUCKETS}
    regs = {k: re.compile(v, re.I) for k, v in BUCKETS.items()}
    for ts, h, body in _post_iter():
        age = now - ts
        if age > 2 * WINDOW:
            continue
        recent = age <= WINDOW
        if recent:
            n_cur += 1
        else:
            n_prev += 1
        for k, rx in regs.items():
            if rx.search(body):
                if recent:
                    cur[k]["posts"] += 1
                    cur[k]["accounts"].add(h)
                    if len(examples[k]) < 2 and len(body) > 60:
                        examples[k].append(f"@{h}: " + re.sub(r"https?://\S+", "", body).strip().replace("\n", " ")[:110])
                else:
                    prev[k] += 1

    buckets = {}
    for k in BUCKETS:
        share_now = round(100 * cur[k]["posts"] / n_cur, 1) if n_cur else 0.0
        share_prev = round(100 * prev[k] / n_prev, 1) if n_prev else 0.0
        buckets[k] = {"posts_7d": cur[k]["posts"], "accounts_7d": len(cur[k]["accounts"]),
                      "share_now_pct": share_now, "share_prev_pct": share_prev,
                      "delta_pp": round(share_now - share_prev, 1)}
    moved = sorted(buckets.items(), key=lambda x: -abs(x[1]["delta_pp"]))
    out = {
        "updated": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "window": {"posts_7d": n_cur, "posts_prev7d": n_prev},
        "note": "watchlist全発言(ティッカー無し含む)の話題重心。share=その話題に触れた投稿の割合・delta_pp=前7日比。",
        "buckets": buckets,
        "top_moves": [{"topic": k, "delta_pp": v["delta_pp"], "share_now_pct": v["share_now_pct"],
                       "accounts": v["accounts_7d"],
                       "examples": examples.get(k, [])[:2]} for k, v in moved[:4] if abs(v["delta_pp"]) >= 0.5],
    }
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, OUT)
    print("flow-pulse: 7d {}posts / 前7d {}posts / 最大移動: {}".format(
        n_cur, n_prev, ", ".join(f"{m['topic']} {m['delta_pp']:+}pp" for m in out["top_moves"]) or "有意な移動なし"))


if __name__ == "__main__":
    main()
