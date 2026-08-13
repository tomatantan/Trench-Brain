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

★2026-08-13精度改修(本人指示・$mancoin実地調査で見つけた偽陽性を受けて):
  1. limitをHelius上限100にclamp(150等を渡すと400 Bad Requestで即死してた実バグ)。
  2. pump.fun側のbonding_curve/associated_bonding_curve/pump_swap_pool(migrated後のAMM pool)を
     mint情報から取得し「recipient」から除外。従来はswapで機械的に触れるだけのpool自体を
     "2人目の受取人"として誤検知していた(mancoin実測: 生の25 single-tx bundleのうち19件がこれ)。
  3. fee_payerがrecipientsに含まれるか否かでconfidenceを分離: fee_payerが受取人に**含まれない**
     (第三者が複数の別ウォレットに配ってる=最強のbundling signal)場合のみ"strong"、fee_payer自身も
     受取人の一人(自分+誰か1人への送付、で片付く弱いパターン)は"weak"として分ける。判断語ではなく
     観測の強弱ラベル(指針10に沿う)。
  4. "strong"判定でも実地確認で見つけた残穴: 受取人が実は単なる中継/associated-token-account
     (プールとは別カテゴリ)で、その場でtoken残高ゼロに戻る=保有してない=結託した「買い手」とは
     言えないケースがあった(受取人2件とも現残高0で確認)。"strong"判定の各受取人について現在
     そのmintを保有してるかHeliusのbalancesで確認し、保有0のみなら"strong_no_holdings"
     (中継の疑い・保有継続してれば"strong"のまま)に格下げする。追加API呼び出しはstrong件のみ
     (件数が少ない前提)。
"""
import argparse
import json
import os
import sys
from collections import defaultdict

import urllib.request
import urllib.parse

HELIUS_BASE = "https://api.helius.xyz/v0/addresses/{mint}/transactions"
PUMPFUN_COIN = "https://frontend-api-v3.pump.fun/coins/{mint}"


def _get_json(url, params=None, timeout=15):
    full = url + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(full, headers={"User-Agent": "trench-brain"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_early_transfers(mint, api_key, limit=100):
    """Heliusのparsed transactionsからそのmintのtoken transferを取得。limitはHelius側の上限100にclamp
    (100超を渡すと'invalid query parameter limit'で400になり即死する実バグを2026-08-13に確認・修正)。"""
    limit = min(limit, 100)
    url = HELIUS_BASE.format(mint=mint)
    return _get_json(url, {"api-key": api_key, "limit": limit})


def fetch_pool_addresses(mint):
    """pump.fun APIからそのmintのbonding_curve/associated_bonding_curve/pump_swap_pool(migrated後)を取得。
    これらはswapで機械的にtoken transferの片側に現れるだけの infrastructure address であり、
    「もう一人の受取人」として数えると誤検知になる(mancoin実測で確認済み)。取得失敗時は空集合を返し
    (fail-open。除外できないだけで、既存のbundle検知自体は止めない)、呼び出し側で明示する。"""
    try:
        d = _get_json(PUMPFUN_COIN.format(mint=mint))
    except Exception:
        return set(), False
    addrs = {d.get("bonding_curve"), d.get("associated_bonding_curve"), d.get("pump_swap_pool"), d.get("pool_address")}
    return {a for a in addrs if a}, True


def wallet_holds_mint(wallet, mint, api_key, timeout=15):
    """そのwalletが"今"そのmintを保有してるか確認。
    2026-08-13追加→即日修正: 最初 v0 /addresses/{w}/balances REST を使ったが、このエンドポイントが
    セッション中に "Method not found"(404)で死んでるのを発見(全アドレスで再現・エンドポイント側の問題)。
    さらに悪いことに、生きてた時も token-2022 program のtoken(mancoinはこれ)を正しく拾えておらず、
    実際は219,769枚保有してるアドレスを「保有0」と誤判定していた(本人に一度誤った結論を報告→訂正済み)。
    標準の getTokenAccountsByOwner JSON-RPC(mint指定)に切替＝token-2022/classic両対応で確実。"""
    url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner",
        "params": [wallet, {"mint": mint}, {"encoding": "jsonParsed"}],
    }
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"User-Agent": "trench-brain", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception:
        return None  # 取得失敗=不明(0とは区別する)
    for acc in (d.get("result") or {}).get("value", []):
        amt = acc.get("account", {}).get("data", {}).get("parsed", {}).get("info", {}) \
            .get("tokenAmount", {}).get("uiAmount")
        if amt and amt > 0:
            return True
    return False


def detect_single_tx_bundles(txs, mint, exclude=frozenset()):
    """1トランザクションで複数walletへ同時配布=最も強いbundling signal。
    出典: agiprolabs/claude-trench-skills sybil-detection/references/bundler_detection.md を移植。
    exclude: pool/bonding-curve等のinfrastructure addressをrecipient候補から除外(2026-08-13追加)。
    confidence: fee_payerが受取人に含まれない(第三者が複数ウォレットに配布)場合のみ"strong"。
    fee_payer自身も受取人の一人の場合は"weak"(自分+誰か1人、程度の弱いpattern)。"""
    bundled = []
    for tx in txs:
        transfers = [t for t in tx.get("tokenTransfers", []) if t.get("mint") == mint]
        recipients = set(t.get("toUserAccount") for t in transfers if t.get("toUserAccount"))
        recipients -= exclude
        if len(recipients) >= 2:
            fee_payer = tx.get("feePayer", "")
            bundled.append({
                "signature": tx.get("signature", ""),
                "slot": tx.get("slot", 0),
                "recipient_count": len(recipients),
                "recipients": sorted(recipients),
                "fee_payer": fee_payer,
                "confidence": "weak" if fee_payer in recipients else "strong",
            })
    return bundled


def detect_same_slot_clusters(txs, mint, min_wallets=3, exclude=frozenset()):
    """同slotで別トランザクションから買った複数wallet=Jito bundle疑い(実行順保証)。
    出典: 同上、slot単位でグルーピングする実装を移植・簡略化。
    exclude: pool/bonding-curve等のinfrastructure addressを除外(2026-08-13追加)。"""
    slot_groups = defaultdict(set)
    slot_sigs = defaultdict(set)
    for tx in txs:
        transfers = [t for t in tx.get("tokenTransfers", []) if t.get("mint") == mint]
        if not transfers:
            continue
        slot = tx.get("slot", 0)
        slot_sigs[slot].add(tx.get("signature", ""))
        for t in transfers:
            to = t.get("toUserAccount")
            if to and to not in exclude:
                slot_groups[slot].add(to)
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
    ap.add_argument("--limit", type=int, default=100, help="遡るtx数(Helius上限100にclampされる。default 100)")
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

    pool_addrs, pool_fetch_ok = fetch_pool_addresses(args.mint)

    single_tx_bundles = detect_single_tx_bundles(txs, args.mint, exclude=pool_addrs)
    slot_clusters = detect_same_slot_clusters(txs, args.mint, exclude=pool_addrs)

    # ★保有裏取り(2026-08-13): strong判定の受取人が今もそのmintを保有してるか確認。
    #   全員が保有0(受け取った瞬間に右から左=中継アカウントの疑い)なら strong_no_holdings に格下げ。
    #   1人でも保有してれば strong のまま(実際に持ってる=結託した買い手の疑いが本物に近い)。
    holdings_cache = {}
    for b in single_tx_bundles:
        if b["confidence"] != "strong":
            continue
        holds = {}
        for w in b["recipients"]:
            if w not in holdings_cache:
                holdings_cache[w] = wallet_holds_mint(w, args.mint, api_key)
            holds[w] = holdings_cache[w]
        b["recipients_currently_hold"] = holds
        if any(v is True for v in holds.values()):
            pass  # 保有継続してる人がいる=strongのまま
        elif all(v is False for v in holds.values()):
            b["confidence"] = "strong_no_holdings"

    strong = [b for b in single_tx_bundles if b["confidence"] == "strong"]
    strong_no_holdings = [b for b in single_tx_bundles if b["confidence"] == "strong_no_holdings"]
    weak = [b for b in single_tx_bundles if b["confidence"] == "weak"]

    involved_wallets = set()
    for b in single_tx_bundles:
        involved_wallets.update(b["recipients"])
    for c in slot_clusters:
        involved_wallets.update(c["wallets"])

    result = {
        "observed": True,
        "mint": args.mint,
        "tx_scanned": len(txs),
        "pool_addresses_excluded": sorted(pool_addrs),
        "pool_lookup_ok": pool_fetch_ok,
        "single_tx_bundles_strong": len(strong),
        "single_tx_bundles_strong_no_holdings": len(strong_no_holdings),
        "single_tx_bundles_weak": len(weak),
        "same_slot_clusters": len(slot_clusters),
        "involved_wallets": len(involved_wallets),
        "detail": {"single_tx_bundles": single_tx_bundles[:10], "same_slot_clusters": slot_clusters[:10]},
    }
    if not pool_fetch_ok:
        result["caveat"] = "pump.fun API取得失敗＝pool address除外なし。single_tx_bundlesにpool由来の偽陽性が残ってる可能性が高い。"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
