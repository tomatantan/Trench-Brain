#!/usr/bin/env python3
"""
expand_watchlist.py — watchlist(収集の門)を**自動で賢く広げる**仕組み。

憲法 指針2: 「watchlist拡張すら半自動化可（…繰り返し引用されるアカを候補化→人は承認だけ）」。
＝既収集ツイの**引用グラフ**を見て、「watchlist の複数KOLが繰り返し言及してる、まだ未収集のアカ」を
自動でランク付けし watchlist.md の「自動拡張候補」節に書き出す（＝人は承認だけ＝門を機械が広げる素材を出す）。
これで corpus が放っておいても広がる方向に向く（辞書が厚くなる）。

★firehoseでない: 「複数の信頼アカが繰り返し引用する」＝KOL言及門＝立派なキュレーション(指針2)。
無差別に全アカ追加でなく、**引用グラフで濾した候補**を出すだけ。採否(門に入れる)は人 or 高signal自動昇格。

選別: 未watchlist & watchlistアカからの言及 distinct citers >= MIN_CITERS。
出力: watchlist.md の <!-- auto-candidates --> 節を冪等再生成（引用元アカ数 × 総言及で降順）。
"""
import glob
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
WL = ROOT / "watchlist.md"
MIN_CITERS = 2          # watchlistの何アカ以上が言及してたら候補にするか(KOL言及門)。
                        # ★2に緩和(本人2026-07-02「調べる人をめちゃくちゃ増やせ」)＝矛盾の表面積を広げる。
TOPN = 60
START = "<!-- auto-candidates:start -->"
END = "<!-- auto-candidates:end -->"
# ★"人の思考をモデル化する"目的にはorg/app/chain/exchangeは不要(ノイズ)＝候補から外す。
#   目的は KOL/トレーダーの脳。プロダクト告知フィードは要らない(mind-modelにならない)。
NOISE = {"sbf_ftx", "fifaworldcup", "ftx_official",
         # exchange/wallet/app/chain/protocol(＝人でなくorg)
         "phantom", "backpack", "robinhoodapp", "polymarket", "kalshi", "base",
         "zksync", "avax", "optimism", "strategy", "world_xyz", "ethlabs_org",
         "ethereumfndn", "sunrisedefi", "coinbase", "binance", "solana", "ethereum",
         "uniswap", "jupiterexchange", "raydiumprotocol", "pumpdotfun", "bullx_io",
         "photonsol", "axiomexchange", "gmgnai", "dexscreener", "birdeye_so", "re"}
HANDLE_RE = re.compile(r"\[\[@([A-Za-z0-9_]{2,15})\]\]")
MENTION_RE = re.compile(r"(?<![A-Za-z0-9_/])@([A-Za-z0-9_]{2,15})\b")


def current_watchlist(text):
    return {m.group(1).lower() for m in HANDLE_RE.finditer(text)}


def main():
    if not WL.exists():
        print("watchlist.md が見つかりません。スキップ。")
        return
    text = WL.read_text(encoding="utf-8")
    # 候補節を除いた本文で現watchlistを判定（候補節の@は数えない）
    base = text
    if START in base and END in base:
        base = base[:base.index(START)] + base[base.index(END) + len(END):]
    wl = current_watchlist(base)

    ment = Counter()
    citers = defaultdict(set)
    examples = {}
    for f in glob.glob(str(SRC / "*.md")):
        t = open(f, encoding="utf-8", errors="replace").read()
        am = re.search(r"^account: (\S+)", t, re.M)
        author = (am.group(1) if am else "?").lower()
        parts = t.split("---", 2)
        body = parts[2] if len(parts) >= 3 else t
        for mm in MENTION_RE.finditer(body):
            h = mm.group(1)
            hl = h.lower()
            if hl in wl or hl == author or hl in NOISE:
                continue
            ment[h] += 1
            citers[h].add(author)
            examples.setdefault(h, author)

    rows = [(len(citers[h]), ment[h], h) for h in ment if len(citers[h]) >= MIN_CITERS]
    rows.sort(reverse=True)
    rows = rows[:TOPN]

    lines = [START,
             f"## 自動拡張候補（引用グラフ・要承認 / `expand_watchlist.py` 自動生成）",
             f"watchlist の **{MIN_CITERS}アカ以上**が言及した未収集アカ＝門に足す候補（指針2: 繰り返し引用＝KOL言及門）。",
             "**承認のしかた**: 良いものを上の watchlist 本体に `[[@handle]]` で足すだけ→次サイクルから収集開始。",
             "", "| 候補 | 言及したwatchlistアカ数 | 総言及 |", "|---|---|---|"]
    for c, n, h in rows:
        lines.append(f"| @{h} | {c} | {n} |")
    if not rows:
        lines.append("| (候補なし) | | |")
    lines.append(END)
    block = "\n".join(lines)

    if START in text and END in text:
        new = text[:text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        new = text.rstrip() + "\n\n" + block + "\n"
    WL.write_text(new, encoding="utf-8")
    print(f"watchlist auto-candidates: {len(rows)}件 (>= {MIN_CITERS}アカ引用) -> watchlist.md")
    for c, n, h in rows[:8]:
        print(f"  @{h}: {c}アカ / {n}言及")


if __name__ == "__main__":
    main()
