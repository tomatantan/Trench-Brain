#!/usr/bin/env python3
"""
Trench-Brain digest — 「仕分ける仕組み」v1（脳の前処理層）

sources/x/ の生ツイを走査し、ノイズを落として信号を集計する。
- ノイズ除外: 純RT / 極端に短い / gm,gn,lfg等の中身なし
- 信号集計: $ticker頻度, ticker×アカウント共起, アカウント別活動, 高エンゲージ抜粋
出力: wiki/dashboards/signal.md（Obsidianで見える集計）＋ stdoutに要約。

合成(concept生成)はこの集計を入力に、エージェント(Claude)が行う。
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
OUT = ROOT / "wiki" / "dashboards" / "signal.md"

NOISE_RE = re.compile(r"^(gm+|gn+|lfg+|wagmi|ngmi|wen|soon|ser|fr+|lol+|gg+|\.+|🚀+)$", re.I)
TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")
URL_RE = re.compile(r"https?://\S+")


def parse(path):
    """ノートを (meta dict, body) に。"""
    txt = path.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return None, ""
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return None, ""   # 同上(2026-07-02 M1)
    _, fm, body = parts
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.strip()


def is_noise(meta, body):
    if str(meta.get("is_retweet", "")).lower() == "true":
        return True
    stripped = URL_RE.sub("", body)
    stripped = re.sub(r"[@#]\w+", "", stripped).strip()
    if len(stripped) < 12:
        return True
    if NOISE_RE.match(stripped.replace(" ", "")):
        return True
    return False


def to_int(s):
    try:
        return int(s)
    except Exception:
        return 0


def main():
    notes = list(SRC.glob("*.md"))
    total = len(notes)
    kept = 0
    ticker_count = Counter()
    ticker_accounts = defaultdict(set)
    acct_activity = Counter()
    acct_likes = Counter()
    top_tweets = []  # (likes, account, ticker_list, body, url)

    for p in notes:
        meta, body = parse(p)
        if meta is None:
            continue
        acct = meta.get("account", "?")
        acct_activity[acct] += 1
        acct_likes[acct] += to_int(meta.get("likes"))
        if is_noise(meta, body):
            continue
        kept += 1
        tickers = TICKER_RE.findall(body)
        for t in set(tickers):
            tk = t.upper()
            ticker_count[tk] += 1
            ticker_accounts[tk].add(acct)
        likes = to_int(meta.get("likes"))
        top_tweets.append((likes, acct, sorted(set(t.upper() for t in tickers)),
                           body.replace("\n", " "), meta.get("url", "")))

    top_tweets.sort(reverse=True)

    def md_table(rows, header):
        out = ["| " + " | ".join(header) + " |",
               "|" + "|".join("---" for _ in header) + "|"]
        out += rows
        return "\n".join(out)

    lines = [
        "---", "type: dashboard", "title: Signal digest",
        "updated: 2026-06-22", "tags: [trench, dashboard]", "---", "",
        "# Signal digest（仕分け集計）", "",
        f"生ツイ {total} 件 → ノイズ(RT/短文/中身なし)除外後 **{kept} 件**が信号。",
        "[[index]] / この集計を入力にエージェントが [[concepts|concept]] を合成する。", "",
        "## ホット $ticker（言及ノート数 × 言及アカ数）", "",
    ]
    rows = []
    for tk, c in ticker_count.most_common(30):
        na = len(ticker_accounts[tk])
        accts = ", ".join(sorted(ticker_accounts[tk])[:6])
        rows.append(f"| {tk} | {c} | {na} | {accts} |")
    lines.append(md_table(rows, ["ticker", "言及数", "アカ数", "言及アカ(一部)"]))

    lines += ["", "## 活発なアカウント（信号込み投稿数 / 累計いいね）", ""]
    rows = []
    for acct, n in acct_activity.most_common(25):
        rows.append(f"| [[@{acct}]] | {n} | {acct_likes[acct]:,} |")
    lines.append(md_table(rows, ["account", "投稿数", "累計likes"]))

    lines += ["", "## 高エンゲージ・ツイート Top 25（信号のみ）", ""]
    rows = []
    for likes, acct, tks, body, url in top_tweets[:25]:
        tk = " ".join(tks)[:24]
        snippet = body[:90].replace("|", "/")
        rows.append(f"| {likes:,} | [[@{acct}]] | {tk} | {snippet} |")
    lines.append(md_table(rows, ["likes", "account", "tickers", "抜粋"]))
    lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"total={total} kept_signal={kept} noise={total-kept}")
    print("TOP tickers:", ", ".join(f"{t}({c})" for t, c in ticker_count.most_common(15)))
    print("TOP accounts:", ", ".join(f"{a}({n})" for a, n in acct_activity.most_common(10)))
    print(f"dashboard -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
