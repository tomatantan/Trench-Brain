const predictions = {
  "PERSIAN GULF": {
    score: 89,
    copy: "地名として既に認知され、対立・石油・航路を一語で圧縮できる。画像・旗・地図へ変換しやすく、立場の違う陣営でも再利用可能。",
    path: [["世界情勢", "US–Iran tension"], ["集団感情", "不安・対立・期待"], ["記憶パターン", "2019 tanker crisis"], ["圧縮ワード", "PERSIAN GULF"]],
    evidence: ["ホワイトハウスの航路安全保障発言", "2019年タンカー危機の語彙パターン", "湾岸戦争期の象徴語化"],
  },
  "OIL PANIC": {
    score: 77,
    copy: "生活コストへの不安と戦争報道を接続する短い表現。ガソリン価格画像やパニック反応と組み合わせやすい。",
    path: [["供給不安", "oil route risk"], ["生活感情", "gas price anxiety"], ["X表現", "panic posting"], ["圧縮ワード", "OIL PANIC"]],
    evidence: ["原油価格への言及増加", "過去のガソリン価格meme", "ニュース見出しでのpanic語彙"],
  },
  "RED BUTTON": {
    score: 71,
    copy: "警報・決断・破局を一枚絵にしやすい視覚語。政治家の人物像やカウントダウン表現へ派生しやすい。",
    path: [["警戒報道", "alert graphics"], ["視覚記号", "red interface"], ["人物像", "decision maker"], ["圧縮ワード", "RED BUTTON"]],
    evidence: ["赤色警報画面の拡散", "核ボタンmemeの履歴", "カウントダウン画像の再利用"],
  },
  "DEALMAKER": {
    score: 58,
    copy: "交渉を人物キャラクターへ圧縮する語。支持・皮肉のどちらにも利用できるが、新規性はやや低い。",
    path: [["要人発言", "negotiation claim"], ["人物化", "hero / villain"], ["既存記憶", "deal rhetoric"], ["圧縮ワード", "DEALMAKER"]],
    evidence: ["過去の選挙スローガン", "交渉報道での反復", "人物中心memeの型"],
  },
};

const mockWordSets = [
  ["PERSIAN GULF", "OIL PANIC", "RED BUTTON", "DEALMAKER"],
  ["COPYRIGHT WAR", "PROMPT POLICE", "DATA GHOST", "ROBOT AUTHOR"],
  ["MARS RACE", "SPACE KING", "MOON TAX", "RED PLANET"],
  ["RED OCEAN", "BLOOD TIDE", "SEA GLITCH", "OCEAN ALERT"],
];

const canvas = document.querySelector("#brain-canvas");
const layer = document.querySelector("#synapse-layer");
const seed = document.querySelector("#query-seed");
const dialog = document.querySelector("#word-dialog");

function center(el, parent) {
  const r = el.getBoundingClientRect(), p = parent.getBoundingClientRect();
  return { x: r.left - p.left + r.width / 2, y: r.top - p.top + r.height / 2 };
}

function drawSynapses() {
  const r = canvas.getBoundingClientRect();
  layer.setAttribute("viewBox", `0 0 ${r.width} ${r.height}`);
  const nodes = [...document.querySelectorAll(".word-neuron")];
  const evidence = [...document.querySelectorAll(".evidence-node")];
  const paths = [];
  const s = center(seed, canvas);
  nodes.forEach((node) => {
    const n = center(node, canvas);
    paths.push(`<path class="synapse" style="stroke:${getComputedStyle(node).getPropertyValue("--tone")}" d="M${s.x},${s.y} C${s.x+70},${s.y} ${n.x-70},${n.y} ${n.x},${n.y}"/>`);
  });
  evidence.forEach((item) => {
    const target = document.querySelector(`.word-neuron[data-word="${item.dataset.target}"]`);
    if (!target) return;
    const a = center(item, canvas), b = center(target, canvas);
    paths.push(`<path class="synapse dim" style="stroke:#9e72ff" d="M${a.x},${a.y} C${(a.x+b.x)/2},${a.y} ${(a.x+b.x)/2},${b.y} ${b.x},${b.y}"/>`);
  });
  layer.innerHTML = paths.join("");
  requestAnimationFrame(drawSynapses);
}

function selectWord(word) {
  const data = predictions[word] || {
    score: 65,
    copy: "LLM Wiki内の事象・世論・過去パターンから生成された連想候補。実データ接続時は根拠ページと出典を表示します。",
    path: [["入力事象", "current event"], ["世論", "collective emotion"], ["過去パターン", "historical analogy"], ["候補ワード", word]],
    evidence: ["関連ニュース", "要人発言", "過去の類似meme"],
  };
  document.querySelectorAll(".word-neuron").forEach((n) => n.classList.toggle("selected", n.dataset.word === word));
  document.querySelector("#selected-word").textContent = word;
  document.querySelector("#forecast-word").textContent = word;
  document.querySelector("#forecast-score").textContent = data.score;
  document.querySelector("#forecast-copy").textContent = data.copy;
  document.querySelector("#association-path").innerHTML = data.path.map(([a,b]) => `<li><b>${a}</b><small>${b}</small></li>`).join("");
}

function openWord(word) {
  selectWord(word);
  const data = predictions[word] || { copy: "予測候補", evidence: ["関連ソースを収集中"] };
  document.querySelector("#dialog-word").textContent = word;
  document.querySelector("#dialog-reason").textContent = data.copy;
  document.querySelector("#dialog-evidence").innerHTML = data.evidence.map((e) => `<div>${e}</div>`).join("");
  dialog.showModal();
}

function runQuery(query, setIndex = 0) {
  const words = mockWordSets[setIndex % mockWordSets.length];
  document.querySelector("#query-seed strong").textContent = query.includes("イラン") ? "US × IRAN" : query.slice(0, 13).toUpperCase();
  document.querySelectorAll(".word-neuron").forEach((node, i) => {
    node.dataset.word = words[i];
    node.querySelector("h2").innerHTML = words[i].replace(" ", "<br>");
  });
  selectWord(words[0]);
}

document.querySelectorAll(".word-neuron").forEach((node) => {
  node.addEventListener("click", () => openWord(node.dataset.word));
});
document.querySelectorAll(".evidence-node").forEach((node) => {
  node.addEventListener("click", () => openWord(node.dataset.target));
});
document.querySelector("#cortex-search").addEventListener("submit", (e) => {
  e.preventDefault();
  const q = document.querySelector("#query-input").value.trim();
  const idx = q.includes("AI") ? 1 : q.includes("宇宙") ? 2 : q.includes("気象") || q.includes("海") ? 3 : 0;
  runQuery(q, idx);
});
document.querySelectorAll(".pulse-item").forEach((item, i) => {
  item.addEventListener("click", () => {
    document.querySelector(".pulse-item.active")?.classList.remove("active");
    item.classList.add("active");
    document.querySelector("#query-input").value = item.dataset.query;
    runQuery(item.dataset.query, i);
  });
});
document.querySelectorAll(".suggestion-row button").forEach((b) => {
  b.addEventListener("click", () => {
    document.querySelector("#query-input").value = `${b.textContent}からmeme化するワード`;
    document.querySelector("#query-input").focus();
  });
});
document.querySelector(".close-dialog").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });

const feedWords = [
  ["GULF","US/MENA","航路・石油・対立が交差","#4ff4ff"],
  ["PROMPT POLICE","US/EU","AI著作権争いから浮上","#9e72ff"],
  ["RED OCEAN","EU","異常映像の再利用性が上昇","#ff5bac"],
  ["SPACE KING","US","要人発言と宇宙競争が接続","#ffb64d"],
];
document.querySelector("#feed-track").innerHTML = feedWords.map(([w,a,t,c]) => `<button class="feed-word" data-word="${w}" style="--word-color:${c}"><b>${w}</b><span>${a}</span><small>${t}</small></button>`).join("");
document.querySelectorAll(".feed-word").forEach((b) => b.addEventListener("click", () => openWord(b.dataset.word)));

function clock() {
  document.querySelector("#clock").textContent = new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Tokyo",hour:"2-digit",minute:"2-digit",second:"2-digit",hour12:false}).format(new Date())+" JST";
}
clock(); setInterval(clock,1000); selectWord("PERSIAN GULF"); requestAnimationFrame(drawSynapses);
