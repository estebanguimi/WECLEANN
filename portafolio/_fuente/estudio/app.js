/* ESTUDIO · motor: retícula que se dibuja, panel de transición numerado, visor WebGL con disolución de ruido,
   índice desplegable, cambio lista/cuadrícula con Flip y textos por líneas. */
(function () {
  "use strict";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fino = matchMedia("(hover: hover) and (pointer: fine)").matches;
  var G = window.gsap, ST = window.ScrollTrigger;
  if (!G) return;
  if (ST) G.registerPlugin(ST);
  if (window.Flip) G.registerPlugin(window.Flip);

  var lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ lerp: 0.09 });
    if (ST) lenis.on("scroll", ST.update);
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
  }

  /* ---------- Texto por líneas ---------- */
  function lineas(el) {
    var tieneBr = el.querySelector("br"), hijos = el.children.length && !tieneBr && el.children[0].tagName === "SPAN";
    if (hijos) {
      Array.prototype.slice.call(el.children).forEach(function (c) {
        var w = document.createElement("span"); w.className = "ln"; el.replaceChild(w, c); w.appendChild(c);
      });
    } else if (tieneBr) {
      var partes = el.innerHTML.split(/<br\s*\/?>/i);
      el.innerHTML = partes.map(function (p) { return '<span class="ln"><span>' + p.trim() + "</span></span>"; }).join("");
    } else {
      el.innerHTML = el.textContent.trim().split(/\s+/).map(function (w) { return '<span class="ln" style="display:inline-block"><span>' + w + "</span></span>"; }).join(" ");
    }
    return el.querySelectorAll(".ln > span");
  }
  var grupos = G.utils.toArray("[data-lineas]").map(function (el) { return { el: el, ls: lineas(el) }; });
  if (!reduce) grupos.forEach(function (g) { G.set(g.ls, { yPercent: 105 }); });
  function revelar(g, d) { G.to(g.ls, { yPercent: 0, duration: 1.2, ease: "expo.out", stagger: .07, delay: d || 0 }); }

  /* ---------- Rodillo en botones ---------- */
  document.querySelectorAll("[data-roll]").forEach(function (el) {
    var s = el.querySelector(":scope > span:not(.mono):not(.sig-img):not(.sig-t)");
    if (!s) return;
    var t = s.textContent;
    s.innerHTML = '<span class="roll"><span>' + t + "</span><span>" + t + "</span></span>";
  });

  /* ---------- Retícula ---------- */
  var ret = document.querySelector("[data-reticula-el]");
  var verRet = function () { ret.classList.toggle("ver"); };
  document.addEventListener("keydown", function (ev) { if ((ev.key === "g" || ev.key === "G") && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) verRet(); });
  var bret = document.querySelector("[data-reticula]");
  if (bret) bret.addEventListener("click", verRet);

  /* ---------- Panel de transición ---------- */
  var panel = document.querySelector("[data-panel]");
  var pn = document.querySelector("[data-panel-n]"), pt = document.querySelector("[data-panel-t]");
  function entrar() {
    var tl = G.timeline();
    if (!reduce) {
      tl.from(pt, { yPercent: 40, opacity: 0, duration: .5, ease: "expo.out" })
        .to(panel, { yPercent: -100, duration: 1, ease: "expo.inOut" }, "+=.15")
        .add(function () { panel.style.pointerEvents = "none"; });
      ret.classList.add("intro");
      tl.fromTo(ret.children, { scaleY: 0 }, { scaleY: 1, duration: 1, ease: "expo.inOut", stagger: .04 }, "-=.7")
        .add(function () { ret.classList.remove("intro"); }, "+=.2")
        .add(function () { grupos.forEach(function (g, i) { if (g.el.getBoundingClientRect().top < innerHeight) revelar(g, i * .1); }); }, "-=1.3");
      tl.from(".hero-meta, .visor-wrap, .p-portada, .pag-intro, .herr-barra", { opacity: 0, y: 30, duration: 1, ease: "expo.out", stagger: .08 }, "-=.9");
    } else { G.set(panel, { yPercent: -100 }); }
    if (ST && !reduce) grupos.forEach(function (g) {
      if (g.el.getBoundingClientRect().top >= innerHeight) ST.create({ trigger: g.el, start: "top 85%", once: true, onEnter: function () { revelar(g); } });
    });
  }
  function salir(href, n, t) {
    if (reduce) { location.href = href; return; }
    pn.textContent = n; pt.textContent = t;
    panel.style.pointerEvents = "auto";
    G.set(panel, { yPercent: 100 }); G.set(pt, { yPercent: 0, opacity: 1 });
    G.timeline({ onComplete: function () { location.href = href; } })
      .to(panel, { yPercent: 0, duration: .8, ease: "expo.inOut" })
      .from(pt, { yPercent: 60, opacity: 0, duration: .5, ease: "expo.out" }, "-=.3");
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[href]");
    if (!a || a.target === "_blank" || ev.metaKey || ev.ctrlKey) return;
    var h = a.getAttribute("href");
    if (!/\.html$/.test(h) || /^https?:/.test(h)) return;
    ev.preventDefault();
    var n = a.getAttribute("data-n") || (a.querySelector(".mono") ? a.querySelector(".mono").textContent.replace(/\D/g, "").slice(0, 2) : "");
    var tEl = a.querySelector(".ix-t, .it-t, .sig-t, .pal-t") || a;
    var t = tEl.textContent.replace(/^\d+/, "").replace(/\s+/g, " ").trim();
    salir(h, n, t.slice(0, 34));
  });
  addEventListener("pageshow", function (ev) { if (ev.persisted) { G.set(panel, { yPercent: -100 }); panel.style.pointerEvents = "none"; } });

  /* ---------- Reloj ---------- */
  var reloj = document.querySelector("[data-reloj]");
  var hora = function () { try { reloj.textContent = new Intl.DateTimeFormat("es", { hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: "America/New_York" }).format(new Date()) + " EST"; } catch (e) {} };
  if (reloj) { hora(); setInterval(hora, 1000); }

  /* ---------- Visor WebGL ---------- */
  var visor = document.querySelector("[data-visor]");
  if (visor) iniciarVisor(visor);
  function iniciarVisor(fig) {
    var datos = JSON.parse(document.querySelector("[data-visor-datos]").textContent);
    var cv = fig.querySelector("[data-gl]"), gl = cv.getContext("webgl");
    var vn = fig.querySelector("[data-v-n]"), vt = fig.querySelector("[data-v-t]"), vc = fig.querySelector("[data-v-c]"), barra = fig.querySelector("[data-v-barra]");
    var lista = document.querySelectorAll("[data-visor-lista] a");
    var actual = 0, enCurso = false, auto;
    function marcarLista(i) { lista.forEach(function (a, k) { a.classList.toggle("activo", k === i); }); }
    function rotulo(i) {
      var d = datos[i];
      vn.textContent = (i < 9 ? "0" : "") + (i + 1) + " / " + datos.length;
      G.fromTo([vt, vc], { yPercent: 100, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .6, ease: "expo.out", stagger: .05 });
      vt.textContent = d.t; vc.textContent = d.c;
      fig.onclick = function () { location.href = d.slug + ".html"; };
      fig.style.cursor = "pointer";
    }
    marcarLista(0); rotulo(0);
    if (!gl) return;
    var vs = "attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;gl_Position=vec4(p,0.,1.);}";
    var fs = [
      "precision highp float;varying vec2 v;uniform sampler2D a;uniform sampler2D b;uniform vec2 ra;uniform vec2 rb;uniform vec2 r;uniform float k;",
      "float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}",
      "float n(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1,0)),u.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),u.x),u.y);}",
      "vec2 cub(vec2 uv,vec2 ir){float ca=r.x/r.y,ia=ir.x/ir.y;vec2 s=ca>ia?vec2(1.,ia/ca):vec2(ca/ia,1.);return (uv-.5)*s+.5;}",
      "void main(){vec2 uv=vec2(v.x,1.-v.y);",
      " float ns=n(uv*vec2(r.x/r.y,1.)*4.)*.6+n(uv*18.)*.4;",
      " float f=ns*.8+uv.x*.2; float th=k*1.24-.12;",
      " float t=1.-smoothstep(th-.015,th+.015,f);",
      " vec3 ca=texture2D(a,cub(uv+vec2(.05*(1.-k)*(ns-.5)),ra)).rgb;",
      " vec3 cb=texture2D(b,cub(uv-vec2(.05*k*(ns-.5)),rb)).rgb;",
      " vec3 col=mix(cb,ca,t);",
      " float e=1.-smoothstep(0.,.03,abs(f-th));",
      " col=mix(col,vec3(1.,.3,.11),e*step(.001,k)*step(k,.999));",
      " gl_FragColor=vec4(col,1.);}"].join("\n");
    function sh(tp, s) { var o = gl.createShader(tp); gl.shaderSource(o, s); gl.compileShader(o); return o; }
    var pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var bf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var lp = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ["a", "b", "ra", "rb", "r", "k"].forEach(function (x) { U[x] = gl.getUniformLocation(pr, x); });
    gl.uniform1i(U.a, 0); gl.uniform1i(U.b, 1);
    var tex = [], tam = [];
    function cargar(i, cb) {
      if (tex[i]) { cb(); return; }
      var im = new Image();
      im.onload = function () {
        var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, im);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        tex[i] = t; tam[i] = [im.width, im.height]; cb();
      };
      im.src = datos[i].src;
    }
    function medir() { var dpr = Math.min(devicePixelRatio || 1, 2); cv.width = cv.clientWidth * dpr; cv.height = cv.clientHeight * dpr; gl.viewport(0, 0, cv.width, cv.height); }
    medir(); addEventListener("resize", function () { medir(); dibujar(1); });
    var desde = 0, hacia = 0;
    function dibujar(k) {
      if (!tex[desde] || !tex[hacia]) return;
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex[hacia]);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, tex[desde]);
      gl.uniform2f(U.ra, tam[hacia][0], tam[hacia][1]); gl.uniform2f(U.rb, tam[desde][0], tam[desde][1]);
      gl.uniform2f(U.r, cv.width, cv.height); gl.uniform1f(U.k, k);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    function ir(i) {
      if (i === actual || enCurso) return;
      enCurso = true;
      cargar(i, function () {
        desde = actual; hacia = i; actual = i;
        marcarLista(i); rotulo(i);
        var o = { k: 0 };
        G.to(o, { k: 1, duration: reduce ? .01 : 1.3, ease: "power2.inOut", onUpdate: function () { dibujar(o.k); }, onComplete: function () { enCurso = false; } });
        cargar((i + 1) % datos.length, function () {});
      });
    }
    cargar(0, function () { desde = hacia = 0; fig.classList.add("gl"); dibujar(1); cargar(1, function () {}); arrancarAuto(); });
    function arrancarAuto() {
      if (auto) auto.kill();
      if (reduce) return;
      G.set(barra, { scaleX: 0 });
      auto = G.to(barra, { scaleX: 1, duration: 4.2, ease: "none", onComplete: function () { ir((actual + 1) % datos.length); arrancarAuto(); } });
    }
    lista.forEach(function (a, i) { a.addEventListener("pointerenter", function () { ir(i); arrancarAuto(); }); a.addEventListener("focus", function () { ir(i); }); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { if (auto) { if (en[0].isIntersecting) auto.resume(); else auto.pause(); } }).observe(fig);
  }

  /* ---------- Índice desplegable ---------- */
  if (fino && !reduce) document.querySelectorAll("[data-ix]").forEach(function (f) {
    var tira = f.querySelector("[data-ix-tira]");
    f.addEventListener("pointerenter", function () { G.to(tira, { height: "auto", duration: .6, ease: "expo.out" }); G.fromTo(tira.querySelectorAll("img"), { yPercent: 30, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .6, ease: "expo.out", stagger: .04 }); });
    f.addEventListener("pointerleave", function () { G.to(tira, { height: 0, duration: .5, ease: "expo.inOut" }); });
  });

  /* ---------- Lista / cuadrícula + filtros con Flip ---------- */
  var items = document.querySelector("[data-items]");
  if (items) {
    var its = items.querySelectorAll(".it");
    var flip = function (cambio) {
      var est = window.Flip ? Flip.getState(items.querySelectorAll(".it, .it-img, .it-t")) : null;
      cambio();
      if (est && !reduce) Flip.from(est, { duration: .9, ease: "expo.inOut", nested: true, absolute: false, stagger: .015,
        onEnter: function (els) { return G.fromTo(els, { opacity: 0 }, { opacity: 1, duration: .4 }); },
        onLeave: function (els) { return G.to(els, { opacity: 0, duration: .3 }); } });
      if (ST) setTimeout(function () { ST.refresh(); }, 950);
    };
    document.querySelectorAll("[data-vista]").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-vista");
        document.querySelectorAll("[data-vista]").forEach(function (x) { x.classList.toggle("activo", x === b); x.setAttribute("aria-pressed", String(x === b)); });
        flip(function () { items.classList.toggle("vista-lista", v === "lista"); items.classList.toggle("vista-cuadricula", v === "cuadricula"); });
      });
    });
    document.querySelectorAll("[data-filtro]").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-filtro");
        document.querySelectorAll("[data-filtro]").forEach(function (x) { x.classList.toggle("activo", x === b); x.setAttribute("aria-pressed", String(x === b)); });
        flip(function () { its.forEach(function (it) { it.classList.toggle("oculta", f !== "todo" && it.getAttribute("data-cat") !== f); }); });
      });
    });
  }

  /* ---------- Apariciones ---------- */
  if (ST && !reduce) {
    ST.batch(".mod, .it, .servicios li, .herrs li, .cv tr, .ct-tabla div, .p-datos div", { start: "top 94%", onEnter: function (b) { G.from(b, { opacity: 0, y: 40, duration: 1, ease: "expo.out", stagger: .05 }); } });
    ST.batch(".ix-fila, .pal-f, .pal-sw", { start: "top 94%", onEnter: function (b) { G.from(b, { opacity: 0, x: -30, duration: .9, ease: "expo.out", stagger: .04 }); } });
    G.utils.toArray(".mod img").forEach(function (im) { G.from(im, { clipPath: "inset(100% 0 0 0)", duration: 1.3, ease: "expo.inOut", scrollTrigger: { trigger: im, start: "top 92%" } }); });
    G.utils.toArray("[data-portada] img").forEach(function (im) {
      G.fromTo(im, { scale: 1.2 }, { scale: 1, yPercent: 6, ease: "none", scrollTrigger: { trigger: im.closest("[data-portada]"), start: "top bottom", end: "bottom top", scrub: true } });
    });
    var pc = document.querySelector(".pie-correo");
    if (pc) G.from(pc, { yPercent: 50, opacity: 0, duration: 1.2, ease: "expo.out", scrollTrigger: { trigger: pc, start: "top 95%" } });
    document.querySelectorAll("[data-contar]").forEach(function (el) {
      var fin = parseInt(el.getAttribute("data-contar"), 10), o = { v: 0 };
      el.textContent = "0";
      ST.create({ trigger: el, start: "top 95%", once: true, onEnter: function () { G.to(o, { v: fin, duration: 2, ease: "expo.out", delay: .8, onUpdate: function () { el.textContent = Math.round(o.v); } }); } });
    });
  }

  /* ---------- Lightbox ---------- */
  var lb = document.querySelector("[data-lb]"), gal = document.querySelector("[data-galeria]");
  if (lb && gal) {
    var srcs = Array.prototype.map.call(gal.querySelectorAll("img"), function (i) { return i.getAttribute("src"); });
    var li = lb.querySelector("[data-lb-img]"), ln = lb.querySelector("[data-lb-n]"), j = 0;
    var ver = function (i) { j = (i + srcs.length) % srcs.length; li.src = srcs[j]; ln.textContent = (j + 1 < 10 ? "0" : "") + (j + 1) + " / " + srcs.length; G.fromTo(li, { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: .7, ease: "expo.out" }); };
    var cerrar = function () { lb.hidden = true; if (lenis) lenis.start(); };
    gal.addEventListener("click", function (ev) { var m = ev.target.closest(".mod"); if (m) { lb.hidden = false; if (lenis) lenis.stop(); ver(parseInt(m.getAttribute("data-i"), 10)); } });
    lb.querySelector("[data-lb-x]").addEventListener("click", cerrar);
    lb.querySelector("[data-lb-a]").addEventListener("click", function () { ver(j - 1); });
    lb.querySelector("[data-lb-s]").addEventListener("click", function () { ver(j + 1); });
    document.addEventListener("keydown", function (ev) { if (lb.hidden) return; if (ev.key === "Escape") cerrar(); if (ev.key === "ArrowRight") ver(j + 1); if (ev.key === "ArrowLeft") ver(j - 1); });
  }

  /* ---------- Copiar ---------- */
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function (ev) {
      ev.preventDefault(); ev.stopPropagation();
      var txt = b.getAttribute("data-copiar");
      var et = b.querySelector(".mono") || b;
      var orig = et.textContent;
      var ok = function () { et.textContent = "Copiado"; setTimeout(function () { et.textContent = orig; }, 1400); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () {}); else ok();
    });
  });

  var ya = false, go = function () { if (ya) return; ya = true; entrar(); if (ST) ST.refresh(); };
  if (document.readyState === "complete") go(); else { addEventListener("load", go); setTimeout(go, 2500); }
})();
