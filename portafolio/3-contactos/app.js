/* CONTACTOS · lupa sobre los fotogramas (solo con ratón o lápiz). */
(function () {
  "use strict";
  var lupa = document.querySelector("[data-lupa-el]");
  var fina = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var ZOOM = 2.6;

  if (lupa && fina) {
    var actual = null;
    document.querySelectorAll("[data-lupa]").forEach(function (cuadro) {
      cuadro.addEventListener("pointerenter", function () {
        actual = cuadro;
        lupa.style.backgroundImage = "url(" + cuadro.getAttribute("data-img") + ")";
        lupa.hidden = false;
      });
      cuadro.addEventListener("pointerleave", function () { actual = null; lupa.hidden = true; });
      cuadro.addEventListener("pointermove", function (ev) {
        if (actual !== cuadro) return;
        var r = cuadro.getBoundingClientRect();
        var sz = parseFloat(cuadro.getAttribute("data-sz"));
        var arImg = parseFloat(cuadro.getAttribute("data-ar"));
        var px = parseFloat(cuadro.getAttribute("data-px")) / 100;
        var py = parseFloat(cuadro.getAttribute("data-py")) / 100;
        // Tamaño y desplazamiento reales del fondo dentro del fotograma.
        var bw = r.width * sz, bh = bw / arImg;
        var ox = (r.width - bw) * px, oy = (r.height - bh) * py;
        var u = ev.clientX - r.left - ox, v = ev.clientY - r.top - oy;
        var L = lupa.offsetWidth / 2;
        lupa.style.backgroundSize = (bw * ZOOM) + "px " + (bh * ZOOM) + "px";
        lupa.style.backgroundPosition = (L - u * ZOOM) + "px " + (L - v * ZOOM) + "px";
        lupa.style.left = ev.clientX + "px";
        lupa.style.top = ev.clientY + "px";
      });
    });
    window.addEventListener("scroll", function () { if (actual) { lupa.hidden = true; actual = null; } }, { passive: true });
  }

  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var el = document.getElementById(b.getAttribute("data-copiar"));
      var aviso = document.querySelector("[data-copiado]");
      var marcar = function () { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); if (aviso) aviso.textContent = "Selecciona y copia"; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(el.textContent.trim()).then(function () { if (aviso) aviso.textContent = "Copiado"; }, marcar);
      } else marcar();
    });
  });
})();
