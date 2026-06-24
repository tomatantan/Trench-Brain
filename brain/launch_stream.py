#!/usr/bin/env python3
"""
launch_stream.py — pump.fun 新規ローンチを**リアルタイム検知→launch時に即ふるい→通過分を流し合成キューへ**。

本人設計(2026-06-23): 「ローンチを検知したらすぐふるいにかける。湯水のように流れてくるトークンを合成しつづける」。
旧 track.py の「3hサンプル + mcap≥$30k門(=噴くまで待つ=lagging)」を廃し、**出来立てを即・安全性で濾す**。

ふるい(mcap門でなく "scamれるか + 過去 + 板 + 社会 + メタ"):
  ① scam可能性(RugCheck): mint/freeze authority 放棄済か・rugged か・LP・danger risk
  ② creator の rug履歴(RugCheck creatorTokens / creatorBalance)
  ④ 初動の買い方: top holder 集中%・insiderNetworks/graphInsiders(sniper/bundle)
  ⑤ メタ質: name + socials(twitter/website)
  ③ KOL言及: sources/x に CA(mint) が出てるか(出てたら最優先 PASS)
通過 → brain/state/launch_queue.jsonl に1行追記(=流し合成の入力)。観測≠採用は不変(通過分だけ採用)。

★firehoseでない: 「安全 × 何かしらの signal」で薄く濾す＝指針2の門を launch時に置いただけ。scam/junk は落ちる。
常駐daemon(cron が自己修復で起こす)。RugCheck/pump.fun は keyless。stdlib のみ。

env: LS_POLL_SEC(既定60) / LS_TOP_PCT_MAX(既定35) / LS_SCORE_MAX(既定2500) / LS_RUGCHECK_PER_CYCLE(既定40)
"""
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRCX = ROOT / "sources" / "x"
STATE = ROOT / "brain" / "state"
SEEN = STATE / "launch_seen.txt"
QUEUE = STATE / "launch_queue.jsonl"
LOG = STATE / "launch_stream.log"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

POLL = int(os.environ.get("LS_POLL_SEC", "60"))
TOP_PCT_MAX = float(os.environ.get("LS_TOP_PCT_MAX", "35"))   # 最大holder集中%上限(超=薄い板/集中=落とす)
SCORE_MAX = float(os.environ.get("LS_SCORE_MAX", "2500"))      # RugCheck score(高=危険)上限
RC_PER_CYCLE = int(os.environ.get("LS_RUGCHECK_PER_CYCLE", "40"))  # 1周でRugCheckする最大数(rate保護)
PAGES = int(os.environ.get("LS_PAGES", "4"))                   # newest 何ページ(50/page)


def _get(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {msg}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_seen():
    if not SEEN.exists():
        return set()
    return set(SEEN.read_text(encoding="utf-8").split())


def save_seen(seen):
    # 直近 12000 mint だけ保持(無限肥大防止)
    arr = list(seen)[-12000:]
    SEEN.write_text("\n".join(arr) + "\n", encoding="utf-8")


def fetch_newest():
    out = []
    for i in range(PAGES):
        try:
            d = _get("https://frontend-api-v3.pump.fun/coins?"
                     f"offset={i*50}&limit=50&sort=created_timestamp&order=DESC&includeNsfw=false")
            if not d:
                break
            out.extend(d)
        except Exception as e:
            log(f"newest fetch err p{i}: {type(e).__name__}")
            break
    return out


def prefilter(c):
    """⑤メタ質の安価な事前ふるい: 名前 + socials(twitter or website)。no-effort junk を落とす。"""
    name = (c.get("name") or "").strip()
    sym = (c.get("symbol") or "").strip()
    has_social = bool(c.get("twitter") or c.get("website") or c.get("telegram"))
    return bool(name and sym and has_social)


def rugcheck(mint):
    """①scam可能性 ②creator履歴 ④板/insider を1発で。"""
    try:
        d = _get(f"https://api.rugcheck.xyz/v1/tokens/{mint}/report", timeout=15)
    except Exception as e:
        return None
    th = d.get("topHolders") or []
    top_pct = max((h.get("pct") or 0) for h in th) if th else 0
    risks = d.get("risks") or []
    danger = [r.get("name") for r in risks if (r.get("level") == "danger")]
    return {
        "mint_auth": d.get("mintAuthority"),
        "freeze_auth": d.get("freezeAuthority"),
        "rugged": bool(d.get("rugged")),
        "score": d.get("score") or 0,
        "score_norm": d.get("score_normalised"),
        "top_pct": top_pct,
        "danger": danger,
        "n_risks": len(risks),
        "creator_tokens": len(d.get("creatorTokens") or []),
        "insiders": bool(d.get("insiderNetworks")) or bool(d.get("graphInsidersDetected")),
        "lp_providers": d.get("totalLPProviders"),
    }


# CA(mint)が sources/x に出てるか= KOL言及(③)。直近ファイルだけ走査(安価)。
_kol_cache = {"t": 0, "text": ""}
def kol_blob():
    now = time.time()
    if now - _kol_cache["t"] > 300:  # 5分キャッシュ
        buf = []
        files = sorted(SRCX.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:800]
        for p in files:
            try:
                buf.append(p.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                pass
        _kol_cache["text"] = "\n".join(buf)
        _kol_cache["t"] = now
    return _kol_cache["text"]


# ★"わかりやすいscam"だけ弾く(本人2026-06-23): freeze/mint authority・honeypot/売れない・creator-rug履歴。
#   構造的な集中%等(出来立てで普通に高い)は弾かない＝湯水を素通しに近く流す。
CLEAR_SCAM_KEYS = ("honeypot", "freeze", "cannot sell", "can't sell", "transfer fee",
                   "creator history of rugged", "scam", "blacklist", "mint authority")

def sieve(c, rc, dup_count=0):
    """scam門=明白なやつだけ。freeze/mint authority・honeypot・creator-rug・copycat を弾く。
    返り=(passed:bool, reason:str, kol:bool)。"""
    mint = c.get("mint")
    kol = mint in kol_blob() if mint else False
    if rc is None:
        return (False, "rugcheck-none", kol)
    if rc["rugged"]:
        return (False, "rugged", kol)
    # ① 明白: authority未放棄(無限mint/凍結できる)=即scam
    if rc["mint_auth"] or rc["freeze_auth"]:
        return (False, "authority未放棄(freeze/mint可)", kol)
    # 明白なscam danger のみ(honeypot/売れない/creator-rug履歴)。集中%等の構造danger は弾かない。
    clear = [dr for dr in rc["danger"] if any(k in dr.lower() for k in CLEAR_SCAM_KEYS)]
    if clear:
        return (False, f"scam:{clear[0]}", kol)
    # 同名copycat spam(QUANTUM×5等)=わかりやすいjunk。
    if dup_count >= 3:
        return (False, f"copycat重複x{dup_count}", kol)
    reason = "KOL言及+非scam" if kol else "非scam(clean launch)"
    return (True, reason, kol)


def enqueue(c, rc, reason, kol):
    rec = {
        "mint": c.get("mint"), "symbol": c.get("symbol"), "name": c.get("name"),
        "creator": c.get("creator"), "created": c.get("created_timestamp"),
        "twitter": c.get("twitter"), "website": c.get("website"),
        "usd_mcap": c.get("usd_market_cap"), "reply": c.get("reply_count"),
        "rc_score": rc.get("score"), "top_pct": round(rc.get("top_pct", 0), 1),
        "creator_tokens": rc.get("creator_tokens"), "insiders": rc.get("insiders"),
        "kol": kol, "reason": reason, "detected_at": int(time.time()),
    }
    with open(QUEUE, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def one_cycle(seen):
    coins = fetch_newest()
    new = [c for c in coins if c.get("mint") and c.get("mint") not in seen]
    meta = [c for c in new if prefilter(c)]
    # copycat検出: この周回で同じsymbolが何回出てるか(spam=同名連発)
    from collections import Counter
    symcount = Counter((c.get("symbol") or "").lower() for c in new)
    passed = 0
    rc_done = 0
    for c in meta:
        if rc_done >= RC_PER_CYCLE:
            break
        rc = rugcheck(c["mint"])
        rc_done += 1
        ok, reason, kol = sieve(c, rc, symcount.get((c.get("symbol") or "").lower(), 0))
        if ok:
            enqueue(c, rc, reason, kol)
            passed += 1
            log(f"PASS {c.get('symbol')} ({reason}) top%={rc.get('top_pct',0):.0f} score={rc.get('score')} kol={kol}")
        time.sleep(0.25)  # RugCheck rate保護
    for c in new:
        seen.add(c["mint"])
    log(f"cycle: newest{len(coins)} new{len(new)} meta通過{len(meta)} rugcheck{rc_done} → PASS{passed}")
    _bump_stats(observed=len(new), meta=len(meta), rugchecked=rc_done, passed=passed,
                rejected=max(0, rc_done - passed))
    return passed


def _bump_stats(**delta):
    """scam率/通過率の累積stat(launch_pulse が読む)。"""
    f = STATE / "launch_stats.json"
    try:
        s = json.loads(f.read_text()) if f.exists() else {}
    except Exception:
        s = {}
    for k, v in delta.items():
        s[k] = s.get(k, 0) + v
    f.write_text(json.dumps(s), encoding="utf-8")


import subprocess
DRAIN_EVERY = int(os.environ.get("LS_DRAIN_EVERY", "15"))  # 何周毎に連続合成drainを回すか(~15min)

def spawn_drain():
    """launch_synth.sh を背景spawn(非blocking)。多重起動は避ける。"""
    try:
        running = subprocess.run(["pgrep", "-f", "launch_synth.sh"],
                                 capture_output=True).returncode == 0
        if running:
            return
        subprocess.Popen(["bash", str(ROOT / "brain" / "launch_synth.sh")],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("drain spawn(連続合成)")
    except Exception as e:
        log(f"drain spawn err: {type(e).__name__}")


def run_track():
    """死の分母tracker(track.py)を背景実行=launchd cron非依存でbase_rate鮮度を保つ(監査2026-06-24 重大1)。
    cron未発火(Mac sleep等)でも daemon が回ってる限り base_rate が凍結しない。多重起動はguard。"""
    try:
        if subprocess.run(["pgrep", "-f", "brain/track.py"], capture_output=True).returncode == 0:
            return
        subprocess.Popen([sys.executable, str(ROOT / "brain" / "track.py"), "run"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("track.py 背景実行(死の分母更新=launchd非依存)")
    except Exception as e:
        log(f"track spawn err: {type(e).__name__}")


def main():
    STATE.mkdir(parents=True, exist_ok=True)
    seen = load_seen()
    log(f"launch_stream 起動 (poll={POLL}s drain毎{DRAIN_EVERY}周 seen既知{len(seen)})")
    cyc = 0
    while True:
        try:
            one_cycle(seen)
            cyc += 1
            if cyc % 10 == 0:
                save_seen(seen)
            if cyc % DRAIN_EVERY == 0:
                run_track()          # 死の分母を launchd非依存で更新(凍結防止)
                spawn_drain()        # 連続合成: 定期的に queue を drain(背景・throughput分だけ)
        except Exception as e:
            log(f"cycle err: {type(e).__name__}: {e}")
        time.sleep(POLL)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        s = load_seen(); one_cycle(s); save_seen(s)
    else:
        main()
