const API = "https://YOUR-RENDER-URL.onrender.com";

// Allow Enter key to trigger search
document.getElementById("searchInput")
  .addEventListener("keydown", e => { if (e.key === "Enter") search(); });

function showSkeletons() {
  const grid = document.getElementById("results");
  grid.innerHTML = Array(6).fill(`
    <div class="skeleton">
      <div class="skel-img"></div>
      <div class="skel-body">
        <div class="skel-line"></div>
        <div class="skel-line med"></div>
        <div class="skel-line short"></div>
      </div>
    </div>`).join("");
}

function starsHtml(rating) {
  const r = parseFloat(rating);
  if (!r || isNaN(r)) return "";
  const full  = Math.round(r);
  const empty = 5 - full;
  return `<span class="stars">${"★".repeat(full)}${"☆".repeat(empty)}</span> ${r}`;
}

function renderCard(item) {
  const src       = item.source.toLowerCase();
  const bestBadge = item.best_deal
    ? `<div class="best-badge">🏆 Best Deal</div>` : "";
  const imgTag    = item.image
    ? `<img class="card-img" src="${item.image}" alt="${item.title}" loading="lazy" onerror="this.style.display='none'">`
    : `<div class="card-img" style="display:flex;align-items:center;justify-content:center;color:#555;font-size:2rem">🛍️</div>`;
  const discount  = item.discount
    ? `<span style="color:#ff9900;font-size:0.82rem">${item.discount}</span>` : "";
  const reviews   = item.reviews !== "N/A"
    ? `· ${item.reviews} reviews` : "";

  return `
    <div class="card ${item.best_deal ? "best" : ""}">
      ${bestBadge}
      <div class="source-badge ${src}">${item.source}</div>
      ${imgTag}
      <div class="card-body">
        <div class="card-title">${item.title}</div>
        <div class="card-price">${item.price}</div>
        <div class="card-meta">
          ${starsHtml(item.rating)}
          <span>${reviews}</span>
          ${discount}
        </div>
      </div>
      <div class="card-footer">
        <a class="buy-btn ${src}" href="${item.link}" target="_blank" rel="noopener">
          Buy on ${item.source} →
        </a>
      </div>
    </div>`;
}

async function search() {
  const query = document.getElementById("searchInput").value.trim();
  if (!query) return;

  const btn    = document.getElementById("searchBtn");
  const status = document.getElementById("status");
  const summary= document.getElementById("summary");
  const results= document.getElementById("results");

  // UI: loading state
  btn.disabled = true;
  btn.textContent = "Searching...";
  status.className = "status loading";
  status.textContent = "⏳ Fetching prices from Amazon & Flipkart...";
  summary.classList.add("hidden");
  showSkeletons();

  try {
    const res  = await fetch(`${API}/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();

    if (!res.ok || data.error) {
      status.className   = "status error";
      status.textContent = `❌ ${data.error || "Something went wrong. Try again."}`;
      results.innerHTML  = "";
      return;
    }

    // Render cards
    results.innerHTML = data.results.map(renderCard).join("");

    // Summary bar
    const sources = [...new Set(data.results.map(r => r.source))].join(" & ");
    const best    = data.results.find(r => r.best_deal);
    summary.classList.remove("hidden");
    document.getElementById("summaryText").innerHTML =
      `Found <strong>${data.total} results</strong> from ${sources}` +
      (best ? ` · Best deal: <strong>${best.price}</strong> on ${best.source}` : "");

    status.classList.add("hidden");

  } catch (err) {
    status.className   = "status error";
    status.textContent = "❌ Cannot connect to backend. Make sure python app.py is running.";
    results.innerHTML  = "";
  } finally {
    btn.disabled    = false;
    btn.textContent = "Search";
  }
}
