// ingest/run.mjs — Trench-Brain 多層 ingest エンジン（無料・鍵不要ソース）
// X(syndication) / News(RSS) / DefiLlama / Reddit を取得 → sources/<type>/ に保存。
// 既存ファイル名でdedup（新規だけ保存）。GitHub Actions(無料cron)からも回せる。
//
// 使い方:
//   node ingest/run.mjs --dry            … 取得して件数/サンプルだけ（保存しない）
//   node ingest/run.mjs --limit=5        … 各ソース上限5件
//   node ingest/run.mjs                  … 全部 取得して保存
//   node ingest/run.mjs --only=x,news    … 指定ソースだけ
//
// 設計: ソースごとの adapter を足すだけ＝多層化。鍵が要るもの(CryptoPanic/Neynar/Podcast全文)は別途。

import { readFileSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const DRY = args.includes("--dry");
const LIMIT = Number((args.find(a => a.startsWith("--limit=")) || "").split("=")[1] || 0) || 0;
const ONLY = ((args.find(a => a.startsWith("--only=")) || "").split("=")[1] || "").split(",").filter(Boolean);
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36";

const NEWS_FEEDS = [
  ["decrypt", "https://decrypt.co/feed"],
  ["coindesk", "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"],
  ["cointelegraph", "https://cointelegraph.com/rss"],
  ["bankless", "https://www.bankless.com/rss/feed"],
];
const SUBREDDITS = ["CryptoCurrency", "solana"];

const OFFSET = Number((args.find(a => a.startsWith("--offset=")) || "").split("=")[1] || 0) || 0;
const COUNT = Number((args.find(a => a.startsWith("--count=")) || "").split("=")[1] || 0) || 0;
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const slug = (s) => (s || "").replace(/[\\/:*?"<>|#\[\]\n]/g, "").replace(/\s+/g, " ").trim().slice(0, 80);
async function get(url, opts = {}) {
  const ctrl = new AbortController();
  const to = setTimeout(() => ctrl.abort(), opts.timeout || 8000);
  try {
    const r = await fetch(url, { headers: { "User-Agent": UA, ...(opts.headers || {}) }, signal: ctrl.signal });
    return opts.json ? r.json() : r.text();
  } finally { clearTimeout(to); }
}
function decode(s) {
  return (s || "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'")
    .replace(/\\n/g, "\n").replace(/\\"/g, '"').replace(/&[a-z#0-9]+;/gi, " ");
}
function stripTags(s) { return decode((s || "").replace(/<[^>]+>/g, " ")).replace(/\s+/g, " ").trim(); }

// ---- adapters ----
function watchlistHandles() {
  try {
    const md = readFileSync(join(ROOT, "wiki/watchlist.md"), "utf-8");
    const set = new Set();
    for (const m of md.matchAll(/\[\[@([A-Za-z0-9_]+)\]\]/g)) set.add(m[1]);
    return [...set];
  } catch { return []; }
}
function findTweets(node, out = []) {
  if (!node || typeof node !== "object") return out;
  if (node.full_text && (node.id_str || node.id)) {
    out.push({
      id: String(node.id_str || node.id),
      text: node.full_text,
      created_at: node.created_at || "",
      likes: node.favorite_count || 0,
      screen: (node.user && node.user.screen_name) || node.screen_name || "",
    });
  }
  for (const k of Object.keys(node)) if (typeof node[k] === "object") findTweets(node[k], out);
  return out;
}
const NITTERS = ["https://nitter.net", "https://nitter.poast.org"];
async function xFromNitter(h) {
  for (const base of NITTERS) {
    try {
      const xml = await get(`${base}/${h}/rss`, { timeout: 6000 });
      if (xml.length < 300 || /<title>.*(error|not found)/i.test(xml.slice(0, 200))) continue;
      const out = [];
      for (const it of parseFeed(xml)) {
        const idm = (it.link || "").match(/status\/(\d+)/);
        const id = idm ? idm[1] : String(Math.abs([...it.title].reduce((a, c) => a * 31 + c.charCodeAt(0) | 0, 7)));
        out.push({ id, text: it.title + (it.desc && it.desc !== it.title ? "\n\n" + it.desc : ""), screen: h, created_at: it.date });
      }
      if (out.length) return out;
    } catch {}
  }
  return [];
}
async function xFromSyndication(h) {
  const html = await get(`https://syndication.twitter.com/srv/timeline-profile/screen-name/${h}`, { timeout: 8000 });
  if (html.length < 500) return []; // blocked/empty
  let tweets = [];
  const m = html.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
  if (m) { try { tweets = findTweets(JSON.parse(m[1])); } catch {} }
  if (!tweets.length) for (const fm of html.matchAll(/"full_text":"((?:[^"\\]|\\.)*)"/g)) tweets.push({ id: "", text: fm[1], screen: h });
  return tweets;
}
async function fetchX() {
  let handles = watchlistHandles();
  if (COUNT) handles = handles.slice(OFFSET, OFFSET + COUNT); // バッチ処理（cronで分割）
  const items = [];
  for (const h of handles) {
    try {
      let tweets = await xFromSyndication(h).catch(() => []); // 速い・確実、バーストだけ注意
      if (!tweets.length) tweets = await xFromNitter(h).catch(() => []); // フォールバック
      tweets = (tweets || []).slice(0, LIMIT || 25);
      const seen = new Set();
      let n = 0;
      for (const t of tweets) {
        const id = t.id || String(Math.abs([...t.text].reduce((a, c) => a * 31 + c.charCodeAt(0) | 0, 7)));
        if (seen.has(id)) continue; seen.add(id);
        items.push({ type: "x", id: `${h}__${id}`, author: t.screen || h, title: `@${t.screen || h}`, text: decode(t.text), source: `https://x.com/${h}/status/${t.id || id}`, ts: t.created_at || "", likes: t.likes || 0 });
        if (LIMIT && ++n >= LIMIT) break;
      }
      await sleep(700); // レート制限回避（バースト禁物）
    } catch { /* skip handle */ }
  }
  return items;
}
function parseFeed(xml, kind) {
  const items = [];
  const blocks = xml.match(/<item[\s>][\s\S]*?<\/item>/gi) || xml.match(/<entry[\s>][\s\S]*?<\/entry>/gi) || [];
  for (const b of blocks) {
    const title = stripTags((b.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || "");
    let link = (b.match(/<link[^>]*href="([^"]+)"/i) || [])[1] || stripTags((b.match(/<link>([\s\S]*?)<\/link>/i) || [])[1] || "");
    const desc = stripTags((b.match(/<(?:description|summary|content)[^>]*>([\s\S]*?)<\/(?:description|summary|content)>/i) || [])[1] || "").slice(0, 1200);
    const date = stripTags((b.match(/<(?:pubDate|updated|published)>([\s\S]*?)<\/(?:pubDate|updated|published)>/i) || [])[1] || "");
    if (title) items.push({ title, link, desc, date });
  }
  return items;
}
async function fetchNews() {
  const out = [];
  for (const [name, url] of NEWS_FEEDS) {
    try {
      const xml = await get(url);
      let n = 0;
      for (const it of parseFeed(xml)) {
        const id = slug(it.link || it.title).replace(/https?:\/\//, "").replace(/[/.]/g, "_").slice(0, 80);
        out.push({ type: "news", id: `${name}__${id}`, author: name, title: it.title, text: `${it.title}\n\n${it.desc}`, source: it.link, ts: it.date });
        if (LIMIT && ++n >= LIMIT) break;
      }
      await sleep(100);
    } catch {}
  }
  return out;
}
async function fetchReddit() {
  const out = [];
  for (const sub of SUBREDDITS) {
    try {
      const xml = await get(`https://www.reddit.com/r/${sub}/top/.rss?t=day`);
      let n = 0;
      for (const it of parseFeed(xml)) {
        const id = slug(it.link).replace(/https?:\/\//, "").replace(/[/.]/g, "_").slice(0, 80);
        out.push({ type: "reddit", id: `${sub}__${id}`, author: `r/${sub}`, title: it.title, text: `${it.title}\n\n${it.desc}`, source: it.link, ts: it.date });
        if (LIMIT && ++n >= LIMIT) break;
      }
      await sleep(100);
    } catch {}
  }
  return out;
}
async function fetchLlama() {
  const out = [];
  try {
    const ps = await get("https://api.llama.fi/protocols", { json: true });
    const ranked = ps.filter(p => (p.tvl || 0) > 1e6 && typeof p.change_1d === "number")
      .sort((a, b) => Math.abs(b.change_1d) - Math.abs(a.change_1d)).slice(0, LIMIT || 30);
    for (const p of ranked) {
      out.push({
        type: "onchain", id: `llama__${slug(p.slug || p.name)}__${new Date().toISOString().slice(0, 10)}`,
        author: "DefiLlama", title: `${p.name} TVL $${Math.round(p.tvl).toLocaleString()} (24h ${p.change_1d.toFixed(1)}%)`,
        text: `${p.name} (${p.category||""}, ${(p.chains||[]).join("/")}) — TVL $${Math.round(p.tvl).toLocaleString()}, 24h変化 ${p.change_1d.toFixed(2)}%, 7d ${p.change_7d??"?"}%`,
        source: `https://defillama.com/protocol/${p.slug || ""}`, ts: new Date().toISOString(),
      });
    }
  } catch {}
  return out;
}

function save(it) {
  const dir = join(ROOT, "sources", it.type);
  const fp = join(dir, `${slug(it.id)}.md`);
  if (existsSync(fp)) return false;
  if (DRY) return true;
  mkdirSync(dir, { recursive: true });
  const fm = `---\ntype: source\nlayer: ${it.type}\nauthor: ${it.author || ""}\nsource: ${it.source || ""}\nts: ${it.ts || ""}\ningested_at: ${new Date().toISOString()}\n---\n\n`;
  writeFileSync(fp, fm + `# ${it.title}\n\n${it.text}\n`, "utf-8");
  return true;
}

async function main() {
  const all = { x: fetchX, news: fetchNews, reddit: fetchReddit, llama: fetchLlama };
  const run = ONLY.length ? ONLY : Object.keys(all);
  let total = 0, saved = 0;
  for (const k of run) {
    if (!all[k]) continue;
    const items = await all[k]();
    let s = 0;
    for (const it of items) { total++; if (save(it)) s++; }
    saved += s;
    console.log(`[${k}] 取得 ${items.length} / 新規保存 ${s}` + (DRY ? " (dry)" : ""));
    if (DRY && items[0]) console.log(`   例: ${items[0].title} — ${(items[0].text||"").slice(0,80)}`);
  }
  console.log(`=== 計 取得 ${total} / 新規 ${saved}${DRY ? " (dry・未保存)" : " 保存"} ===`);
}
main();
