# -*- coding: utf-8 -*-
import os
from html import escape as _esc

from PIL import Image

import datos as D

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

# Prefijo de imágenes: en el repositorio las webs usan ../img/, al publicar se usa img/
IMG = {"p": "../img/"}


def e(s):
    return _esc(str(s), quote=True)


def img(slug, nombre):
    return f"{IMG['p']}{slug}/{nombre}"


def retrato():
    return f"{IMG['p']}retrato.jpg"


def medida(slug, nombre):
    for n, w, h in D.imagenes(slug):
        if n == nombre:
            return w, h
    return 1600, 1000


def documento(titulo, descripcion, fuentes, cuerpo, clase="", extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(descripcion)}">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fuentes}&display=swap">
<link rel="stylesheet" href="estilo.css">
{extra_head}
</head>
<body class="{clase}">
{cuerpo}
<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script src="vendor/Flip.min.js"></script>
<script src="vendor/lenis.min.js"></script>
<script src="app.js"></script>
</body>
</html>
"""


_PAL = {}


def paleta(slug, n=5):
    """Colores dominantes reales del proyecto (para mostrar su paleta)."""
    if slug in _PAL:
        return _PAL[slug]
    ims = D.imagenes(slug)
    muestra = Image.new("RGB", (120 * min(6, len(ims)), 120))
    for i, (nombre, w, h) in enumerate(ims[:6]):
        t = Image.open(os.path.join(RAIZ, "img", slug, nombre)).convert("RGB").resize((120, 120))
        muestra.paste(t, (i * 120, 0))
    q = muestra.quantize(colors=n * 3, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: n * 3 * 3]
    cuentas = sorted(q.getcolors(), reverse=True)
    out = []
    for c, idx in cuentas:
        r, g, b = pal[idx * 3: idx * 3 + 3]
        if all(abs(r - x[0]) + abs(g - x[1]) + abs(b - x[2]) > 60 for x in out):
            out.append((r, g, b))
        if len(out) == n:
            break
    _PAL[slug] = ["#%02x%02x%02x" % c for c in out]
    return _PAL[slug]


def filas(slug, excluir=()):
    """Agrupa las imágenes en filas justificadas (misma altura por fila) según su proporción."""
    ims = [x for x in D.imagenes(slug) if x[0] not in excluir]
    out, fila, suma = [], [], 0.0
    for n, w, h in ims:
        ar = w / h
        if ar > 2.4:  # páginas largas o banners: fila propia
            if fila:
                out.append(fila); fila, suma = [], 0.0
            out.append([(n, w, h)]); continue
        fila.append((n, w, h)); suma += ar
        if suma >= 2.6 or len(fila) == 3:
            out.append(fila); fila, suma = [], 0.0
    if fila:
        out.append(fila)
    return out


def galeria(slug, clase="galeria", extra_attr=""):
    html = []
    k = 0
    for fila in filas(slug):
        celdas = []
        for n, w, h in fila:
            ar = w / h
            alto = ""
            if ar < 0.45:  # página web larga: se recorta y se puede abrir completa
                ar = 0.62
                alto = " largo"
            celdas.append(
                f'<figure class="g-item{alto}" style="flex:{ar:.4f} 1 0;aspect-ratio:{ar:.4f}" data-i="{k}">'
                f'<img src="{img(slug, n)}" alt="" loading="lazy" decoding="async" width="{w}" height="{h}"{extra_attr}></figure>')
            k += 1
        html.append(f'<div class="g-fila">{"".join(celdas)}</div>')
    return f'<div class="{clase}" data-galeria>{"".join(html)}</div>'


def videos(slug):
    """Videos propios del proyecto: img/video/<slug>-1.mp4, <slug>-2.mp4 ... (se muestran si existen)."""
    d = os.path.join(RAIZ, "img", "video")
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.startswith(slug + "-") and f.endswith(".mp4"))


def bloque_video(p, clase="videos-p"):
    vs = videos(p["slug"])
    if not vs:
        return ""
    poster = img(p["slug"], p["portada"])
    items = "".join(
        f'<figure class="video-p"><video controls playsinline preload="metadata" poster="{poster}" src="{IMG["p"]}video/{v}"></video></figure>'
        for v in vs)
    return f'<div class="{clase}">{items}</div>'


def cv_nav_pdf():
    return D.CV_PDF


# ---------------------------------------------------------------- Currículum (marcado común; cada línea le da su estilo)
def cv_secciones(eti_h2="cv-h"):
    exp = []
    for x in D.EXPERIENCIA:
        proys = "".join(
            f'<a class="cv-proy" href="{s}.html"><img src="{img(s, D.por_slug(s)["portada"])}" alt="" loading="lazy"><span>{e(D.por_slug(s)["corto"])}</span></a>'
            for s in x["proyectos"])
        exp.append(f"""<li class="cv-item">
  <p class="cv-fechas">{e(x['fechas'])}</p>
  <div class="cv-cuerpo">
    <h3>{e(x['puesto'])} <span>{e(x['empresa'])}</span></h3>
    <p class="cv-lugar">{e(x['lugar'])}</p>
    <ul>{''.join(f'<li>{e(p)}</li>' for p in x['puntos'])}</ul>
    {f'<div class="cv-proys">{proys}</div>' if proys else ''}
  </div>
</li>""")
    hab = "".join(f"<div><dt>{e(t)}</dt><dd>{e(' · '.join(l))}</dd></div>" for t, l in D.HABILIDADES)
    her = "".join(f"<li>{e(h)}</li>" for h in D.HERRAMIENTAS)
    idi = "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in D.IDIOMAS)
    cif = "".join(f'<div class="cv-cifra"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in D.CIFRAS)
    return f"""<div class="cv">
  <div class="cv-cab">
    <img class="cv-foto" src="{retrato()}" alt="Portrait of {e(D.NOMBRE)}">
    <div class="cv-id">
      <p class="cv-puesto">{e(D.PUESTO)}</p>
      <p class="cv-resumen">{e(D.CV_RESUMEN)}</p>
      <div class="cv-acciones">
        <a class="cv-pdf" href="{D.CV_PDF}" download>Download CV (PDF)</a>
        <button type="button" class="cv-correo" data-copiar="{e(D.CORREO)}">{e(D.CORREO)}</button>
      </div>
    </div>
  </div>
  <div class="cv-cifras">{cif}</div>
  <section class="cv-bloque"><h2 class="{eti_h2}">Experience</h2><ol class="cv-exp">{''.join(exp)}</ol></section>
  <section class="cv-bloque cv-dos">
    <div><h2 class="{eti_h2}">Skills</h2><dl class="cv-hab">{hab}</dl></div>
    <div><h2 class="{eti_h2}">Tools</h2><ul class="cv-chips">{her}</ul>
      <h2 class="{eti_h2}">Languages</h2><ul class="cv-idiomas">{idi}</ul>
      <h2 class="{eti_h2}">Location</h2><p class="cv-base">{e(D.CIUDAD)} · From {e(D.ORIGEN)}<br>{e(D.DISPONIBLE)}</p></div>
  </section>
</div>"""


def recorrido(eti_h2="cv-h"):
    """Resumen de experiencia para la portada: puesto, empresa y fechas."""
    filas = "".join(
        f'<li><span class="rc-f">{e(x["fechas"])}</span><b>{e(x["puesto"])}</b><span class="rc-e">{e(x["empresa"])}</span></li>'
        for x in D.EXPERIENCIA)
    return f'<ol class="recorrido">{filas}</ol>'
