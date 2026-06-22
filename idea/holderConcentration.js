// holderConcentration.js  （ホルダー取得）
// ───────────────────────────────────────────────────────────
// トークンの「ホルダー集中度（top1 / top10 が供給の何%か）」を取る。
//
// "ホルダー比率が取れない" の原因はだいたいコレ↓
//   LP / プール / ボンディングカーブ(pump.fun) のトークンアカウントを除外してない
//   → 「1アドレスが90%保有」みたいに見えて壊れる。除外してから % を出す。
//
// 取得：getTokenLargestAccounts(上位20・無料) ＋ getTokenSupply。RPCは rpcFailover 経由。
// 注意：RPC仕様で上位20まで。memecoin選別なら top10集中度で実用十分。完全分布は有料API。
// ───────────────────────────────────────────────────────────
import { rpcCall } from "./rpcFailover.js";

/**
 * @param {string} mint
 * @param {object} opts
 *   - exclude        : 除外する "トークンアカウントaddress" 配列（LP/pool/dev/CEX）
 *   - dropTop1AsPool : 除外リストが無い時、最大保有をpoolとみなして1件落とす近似
 * @returns {{supply,top1Pct,top10Pct,holders:{account,pct}[]}|null}
 */
export async function getHolderConcentration(mint, opts = {}) {
  const { exclude = [], dropTop1AsPool = false } = opts;
  const ex = new Set(exclude);

  const sup = await rpcCall("getTokenSupply", [mint]);
  const decimals = sup.value.decimals;
  const supply = Number(sup.value.uiAmount) || Number(sup.value.amount) / 10 ** decimals;
  if (!supply) return null;

  const largest = await rpcCall("getTokenLargestAccounts", [mint]);
  let rows = (largest.value || [])
    .map((a) => ({ account: a.address, amount: Number(a.uiAmount) || Number(a.amount) / 10 ** decimals }))
    .filter((r) => !ex.has(r.account))
    .sort((a, b) => b.amount - a.amount);

  if (dropTop1AsPool && rows.length) rows = rows.slice(1);

  const pct = (n) => (n / supply) * 100;
  return {
    supply,
    top1Pct: rows.length ? +pct(rows[0].amount).toFixed(2) : 0,
    top10Pct: +pct(rows.slice(0, 10).reduce((s, r) => s + r.amount, 0)).toFixed(2),
    holders: rows.slice(0, 20).map((r) => ({ account: r.account, pct: +pct(r.amount).toFixed(2) })),
  };
}

// 厳密に owner(ウォレット)単位で集計したい場合は、各 address を getAccountInfo(jsonParsed) で
// owner解決し、既知のpool/AMMプログラム所有を除外する（簡易版で詰まったらそこまで踏む）。
