/* MATCHDAY · motor: intro de partido, barridos diagonales, textos que golpean, abanico de afiches,
   marquesinas por velocidad, marcador odómetro, carrusel arrastrable y alineación. */
(function () {
  "use strict";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fino = matchMedia("(hover: hover) and (pointer: fine)").matches;
  var G = window.gsap, ST = window.ScrollTrigger;
  if (!G) return;
  if (ST) G.registerPlugin(ST);
  if (window.Flip) G.registerPlugin(window.Flip);

  var lenis = null, velocidad = 0;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ lerp: 0.1 });
    lenis.on("scroll", function (l) { velocidad = l.velocity; if (ST) ST.update(); });
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
  }

  /* ---------- Cabecera ---------- */
  var cab = document.querySelector("[data-cab]"), ultY = 0;
  function cabScroll(y) { if (y > ultY + 4 && y > 240) cab.classList.add("oculta"); else if (y < ultY - 4) cab.classList.remove("oculta"); ultY = y; }
  if (lenis) lenis.on("scroll", function (l) { cabScroll(l.scroll); }); else addEventListener("scroll", function () { cabScroll(scrollY); }, { passive: true });

  /* ---------- Textos que golpean ---------- */
  var golpes = G.utils.toArray("[data-golpe]");
  if (!reduce) G.set(golpes, { opacity: 0 });
  function golpear() {
    if (reduce) return;
    G.fromTo(golpes, { opacity: 0, scale: 2.4, rotation: -7, y: -30 }, { opacity: 1, scale: 1, rotation: 0, y: 0, duration: .55, ease: "back.out(1.7)", stagger: .12,
      onComplete: function () { G.fromTo("main", { x: -6 }, { x: 0, duration: .4, ease: "elastic.out(1.2, .25)" }); } });
    G.from(".hero-bio, .hero-acc, .ph-res, .pag-intro, .kicker", { opacity: 0, y: 24, duration: .8, ease: "expo.out", delay: .35, stagger: .06 });
  }

  /* ---------- Intro y barridos ---------- */
  var intro = document.querySelector("[data-intro]");
  var barrido = document.querySelector("[data-barrido]");
  var franjas = barrido ? barrido.querySelectorAll("i") : [];
  var barT = document.querySelector("[data-barrido-t]");
  var vieneDeBarrido = false, primera = false;
  try { vieneDeBarrido = sessionStorage.getItem("md-barrido") === "1"; sessionStorage.removeItem("md-barrido"); primera = !sessionStorage.getItem("md-visto"); sessionStorage.setItem("md-visto", "1"); } catch (e) {}

  function arrancar() {
    if (reduce) { golpear(); return; }
    if (vieneDeBarrido) {
      barrido.classList.add("activo");
      G.set(franjas, { x: function (i) { return i === 2 ? "170vw" : "260vw"; } });
      G.to(franjas[2], { x: "340vw", duration: .9, ease: "expo.inOut", delay: .05, onComplete: function () { barrido.classList.remove("activo"); } });
      G.delayedCall(.45, golpear);
    } else if (primera && intro && document.body.classList.contains("pg-inicio")) {
      intro.classList.add("activa");
      var t = intro.querySelector("[data-intro-t]");
      t.innerHTML = t.textContent.split("").map(function (c) { return "<span>" + c + "</span>"; }).join("");
      var tl = G.timeline({ onComplete: function () { intro.classList.remove("activa"); } });
      tl.from(t.children, { scale: 3, opacity: 0, rotation: function () { return G.utils.random(-14, 14); }, duration: .45, ease: "back.out(2)", stagger: .06 })
        .from(".intro-sub", { opacity: 0, y: 20, duration: .4 }, "-=.2")
        .to(t, { x: 10, duration: .05, repeat: 5, yoyo: true })
        .to(intro, { clipPath: "polygon(0 0,100% 0,100% 0%,90% 0%,80% 0%,70% 0%,60% 0%,50% 0%,40% 0%,30% 0%,20% 0%,10% 0%,0 0%)", duration: .8, ease: "expo.inOut" }, "+=.25")
        .add(golpear, "-=.35");
      G.set(intro, { clipPath: "polygon(0 0,100% 0,100% 100%,90% 96%,80% 100%,70% 95%,60% 100%,50% 96%,40% 100%,30% 95%,20% 100%,10% 96%,0 100%)" });
    } else golpear();
  }

  function salir(href, titulo) {
    if (reduce) { location.href = href; return; }
    barrido.style.pointerEvents = "auto";
    barrido.classList.add("activo");
    barT.textContent = titulo || "";
    G.set(franjas, { x: 0 }); G.set(barT, { opacity: 0, scale: 1.4 });
    G.timeline({ onComplete: function () { try { sessionStorage.setItem("md-barrido", "1"); } catch (e) {} location.href = href; } })
      .to(franjas[0], { x: "260vw", duration: .7, ease: "power3.in" })
      .to(franjas[1], { x: "260vw", duration: .7, ease: "power3.in" }, .06)
      .to(franjas[2], { x: "170vw", duration: .75, ease: "expo.inOut" }, .1)
      .to(barT, { opacity: 1, scale: 1, duration: .35, ease: "back.out(2)" }, "-=.25");
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[href]");
    if (!a || a.target === "_blank" || ev.metaKey || ev.ctrlKey) return;
    var h = a.getAttribute("href");
    if (!/\.html$/.test(h) || /^https?:/.test(h)) return;
    ev.preventDefault();
    var t = a.querySelector(".p-visita, .cromo-banda b, .proximo-t");
    salir(h, (t ? t.textContent : a.textContent).replace(/\s+/g, " ").trim().slice(0, 32));
  });
  addEventListener("pageshow", function (ev) { if (ev.persisted) { G.set(franjas, { x: 0 }); barrido.style.pointerEvents = "none"; barrido.classList.remove("activo"); } });

  /* ---------- Marquesinas guiadas por la velocidad del scroll ---------- */
  var filas = G.utils.toArray(".fila-nombre");
  var ticker = document.querySelector("[data-ticker]");
  var pos = filas.map(function () { return Math.random() * -40; }), tpos = 0;
  if (!reduce) G.ticker.add(function (t, dt) {
    var v = Math.min(Math.abs(velocidad), 60);
    filas.forEach(function (f, i) {
      var dir = parseFloat(f.getAttribute("data-vel"));
      pos[i] -= dir * (0.012 + v * 0.01) * dt * 0.06;
      if (pos[i] <= -50) pos[i] += 50; if (pos[i] > 0) pos[i] -= 50;
      f.style.transform = "translate3d(" + pos[i] + "%,0,0)";
    });
    if (ticker) { tpos -= (0.02 + v * 0.008) * dt * 0.06; if (tpos <= -50) tpos += 50; ticker.style.transform = "translate3d(" + tpos + "%,0,0)"; }
  });

  /* ---------- Abanico de afiches ---------- */
  var abanico = document.querySelector("[data-abanico]");
  if (abanico) {
    var cartas = G.utils.toArray(abanico.querySelectorAll(".carta"));
    var n = cartas.length, mid = (n - 1) / 2;
    var abrir = function (extra) {
      var w = abanico.clientWidth;
      cartas.forEach(function (c, i) {
        var k = i - mid;
        G.to(c, { x: k * w * (0.13 + extra), rotation: k * (9 + extra * 30), y: Math.abs(k) * 18, duration: 1.1, ease: "expo.out", overwrite: "auto" });
      });
    };
    if (!reduce) {
      G.set(cartas, { y: 260, rotation: 0, opacity: 0 });
      G.to(cartas, { y: 0, opacity: 1, duration: .8, ease: "expo.out", stagger: .07, delay: primera ? 2.4 : .5, onComplete: function () { abrir(0); } });
    } else abrir(0);
    if (fino && !reduce) {
      var hero = document.querySelector("[data-hero]");
      var rx = G.quickTo(abanico, "rotationX", { duration: .8 }), ry = G.quickTo(abanico, "rotationY", { duration: .8 });
      hero.addEventListener("pointermove", function (ev) {
        var r = hero.getBoundingClientRect();
        var px = (ev.clientX - r.left) / r.width - .5, py = (ev.clientY - r.top) / r.height - .5;
        ry(px * 16); rx(-py * 12);
      });
      cartas.forEach(function (c) {
        c.addEventListener("pointerenter", function () { G.to(c, { scale: 1.08, zIndex: 10, duration: .4, ease: "back.out(2)" }); });
        c.addEventListener("pointerleave", function () { G.to(c, { scale: 1, zIndex: 1, duration: .5 }); });
      });
    }
    if (ST && !reduce) ST.create({ trigger: "[data-hero]", start: "top top", end: "bottom top", scrub: true, onUpdate: function (s) {
      var w = abanico.clientWidth;
      cartas.forEach(function (c, i) { var k = i - mid; G.set(c, { x: k * w * (0.13 + s.progress * .25), rotation: k * (9 + s.progress * 14) }); });
    } });
    addEventListener("resize", function () { abrir(0); });
  }

  /* ---------- Fixture con afiche flotante ---------- */
  var fx = document.querySelector("[data-fixture]");
  if (fx && fino) {
    var prev = fx.querySelector("[data-fx-prev]"), pim = prev.querySelector("img");
    var mx = G.quickTo(prev, "x", { duration: .5, ease: "power3" }), my = G.quickTo(prev, "y", { duration: .5, ease: "power3" });
    fx.querySelectorAll(".partido").forEach(function (p) { p.addEventListener("pointerenter", function () { pim.src = p.getAttribute("data-prev"); fx.classList.add("activo"); }); });
    fx.addEventListener("pointerleave", function () { fx.classList.remove("activo"); });
    fx.addEventListener("pointermove", function (ev) { mx(ev.clientX + 40); my(ev.clientY - 160); });
  }

  /* ---------- Marcador odómetro ---------- */
  document.querySelectorAll("[data-odo]").forEach(function (el) {
    var txt = el.getAttribute("data-odo");
    if (reduce || !ST) return;
    el.innerHTML = txt.split("").map(function () {
      var s = ""; for (var d = 0; d <= 9; d++) s += "<span>" + d + "</span>";
      return '<span class="odo-col"><span>' + s + "</span></span>";
    }).join("");
    var cols = el.querySelectorAll(".odo-col > span");
    ST.create({ trigger: el, start: "top 85%", once: true, onEnter: function () {
      cols.forEach(function (c, i) { G.to(c, { yPercent: -parseInt(txt[i], 10) * 10, duration: 1.6 + i * .25, ease: "expo.out", delay: i * .08 }); });
    } });
  });

  /* ---------- Carrusel arrastrable con inercia ---------- */
  var car = document.querySelector("[data-carrusel]");
  if (car) {
    var pista = car.querySelector("[data-pista]"), afiches = G.utils.toArray(car.querySelectorAll(".afiche"));
    var contador = document.querySelector("[data-car-n]");
    var x = 0, objetivo = 0, abajo = false, x0 = 0, o0 = 0, vel = 0, ultX = 0, movido = false;
    var limite = function () { return -(pista.scrollWidth - innerWidth * 0.6); };
    car.addEventListener("pointerdown", function (ev) { abajo = true; movido = false; x0 = ev.clientX; o0 = objetivo; ultX = ev.clientX; car.classList.add("arrastrando"); car.setPointerCapture(ev.pointerId); });
    car.addEventListener("pointermove", function (ev) {
      if (!abajo) return;
      var dx = ev.clientX - x0; if (Math.abs(dx) > 4) movido = true;
      objetivo = o0 + dx * 1.2; vel = ev.clientX - ultX; ultX = ev.clientX;
    });
    var soltar = function () { if (!abajo) return; abajo = false; car.classList.remove("arrastrando"); objetivo += vel * 14; };
    car.addEventListener("pointerup", soltar); car.addEventListener("pointercancel", soltar);
    car.addEventListener("wheel", function (ev) { if (Math.abs(ev.deltaX) > Math.abs(ev.deltaY)) { objetivo -= ev.deltaX; ev.preventDefault(); } }, { passive: false });
    G.ticker.add(function () {
      objetivo = Math.min(0, Math.max(limite(), objetivo));
      var antes = x;
      x += (objetivo - x) * (reduce ? 1 : 0.09);
      pista.style.transform = "translate3d(" + x + "px,0,0)";
      var sk = Math.max(-10, Math.min(10, (x - antes) * 0.35));
      afiches.forEach(function (a) { a.style.transform = "rotate(" + (-sk * .4) + "deg) skewX(" + (-sk) + "deg)"; });
      if (contador && afiches[0]) {
        var paso = afiches[0].offsetWidth + 22;
        var idx = Math.min(afiches.length, Math.max(1, Math.round(-x / paso) + 1));
        contador.textContent = (idx < 10 ? "0" : "") + idx;
      }
    });
  }

  /* ---------- Alineación ---------- */
  var cancha = document.querySelector("[data-cancha]");
  if (cancha) {
    var jug = cancha.querySelectorAll(".jugador"), dets = document.querySelectorAll("[data-det]");
    var marcar = function (i) {
      jug.forEach(function (j) { j.classList.toggle("activo", j.getAttribute("data-pos") === String(i)); });
      dets.forEach(function (d) { d.classList.toggle("activo", d.getAttribute("data-det") === String(i)); });
    };
    jug.forEach(function (j) { var i = j.getAttribute("data-pos"); j.addEventListener("click", function () { marcar(i); }); j.addEventListener("pointerenter", function () { marcar(i); }); });
    marcar(0);
    if (ST && !reduce) G.from(jug, { scale: 0, opacity: 0, duration: .6, ease: "back.out(2)", stagger: .08, scrollTrigger: { trigger: cancha, start: "top 75%" } });
  }

  /* ---------- Inclinación 3D y botones magnéticos ---------- */
  if (fino && !reduce) {
    document.querySelectorAll("[data-tilt]").forEach(function (el) {
      el.addEventListener("pointermove", function (ev) {
        var r = el.getBoundingClientRect(), px = (ev.clientX - r.left) / r.width - .5, py = (ev.clientY - r.top) / r.height - .5;
        G.to(el, { rotationY: px * 18, rotationX: -py * 14, transformPerspective: 900, duration: .6, ease: "power3" });
      });
      el.addEventListener("pointerleave", function () { G.to(el, { rotationY: 0, rotationX: 0, duration: 1, ease: "elastic.out(1, .4)" }); });
    });
    document.querySelectorAll("[data-magnetico]").forEach(function (el) {
      el.addEventListener("pointermove", function (ev) {
        var r = el.getBoundingClientRect();
        G.to(el, { x: (ev.clientX - r.left - r.width / 2) * .25, y: (ev.clientY - r.top - r.height / 2) * .35, duration: .4, ease: "power3" });
      });
      el.addEventListener("pointerleave", function () { G.to(el, { x: 0, y: 0, duration: .9, ease: "elastic.out(1, .35)" }); });
    });
  }

  /* ---------- Apariciones al hacer scroll ---------- */
  if (ST && !reduce) {
    ST.batch(".partido, .mc, .tray li, .conv-cols > div, .ficha", { start: "top 92%", onEnter: function (b) { G.from(b, { opacity: 0, x: -60, duration: .8, ease: "expo.out", stagger: .06 }); } });
    ST.batch(".cromo, .g-item, .afiche", { start: "top 95%", onEnter: function (b) {
      G.from(b, { opacity: 0, y: 80, rotation: function () { return G.utils.random(-6, 6); }, duration: .9, ease: "back.out(1.4)", stagger: .06 });
    } });
    G.utils.toArray(".titulo-sec h2").forEach(function (h) {
      G.from(h, { xPercent: -12, opacity: 0, duration: 1, ease: "expo.out", scrollTrigger: { trigger: h, start: "top 88%" } });
    });
    var phn = document.querySelector(".ph-num");
    if (phn) G.to(phn, { yPercent: 40, ease: "none", scrollTrigger: { trigger: "[data-ph]", start: "top top", end: "bottom top", scrub: true } });
    var pg = document.querySelector(".pie-grande");
    if (pg) G.from(pg, { yPercent: 60, rotation: -4, opacity: 0, duration: 1, ease: "back.out(1.6)", scrollTrigger: { trigger: pg, start: "top 95%" } });
  }

  /* ---------- Filtros de la plantilla ---------- */
  var album = document.querySelector("[data-album]");
  if (album) {
    var tabs = document.querySelectorAll("[data-filtro]"), cromos = album.querySelectorAll(".cromo");
    tabs.forEach(function (tb) {
      tb.addEventListener("click", function () {
        var f = tb.getAttribute("data-filtro");
        var est = window.Flip ? Flip.getState(cromos) : null;
        tabs.forEach(function (x) { x.classList.toggle("activo", x === tb); x.setAttribute("aria-pressed", String(x === tb)); });
        cromos.forEach(function (c) { c.classList.toggle("oculta", f !== "todo" && c.getAttribute("data-cat") !== f); });
        if (est && !reduce) Flip.from(est, { duration: .7, ease: "back.out(1.2)", absolute: true, stagger: .03,
          onEnter: function (els) { return G.fromTo(els, { opacity: 0, scale: .6, rotation: -10 }, { opacity: 1, scale: 1, rotation: 0, duration: .6 }); },
          onLeave: function (els) { return G.to(els, { opacity: 0, scale: .6, duration: .3 }); } });
        if (ST) ST.refresh();
      });
    });
  }

  /* ---------- Visor ---------- */
  var visor = document.querySelector("[data-visor]"), gal = document.querySelector("[data-galeria]");
  if (visor && gal) {
    var srcs = Array.prototype.map.call(gal.querySelectorAll("img"), function (i) { return i.getAttribute("src"); });
    var vi = visor.querySelector("[data-visor-img]"), vn = visor.querySelector("[data-visor-n]"), k = 0;
    var ver = function (i) { k = (i + srcs.length) % srcs.length; vi.src = srcs[k]; vn.textContent = (k + 1) + " / " + srcs.length; G.fromTo(vi, { rotation: G.utils.random(-4, 4), scale: .9 }, { rotation: 0, scale: 1, duration: .5, ease: "back.out(1.8)" }); };
    var cerrar = function () { visor.hidden = true; if (lenis) lenis.start(); };
    gal.addEventListener("click", function (ev) { var f = ev.target.closest(".g-item"); if (f) { visor.hidden = false; if (lenis) lenis.stop(); ver(parseInt(f.getAttribute("data-i"), 10)); } });
    visor.querySelector("[data-visor-cerrar]").addEventListener("click", cerrar);
    visor.querySelector("[data-visor-ant]").addEventListener("click", function () { ver(k - 1); });
    visor.querySelector("[data-visor-sig]").addEventListener("click", function () { ver(k + 1); });
    visor.addEventListener("click", function (ev) { if (ev.target === visor) cerrar(); });
    document.addEventListener("keydown", function (ev) { if (visor.hidden) return; if (ev.key === "Escape") cerrar(); if (ev.key === "ArrowRight") ver(k + 1); if (ev.key === "ArrowLeft") ver(k - 1); });
  }

  /* ---------- Copiar correo ---------- */
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var av = b.querySelector("[data-copiado]"), txt = b.getAttribute("data-copiar"), orig = av ? av.textContent : "";
      var ok = function () { if (av) { av.textContent = "Copied!"; setTimeout(function () { av.textContent = orig; }, 1800); } G.fromTo(b, { rotation: -3 }, { rotation: 0, duration: .6, ease: "elastic.out(1.2, .3)" }); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () { if (av) av.textContent = txt; }); else if (av) av.textContent = txt;
    });
  });

  var ya = false;
  var go = function () { if (ya) return; ya = true; arrancar(); if (ST) ST.refresh(); };
  if (document.readyState === "complete") go(); else { addEventListener("load", go); setTimeout(go, 2500); }
})();

/* Aviso al copiar el correo desde el currículum */
document.querySelectorAll(".cv-correo").forEach(function (b) {
  b.addEventListener("click", function () { var t = b.textContent; b.textContent = "Email copied"; setTimeout(function () { b.textContent = t; }, 1600); });
});
