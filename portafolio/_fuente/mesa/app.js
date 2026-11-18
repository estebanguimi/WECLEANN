/* MESA — interacción. Lienzo con cámara (arrastre, zoom, inercia), minimapa, reglas, inspector,
   cursor de Esteban, notas adhesivas, transición de zoom a un frame. Sin dependencias salvo GSAP/Lenis. */
(function () {
  "use strict";
  var reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var tactil = window.matchMedia("(hover: none)").matches;
  var movil = function () { return window.innerWidth <= 860; };
  var body = document.body;
  var G = window.gsap;

  /* ---------------- menú ---------------- */
  var menu = document.querySelector("[data-menu]"), nav = document.querySelector("[data-nav]");
  if (menu && nav) menu.addEventListener("click", function () {
    var a = nav.classList.toggle("abierto"); menu.setAttribute("aria-expanded", a ? "true" : "false");
  });

  /* ---------------- copiar ---------------- */
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var t = b.getAttribute("data-copiar"), av = b.querySelector("[data-copiado]");
      var ok = function () {
        if (av) { var o = av.textContent; av.textContent = "Copiado"; setTimeout(function () { av.textContent = o; }, 1500); }
        if (b.classList.contains("sw")) { b.classList.add("copiado"); setTimeout(function () { b.classList.remove("copiado"); }, 1500); }
      };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, ok); else ok();
    });
  });

  /* ---------------- transición: el frame clicado crece hasta llenar la pantalla ---------------- */
  var zt = document.querySelector("[data-zoomt]");
  function salir(href, rect) {
    if (!zt || reducido || !G) { location.href = href; return; }
    var W = innerWidth, H = innerHeight;
    rect = rect || { left: W * .3, top: H * .3, width: W * .4, height: H * .4 };
    var s = zt.firstElementChild;
    zt.classList.add("activo");
    G.set(s, { left: rect.left, top: rect.top, width: rect.width, height: rect.height, right: "auto", bottom: "auto", opacity: .0 });
    G.to(s, { opacity: 1, duration: .18 });
    G.to(s, { left: 0, top: 0, width: W, height: H, duration: .6, ease: "expo.inOut", onComplete: function () { location.href = href; } });
    try { sessionStorage.setItem("mesa-t", "1"); } catch (e) {}
  }
  function entrar() {
    var vino = false;
    try { vino = sessionStorage.getItem("mesa-t") === "1"; sessionStorage.removeItem("mesa-t"); } catch (e) {}
    if (!zt || !vino || reducido || !G) return;
    var s = zt.firstElementChild;
    zt.classList.add("activo");
    G.set(s, { inset: 0, opacity: 1 });
    G.to(s, { opacity: 0, duration: .55, ease: "power2.out", delay: .05, onComplete: function () { zt.classList.remove("activo"); } });
  }
  entrar();
  window.addEventListener("pageshow", function (e) { if (e.persisted && zt) zt.classList.remove("activo"); });
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[href]");
    if (!a || ev.defaultPrevented || ev.metaKey || ev.ctrlKey || ev.shiftKey || a.target === "_blank" || a.hasAttribute("download")) return;
    var h = a.getAttribute("href");
    if (!/\.html(#.*)?$/.test(h) || /^https?:/.test(h)) return;
    if (a.closest("[data-mundo]")) return; // el lienzo decide
    ev.preventDefault();
    salir(h, a.getBoundingClientRect());
  });

  /* ---------------- titulares por líneas ---------------- */
  function partir(el) {
    var html = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = html.map(function (l) { return '<span class="ln"><span>' + l + "</span></span>"; }).join("");
    return el.querySelectorAll(".ln > span");
  }
  if (G && !reducido) document.querySelectorAll("[data-lineas]").forEach(function (el) {
    G.from(partir(el), { yPercent: 110, duration: 1.1, ease: "expo.out", stagger: .08, delay: .15 });
  });

  /* ---------------- reglas ---------------- */
  var rh = document.querySelector('[data-regla="h"]'), rv = document.querySelector('[data-regla="v"]');
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  var marca = { x: -1, y: -1 };
  function dibujarRegla(cv, horizontal, origen, z) {
    if (!cv || !cv.offsetWidth) return;
    var w = cv.offsetWidth, h = cv.offsetHeight;
    if (cv.width !== w * dpr || cv.height !== h * dpr) { cv.width = w * dpr; cv.height = h * dpr; }
    var c = cv.getContext("2d");
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.clearRect(0, 0, w, h);
    c.fillStyle = "#8b877e"; c.strokeStyle = "#b9b5ab"; c.font = "9px 'IBM Plex Mono', monospace"; c.lineWidth = 1;
    var pasos = [10, 25, 50, 100, 250, 500, 1000], paso = 100;
    for (var i = 0; i < pasos.length; i++) { if (pasos[i] * z >= 60) { paso = pasos[i]; break; } paso = pasos[i]; }
    var largo = horizontal ? w : h;
    var ini = Math.floor((-origen / z) / paso) * paso;
    c.beginPath();
    for (var v = ini; (v * z + origen) < largo + paso * z; v += paso / 5) {
      var p = Math.round(v * z + origen) + .5, mayor = Math.abs(v % paso) < 0.001;
      var t = mayor ? 9 : 4;
      if (horizontal) { c.moveTo(p, h); c.lineTo(p, h - t); } else { c.moveTo(w, p); c.lineTo(w - t, p); }
      if (mayor) {
        if (horizontal) c.fillText(String(Math.round(v)), p + 3, 9);
        else { c.save(); c.translate(9, p - 3); c.rotate(-Math.PI / 2); c.fillText(String(Math.round(v)), 0, 0); c.restore(); }
      }
    }
    c.stroke();
    var m = horizontal ? marca.x : marca.y;
    if (m >= 0) { c.fillStyle = "#3b30ff"; if (horizontal) c.fillRect(m - .5, 0, 1.5, h); else c.fillRect(0, m - .5, w, 1.5); }
  }

  /* ================================================================ INICIO: el lienzo ================================================================ */
  var lienzo = document.querySelector("[data-lienzo]");
  if (lienzo) iniciarLienzo(); else iniciarPagina();

  function iniciarLienzo() {
    var mundo = document.querySelector("[data-mundo]");
    var frames = Array.prototype.slice.call(mundo.querySelectorAll("[data-fr]"));
    var datos = {};
    try { datos = JSON.parse(document.getElementById("datos-proyectos").textContent); } catch (e) {}
    var cam = { x: 0, y: 0, z: .5 };
    var zoomT = document.querySelector("[data-zoom-t]");
    var mini = document.querySelector("[data-mini]");
    var insp = document.querySelector("[data-insp]"), inspSel = document.querySelector("[data-insp-sel]"), inspDoc = document.querySelector("[data-insp-doc]");
    var guia = document.querySelector("[data-guia]");
    var cursorEg = document.querySelector("[data-cursor-eg]");
    var limites = medirMundo();
    var pendiente = false;

    function medirMundo() {
      var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
      mundo.querySelectorAll(".fr, .m-sec, .nota").forEach(function (el) {
        var x = el.offsetLeft, y = el.offsetTop;
        x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x + el.offsetWidth); y1 = Math.max(y1, y + el.offsetHeight);
      });
      return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
    }
    function area() {
      var r = lienzo.getBoundingClientRect(), rg = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--rg")) || 0;
      return { l: rg, t: rg, w: r.width - rg, h: r.height - rg, W: r.width, H: r.height };
    }
    function aplicar() {
      mundo.style.transform = "translate3d(" + cam.x + "px," + cam.y + "px,0) scale(" + cam.z + ")";
      mundo.style.setProperty("--z", cam.z);
      var pt = 24 * cam.z; while (pt < 12) pt *= 2; while (pt > 48) pt /= 2;
      lienzo.style.setProperty("--pt", pt + "px");
      lienzo.style.setProperty("--px", cam.x + "px"); lienzo.style.setProperty("--py", cam.y + "px");
      if (zoomT) zoomT.textContent = Math.round(cam.z * 100) + "%";
      lienzo.classList.toggle("lejos", cam.z < .22);
      if (!pendiente) { pendiente = true; requestAnimationFrame(dibujar); }
    }
    function dibujar() {
      pendiente = false;
      var a = area();
      dibujarRegla(rh, true, cam.x - a.l, cam.z);
      dibujarRegla(rv, false, cam.y - a.t, cam.z);
      dibujarMini();
    }
    function limitar() { cam.z = Math.max(.08, Math.min(2.2, cam.z)); }
    function zoomEn(px, py, f) {
      var z0 = cam.z; cam.z *= f; limitar(); var k = cam.z / z0;
      cam.x = px - (px - cam.x) * k; cam.y = py - (py - cam.y) * k; aplicar();
    }
    function encuadre(r, pad, dur) {
      var a = area(); pad = pad == null ? 60 : pad;
      var z = Math.min((a.w - pad * 2) / r.w, (a.h - pad * 2) / r.h); z = Math.max(.08, Math.min(1.4, z));
      var obj = { z: z, x: a.l + a.w / 2 - (r.x + r.w / 2) * z, y: a.t + a.h / 2 - (r.y + r.h / 2) * z };
      if (!G || reducido || dur === 0) { cam.x = obj.x; cam.y = obj.y; cam.z = obj.z; aplicar(); return; }
      G.killTweensOf(cam);
      G.to(cam, { x: obj.x, y: obj.y, z: obj.z, duration: dur || 1.1, ease: "expo.inOut", onUpdate: aplicar });
    }
    function rectDe(el) { return { x: el.offsetLeft, y: el.offsetTop, w: el.offsetWidth, h: el.offsetHeight }; }

    /* minimapa */
    var miniEsc = 1, miniOx = 0, miniOy = 0;
    function dibujarMini() {
      if (!mini || !mini.offsetWidth) return;
      var w = mini.offsetWidth, h = mini.offsetHeight;
      if (mini.width !== w * dpr) { mini.width = w * dpr; mini.height = h * dpr; }
      var c = mini.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, w, h);
      var pad = 10; miniEsc = Math.min((w - pad * 2) / limites.w, (h - pad * 2) / limites.h);
      miniOx = pad + ((w - pad * 2) - limites.w * miniEsc) / 2 - limites.x * miniEsc; miniOy = pad + ((h - pad * 2) - limites.h * miniEsc) / 2 - limites.y * miniEsc;
      frames.forEach(function (f) {
        c.fillStyle = f.classList.contains("sel") ? "#3b30ff" : "#cfcbc2";
        c.fillRect(miniOx + f.offsetLeft * miniEsc, miniOy + f.offsetTop * miniEsc, Math.max(1, f.offsetWidth * miniEsc), Math.max(1, f.offsetHeight * miniEsc));
      });
      var a = area();
      var vx = (a.l - cam.x) / cam.z, vy = (a.t - cam.y) / cam.z, vw = a.w / cam.z, vh = a.h / cam.z;
      c.strokeStyle = "#3b30ff"; c.lineWidth = 1.5;
      c.strokeRect(miniOx + vx * miniEsc, miniOy + vy * miniEsc, vw * miniEsc, vh * miniEsc);
    }
    if (mini) mini.addEventListener("pointerdown", function (ev) {
      ev.stopPropagation();
      var r = mini.getBoundingClientRect();
      var wx = (ev.clientX - r.left - miniOx) / miniEsc, wy = (ev.clientY - r.top - miniOy) / miniEsc;
      var a = area();
      G.to(cam, { x: a.l + a.w / 2 - wx * cam.z, y: a.t + a.h / 2 - wy * cam.z, duration: .7, ease: "expo.out", onUpdate: aplicar });
    });

    /* selección e inspector */
    var seleccion = null;
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function seleccionar(el, volar) {
      frames.forEach(function (f) { f.classList.remove("sel"); });
      document.querySelectorAll(".capas [data-ir]").forEach(function (b) { b.classList.remove("sel"); });
      seleccion = el;
      if (!el) { inspSel.hidden = true; inspDoc.hidden = false; insp.classList.remove("abierto"); aplicar(); return; }
      var slug = el.getAttribute("data-slug"), clave = el.getAttribute("data-clave");
      var grupo = slug ? frames.filter(function (f) { return f.getAttribute("data-slug") === slug; }) : [el];
      grupo.forEach(function (f) { f.classList.add("sel"); });
      var b = document.querySelector('.capas [data-ir="' + (slug || clave) + '"]'); if (b) b.classList.add("sel");
      var d = slug && datos[slug];
      if (d) {
        inspSel.innerHTML = '<button type="button" class="insp-cerrar" aria-label="Cerrar">✕</button><p class="panel-t mono">Frame seleccionado</p><img class="insp-img" src="' + d.img + '" alt="">' +
          "<h2>" + esc(d.t) + '</h2><p class="res">' + esc(d.res) + '</p><dl class="insp-dl">' +
          "<div><dt class='mono'>Cliente</dt><dd>" + esc(d.cli) + "</dd></div><div><dt class='mono'>Mi rol</dt><dd>" + esc(d.rol) + "</dd></div>" +
          "<div><dt class='mono'>Año</dt><dd>" + esc(d.a) + "</dd></div><div><dt class='mono'>Herramientas</dt><dd>" + esc(d.herr) + "</dd></div></dl>" +
          '<div class="insp-datos">' + d.d.map(function (x) { return "<div><b>" + esc(x[0]) + "</b><span>" + esc(x[1]) + "</span></div>"; }).join("") + "</div>" +
          '<div class="insp-pal">' + d.pal.map(function (c) { return '<span class="sw" style="--c:' + c + '"><i></i><span class="mono">' + c + "</span></span>"; }).join("") + "</div>" +
          '<a class="btn" href="' + slug + '.html" data-abrir>Abrir proyecto →</a>';
        inspSel.hidden = false; inspDoc.hidden = true;
        inspSel.querySelector("[data-abrir]").addEventListener("click", function (ev) { ev.preventDefault(); abrir(el); });
        inspSel.querySelector(".insp-cerrar").addEventListener("click", function () { seleccionar(null); });
        insp.classList.add("abierto");
      } else { inspSel.hidden = true; inspDoc.hidden = false; insp.classList.remove("abierto"); }
      if (volar) {
        var r = grupo.reduce(function (acc, f) {
          var x0 = Math.min(acc.x, f.offsetLeft), y0 = Math.min(acc.y, f.offsetTop);
          var x1 = Math.max(acc.x + acc.w, f.offsetLeft + f.offsetWidth), y1 = Math.max(acc.y + acc.h, f.offsetTop + f.offsetHeight);
          return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
        }, rectDe(grupo[0]));
        encuadre(r, movil() ? 30 : 80);
      }
      aplicar();
    }
    function abrir(el) {
      var href = el.getAttribute("href") || (el.getAttribute("data-slug") ? el.getAttribute("data-slug") + ".html" : null);
      if (!href) { seleccionar(el, true); return; }
      encuadre(rectDe(el), 0, .7);
      setTimeout(function () { salir(href, el.getBoundingClientRect()); }, reducido ? 0 : 500);
    }
    document.querySelectorAll(".capas [data-ir]").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-ir");
        var el = mundo.querySelector('[data-slug="' + k + '"]') || mundo.querySelector('[data-clave="' + k + '"]');
        if (el) seleccionar(el, true);
      });
    });

    /* arrastre, notas, toque, pellizco */
    var punteros = new Map(), arr = null, nota = null, vel = { x: 0, y: 0 }, tUlt = 0, pinch = null;
    lienzo.addEventListener("pointerdown", function (ev) {
      if (ev.target.closest(".zoom-ctl, .mini")) return;
      lienzo.setPointerCapture(ev.pointerId);
      punteros.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
      if (G) G.killTweensOf(cam);
      ocultarGuia(); detenerCursor();
      if (punteros.size === 2) {
        var p = Array.from(punteros.values());
        pinch = { d: Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y), cx: (p[0].x + p[1].x) / 2, cy: (p[0].y + p[1].y) / 2 };
        arr = null; return;
      }
      var n = ev.target.closest("[data-nota]");
      if (n) { nota = { el: n, x: ev.clientX, y: ev.clientY, l: n.offsetLeft, t: n.offsetTop }; n.style.zIndex = 9; return; }
      arr = { x: ev.clientX, y: ev.clientY, sx: ev.clientX, sy: ev.clientY, mov: false, el: ev.target.closest("[data-fr]") };
      vel = { x: 0, y: 0 }; tUlt = performance.now();
    });
    lienzo.addEventListener("pointermove", function (ev) {
      var r = lienzo.getBoundingClientRect(); var a = area();
      marca.x = ev.clientX - r.left - a.l; marca.y = ev.clientY - r.top - a.t;
      if (!pendiente) { pendiente = true; requestAnimationFrame(dibujar); }
      if (!punteros.has(ev.pointerId)) return;
      punteros.set(ev.pointerId, { x: ev.clientX, y: ev.clientY });
      if (pinch && punteros.size === 2) {
        var p = Array.from(punteros.values());
        var d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y), cx = (p[0].x + p[1].x) / 2, cy = (p[0].y + p[1].y) / 2;
        cam.x += cx - pinch.cx; cam.y += cy - pinch.cy;
        zoomEn(cx - r.left, cy - r.top, d / pinch.d);
        pinch = { d: d, cx: cx, cy: cy }; return;
      }
      if (nota) {
        nota.el.style.left = nota.l + (ev.clientX - nota.x) / cam.z + "px"; nota.el.style.top = nota.t + (ev.clientY - nota.y) / cam.z + "px"; return;
      }
      if (!arr) return;
      var dx = ev.clientX - arr.x, dy = ev.clientY - arr.y, ahora = performance.now(), dt = Math.max(1, ahora - tUlt);
      if (!arr.mov && Math.hypot(ev.clientX - arr.sx, ev.clientY - arr.sy) > 5) { arr.mov = true; lienzo.classList.add("arrastrando"); }
      if (arr.mov) { cam.x += dx; cam.y += dy; vel.x = dx / dt * 16; vel.y = dy / dt * 16; aplicar(); }
      arr.x = ev.clientX; arr.y = ev.clientY; tUlt = ahora;
    });
    function soltar(ev) {
      punteros.delete(ev.pointerId);
      if (punteros.size < 2) pinch = null;
      if (nota) { nota = null; return; }
      if (!arr) return;
      lienzo.classList.remove("arrastrando");
      if (!arr.mov) {
        var el = arr.el;
        if (el) {
          if (tactil && seleccion && (seleccion === el || (el.dataset.slug && seleccion.dataset.slug === el.dataset.slug))) abrir(el);
          else seleccionar(el, tactil);
        } else seleccionar(null);
      } else if (!reducido && G && performance.now() - tUlt < 80) {
        var o = { vx: vel.x, vy: vel.y };
        G.to(o, { vx: 0, vy: 0, duration: .9, ease: "power3.out", onUpdate: function () { cam.x += o.vx; cam.y += o.vy; aplicar(); } });
      }
      arr = null;
    }
    lienzo.addEventListener("pointerup", soltar);
    lienzo.addEventListener("pointercancel", soltar);
    lienzo.addEventListener("pointerleave", function () { marca.x = marca.y = -1; if (!pendiente) { pendiente = true; requestAnimationFrame(dibujar); } });
    mundo.addEventListener("click", function (ev) { if (ev.target.closest("a")) ev.preventDefault(); });
    mundo.addEventListener("dblclick", function (ev) { var el = ev.target.closest("[data-fr]"); if (el) abrir(el); });
    lienzo.addEventListener("wheel", function (ev) {
      ev.preventDefault(); ocultarGuia(); detenerCursor(); if (G) G.killTweensOf(cam);
      var r = lienzo.getBoundingClientRect();
      var dy = ev.deltaMode === 1 ? ev.deltaY * 16 : ev.deltaY, dx = ev.deltaMode === 1 ? ev.deltaX * 16 : ev.deltaX;
      if (ev.ctrlKey || ev.metaKey) zoomEn(ev.clientX - r.left, ev.clientY - r.top, Math.exp(-dy * .01));
      else if (Math.abs(dx) < 1 && Math.abs(dy) >= 50 && dy % 1 === 0 && !ev.shiftKey) zoomEn(ev.clientX - r.left, ev.clientY - r.top, Math.exp(-dy * .0015)); // rueda de ratón: zoom
      else { cam.x -= ev.shiftKey ? dy : dx; cam.y -= ev.shiftKey ? 0 : dy; aplicar(); } // trackpad: mover
    }, { passive: false });
    document.querySelectorAll("[data-zoom]").forEach(function (b) {
      b.addEventListener("click", function () {
        var t = b.getAttribute("data-zoom"), a = area();
        if (t === "fit") { encuadre(limites, 40); return; }
        var o = { f: 1 }, z0 = cam.z, x0 = cam.x, y0 = cam.y, cx = a.l + a.w / 2, cy = a.t + a.h / 2, f = t === "+" ? 1.5 : 1 / 1.5;
        G.to(o, { f: f, duration: .45, ease: "power3.out", onUpdate: function () { cam.z = z0; cam.x = x0; cam.y = y0; zoomEn(cx, cy, o.f); } });
      });
    });
    lienzo.addEventListener("keydown", function (ev) {
      var a = area(), k = ev.key, paso = 80;
      if (k === "ArrowLeft") cam.x += paso; else if (k === "ArrowRight") cam.x -= paso;
      else if (k === "ArrowUp") cam.y += paso; else if (k === "ArrowDown") cam.y -= paso;
      else if (k === "+" || k === "=") zoomEn(a.l + a.w / 2, a.t + a.h / 2, 1.25);
      else if (k === "-") zoomEn(a.l + a.w / 2, a.t + a.h / 2, .8);
      else if (k === "0") encuadre(limites, 40);
      else if (k === "Escape") seleccionar(null);
      else if (k === "Enter" && seleccion) abrir(seleccion);
      else return;
      ev.preventDefault(); aplicar();
    });
    window.addEventListener("resize", function () { aplicar(); });

    /* guía y cursor de Esteban */
    function ocultarGuia() { if (guia) guia.classList.add("oculta"); }
    var cursorActivo = true, tlCursor = null;
    function detenerCursor() {
      if (!cursorActivo) return; cursorActivo = false;
      if (tlCursor) tlCursor.kill();
      if (G && cursorEg) G.to(cursorEg, { opacity: 0, duration: .4 });
    }
    function puntoPantalla(el, fx, fy) {
      return { x: cam.x + (el.offsetLeft + el.offsetWidth * fx) * cam.z, y: cam.y + (el.offsetTop + el.offsetHeight * fy) * cam.z };
    }
    function pasearCursor() {
      if (!G || !cursorEg || reducido || tactil) return;
      var objetivos = [mundo.querySelector('[data-clave="intro"]'), mundo.querySelector('[data-clave="cv"]'), mundo.querySelector('[data-clave="contacto"]'), mundo.querySelector('[data-clave="perfil"]')].filter(Boolean);
      var i = 0;
      var p0 = puntoPantalla(objetivos[0], .82, .3);
      G.set(cursorEg, { x: p0.x, y: p0.y });
      G.to(cursorEg, { opacity: 1, duration: .5 });
      (function sig() {
        if (!cursorActivo) return;
        var el = objetivos[i % objetivos.length]; i++;
        var p = puntoPantalla(el, .3 + Math.random() * .5, .25 + Math.random() * .5);
        tlCursor = G.to(cursorEg, { x: p.x, y: p.y, duration: 1.6, ease: "power2.inOut", onComplete: function () {
          if (!cursorActivo) return;
          el.classList.add("sel"); dibujarMini();
          setTimeout(function () { if (seleccion !== el) el.classList.remove("sel"); }, 1400);
          tlCursor = G.delayedCall(2.1, sig);
        } });
      })();
    }

    /* arranque: vista general y vuelo a la presentación */
    var intro = mundo.querySelector('[data-clave="intro"]');
    var cvF = mundo.querySelector('[data-clave="cv"]');
    var foco = { x: intro.offsetLeft - 40, y: intro.offsetTop - 80, w: cvF.offsetLeft + cvF.offsetWidth - intro.offsetLeft + 80, h: intro.offsetHeight + 140 };
    if (movil()) foco = rectDe(intro);
    encuadre(limites, 20, 0);
    if (G && !reducido) {
      G.from(frames.concat(Array.prototype.slice.call(mundo.querySelectorAll(".m-sec, .nota"))), { opacity: 0, scale: .94, duration: .7, ease: "power3.out", stagger: { each: .025, from: "random" }, transformOrigin: "50% 50%" });
      G.delayedCall(1.1, function () { encuadre(foco, movil() ? 16 : 50, 1.6); });
      G.delayedCall(3.1, pasearCursor);
    } else { encuadre(foco, 40, 0); }
    aplicar();
  }

  /* ================================================================ páginas interiores ================================================================ */
  function iniciarPagina() {
    var lenis = null;
    if (window.Lenis && !reducido) {
      lenis = new Lenis({ lerp: .1, smoothWheel: true });
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
      if (window.ScrollTrigger) lenis.on("scroll", ScrollTrigger.update);
    }
    function reglas() {
      var a = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--rg")) || 0;
      dibujarRegla(rh, true, 0, 1);
      dibujarRegla(rv, false, -window.scrollY, 1);
    }
    var pend = false;
    function pedir() { if (!pend) { pend = true; requestAnimationFrame(function () { pend = false; reglas(); }); } }
    window.addEventListener("scroll", pedir, { passive: true });
    window.addEventListener("resize", pedir);
    window.addEventListener("pointermove", function (ev) {
      var rg = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--rg")) || 0;
      marca.x = ev.clientX - rg; marca.y = ev.clientY - (rv ? rv.getBoundingClientRect().top : 0); pedir();
    });
    reglas();
    if (document.fonts) document.fonts.ready.then(reglas);

    /* aparición de frames */
    if (G && window.ScrollTrigger && !reducido) {
      G.registerPlugin(ScrollTrigger);
      document.querySelectorAll(".pz, .fr-t, .recorrido, .servicios li, .cv-item, .ct-fr, .perfil-foto").forEach(function (el) {
        G.from(el, { y: 40, opacity: 0, duration: 1, ease: "expo.out", scrollTrigger: { trigger: el, start: "top 92%", once: true } });
      });
    }

    /* filtros del tablero con Flip */
    var tablero = document.querySelector("[data-tablero]");
    if (tablero) document.querySelectorAll("[data-filtro]").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-filtro");
        document.querySelectorAll("[data-filtro]").forEach(function (x) { x.classList.toggle("activo", x === b); x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        var items = tablero.querySelectorAll(".fr-t");
        var estado = window.Flip && !reducido ? Flip.getState(items) : null;
        items.forEach(function (it) { it.classList.toggle("oculto", f !== "todo" && it.getAttribute("data-cat") !== f); });
        if (estado) Flip.from(estado, { duration: .7, ease: "expo.inOut", absolute: true, onEnter: function (els) { return G.fromTo(els, { opacity: 0, scale: .9 }, { opacity: 1, scale: 1, duration: .5 }); }, onLeave: function (els) { return G.to(els, { opacity: 0, scale: .9, duration: .3 }); } });
        if (window.ScrollTrigger) ScrollTrigger.refresh();
      });
    });

    /* proyecto: inspector en móvil, capas activas, visor */
    var proyC = document.querySelector(".proy-c"), inspP = document.querySelector(".insp-p");
    if (proyC && inspP && movil()) proyC.querySelector(".proy-cab").after(inspP);
    var capas = document.querySelectorAll(".capas-p .cp-lista a");
    if (capas.length && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          capas.forEach(function (a) { a.classList.toggle("activo", a.getAttribute("href") === "#" + en.target.id); });
        });
      }, { rootMargin: "-45% 0px -45% 0px" });
      document.querySelectorAll(".piezas .pz").forEach(function (p) { io.observe(p); });
      capas.forEach(function (a) {
        a.addEventListener("click", function (ev) {
          var t = document.querySelector(a.getAttribute("href")); if (!t) return;
          ev.preventDefault(); if (lenis) lenis.scrollTo(t, { offset: -110 }); else t.scrollIntoView({ behavior: "smooth", block: "center" });
        });
      });
    }
    var lb = document.querySelector("[data-lb]");
    if (lb) {
      var imgs = Array.prototype.slice.call(document.querySelectorAll(".pz img")), i = 0;
      var lbImg = lb.querySelector("[data-lb-img]"), lbN = lb.querySelector("[data-lb-n]");
      var mostrar = function (k) { i = (k + imgs.length) % imgs.length; lbImg.src = imgs[i].src; lbN.textContent = (i + 1) + " / " + imgs.length; };
      imgs.forEach(function (im, k) { im.closest(".pz").addEventListener("click", function () { mostrar(k); lb.hidden = false; if (lenis) lenis.stop(); }); });
      var cerrar = function () { lb.hidden = true; if (lenis) lenis.start(); };
      lb.querySelector("[data-lb-x]").addEventListener("click", cerrar);
      lb.querySelector("[data-lb-a]").addEventListener("click", function () { mostrar(i - 1); });
      lb.querySelector("[data-lb-s]").addEventListener("click", function () { mostrar(i + 1); });
      lb.addEventListener("click", function (ev) { if (ev.target === lb) cerrar(); });
      document.addEventListener("keydown", function (ev) {
        if (lb.hidden) return;
        if (ev.key === "Escape") cerrar(); else if (ev.key === "ArrowLeft") mostrar(i - 1); else if (ev.key === "ArrowRight") mostrar(i + 1);
      });
    }

    /* copiar correo del currículum */
    document.querySelectorAll(".cv-correo").forEach(function (b) {
      b.addEventListener("click", function () { var t = b.textContent; b.textContent = "Correo copiado"; setTimeout(function () { b.textContent = t; }, 1600); });
    });
  }
})();
