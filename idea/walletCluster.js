// walletCluster.js  （クラスター）
// ───────────────────────────────────────────────────────────
// 連結(relatedWallets)の結果 [{wallet, funder}] を、funderごとにグルーピング → クラスタ化。
// 1つのfunder配下に多数ウォレット = 1エンティティが分けて保有 = 偽の分散 / バンドル疑い。
//
// この関数自体は純関数（I/O無し）＝軽い・テストしやすい。
// 重いのは前段の linkWallets（履歴取得）の方。だからクラスタ化は最後に少数へ。
// ───────────────────────────────────────────────────────────

/**
 * @param {{wallet:string, funder:string|null}[]} links  relatedWallets.linkWallets の出力
 * @param {object} opts { minClusterSize=2 }  この人数以上を「クラスタ」とみなす
 * @returns {{
 *   clusters: {funder:string, wallets:string[], size:number}[],  // size降順
 *   clusteredRatio: number,   // クラスタ(2件以上)に属するウォレットの割合(0-1)。高い=偽分散の疑い
 *   biggest: number           // 最大クラスタの人数
 * }}
 */
export function clusterByFunder(links, opts = {}) {
  const { minClusterSize = 2 } = opts;
  const byFunder = new Map();
  for (const { wallet, funder } of links) {
    if (!funder) continue;
    if (!byFunder.has(funder)) byFunder.set(funder, []);
    byFunder.get(funder).push(wallet);
  }
  const clusters = [...byFunder.entries()]
    .map(([funder, wallets]) => ({ funder, wallets, size: wallets.length }))
    .filter((c) => c.size >= minClusterSize)
    .sort((a, b) => b.size - a.size);

  const total = links.length || 1;
  const clustered = clusters.reduce((s, c) => s + c.size, 0);
  return {
    clusters,
    clusteredRatio: +(clustered / total).toFixed(2),
    biggest: clusters[0]?.size || 0,
  };
}
