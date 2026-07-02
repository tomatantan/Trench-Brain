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
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK = ROOT / "wiki" / "entities" / "tokens"
CONCEPTS = ROOT / "wiki" / "concepts"
STATE = ROOT / "brain" / "state"
OUT = ROOT / "wiki" / "ui-data.json"

MACRO = {"$BTC", "$ETH", "$SOL", "$USDC", "$USDT", "$HYPE", "$BNB", "$XRP", "$DOGE"}
PALETTE = {"MACRO": "#28e1f2", "WORLD": "#ff4ba8", "MEME": "#48eca0", "TOKEN": "#ffb749"}


def fm_and_body(p):
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return {}, t
    parts = t.split("---", 2)
    if len(parts) < 3:
        return {}, t   # 同上(2026-07-02 M1)
    _, fm, body = parts
    m = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            m[k.strip()] = v.strip()
    return m, body


def track_data():
    """brain/track.py の状態(launch lifecycle)を UI 用に整形。
    live[] = TRACKED/dead トークンのライフサイクル, base_rate = 生存者バイアスの分母。
    (state は gitignore=local だが、ここで ui-data.json に焼くので UIチームに渡る)"""
    def _load(p):
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    tracked = _load(STATE / "tracked.json")
    base = _load(STATE / "base_rate.json")
    SC = {"tracked": "#48eca0", "dead": "#5a6472", "retired": "#5a6472"}
    live = []
    for mint, v in tracked.items():
        last = v.get("last", {})
        outcome = v.get("outcome")
        status = v.get("status", "tracked")
        live.append({
            "ticker": v.get("ticker"), "name": v.get("name"), "mint": mint,
            "mcap": round(last.get("mcap_usd", 0)),
            "peak_mcap": round(v.get("peak_mcap", 0)),
            "status": status, "outcome": outcome,
            "color": "#ffb749" if outcome == "graduated" else SC.get(status, "#48eca0"),
            "gate": v.get("gate"), "kol": v.get("kol_ca", []),
            "ai_agent": v.get("tokenized_agent", False),
            "reply_count": last.get("reply_count", 0),
            "first_seen": v.get("first_seen"), "died_at": v.get("died_at"),
            "link": f"https://pump.fun/coin/{mint}",
            "spark": [round(h.get("mcap_usd", 0)) for h in v.get("history", [])][-24:],
        })
    # 生存中→mcap降順、その後 dead。UIは上から「今アツい/最近死んだ」を出せる。
    live.sort(key=lambda x: (x["status"] != "tracked", -x["mcap"]))
    pr = (base.get("gate_passed", 0) / base.get("mints_seen", 1)) if base.get("mints_seen") else 0
    return live[:60], {
        "mints_seen": base.get("mints_seen", 0),
        "gate_passed": base.get("gate_passed", 0),
        "died": base.get("died", 0),
        "graduated": base.get("graduated", 0),
        "pass_rate_pct": round(pr * 100, 2),
        "note": "全mint観測→篩通過率。生存者バイアスの分母(launchpad-economics の実測)。",
    }


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

    live, base_rate = track_data()   # launch pipeline のライブ層

    OUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generated_for": "trench-brain UI (泡=signal / click=SIGNAL TRACE / live=launch radar)",
        "schema": ("signals[]: concept由来の泡 {type,title,size,color,glow,trace} / "
                   "live[]: launch lifecycle {ticker,name,mcap,peak_mcap,status,outcome,color,"
                   "gate,kol[],ai_agent,spark[],link} / base_rate: 篩通過率(生存者バイアスの分母)"),
        "count": len(signals),
        "signals": signals,
        "live": live,
        "base_rate": base_rate,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"ui-data.json: {len(signals)} signals + {len(live)} live "
          f"(base_rate pass {base_rate['pass_rate_pct']}%) -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
