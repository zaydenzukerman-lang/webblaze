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

  // Prefill the quote form's "project" field from a picker click or ?job= query param
  function prefill(text) {
    var field = document.getElementById("job-field");
    if (!field) return;
    field.value = text;
    var form = document.getElementById("quote");
    if (form) form.scrollIntoView({ behavior: "smooth", block: "start" });
    field.classList.remove("flash"); void field.offsetWidth; field.classList.add("flash");
    setTimeout(function () { try { field.focus({ preventScroll: true }); } catch (e) { field.focus(); } }, 450);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".js-pick");
    if (!b) return;
    // Only hijack the click if the quote form already lives on this page;
    // otherwise let the link navigate to contact/?job=...#quote normally.
    if (document.getElementById("job-field")) {
      e.preventDefault();
      prefill(b.getAttribute("data-job"));
    }
  });
  var qs = new URLSearchParams(location.search);
  if (qs.get("job") && document.getElementById("job-field")) {
    prefill(qs.get("job"));
  }
})();
