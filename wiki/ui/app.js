const DATA_URLS = ["../ui-data.json", "https://raw.githubusercontent.com/tomatantan/Trench-Brain/main/wiki/ui-data.json"];

const API_BASE = "/api";

const fallbackSignals = [
  {
    word: "PERSIAN GULF",
    type: "WORLD",
    accounts: 4,
    area: "GLOBAL",
    observed: "mock",
    summary: "A geopolitical phrase where shipping lanes, oil, and security narratives converge.",
    events: [["NOW", "WORLD", "Maritime security references increased", "GLOBAL", "mock source"]],
    posts: [["@WhiteHouse", "Regional security remarks are being watched by CT.", "mock"]],
    history: [["2019", "TANKER", "Shipping-route anxiety translated into market memes."]],
    why: "Short, visual, and map-friendly. Easy to compress into a meme symbol."
  },
  {
    word: "CONVICTION POSTING",
    type: "MEME KOL",
    accounts: 2,
    area: "CT",
    observed: "mock",
    summary: "A repeated KOL behavior where belief itself becomes the content.",
    events: [["NOW", "KOL", "Large accounts repeatedly pushed the same meme", "CT", "mock source"]],
    posts: [["@theunipcs", "still here, still posting, still believe", "mock"]],
    history: [["2021", "LASER EYES", "Belief became a profile symbol."]],
    why: "Persona, repetition, and belief make it useful both for support and backlash."
  }
];

let state = {
  signals: fallbackSignals,
  launches: [],
  baseRate: null,
  selected: fallbackSignals[0],
  category: "ALL",
  activeTool: "terminal",
  callFilter: "ALL",
  selectedCall: null,
  backendLive: false,
  queue: JSON.parse(localStorage.getItem("trenchBrainLearningQueue") || "[]")
};

const $ = (selector) => document.querySelector(selector);

async function apiGet(path, params = {}, options = {}) {
  const url = new URL(`${API_BASE}${path}`, window.location.origin);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, value);
  });
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs || 2600);
  try {
    const response = await fetch(url, { cache: "no-store", signal: controller.signal });
    if (response.status === 429) throw new Error("rate limited / 429");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const json = await response.json();
    if (json && json.ok === false) throw new Error(json.error || "backend ok:false");
    return json;
  } finally {
    clearTimeout(timeout);
  }
}

function apiErrorMessage(status, fallback = "backend unavailable") {
  if (status === 429 || String(fallback).includes("429")) return "連投しすぎ。少し待ってから再送してください。";
  if (status === 504 || String(fallback).includes("504")) return "時間内に返せず。問いを短くして再送してください。";
  if (status >= 500 || String(fallback).includes("500")) return "backend側で空応答または処理失敗。少し待って再送してください。";
  return fallback || "backend unavailable";
}

function renderMarkdownInline(text) {
  return escapeHtml(text || "")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[\[([^\]]+)\]\]/g, '<span class="cite">[[$1]]</span>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/__([^_]+)__/g, "<strong>$1</strong>")
    .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
}

function renderAskMarkdown(answer) {
  const source = String(answer || "").trim();
  if (!source) return `<div class="brain-answer"><p>No answer returned from /api/ask.</p></div>`;

  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  const html = [];
  let paragraph = [];
  let list = null;
  let quote = [];
  let code = [];
  let inCode = false;

  const flushParagraph = () => {
    if (!paragraph.length) return;
    html.push(`<p>${renderMarkdownInline(paragraph.join(" "))}</p>`);
    paragraph = [];
  };
  const flushList = () => {
    if (!list) return;
    html.push(`<${list.type}>${list.items.map((item) => `<li>${renderMarkdownInline(item)}</li>`).join("")}</${list.type}>`);
    list = null;
  };
  const flushQuote = () => {
    if (!quote.length) return;
    html.push(`<blockquote>${quote.map((item) => `<p>${renderMarkdownInline(item)}</p>`).join("")}</blockquote>`);
    quote = [];
  };
  const closeOpenBlocks = () => {
    flushParagraph();
    flushList();
    flushQuote();
  };

  lines.forEach((rawLine) => {
    const line = rawLine.trimEnd();
    const trimmed = line.trim();

    if (trimmed.startsWith("```")) {
      if (inCode) {
        html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
        code = [];
        inCode = false;
      } else {
        closeOpenBlocks();
        inCode = true;
      }
      return;
    }

    if (inCode) {
      code.push(rawLine);
      return;
    }

    if (!trimmed) {
      closeOpenBlocks();
      return;
    }

    const heading = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      closeOpenBlocks();
      const level = Math.min(heading[1].length + 2, 5);
      html.push(`<h${level}>${renderMarkdownInline(heading[2])}</h${level}>`);
      return;
    }

    const unordered = trimmed.match(/^[-*]\s+(.+)$/);
    if (unordered) {
      flushParagraph();
      flushQuote();
      if (!list || list.type !== "ul") {
        flushList();
        list = { type: "ul", items: [] };
      }
      list.items.push(unordered[1]);
      return;
    }

    const ordered = trimmed.match(/^\d+\.\s+(.+)$/);
    if (ordered) {
      flushParagraph();
      flushQuote();
      if (!list || list.type !== "ol") {
        flushList();
        list = { type: "ol", items: [] };
      }
      list.items.push(ordered[1]);
      return;
    }

    const quoted = trimmed.match(/^>\s?(.+)$/);
    if (quoted) {
      flushParagraph();
      flushList();
      quote.push(quoted[1]);
      return;
    }

    flushList();
    flushQuote();
    paragraph.push(trimmed);
  });

  if (inCode) html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
  closeOpenBlocks();

  return `<div class="brain-answer markdown-body">${html.join("")}</div>`;
}

async function apiAsk(question) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 240000);
  try {
    const response = await fetch(new URL(`${API_BASE}/ask`, window.location.origin), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      cache: "no-store",
      signal: controller.signal
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch (_) {
      payload = {};
    }
    if (!response.ok || payload.ok === false) {
      const err = new Error(apiErrorMessage(response.status, payload.error || `HTTP ${response.status}`));
      err.status = response.status;
      throw err;
    }
    return payload.answer || "";
  } catch (error) {
    if (error.name === "AbortError") {
      const err = new Error(apiErrorMessage(504));
      err.status = 504;
      throw err;
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

function listFromPayload(payload, keys) {
  for (const key of keys) {
    const value = payload?.[key];
    if (Array.isArray(value)) return value;
    if (value && Array.isArray(value.items)) return value.items;
    if (value && Array.isArray(value.results)) return value.results;
  }
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.data)) return payload.data;
  if (Array.isArray(payload?.items)) return payload.items;
  if (Array.isArray(payload?.results)) return payload.results;
  return [];
}

function normalizeFeedSignal(item, index) {
  return normalizeSignal({
    title: item.word || item.title || item.token || item.ticker || item.name || `SIGNAL-${index + 1}`,
    type: item.type || item.category || item.kind || "WORLD",
    category: item.category || item.type,
    mention_accounts: item.mention_accounts || item.accounts || item.accounts_n || item.count,
    observed_at: item.observed_at || item.updated_at || item.time,
    area: item.area || item.region,
    summary: item.summary || item.desc || item.description || item.why,
    why: item.why || item.reason || item.summary,
    confidence: item.confidence,
    events: item.events || item.observed_events || [],
    posts: item.posts || item.top || item.tweets || [],
    history: item.history || item.patterns || [],
    trace: item.trace || {
      why: item.why || item.reason,
      top: item.top || item.posts || [],
      causal: item.causal || item.association_path || [],
      confidence: item.confidence
    }
  }, index);
}

function normalizeFeedLaunch(item) {
  return {
    ticker: item.ticker || item.token || item.symbol || item.title || item.name || "UNKNOWN",
    name: item.name || item.title || item.token || item.ticker || "UNKNOWN",
    mint: item.mint || item.ca || item.address || item.contract || "",
    mcap: item.mcap || item.market_cap || item.marketCap || item.liquidity || 0,
    peak_mcap: item.peak_mcap || item.peak_market_cap || item.ath_mcap || item.mcap || 0,
    status: item.status || item.verdict || item.call || "tracked",
    outcome: item.outcome || item.risk || null,
    color: item.color || "#48eca0",
    gate: item.gate || item.reason || item.summary || "",
    kol: item.kol || item.kols || item.accounts || [],
    ai_agent: Boolean(item.ai_agent),
    reply_count: item.reply_count || item.replies || item.mentions || 0,
    first_seen: item.first_seen || item.created_at || item.observed_at || item.updated_at || "",
    died_at: item.died_at || null,
    link: item.link || item.url || "",
    spark: item.spark || item.series || []
  };
}

function inferType(signal) {
  const accounts = (signal.trace?.top || []).map((post) => String(post.account || "").toLowerCase());
  if (signal.type === "WORLD" || signal.type === "MACRO") return "WORLD";
  if (accounts.some((name) => ["cobie", "theunipcs", "ansem", "blknoiz06"].includes(name))) return "MEME KOL";
  return "CRYPTO TWITTER";
}

function normalizeSignal(signal, index) {
  const top = signal.trace?.top || [];
  const causal = signal.trace?.causal || [];
  const accounts = signal.mention_accounts || signal.accounts || signal.trace?.accounts_n || new Set(top.map((post) => post.account)).size || 1;
  return {
    word: signal.word || signal.title || `SIGNAL-${index + 1}`,
    type: String(signal.category || signal.type || inferType(signal)).replaceAll("_", " "),
    accounts,
    area: Array.isArray(signal.area) ? signal.area.join(" / ") : (signal.area || (signal.type === "WORLD" ? "GLOBAL" : "CT")),
    observed: signal.observed || signal.observed_at || "latest",
    summary: signal.summary || signal.trace?.why || "LLM Wiki observed this signal.",
    events: (signal.events || []).map((event) => [
      event.time || event.date || "NOW",
      event.type || signal.type || "EVENT",
      event.title || event.text || "observed event",
      event.area || "GLOBAL",
      event.source || event.wiki || ""
    ]).concat(causal.slice(0, 3).map((item, i) => [`PATH ${i + 1}`, "CONCEPT", item, "WIKI", item])),
    posts: (signal.posts || top || []).map((post) => [
      `@${post.account || "unknown"}`,
      post.text || post.title || "",
      post.likes ? `${Number(post.likes).toLocaleString()} likes` : (post.source || "source"),
      post.source || post.wiki || ""
    ]),
    history: (signal.history || []).map((entry) => [
      entry.date || entry.year || "-",
      entry.title || entry.name || "past pattern",
      entry.summary || entry.similarity || "",
      entry.wiki || entry.source || ""
    ]),
    why: signal.why || signal.trace?.why || "Inference reason is not recorded yet.",
    confidence: Number(signal.confidence ?? signal.trace?.confidence ?? 0.55)
  };
}

function money(value) {
  const amount = Number(value || 0);
  if (amount >= 1_000_000) return `$${(amount / 1_000_000).toFixed(2)}M`;
  if (amount >= 1_000) return `$${Math.round(amount / 1_000)}K`;
  return `$${amount.toLocaleString()}`;
}

function renderAll() {
  renderMetrics();
  renderTickers();
  renderSignals();
  renderLaunches();
  renderIntel();
  renderBrainCalls();
}

function renderMetrics() {
  $("#signal-count").textContent = state.signals.length;
  $("#metric-mints").textContent = Number(state.baseRate?.mints_seen || 0).toLocaleString();
  $("#metric-passed").textContent = Number(state.baseRate?.gate_passed || 0).toLocaleString();
  $("#metric-rate").textContent = `${Number(state.baseRate?.pass_rate_pct || 0).toFixed(2)}%`;
}

function renderTickers() {
  const hotSignals = [...state.signals]
    .sort((a, b) => (b.accounts || 0) - (a.accounts || 0))
    .slice(0, 14);
  const hotMarkup = hotSignals.map((signal) => `
    <button class="hotword-link" type="button" data-word="${escapeHtml(signal.word)}">
      <span>▲</span>${escapeHtml(signal.word)}
      <small>${Number(signal.accounts || 0).toLocaleString()} accounts / ${escapeHtml(signal.type)}</small>
    </button>
  `).join("");
  $("#hot-ticker").innerHTML = `<span>${hotMarkup}${hotMarkup}</span>`;

  const posts = state.signals
    .flatMap((signal) => signal.posts.map((post) => `${post[0]}: ${post[1]}`))
    .slice(0, 10)
    .join("     ");
  const wire = posts || "No KOL / figure wire yet.";
  $("#post-ticker").innerHTML = `<span>${escapeHtml(wire)}     ${escapeHtml(wire)}</span>`;
}

function signalAnalysis(signal) {
  const events = (signal.events || []).slice(0, 3);
  const posts = (signal.posts || []).slice(0, 3);
  return `
    <p><b>${escapeHtml(signal.word)}</b> selected from HOT WORD wire.</p>
    <p>${escapeHtml(signal.summary)}</p>
    <p>Observed by <b>${Number(signal.accounts || 0).toLocaleString()}</b> independent accounts. Area: ${escapeHtml(signal.area)}. Type: ${escapeHtml(signal.type)}.</p>
    ${events.length ? `<p>Observed events:</p><ul>${events.map((event) => `<li>${escapeHtml(event[2] || "event")} <span class="cite">[[${escapeHtml(event[4] || signal.word)}]]</span></li>`).join("")}</ul>` : ""}
    ${posts.length ? `<p>Observed posts:</p><ul>${posts.map((post) => `<li>${escapeHtml(post[0])}: ${escapeHtml(post[1])}</li>`).join("")}</ul>` : ""}
    <p>LLM inference: ${escapeHtml(signal.why)}</p>
    <p class="unknown">confidence: ${Math.round(Number(signal.confidence <= 1 ? signal.confidence * 100 : signal.confidence) || 0)}%</p>
  `;
}

function openSignalAnalysis(word) {
  const signal = state.signals.find((item) => item.word === word);
  if (!signal) return;
  const now = Date.now();
  if (state.lastHotwordClick?.word === word && now - state.lastHotwordClick.time < 450) return;
  state.lastHotwordClick = { word, time: now };
  state.selected = signal;
  renderSignals();
  renderIntel();
  addMessage("brain", signalAnalysis(signal));
}
function renderSignals() {
  const visible = state.category === "ALL"
    ? state.signals
    : state.signals.filter((signal) => signal.type === state.category);

  $("#signal-list").innerHTML = visible.map((signal) => `
    <button class="signal-item ${signal.word === state.selected?.word ? "active" : ""}" data-word="${escapeHtml(signal.word)}">
      <span class="score">${signal.accounts} acct</span>
      <b>${escapeHtml(signal.word)}</b>
      <small>${escapeHtml(signal.type)} / ${escapeHtml(signal.area)} / ${escapeHtml(String(signal.observed).slice(0, 16))}</small>
    </button>
  `).join("") || `<p class="muted">No signals in this category.</p>`;

  document.querySelectorAll(".signal-item").forEach((button) => {
    button.onclick = () => {
      state.selected = state.signals.find((signal) => signal.word === button.dataset.word) || state.selected;
      renderSignals();
      renderIntel();
    };
  });
}

function renderLaunches() {
  $("#launch-list").innerHTML = state.launches.length ? state.launches.map((launch) => `
    <button class="launch-item">
      <span class="score">${money(launch.mcap)}</span>
      <b>${escapeHtml(launch.ticker || launch.name || "UNKNOWN")}</b>
      <small>${escapeHtml(launch.status || launch.outcome || "tracked")} / peak ${money(launch.peak_mcap)}</small>
    </button>
  `).join("") : `<p class="muted">Launch lifecycle data is not available yet.</p>`;
}

function callType(launch) {
  const mcap = Number(launch.mcap || 0);
  const peak = Number(launch.peak_mcap || 0);
  const replies = Number(launch.reply_count || 0);
  const kolCount = Array.isArray(launch.kol) ? launch.kol.length : 0;
  if (mcap >= 1_000_000 || peak >= 2_500_000 || replies >= 1200 || kolCount >= 2) return "HIGH TIRE DETECT";
  return "SMART DETECT";
}

function callScore(launch) {
  const mcap = Number(launch.mcap || 0);
  const peak = Number(launch.peak_mcap || 0);
  const replies = Number(launch.reply_count || 0);
  const kolCount = Array.isArray(launch.kol) ? launch.kol.length : 0;
  return Math.round(
    Math.min(42, Math.log10(Math.max(mcap, 1)) * 4)
    + Math.min(26, Math.log10(Math.max(peak, 1)) * 3)
    + Math.min(22, replies / 90)
    + Math.min(10, kolCount * 5)
  );
}

function normalizeCalls() {
  return (state.launches || []).map((launch, index) => ({
    id: launch.mint || launch.link || `${launch.ticker || "CALL"}-${index}`,
    type: callType(launch),
    score: callScore(launch),
    ...launch
  })).sort((a, b) => b.score - a.score);
}

function renderBrainCalls() {
  const feed = $("#call-feed");
  if (!feed) return;
  const calls = normalizeCalls();
  if (!state.selectedCall && calls.length) state.selectedCall = calls[0].id;
  const visible = state.callFilter === "ALL" ? calls : calls.filter((call) => call.type === state.callFilter);
  const selected = calls.find((call) => call.id === state.selectedCall) || visible[0] || calls[0] || null;
  if (selected) state.selectedCall = selected.id;

  $("#call-total").textContent = calls.length;
  $("#smart-total").textContent = calls.filter((call) => call.type === "SMART DETECT").length;
  $("#tire-total").textContent = calls.filter((call) => call.type === "HIGH TIRE DETECT").length;

  feed.innerHTML = visible.length ? visible.map((call) => {
    const isHigh = call.type === "HIGH TIRE DETECT";
    return `
      <button class="call-card ${isHigh ? "high" : "smart"} ${call.id === state.selectedCall ? "active" : ""}" type="button" data-call-id="${escapeHtml(call.id)}">
        <span class="call-badge ${isHigh ? "high" : "smart"}">${escapeHtml(call.type)}</span>
        <h3>${escapeHtml(call.ticker || call.name || "UNKNOWN")}</h3>
        <p>${escapeHtml(call.name || call.status || "observed launch candidate")}</p>
        <div class="call-meta">
          <span>score ${call.score}</span>
          <span>${money(call.mcap)}</span>
          <span>${escapeHtml(call.gate || "gate n/a")}</span>
        </div>
      </button>
    `;
  }).join("") : `<p class="muted">No calls in this detect lane.</p>`;

  document.querySelectorAll(".call-card").forEach((button) => {
    button.onclick = () => {
      state.selectedCall = button.dataset.callId;
      renderBrainCalls();
    };
  });

  renderCallDetail(selected);
}

function renderCallDetail(call) {
  const detail = $("#call-detail");
  if (!detail) return;
  if (!call) {
    detail.innerHTML = `
      <span class="call-badge smart">WAITING</span>
      <h2>No call feed</h2>
      <p>Brain CALLL is waiting for <span class="cite">[[ui-data.json live[]]]</span>.</p>
    `;
    return;
  }
  const isHigh = call.type === "HIGH TIRE DETECT";
  const spark = Array.isArray(call.spark) && call.spark.length
    ? `${money(call.spark[0])} → ${money(call.spark[call.spark.length - 1])}`
    : "not recorded";
  detail.innerHTML = `
    <span class="call-badge ${isHigh ? "high" : "smart"}">${escapeHtml(call.type)}</span>
    <h2>${escapeHtml(call.ticker || call.name || "UNKNOWN")}</h2>
    <p>${escapeHtml(call.name || "observed launch candidate")}</p>
    <p>CALL reason: ${escapeHtml(call.gate || "launch feed observed; detailed reason not recorded yet.")}</p>
    <div class="call-detail-grid">
      <span>mcap<b>${money(call.mcap)}</b></span>
      <span>peak<b>${money(call.peak_mcap)}</b></span>
      <span>reply count<b>${Number(call.reply_count || 0).toLocaleString()}</b></span>
      <span>score<b>${call.score}</b></span>
      <span>KOL<b>${escapeHtml((call.kol || []).join(", ") || "not recorded")}</b></span>
      <span>first seen<b>${escapeHtml(call.first_seen || "not recorded")}</b></span>
      <span>spark<b>${escapeHtml(spark)}</b></span>
      <span>CA<b>${escapeHtml(call.mint || "not recorded")}</b></span>
    </div>
    <p><span class="cite">[[${escapeHtml(call.link || "ui-data.json live[]")}]]</span></p>
  `;
}

function verdictClass(value) {
  const text = String(value || "").toLowerCase();
  if (text.includes("ape") || text.includes("buy") || text.includes("call")) return "ape";
  if (text.includes("avoid") || text.includes("skip") || text.includes("danger")) return "avoid";
  return "watch";
}

function renderScoreResult(payload, token) {
  const box = $("#scan-result");
  if (!box) return;
  const data = (payload?.score && typeof payload.score === "object")
    ? payload.score
    : (payload?.result && typeof payload.result === "object")
      ? payload.result
      : (payload?.data && typeof payload.data === "object")
        ? payload.data
        : (payload || {});
  const verdict = data.verdict || data.call || data.label || data.decision || data.status || "WATCH";
  const score = data.score ?? data.total_score ?? data.confidence ?? data.rating ?? "--";
  const confidence = data.confidence ?? data.probability ?? data.conf ?? null;
  const reason = data.reason || data.why || data.summary || data.explanation || "Backend returned a score response.";
  const risks = listFromPayload(data, ["risks", "risk", "warnings"]).slice(0, 4);
  const evidence = listFromPayload(data, ["evidence", "sources", "links", "wiki"]).slice(0, 5);
  const klass = verdictClass(verdict);
  box.className = `scan-result ${klass}`;
  box.innerHTML = `
    <span class="call-badge ${klass === "avoid" ? "high" : "smart"}">SCAN</span>
    <h2>${escapeHtml(String(verdict).toUpperCase())}</h2>
    <p><b>${escapeHtml(token)}</b> / score: ${escapeHtml(score)}${confidence !== null ? ` / confidence: ${escapeHtml(confidence)}` : ""}</p>
    <p>${escapeHtml(reason)}</p>
    ${risks.length ? `<p class="unknown">Risk:</p><ul>${risks.map((risk) => `<li>${escapeHtml(typeof risk === "string" ? risk : JSON.stringify(risk))}</li>`).join("")}</ul>` : ""}
    ${evidence.length ? `<p>Evidence:</p><ul>${evidence.map((item) => `<li><span class="cite">[[${escapeHtml(typeof item === "string" ? item : (item.path || item.title || item.url || JSON.stringify(item)))}]]</span></li>`).join("")}</ul>` : ""}
  `;
}

function renderScoreFallback(token) {
  const launch = findLaunchByMint(token) || state.launches.find((item) => {
    const needle = token.toLowerCase();
    return String(item.ticker || "").toLowerCase() === needle
      || String(item.name || "").toLowerCase() === needle
      || String(item.ticker || "").toLowerCase() === `$${needle.replace(/^\$/, "")}`;
  });
  if (!launch) {
    renderScoreResult({
      verdict: "UNRECORDED",
      score: "--",
      reason: "Backend /api/score is offline and fallback live[] has no matching token/CA. No inferred call is made.",
      risks: ["No backend score", "No local launch match"]
    }, token);
    return;
  }
  renderScoreResult({
    verdict: callType(launch) === "HIGH TIRE DETECT" ? "WATCH" : "SMART WATCH",
    score: callScore(launch),
    confidence: "fallback",
    reason: launch.gate || "Fallback result from local ui-data.json live[].",
    evidence: [launch.link || "ui-data.json live[]"]
  }, token);
}

async function runScan(token) {
  const value = String(token || "").trim();
  if (!value) return;
  $("#scan-status").textContent = "backend: scoring...";
  try {
    const result = await apiGet("/score", { token: value });
    state.backendLive = true;
    $("#scan-status").textContent = "backend: /api/score live";
    renderScoreResult(result, value);
  } catch (error) {
    state.backendLive = false;
    $("#scan-status").textContent = `backend: offline / fallback (${error.message || "unavailable"})`;
    renderScoreFallback(value);
  }
}

async function answerFromBackend(question) {
  try {
    const answerText = await apiAsk(question);
    state.backendLive = true;
    return renderAskMarkdown(answerText);
  } catch (error) {
    state.backendLive = false;
    const message = apiErrorMessage(error.status, error.message || "backend unavailable");
    return `<p class="unknown">ASK FAILED: ${escapeHtml(message)}</p>`;
  }
}

function renderWikiResults(payload, query) {
  const box = $("#wiki-results");
  const items = listFromPayload(payload, ["results", "items", "pages", "matches"]).slice(0, 20);
  if (!items.length) {
    box.innerHTML = `<article><b>NO MATCH</b><p class="unknown">No backend wiki result for "${escapeHtml(query)}".</p></article>`;
    return;
  }
  box.innerHTML = items.map((item) => {
    const title = typeof item === "string" ? item : (item.title || item.path || item.name || "Untitled");
    const path = typeof item === "string" ? item : (item.path || item.url || item.wiki || title);
    const text = typeof item === "string" ? "" : (item.snippet || item.summary || item.text || item.desc || "");
    return `
      <article>
        <b>${escapeHtml(title)}</b>
        <p>${escapeHtml(text || path)}</p>
        <p><span class="cite">[[${escapeHtml(path)}]]</span></p>
      </article>
    `;
  }).join("");
}

async function runWikiSearch(query) {
  const value = String(query || "").trim();
  if (!value) return;
  $("#wiki-search-status").textContent = "backend: searching...";
  try {
    const payload = await apiGet("/search", { q: value }, { timeoutMs: 30000 });
    $("#wiki-search-status").textContent = "backend: /api/search live";
    renderWikiResults(payload, value);
  } catch (error) {
    $("#wiki-search-status").textContent = `backend: search offline (${error.message || "unavailable"})`;
    $("#wiki-results").innerHTML = `
      <article>
        <b>SEARCH OFFLINE</b>
        <p class="unknown">Backend /api/search is not available. Start <span class="cite">[[brain/ui_server.py]]</span> or pull latest main.</p>
      </article>
    `;
  }
}

function renderIntel() {
  const signal = state.selected;
  if (!signal) return;
  $("#intel-body").innerHTML = `
    <div class="intel-section">
      <span class="fact-tag">OBSERVED</span>
      <b>${escapeHtml(signal.word)}</b>
      <small>${escapeHtml(signal.summary)}</small>
    </div>
    <div class="intel-section">
      <b>Observed events</b>
      ${rows(signal.events, "Not recorded")}
    </div>
    <div class="intel-section">
      <b>Observed posts</b>
      ${rows(signal.posts, "Not recorded")}
    </div>
    <div class="intel-section">
      <span class="infer-tag">LLM INFERENCE</span>
      <small>${escapeHtml(signal.why)}</small>
      <small>confidence: ${Math.round(Number(signal.confidence <= 1 ? signal.confidence * 100 : signal.confidence) || 0)}%</small>
    </div>
  `;
}

function rows(items, empty) {
  if (!items?.length) return `<small class="unknown">${empty}</small>`;
  return items.slice(0, 5).map((row) => `<small>繝ｻ${row.map((cell) => escapeHtml(String(cell || ""))).join(" / ")}</small>`).join("");
}

function flattenSignal(signal) {
  return [
    signal.word,
    signal.type,
    signal.area,
    signal.summary,
    signal.why,
    ...(signal.events || []).flat(),
    ...(signal.posts || []).flat(),
    ...(signal.history || []).flat()
  ].filter(Boolean).join(" ").toLowerCase();
}

function queryTerms(question) {
  const lowered = question.toLowerCase();
  const tickers = question.match(/\$[a-z0-9_]+/gi) || [];
  const commands = new Set([
    "check", "wiki", "hot", "word", "meme", "trend", "source", "origin", "start",
    "why", "kol", "figure", "post", "posts", "what", "this", "that", "from",
    "about", "tell", "show", "今", "これ", "この", "起点", "理由", "関連", "発言"
  ]);
  const words = lowered
    .replace(/[^\p{L}\p{N}$]+/gu, " ")
    .split(/\s+/)
    .filter((term) => term.length >= 2 && !commands.has(term));
  return [...new Set([...tickers.map((term) => term.toLowerCase()), ...words])];
}

function extractMint(question) {
  const commandMint = question.match(/^\/check\s+([^\s]+)/i)?.[1];
  if (commandMint) return commandMint.trim();
  return question.match(/[1-9A-HJ-NP-Za-km-z]{32,48}/)?.[0] || null;
}

function findLaunchByMint(mint) {
  if (!mint) return null;
  const needle = mint.toLowerCase();
  return state.launches.find((launch) => {
    return String(launch.mint || "").toLowerCase() === needle
      || String(launch.link || "").toLowerCase().includes(needle);
  }) || null;
}

function scoreSignal(signal, terms) {
  const haystack = flattenSignal(signal);
  let score = 0;
  for (const term of terms) {
    if (!term) continue;
    if (String(signal.word || "").toLowerCase() === term) score += 80;
    if (String(signal.word || "").toLowerCase().includes(term)) score += 35;
    if (haystack.includes(term)) score += 10;
  }
  return score + Math.min(Number(signal.accounts || 0), 20) / 10;
}

function findSignals(question) {
  const terms = queryTerms(question);
  if (!terms.length) return [];
  return [...state.signals]
    .map((signal) => ({ signal, score: scoreSignal(signal, terms) }))
    .filter((item) => item.score >= 10)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map((item) => item.signal);
}

function launchAnswer(question) {
  const mint = extractMint(question);
  if (!mint) return null;
  const launch = findLaunchByMint(mint);
  if (!launch) {
    return `
      <p><b>CA check</b>: ${escapeHtml(mint)}</p>
      <p class="unknown">未収録。現在の <span class="cite">[[ui-data.json live[] / signals[]]]</span> には、このCAに一致するtoken recordがありません。</p>
      <p>別のHOT WORDへ推測で紐づけません。CA一致がない場合は、根拠なしの関連付けを行いません。</p>
    `;
  }
  const spark = Array.isArray(launch.spark) && launch.spark.length
    ? `${money(launch.spark[0])} → ${money(launch.spark[launch.spark.length - 1])}`
    : "not recorded";
  return `
    <p><b>CA check</b>: ${escapeHtml(mint)}</p>
    <ul>
      <li>token: <b>${escapeHtml(launch.ticker || launch.name || "UNKNOWN")}</b></li>
      <li>name: ${escapeHtml(launch.name || "not recorded")}</li>
      <li>mcap / peak: ${money(launch.mcap)} / ${money(launch.peak_mcap)}</li>
      <li>gate: ${escapeHtml(launch.gate || "not recorded")}</li>
      <li>KOL: ${escapeHtml((launch.kol || []).join(", ") || "not recorded")}</li>
      <li>first seen: ${escapeHtml(launch.first_seen || "not recorded")}</li>
      <li>spark: ${escapeHtml(spark)}</li>
    </ul>
    <p><span class="cite">[[${escapeHtml(launch.link || "ui-data.json live[]")}]]</span></p>
  `;
}

function signalListAnswer(signals, label) {
  if (!signals.length) {
    return `
      <p class="unknown">未収録。現在のUI接続データには、この質問に一致する観測事実がありません。</p>
      <p>根拠なしに現在選択中のHOT WORDへ接続しません。Wiki側の次回生成、またはsource追加が必要です。</p>
    `;
  }
  return `
    <p>${escapeHtml(label)}</p>
    <ul>${signals.map((signal) => `
      <li>
        <b>${escapeHtml(signal.word)}</b> — ${Number(signal.accounts || 0).toLocaleString()} accounts / ${escapeHtml(signal.type)}
        <span class="cite">[[${escapeHtml(signal.word)}]]</span>
      </li>
    `).join("")}</ul>
    <p class="unknown">指標: いいね数ではなく、独立言及アカウント数を優先。</p>
  `;
}

function answer(question) {
  const q = question.toLowerCase();
  const hot = [...state.signals].sort((a, b) => (b.accounts || 0) - (a.accounts || 0)).slice(0, 5);
  const checkedLaunch = launchAnswer(question);
  if (checkedLaunch) return checkedLaunch;

  if (q.includes("hot") || q.includes("meme") || q.includes("trend") || q.includes("word")) {
    return signalListAnswer(hot, "Trench Brain currently sees these as the strongest meme-word candidates.");
  }

  const matches = findSignals(question);

  if (q.includes("why") || q.includes("source") || q.includes("origin") || q.includes("start")) {
    if (!matches.length) return signalListAnswer([], "");
    const target = matches[0];
    return `
      <p>Observed starting points for <b>${escapeHtml(target.word)}</b>:</p>
      <ul>${(target.events || []).slice(0, 4).map((event) => `<li>${escapeHtml(event[2] || "event")} <span class="cite">[[${escapeHtml(event[4] || target.word)}]]</span></li>`).join("") || "<li>Not recorded</li>"}</ul>
      <p>LLM inference: ${escapeHtml(target.why)}</p>
      <p class="unknown">観測事実と推論は分離。未収録部分は補完しません。</p>
    `;
  }

  if (q.includes("kol") || q.includes("figure") || q.includes("post") || q.includes("posts") || q.includes("x発言") || q.includes("twitter") || q.includes("tweet")) {
    const source = matches.length ? matches : state.signals;
    const posts = source.flatMap((signal) => signal.posts.map((post) => ({ signal, post }))).slice(0, 6);
    return `
      <p>Visible KOL / figure wire:</p>
      <ul>${posts.map(({ signal, post }) => `<li>${escapeHtml(post[0])}: ${escapeHtml(post[1])} <span class="cite">[[${escapeHtml(signal.word)}]]</span></li>`).join("") || "<li>Not recorded</li>"}</ul>
    `;
  }

  if (matches.length) {
    return `
      <p>Wiki-connected matches:</p>
      ${matches.slice(0, 3).map((signal) => `
        <p><b>${escapeHtml(signal.word)}</b> — ${escapeHtml(signal.summary)}</p>
        <p>Observed: ${Number(signal.accounts || 0).toLocaleString()} independent accounts / ${escapeHtml(signal.type)} / ${escapeHtml(signal.area)}</p>
        <p>LLM inference: ${escapeHtml(signal.why)}</p>
        <p><span class="cite">[[${escapeHtml(signal.word)}]]</span></p>
      `).join("")}
    `;
  }

  return signalListAnswer([], "");
}
function addMessage(role, html) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  article.innerHTML = `<b>${role === "user" ? "You" : "Trench Brain"}</b>${html}`;
  $("#chat-log").appendChild(article);
  $("#chat-log").scrollTop = $("#chat-log").scrollHeight;
}

async function connectData() {
  let lastError;
  try {
    const feed = await apiGet("/feed");
    const apiSignals = listFromPayload(feed, ["hot", "signals", "words", "themes"]);
    const apiLaunches = listFromPayload(feed, ["launches", "live", "calls"]);
    if (apiSignals.length || apiLaunches.length) {
      state.signals = (apiSignals.length ? apiSignals : fallbackSignals).map(normalizeFeedSignal);
      state.launches = apiLaunches.map(normalizeFeedLaunch);
      state.baseRate = feed.base_rate || feed.baseRate || null;
      state.selected = state.signals[0] || fallbackSignals[0];
      state.backendLive = true;
      $(".status-light").classList.add("live");
      $("#connection-label").textContent = "API LIVE";
      $("#data-source").textContent = "source: Trench-Brain backend /api/feed";
      $("#generated-at").textContent = feed.generated_at || feed.updated_at || "backend live";
      $("#scan-status").textContent = "backend: /api/score ready";
      renderAll();
      return;
    }
  } catch (error) {
    lastError = error;
    state.backendLive = false;
    $("#scan-status").textContent = `backend: offline (${error.message || "unavailable"})`;
  }

  for (const url of DATA_URLS) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 3000);
      const separator = url.includes("?") ? "&" : "?";
      const response = await fetch(`${url}${separator}t=${Date.now()}`, { cache: "no-store", signal: controller.signal });
      clearTimeout(timeout);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      const sourceSignals = payload.words?.length ? payload.words : payload.signals;
      state.signals = (sourceSignals || []).map(normalizeSignal);
      state.launches = payload.live || [];
      state.baseRate = payload.base_rate || null;
      state.selected = state.signals[0] || fallbackSignals[0];
      state.backendLive = false;
      $(".status-light").classList.add("live");
      $("#connection-label").textContent = "LIVE";
      $("#data-source").textContent = url.startsWith("http") ? "source: GitHub MAIN ui-data.json" : "source: local ui-data.json";
      $("#generated-at").textContent = payload.generated_at || "generated_at unknown";
      $("#scan-status").textContent = lastError ? `backend: offline / fallback active` : "backend: fallback active";
      renderAll();
      return;
    } catch (error) {
      lastError = error;
    }
  }
  $("#connection-label").textContent = "FALLBACK";
  $("#generated-at").textContent = lastError?.message || "ui-data unavailable";
  $("#scan-status").textContent = "backend: unavailable";
  renderAll();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

$("#category-filter").onchange = (event) => {
  state.category = event.target.value;
  renderSignals();
};

$("#hot-ticker").onclick = (event) => {
  const button = event.target.closest(".hotword-link");
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  openSignalAnalysis(button.dataset.word);
};

document.querySelectorAll(".tool-tab").forEach((button) => {
  button.onclick = () => {
    state.activeTool = button.dataset.tool;
    document.querySelectorAll(".tool-tab").forEach((tab) => tab.classList.toggle("active", tab === button));
    document.querySelectorAll(".tool-panel").forEach((panel) => {
      panel.classList.toggle("active", panel.dataset.toolPanel === state.activeTool);
    });
    renderBrainCalls();
  };
});

document.querySelectorAll(".call-filter").forEach((button) => {
  button.onclick = () => {
    state.callFilter = button.dataset.callFilter;
    document.querySelectorAll(".call-filter").forEach((filter) => filter.classList.toggle("active", filter === button));
    const calls = normalizeCalls();
    const visible = state.callFilter === "ALL" ? calls : calls.filter((call) => call.type === state.callFilter);
    state.selectedCall = visible[0]?.id || calls[0]?.id || null;
    renderBrainCalls();
  };
});

$("#scan-form").onsubmit = (event) => {
  event.preventDefault();
  runScan($("#scan-token").value);
};

$("#wiki-search-form").onsubmit = (event) => {
  event.preventDefault();
  runWikiSearch($("#wiki-query").value);
};

$("#question").addEventListener("keydown", (event) => {
  if (event.key !== "Enter" || event.shiftKey || event.isComposing) return;
  event.preventDefault();
  $("#chat-form").requestSubmit();
});

$("#chat-form").onsubmit = async (event) => {
  event.preventDefault();
  const input = $("#question");
  const submitButton = $("#chat-form button[type='submit']");
  const text = input.value.trim();
  if (!text) return;
  addMessage("user", `<p>${escapeHtml(text)}</p>`);
  if ($("#queue-consent").checked) {
    state.queue.unshift({
      kind: $("#question-kind").value,
      text,
      context: state.selected?.word,
      time: new Date().toISOString(),
      status: "pending_review"
    });
    localStorage.setItem("trenchBrainLearningQueue", JSON.stringify(state.queue));
  }
  input.value = "";
  input.disabled = true;
  if (submitButton) submitButton.disabled = true;
  addMessage("brain", `<p class="unknown">全wiki横断中…最大数分かかります。/api/ask is thinking.</p>`);
  const pending = $("#chat-log article:last-child");
  try {
    const html = await answerFromBackend(text);
    if (pending) {
      pending.innerHTML = `<b>Trench Brain</b>${html}`;
      $("#chat-log").scrollTop = $("#chat-log").scrollHeight;
    } else {
      addMessage("brain", html);
    }
  } finally {
    input.disabled = false;
    if (submitButton) submitButton.disabled = false;
    input.focus();
  }
};

$("#clear-chat").onclick = () => {
  $("#chat-log").innerHTML = `<article class="message brain"><b>Trench Brain</b><p>Connection request from Trench &gt;&gt;&gt;&gt; Authorized. Knowledge channel is open.</p></article>`;
};

setInterval(() => {
  $("#clock").textContent = `${new Intl.DateTimeFormat("ja-JP", { timeZone: "Asia/Tokyo", hour: "2-digit", minute: "2-digit", second: "2-digit" }).format(new Date())} JST`;
}, 1000);

renderAll();
connectData();

const loginButton = document.querySelector("#login-button");
if (loginButton) {
  loginButton.addEventListener("click", () => {
    document.body.classList.add("login-entering");
    window.setTimeout(() => {
      document.body.classList.add("logged-in");
      document.body.classList.remove("login-entering");
      document.querySelector("#question")?.focus();
    }, 1350);
  });
}
