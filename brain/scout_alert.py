#!/usr/bin/env python3
"""
scout_alert.py — 能動的通知層。LLMは使わない。$0(Telegram Bot APIのみ)。

★なぜ作ったか(2026-08-06 監査で発見した穴): track.py の gate(篩)は既に「本物の門」を持ってる
  (safety_ok + traction_ok、KOL-CA ingestionは CA一致という**強い門**)。だが gate 通過は
  synth_queue.json に積まれるだけ＝次の合成サイクル(worklist処理)を待つ受動的な仕組みで、
  「3時に条件クリアしたtokenが出ても誰も気づかない」という穴があった(監査fork指摘)。
  このscriptは合成を待たず、**gate通過の瞬間**(track.py run直後)にTelegramで即通知する。

★門をさらに締める(firehose化の逆): track.py の gate 通過(TRACKED登録)全部を通知したら
  それ自体がノイズ源になる。ここでは**さらに厳しい門**＝ kol_ca が非空(=KOL がそのCAを直接
  言及した=強い門、track.pyのコメント通り)のものだけに絞る。これは pumpfun-scout skill が
  定義する「traction + 最低1 KOL mention」のKOL条件と一致する。

★判断はしない(CLAUDE.md 指針10): 「買い」等の決定語は出さない。観測事実(gate理由・KOLアカウント・
  metric)だけを報告し、「ca-check <mint> で判定を」という次の一手だけ示す。

状態: brain/state/synth_queue.json(track.pyが直近runで積んだbirths) を読み、
      brain/state/scout_alerted.json(通知済みmintの集合) で二重通知を防ぐ。
呼び出し: brain/cron_collect.sh から track.py run の直後に呼ぶ想定(このscript自体は無引数)。
"""
import json
import os
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
QUEUE = STATE / "synth_queue.json"
ALERTED = STATE / "scout_alerted.json"


def load_json(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=None), encoding="utf-8")


def format_alert(birth):
    m = birth.get("metrics") or {}
    kol_ca = birth.get("kol_ca") or []
    mcap = m.get("mcap_usd")
    mcap_s = f"${mcap:,.0f}" if isinstance(mcap, (int, float)) else "不明"
    lines = [
        f"[trench scout] {birth.get('ticker', '?')} が強い門(KOL CA言及)を通過",
        f"mint: {birth.get('mint')}",
        f"gate: {birth.get('gate')}",
        f"KOL(CA一致): {', '.join(kol_ca)}",
        f"mcap: {mcap_s} / reply: {m.get('reply_count', '不明')}",
        f"→ ca-check {birth.get('mint')} で判定を。",
    ]
    return "\n".join(lines)


def send_telegram(text):
    token = os.environ.get("TG_BOT_TOKEN")
    chat_id = os.environ.get("TG_CHAT_ID")
    if not token or not chat_id:
        print("scout_alert: TG_BOT_TOKEN/TG_CHAT_ID 未設定＝通知スキップ(コンソール出力のみ)")
        print(text)
        return False
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage", data=data
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"scout_alert: telegram送信失敗: {e}")
        return False


def main():
    queue = load_json(QUEUE, {})
    births = queue.get("births") or []
    alerted = load_json(ALERTED, {"mints": []})
    alerted_set = set(alerted.get("mints") or [])

    # ★強い門だけ通知: kol_ca(CA一致=強いKOL言及)が非空のbirthsのみ。
    #   TRACKED登録全部を通知したらノイズ源になる＝pumpfun-scout skillの
    #   「traction+最低1 KOL mention」の水準に合わせる。
    candidates = [b for b in births if b.get("kol_ca") and b.get("mint") not in alerted_set]

    sent = 0
    for b in candidates:
        if send_telegram(format_alert(b)):
            sent += 1
        alerted_set.add(b["mint"])

    save_json(ALERTED, {"mints": sorted(alerted_set)[-2000:]})  # 無限成長を防ぐ簡易キャップ
    print(f"scout_alert: births={len(births)} 強い門候補={len(candidates)} 通知={sent}")


if __name__ == "__main__":
    main()
