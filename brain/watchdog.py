#!/usr/bin/env python3
"""
watchdog.py — Trench-Brain 公開スタックの死活監視（信頼性の土台・silent fail を潰す）。

serve.sh が起動する writer/tunnel/ui_server と、live_pulse鮮度・合成backlog を定期check。
**失敗↔回復の flip を検知**して telegram通知（.env に TG_BOT_TOKEN / TG_CHAT_ID があれば）＋
`brain/state/watchdog_status.json`（現状）＋`brain/state/watchdog.log`（履歴）。

使い方: python3 brain/watchdog.py [--interval 120] [--port 8000] [--fresh-min 15] [--backlog-max 50] [--once]
serve.sh に同梱起動される（独立でも可）。stdlib のみ・read-only。
"""
import argparse
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"


def _env(key):
    try:
        for ln in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if ln.startswith(key + "="):
                return ln.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


def _get(url, timeout=10):
    try:
        return urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "trench-watchdog"}), timeout=timeout).read()
    except Exception:
        return None


def _json_get(url):
    b = _get(url)
    try:
        return json.loads(b) if b else None
    except Exception:
        return None


def _age_min(v):
    """ISO文字列 or epoch(秒/ms) → 経過分。読めなければ巨大値。"""
    now = time.time()
    try:
        s = str(v)
        if s.replace(".", "").isdigit():
            t = float(v)
            if t > 1e11:  # ミリ秒
                t /= 1000
            return (now - t) / 60
        return (now - datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()) / 60
    except Exception:
        return 1e9


def _state_json(name, default=None):
    try:
        return json.loads((STATE / name).read_text(encoding="utf-8"))
    except Exception:
        return default


def _tail_last(name):
    try:
        p = STATE / name
        with open(p, "rb") as f:
            f.seek(max(0, p.stat().st_size - 8192))
            lines = [x for x in f.read().decode("utf-8", "replace").splitlines() if x.strip()]
        return json.loads(lines[-1]) if lines else None
    except Exception:
        return None


def run_checks(port, fresh_min, backlog_max):
    res = {}
    # 1) ui_server 応答
    d = _json_get(f"http://127.0.0.1:{port}/api/index")
    res["ui_server"] = (bool(d and d.get("ok")), f"{(d or {}).get('count', '?')}機能")
    # 2) live_pulse 鮮度（live_pulse_writer 死活）
    lp = _state_json("live_pulse.json", {}) or {}
    age = _age_min(lp.get("generated_at")) if lp.get("generated_at") else 1e9
    res["live_pulse"] = (age < fresh_min, f"{age:.0f}分前" if age < 1e8 else "無/古")
    # 3) launch_stream 死活（launch_queue の最新 detected_at）
    lq = _tail_last("launch_queue.jsonl")
    lage = _age_min(lq.get("detected_at")) if lq else 1e9
    res["launch_stream"] = (lage < fresh_min, f"{lage:.0f}分前" if lage < 1e8 else "無/古")
    # 4) public tunnel（公開URL到達）
    url = ""
    try:
        url = (STATE / "public_url.txt").read_text(encoding="utf-8").strip()
    except Exception:
        pass
    if url:
        res["public_tunnel"] = (bool(_get(f"{url}/api/index", timeout=15)), url)
    else:
        res["public_tunnel"] = (True, "URL未記録(skip)")
    # 5) 合成backlog（scraper化=収集が合成を追い越す検知）
    h = _tail_last("health.jsonl")
    bl = (h or {}).get("signal_backlog")
    res["synthesis"] = (bl is None or bl < backlog_max, f"backlog {bl}")
    return res


def telegram(msg):
    # bot は .env の TG_WIKI_BOT_TOKEN（既存の wiki_bot を流用）。送り先は TG_CHAT_ID(=自分のチャットID)。
    # 通知を有効化するには .env に TG_CHAT_ID=<自分のchat_id> を追加するだけ（token は既にある）。
    tok = _env("TG_WIKI_BOT_TOKEN") or _env("TG_BOT_TOKEN")
    chat = _env("TG_CHAT_ID") or _env("TG_WIKI_CHAT_ID")
    if not tok or not chat:
        return
    try:
        data = urllib.parse.urlencode({"chat_id": chat, "text": msg}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data=data, timeout=10)
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=120)
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--fresh-min", type=int, default=15)
    ap.add_argument("--backlog-max", type=int, default=50)
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args()
    prev = {}
    while True:
        res = run_checks(a.port, a.fresh_min, a.backlog_max)
        allok = all(v[0] for v in res.values())
        status = {"ts": datetime.utcnow().isoformat() + "Z", "all_ok": allok,
                  "checks": {k: {"ok": v[0], "detail": v[1]} for k, v in res.items()}}
        try:
            (STATE / "watchdog_status.json").write_text(json.dumps(status, ensure_ascii=False, indent=1), encoding="utf-8")
            with open(STATE / "watchdog.log", "a", encoding="utf-8") as f:
                f.write(datetime.utcnow().strftime("%m-%d %H:%M") + (" OK " if allok else " !! ")
                        + " ".join(f"{k}={'o' if v[0] else 'X'}" for k, v in res.items()) + "\n")
        except Exception:
            pass
        # flip（死↔復活）検知で通知＝spam しない / 初回 DOWN は即通知
        for k, (ok, detail) in res.items():
            if k not in prev:
                if not ok:
                    telegram(f"[trench watchdog] {k} 初期DOWN ⚠️（{detail}）")
            elif prev[k] != ok:
                telegram(f"[trench watchdog] {k} {'復活 ✅' if ok else '死亡 ⚠️'}（{detail}）")
            prev[k] = ok
        if a.once:
            print(json.dumps(status, ensure_ascii=False, indent=1))
            break
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
