#!/usr/bin/env python3
"""
ingest済の tweet_id を brain/state/ingested.txt に記録する。
エージェントが worklist を処理し終えた後に実行＝次サイクルは新ソースだけが worklist に出る。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
STATE = ROOT / "brain" / "state" / "ingested.txt"
URL_RE = re.compile(r"https?://\S+")
NOISE_RE = re.compile(r"^(gm+|gn+|lfg+|wagmi|ngmi|wen|soon|ser|fr+|lol+|gg+|\.+)$", re.I)


def parse(p):
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return None, ""
    _, fm, body = t.split("---", 2)
    m = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            m[k.strip()] = v.strip()
    return m, body.strip()


def is_noise(m, b):
    if str(m.get("is_retweet", "")).lower() == "true":
        return True
    s = re.sub(r"[@#]\w+", "", URL_RE.sub("", b)).strip()
    return len(s) < 12 or bool(NOISE_RE.match(s.replace(" ", "")))


def main():
    STATE.parent.mkdir(parents=True, exist_ok=True)
    have = set(STATE.read_text(encoding="utf-8").split()) if STATE.exists() else set()
    added = 0
    for p in SRC.glob("*.md"):
        m, b = parse(p)
        if m is None or is_noise(m, b):
            continue
        tid = m.get("tweet_id", "").strip('"')
        if tid and tid not in have:
            have.add(tid)
            added += 1
    STATE.write_text("\n".join(sorted(have)) + "\n", encoding="utf-8")
    print(f"marked ingested: +{added} (total {len(have)})")


if __name__ == "__main__":
    main()
