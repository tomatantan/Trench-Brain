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
import time
import urllib.error
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


# 一時エラー(過負荷/レート/ゲートウェイ)。Gemini は大きめの prompt でしばしば 503 を返す＝
# ここでリトライしないと公開ASKが「ask failed」で落ちる(2026-07-08 gemini専VMで503頻発の根治)。
_RETRIABLE = {429, 500, 502, 503, 504}


def _call(prompt, key, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        # maxOutputTokens は「思考(thinking)トークン込み」の上限。gemini-2.5-flash は思考モデルで
        # 内部thinkingに1700+tok使う→2048では本文が数百字で MAX_TOKENS 打ち切り＝「回答が途中で死ぬ」。
        # 思考+完全な本文が収まる様に8192へ(2026-07-08 根治)。cap なので短い回答は短いまま=コスト増えない。
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192},
    }).encode("utf-8")
    last = None
    for attempt in range(4):  # 最大4回(初回+3リトライ)、指数バックオフ
        try:
            r = urllib.request.urlopen(
                urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=120)
            d = json.loads(r.read())
            cands = d.get("candidates") or []
            if not cands:
                raise RuntimeError(f"応答なし（block/{d.get('promptFeedback')}）")
            parts = cands[0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts).strip()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in _RETRIABLE and attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError as e:  # 接続断/タイムアウトも一時扱いでリトライ
            last = e
            if attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
    raise last if last else RuntimeError("gemini call failed")


# 判断/相場/銘柄の問いで必須の出力構造(ask_prompt.md「出力の型」)。弱いモデルが無視しがち＝
# ここで機械検証する(2026-07-07: 本番geminiが1視点531字の"雑魚"回答を返した根治。テンプレはprompt内に有ったが不服従)。
# ★型B対応(2026-07-10 本人「QとAが一致してない」): 「どう動けば/分からん」系は型B(この人の行動指針)が正答＝
#   型Aの見出しを強制しない。型A/型Bどちらかの構造が有ればOK。
_STRUCT_A = ("複数KOLレンズ", "矛盾")
_STRUCT_B = ("モード", "罠")
_JUDGE_Q = ("どう", "買", "乗る", "避け", "仕込", "ape", "avoid", "$", "相場", "魔界", "熱い", "うごく", "動く", "分から", "すれば", "動け")


def _has_struct(text):
    return all(m in text for m in _STRUCT_A) or all(m in text for m in _STRUCT_B)


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
    #   構造を最後尾で再強制して1回だけ再試行。
    #   ★2026-07-08 変更: 再試行しても不服従なら「空で落として claude fallback に譲る」のは
    #   claude が居る運用者機の話。gemini専の公開VM(claude無し)では空=「ask failed」ハード失敗になる。
    #   実回答がある限り空にせず返す(構造は不完全でも本物の回答 > 失敗)。真に空の時だけ落とす。
    tail = prompt[-400:]
    is_judge = any(k in tail for k in _JUDGE_Q)
    if is_judge and text and not _has_struct(text):
        retry = (prompt
                 + "\n\n★★あなたの前回出力は構造違反だった。問いのタイプで型を選び、必ずその見出しを含めよ:"
                 + "\n型A(銘柄/相場の判断): **複数KOLレンズ**(実在KOL2-3人・実績%付き)/**共通点＝強い信号**/**⚠️矛盾＝ここが学び/edge**/**今すぐ見る1つ**"
                 + "\n型B(この人がどう動くかの相談=「どう動けば/分からん」系): **今のあなたの正しいモード**/**今日やる3つ**/**勝者ならこうする**/**⚠️今のあなたの罠**"
                 + "\n内部名(kol_standouts/traction_candidates等のデータ変数名)は出すな。1視点の買い推奨・相場解説だけの型B回答は失格。")
        try:
            text2 = _call(retry, key, model)
            if text2 and _has_struct(text2):
                text = text2          # 構造遵守=採用
            elif text2:
                text = text2          # 構造不完全でも再試行の方が濃いので採用(空にしない)
        except Exception as e:
            # 再試行が失敗しても初回の text を維持(空にしない)
            sys.stderr.write(f"Gemini retry失敗(初回回答で継続): {str(e)[:200]}")
    if not text:
        sys.stderr.write("Gemini 空応答")
        sys.exit(1)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
