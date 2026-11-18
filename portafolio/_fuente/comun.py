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
<html lang="es">
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
