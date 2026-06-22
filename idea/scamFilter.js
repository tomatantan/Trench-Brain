// scamFilter.js
// ───────────────────────────────────────────────────────────
// 目的：地雷トークンを除外する純関数（YAJUscanの SCAM_FILTER 相当）。
//      トークンの属性を渡すと pass(true/false) と 落ちた理由 を返す。
//      ※属性の取得自体は別（rugcheck系API / オンチェーン / holderConcentration / marketStats）。
//        ここは "閾値判定だけ" を担う純粋ロジックなのでテストしやすく流用しやすい。
// ───────────────────────────────────────────────────────────

/**
 * @param {object} t トークン属性（取れたものだけでOK。未定義はスキップ）
 *   rugged          : 既知のrug (boolean)
 *   mintAuthority   : mint権限が残ってる (boolean)  ← 追加発行できる=危険
 *   freezeAuthority : freeze権限が残ってる (boolean) ← 送金凍結できる=危険
 *   mutable         : メタデータ可変 (boolean)
 *   transferFeePct  : 送金税(%) (number)
 *   lpPct           : LPロック/バーン率(%) (number)  ← 低い=抜かれるリスク
 *   top10Pct        : 上位10保有の集中度(%) (number) ← holderConcentrationから
 *   liquidityUsd    : 流動性(USD) (number)
 * @param {object} cfg 閾値の上書き
 * @returns {{pass:boolean, reasons:string[]}}
 */
export function scamFilter(t = {}, cfg = {}) {
  const c = {
    maxTop10Pct: 90,       // これ以上集中してたら除外
    minLpPct: 50,          // これ未満のLPは除外
    minLiquidityUsd: 2000, // これ未満の流動性は除外
    maxTransferFeePct: 0,  // 送金税があれば除外
    ...cfg,
  };
  const reasons = [];
  if (t.rugged) reasons.push("rugged");
  if (t.mintAuthority) reasons.push("mint権限が残存");
  if (t.freezeAuthority) reasons.push("freeze権限が残存");
  if (t.mutable) reasons.push("メタデータ可変");
  if (t.transferFeePct != null && t.transferFeePct > c.maxTransferFeePct) reasons.push(`送金税 ${t.transferFeePct}%`);
  if (t.lpPct != null && t.lpPct < c.minLpPct) reasons.push(`LP ${t.lpPct}%（薄い）`);
  if (t.top10Pct != null && t.top10Pct > c.maxTop10Pct) reasons.push(`top10集中 ${t.top10Pct}%`);
  if (t.liquidityUsd != null && t.liquidityUsd < c.minLiquidityUsd) reasons.push(`流動性 $${Math.round(t.liquidityUsd)}`);
  return { pass: reasons.length === 0, reasons };
}
