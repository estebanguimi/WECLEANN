# -*- coding: utf-8 -*-
from html import escape as _esc

import datos as D

PAGINAS_FIJAS = [("trabajo.html", "Trabajo"), ("sobre.html", "Sobre mí"), ("contacto.html", "Contacto")]


def e(s):
    return _esc(str(s), quote=True)


def documento(titulo, descripcion, fuentes, cuerpo, css="estilo.css", js="app.js", clase=""):
    """Página HTML completa. `fuentes` es la parte family=... de Google Fonts."""
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(descripcion)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fuentes}&display=swap">
<link rel="stylesheet" href="{css}">
</head>
<body class="{clase}">
{cuerpo}
<script src="{js}"></script>
</body>
</html>
"""


# Línea de tiempo compartida (24 fps). Cada proyecto es un clip con entrada y salida reales.
FPS = 24
DURACIONES = {"harris-media": 38, "arena-pass": 46, "cleanspace": 30, "edicion": 52}
INICIO = 4  # segundos de cola inicial


def tc(segundos):
    f = round(segundos * FPS)
    h, f = divmod(f, 3600 * FPS)
    m, f = divmod(f, 60 * FPS)
    s, f = divmod(f, FPS)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


def clips():
    t = INICIO
    out = []
    for p in D.PROYECTOS:
        d = DURACIONES[p["slug"]]
        out.append({"slug": p["slug"], "titulo": p["titulo"], "tipo": p["tipo"], "color": p["color"],
                    "img": p["imagenes"][0][0], "entrada": t, "salida": t + d,
                    "tc_in": tc(t), "tc_out": tc(t + d), "dur": tc(d)})
        t += d
    return out, t + 6


def contacto_links():
    links = []
    if D.GITHUB:
        links.append(("GitHub", D.GITHUB))
    if D.LINKEDIN:
        links.append(("LinkedIn", D.LINKEDIN))
    if D.VIMEO:
        links.append(("Reel en Vimeo", D.VIMEO))
    return links
