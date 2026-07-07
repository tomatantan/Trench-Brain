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


def _call(prompt, key, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048},
    }).encode("utf-8")
    r = urllib.request.urlopen(
        urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=120)
    d = json.loads(r.read())
    cands = d.get("candidates") or []
    if not cands:
        raise RuntimeError(f"応答なし（block/{d.get('promptFeedback')}）")
    parts = cands[0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts).strip()


# 判断/相場/銘柄の問いで必須の出力構造(ask_prompt.md「出力の型」)。弱いモデルが無視しがち＝
# ここで機械検証する(2026-07-07: 本番geminiが1視点531字の"雑魚"回答を返した根治。テンプレはprompt内に有ったが不服従)。
_STRUCT_MARKS = ("複数KOLレンズ", "矛盾")
_JUDGE_Q = ("どう", "買", "乗る", "避け", "仕込", "ape", "avoid", "$", "相場", "魔界", "熱い", "うごく", "動く")


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
    try:
        text = _call(prompt, key, model)
    except Exception as e:
        sys.stderr.write(f"Gemini 呼び出し失敗: {str(e)[:200]}")
        sys.exit(1)
    # ★構造の門番: 判断系の問い(promptの末尾=ユーザーの問い で近似判定)なのに多視点構造が無ければ、
    #   構造を最後尾で再強制して1回だけ再試行(それでもダメなら空を返し ask.sh の claude fallback に譲る=偽の平文を出さない)。
    tail = prompt[-400:]
    is_judge = any(k in tail for k in _JUDGE_Q)
    if is_judge and text and not all(m in text for m in _STRUCT_MARKS):
        retry = (prompt
                 + "\n\n★★あなたの前回出力は構造違反だった。必ず次の4見出しをこの通り含めよ(判断/相場/銘柄の問いだ):"
                 + "\n**複数KOLレンズ**(実在KOL2-3人・実績%付き)\n**共通点＝強い信号**\n**⚠️矛盾＝ここが学び/edge**\n**今すぐ見る1つ**"
                 + "\n内部名(kol_standouts等のデータ変数名)は出すな。1視点の買い推奨は失格。")
        try:
            text2 = _call(retry, key, model)
            if text2 and all(m in text2 for m in _STRUCT_MARKS):
                text = text2
            else:
                sys.stderr.write("Gemini 構造不服従×2 → claude fallbackへ")
                sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Gemini retry失敗: {str(e)[:200]}")
            sys.exit(1)
    if not text:
        sys.stderr.write("Gemini 空応答")
        sys.exit(1)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
