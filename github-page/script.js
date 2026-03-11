const folders = [
  { key: "logs", path: "log" },
  { key: "history", path: "history" },
  { key: "todo", path: "to-do" },
  { key: "errors", path: "error" },
];

const foldersGrid = document.getElementById("foldersGrid");
const folderTemplate = document.getElementById("folderTemplate");
const fileTemplate = document.getElementById("fileTemplate");
const refreshButton = document.getElementById("refreshButton");
const eventEditor = document.getElementById("eventEditor");
const eventStatus = document.getElementById("eventStatus");
const downloadEventButton = document.getElementById("downloadEventButton");

function detectGitHubRepo() {
  const host = window.location.hostname;
  if (!host.endsWith("github.io")) return null;

  const owner = host.replace(".github.io", "");
  const segments = window.location.pathname.split("/").filter(Boolean);
  const repo = segments[0] || "";
  if (!owner || !repo) return null;
  return { owner, repo };
}

function prettyContent(rawText) {
  try {
    return JSON.stringify(JSON.parse(rawText), null, 2);
  } catch {
    return rawText;
  }
}

function formatSize(bytes) {
  return `${bytes} bytes`;
}

async function listFiles(folderPath) {
  const repo = detectGitHubRepo();

  if (repo) {
    const apiUrl = `https://api.github.com/repos/${repo.owner}/${repo.repo}/contents/${folderPath}`;
    const response = await fetch(apiUrl);
    if (!response.ok) return [];

    const payload = await response.json();
    return Array.isArray(payload)
      ? payload.filter((item) => item.type === "file").map((item) => ({
          name: item.name,
          path: item.path,
          size: item.size,
          downloadUrl: item.download_url,
        }))
      : [];
  }

  const fallback = ["1.json", "2.json", "3.json"];
  return fallback.map((name) => ({
    name,
    path: `${folderPath}/${name}`,
    size: 0,
    downloadUrl: `../${folderPath}/${name}`,
  }));
}

async function readFile(downloadUrl) {
  const response = await fetch(downloadUrl);
  if (!response.ok) throw new Error(`Failed to read ${downloadUrl}`);
  return response.text();
}

async function loadFolder(folder) {
  const fragment = folderTemplate.content.cloneNode(true);
  const title = fragment.querySelector("h3");
  const countPill = fragment.querySelector(".pill");
  const filesNode = fragment.querySelector(".files");

  title.textContent = folder.path;

  const files = await listFiles(folder.path);
  countPill.textContent = `${files.length} files`;

  if (files.length === 0) {
    filesNode.innerHTML = '<p class="muted">No files found.</p>';
    foldersGrid.appendChild(fragment);
    return;
  }

  for (const file of files) {
    const fileFragment = fileTemplate.content.cloneNode(true);
    fileFragment.querySelector(".file-name").textContent = file.name;
    fileFragment.querySelector(".file-size").textContent = formatSize(file.size || 0);
    fileFragment.querySelector(".file-path").textContent = file.path;

    try {
      const content = await readFile(file.downloadUrl);
      fileFragment.querySelector(".file-content").textContent = prettyContent(content);
    } catch (error) {
      fileFragment.querySelector(".file-content").textContent = String(error);
    }

    filesNode.appendChild(fileFragment);
  }

  foldersGrid.appendChild(fragment);
}

async function loadEventJson() {
  const repo = detectGitHubRepo();
  const eventUrl = repo
    ? `https://raw.githubusercontent.com/${repo.owner}/${repo.repo}/main/event.json`
    : "../event.json";

  try {
    const raw = await readFile(eventUrl);
    eventEditor.value = prettyContent(raw);
    eventStatus.textContent = "Loaded event.json";
  } catch (error) {
    eventEditor.value = "";
    eventStatus.textContent = `Could not load event.json: ${String(error)}`;
  }
}

async function loadAll() {
  foldersGrid.innerHTML = "";
  await Promise.all(folders.map((folder) => loadFolder(folder)));
  await loadEventJson();
}

function downloadEventJson() {
  try {
    const parsed = JSON.parse(eventEditor.value);
    const blob = new Blob([`${JSON.stringify(parsed, null, 2)}\n`], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "event.json";
    anchor.click();

    URL.revokeObjectURL(url);
    eventStatus.textContent = "Downloaded updated event.json.";
  } catch (error) {
    eventStatus.textContent = `Invalid JSON: ${String(error)}`;
  }
}

refreshButton.addEventListener("click", () => {
  loadAll().catch((error) => {
    eventStatus.textContent = `Refresh failed: ${String(error)}`;
  });
});

downloadEventButton.addEventListener("click", downloadEventJson);

loadAll().catch((error) => {
  eventStatus.textContent = `Initial load failed: ${String(error)}`;
});
