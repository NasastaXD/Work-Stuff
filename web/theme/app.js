// Render de gráficos radar + buscador en cliente para el Códice de Hierométrica.
(function () {
  // ---------- Gráficos ----------
  function renderCharts() {
    if (typeof Chart === "undefined") return;
    document.querySelectorAll("canvas[data-chart]").forEach(function (cv) {
      var cfg;
      try { cfg = JSON.parse(cv.getAttribute("data-chart")); } catch (e) { return; }
      var ds = (cfg.datasets || []).map(function (d) {
        return {
          label: d.label || "",
          data: d.data || [],
          fill: cfg.fill !== false,
          backgroundColor: "rgba(163,113,247,0.30)",
          borderColor: "#a371f7",
          borderWidth: 2,
          pointBackgroundColor: "#a371f7",
          pointRadius: 3
        };
      });
      var maxVal = 0;
      ds.forEach(function (d) { d.data.forEach(function (v) { if (+v > maxVal) maxVal = +v; }); });
      var top = maxVal > 10 ? 20 : (maxVal > 5 ? 10 : 5);
      new Chart(cv, {
        type: cfg.type || "radar",
        data: { labels: cfg.labels || [], datasets: ds },
        options: {
          responsive: true,
          animation: false,
          scales: {
            r: {
              min: 0, max: top,
              ticks: { display: false, backdropColor: "transparent" },
              grid: { color: "rgba(255,255,255,0.14)" },
              angleLines: { color: "rgba(255,255,255,0.14)" },
              pointLabels: { color: "#dcdde1", font: { size: 13 } }
            }
          },
          plugins: { legend: { display: ds.length > 1 } }
        }
      });
    });
  }

  // ---------- Buscador ----------
  function setupSearch() {
    var input = document.getElementById("search");
    var box = document.getElementById("search-results");
    if (!input || !box || !window.SEARCH_INDEX) return;

    function norm(s) {
      return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    }
    var docs = window.SEARCH_INDEX.map(function (d) {
      return { d: d, hay: norm(d.t + " " + (d.s || "") + " " + (d.x || "")) };
    });

    input.addEventListener("input", function () {
      var q = norm(input.value.trim());
      if (q.length < 2) { box.style.display = "none"; box.innerHTML = ""; return; }
      var terms = q.split(/\s+/);
      var hits = docs.filter(function (e) {
        return terms.every(function (t) { return e.hay.indexOf(t) !== -1; });
      }).slice(0, 12);
      if (!hits.length) {
        box.innerHTML = '<a><span class="sr-section">Sin resultados</span></a>';
      } else {
        box.innerHTML = hits.map(function (e) {
          return '<a href="' + e.d.u + '">' + e.d.t +
                 '<br><span class="sr-section">' + (e.d.s || "") + "</span></a>";
        }).join("");
      }
      box.style.display = "block";
    });

    document.addEventListener("click", function (ev) {
      if (!ev.target.closest(".search-box")) { box.style.display = "none"; }
    });
  }

  // ---------- Menú móvil ----------
  function setupMenu() {
    var btn = document.getElementById("menu-toggle");
    var sb = document.getElementById("sidebar");
    if (btn && sb) btn.addEventListener("click", function () { sb.classList.toggle("open"); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderCharts();
    setupSearch();
    setupMenu();
  });
})();
