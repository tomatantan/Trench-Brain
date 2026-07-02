#!/usr/bin/env python3
"""
live_pulse_writer.py — リアルタイム pump trend store(LLM Wiki と分離・速い鮮度)

launch_pulse.py(pump.fun keyless 集約・決定的)を一定間隔で回し、
brain/state/live_pulse.json に最新スナップショットを書く:
  flow件数 / scam率 / theme分布 / traction候補(live mcap+変化%) / death分母。
UI は ui_server の GET /api/live でこれを読む。

★設計(本人 2026-06-28): 「遅い知恵(Wiki・3h合成)」と「速い鮮度(pump real-time)」を分離。
  これは後者=数分間隔で更新される別レイヤー。wiki markdown には触れない。

前提: launch_stream.py が常駐し launch_queue.jsonl に新規launchを流している事。
      それが無いと flow=0(観測が動いてない)。常時ONホスト(Windows)で
      launch_stream と一緒に回す。state は gitignore=local(machine毎)。

起動: python3 brain/live_pulse_writer.py [--interval 120] [--once]
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brain" / "state" / "live_pulse.json"
PULSE = ROOT / "brain" / "launch_pulse.py"


def snapshot():
    r = subprocess.run(
        ["python3", str(PULSE)], capture_output=True, text=True, timeout=150, cwd=str(ROOT)
    )
    if r.returncode != 0:
        print(f"live_pulse: launch_pulse.py rc={r.returncode}: {(r.stderr or '')[:200]}", file=sys.stderr)
        return None
    try:
        data = json.loads(r.stdout)
    except ValueError:
        print("live_pulse: launch_pulse.py stdout がJSONでない(skip)", file=sys.stderr)
        return None
    data["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=120, help="更新間隔(秒)")
    ap.add_argument("--once", action="store_true", help="1回だけ書いて終了")
    args = ap.parse_args()
    while True:
        try:
            d = snapshot()
        except Exception as e:
            print(f"live_pulse error: {type(e).__name__}: {e}")
            d = None
        if d is not None:
            print(
                f"live_pulse updated: flow={d.get('flow_count_nonscam')} "
                f"traction={len(d.get('traction_candidates', []))} @ {d['generated_at']}"
            )
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
