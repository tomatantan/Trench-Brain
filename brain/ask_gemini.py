#!/usr/bin/env python3
"""
ask_gemini.py — ask.sh の Gemini backend（公開ASK用・無料・$0・GPU負荷ゼロ）。

stdin から組み立て済み PROMPT を受け、Gemini 2.5-flash で合成回答を stdout に返す。
GEMINI_API_KEY を 環境変数 か .env から読む（.env は gitignore=マシン毎に設定）。
サブスク claude を公開に使わない（ToS）ための、公開向け脳。運用者の深いQ&Aは ask.sh 既定(claude)のまま。

使い方: printf '%s' "$PROMPT" | python3 brain/ask_gemini.py
env: GEMINI_API_KEY(必須) / GEMINI_MODEL(既定 gemini-2.5-flash)
"""
import json
import os
import sys
import urllib.request
from pathlib import Path


def _key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if k:
        return k
    try:
        for ln in (Path(__file__).resolve().parent.parent / ".env").read_text(encoding="utf-8").splitlines():
            if ln.startswith("GEMINI_API_KEY="):
                return ln.split("=", 1)[1].strip()
    except Exception:
        pass
    return ""


def main():
    prompt = sys.stdin.read()
    if not prompt.strip():
        sys.stderr.write("空 prompt")
        sys.exit(1)
    key = _key()
    if not key:
        sys.stderr.write("GEMINI_API_KEY 未設定（環境変数か .env に GEMINI_API_KEY=... を入れて）")
        sys.exit(1)
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048},
    }).encode("utf-8")
    try:
        r = urllib.request.urlopen(
            urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=120)
        d = json.loads(r.read())
    except Exception as e:
        sys.stderr.write(f"Gemini 呼び出し失敗: {str(e)[:200]}")
        sys.exit(1)
    # candidates 無し＝safetyブロック等 → 正直にエラー(捏造しない)
    cands = d.get("candidates") or []
    if not cands:
        sys.stderr.write(f"Gemini 応答なし（block/{d.get('promptFeedback')}）")
        sys.exit(1)
    try:
        parts = cands[0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts).strip()
    except Exception:
        text = ""
    if not text:
        sys.stderr.write("Gemini 空応答")
        sys.exit(1)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
