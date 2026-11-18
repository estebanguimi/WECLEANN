/* SECCIÓN · plano del recinto: al pasar o enfocar una sección, el panel muestra el proyecto. */
(function () {
  "use strict";
  document.querySelectorAll("[data-plano]").forEach(function (wrap) {
    var nodo = wrap.querySelector("[data-plano-datos]");
    if (!nodo) return;
    var datos = JSON.parse(nodo.textContent);
    var num = wrap.querySelector("[data-p-num]"), img = wrap.querySelector("[data-p-img]"),
        tit = wrap.querySelector("[data-p-tit]"), sub = wrap.querySelector("[data-p-sub]"),
        link = wrap.querySelector("[data-p-link]");
    var secciones = wrap.querySelectorAll("[data-sec]");
    function mostrar(slug) {
      var d = datos[slug];
      if (!d) return;
      secciones.forEach(function (s) { s.classList.toggle("sel", s.getAttribute("data-sec") === slug); });
      num.textContent = d.num;
      img.src = "assets/" + d.img;
      tit.textContent = d.titulo;
      sub.textContent = d.sub;
      link.href = slug + ".html";
      link.firstChild.textContent = "Ir a la sección " ;
    }
    secciones.forEach(function (s) {
      var slug = s.getAttribute("data-sec");
      s.addEventListener("mouseenter", function () { mostrar(slug); });
      s.addEventListener("focus", function () { mostrar(slug); });
      // En pantallas táctiles el primer toque muestra la sección; el segundo entra.
      s.addEventListener("click", function (ev) {
        if (window.matchMedia("(hover: none)").matches && !s.classList.contains("sel")) { ev.preventDefault(); mostrar(slug); }
      });
    });
    mostrar("arena-pass");
  });

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
