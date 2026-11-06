(function () {
  "use strict";

  // Mobile menu
  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Preview-only forms
  document.querySelectorAll(".js-preview-form").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = f.querySelector(".form-msg");
      if (msg) msg.textContent = "Thanks! This is a design preview, so nothing was sent.";
    });
  });

  // Prefill the request form with a product and scroll to it
  function prefill(text) {
    var field = document.getElementById("product-field");
    if (!field) return;
    field.value = text;
    var form = document.getElementById("request");
    if (form) form.scrollIntoView({ behavior: "smooth", block: "start" });
    field.classList.remove("flash"); void field.offsetWidth; field.classList.add("flash");
    setTimeout(function () { try { field.focus({ preventScroll: true }); } catch (e) { field.focus(); } }, 450);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".js-req");
    if (b) { e.preventDefault(); prefill(b.getAttribute("data-product")); }
  });
  var qs = new URLSearchParams(location.search);
  if (qs.get("product") && document.getElementById("product-field")) {
    document.getElementById("product-field").value = qs.get("product");
  }

  function setChip(group, attr, value) {
    group.querySelectorAll(".chip").forEach(function (c) {
      var on = c.getAttribute(attr) === value;
      c.classList.toggle("is-on", on);
      c.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  // Product finder
  var grid = document.getElementById("mfr-grid");
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".mfr"));
    var search = document.getElementById("mfr-search");
    var chips = document.querySelector(".finder .chips");
    var count = document.getElementById("mfr-count");
    var empty = document.getElementById("mfr-empty");
    var cat = qs.get("cat") || "all";
    if (!chips.querySelector('[data-cat="' + cat + '"]')) cat = "all";
    var apply = function () {
      var q = search.value.trim().toLowerCase(), n = 0;
      var words = q.split(/\s+/).filter(Boolean);
      cards.forEach(function (c) {
        var okCat = cat === "all" || (" " + c.getAttribute("data-cats") + " ").indexOf(" " + cat + " ") > -1;
        var s = c.getAttribute("data-search");
        var okQ = words.every(function (w) { return s.indexOf(w) > -1; });
        var show = okCat && okQ;
        c.hidden = !show;
        if (show) n++;
      });
      count.textContent = n;
      empty.hidden = n !== 0;
    };
    chips.addEventListener("click", function (e) {
      var c = e.target.closest(".chip"); if (!c) return;
      cat = c.getAttribute("data-cat"); setChip(chips, "data-cat", cat); apply();
      var u = new URL(location.href);
      if (cat === "all") u.searchParams.delete("cat"); else u.searchParams.set("cat", cat);
      history.replaceState(null, "", u);
    });
    search.addEventListener("input", apply);
    setChip(chips, "data-cat", cat);
    apply();
  }

  // Inventory search
  var body = document.getElementById("inv-body");
  if (body) {
    var start = function () {
      var rows = window.STOCK || [];
      var s = document.getElementById("inv-search");
      var ichips = document.querySelector(".finder .chips");
      var inStock = document.getElementById("inv-instock");
      var cnt = document.getElementById("inv-count");
      var more = document.getElementById("inv-more");
      var icat = "all", limit = 60, list = [];
      var esc = function (t) { return String(t).replace(/[&<>"]/g, function (m) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]; }); };
      var render = function () {
        var html = "";
        list.slice(0, limit).forEach(function (r) {
          html += "<tr><td class=\"c-cat\">" + esc(r[0]) + "</td><td class=\"c-style\">" + esc(r[1]) + "</td><td class=\"pid\">" + esc(r[2]) +
            "</td><td class=\"c-desc\">" + esc(r[3]) + "</td><td class=\"num\">" + esc(r[4]) +
            "</td><td class=\"c-req\"><button class=\"js-req\" data-product=\"" + esc("Stock item " + r[2]) + "\">Ask</button></td></tr>";
        });
        body.innerHTML = html || "<tr><td colspan=\"6\">No items match. Try a different size or ID, or ask us below.</td></tr>";
        cnt.textContent = list.length;
        more.hidden = list.length <= limit;
      };
      var apply = function () {
        var words = s.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
        list = rows.filter(function (r) {
          if (icat !== "all" && r[0] !== icat) return false;
          if (inStock.checked && !(parseFloat(r[4]) > 0)) return false;
          var hay = (r.join(" ")).toLowerCase();
          return words.every(function (w) { return hay.indexOf(w) > -1; });
        });
        limit = 60; render();
      };
      ichips.addEventListener("click", function (e) {
        var c = e.target.closest(".chip"); if (!c) return;
        icat = c.getAttribute("data-icat"); setChip(ichips, "data-icat", icat); apply();
      });
      s.addEventListener("input", apply);
      inStock.addEventListener("change", apply);
      more.addEventListener("click", function () { limit += 120; render(); });
      apply();
    };
    if (window.STOCK) start(); else window.addEventListener("load", start);
  }
})();
