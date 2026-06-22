// bundleDetect.js  （バンドル）
// ───────────────────────────────────────────────────────────
// ローンチ時に "同一/近接ブロックでまとめて買われた" か（coordinated bundle）を検出。
// 多数のウォレットが launch直後の数ブロックで一斉取得 = バンドル/インサイダー疑い。
//
// ★重い：各ホルダーの取得slot(ブロック高)が要る＝履歴依存。RPCは rpcFailover 経由
//   （HEAVY_METHODS自動振り分け）。最後の篩で少数に。YAJUscanの該当ロジックに差し替え可。
// ───────────────────────────────────────────────────────────
import { rpcCall } from "./rpcFailover.js";

/**
 * @param {string[]} wallets ホルダー（ownerウォレット）
 * @param {string} mint
 * @param {object} opts { windowSlots=5, minBundle=3 }
 * @returns {{ bundles:{startSlot,wallets,size}[], bundledRatio:number }}
 */
export async function detectBundle(wallets, mint, opts = {}) {
  const { windowSlots = 5, minBundle = 3 } = opts;

  // 各walletの最古署名のslot（簡易：取得txに近い前提。厳密化はtoken transferを特定）
  const entries = [];
  for (const w of wallets) {
    try {
      const sigs = await rpcCall("getSignaturesForAddress", [w, { limit: 1000 }]);
      if (sigs && sigs.length) entries.push({ wallet: w, slot: sigs[sigs.length - 1].slot });
    } catch (_) {}
  }
  entries.sort((a, b) => a.slot - b.slot);

  // 近接slotでまとめる
  const bundles = [];
  let cur = [];
  for (const e of entries) {
    if (cur.length && e.slot - cur[0].slot > windowSlots) {
      if (cur.length >= minBundle) bundles.push({ startSlot: cur[0].slot, wallets: cur.map((x) => x.wallet), size: cur.length });
      cur = [];
    }
    cur.push(e);
  }
  if (cur.length >= minBundle) bundles.push({ startSlot: cur[0].slot, wallets: cur.map((x) => x.wallet), size: cur.length });

  const total = entries.length || 1;
  const bundled = bundles.reduce((s, b) => s + b.size, 0);
  return { bundles, bundledRatio: +(bundled / total).toFixed(2) };
}
