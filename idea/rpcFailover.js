// rpcFailover.js
// ───────────────────────────────────────────────────────────
// 複数の無料Solana RPCを failover で回す共通RPCクライアント。
// さらに「重い履歴メソッド(getSignaturesForAddress / getTransaction 等)」だけは
// 履歴に強いRPC(PublicNode)を最優先に振る = method-aware routing。
//
// 由来：YAJUscan の multi-rpc.ts のエッセンス。共有IP(Vercel等)が無料公共RPCに
//       重い履歴メソッドを弾かれる問題の対策で入れたやつ。
//       ※YAJUscanの実物(失敗カウント/クールダウン等込み)に差し替え可。これは要点版。
// ───────────────────────────────────────────────────────────

// 履歴系＝重い。これらは HEAVY_RPCS を優先で回す。
const HEAVY_METHODS = new Set([
  "getSignaturesForAddress",
  "getTransaction",
  "getBlock",
  "getBlockTime",
]);

// 履歴に強い順（PublicNodeはkeylessでarchival寄り）
const HEAVY_RPCS = [
  "https://solana-rpc.publicnode.com",
  "https://api.mainnet-beta.solana.com",
];

// 軽い汎用メソッド用（getTokenSupply / getTokenLargestAccounts / getAccountInfo 等）
const GENERAL_RPCS = [
  "https://api.mainnet-beta.solana.com",
  "https://solana-rpc.publicnode.com",
  "https://rpc.ankr.com/solana",
];

/**
 * failover付きRPC呼び出し。method種別で送り先を自動振り分け。
 * @param {string} method  JSON-RPCメソッド
 * @param {any[]} params
 * @param {object} opts { rpcs?: string[] }  rpcs指定で送り先を上書き
 * @returns RPC result
 */
export async function rpcCall(method, params, opts = {}) {
  const list = opts.rpcs || (HEAVY_METHODS.has(method) ? HEAVY_RPCS : GENERAL_RPCS);
  let lastErr;
  for (const url of list) {
    try {
      const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params }),
      });
      if (!r.ok) { lastErr = new Error(`${url} HTTP ${r.status}`); continue; }
      const j = await r.json();
      if (j.error) { lastErr = new Error(j.error.message); continue; }
      return j.result;
    } catch (e) { lastErr = e; }
  }
  throw new Error(`RPC失敗(${method}): ${lastErr?.message || "全RPCで失敗"}`);
}
