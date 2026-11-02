(function () {
  var D = window.ORANA || {};
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* WhatsApp links: <a data-wa="message"> */
  document.querySelectorAll("[data-wa]").forEach(function (a) {
    a.href = "https://wa.me/" + D.whatsapp + "?text=" + encodeURIComponent(a.getAttribute("data-wa"));
    a.target = "_blank";
    a.rel = "noopener";
  });

  /* Blur-in words */
  document.querySelectorAll("[data-bw]").forEach(function (el) {
    var html = el.innerHTML.split(/(<[^>]+>)/g).map(function (part) {
      if (part.charAt(0) === "<") return part;
      return part.replace(/(\S+)/g, '<span class="bw">$1</span>');
    }).join("");
    el.innerHTML = html;
    el.querySelectorAll(".bw").forEach(function (w, i) { w.style.transitionDelay = (i * 0.09) + "s"; });
  });

  /* Reveal on scroll */
  var targets = document.querySelectorAll(".rv,[data-bw]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -6% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("in"); });
  }

  /* Next Saturday (Ecuador time) */
  var S = D.saturday || {};
  var dateEl = document.getElementById("sat-date");
  if (dateEl) {
    var d;
    if (S.dateOverride) {
      var p = S.dateOverride.split("-");
      d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2], 12));
    } else {
      var parts = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Guayaquil", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date()).split("-");
      d = new Date(Date.UTC(+parts[0], +parts[1] - 1, +parts[2], 12));
      var add = (6 - d.getUTCDay() + 7) % 7;
      d.setUTCDate(d.getUTCDate() + add);
    }
    var label = new Intl.DateTimeFormat("es-EC", { timeZone: "UTC", weekday: "long", day: "numeric", month: "long" }).format(d);
    label = label.charAt(0).toUpperCase() + label.slice(1);
    dateEl.textContent = label;
    var cls = document.getElementById("sat-class");
    if (cls) cls.textContent = S.classTitle || "Clase especial de sábado";
    var tm = document.getElementById("sat-time");
    if (tm) tm.textContent = S.time || "08H00";
    document.querySelectorAll("[data-sat-wa]").forEach(function (a) {
      var msg = "Hola Orana, quiero reservar la clase del " + label + " a las " + (S.time || "08H00") + ".";
      a.href = "https://wa.me/" + D.whatsapp + "?text=" + encodeURIComponent(msg);
      a.target = "_blank"; a.rel = "noopener";
    });
  }

  /* Pricing tabs */
  var tabs = document.querySelectorAll(".tab");
  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (x) { x.setAttribute("aria-selected", x === t ? "true" : "false"); });
      document.querySelectorAll(".panel").forEach(function (p) { p.hidden = p.id !== t.getAttribute("aria-controls"); });
    });
  });


  /* Membership cards: scroll-driven movement + pointer tilt */
  var wraps = [].slice.call(document.querySelectorAll(".cwrap"));
  var ticking = false;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function updateCards() {
    ticking = false;
    var vh = window.innerHeight;
    wraps.forEach(function (w, i) {
      if (!w.offsetParent) return;
      var r = w.getBoundingClientRect();
      var p = clamp((vh - r.top) / (vh + r.height), 0, 1);   // 0 = entering, .5 = centered, 1 = leaving
      var d = 0.5 - p;
      var k = 1 + (i % 4) * 0.35;                            // each card moves at a different speed
      w.style.setProperty("--ty", (d * 70 * k).toFixed(1) + "px");
      w.style.setProperty("--rx", (d * 24).toFixed(2) + "deg");
      w.style.setProperty("--rz", (d * (i % 2 ? 7 : -7)).toFixed(2) + "deg");
    });
  }
  function requestUpdate() { if (!ticking) { ticking = true; requestAnimationFrame(updateCards); } }
  if (wraps.length && !reduce) {
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
    document.querySelectorAll(".tab").forEach(function (t) { t.addEventListener("click", function () { setTimeout(requestUpdate, 30); }); });
    requestUpdate();
    if (window.matchMedia("(hover:hover)").matches) {
      document.querySelectorAll(".card").forEach(function (card) {
        var cc = card.querySelector(".ccard");
        if (!cc) return;
        card.addEventListener("pointermove", function (e) {
          var r = cc.getBoundingClientRect();
          var x = clamp((e.clientX - r.left) / r.width, 0, 1), y = clamp((e.clientY - r.top) / r.height, 0, 1);
          cc.style.setProperty("--hy", ((x - 0.5) * 18).toFixed(2) + "deg");
          cc.style.setProperty("--hx", ((0.5 - y) * 14).toFixed(2) + "deg");
          cc.style.setProperty("--gx", (x * 100).toFixed(0) + "%");
          cc.style.setProperty("--gy", (y * 100).toFixed(0) + "%");
        });
        card.addEventListener("pointerleave", function () {
          cc.style.setProperty("--hy", "0deg"); cc.style.setProperty("--hx", "0deg");
        });
      });
    }
  }

  /* Sticky mobile CTA after hero */
  var sticky = document.getElementById("sticky");
  var hero = document.querySelector(".hero");
  if (sticky && hero && "IntersectionObserver" in window) {
    new IntersectionObserver(function (e) {
      sticky.classList.toggle("show", !e[0].isIntersecting);
    }, { threshold: 0.05 }).observe(hero);
  }

  /* Cursor glow (desktop pointer only) */
  var glow = document.querySelector(".glow");
  if (glow && !reduce && window.matchMedia("(hover:hover)").matches) {
    window.addEventListener("pointermove", function (e) {
      glow.style.opacity = 1;
      glow.style.left = e.clientX + "px";
      glow.style.top = e.clientY + "px";
    }, { passive: true });
  }

  var y = document.getElementById("yr");
  if (y) y.textContent = new Date().getFullYear();
})();
