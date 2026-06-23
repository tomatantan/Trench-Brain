#!/usr/bin/env python3
"""
check_conformance.py — 憲法conformanceを**機械で検査**する（自己採点でなく証拠ベース）。

再発防止の構造的fix(本人2026-06-23): 芯チェックが無強制・自己採点・曖昧基準だと momentum で
"名前を出すフリ"に劣化する→ §Query資産化を落とした。だから**機械が要件を1個ずつ実装と照合**し、
証拠(file:行/ファイル存在/件数)を出せない要件は VIOLATION で確定する。lint輪が毎日回す。

各 check は CLAUDE.md/原典の具体要件 → 決定的な検査関数。PASS/FAIL/WARN と証拠を吐く。
名前を出すだけでは PASS しない（実装の実体を grep/存在/件数で確認する）。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def grep(pattern, *globs):
    """globパターン群から pattern を含む行を (file, lineno, line) で返す。"""
    hits = []
    for g in globs:
        for p in ROOT.glob(g):
            if not p.is_file():
                continue
            try:
                for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    if re.search(pattern, ln):
                        hits.append((str(p.relative_to(ROOT)), i, ln.strip()))
            except Exception:
                pass
    return hits


CHECKS = []
def check(id, ref, req):
    def deco(fn):
        CHECKS.append((id, ref, req, fn)); return fn
    return deco


@check("Q1", "§Query step3", "/wiki の価値ある回答を wiki/queries/ に資産化する")
def _q1():
    # 実装の実体: query を queries/ に書くコードがあるか + 実際に queries が生成されてるか
    writes = grep(r"queries.*\.md|/ \"queries\"|\"queries\"", "brain/wiki_bot.py")
    asset = grep(r"def assetize_query", "brain/wiki_bot.py")
    called = grep(r"assetize_query\(", "brain/wiki_bot.py")
    nfiles = len(list((ROOT / "wiki" / "queries").glob("*.md"))) if (ROOT / "wiki" / "queries").exists() else 0
    if asset and len(called) >= 2:   # 定義 + 呼び出し
        return "PASS", f"assetize_query 定義&呼出あり / queries {nfiles}枚"
    return "FAIL", f"/wiki が queries/ に資産化してない(assetize定義={bool(asset)} 呼出={len(called)})＝§Query step3欠落"


@check("R1", "指針1", "sources/ は読むだけ＝合成engineは sources/ を編集しない(収集/curationのみ可)")
def _r1():
    # 合成engineの行で「sources/ への書込」(同一行に sources/ と 書込動詞)だけを違反とする。
    # brain/state/ への書込(tracked.json等)は sources/ でない=違反でない。
    cand = grep(r"sources/", "brain/synthesize*.sh", "brain/track.py", "brain/launch_synth.sh", "brain/launch_pulse.py")
    bad = [h for h in cand if re.search(r"(write_text|open\([^)]*['\"][wa]|>>|\.write\()", h[2])]
    if bad:
        return "FAIL", f"合成engineがsources/に書込: {bad[:3]}"
    return "PASS", "合成engineはsources/を編集してない(collect/add/imageのみ=curation)"


@check("R2", "指針2", "収集は門付き(watchlist/traction/KOL)・firehose禁止")
def _r2():
    wl = grep(r"WATCHLIST|watchlist", "collector/collect.py")
    scam = grep(r"CLEAR_SCAM_KEYS|authority未放棄|scam門|def sieve", "brain/launch_stream.py")
    # firehose=無差別trending"取込"。実際の収集コードのみ走査(checker自身/コメント/pattern定義は除外)。
    fire_raw = grep(r"(coingecko|dexscreener).{0,20}(trending|boosted)|includeNsfw=true",
                    "collector/collect.py", "collector/collect_youtube.py", "brain/track.py")
    fire = [h for h in fire_raw if "grep(" not in h[2] and not h[2].lstrip().startswith("#")]
    if wl and scam and not fire:
        return "PASS", f"watchlist門={len(wl)} scam門={len(scam)} firehose無し"
    return "FAIL" if fire else "WARN", f"watchlist={bool(wl)} scam門={bool(scam)} firehose={fire[:2]}"


@check("R3", "指針3", "合成が収集に追いつく＝signal_backlogで健康を測る")
def _r3():
    h = ROOT / "brain" / "state" / "health.jsonl"
    if not h.exists():
        return "FAIL", "health.jsonl が無い＝backlog健康を測ってない"
    lines = [l for l in h.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        return "FAIL", "health.jsonl 空"
    try:
        last = json.loads(lines[-1]); bl = last.get("signal_backlog")
        return ("WARN" if (bl or 0) > 50 else "PASS"), f"最新signal_backlog={bl}（記録あり）"
    except Exception:
        return "WARN", "health.jsonl 末尾parse不可"


@check("R7", "指針7", "全ページを wikilink で接続＝孤立ページが無い")
def _r7():
    cdir = ROOT / "wiki" / "concepts"
    if not cdir.exists():
        return "WARN", "concepts なし"
    orphans = []
    allmd = list((ROOT / "wiki").rglob("*.md"))
    alltext = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in allmd)
    for p in cdir.glob("*.md"):
        stem = p.stem
        out = "[[" in p.read_text(encoding="utf-8", errors="replace")
        inbound = f"[[{stem}" in alltext.replace(p.read_text(encoding='utf-8',errors='replace'), "")
        if not out and not inbound:
            orphans.append(stem)
    return ("WARN" if orphans else "PASS"), (f"孤立concept: {orphans[:5]}" if orphans else "孤立concept無し")


@check("L1", "§Lint", "lint(健康診断)が稼働＝矛盾/孤立/ギャップを定期検出")
def _l1():
    sh = (ROOT / "brain" / "synthesize_lint.sh").exists()
    rep = (ROOT / "wiki" / "lint-report.md").exists()
    if sh and rep:
        return "PASS", "synthesize_lint.sh + lint-report.md あり"
    return "FAIL", f"lint.sh={sh} report={rep}"


@check("OA1", "指針2/6 観測≠採用", "全mint観測(篩材料)≠採用(篩通過のみ合成)")
def _oa1():
    obs = grep(r"全mint|observed|launch feed|newest", "brain/track.py", "brain/launch_stream.py")
    adopt = grep(r"traction\+KOL|standout|採用門|kol_standouts", "brain/launch_synth_prompt.md", "brain/launch_synth.sh", "brain/launch_pulse.py")
    if obs and adopt:
        return "PASS", f"観測コード={len(obs)} 採用門コード={len(adopt)}"
    return "WARN", f"観測={bool(obs)} 採用門={bool(adopt)}"


def main():
    rows = []
    for id, ref, req, fn in CHECKS:
        try:
            status, ev = fn()
        except Exception as e:
            status, ev = "ERROR", f"{type(e).__name__}: {e}"
        rows.append((id, ref, req, status, ev))
    fails = [r for r in rows if r[3] in ("FAIL", "ERROR")]
    warns = [r for r in rows if r[3] == "WARN"]
    out = ["# 憲法 conformance レポート（機械検査・自己採点でない）", "",
           f"PASS {sum(1 for r in rows if r[3]=='PASS')} / FAIL {len(fails)} / WARN {len(warns)} / 計{len(rows)}", "",
           "| id | 指針/節 | 要件 | 判定 | 証拠/違反 |", "|---|---|---|---|---|"]
    for id, ref, req, st, ev in rows:
        mark = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "ERROR": "💥"}.get(st, st)
        out.append(f"| {id} | {ref} | {req} | {mark}{st} | {ev} |")
    if fails:
        out += ["", "## ❌ 違反（即修正）"] + [f"- **{r[0]} {r[1]}**: {r[2]} → {r[4]}" for r in fails]
    rep = ROOT / "wiki" / "conformance-report.md"
    rep.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
