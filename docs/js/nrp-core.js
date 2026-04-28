/* Neural Report — optional GA4 (no-op until GA_MEASUREMENT_ID is set) */
(function () {
  var GA_MEASUREMENT_ID = "";

  if (!GA_MEASUREMENT_ID || GA_MEASUREMENT_ID.indexOf("XXXX") !== -1) {
    return;
  }

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA_MEASUREMENT_ID);

  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA_MEASUREMENT_ID);
  document.head.appendChild(s);
})();
/* Keep GA block above separate from link hardening below. */

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    try {
      var u = new URL(a.href);
      if (u.origin !== window.location.origin) {
        var parts = (a.getAttribute("rel") || "").split(/\s+/).filter(Boolean);
        ["noopener", "noreferrer"].forEach(function (r) {
          if (parts.indexOf(r) === -1) {
            parts.push(r);
          }
        });
        a.setAttribute("rel", parts.join(" "));
      }
    } catch (e) {
      /* ignore invalid URLs */
    }
  });

  var archiveSearch = document.getElementById("archive-search");
  var archiveTag = document.getElementById("archive-tag-filter");
  var archiveRows = Array.prototype.slice.call(document.querySelectorAll("#archive-table tbody tr.archive-row"));
  var archiveSummary = document.getElementById("archive-results-summary");
  if (archiveRows.length > 0 && archiveSummary) {
    var applyArchiveFilters = function () {
      var q = (archiveSearch && archiveSearch.value ? archiveSearch.value : "").trim().toLowerCase();
      var tag = (archiveTag && archiveTag.value ? archiveTag.value : "").trim().toLowerCase();
      var visible = 0;
      archiveRows.forEach(function (row) {
        var title = (row.getAttribute("data-title") || "").toLowerCase();
        var tags = (row.getAttribute("data-tags") || "").toLowerCase();
        var matchesQ = !q || title.indexOf(q) !== -1 || tags.indexOf(q) !== -1;
        var matchesTag = !tag || tags.indexOf(tag) !== -1;
        var show = matchesQ && matchesTag;
        row.style.display = show ? "" : "none";
        if (show) visible += 1;
      });
      archiveSummary.textContent = "Showing " + visible + " brief" + (visible === 1 ? "" : "s") + ".";
    };
    if (archiveSearch) archiveSearch.addEventListener("input", applyArchiveFilters);
    if (archiveTag) archiveTag.addEventListener("change", applyArchiveFilters);
    applyArchiveFilters();
  }
});
