// relatedWallets.js  （連結）
// ───────────────────────────────────────────────────────────
// 各ウォレットの「資金源（最初にSOLを送ってきた元）」を辿ってウォレット同士を連結する。
// 同じ資金源 = 同じ人/グループが操ってる疑い。
//
// ★重い：取引履歴(getSignaturesForAddress + getTransaction)依存。RPCは rpcFailover 経由
//   （HEAVY_METHODSなので自動でPublicNode優先に振られる）。
//   全候補に回さず "最後の篩" で少数にだけ。YAJUscanの related-wallets 実物に差し替え可。
// ───────────────────────────────────────────────────────────
import { rpcCall } from "./rpcFailover.js";

/**
 * 1ウォレットの資金源(funder)。最古txでSOLを最も払った相手＝funder候補。
 * ※簡易版：直近1000署名の最古を起点。厳密化はページングで真の最古へ。
 */
export async function getFundingSource(wallet) {
  const sigs = await rpcCall("getSignaturesForAddress", [wallet, { limit: 1000 }]);
  if (!sigs || !sigs.length) return null;
  const oldest = sigs[sigs.length - 1].signature;
  const tx = await rpcCall("getTransaction", [oldest, { maxSupportedTransactionVersion: 0, encoding: "jsonParsed" }]);
  const keys = tx?.transaction?.message?.accountKeys || [];
  const pre = tx?.meta?.preBalances || [];
  const post = tx?.meta?.postBalances || [];
  let funder = null, maxOut = 0;
  keys.forEach((k, i) => {
    const addr = k.pubkey || k;
    if (addr === wallet) return;
    const out = (pre[i] || 0) - (post[i] || 0);
    if (out > maxOut) { maxOut = out; funder = addr; }
  });
  return funder;
}

/**
 * ウォレット配列 → [{ wallet, funder }] の連結リスト
 */
export async function linkWallets(wallets) {
  const out = [];
  for (const w of wallets) {
    try { out.push({ wallet: w, funder: await getFundingSource(w) }); }
    catch (_) { out.push({ wallet: w, funder: null }); }
  }
  return out;
}
