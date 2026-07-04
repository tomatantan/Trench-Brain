#!/usr/bin/env python3
"""
score_queries.py — G5b: 過去の回答(query_log)を実outcomeで採点する（決定的・LLM不使用・network不使用）。

設計書 ENGINE-REDESIGN §1 G5: 「答え/予測が二度と採点されない（query_log write-only）」を閉じる。
各回答が言及した銘柄($ticker/CA)とKOL(@handle)を抽出し、tracked.json / ca_outcome_cache.json /
kol_track_records.json の現outcomeと照合＝「あの答えが触れた物はその後どうなったか」を機械で記録する。

正直さの線引き(観測≠判定・指針6):
  回答のstance(ape推奨かavoid警告か)は自然文でv1では決定的に取れない。だからここで出すのは
  「言及銘柄のその後」という観測であり「回答の正誤判定」ではない(死んだ銘柄はavoid的中かもしれない)。
  ただし初採点時のsnapshot(at_first_score)を保存するので、「答えた後に何が変わったか」は machine-readable になる。
  stance対応の本採点は ask.sh の構造化ログ(a_tickers等)が貯まってから拡張する。

出力: brain/state/answer_scorecard.json + wiki/dashboards/answer-scorecard.md（feedback.py と同じ二段）。
下流: ask_context.py がこの scorecard を第4注入「過去の自分の回答のその後」として読む＝自己校正loop。
cron: kol_track_record.py の直後(ca_outcome_cache が同 run で更新された直後)。
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "brain" / "state"
LOG = STATE / "query_log.jsonl"
TRACKED = STATE / "tracked.json"
CACHE = STATE / "ca_outcome_cache.json"
KTR = STATE / "kol_track_records.json"
OUT_JSON = STATE / "answer_scorecard.json"
OUT_MD = ROOT / "wiki" / "dashboards" / "answer-scorecard.md"

CA_RE = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")
TICK_RE = re.compile(r"\$([A-Za-z0-9]{2,15})\b")
HANDLE_RE = re.compile(r"@([A-Za-z0-9_]{3,15})")
MONEY_RE = re.compile(r"\d+(?:[.,]\d+)?[kKmMbB]?$")  # $414k / $10K 等の金額ノイズ


def _load(p, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return default


def tickers_of(text):
    return sorted({t.upper() for t in TICK_RE.findall(text) if not MONEY_RE.fullmatch(t)})


def main():
    if not LOG.exists():
        print("score_queries: query_log無し → skip")
        return
    entries = []
    for ln in LOG.read_text(encoding="utf-8").splitlines():
        try:
            entries.append(json.loads(ln))
        except ValueError:
            continue
    if not entries:
        print("score_queries: query_log空 → skip")
        return

    tracked = _load(TRACKED, {})
    titems = tracked if isinstance(tracked, list) else list(tracked.values())
    by_ticker = {}
    for x in titems:
        tk = (x.get("ticker") or "").lstrip("$").upper()
        if tk:
            by_ticker.setdefault(tk, []).append(x)
    by_mint = {x.get("mint"): x for x in titems if x.get("mint")}
    cache = _load(CACHE, {})
    ktr = _load(KTR, {})
    prev = _load(OUT_JSON, {})
    prev_answers = prev.get("answers", {}) if isinstance(prev, dict) else {}

    def token_outcome(rec):
        st = rec.get("status")
        last = rec.get("last") or {}
        return {"status": "dead" if st == "dead" else ("alive" if st == "tracked" else st),
                "peak_mcap": rec.get("peak_mcap"), "mcap_now": last.get("mcap_usd")}

    answers = {}
    for e in entries:
        q, a, ts = e.get("question", ""), e.get("answer", ""), e.get("ts", "")
        if not a:
            continue
        aid = ts + "-" + hashlib.md5(q.encode()).hexdigest()[:8]
        # 構造化ログ(新)があれば使う。旧エントリは本文から抽出(fallback)。
        # q_tickers も採点対象に含める(質問の主語銘柄を回答が復唱しないケース・敵対検証C3)。
        tks = sorted(set(e.get("a_tickers") or tickers_of(q + " " + a)) | set(e.get("q_tickers") or []))
        cas = e.get("q_cas") or sorted(set(CA_RE.findall(q)))
        handles = e.get("a_handles") or sorted({h.lower() for h in HANDLE_RE.findall(a)})

        tokens = {}
        for tk in tks:
            recs = by_ticker.get(tk)
            if recs:
                # 同ticker複数mintは「回答時点までに生まれた中で最新」を採る。
                # 回答時点より後に生まれたmintしか無ければ誤帰属せず unknown に倒す(敵対検証C2)。
                cand = [r for r in recs if (r.get("first_seen") or "") <= (ts or "9999")]
                if cand:
                    rec = max(cand, key=lambda r: r.get("first_seen") or "")
                    o = token_outcome(rec)
                    if len(cand) > 1:
                        o["ambiguous_candidates"] = len(cand)  # 同ticker多mint=誤帰属リスクを明示
                    tokens[f"${tk}"] = o
                else:
                    tokens[f"${tk}"] = {"status": "unknown", "note": "回答時点で既知のmint無し(後発tickerのみ)"}
            else:
                tokens[f"${tk}"] = {"status": "unknown", "note": "trackedに無し(ticker未解決)"}
        for ca in cas:
            if ca in by_mint:
                tokens[ca[:8] + "…"] = token_outcome(by_mint[ca])
            elif ca in cache:
                c = cache[ca]
                tokens[ca[:8] + "…"] = {"status": c.get("outcome"), "mcap_now": c.get("mcap")}

        kols = {}
        for h in handles:
            v = ktr.get(h)
            if isinstance(v, dict) and v.get("evaluated"):
                kols[h] = {"death_rate_now": v.get("death_rate"), "evaluated_now": v.get("evaluated")}

        entry = {"ts": ts, "question": q[:120], "tokens": tokens, "kols": kols}
        old = prev_answers.get(aid)
        if old and old.get("at_first_score"):
            entry["at_first_score"] = old["at_first_score"]  # 初採点snapshotは不変
        else:
            entry["at_first_score"] = {"scored_ts": None, "tokens": tokens, "kols": kols}
        answers[aid] = entry

    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    for v in answers.values():
        if v["at_first_score"]["scored_ts"] is None:
            v["at_first_score"]["scored_ts"] = now

    # 集計: 言及銘柄の現状(観測)
    tok_all = [t for v in answers.values() for t in v["tokens"].values()]
    dead = sum(1 for t in tok_all if t.get("status") == "dead")
    alive = sum(1 for t in tok_all if t.get("status") == "alive")
    unk = len(tok_all) - dead - alive
    summary = {"answers": len(answers), "tokens_mentioned": len(tok_all),
               "dead_now": dead, "alive_now": alive, "unknown": unk,
               "dead_pct_of_resolved": (100 * dead // (dead + alive)) if (dead + alive) else None}

    OUT_JSON.write_text(json.dumps({"ts": now, "summary": summary, "answers": answers},
                                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    lines = [
        "---", "type: dashboard", "title: Answer Scorecard — 回答のその後（実outcome照合）",
        "updated: auto", "tags: [feedback, scorecard, g5]", "---", "",
        "# Answer Scorecard — 過去の回答が触れた物はその後どうなったか", "",
        "> `brain/score_queries.py` が query_log の各回答の言及銘柄/KOLを実outcomeと照合（観測であり正誤判定ではない＝",
        "> 死んだ銘柄はavoid的中の可能性がある。stance対応採点は構造化ログ蓄積後に拡張）。", "",
        f"## 集計: 回答{summary['answers']}件・言及銘柄{summary['tokens_mentioned']}件"
        f"（現在 dead {dead} / alive {alive} / 不明 {unk}）", "",
        "| 回答日時 | 問い | 言及銘柄→現状 | 言及KOL(現death%) |", "|---|---|---|---|",
    ]
    for aid in sorted(answers, reverse=True)[:20]:
        v = answers[aid]
        tstr = " ".join(f"{k}:{t.get('status')}" for k, t in list(v["tokens"].items())[:6]) or "—"
        kstr = " ".join(f"@{h}({d.get('death_rate_now')}%)" for h, d in list(v["kols"].items())[:5]) or "—"
        lines.append(f"| {v['ts']} | {v['question'][:60]} | {tstr} | {kstr} |")
    lines += ["", "関連: [[feedback]] / [[kol-track-records]] / 下流: ask_context.py 第4注入（自己校正）"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"score_queries: 回答{summary['answers']}件を採点(言及銘柄{len(tok_all)}: "
          f"dead{dead}/alive{alive}/unk{unk}) → answer_scorecard.json + dashboards/answer-scorecard.md")


if __name__ == "__main__":
    main()
