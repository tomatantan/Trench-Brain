const DATA_URLS = ["../ui-data.json", "https://raw.githubusercontent.com/tomatantan/Trench-Brain/main/wiki/ui-data.json"];

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
  queue: JSON.parse(localStorage.getItem("trenchBrainLearningQueue") || "[]")
};

const $ = (selector) => document.querySelector(selector);

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

function answer(question) {
  const q = question.toLowerCase();
  const hot = [...state.signals].sort((a, b) => (b.accounts || 0) - (a.accounts || 0)).slice(0, 5);

  if (q.includes("hot") || q.includes("meme") || q.includes("trend") || q.includes("word")) {
    // 「meme」なら MEMEカテゴリだけ(majors=MACRO/WORLD除外)。それ以外は全signal。
    const wantMeme = q.includes("meme");
    const pool = wantMeme ? state.signals.filter((s) => String(s.type || "").toUpperCase() === "MEME") : state.signals;
    const top = [...pool].sort((a, b) => (b.accounts || 0) - (a.accounts || 0)).slice(0, 5);
    const head = wantMeme
      ? "MEMEカテゴリの候補（majors除外・独立言及アカ数順）"
      : "strongest signals by independent account mentions";
    return `
      <p>${head}</p>
      <ul>${top.map((signal) => `<li><b>${escapeHtml(signal.word)}</b> — ${Number(signal.accounts || 0).toLocaleString()} accounts <span class="cite">[[${escapeHtml(signal.word)}]]</span></li>`).join("") || "<li class='unknown'>該当カテゴリのsignalなし</li>"}</ul>
      <p class="unknown">簡易ダッシュボード応答（独立言及アカ数優先）。深い答えは実脳=/api/ask。</p>
    `;
  }

  if (q.includes("why") || q.includes("source") || q.includes("origin") || q.includes("start")) {
    return `
      <p>Observed starting points for <b>${escapeHtml(state.selected.word)}</b>:</p>
      <ul>${(state.selected.events || []).slice(0, 4).map((event) => `<li>${escapeHtml(event[2] || "event")} <span class="cite">[[${escapeHtml(event[4] || state.selected.word)}]]</span></li>`).join("") || "<li>Not recorded</li>"}</ul>
      <p>Inference: ${escapeHtml(state.selected.why)}</p>
    `;
  }

  if (q.includes("kol") || q.includes("figure") || q.includes("post") || q.includes("x")) {
    const posts = state.signals.flatMap((signal) => signal.posts.map((post) => ({ signal, post }))).slice(0, 6);
    return `
      <p>Visible KOL / figure wire:</p>
      <ul>${posts.map(({ signal, post }) => `<li>${escapeHtml(post[0])}: ${escapeHtml(post[1])} <span class="cite">[[${escapeHtml(signal.word)}]]</span></li>`).join("") || "<li>Not recorded</li>"}</ul>
    `;
  }

  return `
    <p>Current selected signal: <b>${escapeHtml(state.selected.word)}</b></p>
    <p>${escapeHtml(state.selected.summary)}</p>
    <p>Inference: ${escapeHtml(state.selected.why)}</p>
    <p><span class="cite">[[${escapeHtml(state.selected.word)}]]</span></p>
  `;
}
function addMessage(role, html) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  article.innerHTML = `<b>${role === "user" ? "You" : "Trench Brain"}</b>${html}`;
  $("#chat-log").appendChild(article);
  $("#chat-log").scrollTop = $("#chat-log").scrollHeight;
  return article;
}

// ---- 実脳(brain/ask.sh 経由) への配線 ----
const ASK_URL = "/api/ask";
async function askBrain(question) {
  const res = await fetch(ASK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  const data = await res.json().catch(() => ({ ok: false, error: "bad response" }));
  if (!data.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data.answer || "";
}

// 実脳の markdown を最小HTML化(太字 / 箇条書き / [[wikilink]] / 段落)
function mdToHtml(md) {
  const lines = escapeHtml(md).split("\n");
  let html = "", inList = false;
  for (let line of lines) {
    line = line
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/\[\[([^\]]+)\]\]/g, '<span class="cite">[[$1]]</span>');
    const m = line.match(/^\s*[-•]\s+(.*)/);
    if (m) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${m[1]}</li>`;
    } else {
      if (inList) { html += "</ul>"; inList = false; }
      if (line.trim()) html += `<p>${line}</p>`;
    }
  }
  if (inList) html += "</ul>";
  return html;
}

async function connectData() {
  let lastError;
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
      $(".status-light").classList.add("live");
      $("#connection-label").textContent = "LIVE";
      $("#data-source").textContent = url.startsWith("http") ? "source: GitHub MAIN ui-data.json" : "source: local ui-data.json";
      $("#generated-at").textContent = payload.generated_at || "generated_at unknown";
      renderAll();
      return;
    } catch (error) {
      lastError = error;
    }
  }
  $("#connection-label").textContent = "FALLBACK";
  $("#generated-at").textContent = lastError?.message || "ui-data unavailable";
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

$("#chat-form").onsubmit = (event) => {
  event.preventDefault();
  const input = $("#question");
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
  // 実脳(/api/ask=ask.sh)に問う。返るまで thinking 表示→差し替え。
  // backend(brain/ui_server.py)が無ければ決め打ちダッシュボードに fallback。
  const thinking = addMessage("brain", `<p class="unknown">脳が wiki を横断中… <span class="dots">(実脳=headless・最大2-3分)</span></p>`);
  askBrain(text)
    .then((ans) => {
      thinking.innerHTML = `<b>Trench Brain</b>${mdToHtml(ans)}`;
      $("#chat-log").scrollTop = $("#chat-log").scrollHeight;
    })
    .catch(() => {
      thinking.innerHTML = `<b>Trench Brain</b>${answer(text)}`
        + `<p class="unknown">(offline: ui_server未起動 → ダッシュボード簡易応答。実脳には <code>python3 brain/ui_server.py</code> が要る)</p>`;
      $("#chat-log").scrollTop = $("#chat-log").scrollHeight;
    });
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
