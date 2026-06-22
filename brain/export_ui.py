#!/usr/bin/env python3
"""
Trench-Brain → UI 連携エクスポータ。

wiki/entities/tokens と wiki/concepts を読んで、UI(泡＋SIGNAL TRACE)が消費する
JSON を `wiki/ui-data.json` に書き出す。UI側はこの配列を fetch して泡を描画する。

各 signal:
  { type, title, size, color, glow, trace:{ why, accounts, top, causal, confidence } }
  size/glow = 言及数×アカ数×エンゲージのスケール（=memetic potentialの近似）
  trace = ドロワー(なぜ浮上+CAUSAL CHAIN+confidence)用
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK = ROOT / "wiki" / "entities" / "tokens"
CONCEPTS = ROOT / "wiki" / "concepts"
OUT = ROOT / "wiki" / "ui-data.json"

MACRO = {"$BTC", "$ETH", "$SOL", "$USDC", "$USDT", "$HYPE", "$BNB", "$XRP", "$DOGE"}
PALETTE = {"MACRO": "#28e1f2", "WORLD": "#ff4ba8", "MEME": "#48eca0", "TOKEN": "#ffb749"}


def fm_and_body(p):
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return {}, t
    _, fm, body = t.split("---", 2)
    m = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            m[k.strip()] = v.strip()
    return m, body


def main():
    # concept側: どのtickerがどの動線/型に属すか
    concept_links = {}   # TICKER -> [concept titles]
    for c in CONCEPTS.glob("*.md"):
        m, body = fm_and_body(c)
        title = m.get("title", c.stem)
        for tk in set(re.findall(r"\[\[(\$[A-Za-z][A-Za-z0-9]{1,9})\]\]", body)):
            concept_links.setdefault(tk.upper(), []).append(title)

    signals = []
    for p in TOK.glob("*.md"):
        m, body = fm_and_body(p)
        tk = m.get("title", p.stem)
        mentions = int(m.get("mentions", 0) or 0)
        accounts = int(m.get("accounts", 0) or 0)
        # 高エンゲージ表からtop抽出
        top = []
        for row in re.findall(r"^\| ([\d,]+) \| \[\[@([^\]]+)\]\] \| (.+?) \| ", body, re.M):
            likes = int(row[0].replace(",", ""))
            top.append({"likes": likes, "account": row[1], "text": row[2].strip()})
        top = sorted(top, key=lambda x: -x["likes"])[:5]
        eng = sum(t["likes"] for t in top)
        # synthesis(confidence/物語)
        syn = ""
        ms = re.search(r"<!-- synthesis:start -->(.*?)<!-- synthesis:end -->", body, re.S)
        if ms and "未記入" not in ms.group(1):
            syn = ms.group(1).strip()
        conf = "—"
        mc = re.search(r"confidence\s*=\s*([^\s。/]+)", syn)
        if mc:
            conf = mc.group(1)

        cat = "MACRO" if tk.upper() in MACRO else ("WORLD" if tk.upper() in concept_links else "MEME")
        # サイズ: 言及×アカ×エンゲージの合成を 60-130 に正規化(近似)
        score = mentions * 2 + accounts * 4 + min(eng // 500, 40)
        size = max(60, min(130, 60 + score))

        signals.append({
            "type": cat,
            "title": tk,
            "size": size,
            "color": PALETTE[cat],
            "glow": round(min(1.0, score / 80), 2),
            "mentions": mentions,
            "accounts": accounts,
            "trace": {
                "why": f"{mentions}件の言及 / {accounts}アカ / 高エンゲージ計{eng:,}♥",
                "accounts_n": accounts,
                "top": top,
                "causal": concept_links.get(tk.upper(), []),
                "confidence": conf,
                "synthesized": bool(syn),
            },
        })

    signals.sort(key=lambda s: -s["size"])
    signals = signals[:40]
    OUT.write_text(json.dumps({
        "generated_for": "trench-brain UI (泡=signal / click=SIGNAL TRACE)",
        "schema": "signals[]: {type,title,size,color,glow,trace:{why,top[],causal[],confidence}}",
        "count": len(signals),
        "signals": signals,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ui-data.json: {len(signals)} signals -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
