/* LUZ · motor de la web: foco WebGL, scroll suave, transiciones de cortina, setlist y galería horizontal. */
(function () {
  "use strict";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fino = matchMedia("(hover: hover) and (pointer: fine)").matches;
  var G = window.gsap, ST = window.ScrollTrigger;
  if (G && ST) G.registerPlugin(ST);
  if (G && window.Flip) G.registerPlugin(window.Flip);

  /* ---------- Scroll suave ---------- */
  var lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 0.9 });
    if (ST) lenis.on("scroll", ST.update);
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
  }

  /* ---------- Cortina: entrada y salida de página ---------- */
  var cortina = document.querySelector("[data-cortina]");
  var cortinaT = document.querySelector("[data-cortina-t]");
  var primera = false;
  try { primera = !sessionStorage.getItem("luz-visto"); sessionStorage.setItem("luz-visto", "1"); } catch (e) {}

  function entrar() {
    if (!G || !cortina) { if (cortina) cortina.style.display = "none"; animarEntrada(); return; }
    var tl = G.timeline({ onComplete: function () { cortina.style.pointerEvents = "none"; } });
    if (primera && document.body.classList.contains("pg-inicio")) {
      cortinaT.textContent = "Esteban Guillen";
      tl.to(".cortina-linea", { scaleX: 1, duration: 1.1, ease: "expo.inOut" })
        .to(cortinaT, { opacity: 1, y: 0, duration: .8, ease: "expo.out" }, "-=.4")
        .to(cortinaT, { opacity: 0, y: -20, duration: .5, ease: "power2.in" }, "+=.35");
    } else {
      G.set(".cortina-linea", { scaleX: 1 });
    }
    tl.to(".cortina-linea", { scaleX: 0, transformOrigin: "right", duration: .5, ease: "power3.in" })
      .to(cortina, { yPercent: -100, duration: 1, ease: "expo.inOut" }, "-=.15")
      .add(animarEntrada, "-=.55");
  }

  function salir(href, titulo) {
    if (!G || reduce) { location.href = href; return; }
    cortina.style.pointerEvents = "auto";
    cortinaT.textContent = titulo || "";
    G.set(cortina, { yPercent: 100 });
    G.set(".cortina-linea", { scaleX: 0, transformOrigin: "left" });
    G.set(cortinaT, { opacity: 0, y: 20 });
    G.timeline({ onComplete: function () { location.href = href; } })
      .to(cortina, { yPercent: 0, duration: .8, ease: "expo.inOut" })
      .to(".cortina-linea", { scaleX: 1, duration: .5, ease: "expo.out" }, "-=.2")
      .to(cortinaT, { opacity: 1, y: 0, duration: .4, ease: "expo.out" }, "-=.35");
  }

  document.addEventListener("click", function (ev) {
    var a = ev.target.closest("a[href]");
    if (!a || a.target === "_blank" || ev.metaKey || ev.ctrlKey || ev.shiftKey) return;
    var href = a.getAttribute("href");
    if (!/\.html(#.*)?$/.test(href) || /^https?:/.test(href)) return;
    ev.preventDefault();
    var t = a.querySelector(".set-t, .sig-t, b, .video-t");
    salir(href, (t ? t.textContent : a.textContent).trim().slice(0, 40));
  });
  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted && cortina && G) { G.set(cortina, { yPercent: -100 }); cortina.style.pointerEvents = "none"; }
  });

  /* ---------- Texto partido ---------- */
  function partir(el) {
    var nodos = Array.prototype.slice.call(el.childNodes);
    el.innerHTML = "";
    nodos.forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { el.appendChild(document.createTextNode(" ")); return; }
          var o = document.createElement("span"); o.className = "pal";
          var i = document.createElement("span"); i.textContent = w; o.appendChild(i); el.appendChild(o);
        });
      } else if (n.nodeType === 1) {
        if (n.tagName === "BR") { el.appendChild(n); return; }
        var c = n.cloneNode(false); el.appendChild(c);
        partirEn(n, c);
      }
    });
  }
  function partirEn(origen, destino) {
    Array.prototype.forEach.call(origen.childNodes, function (n) {
      if (n.nodeType === 1) { var c = n.cloneNode(false); destino.appendChild(c); partirEn(n, c); return; }
      n.textContent.split(/(\s+)/).forEach(function (w) {
        if (!w) return;
        if (/^\s+$/.test(w)) { destino.appendChild(document.createTextNode(" ")); return; }
        var o = document.createElement("span"); o.className = "pal";
        var i = document.createElement("span"); i.textContent = w; o.appendChild(i); destino.appendChild(o);
      });
    });
  }
  var partidos = document.querySelectorAll("[data-partir]");
  partidos.forEach(partir);
  if (G && !reduce) G.set("[data-partir] .pal > span", { yPercent: 110 });

  function animarEntrada() {
    if (!G || reduce) return;
    G.to("[data-partir] .pal > span", { yPercent: 0, duration: 1.3, ease: "expo.out", stagger: .06 });
    G.from(".hero-sup, .hero-inf, .p-hero-txt .eti", { opacity: 0, y: 20, duration: 1, ease: "expo.out", delay: .35, stagger: .1 });
    G.from(".cab", { opacity: 0, duration: 1, delay: .2 });
  }

  /* ---------- Palabras que se iluminan con el scroll ---------- */
  document.querySelectorAll("[data-iluminar]").forEach(function (el) {
    var palabras = el.textContent.trim().split(/\s+/);
    el.innerHTML = palabras.map(function (w) { return '<span class="ilum">' + w + "</span>"; }).join(" ");
    var spans = el.querySelectorAll(".ilum");
    if (!ST || reduce) { spans.forEach(function (s) { s.style.opacity = 1; }); return; }
    ST.create({
      trigger: el, start: "top 80%", end: "bottom 45%", scrub: true,
      onUpdate: function (st) {
        var n = st.progress * spans.length;
        spans.forEach(function (s, i) { s.style.opacity = Math.min(1, Math.max(.14, n - i + .14)); });
      }
    });
  });

  /* ---------- Cursor ---------- */
  var cur = document.querySelector("[data-cursor-el]");
  if (cur && fino && G) {
    var cx = G.quickTo(cur, "x", { duration: .45, ease: "power3" }), cy = G.quickTo(cur, "y", { duration: .45, ease: "power3" });
    var etiquetas = { ver: "Ver", ir: "Ir", siguiente: "Siguiente", escribir: "Escribir", copiar: "Copiar" };
    window.addEventListener("pointermove", function (ev) { cur.style.opacity = 1; cx(ev.clientX); cy(ev.clientY); });
    document.addEventListener("pointerover", function (ev) {
      var t = ev.target.closest("[data-cursor]");
      if (t) { cur.classList.add("grande"); cur.firstElementChild.textContent = etiquetas[t.getAttribute("data-cursor")] || ""; }
    });
    document.addEventListener("pointerout", function (ev) {
      var t = ev.target.closest("[data-cursor]");
      if (t && !t.contains(ev.relatedTarget)) cur.classList.remove("grande");
    });
  }

  /* ---------- Cabecera y reloj ---------- */
  var cab = document.querySelector("[data-cab]");
  var ultimoY = 0;
  function alScroll(y) {
    if (!cab) return;
    if (y > ultimoY + 4 && y > 200) cab.classList.add("oculta");
    else if (y < ultimoY - 4) cab.classList.remove("oculta");
    ultimoY = y;
  }
  if (lenis) lenis.on("scroll", function (l) { alScroll(l.scroll); });
  else window.addEventListener("scroll", function () { alScroll(scrollY); }, { passive: true });
  var reloj = document.querySelector("[data-reloj]");
  function hora() {
    try { reloj.textContent = "Miami " + new Intl.DateTimeFormat("es", { hour: "2-digit", minute: "2-digit", timeZone: "America/New_York" }).format(new Date()); } catch (e) {}
  }
  if (reloj) { hora(); setInterval(hora, 20000); }

  /* ---------- Foco WebGL del hero ---------- */
  var lienzo = document.querySelector("[data-foco]");
  if (lienzo) iniciarFoco(lienzo);

  function iniciarFoco(cv) {
    var gl = cv.getContext("webgl", { premultipliedAlpha: false, antialias: false });
    if (!gl) return;
    var vs = "attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;gl_Position=vec4(p,0.,1.);}";
    var fs = [
      "precision highp float;varying vec2 v;uniform sampler2D t;uniform vec2 r;uniform vec2 ir;uniform vec2 m;uniform float tm;uniform float ini;",
      "float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}",
      "void main(){",
      " vec2 uv=v; uv.y=1.-uv.y;",
      " float ra=r.x/r.y, ia=ir.x/ir.y; vec2 s=ra>ia?vec2(1.,ia/ra):vec2(ra/ia,1.); vec2 tu=(uv-.5)*s+.5;",
      " vec3 c=texture2D(t,tu).rgb;",
      " vec2 a=vec2(ra,1.); vec2 P=uv*a; vec2 M=m*a; vec2 F=vec2((m.x*.5+.25)*ra,-.12);",
      " vec2 d=M-F; float k=clamp(dot(P-F,d)/dot(d,d),0.,1.25); float dist=length(P-(F+d*k));",
      " float w=mix(.015,.2,k); float haz=smoothstep(w,w*.15,dist)*smoothstep(0.,.25,k)*(1.-smoothstep(1.05,1.25,k));",
      " float pool=smoothstep(.44,.0,length(P-M));",
      " float luz=clamp(haz*.55+pool*1.1,0.,1.);",
      " float lum=dot(c,vec3(.299,.587,.114));",
      " vec3 base=c*.2+vec3(lum)*.04;",
      " vec3 lit=c*1.32+vec3(1.,.71,.28)*pool*.06;",
      " vec3 col=mix(base,lit,luz)+vec3(1.,.71,.28)*haz*.07;",
      " col*=mix(.55,1.,ini)+ini*0.;",
      " col+= (h(uv*r+tm)-.5)*.06;",
      " float vig=smoothstep(1.25,.35,length((uv-.5)*vec2(ra*.8,1.)));",
      " gl_FragColor=vec4(col*vig,1.);",
      "}"].join("\n");
    function sh(tp, src) { var s = gl.createShader(tp); gl.shaderSource(s, src); gl.compileShader(s); return s; }
    var pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
    gl.useProgram(pr);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var lp = gl.getAttribLocation(pr, "p"); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ["t", "r", "ir", "m", "tm", "ini"].forEach(function (n) { U[n] = gl.getUniformLocation(pr, n); });
    var tex = gl.createTexture();
    var im = new Image();
    var obj = { x: .62, y: .55 }, act = { x: .62, y: .55 }, ini = { v: 0 }, ultimoMov = 0, visible = true;
    im.onload = function () {
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, im);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.uniform2f(U.ir, im.width, im.height);
      cv.closest("[data-hero]").classList.add("gl-listo");
      if (G) G.to(ini, { v: 1, duration: 2.4, ease: "power2.out", delay: .6 }); else ini.v = 1;
      requestAnimationFrame(cuadro);
    };
    im.src = cv.getAttribute("data-src");
    function medir() {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.75);
      cv.width = Math.round(cv.clientWidth * dpr); cv.height = Math.round(cv.clientHeight * dpr);
      gl.viewport(0, 0, cv.width, cv.height);
    }
    medir(); window.addEventListener("resize", medir);
    var hero = cv.closest("[data-hero]");
    hero.addEventListener("pointermove", function (ev) {
      var r = cv.getBoundingClientRect();
      obj.x = (ev.clientX - r.left) / r.width; obj.y = (ev.clientY - r.top) / r.height; ultimoMov = performance.now();
    });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) requestAnimationFrame(cuadro); }).observe(cv);
    function cuadro(t) {
      if (!visible) return;
      if (t - ultimoMov > 2600 || !fino) { // deriva sola cuando nadie la mueve
        obj.x = .5 + Math.sin(t * .00023) * .3; obj.y = .5 + Math.sin(t * .00037 + 1.3) * .18;
      }
      var f = reduce ? 1 : .07;
      act.x += (obj.x - act.x) * f; act.y += (obj.y - act.y) * f;
      gl.uniform2f(U.r, cv.width, cv.height);
      gl.uniform2f(U.m, act.x, act.y);
      gl.uniform1f(U.tm, (t * .001) % 10);
      gl.uniform1f(U.ini, ini.v);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      requestAnimationFrame(cuadro);
    }
  }

  /* ---------- Setlist: imagen que sigue al cursor ---------- */
  document.querySelectorAll("[data-setlist]").forEach(function (lista) {
    var prev = lista.querySelector("[data-set-prev]");
    if (!prev || !fino || !G) return;
    var img = prev.querySelector("img");
    var px = G.quickTo(prev, "x", { duration: .6, ease: "power3" }), py = G.quickTo(prev, "y", { duration: .6, ease: "power3" });
    lista.querySelectorAll(".set-fila").forEach(function (f) {
      f.addEventListener("pointerenter", function () { img.src = f.getAttribute("data-prev"); lista.classList.add("activo"); });
    });
    lista.addEventListener("pointerleave", function () { lista.classList.remove("activo"); });
    lista.addEventListener("pointermove", function (ev) { px(ev.clientX + 30); py(ev.clientY - 180); });
  });

  /* ---------- Galería horizontal en vivo ---------- */
  var hz = document.querySelector("[data-horizontal]");
  if (hz && ST && !reduce && innerWidth > 820) {
    var pista = hz.querySelector("[data-pista]");
    var barra = hz.querySelector("[data-barra]");
    var dist = function () { return pista.scrollWidth - innerWidth; };
    var mov = G.to(pista, {
      x: function () { return -dist(); }, ease: "none",
      scrollTrigger: { trigger: hz, pin: ".vivo-pin", start: "top top", end: function () { return "+=" + dist(); }, scrub: 1, invalidateOnRefresh: true,
        onUpdate: function (s) { barra.style.transform = "scaleX(" + s.progress + ")"; } }
    });
    pista.querySelectorAll(".vivo-marco img").forEach(function (im) {
      G.fromTo(im, { xPercent: -6 }, { xPercent: 6, ease: "none", scrollTrigger: { trigger: im.parentNode, containerAnimation: mov, start: "left right", end: "right left", scrub: true } });
    });
  }

  /* ---------- Contadores ---------- */
  document.querySelectorAll("[data-contar]").forEach(function (el) {
    var fin = parseFloat(el.getAttribute("data-contar"));
    if (!ST || reduce) return;
    var o = { v: 0 };
    el.textContent = "0";
    ST.create({ trigger: el, start: "top 88%", once: true, onEnter: function () {
      G.to(o, { v: fin, duration: 2.2, ease: "power3.out", onUpdate: function () { el.textContent = Math.round(o.v).toLocaleString("es"); } });
    } });
  });

  /* ---------- Apariciones ---------- */
  if (G && ST && !reduce) {
    G.utils.toArray(".set-fila, .serv, .cifra, .dato, .video-card, .tarjeta, .exp li, .contacto-cols > div").forEach(function (el) {
      G.from(el, { opacity: 0, y: 40, duration: 1.1, ease: "expo.out", scrollTrigger: { trigger: el, start: "top 92%" } });
    });
    G.utils.toArray(".g-item img").forEach(function (im) {
      G.fromTo(im, { scale: 1.18, yPercent: -4 }, { scale: 1.02, yPercent: 4, ease: "none", scrollTrigger: { trigger: im.parentNode, start: "top bottom", end: "bottom top", scrub: true } });
      G.from(im.parentNode, { clipPath: "inset(12% 0 12% 0)", duration: 1.4, ease: "expo.out", scrollTrigger: { trigger: im.parentNode, start: "top 90%" } });
    });
    var ph = document.querySelector("[data-p-hero]");
    if (ph) {
      G.to(ph.querySelector(".p-hero-img"), { clipPath: "inset(6% 4% 0% 4%)", ease: "none", scrollTrigger: { trigger: ph, start: "top top", end: "bottom top", scrub: true } });
      G.to(ph.querySelector(".p-hero-img img"), { scale: 1.15, yPercent: 8, ease: "none", scrollTrigger: { trigger: ph, start: "top top", end: "bottom top", scrub: true } });
      G.to(ph.querySelector(".p-hero-txt"), { yPercent: -30, opacity: 0, ease: "none", scrollTrigger: { trigger: ph, start: "40% top", end: "bottom top", scrub: true } });
    }
    var hr = document.querySelector("[data-hero] .hero-t");
    if (hr) G.to(hr, { yPercent: -25, opacity: .2, ease: "none", scrollTrigger: { trigger: "[data-hero]", start: "top top", end: "bottom top", scrub: true } });
  }

  /* ---------- Filtros de trabajo con Flip ---------- */
  var mosaico = document.querySelector("[data-mosaico]");
  if (mosaico) {
    var botones = document.querySelectorAll("[data-filtro]");
    var tarjetas = mosaico.querySelectorAll(".tarjeta");
    botones.forEach(function (bt) {
      bt.addEventListener("click", function () {
        var f = bt.getAttribute("data-filtro");
        var estado = window.Flip ? Flip.getState(tarjetas) : null;
        botones.forEach(function (x) { x.classList.toggle("activo", x === bt); x.setAttribute("aria-pressed", String(x === bt)); });
        tarjetas.forEach(function (t) { t.classList.toggle("oculta", f !== "todo" && t.getAttribute("data-cat") !== f); });
        if (estado && !reduce) Flip.from(estado, { duration: .8, ease: "expo.inOut", absolute: true, onEnter: function (els) { return G.fromTo(els, { opacity: 0, scale: .9 }, { opacity: 1, scale: 1, duration: .6 }); }, onLeave: function (els) { return G.to(els, { opacity: 0, scale: .9, duration: .4 }); } });
        if (ST) ST.refresh();
      });
    });
  }

  /* ---------- Visor de imágenes ---------- */
  var visor = document.querySelector("[data-visor]");
  var gal = document.querySelector("[data-galeria]");
  if (visor && gal) {
    var imgs = Array.prototype.map.call(gal.querySelectorAll("img"), function (i) { return i.getAttribute("src"); });
    var vi = visor.querySelector("[data-visor-img]"), vn = visor.querySelector("[data-visor-n]"), idx = 0;
    var mostrar = function (i) { idx = (i + imgs.length) % imgs.length; vi.src = imgs[idx]; vn.textContent = (idx + 1) + " / " + imgs.length; };
    var abrir = function (i) { mostrar(i); visor.hidden = false; if (lenis) lenis.stop(); if (G) G.fromTo(vi, { opacity: 0, scale: .96 }, { opacity: 1, scale: 1, duration: .6, ease: "expo.out" }); };
    var cerrar = function () { visor.hidden = true; if (lenis) lenis.start(); };
    gal.addEventListener("click", function (ev) { var f = ev.target.closest(".g-item"); if (f) abrir(parseInt(f.getAttribute("data-i"), 10)); });
    visor.querySelector("[data-visor-cerrar]").addEventListener("click", cerrar);
    visor.querySelector("[data-visor-ant]").addEventListener("click", function () { mostrar(idx - 1); });
    visor.querySelector("[data-visor-sig]").addEventListener("click", function () { mostrar(idx + 1); });
    visor.addEventListener("click", function (ev) { if (ev.target === visor) cerrar(); });
    document.addEventListener("keydown", function (ev) {
      if (visor.hidden) return;
      if (ev.key === "Escape") cerrar(); else if (ev.key === "ArrowRight") mostrar(idx + 1); else if (ev.key === "ArrowLeft") mostrar(idx - 1);
    });
  }

  /* ---------- Retrato con foco ---------- */
  var fs = document.querySelector("[data-foco-css]");
  if (fs) {
    var base = fs.querySelector("img");
    var luz = base.cloneNode(); luz.className = "luz-img"; luz.alt = ""; fs.insertBefore(luz, base.nextSibling);
    fs.addEventListener("pointermove", function (ev) {
      var r = base.getBoundingClientRect();
      fs.style.setProperty("--mx", (ev.clientX - r.left) + "px"); fs.style.setProperty("--my", (ev.clientY - r.top) + "px");
    });
  }

  /* ---------- Luz del pie ---------- */
  var pie = document.querySelector("[data-pie]");
  if (pie) pie.addEventListener("pointermove", function (ev) {
    var r = pie.getBoundingClientRect();
    pie.style.setProperty("--px", (ev.clientX - r.left) + "px"); pie.style.setProperty("--py", (ev.clientY - r.top) + "px");
  });

  /* ---------- Copiar correo ---------- */
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var txt = b.getAttribute("data-copiar");
      var aviso = b.querySelector("[data-copiado]") || document.querySelector("[data-copiado-g]");
      var ok = function () { if (aviso) aviso.textContent = "Copiado"; setTimeout(function () { if (aviso) aviso.textContent = aviso.hasAttribute("data-copiado-g") ? "Haz clic para copiar el correo" : "Copiar"; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () { if (aviso) aviso.textContent = txt; });
      else if (aviso) aviso.textContent = txt;
    });
  });

  /* ---------- Arranque ---------- */
  var entro = false;
  var go = function () { if (entro) return; entro = true; entrar(); };
  if (document.readyState === "complete") go(); else { window.addEventListener("load", go); setTimeout(go, 2500); }
  window.addEventListener("load", function () { if (ST) ST.refresh(); });
})();

/* Aviso al copiar el correo desde el currículum */
document.querySelectorAll(".cv-correo").forEach(function (b) {
  b.addEventListener("click", function () { var t = b.textContent; b.textContent = "Correo copiado"; setTimeout(function () { b.textContent = t; }, 1600); });
});
