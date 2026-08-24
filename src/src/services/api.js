const API_BASE = "/api";

export async function fetchDashboard() {
  const res = await fetch(`${API_BASE}/dashboard`);
  if (!res.ok) throw new Error("Failed to load dashboard data");
  return res.json();
}

export async function analyzeScript(data) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Script analysis failed");
  return res.json();
}

export async function enhancePrompt(data) {
  const res = await fetch(`${API_BASE}/enhance-prompt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Prompt enhancement failed");
  return res.json();
}

export async function generateCandidates(data) {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Candidate generation failed");
  return res.json();
}

export async function fetchViralLibrary(category = "", search = "") {
  const params = new URLSearchParams();
  if (category && category !== "All") params.append("category", category);
  if (search) params.append("search", search);
  const res = await fetch(`${API_BASE}/viral-library?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch viral library");
  return res.json();
}

export async function addViralScript(data) {
  const res = await fetch(`${API_BASE}/viral-library`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to add viral script");
  return res.json();
}

export async function fetchUserScripts() {
  const res = await fetch(`${API_BASE}/scripts`);
  if (!res.ok) throw new Error("Failed to fetch scripts");
  return res.json();
}

export async function createScript(data) {
  const res = await fetch(`${API_BASE}/scripts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create script");
  return res.json();
}

export async function updateScript(id, data) {
  const res = await fetch(`${API_BASE}/scripts/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update script");
  return res.json();
}

export async function deleteScript(id) {
  const res = await fetch(`${API_BASE}/scripts/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete script");
  return res.json();
}

export async function sendAiAdvisorChat(data) {
  const res = await fetch(`${API_BASE}/ai-advisor`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("AI Advisor failed to respond");
  return res.json();
}

export async function fetchAnalytics() {
  const res = await fetch(`${API_BASE}/analytics`);
  if (!res.ok) throw new Error("Failed to fetch analytics");
  return res.json();
}

export async function generateReport(data) {
  const res = await fetch(`${API_BASE}/reports/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to generate report");
  return res.json();
}

export async function analyzeReel(data) {
  const res = await fetch(`${API_BASE}/analyze-reel`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Reel analysis failed");
  return res.json();
}
