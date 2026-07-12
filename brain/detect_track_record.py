#!/usr/bin/env python3
"""detect_track_record.py — 外部検知bot(猫太郎bot/Smart Wallet等)の成績表 (2026-07-12 本人承認済の提案).

検知シグナルを「出た」で終わらせず「当たるのか」を機械で採点する:
- 検知の実体(detections.jsonl)は serving機(VM)ローカル＝合成脳には届かない
  → 公開API(GET /api/detections)から pull して brain/state/detect_history.json に累積(id dedupe・append-only)。
- 各検知CAの現outcome(pump.fun mcap)を kol_track_record.py と同じ判定・同じ ca_outcome_cache.json で照合(cache共有=タダ)。
- 集計は source×verdict 単位:
    REVIEW/CALL系 → death_rate 低いほど「拾いが良い」
    AVOID        → death_rate 高いほど「避けが当たってる」(=正解率として読む)
- 出力: brain/state/detect_track_records.json（ask.sh が読み、回答で検知に重みを付ける）。
決定的・LLM不使用・bounded。cron_collect から毎サイクル(kol_track_record の後)。失敗しても他を壊さない。
"""
import json
import os
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
HISTORY = STATE / "detect_history.json"
OUT = STATE / "detect_track_records.json"
CACHE = STATE / "ca_outcome_cache.json"   # kol_track_record.py と共有
API = os.environ.get("DETECT_API", "https://trenchbrain.fun/api/detections?include_avoids=1&n=500")
DEAD_MCAP = 12_000
OUTCOME_TTL = 6 * 3600
MAX_CA = 120  # bounded(kolの200と別枠・合計負荷を抑える)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def _fresh(entry):
    if entry.get("outcome") == "dead":
        return True
    return (time.time() - entry.get("ts", 0)) < OUTCOME_TTL


def pf_mcap(ca):
    """(mcap, transient)。kol_track_record.py と同じ transient 規約。"""
    try:
        u = f"https://frontend-api-v3.pump.fun/coins/{ca}"
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10).read())
        return d.get("usd_market_cap"), False
    except urllib.error.HTTPError as e:
        return None, e.code != 404
    except Exception:
        return None, True


def dex_mcap(ca):
    """EVM CA(0x)版のoutcome取得(2026-07-12)。pf_mcapはpump.fun専用でEVMは常に404になるため、
    dexscreenerの汎用tokensエンドポイントで代替。kol_track_record.py の同名関数と同じ規約
    (このファイルは自己完結を優先し小さな重複を許容=INGEST規約の外側なので依存を増やさない)。"""
    try:
        u = f"https://api.dexscreener.com/latest/dex/tokens/{ca}"
        d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=10).read())
        pairs = (d or {}).get("pairs") or []
        if not pairs:
            return None, False
        p0 = max(pairs, key=lambda p: ((p.get("liquidity") or {}).get("usd") or 0))
        return p0.get("marketCap") or p0.get("fdv"), False
    except urllib.error.HTTPError as e:
        return None, e.code != 404
    except Exception:
        return None, True


def _load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _atomic_write(path, obj):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def main():
    # 1) API から検知を pull → 履歴に累積(dedupe by id)。API失敗時は既存履歴だけで採点継続。
    hist = _load(HISTORY, {})
    try:
        d = json.loads(urllib.request.urlopen(
            urllib.request.Request(API, headers={"User-Agent": UA}), timeout=20).read())
        for det in d.get("detections") or []:
            did = det.get("id")
            if not did or did in hist:
                continue
            hist[did] = {"source": det.get("source") or "?",
                         "verdict": (det.get("verdict") or "?").upper(),
                         "type": det.get("type") or "?",
                         "ca": det.get("ca") or det.get("mint") or "",
                         "symbol": det.get("symbol") or det.get("name") or "?"}
        _atomic_write(HISTORY, hist)
    except Exception as e:  # noqa: BLE001
        print(f"detect-tr: API pull失敗({type(e).__name__})→既存履歴{len(hist)}件で継続")

    if not hist:
        print("detect-tr: 検知履歴なし=何もしない")
        return

    # 2) outcome照合(cache共有・bounded・transientはcacheしない)
    cache = _load(CACHE, {})
    cas = {v["ca"] for v in hist.values() if v.get("ca")}
    looked = 0
    for ca in cas:
        if ca in cache and _fresh(cache[ca]):
            continue
        if looked >= MAX_CA:
            break
        mc, transient = dex_mcap(ca) if ca.startswith("0x") else pf_mcap(ca)
        looked += 1
        if transient:
            time.sleep(0.15)
            continue
        if mc is None:
            cache[ca] = {"outcome": "unknown", "mcap": None, "ts": time.time()}
        else:
            cache[ca] = {"outcome": ("dead" if mc < DEAD_MCAP else "alive"), "mcap": round(mc), "ts": time.time()}
        time.sleep(0.15)
    _atomic_write(CACHE, cache)

    # 3) source×verdict 集計
    buckets = defaultdict(lambda: {"n": 0, "dead": 0, "alive": 0, "unknown": 0})
    for v in hist.values():
        key = f"{v['source']}:{v['verdict']}"
        b = buckets[key]
        b["n"] += 1
        oc = (cache.get(v.get("ca") or "") or {}).get("outcome") or "unknown"
        b[oc if oc in ("dead", "alive") else "unknown"] += 1
    recs = {}
    for key, b in buckets.items():
        evaluated = b["dead"] + b["alive"]
        recs[key] = {**b, "evaluated": evaluated,
                     "death_rate": (round(100 * b["dead"] / evaluated) if evaluated else None)}
    _atomic_write(OUT, {"updated": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
                        "note": "AVOIDはdeath_rate高=避けが当たってる/REVIEW系は低=拾いが良い",
                        "records": recs})
    print("detect-tr: " + " / ".join(
        f"{k}: {v['evaluated']}件評価中 死{v['death_rate']}%" for k, v in sorted(recs.items()) if v["evaluated"]))


if __name__ == "__main__":
    main()
