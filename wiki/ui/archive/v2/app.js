const terrain = document.querySelector("#terrain");
const lineLayer = document.querySelector("#terrain-lines");
const clock = document.querySelector("#clock");
const dialog = document.querySelector("#trace-dialog");
const ambientLayer = document.querySelector("#ambient-neural-net");
const ctFeedTrack = document.querySelector("#ct-feed-track");
const dataStatus = document.querySelector("#data-status");
const UI_DATA_URL = "../ui-data.json";
const clusterSlots = ["sky-creature", "blue-foam", "robot-cat", "rate-cut"];
let liveSignals = [];

const clusterData = {
  "sky-creature": {
    label: "SKY CREATURE",
    title: "発言より映像が<br />主導する派生相場",
    copy: "要人発言が起点だが、現在の拡散は「空飛ぶ魚」の視覚素材が牽引。トークン名より画像の再利用性が共通項。",
    confidence: 82,
    color: "#f4d35e",
    area: "US",
    place: "WASHINGTON D.C.",
  },
  "blue-foam": {
    label: "BLUE FOAM",
    title: "珍事映像が生む<br />色彩ベースの銘柄群",
    copy: "現地映像そのものより、青という色と泡の形状が派生語を増殖させている。短命だがローンチ速度は高い。",
    confidence: 71,
    color: "#79d7c5",
    area: "EU",
    place: "GALICIA, SPAIN",
  },
  "robot-cat": {
    label: "ROBOT CAT",
    title: "失敗映像と愛嬌が<br />同時に拡散",
    copy: "技術ニュースではなく、転倒する猫型ロボの不完全さがミームの核。KOL引用後に名称違いの銘柄が分岐。",
    confidence: 64,
    color: "#f08cae",
    area: "ASIA",
    place: "TOKYO, JAPAN",
  },
  "rate-cut": {
    label: "RATE CUT",
    title: "マクロ期待は強いが<br />meme接続はまだ弱い",
    copy: "暗号資産全体への資金流入仮説は補強される一方、特定ナラティブやローンチとの直接接続は不足している。",
    confidence: 43,
    color: "#9b9f91",
    area: "GLOBAL",
    place: "GLOBAL MARKETS",
  },
};

const links = [
  ["sky-creature", "speech"],
  ["sky-creature", "viral-video"],
  ["sky-creature", "skyfish"],
  ["sky-creature", "flyfish"],
  ["sky-creature", "aqua"],
  ["blue-foam", "coast-video"],
  ["blue-foam", "bubble"],
  ["blue-foam", "foam"],
  ["robot-cat", "cat-video"],
  ["robot-cat", "neko"],
  ["rate-cut", "macro-release"],
];

const mockCtPosts = [
  {
    author: "Elon Musk",
    handle: "@elonmusk",
    initials: "EM",
    area: "US",
    text: "Maybe everything should fly.",
    impact: 96,
    cluster: "sky-creature",
    color: "#ff4fa9",
  },
  {
    author: "Toly",
    handle: "@aeyakovenko",
    initials: "TO",
    area: "US",
    text: "Consumer crypto is going to get delightfully weird.",
    impact: 81,
    cluster: "robot-cat",
    color: "#946bff",
  },
  {
    author: "Ansem",
    handle: "@blknoiz06",
    initials: "AN",
    area: "US",
    text: "Timeline is rotating into visual memes again.",
    impact: 88,
    cluster: "blue-foam",
    color: "#37f5ff",
  },
  {
    author: "The White House",
    handle: "@WhiteHouse",
    initials: "WH",
    area: "US",
    text: "Remarks from today’s technology and investment roundtable.",
    impact: 73,
    cluster: "rate-cut",
    color: "#ffd45f",
  },
  {
    author: "Cobie",
    handle: "@cobie",
    initials: "CO",
    area: "EU",
    text: "The animal coins have discovered another dimension.",
    impact: 77,
    cluster: "sky-creature",
    color: "#42ffbf",
  },
  {
    author: "Mert",
    handle: "@0xMert_",
    initials: "ME",
    area: "US",
    text: "Three launches using the same dev graph in six minutes.",
    impact: 84,
    cluster: "robot-cat",
    color: "#62b6ff",
  },
];

const linkElements = links.map(([cluster, node]) => {
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.classList.add("terrain-link");
  path.dataset.cluster = cluster;
  path.style.stroke = clusterData[cluster].color;
  lineLayer.appendChild(path);
  return { cluster, node, path };
});

const ambientNodes = Array.from({ length: 42 }, (_, index) => {
  const x = 4 + ((index * 37) % 92);
  const y = 5 + ((index * 61) % 88);
  const radius = index % 9 === 0 ? 2.6 : index % 4 === 0 ? 1.8 : 1.1;
  return { x, y, radius };
});

function buildAmbientNetwork() {
  ambientLayer.setAttribute("viewBox", "0 0 100 100");
  const lines = [];

  ambientNodes.forEach((node, index) => {
    const candidates = ambientNodes
      .map((target, targetIndex) => ({
        target,
        targetIndex,
        distance: Math.hypot(target.x - node.x, target.y - node.y),
      }))
      .filter(({ targetIndex }) => targetIndex !== index)
      .sort((a, b) => a.distance - b.distance)
      .slice(0, index % 5 === 0 ? 3 : 2);

    candidates.forEach(({ target, targetIndex }) => {
      if (targetIndex < index) return;
      lines.push(
        `<line x1="${node.x}" y1="${node.y}" x2="${target.x}" y2="${target.y}" style="--pulse-delay:${(index % 8) * -0.45}s"></line>`,
      );
    });
  });

  ambientLayer.innerHTML = `
    <g class="ambient-axons">${lines.join("")}</g>
    <g class="ambient-nodes">
      ${ambientNodes
        .map(
          (node, index) =>
            `<circle cx="${node.x}" cy="${node.y}" r="${node.radius}" style="--node-delay:${(index % 11) * -0.38}s"></circle>`,
        )
        .join("")}
    </g>
  `;
}

function centerOf(element, parentRect) {
  const rect = element.getBoundingClientRect();
  return {
    x: rect.left - parentRect.left + rect.width / 2,
    y: rect.top - parentRect.top + rect.height / 2,
  };
}

function drawLinks() {
  const parentRect = terrain.getBoundingClientRect();
  lineLayer.setAttribute("viewBox", `0 0 ${parentRect.width} ${parentRect.height}`);

  linkElements.forEach(({ cluster, node, path }) => {
    const sourceElement = document.querySelector(`#${cluster} .island-core`);
    const targetElement = document.querySelector(`[data-node="${node}"]`);
    if (!sourceElement || !targetElement) return;

    const source = centerOf(sourceElement, parentRect);
    const target = centerOf(targetElement, parentRect);
    const bend = Math.max(22, Math.abs(target.x - source.x) * 0.34);
    const direction = target.x > source.x ? 1 : -1;

    path.setAttribute(
      "d",
      `M ${source.x} ${source.y} C ${source.x + bend * direction} ${source.y}, ${target.x - bend * direction} ${target.y}, ${target.x} ${target.y}`,
    );
  });

  requestAnimationFrame(drawLinks);
}

function focusCluster(clusterId) {
  terrain.classList.add("is-focused");
  terrain.querySelectorAll("[data-cluster]").forEach((element) => {
    element.classList.toggle("focused", element.dataset.cluster === clusterId);
  });
  linkElements.forEach(({ cluster, path }) => {
    path.classList.toggle("focused", cluster === clusterId);
  });
  document.querySelectorAll(".source-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.focus === clusterId);
  });
}

function clearFocus() {
  terrain.classList.remove("is-focused");
  terrain.querySelectorAll(".focused").forEach((element) => element.classList.remove("focused"));
}

function selectCluster(clusterId) {
  const data = clusterData[clusterId];
  if (!data) return;

  document.querySelectorAll(".narrative-island").forEach((island) => {
    island.classList.toggle("selected", island.id === clusterId);
  });
  document.querySelector("#selected-label").textContent = data.label;
  document.querySelector("#thesis-title").innerHTML = data.title;
  document.querySelector("#thesis-copy").textContent = data.copy;
  document.querySelector("#confidence-value").textContent = `${data.confidence}%`;
  document.querySelector("#confidence-bar").style.width = `${data.confidence}%`;
  document.querySelector("#confidence-bar").style.background = data.color;
  document.querySelector("#origin-area").textContent = data.area;
  document.querySelector("#origin-place").textContent = data.place;
  updateTraceDialog(data);
}

function confidenceNumber(value, signal) {
  const numeric = Number.parseFloat(value);
  if (Number.isFinite(numeric)) return Math.min(99, Math.max(20, numeric));
  if (value === "高") return 88;
  if (value === "中") return 68;
  if (value === "低") return 42;
  return Math.min(92, 38 + (signal.accounts || 0) * 3 + Math.log2((signal.mentions || 1) + 1) * 5);
}

function areaForType(type) {
  if (type === "WORLD") return { area: "GLOBAL", place: "WORLD EVENT GRAPH" };
  if (type === "MACRO") return { area: "GLOBAL", place: "MACRO / MARKET" };
  return { area: "CT", place: "CRYPTO TWITTER" };
}

function areaClass(area) {
  return {
    US: "us",
    EU: "eu",
    ASIA: "asia",
    GLOBAL: "global",
    CT: "middle-east",
  }[area] || "global";
}

function updateTraceDialog(data) {
  document.querySelector(".trace-dialog .section-code").textContent = `SIGNAL TRACE / ${data.label}`;
  document.querySelector("#trace-dialog-title").innerHTML = `${data.label}<br />が浮上した理由`;

  const causal = data.trace?.causal?.length
    ? data.trace.causal
    : ["X mentions", "cross-account spread", "token attention"];
  document.querySelector("#trace-chain").innerHTML = causal
    .slice(0, 4)
    .map((item, index) => `${index ? "<i>→</i>" : ""}<span>${item}<small>${index === 0 ? "OBSERVED" : "SYNTHESIZED"}</small></span>`)
    .join("");

  document.querySelector("#trace-top-posts").innerHTML = (data.trace?.top || [])
    .slice(0, 3)
    .map(
      (post) => `
        <div class="trace-top-post">
          <b>@${post.account}</b>
          <span>${post.text}</span>
          <i>${Number(post.likes || 0).toLocaleString()} ♥</i>
        </div>`,
    )
    .join("");
}

function applySignalToSlot(signal, clusterId, index) {
  const area = areaForType(signal.type);
  const confidence = confidenceNumber(signal.trace?.confidence, signal);
  const topPost = signal.trace?.top?.[0];
  const data = clusterData[clusterId];

  Object.assign(data, {
    label: signal.title,
    title: `${signal.title} が<br />神経核へ浮上`,
    copy: signal.trace?.why || `${signal.mentions || 0} mentions / ${signal.accounts || 0} accounts`,
    confidence,
    color: signal.color,
    area: area.area,
    place: area.place,
    trace: signal.trace,
    raw: signal,
  });

  const island = document.querySelector(`#${clusterId}`);
  island.style.setProperty("--tone", signal.color);
  island.style.setProperty("--scale", String(0.58 + Math.min(130, signal.size || 80) / 310));
  island.querySelector(".island-rank").textContent = `#${String(index + 1).padStart(2, "0")}`;
  island.querySelector(".island-area").className = `island-area ${areaClass(area.area)}`;
  island.querySelector(".island-area").textContent = area.area;
  island.querySelector(".island-core > small").textContent = signal.type;
  island.querySelector(".island-core h2").innerHTML = signal.title.replace("$", "$<br>");
  island.querySelector(".island-score b").textContent = Math.round((signal.glow || 0.5) * 100);

  const sourceItem = document.querySelector(`.source-item[data-focus="${clusterId}"]`);
  sourceItem.querySelector(".source-kind").className = `source-kind ${signal.type.toLowerCase()}`;
  sourceItem.querySelector(".source-kind").textContent = signal.type;
  sourceItem.querySelector(".area-tag").className = `area-tag ${areaClass(area.area)}`;
  sourceItem.querySelector(".area-tag").textContent = `AREA / ${area.area}`;
  sourceItem.querySelector("strong").textContent = topPost
    ? `@${topPost.account}: ${topPost.text}`
    : signal.trace?.why || signal.title;
  sourceItem.querySelector("small").textContent =
    `${signal.mentions || 0} mentions · ${signal.accounts || 0} accounts · ${Number(topPost?.likes || 0).toLocaleString()} ♥`;
  sourceItem.querySelector(".heat-bar").style.setProperty("--heat", `${Math.round((signal.glow || 0.5) * 100)}%`);

  const clusterNodes = [...document.querySelectorAll(`.field-node[data-cluster="${clusterId}"]`)];
  clusterNodes.forEach((node, nodeIndex) => {
    const post = signal.trace?.top?.[nodeIndex];
    if (post) {
      node.querySelector("span").textContent = `@${post.account}`;
      node.querySelector("small").textContent = `${Number(post.likes || 0).toLocaleString()} ♥`;
    } else if (node.classList.contains("token-node")) {
      node.querySelector("span").textContent = signal.title;
      node.querySelector("small").textContent = `${signal.mentions || 0} MENTIONS`;
    }
  });
}

function feedPostsFromSignals(signals) {
  return signals.flatMap((signal) =>
    (signal.trace?.top || []).slice(0, 2).map((post) => ({
      author: post.account,
      handle: `@${post.account}`,
      initials: post.account.slice(0, 2).toUpperCase(),
      area: areaForType(signal.type).area,
      text: post.text,
      impact: Math.min(99, 45 + Math.round(Math.log10((post.likes || 0) + 1) * 12)),
      cluster: signal.__cluster,
      color: signal.color,
    })),
  );
}

async function loadUiData() {
  try {
    const response = await fetch(`${UI_DATA_URL}?t=${Date.now()}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`ui-data ${response.status}`);
    const payload = await response.json();
    liveSignals = (payload.signals || []).slice(0, clusterSlots.length);
    liveSignals.forEach((signal, index) => {
      signal.__cluster = clusterSlots[index];
      applySignalToSlot(signal, clusterSlots[index], index);
    });

    const liveFeedPosts = feedPostsFromSignals(liveSignals);
    if (liveFeedPosts.length) {
      mockCtPosts.splice(0, mockCtPosts.length, ...liveFeedPosts);
      ctFeedTrack.replaceChildren();
      mockFeedCursor = 0;
      seedCtFeed();
    }

    linkElements.forEach(({ cluster, path }) => {
      path.style.stroke = clusterData[cluster].color;
    });
    selectCluster(clusterSlots[0]);
    dataStatus.lastChild.textContent = " LIVE DATA";
    dataStatus.classList.add("connected");
  } catch (error) {
    dataStatus.lastChild.textContent = " MOCK DATA";
    dataStatus.title = `ui-data.json unavailable: ${error.message}`;
  }
}

function fireFromFeed(clusterId) {
  selectCluster(clusterId);
  focusCluster(clusterId);
  const island = document.querySelector(`#${clusterId}`);
  island?.classList.remove("feed-fired");
  requestAnimationFrame(() => island?.classList.add("feed-fired"));
  setTimeout(() => {
    island?.classList.remove("feed-fired");
    clearFocus();
  }, 1800);
}

function formatFeedTime(date = new Date()) {
  return new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Tokyo",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

function createCtPost(post, isNew = false) {
  const item = document.createElement("button");
  item.className = `ct-post${isNew ? " is-new" : ""}`;
  item.style.setProperty("--post-color", post.color);
  item.dataset.cluster = post.cluster;
  item.innerHTML = `
    <span class="ct-avatar">${post.initials}</span>
    <span class="ct-copy">
      <span class="ct-author">${post.author}</span>
      <span class="ct-meta">${post.handle} · ${post.area} · ${formatFeedTime()}</span>
      <span class="ct-text">${post.text}</span>
    </span>
    <span class="ct-impact">
      <span>MEME IMPACT</span>
      <strong>${post.impact}</strong>
      <i><b style="--impact:${post.impact}%"></b></i>
    </span>
  `;
  item.addEventListener("click", () => fireFromFeed(post.cluster));
  return item;
}

let mockFeedCursor = 0;

function seedCtFeed() {
  mockCtPosts.slice(0, 3).forEach((post) => ctFeedTrack.appendChild(createCtPost(post)));
  mockFeedCursor = 3;
}

function injectMockCtPost() {
  const post = mockCtPosts[mockFeedCursor % mockCtPosts.length];
  const item = createCtPost(post, true);
  ctFeedTrack.prepend(item);
  mockFeedCursor += 1;

  while (ctFeedTrack.children.length > 6) {
    ctFeedTrack.lastElementChild?.remove();
  }

  document.querySelector("#high-impact-count").textContent = String(
    [...ctFeedTrack.children].filter((element) => {
      const impact = Number(element.querySelector(".ct-impact strong")?.textContent || 0);
      return impact >= 80;
    }).length,
  ).padStart(2, "0");
}

document.querySelectorAll(".narrative-island").forEach((island) => {
  island.addEventListener("pointerenter", () => focusCluster(island.dataset.cluster));
  island.addEventListener("pointerleave", clearFocus);
  island.addEventListener("focus", () => focusCluster(island.dataset.cluster));
  island.addEventListener("blur", clearFocus);
  island.addEventListener("click", () => selectCluster(island.dataset.cluster));
});

document.querySelectorAll(".field-node").forEach((node) => {
  node.addEventListener("pointerenter", () => focusCluster(node.dataset.cluster));
  node.addEventListener("pointerleave", clearFocus);
  node.addEventListener("click", () => selectCluster(node.dataset.cluster));
});

document.querySelectorAll(".source-item").forEach((item) => {
  item.addEventListener("pointerenter", () => focusCluster(item.dataset.focus));
  item.addEventListener("pointerleave", clearFocus);
  item.addEventListener("click", () => {
    selectCluster(item.dataset.focus);
    document.querySelector(`#${item.dataset.focus}`)?.focus();
  });
});

document.querySelectorAll(".mode-switch button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector(".mode-switch button.active")?.classList.remove("active");
    button.classList.add("active");
  });
});

document.querySelector("#open-trace").addEventListener("click", () => dialog.showModal());
document.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

function updateClock() {
  const value = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Tokyo",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date());
  clock.textContent = `${value} JST`;
}

updateClock();
setInterval(updateClock, 1000);
buildAmbientNetwork();
seedCtFeed();
setInterval(injectMockCtPost, 6500);
loadUiData();
requestAnimationFrame(drawLinks);
