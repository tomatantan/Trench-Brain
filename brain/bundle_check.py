#!/usr/bin/env python3
"""
bundle_check.py — 門通過token の早期買いに bundling(insider結託) の跡が無いか観測する。LLM不使用。

★出典・帰属: 検出ロジックは agiprolabs/claude-trading-skills (MIT License, Copyright (c) 2026 AGIPro)
  の `skills/sybil-detection` を本人指示(2026-08-06「有益なスキル盗んでこい」)で調査・移植。
  元実装のfunding-source/co-trade/bundle判定パターンをtrench-brain向けに書き直した。
  https://github.com/agiprolabs/claude-trading-skills （MITなので改変・組込み可・帰属明記で足りる）

★なぜ作ったか: 監査(2026-08-06)で「on-chain event collectorが無い」という穴を指摘したが、
  当初考えてた「大口転送を単純監視」は甘い設計だった(WebSearch調査で判明＝本物の結託検知は
  資金フロー/同slot買い集中のグラフ分析が要る)。既存の実装(sybil-detection skill)を
  調べたら Helius API 一発で実用的な検知ができるパターンが見つかった＝ゼロから設計するより先に盗む。

★観測の言葉で報告する(CLAUDE.md 指針10): 「rug/avoid」等の判断語は出さない。
  bundle_ratio・bundled_supply_pct・関与walletの数だけを返す。判断はca-check/本人の仕事。

必要credential: HELIUS_API_KEY (.env)。無ければ「無いので観測できない」と明示して止まる
  (pumpfun-scout skillの原則「キーが無ければ黙ってスキップしない」に合わせた)。
"""
import argparse
import json
import os
import sys
from collections import defaultdict

import urllib.request
import urllib.parse

HELIUS_BASE = "https://api.helius.xyz/v0/addresses/{mint}/transactions"


def _get_json(url, params, timeout=15):
    full = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, headers={"User-Agent": "trench-brain"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_early_transfers(mint, api_key, limit=100):
    """Heliusのparsed transactionsからそのmintのtoken transferを取得。"""
    url = HELIUS_BASE.format(mint=mint)
    return _get_json(url, {"api-key": api_key, "limit": limit})


def detect_single_tx_bundles(txs, mint):
    """1トランザクションで複数walletへ同時配布=最も強いbundling signal。
    出典: agiprolabs/claude-trench-skills sybil-detection/references/bundler_detection.md を移植。"""
    bundled = []
    for tx in txs:
        transfers = [t for t in tx.get("tokenTransfers", []) if t.get("mint") == mint]
        recipients = set(t.get("toUserAccount") for t in transfers if t.get("toUserAccount"))
        if len(recipients) >= 2:
            bundled.append({
                "signature": tx.get("signature", ""),
                "slot": tx.get("slot", 0),
                "recipient_count": len(recipients),
                "recipients": sorted(recipients),
                "fee_payer": tx.get("feePayer", ""),
            })
    return bundled


def detect_same_slot_clusters(txs, mint, min_wallets=3):
    """同slotで別トランザクションから買った複数wallet=Jito bundle疑い(実行順保証)。
    出典: 同上、slot単位でグルーピングする実装を移植・簡略化。"""
    slot_groups = defaultdict(set)
    slot_sigs = defaultdict(set)
    for tx in txs:
        transfers = [t for t in tx.get("tokenTransfers", []) if t.get("mint") == mint]
        if not transfers:
            continue
        slot = tx.get("slot", 0)
        slot_sigs[slot].add(tx.get("signature", ""))
        for t in transfers:
            if t.get("toUserAccount"):
                slot_groups[slot].add(t["toUserAccount"])
    clusters = []
    for slot, wallets in slot_groups.items():
        if len(wallets) >= min_wallets:
            clusters.append({
                "slot": slot,
                "wallet_count": len(wallets),
                "tx_count": len(slot_sigs[slot]),
                "wallets": sorted(wallets),
            })
    return sorted(clusters, key=lambda c: c["slot"])


def main():
    ap = argparse.ArgumentParser(description="早期bundling観測(insider結託の兆候)")
    ap.add_argument("mint", help="観測対象のtoken mint address")
    ap.add_argument("--limit", type=int, default=100, help="遡るtx数(default 100)")
    args = ap.parse_args()

    api_key = os.environ.get("HELIUS_API_KEY")
    if not api_key:
        print(json.dumps({
            "observed": False,
            "reason": "HELIUS_API_KEY が .env に無い。この観測はできない(黙ってスキップしない)。",
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        txs = fetch_early_transfers(args.mint, api_key, args.limit)
    except Exception as e:
        print(json.dumps({"observed": False, "reason": f"Helius取得失敗: {e}"}, ensure_ascii=False))
        sys.exit(1)

    single_tx_bundles = detect_single_tx_bundles(txs, args.mint)
    slot_clusters = detect_same_slot_clusters(txs, args.mint)

    involved_wallets = set()
    for b in single_tx_bundles:
        involved_wallets.update(b["recipients"])
    for c in slot_clusters:
        involved_wallets.update(c["wallets"])

    result = {
        "observed": True,
        "mint": args.mint,
        "tx_scanned": len(txs),
        "single_tx_bundles": len(single_tx_bundles),
        "same_slot_clusters": len(slot_clusters),
        "involved_wallets": len(involved_wallets),
        "detail": {"single_tx_bundles": single_tx_bundles[:10], "same_slot_clusters": slot_clusters[:10]},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
