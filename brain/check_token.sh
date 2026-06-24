#!/bin/bash
# check_token.sh — 魔界スクリーニング。CA(or pump.fun URL)を投げたら ape/avoid を live で判定。
# 本人の実トレード(Sol魔界)の core decision。scam門(RugCheck)+pump.funデータ+KOL-CA照合 を集め、
# headless claude が wiki型(rug-anatomy/launchpad/survivor/feedback)と束ねて「乗る/避ける+理由+⚠️+確信度」。
# read-only(wiki編集しない)・--strict-mcp-config。将来 bot の /check $CA に繋ぐ。
set -euo pipefail
cd /Users/toma/trench-brain
export PATH="/usr/bin:/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
MODEL="${CHECK_MODEL:-sonnet}"
ARG="${*:-}"
CA="$(printf '%s' "$ARG" | grep -oE '[1-9A-HJ-NP-Za-km-z]{32,44}' | head -1)"
[ -n "$CA" ] || { echo "CA(mint address) か pump.fun URL を渡して: bash brain/check_token.sh <CA>" >&2; exit 1; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI なし" >&2; exit 1; }

DATA="$(python3 - "$CA" <<'PY'
import json, sys, urllib.request, glob, re
CA = sys.argv[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
def get(u, t=12):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=t).read())

out = {"CA": CA}
# pump.fun
try:
    c = get(f"https://frontend-api-v3.pump.fun/coins/{CA}", 10)
    out["pump"] = {"symbol": c.get("symbol"), "name": c.get("name"), "usd_mcap": c.get("usd_market_cap"),
                   "reply": c.get("reply_count"), "complete": c.get("complete"), "creator": c.get("creator"),
                   "twitter": c.get("twitter"), "website": c.get("website")}
except Exception as e:
    out["pump"] = f"取得不可({type(e).__name__})=pump.fun銘柄でないかも"
# RugCheck(scam門・T1)
try:
    d = get(f"https://api.rugcheck.xyz/v1/tokens/{CA}/report", 15)
    th = d.get("topHolders") or []
    top = max((h.get("pct") or 0) for h in th) if th else None
    out["rugcheck"] = {"mint_authority": d.get("mintAuthority"), "freeze_authority": d.get("freezeAuthority"),
                       "rugged": d.get("rugged"), "score": d.get("score"), "score_norm": d.get("score_normalised"),
                       "top_holder_pct": round(top, 1) if top else None,
                       "danger": [r.get("name") for r in (d.get("risks") or []) if r.get("level") == "danger"],
                       "all_risks": [r.get("name") for r in (d.get("risks") or [])][:8],
                       "insiders": bool(d.get("insiderNetworks")) or bool(d.get("graphInsidersDetected")),
                       "creatorTokens_n": len(d.get("creatorTokens") or []),
                       "lp_locked_pct": d.get("lpLockedPct"), "totalHolders": d.get("totalHolders")}
except Exception as e:
    out["rugcheck"] = f"取得不可({type(e).__name__})"
# KOL-CA照合: このCAを watchlist の誰が言及してるか(直近ソース)
accts = set()
for p in sorted(glob.glob("sources/x/*.md"))[-1500:]:
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    if CA in t:
        m = re.search(r"^account:\s*(\S+)", t, re.M)
        if m:
            accts.add(m.group(1))
out["kol_言及"] = sorted(accts) or "watchlist内で言及なし(=traction無し)"
print(json.dumps(out, ensure_ascii=False, indent=2))
PY
)"

PROMPT="$(cat brain/check_token_prompt.md)
$DATA"
claude --print --model "$MODEL" --dangerously-skip-permissions --strict-mcp-config "$PROMPT"
