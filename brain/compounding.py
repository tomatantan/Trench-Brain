#!/usr/bin/env python3
"""brain/compounding.py — the compounding meter (moat gauge).

Measures whether the wiki is genuinely getting SMARTER over time (compounding)
or just BIGGER (scrape-heap = "積んだフリ"). The moat is accumulation that can't
be time-shortcut — but only if it truly compounds. This is the instrument that
proves it, mechanically, from git history.

Core question: are the entities (facts) being WOVEN into concepts (synthesis),
or piling up orphaned? Rising density + connectedness while the corpus grows =
real compounding. Corpus grows but connectedness falls = rotting into a scrape.

Deterministic, stdlib only, read-only. Reads any git rev so it can chart the
trajectory, not just a single snapshot.

Usage:
  python3 brain/compounding.py                 # trajectory: ~7d ago -> now
  python3 brain/compounding.py --since "14 days ago"
  python3 brain/compounding.py --rev <sha>     # single snapshot at a rev
Appends the current reading to brain/state/compounding_history.jsonl.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "brain", "state", "compounding_history.jsonl")
LINK = re.compile(r"\[\[([^\]|]+)")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, "-c", "core.quotepath=false", *args],
                          capture_output=True, text=True).stdout


def norm(name):
    return name.strip().lstrip("$@").lower().replace(" ", "-")


def ls(rev, path):
    out = git("ls-tree", "-r", "--name-only", rev, "--", path)
    return [l for l in out.splitlines() if l.endswith(".md")]


def measure(rev):
    """Compute compounding metrics for the wiki at a git rev."""
    concepts = ls(rev, "wiki/concepts")
    entities = ls(rev, "wiki/entities")
    if not concepts and not entities:
        return None

    total_links = 0
    contradictions = 0
    link_targets = set()
    depth_samples = []
    for cf in concepts:
        body = git("show", f"{rev}:{cf}")
        links = LINK.findall(body)
        total_links += len(links)
        contradictions += body.count("⚠️")
        tset = {norm(t) for t in links}
        link_targets |= tset
        depth_samples.append(len(tset))   # distinct things woven into this concept

    ent_stems = {norm(os.path.splitext(os.path.basename(e))[0]) for e in entities}
    referenced = len(ent_stems & link_targets)

    n_c, n_e = len(concepts), len(entities)
    return {
        "rev": git("rev-parse", "--short", rev).strip(),
        "n_concepts": n_c,
        "n_entities": n_e,
        "total_concept_links": total_links,
        "avg_links_per_concept": round(total_links / n_c, 1) if n_c else 0,
        "avg_depth_per_concept": round(sum(depth_samples) / n_c, 1) if n_c else 0,
        "contradictions_surfaced": contradictions,
        "entities_referenced": referenced,
        # THE headline: fraction of the fact-pile actually woven into synthesis
        "connectedness_pct": round(referenced / n_e * 100, 1) if n_e else 0,
    }


def health_backlog():
    p = os.path.join(ROOT, "brain", "state", "health.jsonl")
    try:
        with open(p, encoding="utf-8") as f:
            last = f.readlines()[-1]
        return json.loads(last).get("signal_backlog")
    except Exception:  # noqa: BLE001
        return None


def delta(old, new):
    keys = ["n_concepts", "n_entities", "avg_links_per_concept",
            "avg_depth_per_concept", "connectedness_pct", "contradictions_surfaced"]
    return {k: round(new[k] - old[k], 1) for k in keys}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="7 days ago")
    ap.add_argument("--rev", default=None)
    args = ap.parse_args()

    now = measure(args.rev or "HEAD")
    if now is None:
        print(json.dumps({"ok": False, "error": "no wiki concepts/entities at rev"}))
        sys.exit(2)
    now["signal_backlog"] = health_backlog()
    now["ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    result = {"ok": True, "now": now}

    if not args.rev:
        old_sha = git("rev-list", "-1", f"--before={args.since}", "HEAD").strip()
        if old_sha:
            old = measure(old_sha)
            if old:
                d = delta(old, now)
                result["baseline"] = {"since": args.since, **old}
                result["delta"] = d
                # compounding verdict: smarter (density/connectedness up) vs just bigger
                grew = d["n_entities"] > 0
                wove = d["connectedness_pct"] >= 0 and d["avg_depth_per_concept"] >= 0
                result["verdict"] = (
                    "compounding" if (d["avg_links_per_concept"] > 0 or d["connectedness_pct"] > 0)
                    else "flat/at-risk" if grew and not wove
                    else "stable")

        # append snapshot to history (trajectory builds over time)
        try:
            with open(HIST, "a", encoding="utf-8") as f:
                f.write(json.dumps(now, ensure_ascii=False) + "\n")
        except OSError:
            pass

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
