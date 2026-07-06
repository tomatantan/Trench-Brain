#!/usr/bin/env python3
"""
Trench-Brain entity builder — LLM Wiki の背骨(entityページ)を自動生成/更新する。

Karpathy の LLM Wiki パターン準拠:
- entityページ = 人/トークン毎に「自動生成され、参照される度に更新される」データの背骨。
- このスクリプトは sources/x/ の信号ツイを集計し、entityページを **冪等に再生成** する
  (= 新ツイ取り込み後に再実行すれば波及更新される)。
- synthesis(物語/動線/矛盾の判断)は concept ページ側でエージェントが行う。entityは事実の集約。

出力:
  wiki/entities/players/@<handle>.md   各監視アカ
  wiki/entities/tokens/$<TICKER>.md    閾値超えの $ticker
"""
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "x"
ENT = ROOT / "wiki" / "entities"
TICKER_RE = re.compile(r"\$[A-Za-z][A-Za-z0-9]{1,9}\b")
URL_RE = re.compile(r"https?://\S+")
NOISE_RE = re.compile(r"^(gm+|gn+|lfg+|wagmi|ngmi|wen|soon|ser|fr+|lol+|gg+|\.+)$", re.I)

# token entity を作る閾値（ノイズ$を弾く）
MIN_NOTES = 3      # 言及ノート数
MIN_ACCOUNTS = 2   # 言及アカ数


def parse(path):
    txt = path.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return None, ""
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return None, ""   # 閉じ---無し(書込み中のtruncated file)でunpack死→run全滅を防ぐ(2026-07-02 M1)
    _, fm, body = parts
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.strip()


def is_noise(meta, body):
    if str(meta.get("is_retweet", "")).lower() == "true":
        return True
    s = re.sub(r"[@#]\w+", "", URL_RE.sub("", body)).strip()
    return len(s) < 12 or bool(NOISE_RE.match(s.replace(" ", "")))


def to_int(s):
    try:
        return int(s)
    except Exception:
        return 0


SYN_START = "<!-- synthesis:start -->"
SYN_END = "<!-- synthesis:end -->"
SYN_DEFAULT = (
    f"{SYN_START}\n## 合成メモ（synthesis / エージェント記述）\n"
    "_（未記入。エージェントがingest時に物語/動線/⚠️矛盾/賭け仮説を追記し、関連する concept ページへリンクする）_\n"
    f"{SYN_END}"
)


def keep_synthesis(path):
    """既存ファイルのsynthesisブロックを保持(再生成で消さない)。"""
    if not path.exists():
        return SYN_DEFAULT
    t = path.read_text(encoding="utf-8")
    i, j = t.find(SYN_START), t.find(SYN_END)
    if i != -1 and j != -1:
        return t[i:j + len(SYN_END)]
    return SYN_DEFAULT


PROF_START = "<!-- profile:start -->"
PROF_END = "<!-- profile:end -->"


def keep_profile(path):
    """curated深堀りprofileブロックを保持。synthesis(cron自動合成)と別枠＝機械が上書きしない層。
    無ければ空(全playerにデフォルト雛形は撒かない=乱造防止)。"""
    if not path.exists():
        return ""
    t = path.read_text(encoding="utf-8")
    i, j = t.find(PROF_START), t.find(PROF_END)
    if i != -1 and j != -1:
        return t[i:j + len(PROF_END)]
    return ""


def snip(body, n=84):
    return html.unescape(URL_RE.sub("", body).replace("\n", " ").replace("|", "/")).strip()[:n]


def main():
    notes = list(SRC.glob("*.md"))
    # 集計
    pl_posts = defaultdict(list)         # handle -> [(likes, body, fname, tickers)]
    pl_tokens = defaultdict(Counter)     # handle -> ticker counts
    tk_notes = defaultdict(list)         # TICKER -> [(likes, account, body, fname)]
    tk_accounts = defaultdict(set)       # TICKER -> {accounts}
    tk_cooc = defaultdict(Counter)       # TICKER -> co-occurring TICKER counts

    for p in notes:
        meta, body = parse(p)
        if meta is None or is_noise(meta, body):
            continue
        acct = meta.get("account", "?")
        via = meta.get("via", acct)
        # ★handle健全化(2026-06-24 bug fix): image/system source の via(例 "/add-image")が
        #   player entity の path を壊す(players/@/add-image.md で crash)のを防ぐ。有効X handle のみ player化。
        def _handle(x):
            # ★lowercase正規化(2026-07-04): X handleはcase-insensitive。caseをそのまま鍵/pathに使うと
            #   同一人物が @RaoulGMI.md / @raoulgmi.md に分裂(実害9ペア)し、macOSのpull/resetも塞ぐ。
            x = str(x or "").lstrip("@").strip().lower()
            return x if re.match(r"^[a-z0-9_]{1,30}$", x) else None
        via_h = _handle(via)
        acct_h = _handle(acct)
        likes = to_int(meta.get("likes"))
        tickers = sorted({t.upper() for t in TICKER_RE.findall(body)})
        # player集計は監視主体(via)に寄せる。handleでない source(画像/system)は player化しない。
        if via_h:
            pl_posts[via_h].append((likes, body, p.stem, tickers))
        for tk in tickers:
            if via_h:
                pl_tokens[via_h][tk] += 1
            tk_notes[tk].append((likes, acct_h or "?", body, p.stem))
            if acct_h:
                tk_accounts[tk].add(acct_h)
            for other in tickers:
                if other != tk:
                    tk_cooc[tk][other] += 1

    (ENT / "players").mkdir(parents=True, exist_ok=True)
    (ENT / "tokens").mkdir(parents=True, exist_ok=True)
    n_pl = n_tk = 0

    # ---- token entity ----
    for tk, notes_ in tk_notes.items():
        if len(notes_) < MIN_NOTES or len(tk_accounts[tk]) < MIN_ACCOUNTS:
            continue
        n_tk += 1
        notes_.sort(reverse=True)
        accts = sorted(tk_accounts[tk])
        cooc = [f"[[{t}]]" for t, _ in tk_cooc[tk].most_common(8)]
        # ac="?"(handle不明)は [[@?]] の壊れリンクになる→リンクにせず素の"?"にする(dangling根絶)
        rows = [f"| {lk:,} | {('[[@'+ac+']]') if ac != '?' else '?'} | {snip(bd)} | [[{fn}]] |"
                for lk, ac, bd, fn in notes_[:10]]
        page = [
            "---", "type: entity", "kind: token", f"title: {tk}",
            "updated: 2026-06-22", "tags: [trench, entity, token]",
            f"mentions: {len(notes_)}", f"accounts: {len(accts)}", "---", "",
            f"# {tk}", "",
            f"> 自動生成(brain/build_entities.py)。言及 {len(notes_)}件 / {len(accts)}アカ。",
            "事実=この自動集約 / 判断=下の合成メモ＋関連する concept ページ。", "",
            "## 言及アカウント", " ".join(f"[[@{a}]]" for a in accts), "",
            "## 共起トークン", " ".join(cooc) or "—", "",
            "## 高エンゲージ言及",
            "| likes | account | 抜粋 | source |", "|---|---|---|---|",
            *rows, "",
            *([kp, ""] if (kp := keep_profile(ENT / "tokens" / f"{tk}.md")) else []),
            keep_synthesis(ENT / "tokens" / f"{tk}.md"), "",
        ]
        (ENT / "tokens" / f"{tk}.md").write_text("\n".join(page), encoding="utf-8")

    # KOL track-record(call生存率)を entity に焼く=信頼性の合成(kol_track_record.py が生成・/checkも読む)
    ktr_f = ROOT / "brain" / "state" / "kol_track_records.json"
    try:
        ktr = json.loads(ktr_f.read_text(encoding="utf-8")) if ktr_f.exists() else {}
    except Exception:
        ktr = {}

    # ---- player entity ----
    for h, posts in pl_posts.items():
        n_pl += 1
        posts.sort(reverse=True)
        toptok = [f"[[{t}]]({c})" for t, c in pl_tokens[h].most_common(10)]
        rows = [f"| {lk:,} | {' '.join('[['+t+']]' for t in tks[:3])} | {snip(bd)} | [[{fn}]] |"
                for lk, bd, fn, tks in posts[:10]]
        hl = h.lower()
        tr = ktr.get(hl) or ktr.get(hl.rstrip("_")) or ktr.get(hl + "_")  # handle variant(末尾_)も照合
        dr = tr.get("death_rate") if tr else None
        if tr and tr.get("evaluated", 0) >= 2 and dr is not None:
            read = "⚠️callの死多(信頼性低)" if (dr or 0) >= 70 else "平均的" if (dr or 0) >= 40 else "callが残りやすい(相対的に注目)"
            tr_section = [f"## call track-record（[[manipulation-playbook]]・[[kol-track-records]]）",
                          f"CA言及 {tr.get('mentioned', '?')}件 / 現outcome評価 {tr.get('evaluated', '?')}件中 **死{tr.get('dead', '?')}（{dr}%）** ＝{read}。",
                          "> ★近似(現mcap基準)・小N。母集団は[[launchpad-economics]]で大半死＝相対比較で読む。", ""]
        else:
            tr_section = []
        page = [
            "---", "type: entity", "kind: player", f"title: @{h}",
            "updated: 2026-06-22", "tags: [trench, entity, player]",
            f"posts: {len(posts)}", "---", "",
            f"# @{h}", "",
            f"> 自動生成。信号投稿 {len(posts)}件。watchlist: [[watchlist]]。", "",
            *tr_section,
            "## よく言及するトークン", " ".join(toptok) or "—", "",
            "## 高エンゲージ投稿",
            "| likes | tickers | 抜粋 | source |", "|---|---|---|---|",
            *rows, "",
            *([kp, ""] if (kp := keep_profile(ENT / "players" / f"@{h}.md")) else []),
            keep_synthesis(ENT / "players" / f"@{h}.md"), "",
        ]
        (ENT / "players" / f"@{h}.md").write_text("\n".join(page), encoding="utf-8")

    print(f"entities written: {n_pl} players, {n_tk} tokens")


if __name__ == "__main__":
    main()
