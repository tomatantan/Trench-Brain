const signals = [
  {
    id: "speech",
    cluster: "skyfish",
    type: "FIGURE",
    title: "要人発言を検知",
    color: "#ff4ba8",
    size: 114,
    left: 54,
    duration: 24,
    delay: -8,
    related: ["flying-video", "space-fish"],
  },
  {
    id: "flying-video",
    cluster: "skyfish",
    type: "X BUZZ",
    title: "空飛ぶ魚の映像",
    color: "#ffb749",
    size: 98,
    left: 65,
    duration: 24,
    delay: -8,
    related: ["space-fish", "skyfish", "flyfish"],
  },
  {
    id: "space-fish",
    cluster: "skyfish",
    type: "NARRATIVE",
    title: "空飛ぶ生物",
    color: "#9d62ff",
    size: 86,
    left: 74,
    duration: 24,
    delay: -8,
    related: ["skyfish", "flyfish", "aqua"],
  },
  {
    id: "skyfish",
    cluster: "skyfish",
    type: "PUMP.FUN",
    title: "$SKYFISH",
    color: "#48eca0",
    size: 79,
    left: 82,
    duration: 24,
    delay: -8,
    related: [],
  },
  {
    id: "flyfish",
    cluster: "skyfish",
    type: "LAUNCH",
    title: "$FLYFISH",
    color: "#48eca0",
    size: 66,
    left: 88,
    duration: 24,
    delay: -8,
    related: [],
  },
  {
    id: "aqua",
    cluster: "skyfish",
    type: "LAUNCH",
    title: "$AQUA",
    color: "#48eca0",
    size: 61,
    left: 70,
    duration: 24,
    delay: -8,
    related: [],
  },
  {
    id: "blue-coast",
    cluster: "blue-bubble",
    type: "ODDITY",
    title: "海岸に青い泡",
    color: "#28e1f2",
    size: 91,
    left: 34,
    duration: 27,
    delay: -20,
    related: ["blue-posts", "bubble"],
  },
  {
    id: "blue-posts",
    cluster: "blue-bubble",
    type: "X BUZZ",
    title: "映像が世界拡散",
    color: "#ffb749",
    size: 73,
    left: 42,
    duration: 27,
    delay: -20,
    related: ["bubble", "foam"],
  },
  {
    id: "bubble",
    cluster: "blue-bubble",
    type: "PUMP.FUN",
    title: "$BUBBLE",
    color: "#48eca0",
    size: 68,
    left: 48,
    duration: 27,
    delay: -20,
    related: [],
  },
  {
    id: "foam",
    cluster: "blue-bubble",
    type: "LAUNCH",
    title: "$FOAM",
    color: "#48eca0",
    size: 59,
    left: 38,
    duration: 27,
    delay: -20,
    related: [],
  },
  {
    id: "robot-cat",
    cluster: "robot-cat",
    type: "SOCIAL",
    title: "猫型ロボが急上昇",
    color: "#28e1f2",
    size: 83,
    left: 18,
    duration: 22,
    delay: -14,
    related: ["kol-quote", "neko"],
  },
  {
    id: "kol-quote",
    cluster: "robot-cat",
    type: "KOL",
    title: "KOLが引用投稿",
    color: "#ff4ba8",
    size: 68,
    left: 25,
    duration: 22,
    delay: -14,
    related: ["neko", "mechacat"],
  },
  {
    id: "neko",
    cluster: "robot-cat",
    type: "LAUNCH",
    title: "$NEKO",
    color: "#48eca0",
    size: 63,
    left: 31,
    duration: 22,
    delay: -14,
    related: [],
  },
  {
    id: "mechacat",
    cluster: "robot-cat",
    type: "LAUNCH",
    title: "$MECHACAT",
    color: "#48eca0",
    size: 56,
    left: 21,
    duration: 22,
    delay: -14,
    related: [],
  },
];

const clusterLayouts = {
  skyfish: {
    label: "SKY CREATURE",
    color: "#9d62ff",
    lane: 84,
    width: 390,
    height: 300,
    duration: 31,
    delay: -8,
    positions: {
      speech: [28, 45],
      "flying-video": [58, 20],
      "space-fish": [57, 55],
      skyfish: [83, 34],
      flyfish: [90, 69],
      aqua: [69, 82],
    },
  },
  "blue-bubble": {
    label: "BLUE FOAM",
    color: "#28e1f2",
    lane: 50,
    width: 320,
    height: 270,
    duration: 35,
    delay: -24,
    positions: {
      "blue-coast": [34, 35],
      "blue-posts": [66, 22],
      bubble: [75, 64],
      foam: [37, 78],
    },
  },
  "robot-cat": {
    label: "ROBOT CAT",
    color: "#ff4ba8",
    lane: 17,
    width: 300,
    height: 250,
    duration: 28,
    delay: -17,
    positions: {
      "robot-cat": [30, 33],
      "kol-quote": [68, 25],
      neko: [72, 70],
      mechacat: [30, 78],
    },
  },
};

const field = document.querySelector("#signal-field");
const drawer = document.querySelector("#detail-drawer");
const backdrop = document.querySelector(".drawer-backdrop");
const drawerTitle = document.querySelector("#drawer-title");
const bubbleElements = new Map();
const clusterElements = new Map();

const linkLayer = document.createElementNS("http://www.w3.org/2000/svg", "svg");
linkLayer.classList.add("signal-links");
linkLayer.setAttribute("aria-hidden", "true");
linkLayer.innerHTML = `
  <defs>
    <filter id="signal-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.4" result="blur"></feGaussianBlur>
      <feMerge>
        <feMergeNode in="blur"></feMergeNode>
        <feMergeNode in="SourceGraphic"></feMergeNode>
      </feMerge>
    </filter>
  </defs>
`;
field.appendChild(linkLayer);

const relations = signals.flatMap((signal) =>
  signal.related.map((target) => ({
    source: signal.id,
    target,
    cluster: signal.cluster,
    color: signal.color,
  })),
);

const relationPaths = relations.map((relation) => {
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.classList.add("signal-link");
  path.dataset.cluster = relation.cluster;
  path.style.setProperty("--link-color", relation.color);
  linkLayer.appendChild(path);
  return { ...relation, path };
});

Object.entries(clusterLayouts).forEach(([clusterId, layout]) => {
  const cluster = document.createElement("section");
  cluster.className = "signal-cluster";
  cluster.dataset.cluster = clusterId;
  cluster.style.cssText = `
    --cluster-color:${layout.color};
    --cluster-left:${layout.lane}%;
    --cluster-width:${layout.width}px;
    --cluster-height:${layout.height}px;
    --cluster-duration:${layout.duration}s;
    --cluster-delay:${layout.delay}s;
  `;
  cluster.innerHTML = `
    <span class="cluster-halo"></span>
    <span class="cluster-label">${layout.label}</span>
    <span class="cluster-count">${
      signals.filter((signal) => signal.cluster === clusterId).length
    } SIGNALS</span>
  `;
  cluster.addEventListener("pointerenter", () => highlightCluster(clusterId));
  cluster.addEventListener("pointerleave", clearClusterHighlight);
  field.appendChild(cluster);
  clusterElements.set(clusterId, cluster);
});

signals.forEach((signal) => {
  const layout = clusterLayouts[signal.cluster];
  const position = layout.positions[signal.id];
  const bubble = document.createElement("button");
  bubble.className = "bubble";
  bubble.dataset.signalId = signal.id;
  bubble.dataset.cluster = signal.cluster;
  bubble.style.cssText = `
    --size:${signal.size}px;
    --bubble-color:${signal.color};
    --bubble-x:${position[0]}%;
    --bubble-y:${position[1]}%;
  `;
  bubbleElements.set(signal.id, bubble);
  bubble.setAttribute("aria-label", `${signal.type}: ${signal.title}`);
  bubble.innerHTML = `
    <span class="bubble-content">
      <span class="bubble-type">${signal.type}</span>
      <span class="bubble-title">${signal.title}</span>
    </span>
  `;
  bubble.addEventListener("click", () => openDrawer(signal));
  bubble.addEventListener("pointerenter", () => highlightCluster(signal.cluster));
  bubble.addEventListener("pointerleave", clearClusterHighlight);
  bubble.addEventListener("focus", () => highlightCluster(signal.cluster));
  bubble.addEventListener("blur", clearClusterHighlight);
  clusterElements.get(signal.cluster).appendChild(bubble);
});

function openDrawer(signal) {
  if (typeof signal === "string") {
    drawerTitle.textContent = signal;
    drawer.classList.add("open");
    backdrop.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    return;
  }

  const connected = signals
    .filter((candidate) => candidate.cluster === signal.cluster && candidate.id !== signal.id)
    .map((candidate) => candidate.title)
    .join(" / ");
  drawerTitle.textContent = signal.title;
  const notice = drawer.querySelector(".drawer-section p");
  if (notice) {
    notice.textContent = `同じ話題として ${connected} を検出。単一銘柄ではなく、発言・投稿・ナラティブ・複数ローンチを一つのクラスターとして追跡しています。`;
  }
  drawer.classList.add("open");
  backdrop.classList.add("open");
  drawer.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function highlightCluster(cluster) {
  field.classList.add("is-inspecting");
  field.querySelectorAll(".bubble").forEach((bubble) => {
    bubble.classList.toggle("is-related", bubble.dataset.cluster === cluster);
  });
  relationPaths.forEach(({ path, cluster: pathCluster }) => {
    path.classList.toggle("is-related", pathCluster === cluster);
  });
}

function clearClusterHighlight() {
  field.classList.remove("is-inspecting");
  field.querySelectorAll(".bubble, .signal-link").forEach((element) => {
    element.classList.remove("is-related");
  });
}

function updateSignalLinks() {
  const fieldRect = field.getBoundingClientRect();
  linkLayer.setAttribute("viewBox", `0 0 ${fieldRect.width} ${fieldRect.height}`);

  relationPaths.forEach(({ source, target, path }) => {
    const sourceElement = bubbleElements.get(source);
    const targetElement = bubbleElements.get(target);
    if (!sourceElement || !targetElement) return;
    if (sourceElement.offsetParent === null || targetElement.offsetParent === null) {
      path.style.visibility = "hidden";
      return;
    }
    path.style.visibility = "visible";

    const sourceRect = sourceElement.getBoundingClientRect();
    const targetRect = targetElement.getBoundingClientRect();
    const x1 = sourceRect.left - fieldRect.left + sourceRect.width / 2;
    const y1 = sourceRect.top - fieldRect.top + sourceRect.height / 2;
    const x2 = targetRect.left - fieldRect.left + targetRect.width / 2;
    const y2 = targetRect.top - fieldRect.top + targetRect.height / 2;
    const bend = Math.max(24, Math.abs(x2 - x1) * 0.32);

    path.setAttribute(
      "d",
      `M ${x1} ${y1} C ${x1 + bend} ${y1 - 10}, ${x2 - bend} ${y2 + 10}, ${x2} ${y2}`,
    );
  });

  requestAnimationFrame(updateSignalLinks);
}

requestAnimationFrame(updateSignalLinks);

function closeDrawer() {
  drawer.classList.remove("open");
  backdrop.classList.remove("open");
  drawer.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

document.querySelector(".drawer-close").addEventListener("click", closeDrawer);
backdrop.addEventListener("click", closeDrawer);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeDrawer();
});

document.querySelectorAll(".lead-signal, .signal-card").forEach((card) => {
  const title = card.querySelector("h3")?.textContent.replace(/\s+/g, " ").trim();
  card.addEventListener("click", () => openDrawer(title));
  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") openDrawer(title);
  });
});

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector(".filter.active")?.classList.remove("active");
    button.classList.add("active");
    const filter = button.dataset.filter;
    document.querySelectorAll("[data-category]").forEach((card) => {
      card.classList.toggle("is-hidden", filter !== "all" && card.dataset.category !== filter);
    });
  });
});

function updateTime() {
  const time = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Asia/Tokyo",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date());
  document.querySelector("#local-time").textContent = `${time} JST`;
}

updateTime();
setInterval(updateTime, 1000);

const glow = document.querySelector(".cursor-glow");
document.addEventListener("pointermove", (event) => {
  glow.style.left = `${event.clientX}px`;
  glow.style.top = `${event.clientY}px`;
});

document.querySelector("#search-button").addEventListener("click", () => {
  document.querySelector("#feed").scrollIntoView({ behavior: "smooth" });
});
