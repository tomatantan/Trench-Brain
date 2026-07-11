#!/usr/bin/env python3
"""entity_paths.py — token entity ページ名の casefold 衝突を後処理で正規化する normalizer(2026-07-11)。
synthesis 後・git add 前に cron_collect から走らせる(build_moc直前)。LLM が何を書こうが、毎サイクル
機械的に casefold 衝突を潰す＝macOS(case-insensitive FS)の pull/rebase 詰まり根治。writerを信用しない安全層。

規則(本人確定 2026-07-11):
- 同mint双子: **合成の実質量(bytes)が大きい側を勝たせる。同等に厚い時だけ新しい(mtime)方**(recency=tiebreak)。
  canonical名は UPPER ticker(mint6サフィックス保持)。負け側の消滅は必ずログ(沈黙マージ禁止)。
- 別mint(同ticker): 各ファイルを $<UPPER-TICKER>-<mint6>.md(mint先頭6・case保持)＝相互曖昧性解消。
- wikilink置換は**完全一致のみ**([[<t>]] / [[<t>| / [[<t>#)。前方一致事故($ANSEM vs $ANSEMCT)防止。

CLI: --check(dry・残衝突あれば exit 1) / --fix(実行・git mv/rm/add まで)
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOK = ROOT / "wiki" / "entities" / "tokens"
FM_MINT = re.compile(r"(?im)^\s*mint:\s*`?([1-9A-HJ-NP-Za-km-z]{32,44})")
ANY_MINT = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
NAME_RE = re.compile(r"^\$(?P<tk>.+?)(?:-(?P<m6>[1-9A-HJ-NP-Za-km-z]{6}))?\.md$")
THICK = 0.85  # 小/大 >= これ なら"両方厚い"→ recency tiebreak


def _git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)


def _mint(f):
    try:
        t = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    m = FM_MINT.search(t)
    if m:
        return m.group(1)
    m = ANY_MINT.search(t)
    return m.group(0) if m else None


def _parse(name):
    mm = NAME_RE.match(name)
    if mm:
        return mm.group("tk"), mm.group("m6")
    return name[1:-3], None


def normalize(do=False):
    acts, renames = [], {}   # renames: "$OLD"(拡張子抜き) -> "$NEW"
    if not TOK.exists():
        return acts
    groups = {}
    for f in sorted(TOK.glob("$*.md")):
        groups.setdefault(f.name.lower(), []).append(f)

    for low, fs in groups.items():
        if len(fs) < 2:
            continue
        infos = []
        for f in fs:
            tk, m6 = _parse(f.name)
            st = f.stat()
            infos.append({"f": f, "tk": tk, "m6": m6, "mint": _mint(f),
                          "size": st.st_size, "mtime": st.st_mtime})
        upper = infos[0]["tk"].upper()
        distinct = {i["mint"] for i in infos if i["mint"]}

        if not distinct:
            # ---- 全員mint不明: 同一トークンの証拠ゼロ=マージすると別トークンを消し合う恐れ ----
            # (2026-07-11 Mac側の敵対的検証で発見: LLMがmint欄を書き損ねた別トークン同士がMERGEされるedge)
            acts.append("SKIP(全mint不明・同一性を確認できずマージしない・要人力確認): "
                        + ", ".join(i["f"].name for i in infos))
            continue
        if len(distinct) <= 1:
            # ---- 同mint(or mint不明を同一視) : merge ----
            m6 = next((i["m6"] for i in infos if i["m6"]), None)
            canon = f"${upper}" + (f"-{m6}" if m6 else "") + ".md"
            sz = sorted(infos, key=lambda i: i["size"])
            small, big = sz[0], sz[-1]
            if small["size"] and big["size"] and small["size"] / big["size"] >= THICK:
                winner = max(infos, key=lambda i: i["mtime"]); why = "両方厚い→新しい(mtime)"
            else:
                winner = big; why = "内容量大"
            losers = [i for i in infos if i["f"] is not winner["f"]]
            lose_s = ", ".join(f"{l['f'].name}({l['size']}b)" for l in losers)
            acts.append(f"MERGE {canon} <- {winner['f'].name}({winner['size']}b/{why}) 消滅: {lose_s}")
            content = winner["f"].read_text(encoding="utf-8", errors="replace")
            if do:
                for i in infos:
                    _git("rm", "-q", "-f", str(i["f"].relative_to(ROOT)))
                (TOK / canon).write_text(content, encoding="utf-8")
                _git("add", str((TOK / canon).relative_to(ROOT)))
            for i in infos:
                if i["f"].name != canon:
                    renames[i["f"].name[:-3]] = canon[:-3]
        else:
            # ---- 別mint(同ticker) : 各々 $UPPER-<mint6> ----
            for i in infos:
                if not i["mint"]:
                    acts.append(f"SKIP(mint不明) {i['f'].name}")
                    continue
                new_name = f"${upper}-{i['mint'][:6]}.md"
                if i["f"].name == new_name:
                    continue
                acts.append(f"RENAME(別mint) {i['f'].name} -> {new_name}")
                content = i["f"].read_text(encoding="utf-8", errors="replace")
                if do:
                    _git("rm", "-q", "-f", str(i["f"].relative_to(ROOT)))
                    (TOK / new_name).write_text(content, encoding="utf-8")
                    _git("add", str((TOK / new_name).relative_to(ROOT)))
                renames[i["f"].name[:-3]] = new_name[:-3]

    # ---- wikilink 完全一致置換 ----
    if renames:
        pats = {old: re.compile(r"(\[\[)" + re.escape(old) + r"(?=[\]|#])") for old in renames}
        hits = 0
        for md in ROOT.glob("wiki/**/*.md"):
            try:
                t = md.read_text(encoding="utf-8")
            except Exception:
                continue
            orig = t
            for old, new in renames.items():
                t, n = pats[old].subn(r"\1" + new, t)
                hits += n
            if t != orig and do:
                md.write_text(t, encoding="utf-8")
                _git("add", str(md.relative_to(ROOT)))
        if hits:
            acts.append(f"wikilink置換 {hits}箇所")
    return acts


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    for a in normalize(do=(mode == "--fix")):
        print(a)
    dup = subprocess.run(
        f"git -C {ROOT} ls-files wiki/entities/tokens/ | tr 'A-Z' 'a-z' | sort | uniq -d",
        shell=True, capture_output=True, text=True).stdout.strip()
    if mode == "--check" and dup:
        print("REMAINING casefold dup:\n" + dup)
        sys.exit(1)
    print(f"casefold dup: {'0' if not dup else 'STILL ' + str(len(dup.splitlines()))}")
