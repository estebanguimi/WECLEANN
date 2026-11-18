/* RECORTE — interacción. Letras recortadas que caen y se arrastran, fotos sueltas con paralaje,
   máquina de escribir, sellos que golpean el papel, hoja rasgada entre páginas, cinta con velocidad de scroll. */
(function () {
  "use strict";
  var G = window.gsap, ST = window.ScrollTrigger;
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var tactil = window.matchMedia("(hover: none)").matches;
  if (G && ST) G.registerPlugin(ST);

  var lenis = null;
  if (window.Lenis && !reducido) {
    lenis = new Lenis({ lerp: .1, smoothWheel: true });
    if (ST) lenis.on("scroll", ST.update);
    if (G) { G.ticker.add(function (t) { lenis.raf(t * 1000); }); G.ticker.lagSmoothing(0); }
  }

  /* menú, cabecera, copiar */
  var menu = document.querySelector("[data-menu]"), nav = document.querySelector("[data-nav]");
  if (menu) menu.addEventListener("click", function () { var a = nav.classList.toggle("abierto"); menu.setAttribute("aria-expanded", a ? "true" : "false"); });
  var cab = document.querySelector("[data-cab]"), yUlt = 0;
  window.addEventListener("scroll", function () {
    var y = window.scrollY; if (cab && !(nav && nav.classList.contains("abierto"))) cab.classList.toggle("oculta", y > yUlt && y > 260); yUlt = y;
  }, { passive: true });
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var av = b.querySelector("[data-copiado]"), t = b.getAttribute("data-copiar");
      var ok = function () { if (av) { var o = av.textContent; av.textContent = "copied!"; setTimeout(function () { av.textContent = o; }, 1500); } };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
    });
  });
  document.querySelectorAll(".cv-correo").forEach(function (b) {
    b.addEventListener("click", function () { var t = b.textContent; b.textContent = "Email copied!"; setTimeout(function () { b.textContent = t; }, 1600); });
  });

  /* ---------------- hoja rasgada entre páginas ---------------- */
  var hoja = document.querySelector("[data-hoja]"), hojaTxt = document.querySelector("[data-hoja-txt]");
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[href]");
    if (!a || ev.defaultPrevented || ev.metaKey || ev.ctrlKey || ev.shiftKey || a.target === "_blank" || a.hasAttribute("download")) return;
    var h = a.getAttribute("href");
    if (!/\.html(#.*)?$/.test(h) || /^https?:/.test(h)) return;
    if (a.closest("[data-flot]") && arrastreFlot) { ev.preventDefault(); return; }
    ev.preventDefault();
    if (reducido || !G || !hoja) { location.href = h; return; }
    var nombre = (a.querySelector("b") || a).textContent.trim().split("\n")[0].slice(0, 28);
    hojaTxt.textContent = nombre.length > 2 ? nombre : "";
    try { sessionStorage.setItem("recorte-t", "1"); } catch (e) {}
    G.set(hoja, { visibility: "visible" });
    G.fromTo(hoja, { yPercent: 105, rotation: 2 }, { yPercent: 0, rotation: 0, duration: .65, ease: "expo.inOut", onComplete: function () { location.href = h; } });
  });
  var vino = false;
  try { vino = sessionStorage.getItem("recorte-t") === "1"; sessionStorage.removeItem("recorte-t"); } catch (e) {}
  if (hoja && G && vino && !reducido) {
    G.set(hoja, { yPercent: 0, visibility: "visible" });
    G.to(hoja, { yPercent: -110, rotation: -2, duration: .8, ease: "expo.inOut", delay: .05, onComplete: function () { G.set(hoja, { yPercent: 105, rotation: 0, visibility: "hidden" }); } });
  }
  window.addEventListener("pageshow", function (e) { if (e.persisted && hoja && G) G.set(hoja, { yPercent: 105, visibility: "hidden" }); });
  var retraso = vino ? .45 : .1;

  /* ---------------- letras recortadas: caen al cargar ---------------- */
  if (G && !reducido) {
    document.querySelectorAll(".hero-t, .pag-cab h1, .p-cab h1").forEach(function (h) {
      var ls = h.querySelectorAll("[data-letra]");
      G.from(ls, { y: function () { return -120 - Math.random() * 160; }, rotation: function () { return (Math.random() - .5) * 70; }, opacity: 0,
        duration: .9, ease: "bounce.out", stagger: { each: .045, from: "random" }, delay: retraso, clearProps: "transform,opacity" });
    });
  }

  /* letras del hero: se pueden arrastrar */
  var heroT = document.querySelector(".hero-t");
  if (heroT && !tactil) {
    heroT.querySelectorAll("[data-letra]").forEach(function (l) {
      var dx = 0, dy = 0, ini = null;
      l.addEventListener("pointerdown", function (ev) {
        ev.preventDefault(); l.setPointerCapture(ev.pointerId); l.classList.add("arrastrando");
        ini = { x: ev.clientX - dx, y: ev.clientY - dy };
      });
      l.addEventListener("pointermove", function (ev) {
        if (!ini) return;
        var nx = ev.clientX - ini.x, ny = ev.clientY - ini.y, giroV = (nx - dx) * .8;
        dx = nx; dy = ny;
        l.style.transform = "translate(" + dx + "px," + dy + "px) rotate(calc(var(--r) + " + Math.max(-25, Math.min(25, giroV)) + "deg))";
      });
      var soltar = function () {
        if (!ini) return; ini = null; l.classList.remove("arrastrando");
        l.style.transform = "translate(" + dx + "px," + dy + "px) rotate(var(--r))";
      };
      l.addEventListener("pointerup", soltar); l.addEventListener("pointercancel", soltar);
    });
  }

  /* fotos sueltas: paralaje con el cursor y con el scroll */
  var arrastreFlot = false;
  var flots = document.querySelectorAll("[data-flot]");
  if (flots.length && G && !reducido) {
    G.from(flots, { y: 80, opacity: 0, rotation: function () { return (Math.random() - .5) * 30; }, duration: 1.2, ease: "expo.out", stagger: .08, delay: retraso + .3 });
    if (!tactil) {
      var qs = Array.prototype.map.call(flots, function (f, i) {
        return { x: G.quickTo(f, "x", { duration: 1, ease: "power3" }), y: G.quickTo(f, "y", { duration: 1, ease: "power3" }), k: (i % 3 + 1) * 10 };
      });
      window.addEventListener("pointermove", function (ev) {
        var nx = ev.clientX / innerWidth - .5, ny = ev.clientY / innerHeight - .5;
        qs.forEach(function (q) { q.x(-nx * q.k * 2); q.y(-ny * q.k * 2); });
      });
    }
    if (ST) flots.forEach(function (f, i) {
      G.to(f, { yPercent: -30 - i * 12, ease: "none", scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true } });
    });
  }

  /* máquina de escribir */
  document.querySelectorAll("[data-maquina]").forEach(function (el) {
    if (reducido) return;
    var txt = el.textContent; el.textContent = ""; el.style.minHeight = "1.6em";
    var i = 0;
    setTimeout(function esc() { el.textContent = txt.slice(0, ++i) + (i < txt.length ? "▌" : ""); if (i < txt.length) setTimeout(esc, 28 + Math.random() * 40); }, (retraso + .8) * 1000);
  });

  /* cinta: avanza más rápido cuanto más rápido se hace scroll */
  document.querySelectorAll("[data-cinta]").forEach(function (c) {
    if (reducido || !G) return;
    var x = 0, vel = 0, w = c.scrollWidth / 2, ult = window.scrollY;
    G.ticker.add(function () {
      var y = window.scrollY; vel += ((y - ult) * .3 - vel) * .1; ult = y;
      x -= .9 + Math.abs(vel); if (-x >= w) x += w; c.style.transform = "translate3d(" + x + "px,0,0)";
    });
    window.addEventListener("resize", function () { w = c.scrollWidth / 2; });
  });

  if (G && ST && !reducido) {
    /* piezas que se pegan al llegar */
    document.querySelectorAll(".pz, .gz, .serv, .p-portada, .ficha, .polaroid, .hoja-maq, .hoja-cv, .sobre-carta, .video-p").forEach(function (el) {
      G.from(el, { y: 70, rotation: "+=6", opacity: 0, duration: 1, ease: "expo.out", scrollTrigger: { trigger: el, start: "top 92%", once: true } });
    });
    /* sellos que golpean */
    document.querySelectorAll("[data-sello], .cv-cifra").forEach(function (s, i) {
      G.timeline({ scrollTrigger: { trigger: s, start: "top 86%", once: true }, delay: (i % 4) * .12 })
        .from(s, { scale: 2.6, opacity: 0, rotation: "+=18", duration: .22, ease: "power4.in" })
        .to(s, { x: 3, duration: .05, yoyo: true, repeat: 3, ease: "none" })
        .set(s, { x: 0 });
    });
    /* recorrido mecanografiado línea por línea */
    document.querySelectorAll(".recorrido li").forEach(function (li, i) {
      G.from(li, { clipPath: "inset(0 100% 0 0)", duration: .9, ease: "steps(22)", scrollTrigger: { trigger: li, start: "top 90%", once: true }, delay: i * .08 });
    });
  }

  /* filtros del archivo */
  var muro = document.querySelector("[data-muro]");
  if (muro) document.querySelectorAll("[data-filtro]").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filtro");
      document.querySelectorAll("[data-filtro]").forEach(function (x) { x.classList.toggle("activo", x === b); x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var items = muro.querySelectorAll(".pz");
      var st = window.Flip && !reducido ? Flip.getState(items) : null;
      items.forEach(function (it) { it.classList.toggle("oculto", f !== "todo" && it.getAttribute("data-cat") !== f); });
      if (st) Flip.from(st, { duration: .7, ease: "expo.inOut", absolute: true, onEnter: function (els) { return G.fromTo(els, { opacity: 0, y: -60, rotation: 12 }, { opacity: 1, y: 0, rotation: 0, duration: .6, ease: "back.out(1.6)", clearProps: "transform" }); }, onLeave: function (els) { return G.to(els, { opacity: 0, y: 40, duration: .3 }); } });
      if (ST) ST.refresh();
    });
  });

  /* visor */
  var lb = document.querySelector("[data-lb]");
  if (lb) {
    var ims = Array.prototype.slice.call(document.querySelectorAll(".gz img")), k = 0;
    var lbImg = lb.querySelector("[data-lb-img]"), lbN = lb.querySelector("[data-lb-n]");
    var mostrar = function (n) { k = (n + ims.length) % ims.length; lbImg.src = ims[k].src; lbN.textContent = (k + 1) + " / " + ims.length; };
    ims.forEach(function (im, n) { im.closest(".gz").addEventListener("click", function () { mostrar(n); lb.hidden = false; if (lenis) lenis.stop(); }); });
    var cerrar = function () { lb.hidden = true; if (lenis) lenis.start(); };
    lb.querySelector("[data-lb-x]").addEventListener("click", cerrar);
    lb.querySelector("[data-lb-a]").addEventListener("click", function () { mostrar(k - 1); });
    lb.querySelector("[data-lb-s]").addEventListener("click", function () { mostrar(k + 1); });
    lb.addEventListener("click", function (ev) { if (ev.target === lb) cerrar(); });
    document.addEventListener("keydown", function (ev) { if (lb.hidden) return; if (ev.key === "Escape") cerrar(); else if (ev.key === "ArrowLeft") mostrar(k - 1); else if (ev.key === "ArrowRight") mostrar(k + 1); });
  }
})();
