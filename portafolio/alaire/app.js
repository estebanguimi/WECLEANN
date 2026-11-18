/* AL AIRE — interacción. Zapping con estática, encendido de tubo, código de tiempo continuo entre páginas,
   rótulos animados, ticker con velocidad de scroll, guía con ventana PIP, tira de episodios arrastrable, créditos. */
(function () {
  "use strict";
  var G = window.gsap, ST = window.ScrollTrigger;
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (G && ST) G.registerPlugin(ST);

  /* ---------------- scroll suave ---------------- */
  var lenis = null;
  if (window.Lenis && !reducido) {
    lenis = new Lenis({ lerp: .1, smoothWheel: true });
    if (ST) lenis.on("scroll", ST.update);
    if (G) { G.ticker.add(function (t) { lenis.raf(t * 1000); }); G.ticker.lagSmoothing(0); }
  }

  /* ---------------- menú, cabecera, copiar ---------------- */
  var menu = document.querySelector("[data-menu]"), nav = document.querySelector("[data-nav]");
  if (menu) menu.addEventListener("click", function () { var a = nav.classList.toggle("abierto"); menu.setAttribute("aria-expanded", a ? "true" : "false"); });
  var cab = document.querySelector("[data-cab]"), yUlt = 0;
  window.addEventListener("scroll", function () {
    var y = window.scrollY; if (cab && !(nav && nav.classList.contains("abierto"))) cab.classList.toggle("oculta", y > yUlt && y > 300); yUlt = y;
  }, { passive: true });
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var av = b.querySelector("[data-copiado]"), t = b.getAttribute("data-copiar");
      var ok = function () { if (av) { var o = av.textContent; av.textContent = "Copied"; setTimeout(function () { av.textContent = o; }, 1500); } };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
    });
  });
  document.querySelectorAll(".cv-correo").forEach(function (b) {
    b.addEventListener("click", function () { var t = b.textContent; b.textContent = "Email copied"; setTimeout(function () { b.textContent = t; }, 1600); });
  });

  /* ---------------- código de tiempo: la transmisión sigue entre páginas ---------------- */
  var tcEl = document.querySelector("[data-tc]"), t0 = Date.now();
  try { var g = sessionStorage.getItem("aire-t0"); if (g) t0 = +g; else sessionStorage.setItem("aire-t0", String(t0)); } catch (e) {}
  function dos(n) { return (n < 10 ? "0" : "") + n; }
  if (tcEl) (function tick() {
    var ms = Date.now() - t0, s = Math.floor(ms / 1000);
    tcEl.textContent = dos(Math.floor(s / 3600)) + ":" + dos(Math.floor(s / 60) % 60) + ":" + dos(s % 60) + ":" + dos(Math.floor((ms % 1000) / 40));
    requestAnimationFrame(tick);
  })();

  /* ---------------- estática ---------------- */
  function ruido(cv) {
    var c = cv.getContext("2d"), w = 160, h = 100; cv.width = w; cv.height = h;
    var img = c.createImageData(w, h), d = img.data, vivo = false;
    function cuadro() {
      if (!vivo) return;
      for (var i = 0; i < d.length; i += 4) { var v = Math.random() * 255 | 0; d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255; }
      var y = Math.random() * h | 0; // franja de sincronía
      for (var x = 0; x < w; x++) { var k = (y * w + x) * 4; d[k] = d[k + 1] = d[k + 2] = 255; }
      c.putImageData(img, 0, 0); requestAnimationFrame(cuadro);
    }
    return { on: function () { if (!vivo) { vivo = true; cuadro(); } }, off: function () { vivo = false; } };
  }
  var zap = document.querySelector("[data-zap]"), zapR = zap ? ruido(zap.querySelector("canvas")) : null, zapCh = document.querySelector("[data-zap-ch]");
  var crt = document.querySelector("[data-crt]");

  /* salir: zapping a la página destino */
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[href]");
    if (!a || ev.defaultPrevented || ev.metaKey || ev.ctrlKey || ev.shiftKey || a.target === "_blank" || a.hasAttribute("download")) return;
    var h = a.getAttribute("href");
    if (!/\.html(#.*)?$/.test(h) || /^https?:/.test(h) || a.closest("[data-tira]") && tiraMovio) { if (tiraMovio) ev.preventDefault(); return; }
    ev.preventDefault();
    if (reducido || !zap) { location.href = h; return; }
    var n = 1 + Math.floor(Math.random() * 6);
    zapCh.textContent = "CH " + dos(n);
    zap.classList.add("activo"); zapR.on();
    try { sessionStorage.setItem("aire-zap", "1"); } catch (e) {}
    setTimeout(function () { location.href = h; }, 380);
  });
  window.addEventListener("pageshow", function (e) { if (e.persisted && zap) { zap.classList.remove("activo"); zapR.off(); } });

  /* entrar: encendido de tubo */
  var vino = false;
  try { vino = sessionStorage.getItem("aire-zap") === "1"; sessionStorage.removeItem("aire-zap"); } catch (e) {}
  if (crt && G && !reducido && vino) {
    crt.classList.add("activo");
    var o = { sx: 0, o: 1, op: 1 };
    G.timeline({ onComplete: function () { crt.classList.remove("activo"); G.set(crt, { opacity: 1 }); } })
      .to(o, { sx: 1, duration: .3, ease: "power2.out", onUpdate: function () { crt.style.setProperty("--sx", o.sx); crt.style.setProperty("--o", 1); } })
      .to(crt, { opacity: 0, duration: .45, ease: "power2.in" });
  }

  /* ---------------- titulares con golpe y rótulos ---------------- */
  if (G && !reducido) {
    document.querySelectorAll("[data-golpe]").forEach(function (el) {
      var partes = el.innerHTML.split(/<br\s*\/?>/i);
      el.innerHTML = partes.map(function (l) { return '<span style="display:block;overflow:hidden"><span style="display:block">' + l + "</span></span>"; }).join("");
      G.from(el.querySelectorAll("span > span"), { yPercent: 105, skewY: 6, duration: 1, ease: "expo.out", stagger: .09, delay: vino ? .5 : .15 });
    });
    document.querySelectorAll("[data-tercio]").forEach(function (t) {
      var a = t.querySelector(".tercio-a"), b = t.querySelector(".tercio-b");
      G.timeline({ delay: vino ? .65 : .3 })
        .from(a, { clipPath: "inset(0 100% 0 0)", duration: .7, ease: "expo.inOut" })
        .from(b, { clipPath: "inset(0 100% 0 0)", x: -20, duration: .6, ease: "expo.out" }, "-=.25");
    });
  }

  /* ---------------- ticker ---------------- */
  document.querySelectorAll("[data-ticker]").forEach(function (tk) {
    if (reducido || !G) return;
    var x = 0, vel = 0, w = tk.scrollWidth / 2, ult = window.scrollY;
    G.ticker.add(function () {
      var y = window.scrollY; vel += (Math.abs(y - ult) * .25 - vel) * .1; ult = y;
      x -= 1.1 + vel; if (-x >= w) x += w; tk.style.transform = "translate3d(" + x + "px,0,0)";
    });
    window.addEventListener("resize", function () { w = tk.scrollWidth / 2; });
  });

  /* ---------------- transmisión: zapping entre programas ---------------- */
  var tx = document.querySelector("[data-tx]");
  if (tx) (function () {
    var progs = []; try { progs = JSON.parse(document.getElementById("programas").textContent); } catch (e) {}
    var imgs = tx.querySelectorAll(".tx-img"), i = 0, dur = 6, visible = true, tl = null;
    var ch = tx.querySelector("[data-ch]"), pt = tx.querySelector("[data-prog-t]"), pc = tx.querySelector("[data-prog-c]"), pa = tx.querySelector("[data-prog]"), barra = tx.querySelector("[data-prog-barra]");
    var cv = document.createElement("canvas"); cv.setAttribute("aria-hidden", "true");
    cv.style.cssText = "position:absolute;inset:0;width:100%;height:100%;opacity:0;image-rendering:pixelated;pointer-events:none;mix-blend-mode:screen";
    tx.querySelector("[data-pant]").appendChild(cv);
    var r = ruido(cv);
    function correr() {
      if (!G || reducido) return;
      if (tl) tl.kill();
      tl = G.fromTo(barra, { scaleX: 0 }, { scaleX: 1, duration: dur, ease: "none", onComplete: function () { if (visible) ir(1); else correr(); } });
    }
    function ir(d) {
      var n = (i + d + progs.length) % progs.length, p = progs[n];
      var cambiar = function () {
        imgs[i].classList.remove("activa"); i = n;
        if (imgs[i].loading === "lazy") imgs[i].loading = "eager";
        imgs[i].classList.add("activa");
        ch.textContent = "CH " + dos(p.ch); pt.textContent = p.t; pc.textContent = p.c + " · " + p.cifra; pa.setAttribute("href", p.slug + ".html");
      };
      if (!G || reducido) { cambiar(); return; }
      r.on();
      G.timeline().to(cv, { opacity: .85, duration: .08 }).add(cambiar).to(cv, { opacity: 0, duration: .32, delay: .14, onComplete: r.off });
      correr();
    }
    tx.querySelectorAll("[data-zap-btn]").forEach(function (b) { b.addEventListener("click", function () { ir(+b.getAttribute("data-zap-btn")); }); });
    document.addEventListener("keydown", function (ev) {
      if (!visible || /input|textarea/i.test(ev.target.tagName)) return;
      if (ev.key === "ArrowRight") ir(1); else if (ev.key === "ArrowLeft") ir(-1);
    });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }, { threshold: .3 }).observe(tx);
    correr();
  })();

  /* ---------------- textos que se encienden con el scroll ---------------- */
  document.querySelectorAll("[data-revelar]").forEach(function (el) {
    if (!G || !ST || reducido) return;
    el.innerHTML = el.textContent.split(" ").map(function (w) { return '<span class="pl">' + w + "</span>"; }).join(" ");
    G.to(el.querySelectorAll(".pl"), { opacity: 1, stagger: .1, ease: "none", scrollTrigger: { trigger: el, start: "top 80%", end: "bottom 45%", scrub: true } });
  });

  /* ---------------- rating ---------------- */
  if (G && ST && !reducido) {
    document.querySelectorAll(".rt-b i").forEach(function (b) {
      G.from(b, { scaleX: 0, duration: 1.6, ease: "expo.out", scrollTrigger: { trigger: b, start: "top 88%", once: true } });
    });
    document.querySelectorAll("[data-contar]").forEach(function (el) {
      var fin = +el.getAttribute("data-contar"), o = { v: 0 };
      G.to(o, { v: fin, duration: 1.6, ease: "expo.out", scrollTrigger: { trigger: el, start: "top 90%", once: true }, onUpdate: function () { el.textContent = Math.round(o.v); } });
    });
    document.querySelectorAll(".ep, .formatos li, .recorrido li, .cv-item, .cd, .epg-p, .canal-cab").forEach(function (el) {
      if (el.closest("[data-tira]")) return;
      G.from(el, { y: 30, opacity: 0, duration: .9, ease: "expo.out", scrollTrigger: { trigger: el, start: "top 94%", once: true } });
    });
  }

  /* ---------------- guía: ventana PIP ---------------- */
  var epg = document.querySelector("[data-epg]");
  if (epg) {
    var pip = epg.querySelector("[data-pip-v]"), pImg = pip.querySelector("[data-pip-img]"), pT = pip.querySelector("[data-pip-t]"), pS = pip.querySelector("[data-pip-s]");
    epg.addEventListener("pointerover", function (ev) {
      var a = ev.target.closest("[data-pip]"); if (!a || ev.pointerType === "touch") return;
      var d = a.getAttribute("data-pip").split("|");
      pT.textContent = d[0]; pS.textContent = d[1]; if (pImg.getAttribute("src") !== d[2]) pImg.src = d[2];
      epg.classList.add("con-pip");
    });
    epg.addEventListener("pointerleave", function () { epg.classList.remove("con-pip"); });
  }

  /* ---------------- tira de episodios ---------------- */
  var tiraMovio = false;
  var tira = document.querySelector("[data-tira]");
  if (tira) (function () {
    var pista = tira.querySelector("[data-tira-in]"), barra = document.querySelector("[data-tira-barra]");
    var x = 0, min = 0, arr = null, vel = 0;
    function medir() { min = Math.min(0, tira.clientWidth - pista.scrollWidth); }
    function poner(v, anim) {
      x = Math.max(min, Math.min(0, v));
      if (G && anim && !reducido) G.to(pista, { x: x, duration: .8, ease: "expo.out" }); else pista.style.transform = "translate3d(" + x + "px,0,0)";
      if (barra) barra.style.transform = "scaleX(" + (min ? .1 + .9 * (x / min) : 1) + ")";
    }
    medir(); window.addEventListener("resize", function () { medir(); poner(x); });
    tira.addEventListener("pointerdown", function (ev) {
      if (ev.pointerType === "touch") return;
      arr = { x0: ev.clientX, xi: x, t: performance.now(), ult: ev.clientX }; tiraMovio = false; vel = 0;
      if (G) G.killTweensOf(pista);
    });
    window.addEventListener("pointermove", function (ev) {
      if (!arr) return;
      var dx = ev.clientX - arr.x0;
      if (Math.abs(dx) > 6) { tiraMovio = true; tira.classList.add("arrastrando"); }
      vel = ev.clientX - arr.ult; arr.ult = ev.clientX;
      if (tiraMovio) poner(arr.xi + dx);
    });
    window.addEventListener("pointerup", function () {
      if (!arr) return; arr = null; tira.classList.remove("arrastrando");
      if (tiraMovio) poner(x + vel * 14, true);
      setTimeout(function () { tiraMovio = false; }, 50);
    });
    /* en táctil, la tira se desplaza con scroll nativo */
    if (window.matchMedia("(hover: none)").matches) { tira.style.overflowX = "auto"; tira.addEventListener("scroll", function () { if (barra) barra.style.transform = "scaleX(" + (.1 + .9 * tira.scrollLeft / Math.max(1, tira.scrollWidth - tira.clientWidth)) + ")"; }); }
    document.querySelectorAll("[data-tira-btn]").forEach(function (b) {
      b.addEventListener("click", function () {
        var paso = (pista.firstElementChild.offsetWidth + 18) * 2 * +b.getAttribute("data-tira-btn");
        if (tira.style.overflowX === "auto") tira.scrollBy({ left: paso, behavior: "smooth" }); else poner(x - paso, true);
      });
    });
    tira.querySelectorAll("img").forEach(function (im) { im.addEventListener("dragstart", function (e) { e.preventDefault(); }); });
  })();

  /* ---------------- créditos ---------------- */
  var cred = document.querySelector("[data-creditos]");
  if (cred && G && ST && !reducido) {
    var rollo = cred.querySelector("[data-rollo]");
    G.to(rollo, { y: function () { return -(rollo.offsetHeight - window.innerHeight * .6); }, ease: "none",
      scrollTrigger: { trigger: cred, start: "top top", end: "bottom bottom", scrub: true, invalidateOnRefresh: true } });
  }

  /* ---------------- episodio: barra de "a continuación" y visor ---------------- */
  var sb = document.querySelector("[data-sigue-barra]");
  if (sb && G && ST && !reducido) G.to(sb, { scaleX: 1, ease: "none", scrollTrigger: { trigger: sb, start: "top 95%", end: "top 45%", scrub: true } });
  var lb = document.querySelector("[data-lb]");
  if (lb) {
    var ims = Array.prototype.slice.call(document.querySelectorAll(".cd img")), k = 0;
    var lbImg = lb.querySelector("[data-lb-img]"), lbN = lb.querySelector("[data-lb-n]");
    var mostrar = function (n) { k = (n + ims.length) % ims.length; lbImg.src = ims[k].src; lbN.textContent = dos(k + 1) + " / " + dos(ims.length); };
    ims.forEach(function (im, n) { im.closest(".cd").addEventListener("click", function () { mostrar(n); lb.hidden = false; if (lenis) lenis.stop(); }); });
    var cerrar = function () { lb.hidden = true; if (lenis) lenis.start(); };
    lb.querySelector("[data-lb-x]").addEventListener("click", cerrar);
    lb.querySelector("[data-lb-a]").addEventListener("click", function () { mostrar(k - 1); });
    lb.querySelector("[data-lb-s]").addEventListener("click", function () { mostrar(k + 1); });
    lb.addEventListener("click", function (ev) { if (ev.target === lb) cerrar(); });
    document.addEventListener("keydown", function (ev) { if (lb.hidden) return; if (ev.key === "Escape") cerrar(); else if (ev.key === "ArrowLeft") mostrar(k - 1); else if (ev.key === "ArrowRight") mostrar(k + 1); });
  }
})();
