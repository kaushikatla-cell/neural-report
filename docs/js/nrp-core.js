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
  var copyText = function (text, cb) {
    if (!text) {
      cb(false);
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () {
          cb(true);
        },
        function () {
          cb(false);
        }
      );
      return;
    }
    try {
      var ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      cb(true);
    } catch (e) {
      cb(false);
    }
  };

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

  if (briefContent) {
    var canonicalEl = document.querySelector('link[rel="canonical"]');
    var canonical = canonicalEl ? canonicalEl.href : window.location.href;
    var titleEl = document.querySelector('meta[property="og:title"]');
    var title = titleEl ? titleEl.getAttribute("content") : document.title;
    var ldScript = document.querySelector('script[type="application/ld+json"]');
    var dateIso = "";
    if (ldScript) {
      try {
        var ld = JSON.parse(ldScript.textContent || "{}");
        dateIso = ld.datePublished || "";
      } catch (e) {
        dateIso = "";
      }
    }
    var d = dateIso ? new Date(dateIso + "T00:00:00Z") : new Date();
    var y = d.getUTCFullYear();
    var m = d.toLocaleString("en-US", { month: "long", timeZone: "UTC" });
    var mShort = d.toLocaleString("en-US", { month: "short", timeZone: "UTC" });
    var day = String(d.getUTCDate()).padStart(2, "0");
    var mm = String(d.getUTCMonth() + 1).padStart(2, "0");
    var slug = canonical.split("/").pop().replace(".html", "");

    var citationDefault =
      'Neural Report, "' +
      title +
      '," NRP Evidence Brief, ' +
      (dateIso || "") +
      ", " +
      canonical +
      ".";
    var citationAPA = "Neural Report. (" + y + ", " + m + " " + day + "). " + title + ". " + canonical;
    var citationMLA = '"' + title + '." Neural Report, ' + day + " " + mShort + " " + y + ", " + canonical + ".";
    var citationBib =
      "@misc{" +
      slug.replace(/[^a-zA-Z0-9_-]/g, "") +
      ",\n" +
      '  author = "{Neural Report}",\n' +
      '  title = "{' +
      title.replace(/[{}]/g, "") +
      '}",\n' +
      "  year = {" +
      y +
      "},\n" +
      "  month = {" +
      mm +
      "},\n" +
      '  howpublished = "{\\url{' +
      canonical +
      '}}",\n' +
      '  note = "{NRP Evidence Brief}"\n' +
      "}";

    var wireCopyButton = function (id, text) {
      var btn = document.getElementById(id);
      if (!btn) return;
      btn.addEventListener("click", function () {
        var original = btn.textContent;
        copyText(text, function (ok) {
          btn.textContent = ok ? "Copied" : "Copy failed";
          window.setTimeout(function () {
            btn.textContent = original;
          }, 1400);
        });
      });
    };

    wireCopyButton("copy-citation", citationDefault);
    wireCopyButton("copy-citation-apa", citationAPA);
    wireCopyButton("copy-citation-mla", citationMLA);

    var densityBtns = [
      document.getElementById("reader-density-default"),
      document.getElementById("reader-density-compact"),
      document.getElementById("reader-density-spacious"),
    ].filter(Boolean);
    var setDensity = function (mode) {
      document.body.classList.remove("reader-compact", "reader-spacious");
      if (mode === "compact") document.body.classList.add("reader-compact");
      if (mode === "spacious") document.body.classList.add("reader-spacious");
      try {
        localStorage.setItem("nrp_reader_density", mode || "default");
      } catch (e) {}
      densityBtns.forEach(function (b) {
        b.classList.toggle("is-active", b.getAttribute("data-density-mode") === (mode || "default"));
      });
    };
    var storedDensity = "default";
    try {
      storedDensity = localStorage.getItem("nrp_reader_density") || "default";
    } catch (e) {}
    setDensity(storedDensity);
    densityBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        setDensity(b.getAttribute("data-density-mode") || "default");
      });
    });

    var bibBtn = document.getElementById("download-citation-bib");
    if (bibBtn) {
      bibBtn.addEventListener("click", function () {
        var blob = new Blob([citationBib], { type: "text/plain;charset=utf-8" });
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = slug + ".bib";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    var printBtn = document.getElementById("print-brief");
    if (printBtn) {
      printBtn.addEventListener("click", function () {
        window.print();
      });
    }

    var progress = document.createElement("div");
    progress.className = "reading-progress no-print";
    progress.innerHTML = "<span></span>";
    document.body.appendChild(progress);
    var progressFill = progress.querySelector("span");
    var updateProgress = function () {
      var rect = briefContent.getBoundingClientRect();
      var full = briefContent.scrollHeight - window.innerHeight;
      var scrolled = window.scrollY - (window.scrollY + rect.top);
      var pct = full > 0 ? Math.max(0, Math.min(1, scrolled / full)) : 0;
      progressFill.style.width = String(Math.round(pct * 100)) + "%";
    };
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
    updateProgress();

    var sourcesHeading = Array.prototype.slice
      .call(briefContent.querySelectorAll("h2"))
      .find(function (h) {
        return (h.textContent || "").trim().toLowerCase().indexOf("sources") === 0;
      });
    if (sourcesHeading) {
      var tooltip = document.createElement("div");
      tooltip.className = "source-preview-tooltip";
      document.body.appendChild(tooltip);
      var links = [];
      var node = sourcesHeading.nextElementSibling;
      while (node && node.tagName !== "H2") {
        if (node.querySelectorAll) {
          links = links.concat(Array.prototype.slice.call(node.querySelectorAll('a[href^="http"]')));
        }
        node = node.nextElementSibling;
      }
      links.forEach(function (a) {
        var href = a.getAttribute("href") || "";
        var host = "";
        try {
          host = new URL(href).hostname.replace(/^www\./, "");
        } catch (e) {
          host = "";
        }
        var preview = (a.textContent || "External source").trim();
        var badge = document.createElement("span");
        badge.className = "source-badge";
        if (
          /(\.|^)(gov|edu)$/i.test(host) ||
          host.indexOf("imf.org") !== -1 ||
          host.indexOf("oecd.org") !== -1 ||
          host.indexOf("federalreserve.gov") !== -1 ||
          host.indexOf("bls.gov") !== -1 ||
          host.indexOf("iea.org") !== -1
        ) {
          badge.classList.add("source-badge-high");
          badge.textContent = "primary";
        } else if (host.indexOf("nber.org") !== -1 || host.indexOf("arxiv.org") !== -1 || host.indexOf("stanford.edu") !== -1) {
          badge.classList.add("source-badge-medium");
          badge.textContent = "research";
        } else {
          badge.classList.add("source-badge-reference");
          badge.textContent = "reference";
        }
        a.insertAdjacentElement("afterend", badge);
        a.addEventListener("mouseenter", function () {
          tooltip.textContent = preview + (host ? " — " + host : "");
          tooltip.classList.add("show");
        });
        a.addEventListener("mousemove", function (ev) {
          tooltip.style.left = ev.clientX + 14 + "px";
          tooltip.style.top = ev.clientY + 14 + "px";
        });
        a.addEventListener("mouseleave", function () {
          tooltip.classList.remove("show");
        });
      });
    }

    var gPressedAt = 0;
    window.addEventListener("keydown", function (ev) {
      if (ev.defaultPrevented || ev.metaKey || ev.ctrlKey || ev.altKey) return;
      var tag = (ev.target && ev.target.tagName) || "";
      if (/INPUT|TEXTAREA|SELECT/.test(tag) || (ev.target && ev.target.isContentEditable)) return;
      var key = (ev.key || "").toLowerCase();
      if (key === "j") {
        window.scrollBy({ top: 110, behavior: "smooth" });
      } else if (key === "k") {
        window.scrollBy({ top: -110, behavior: "smooth" });
      } else if (key === "g") {
        var now = Date.now();
        if (now - gPressedAt < 450) {
          window.scrollTo({ top: 0, behavior: "smooth" });
          gPressedAt = 0;
        } else {
          gPressedAt = now;
        }
      } else if (key === "s") {
        if (Date.now() - gPressedAt < 800) {
          window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
          gPressedAt = 0;
        }
      }
    });
  }
});
