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

  var librarySearch = document.getElementById("library-search");
  var librarySummary = document.getElementById("library-summary");
  var libraryCards = Array.prototype.slice.call(document.querySelectorAll("#library-grid .paper-card"));
  var domainButtons = Array.prototype.slice.call(document.querySelectorAll("[data-library-domain]"));
  if (libraryCards.length > 0 && librarySummary) {
    var activeDomain = "";
    var updateDomainButtons = function () {
      domainButtons.forEach(function (btn) {
        var d = (btn.getAttribute("data-library-domain") || "").toLowerCase();
        var on = d === activeDomain;
        btn.classList.toggle("is-active", on);
      });
    };
    var applyLibraryFilters = function () {
      var q = (librarySearch && librarySearch.value ? librarySearch.value : "").trim().toLowerCase();
      var visible = 0;
      libraryCards.forEach(function (card) {
        var title = (card.getAttribute("data-title") || "").toLowerCase();
        var dom = (card.getAttribute("data-domain") || "").toLowerCase();
        var text = (card.textContent || "").toLowerCase();
        var matchesQ = !q || title.indexOf(q) !== -1 || text.indexOf(q) !== -1;
        var matchesD = !activeDomain || dom === activeDomain;
        var show = matchesQ && matchesD;
        card.style.display = show ? "" : "none";
        if (show) visible += 1;
      });
      librarySummary.textContent = "Showing " + visible + " source" + (visible === 1 ? "" : "s") + ".";
      updateDomainButtons();
    };
    if (librarySearch) librarySearch.addEventListener("input", applyLibraryFilters);
    domainButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activeDomain = (btn.getAttribute("data-library-domain") || "").toLowerCase();
        applyLibraryFilters();
      });
    });
    applyLibraryFilters();
  }

  var briefContent = document.querySelector(".brief-content");
  var briefToc = document.querySelector(".brief-toc");
  if (briefContent && briefToc) {
    var h2s = Array.prototype.slice.call(briefContent.querySelectorAll("h2"));
    var norm = function (s) {
      return (s || "")
        .toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .trim()
        .replace(/\s+/g, "-");
    };
    h2s.forEach(function (h) {
      var txt = (h.textContent || "").trim().toLowerCase();
      if (txt.indexOf("tl;dr") === 0 || txt.indexOf("tl") === 0) {
        h.id = "tldr";
      } else if (txt.indexOf("claims and evidence") === 0) {
        h.id = "claims-and-evidence";
      } else if (txt.indexOf("still uncertain because") === 0) {
        h.id = "still-uncertain-because";
      } else if (txt.indexOf("sources") === 0) {
        h.id = "sources";
      } else if (!h.id) {
        h.id = norm(h.textContent);
      }
    });
    var tocLinks = Array.prototype.slice.call(briefToc.querySelectorAll("a[href^='#']"));
    var byId = {};
    tocLinks.forEach(function (a) {
      var id = (a.getAttribute("href") || "").replace(/^#/, "");
      if (id) byId[id] = a;
    });
    var activate = function () {
      var y = window.scrollY + 120;
      var current = "";
      h2s.forEach(function (h) {
        if (h.offsetTop <= y) current = h.id;
      });
      tocLinks.forEach(function (a) {
        a.classList.toggle("active", a === byId[current]);
      });
    };
    window.addEventListener("scroll", activate, { passive: true });
    activate();
  }

  var copyCitationBtn = document.getElementById("copy-citation");
  if (copyCitationBtn) {
    copyCitationBtn.addEventListener("click", function () {
      var text = copyCitationBtn.getAttribute("data-citation") || "";
      var finish = function (ok) {
        copyCitationBtn.textContent = ok ? "Citation copied" : "Copy failed";
        window.setTimeout(function () {
          copyCitationBtn.textContent = "Copy citation";
        }, 1600);
      };
      if (!text) {
        finish(false);
        return;
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () {
            finish(true);
          },
          function () {
            finish(false);
          }
        );
      } else {
        try {
          var ta = document.createElement("textarea");
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          document.body.removeChild(ta);
          finish(true);
        } catch (e) {
          finish(false);
        }
      }
    });
  }
});
