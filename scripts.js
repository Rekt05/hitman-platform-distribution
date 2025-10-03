async function loadData() {
  const boardFile = document.getElementById("boardSelect").value;
  const res = await fetch(boardFile);
  const data = await res.json();

  await updatePlaceholder();

  return data
    .filter(r => r.platform)
    .sort((a, b) => {
      const [bd, bm, by] = a.submitted.split("/");
      const [ad, am, ay] = b.submitted.split("/");
      return new Date(`${ay}-${am}-${bd}`) - new Date(`${by}-${bm}-${ad}`);
    });
}

function classifyPlatform(platformName) {
  return platformName === "PC" ? "PC" : "Console";
}

function countPlatforms(runs) {
  const platformCounts = {};
  const pcConsoleCounts = { PC: 0, Console: 0 };

  runs.forEach(run => {
    const platform = run.platform;
    platformCounts[platform] = (platformCounts[platform] || 0) + 1;
    pcConsoleCounts[classifyPlatform(platform)]++;
  });

  return { platformCounts, pcConsoleCounts };
}

function renderCounts(counts, total, selectedRuns) {
  const pcDiv = document.getElementById("pcConsoleBreakdown");
  const allDiv = document.getElementById("allPlatformsBreakdown");
  const summaryDiv = document.getElementById("summaryInfo");

  const dates = selectedRuns.map(r => r.submitted);
  const minDate = dates[dates.length - 1];
  const maxDate = dates[0];
  summaryDiv.innerHTML = `Showing ${selectedRuns.length} most recent runs<br>From ${maxDate} to ${minDate}`;

  pcDiv.innerHTML = Object.entries(counts.pcConsoleCounts)
    .map(([k, v]) => `<div class="platform-entry"><span>${k}</span><span>${v} (${((v / total) * 100).toFixed(1)}%)</span></div>`)
    .join("");

  allDiv.innerHTML = Object.entries(counts.platformCounts)
    .map(([k, v]) => `<div class="platform-entry"><span>${k}</span><span>${v} (${((v / total) * 100).toFixed(1)}%)</span></div>`)
    .join("");
}

async function updatePlaceholder() {
  const boardFile = document.getElementById("boardSelect").value;
  const res = await fetch(boardFile);
  const data = await res.json();
  const input = document.getElementById("amount");
  input.placeholder = `Max runs: ${data.length}`;
}

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const num = parseInt(document.getElementById("amount").value);
  if (isNaN(num) || num <= 0) {
    alert("Please enter a valid number.");
    return;
  }

  const data = await loadData();
  const selectedRuns = data.slice(0, num);
  const counts = countPlatforms(selectedRuns);
  renderCounts(counts, selectedRuns.length, selectedRuns);
});

document.getElementById("boardSelect").addEventListener("change", updatePlaceholder);

const toggleBtn = document.getElementById('toggleInfoBtn');
const infoDiv = document.getElementById('projectInfo');

toggleBtn.addEventListener('click', () => {
  if (!infoDiv.style.display || infoDiv.style.display === 'none') {
    infoDiv.style.display = 'block';
    toggleBtn.textContent = 'Hide Info';
  } else {
    infoDiv.style.display = 'none';
    toggleBtn.textContent = 'Show Extra Info';
  }
});

updatePlaceholder();
