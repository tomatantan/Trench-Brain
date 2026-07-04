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


@check("R3d", "指針2/3 収集入口の鮮度", "X収集の入口が生きてる＝sources/x が凍結してない(2026-06-26 twitterapi 402 が5日半 false-green だった盲点を塞ぐ)")
def _r3d():
    # signal_backlog(R3)はコーパス内の未合成しか見ない→入口(収集)が死んでも健康に見えた。
    # ここは「入口の鮮度」を独立に測る。①collect_health.json(収集run記録)が第一級ソース。
    # ②無ければ sources/x の最新 created を snowflake tweet_id 上位からサンプルして推定。
    import time as _t
    FRESH_H = 12  # 3h cron が4回連続で新規ゼロ=異常
    hf = ROOT / "brain" / "state" / "collect_health.json"
    if hf.exists():
        try:
            h = json.loads(hf.read_text(encoding="utf-8"))
            from datetime import datetime, timezone
            ts = datetime.strptime(h["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            age_h = (_t.time() - ts.timestamp()) / 3600
            ok = bool(h.get("ok")) and age_h <= FRESH_H
            return ("PASS" if ok else "FAIL"), (
                f"collect_health {age_h:.1f}h前 backend={h.get('backend')} "
                f"new={h.get('new')} err={h.get('errors')}/{h.get('accounts')}"
                f"{'' if ok else ' ＝収集停止/古い'}")
        except Exception as e:
            return "WARN", f"collect_health.json parse不可({e})"
    # フォールバック: 最新 tweet_id(snowflake=時刻単調)上位の created を見る
    sdir = ROOT / "sources" / "x"
    if not sdir.exists():
        return "WARN", "sources/x 無し"
    def _tid(p):
        try:
            return int(p.stem.split("__")[-1])
        except Exception:
            return 0
    files = sorted(sdir.glob("*.md"), key=_tid, reverse=True)[:5]
    newest = ""
    for p in files:
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if ln.startswith("created:"):
                newest = max(newest, ln.split(":", 1)[1].strip()); break
    if not newest:
        return "WARN", "created 読めず"
    try:
        from datetime import datetime, timezone
        age_h = (_t.time() - datetime.strptime(newest, "%Y-%m-%dT%H:%M:%SZ")
                 .replace(tzinfo=timezone.utc).timestamp()) / 3600
        return ("PASS" if age_h <= FRESH_H else "FAIL"), (
            f"最新tweet {age_h:.1f}h前({newest}){'＝収集停止疑い' if age_h > FRESH_H else ''}"
            " [collect_health.json未生成→tweet鮮度で代替]")
    except Exception:
        return "WARN", f"created parse不可({newest})"


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


@check("C4", "指針4", "1ソース取込→複数ページに波及(synthesis)")
def _c4():
    prompt = grep(r"関連.*concept|複数ページ|波及|entity synthesis|多ページ", "brain/INGEST.md", "brain/synth_x_prompt.md", "brain/synth_prompt.md")
    nsum = len(list((ROOT / "wiki" / "summaries").glob("*.md"))) if (ROOT / "wiki" / "summaries").exists() else 0
    nent = len(list((ROOT / "wiki" / "entities").rglob("*.md")))
    if prompt and (nsum + nent) > 0:
        return "PASS", f"波及指示あり・summary{nsum}+entity{nent}枚"
    return "WARN", f"波及指示={bool(prompt)} summary={nsum} entity={nent}"


@check("C5", "指針5", "矛盾は消さず⚠️両論で保持する")
def _c5():
    hits = grep(r"⚠️|矛盾|両論|⇄", "wiki/concepts/*.md")
    prompt = grep(r"矛盾|両論|⚠️", "brain/synth_prompt.md", "brain/synth_x_prompt.md", "brain/methodology/synthesis-rules.md")
    if hits and prompt:
        return "PASS", f"concept内 ⚠️/矛盾 {len(hits)}箇所・prompt指示あり"
    return "WARN", f"concept矛盾痕={len(hits)} prompt指示={bool(prompt)}"


@check("C6", "指針6", "entityで観測(事実)と推論(判断)を分離する")
def _c6():
    ents = list((ROOT / "wiki" / "entities").rglob("*.md"))
    sep = 0
    for p in ents:
        t = p.read_text(encoding="utf-8", errors="replace")
        if "観測" in t and ("判断" in t or "合成メモ" in t or "synthesis" in t):
            sep += 1
    return ("PASS" if sep > 0 else "WARN"), f"観測/判断を分離した entity {sep}/{len(ents)}枚"


@check("C8", "指針8", "bottom-up＝conceptを独断量産しない(動線/型が立つ時だけ)")
def _c8():
    nc = len(list((ROOT / "wiki" / "concepts").glob("*.md"))) if (ROOT / "wiki" / "concepts").exists() else 0
    nsrc = len(list((ROOT / "sources").rglob("*.md")))
    bottomup = grep(r"worklist で|浮上したことから|から合成", "wiki/concepts/*.md")
    ratio = nc / max(1, nsrc)
    if nc < 60 and ratio < 0.2 and bottomup:
        return "PASS", f"concept{nc}枚(source{nsrc}・比{ratio:.3f})・bottom-up痕{len(bottomup)}"
    return "WARN", f"concept{nc} source{nsrc} 比{ratio:.2f} bottomup={bool(bottomup)}（量産疑い?）"


@check("C9", "指針9", "淡々＝煽り/絵文字過多をしない(brainの声のみ・引用ソースは逐語=対象外)")
def _c9():
    # 指針9は brain の合成/判断の声に適用。引用(>)・表(|)・出典行([[..__)は観測=逐語なので除外。
    hype = []
    for p in (ROOT / "wiki").rglob("*.md"):
        emoji = words = 0
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            s = ln.strip()
            if s.startswith(">") or s.startswith("|") or "__" in s or "「" in s:
                continue  # 引用/表/出典=ソース逐語=対象外
            emoji += len(re.findall(r"🚀|🔥|💎|🌙", ln))
            words += len(re.findall(r"爆益確定|億り人確定|100x保証|今すぐ買え|絶対上がる|to da moon", ln, re.I))
        if emoji > 6 or words > 0:
            hype.append((p.name, emoji, words))
    return ("WARN" if hype else "PASS"), (f"brain-voice煽り疑い: {hype[:3]}" if hype else "brain-voiceに煽り/絵文字過多なし(引用は対象外)")


@check("I1", "§Ingest", "index.md/log.md を維持＝取込を記録・カタログ化")
def _i1():
    ok = [(ROOT / f).exists() for f in ("wiki/index.md", "wiki/log.md")]
    return ("PASS" if all(ok) else "FAIL"), f"index={ok[0]} log={ok[1]}"


@check("L2", "§Lint実挙動", "lintが実際に動いてる(stampが新しい＝存在でなく実行)")
def _l2():
    import os
    import time
    stamp = ROOT / "brain" / "state" / "last_lint"
    if not stamp.exists():
        return "WARN", "last_lint stamp なし(まだ実行されてない)"
    age = (time.time() - os.path.getmtime(stamp)) / 3600
    return ("PASS" if age < 48 else "WARN"), f"last_lint {age:.0f}h前(実行痕)"


@check("Q2", "§Query実挙動", "/wiki が実際に queries を蓄積してる(存在でなく稼働痕)")
def _q2():
    qs = list((ROOT / "wiki" / "queries").glob("*.md")) if (ROOT / "wiki" / "queries").exists() else []
    return ("PASS" if qs else "WARN"), f"queries {len(qs)}枚(0なら未稼働)"


@check("R3b", "指針2/3 計測鮮度", "死の分母tracker(base_rate/tracked)が凍結してない=最近更新されてる")
def _r3b():
    # 監査(2026-06-24)で発覚: base_rate.json が14窓凍結してたのにR3(backlog存在)はPASSしてた=見逃し。
    # "存在"でなく"鮮度"を検査=mtimeが古い(>FRESH_H)なら凍結=FAIL。これが死の分母の実稼働を担保する。
    import os
    import time
    FRESH_H = 6
    p = ROOT / "brain" / "state" / "base_rate.json"
    if not p.exists():
        return "FAIL", "base_rate.json 無し=死の分母tracker未稼働"
    age = (time.time() - os.path.getmtime(p)) / 3600
    return ("PASS" if age < FRESH_H else "FAIL"), f"base_rate 最終更新 {age:.1f}h前（>{FRESH_H}h=凍結=FAIL）"


@check("R3c", "指針3/6 死の計測整合", "死の分母counter(base_rate.died)が実dead数(tracked.json)と一致＝正しく数えてる")
def _r3c():
    import json as _j
    # ★再々調整(2026-06-24): 旧R3cは died==死亡台帳件数 を要求したが、それは miscalibrated だった——
    #   死亡台帳は「型通りの死は1行」=**型集約の学習サンプル**(20の同型死→~10型行)で、died(完全counter)と
    #   等しくならないのが設計通り。正しい整合検査は **died vs tracked.json の実dead数**(counterが取りこぼしてないか)。
    #   原バグ(died=0)も counter取りこぼしも これで検出する。台帳の件数比較は廃止(設計と矛盾するfalse-FAILだった)。
    p = ROOT / "brain" / "state" / "base_rate.json"
    t = ROOT / "brain" / "state" / "tracked.json"
    if not (p.exists() and t.exists()):
        return "WARN", "base_rate/tracked無し"
    try:
        died = _j.loads(p.read_text()).get("died", 0)
        td = _j.loads(t.read_text())
        items = td if isinstance(td, list) else list(td.values())
        n_dead = sum(1 for x in items if x.get("status") == "dead")
    except Exception:
        return "WARN", "parse不可"
    n_ledger = len(grep(r"^\| \[\[\$", "wiki/concepts/rug-anatomy.md"))
    if died == 0 and n_dead > 0:
        return "FAIL", f"died=0 だが tracked に dead {n_dead}件=死counter壊れ(原バグ)"
    if died < n_dead:
        return "FAIL", f"died={died} < tracked実dead {n_dead}件=counter取りこぼし"
    return "PASS", f"died={died}=tracked実dead{n_dead}(counter整合) / 台帳{n_ledger}型(型集約の学習サンプル=died≧台帳は正常)"


@check("H1", "衛生/指針6", "concept が confidence frontmatter を持つ(主張の確信度を明示)")
def _h1():
    cdir = ROOT / "wiki" / "concepts"
    if not cdir.exists():
        return "WARN", "concepts なし"
    miss = [p.name for p in cdir.glob("*.md")
            if not re.search(r"^confidence:", p.read_text(encoding="utf-8", errors="replace"), re.M)]
    return ("PASS" if not miss else "WARN"), (f"confidence欠落: {miss[:5]}" if miss else "全conceptにconfidence有")


@check("H2", "衛生/前のめり防止", "強い断定(確証/確定/必ず)が裏付け(⚠️/仮説/N)無しに先走ってない=型化バイアス防止")
def _h2():
    bad = []
    for p in (ROOT / "wiki" / "concepts").glob("*.md"):
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            s = ln.strip()
            if s.startswith(">") or s.startswith("|") or "__" in s or "「" in s:
                continue  # 引用/表/出典は対象外
            if re.search(r"確証(さ|済|し)|確定的|必ず[^し]|絶対に上が|100%確実|間違いなく", ln) and \
               not any(k in ln for k in ("⚠️", "仮説", "未確定", "未検証", "N=")):
                bad.append((p.name, s[:45]))
    return ("WARN" if bad else "PASS"), (f"前のめり断定疑い: {bad[:3]}" if bad else "裏付け無き断定なし(前のめり型化なし)")


@check("OP1", "運用/パイプライン健全", "build_entities が成功して entity が新鮮(=合成パイプラインが crash してない)")
def _op1():
    import time as _t
    pdir = ROOT / "wiki" / "entities" / "players"
    if not pdir.exists():
        return "WARN", "players entity dir無し"
    files = list(pdir.glob("@*.md"))
    if not files:
        return "WARN", "player entity無し"
    newest = max(f.stat().st_mtime for f in files)
    age_h = (_t.time() - newest) / 3600
    # build_entities が crash すると entity が更新されず古くなる→検出(2026-06-24 の @/add-image crash を捕まえる為)
    return ("FAIL" if age_h > 12 else "PASS"), f"最新player entity {age_h:.1f}h前更新({len(files)}件)＝{'古い=build_entities停止疑い' if age_h > 12 else 'パイプライン稼働'}"


@check("K1", "§0.1-1 矛盾=KPI", "conceptsが増えてるのに表面化した矛盾(⚠️)が増えてない=echo-chamber兆候を検出")
def _k1():
    # 設計書 ENGINE-REDESIGN §0.1-1: wikiの健康は coverage でなく surfaced contradictions。
    # 一致だけ増えるのは劣化(echo-chamber)。compounding_history.jsonl(compounding.py が毎サイクル追記)の
    # 推移で「concepts純増 なのに contradictions_surfaced 横這い」を機械検出する。
    import json as _j
    p = ROOT / "brain" / "state" / "compounding_history.jsonl"
    if not p.exists():
        return "WARN", "compounding_history無し(compounding.py 未稼働=矛盾KPIが測れてない)"
    rows = []
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rows.append(_j.loads(ln))
        except ValueError:
            continue
    if len(rows) < 2:
        return "WARN", f"履歴{len(rows)}点=推移未評価(2点以上で評価開始)"
    win = rows[-10:]
    dc = (win[-1].get("n_concepts") or 0) - (win[0].get("n_concepts") or 0)
    dk = (win[-1].get("contradictions_surfaced") or 0) - (win[0].get("contradictions_surfaced") or 0)
    now_k = win[-1].get("contradictions_surfaced")
    if dc >= 2 and dk <= 0:
        return "WARN", f"直近{len(win)}点: concepts +{dc} なのに矛盾表面化 {dk:+d}＝一致だけ増えてる疑い(echo-chamber)→対立ソース/弱者voiceの取り込みを"
    return "PASS", f"直近{len(win)}点: concepts {dc:+d} / 矛盾表面化 {dk:+d}（現在{now_k}）＝矛盾が知識と共に増えてる"


@check("S1", "§Lint/指針7", "内部 wikilink の切れ(指す先のwikiページが存在しない)を検出")
def _s1():
    wdir = ROOT / "wiki"
    if not wdir.exists():
        return "WARN", "wiki/ なし"
    # 既存ページ集合(stem)
    all_stems = {p.stem for p in wdir.rglob("*.md")}
    all_stems_lower = {s.lower() for s in all_stems}
    # ソース参照パターン(dangling扱いしない): 例 0xFunX__2065133916802167217
    source_ref_re = re.compile(r"^[A-Za-z0-9_]+__\d{6,}$")
    dangling: set = set()
    for p in wdir.rglob("*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        targets = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)
        for t in targets:
            t = t.strip()
            if source_ref_re.match(t):
                continue
            if t in all_stems or t.lower() in all_stems_lower:
                continue
            dangling.add(t)
    n = len(dangling)
    sample = sorted(dangling)[:5]
    return ("WARN" if n > 0 else "PASS"), f"内部dangling {n}件(上位: {sample})"


@check("S2", "ページ規約", "summaries/concepts/queries が必須frontmatter(type/title/created/updated/tags・summaryはsource)を持つ")
def _s2():
    REQUIRED_ALL = {"type", "title", "created", "updated", "tags"}
    bad = []
    for subdir in ("summaries", "concepts", "queries"):
        d = ROOT / "wiki" / subdir
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                bad.append(p.name); continue
            parts = text.split("---", 2)
            if len(parts) < 3:
                bad.append(p.name); continue
            fm = parts[1]
            keys = {m.group(1) for m in re.finditer(r"^(\w+)\s*:", fm, re.M)}
            required = REQUIRED_ALL | ({"source"} if subdir == "summaries" else set())
            missing = required - keys
            if missing:
                bad.append(f"{p.name}(欠:{sorted(missing)})")
    total = sum(
        len(list((ROOT / "wiki" / s).glob("*.md")))
        for s in ("summaries", "concepts", "queries")
        if (ROOT / "wiki" / s).exists()
    )
    if not bad:
        return "PASS", f"対象{total}枚すべて規約準拠"
    return "FAIL", f"frontmatter欠落 {len(bad)}件: {bad[:5]}"


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
