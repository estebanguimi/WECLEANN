/* CORTE · línea de tiempo con cabezal, monitor que sigue al cabezal y teclas J K L. */
(function () {
  "use strict";

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function tc(seg, fps) {
    var f = Math.max(0, Math.round(seg * fps));
    var h = Math.floor(f / (3600 * fps)); f -= h * 3600 * fps;
    var m = Math.floor(f / (60 * fps)); f -= m * 60 * fps;
    var s = Math.floor(f / fps); f -= s * fps;
    function p(n) { return (n < 10 ? "0" : "") + n; }
    return p(h) + ":" + p(m) + ":" + p(s) + ":" + p(f);
  }

  // Generador determinista para que la forma de onda sea siempre la misma.
  function azar(semilla) {
    var x = semilla || 1;
    return function () { x = (x * 16807) % 2147483647; return (x - 1) / 2147483646; };
  }

  function dibujarOndas(tl, datos) {
    tl.querySelectorAll("canvas.onda").forEach(function (cv) {
      var dpr = window.devicePixelRatio || 1;
      var w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return;
      cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
      var ctx = cv.getContext("2d");
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      var r = azar(parseInt(cv.getAttribute("data-semilla"), 10));
      datos.clips.forEach(function (c) {
        var x0 = c.entrada / datos.total * w, x1 = c.salida / datos.total * w;
        ctx.fillStyle = "#24392c";
        ctx.fillRect(x0 + 0.5, 0, x1 - x0 - 1, h);
        ctx.fillStyle = "#86b893";
        var mitad = h / 2, env = 0.4;
        for (var x = x0 + 2; x < x1 - 2; x += 2) {
          env += (r() - 0.5) * 0.18; env = Math.min(0.95, Math.max(0.12, env));
          var a = (0.25 + r() * 0.75) * env * mitad;
          ctx.fillRect(x, mitad - a, 1.2, a * 2);
        }
      });
    });
  }

  function iniciarTimeline(sec) {
    var cuerpo = sec.querySelector("[data-timeline]");
    var cabezal = sec.querySelector("[data-cabezal]");
    var lectura = sec.querySelector("[data-tl-tc]");
    var nodo = sec.querySelector("[data-tl-datos]");
    if (!cuerpo || !cabezal || !nodo) return;
    var datos = JSON.parse(nodo.textContent);
    var monitorImg = document.querySelector("[data-monitor-img]");
    var monitorClip = document.querySelector("[data-monitor-clip]");
    var monitorTc = document.querySelector("[data-monitor-tc]");
    var activo = sec.querySelector(".clip.activo");
    var t = activo ? datos.clips.filter(function (c) { return c.slug === activo.getAttribute("data-slug"); })[0].entrada
                   : datos.clips[1].entrada;
    var imgActual = monitorImg ? monitorImg.getAttribute("src") : "";
    var velocidad = 0, ultimo = 0;
    var IZQ = 44, DER = 14;

    function clipEn(seg) {
      for (var i = 0; i < datos.clips.length; i++) {
        var c = datos.clips[i];
        if (seg >= c.entrada && seg < c.salida) return c;
      }
      return null;
    }

    function pintar() {
      var ancho = cuerpo.clientWidth - IZQ - DER;
      cabezal.style.marginLeft = "0px";
      cabezal.style.left = (IZQ + t / datos.total * ancho) + "px";
      var codigo = tc(t, datos.fps);
      if (lectura) lectura.textContent = codigo;
      cuerpo.setAttribute("aria-valuenow", String(Math.round(t)));
      cuerpo.setAttribute("aria-valuetext", codigo);
      if (!monitorImg) return;
      var c = clipEn(t);
      if (monitorTc) monitorTc.textContent = codigo;
      if (c) {
        var src = "assets/" + c.img;
        if (src !== imgActual) { monitorImg.src = src; imgActual = src; }
        monitorImg.style.visibility = "visible";
        if (monitorClip) monitorClip.textContent = "V1 · " + c.titulo;
      } else {
        monitorImg.style.visibility = "hidden";
        if (monitorClip) monitorClip.textContent = "V1 · Negro";
      }
    }

    function mover(clientX) {
      var r = cuerpo.getBoundingClientRect();
      var ancho = r.width - IZQ - DER;
      var x = Math.min(Math.max(clientX - r.left - IZQ, 0), ancho);
      t = x / ancho * datos.total;
      pintar();
    }

    // Arrastre del cabezal. Si se arrastró, el clic no abre el proyecto.
    var abajo = false, inicioX = 0, arrastro = false;
    cuerpo.addEventListener("pointerdown", function (ev) {
      if (ev.button !== 0) return;
      abajo = true; arrastro = false; inicioX = ev.clientX; velocidad = 0;
      mover(ev.clientX);
    });
    window.addEventListener("pointermove", function (ev) {
      if (!abajo) return;
      if (Math.abs(ev.clientX - inicioX) > 4) arrastro = true;
      if (arrastro) { ev.preventDefault(); mover(ev.clientX); }
    });
    window.addEventListener("pointerup", function () { abajo = false; });
    cuerpo.addEventListener("click", function (ev) {
      if (arrastro) { ev.preventDefault(); arrastro = false; }
    }, true);

    // Reproducción con J K L, como en cualquier editor.
    function bucle(ahora) {
      if (!velocidad) return;
      var dt = ultimo ? (ahora - ultimo) / 1000 : 0;
      ultimo = ahora;
      t += dt * velocidad;
      if (t >= datos.total) { t = datos.total; velocidad = 0; }
      if (t <= 0) { t = 0; velocidad = 0; }
      pintar();
      if (velocidad) requestAnimationFrame(bucle);
    }
    function reproducir(v) {
      var parado = !velocidad;
      velocidad = v; ultimo = 0;
      if (reduce && v) { t = Math.min(datos.total, Math.max(0, t + v)); velocidad = 0; pintar(); return; }
      if (parado && v) requestAnimationFrame(bucle);
    }
    cuerpo.addEventListener("keydown", function (ev) {
      var k = ev.key.toLowerCase();
      var cuadro = 1 / datos.fps;
      if (k === "l") reproducir(velocidad > 0 ? Math.min(velocidad * 2, 8) : 1);
      else if (k === "j") reproducir(velocidad < 0 ? Math.max(velocidad * 2, -8) : -1);
      else if (k === "k") reproducir(0);
      else if (k === " ") reproducir(velocidad ? 0 : 1);
      else if (k === "arrowright") { reproducir(0); t = Math.min(datos.total, t + (ev.shiftKey ? 1 : cuadro)); pintar(); }
      else if (k === "arrowleft") { reproducir(0); t = Math.max(0, t - (ev.shiftKey ? 1 : cuadro)); pintar(); }
      else if (k === "enter") { var c = clipEn(t); if (c) location.href = c.slug + ".html"; return; }
      else return;
      ev.preventDefault();
    });

    dibujarOndas(sec, datos);
    pintar();
    var temporizador;
    window.addEventListener("resize", function () {
      clearTimeout(temporizador);
      temporizador = setTimeout(function () { dibujarOndas(sec, datos); pintar(); }, 80);
    });
  }

  document.querySelectorAll(".timeline").forEach(iniciarTimeline);

  // Vista del bin: lista o iconos (se recuerda por visitante).
  var bin = document.querySelector("[data-bin]");
  if (bin) {
    var botones = bin.querySelectorAll("[data-vista]");
    var poner = function (v) {
      botones.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-vista") === v)); });
      bin.querySelectorAll("[data-panel]").forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== v; });
      try { localStorage.setItem("corte-vista", v); } catch (e) {}
    };
    botones.forEach(function (b) { b.addEventListener("click", function () { poner(b.getAttribute("data-vista")); }); });
    try { var g = localStorage.getItem("corte-vista"); if (g === "iconos" || g === "lista") poner(g); } catch (e) {}
  }

  // Copiar correo
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var el = document.getElementById(b.getAttribute("data-copiar"));
      var aviso = document.querySelector("[data-copiado]");
      var texto = el.textContent.trim();
      var marcar = function () {
        var r = document.createRange(); r.selectNodeContents(el);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto).then(function () { if (aviso) aviso.textContent = "Copiado"; },
          function () { marcar(); if (aviso) aviso.textContent = "Selecciona y copia"; });
      } else { marcar(); if (aviso) aviso.textContent = "Selecciona y copia"; }
    });
  });
})();
