#!/usr/bin/env python3
"""
ask_window_client.py — VM の ask.sh から、ローカル(Windows)のサブスク Haiku 窓口
(ask.trenchbrain.fun)を叩く薄いクライアント(2026-07-10)。

stdin から組み立て済み PROMPT を受け、ASK_WINDOW_URL に POST。窓口(=Windows)が起動してれば
Haiku の合成回答を stdout に返す。Windows が落ちてれば Cloudflare が即エラーを返す→例外→**空を出力**
→ ask.sh 側が Gemini に自動フォールバック(サービスは死なない)。

env: ASK_WINDOW_URL(必須。未設定なら即空=Geminiへ)
     ASK_WINDOW_MODEL(任意。窓口側の既定=haiku)
"""
import json
import os
import sys
import urllib.request

URL = os.environ.get("ASK_WINDOW_URL", "").strip()
MODEL = os.environ.get("ASK_WINDOW_MODEL", "").strip()
TIMEOUT = 200  # claude 合成は数十秒〜。Windows落ち時は Cloudflare が即エラーで返すので待ち続けない。


def main():
    if not URL:
        return  # 未設定 → 空 → Gemini
    prompt = sys.stdin.read()
    if not prompt.strip():
        return
    payload = {"prompt": prompt}
    if MODEL:
        payload["model"] = MODEL
    body = json.dumps(payload).encode("utf-8")
    # ★User-Agent 必須: 既定の "Python-urllib/x.y" は Cloudflare にボット判定され 403。
    #   通常の UA を名乗ると通る(2026-07-10 判明)。
    headers = {"Content-Type": "application/json", "User-Agent": "trench-vm/1.0"}
    try:
        r = urllib.request.urlopen(
            urllib.request.Request(URL, data=body, headers=headers),
            timeout=TIMEOUT)
        d = json.loads(r.read())
        ans = (d.get("answer") or "").strip() if d.get("ok") else ""
    except Exception:
        ans = ""   # 到達不能/タイムアウト/エラー = 静かに空 → Gemini fallback
    if ans:
        sys.stdout.write(ans)


if __name__ == "__main__":
    main()
