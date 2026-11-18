# -*- coding: utf-8 -*-
"""Línea D · MESA — el portafolio como la mesa de trabajo de un diseñador.

Un lienzo infinito con todos los proyectos ordenados por disciplina, reglas, capas, inspector y notas
adhesivas. Se recorre arrastrando y con zoom, como un archivo de diseño abierto.
"""
import json

import comun as C
import datos as D
from comun import e

FUENTES = ("family=Bricolage+Grotesque:opsz,wght@12..96,300..800"
           "&family=IBM+Plex+Mono:wght@400;500&family=Caveat:wght@500;700")

LOGO = """<svg class="logo" viewBox="0 0 56 56" aria-hidden="true">
<rect x="6" y="6" width="44" height="44" fill="var(--hoja)" stroke="var(--sel)" stroke-width="2"/>
<g fill="var(--hoja)" stroke="var(--sel)" stroke-width="2"><rect x="2" y="2" width="8" height="8"/><rect x="46" y="2" width="8" height="8"/><rect x="2" y="46" width="8" height="8"/><rect x="46" y="46" width="8" height="8"/></g>
<text x="28" y="35" text-anchor="middle" font-family="Bricolage Grotesque, sans-serif" font-weight="800" font-size="19" fill="var(--tinta)">EG</text>
</svg>"""

NAV = [("index.html", "Lienzo"), ("trabajo.html", "Trabajo"), ("sobre.html", "Perfil"), ("cv.html", "CV"), ("contacto.html", "Contacto")]

# Imágenes que se cuelgan en el lienzo, por disciplina
SECCIONES = [
    ("video", [("gallucci", "00.jpg"), ("bobby-charles", "00.jpg"), ("bobby-charles", "01.jpg"), ("gallucci", "01.jpg"),
               ("bobby-charles", "03.jpg"), ("bobby-charles", "05.jpg"), ("gallucci", "02.jpg")]),
    ("foto", [("mercyme", "19.jpg"), ("crowder", "17.jpg"), ("mercyme", "03.jpg"), ("for-king-country", "06.jpg"),
              ("crowder", "01.jpg"), ("mercyme", "07.jpg"), ("for-king-country", "01.jpg")]),
    ("deporte", [("nahomi-martinez", "03.jpg"), ("matchdays", "02.jpg"), ("luis-benites", "05.jpg"), ("nahomi-martinez", "09.jpg"),
                 ("matchdays", "21.jpg"), ("luis-benites", "01.jpg"), ("matchdays", "03.jpg")]),
    ("marca", [("qatar-2022", "04.jpg"), ("physo", "02.jpg"), ("qatar-2022", "01.jpg"), ("physo", "01.jpg"),
               ("qatar-2022", "02.jpg"), ("physo", "03.jpg")]),
    ("web", [("zena-coffee", "00.jpg"), ("zena-coffee", "02.jpg"), ("zena-coffee", "01.jpg")]),
    ("gaming", [("valorant", "02.jpg"), ("valorant", "00.jpg"), ("valorant", "01.jpg")]),
]

NOTAS = {
    "video": ("900K + 436K vistas. Edición, motion y grabación.", -4),
    "foto": ("60 fotos en 3 conciertos", 3),
    "deporte": ("53 afiches, 6+ clubes", -2),
    "marca": ("37 piezas para un Mundial", 4),
    "web": ("Diseñado en Figma", -3),
    "gaming": ("Overlays listos para OBS", 2),
}

ANCHO_SEC, GAP, ALTO_FILA = 1800, 36, 360


def empaquetar(items, x0, y0):
    """Filas justificadas dentro de una sección del lienzo. Devuelve frames y alto ocupado."""
    frames, fila, y = [], [], y0
    def cerrar(f, justificar=True):
        nonlocal y
        suma = sum(ar for *_, ar in f)
        alto = (ANCHO_SEC - GAP * (len(f) - 1)) / suma if justificar else ALTO_FILA
        alto = min(alto, ALTO_FILA * 1.6)
        x = x0
        for slug, n, w, h, ar in f:
            frames.append(dict(slug=slug, n=n, w=w, h=h, x=round(x), y=round(y), fw=round(alto * ar), fh=round(alto)))
            x += alto * ar + GAP
        y += alto + GAP + 34
    for slug, n in items:
        w, h = C.medida(slug, n)
        ar = w / h
        fila.append((slug, n, w, h, ar))
        if sum(a for *_, a in fila) * ALTO_FILA + GAP * (len(fila) - 1) >= ANCHO_SEC:
            cerrar(fila); fila = []
    if fila:
        cerrar(fila, justificar=sum(a for *_, a in fila) * ALTO_FILA > ANCHO_SEC * .7)
    return frames, y - y0


def disposicion():
    cols = [-3200, -1000, 1200]
    secs, frames = [], []
    alto_fila1 = 0
    pos = {}
    for i, (cat, items) in enumerate(SECCIONES[:3]):
        f, h = empaquetar(items, cols[i], -2100 + 190)
        pos[cat] = (cols[i], -2100)
        frames += [dict(fr, cat=cat) for fr in f]
        alto_fila1 = max(alto_fila1, h)
    y_medio = -2100 + 190 + alto_fila1 + 260
    y2 = y_medio + 1100
    for i, (cat, items) in enumerate(SECCIONES[3:]):
        f, h = empaquetar(items, cols[i], y2 + 190)
        pos[cat] = (cols[i], y2)
        frames += [dict(fr, cat=cat) for fr in f]
    for cat, items in SECCIONES:
        n_proy = len({s for s, _ in items})
        secs.append(dict(cat=cat, x=pos[cat][0], y=pos[cat][1], n=n_proy))
    return secs, frames, y_medio


def cabecera(activa, inicio=False):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == activa else ""}>{t}</a>' for h, t in NAV)
    zoom = '<span class="tb-zoom mono" data-zoom-t>100%</span>' if inicio else ''
    return f"""<header class="tb" data-tb>
  <a class="tb-marca" href="index.html" aria-label="{e(D.NOMBRE)}, inicio">{LOGO}<span class="tb-arch"><b>Esteban Guillen</b><span class="mono">/ Portafolio 2026</span></span></a>
  <nav class="tb-nav" aria-label="Principal" data-nav>{links}</nav>
  <div class="tb-der">{zoom}<span class="tb-estado mono"><i></i>Disponible</span><a class="tb-cv" href="{D.CV_PDF}" download>CV · PDF</a>
  <button type="button" class="tb-menu" data-menu aria-expanded="false" aria-label="Menú"><span></span><span></span></button></div>
</header>"""


def reglas():
    return '<canvas class="regla regla-h" data-regla="h" aria-hidden="true"></canvas><canvas class="regla regla-v" data-regla="v" aria-hidden="true"></canvas><span class="regla-esq" aria-hidden="true"></span>'


def transicion():
    return '<div class="zoomt" data-zoomt aria-hidden="true"><span></span></div>'


def pie():
    return f"""<footer class="pie">
  <div class="pie-fr">
    <span class="fr-eti mono">Frame · Contacto</span>
    <p class="pie-t">¿Armamos el siguiente?</p>
    <div class="pie-fila">
      <button type="button" class="pie-correo" data-copiar="{e(D.CORREO)}">{e(D.CORREO)}<span class="mono" data-copiado>Copiar</span></button>
      <a class="btn" href="cv.html">Ver currículum</a><a class="btn btn-l" href="{D.CV_PDF}" download>CV en PDF</a>
    </div>
    <div class="pie-legal mono"><span>© 2026 {e(D.NOMBRE)}</span><span>{e(D.CIUDAD)} · {e(D.PUESTO)}</span><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a></div>
  </div>
</footer>"""


def pagina(cuerpo, activa="", clase="", titulo="", desc=""):
    return C.documento(titulo or f"{D.NOMBRE} · Portafolio", desc or D.BIO, FUENTES,
                       f"{transicion()}{cabecera(activa)}{reglas()}<div class=\"hoja-pag\">{cuerpo}{pie()}</div>", clase=clase)


def datos_js():
    out = {}
    for p in D.PROYECTOS:
        out[p["slug"]] = dict(t=p["titulo"], c=p["corto"], cli=p["cliente"], rol=D.ROLES[p["cat"]], a=p["ano"],
                              cat=D.CATEGORIAS[p["cat"]], herr=", ".join(p["herr"]), res=p["resumen"],
                              d=p["datos"], pal=C.paleta(p["slug"]), img=C.img(p["slug"], p["portada"]))
    return json.dumps(out, ensure_ascii=False)


# ---------------------------------------------------------------------------------------------- inicio
def inicio():
    secs, frames, y_medio = disposicion()
    numeros = {cat: i + 1 for i, (cat, _) in enumerate(SECCIONES)}
    html = []
    for s in secs:
        nota, rot = NOTAS[s["cat"]]
        html.append(f'<div class="m-sec" style="left:{s["x"]}px;top:{s["y"]}px"><span class="mono">Página {numeros[s["cat"]]:02d}</span>'
                    f'<h2>{e(D.CATEGORIAS[s["cat"]])}</h2><span class="mono">{s["n"]} {"proyecto" if s["n"] == 1 else "proyectos"}</span></div>')
        html.append(f'<div class="nota" data-nota style="left:{s["x"] + 1420}px;top:{s["y"] - 30}px;--r:{rot}deg">{e(nota)}</div>')
    for f in frames:
        p = D.por_slug(f["slug"])
        html.append(
            f'<a class="fr" href="{f["slug"]}.html" data-fr data-slug="{f["slug"]}" style="left:{f["x"]}px;top:{f["y"]}px;width:{f["fw"]}px;height:{f["fh"]}px">'
            f'<span class="fr-eti mono">{e(p["corto"])} · {f["n"][:2]}</span>'
            f'<img src="{C.img(f["slug"], f["n"])}" alt="{e(p["titulo"])}" loading="lazy" decoding="async" draggable="false">'
            f'<span class="fr-med mono">{f["w"]} × {f["h"]}</span><span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span></a>')
    # banda central: presentación, currículum y contacto
    y = y_medio
    exp = "".join(f'<li><span class="mono">{e(x["fechas"])}</span><b>{e(x["puesto"])}</b><span>{e(x["empresa"])}</span></li>' for x in D.EXPERIENCIA)
    cif = "".join(f'<div><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in D.CIFRAS)
    html.append(f"""<div class="fr fr-txt fr-intro" data-fr data-clave="intro" style="left:-1000px;top:{y}px;width:1180px;height:820px">
  <span class="fr-eti mono">Frame · Hola</span>
  <p class="mono intro-k">{e(D.PUESTO)} · {e(D.CIUDAD)}</p>
  <h1 class="intro-t">Esteban<br>Guillen<span class="cursor-txt" aria-hidden="true"></span></h1>
  <p class="intro-b">{e(D.BIO)}</p>
  <div class="intro-cif">{cif}</div>
  <span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</div>
<a class="fr fr-txt fr-cv" href="cv.html" data-fr data-clave="cv" style="left:300px;top:{y}px;width:600px;height:820px">
  <span class="fr-eti mono">Frame · Currículum A4</span>
  <span class="cv-mini-cab"><img src="{C.retrato()}" alt="" loading="lazy"><span><b>{e(D.NOMBRE)}</b><span class="mono">{e(D.PUESTO)}</span></span></span>
  <ol class="cv-mini">{exp}</ol>
  <span class="cv-mini-pie mono">Doble clic para abrir · PDF en la barra superior</span>
  <span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</a>
<a class="fr fr-txt fr-contacto" href="contacto.html" data-fr data-clave="contacto" style="left:1020px;top:{y}px;width:760px;height:380px">
  <span class="fr-eti mono">Frame · Contacto</span>
  <span class="mono">Escríbeme</span><b class="ct-mini">{e(D.CORREO)}</b><span class="mono">{e(D.DISPONIBLE)}</span>
  <span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</a>
<a class="fr fr-txt fr-perfil" href="sobre.html" data-fr data-clave="perfil" style="left:1020px;top:{y + 440}px;width:760px;height:380px">
  <span class="fr-eti mono">Frame · Perfil</span>
  <img src="{C.retrato()}" alt="Retrato de {e(D.NOMBRE)}" loading="lazy" draggable="false">
  <span class="pf-mini"><span class="mono">Perfil</span><b>De Lima a Miami, desde 2018.</b></span>
  <span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</a>
<div class="nota" data-nota style="left:-1380px;top:{y + 560}px;--r:-5deg">Arrastra para moverte.<br>Doble clic en un frame para abrirlo.</div>
<div class="nota nota-r" data-nota style="left:760px;top:{y - 70}px;--r:4deg">8 años de oficio →</div>""")
    capas = []
    for cat, items in SECCIONES:
        slugs = []
        for s, _ in items:
            if s not in slugs:
                slugs.append(s)
        filas = "".join(f'<button type="button" data-ir="{s}"><span class="cp-ic"></span>{e(D.por_slug(s)["corto"])}</button>' for s in slugs)
        capas.append(f'<div class="cp-g"><p class="mono">{e(D.CATEGORIAS[cat])}</p>{filas}</div>')
    capas.append('<div class="cp-g"><p class="mono">Sobre mí</p><button type="button" data-ir="intro"><span class="cp-ic cp-t"></span>Hola</button>'
                 '<button type="button" data-ir="cv"><span class="cp-ic cp-t"></span>Currículum</button>'
                 '<button type="button" data-ir="perfil"><span class="cp-ic cp-t"></span>Perfil</button>'
                 '<button type="button" data-ir="contacto"><span class="cp-ic cp-t"></span>Contacto</button></div>')
    cuerpo = f"""{transicion()}{cabecera("index.html", inicio=True)}
<main class="app">
  <aside class="capas" aria-label="Capas"><p class="panel-t mono">Capas</p><div class="cp-lista">{''.join(capas)}</div></aside>
  <div class="lienzo" data-lienzo tabindex="0" aria-label="Lienzo con todos los proyectos. Arrastra para moverte.">
    {reglas()}
    <div class="mundo" data-mundo>{''.join(html)}</div>
    <div class="cursor-eg" data-cursor-eg aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M3 2l7 19 2.6-7.4L20 11z" fill="var(--sel)" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg><span>Esteban</span></div>
    <canvas class="mini" data-mini width="220" height="150" aria-hidden="true"></canvas>
    <div class="zoom-ctl"><button type="button" data-zoom="-" aria-label="Alejar">−</button><button type="button" data-zoom="fit" class="mono">Ajustar</button><button type="button" data-zoom="+" aria-label="Acercar">+</button></div>
    <p class="guia mono" data-guia>Arrastra para moverte · Rueda o pellizco para zoom · Doble clic para abrir</p>
  </div>
  <aside class="insp" data-insp aria-live="polite">
    <div class="insp-doc" data-insp-doc>
      <p class="panel-t mono">Documento</p>
      <img class="insp-foto" src="{C.retrato()}" alt="Retrato de {e(D.NOMBRE)}">
      <h2>{e(D.NOMBRE)}</h2>
      <p>{e(D.PUESTO)}</p>
      <dl class="insp-dl">
        <div><dt class="mono">Base</dt><dd>{e(D.CIUDAD)}</dd></div>
        <div><dt class="mono">Hoy</dt><dd>Harris Media Group</dd></div>
        <div><dt class="mono">Experiencia</dt><dd>Desde 2018</dd></div>
        <div><dt class="mono">Idiomas</dt><dd>{e(', '.join(a for a, _ in D.IDIOMAS))}</dd></div>
        <div><dt class="mono">Correo</dt><dd><button type="button" class="enl" data-copiar="{e(D.CORREO)}">{e(D.CORREO)}</button></dd></div>
      </dl>
      <div class="insp-acc"><a class="btn" href="cv.html">Currículum</a><a class="btn btn-l" href="{D.CV_PDF}" download>PDF</a></div>
      <p class="insp-tip mono">Selecciona un frame para ver sus propiedades.</p>
    </div>
    <div class="insp-sel" data-insp-sel hidden></div>
  </aside>
</main>
<script type="application/json" id="datos-proyectos">{datos_js()}</script>"""
    return C.documento(f"{D.NOMBRE} · Mesa", D.BIO, FUENTES, cuerpo, clase="pg-inicio")


# ---------------------------------------------------------------------------------------------- trabajo
def trabajo():
    tabs = [("todo", "Todas", len(D.PROYECTOS))] + [(k, v, sum(1 for p in D.PROYECTOS if p["cat"] == k)) for k, v in D.CATEGORIAS.items()]
    botones = "".join(f'<button type="button" class="tab{" activo" if k == "todo" else ""}" data-filtro="{k}" aria-pressed="{"true" if k == "todo" else "false"}">{e(t)}<sup class="mono">{n}</sup></button>' for k, t, n in tabs)
    frames = []
    for i, p in enumerate(D.PROYECTOS):
        w, h = C.medida(p["slug"], p["portada"])
        forma = "v" if h > w * 1.15 else ("h" if w > h * 1.3 else "c")
        frames.append(f"""<a class="fr fr-t fr-{forma}" href="{p['slug']}.html" data-cat="{p['cat']}">
  <span class="fr-eti mono">{i + 1:02d} · {e(p['corto'])}</span>
  <span class="fr-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}" loading="lazy"></span>
  <span class="fr-med mono">{w} × {h}</span><span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
  <span class="fr-info"><b>{e(p['titulo'])}</b><span>{e(D.CATEGORIAS[p['cat']])} · {e(p['ano'])} · {e(p['cifra'])} {e(p['cifra_t'])}</span></span>
</a>""")
    cuerpo = f"""<main class="envol">
  <header class="pag-cab"><p class="mono k">Trabajo · {len(D.PROYECTOS)} proyectos</p><h1 data-lineas>Todo el trabajo,<br>en una mesa.</h1>
  <p class="pag-intro">Video para campañas, fotografía en vivo, diseño deportivo, marcas, web y gaming. Filtra por página.</p></header>
  <div class="tabs" role="group" aria-label="Filtrar por disciplina">{botones}</div>
  <div class="tablero" data-tablero>{''.join(frames)}</div>
</main>"""
    return pagina(cuerpo, "trabajo.html", "pg-trabajo", f"Trabajo · {D.NOMBRE}", "Doce proyectos de video, fotografía, diseño deportivo, marca, web y gaming.")


# ---------------------------------------------------------------------------------------------- proyecto
def proyecto(p):
    i = D.PROYECTOS.index(p)
    sig, ant = D.siguiente(p["slug"]), D.anterior(p["slug"])
    ims = D.imagenes(p["slug"])
    capas = "".join(f'<a href="#pieza-{k + 1}"><span class="cp-ic"></span>{p["corto"]} · {n[:2]}<span class="mono">{w}×{h}</span></a>' for k, (n, w, h) in enumerate(ims))
    piezas = []
    for k, (n, w, h) in enumerate(ims):
        ar = w / h
        cls = "pz-largo" if ar < 0.45 else ("pz-v" if ar < 0.9 else ("pz-h" if ar > 1.5 else "pz-c"))
        piezas.append(f'<figure class="fr pz {cls}" id="pieza-{k + 1}" data-i="{k}"><span class="fr-eti mono">{e(p["corto"])} · {n[:2]}</span>'
                      f'<span class="fr-img"><img src="{C.img(p["slug"], n)}" alt="{e(p["titulo"])}, pieza {k + 1}" loading="lazy" width="{w}" height="{h}"></span>'
                      f'<span class="fr-med mono">{w} × {h}</span><span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span></figure>')
    datos = "".join(f'<div><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in p["datos"])
    pal = "".join(f'<button type="button" class="sw" style="--c:{c}" data-copiar="{c}"><i></i><span class="mono">{c}</span></button>' for c in C.paleta(p["slug"]))
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    cuerpo = f"""<main class="proy">
  <aside class="capas capas-p"><p class="panel-t mono">Capas · {len(ims)}</p><nav class="cp-lista">{capas}</nav></aside>
  <article class="proy-c">
    <header class="proy-cab">
      <p class="mono k"><a href="trabajo.html">Trabajo</a> / {e(D.CATEGORIAS[p['cat']])} / {i + 1:02d}</p>
      <h1 data-lineas>{e(p['titulo'])}</h1>
      <p class="proy-res">{e(p['resumen'])}</p>
    </header>
    <figure class="fr pz pz-portada" data-i="-1"><span class="fr-eti mono">Portada</span><span class="fr-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"></span><span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span></figure>
    <div class="proy-txt">{textos}</div>
    {C.bloque_video(p)}
    <div class="piezas" data-galeria>{''.join(piezas)}</div>
    <nav class="proy-nav">
      <a href="{ant['slug']}.html"><span class="mono">← Anterior</span><b>{e(ant['corto'])}</b></a>
      <a href="{sig['slug']}.html"><span class="mono">Siguiente →</span><b>{e(sig['corto'])}</b><img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></a>
    </nav>
  </article>
  <aside class="insp insp-p">
    <p class="panel-t mono">Propiedades</p>
    <dl class="insp-dl">
      <div><dt class="mono">Cliente</dt><dd>{e(p['cliente'])}</dd></div>
      <div><dt class="mono">Mi rol</dt><dd>{e(D.ROLES[p['cat']])}</dd></div>
      <div><dt class="mono">Disciplina</dt><dd>{e(D.CATEGORIAS[p['cat']])}</dd></div>
      <div><dt class="mono">Año</dt><dd>{e(p['ano'])}</dd></div>
      <div><dt class="mono">Herramientas</dt><dd>{e(', '.join(p['herr']))}</dd></div>
    </dl>
    <p class="panel-t mono">Resultados</p>
    <div class="insp-datos">{datos}</div>
    <p class="panel-t mono">Paleta medida</p>
    <div class="insp-pal">{pal}</div>
  </aside>
</main>
<div class="lb" data-lb hidden><button type="button" class="lb-x mono" data-lb-x>Cerrar · Esc</button><button type="button" class="lb-a" data-lb-a aria-label="Anterior">←</button><img alt="" data-lb-img><button type="button" class="lb-s" data-lb-s aria-label="Siguiente">→</button><span class="lb-n mono" data-lb-n></span></div>"""
    return pagina(cuerpo, "", "pg-proyecto", f"{p['corto']} · {D.NOMBRE}", p["resumen"])


# ---------------------------------------------------------------------------------------------- perfil, cv, contacto
def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    serv = "".join(f'<li><span class="mono">{i + 1:02d}</span><b>{e(t)}</b><span>{e(d)}</span></li>' for i, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""<main class="envol">
  <header class="pag-cab"><p class="mono k">Perfil</p><h1 data-lineas>Diseño, edito<br>y fotografío.</h1></header>
  <section class="perfil">
    <figure class="fr perfil-foto"><span class="fr-eti mono">Retrato · {e(D.CIUDAD)}</span><span class="fr-img"><img src="{C.retrato()}" alt="Retrato de {e(D.NOMBRE)}"></span><span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      <span class="nota nota-fija" style="--r:-4deg">Hola, soy Esteban</span></figure>
    <div class="perfil-txt"><p class="lead">{e(D.BIO)}</p>{bio}
      <div class="perfil-acc"><a class="btn" href="cv.html">Ver currículum</a><a class="btn btn-l" href="{D.CV_PDF}" download>Descargar PDF</a></div></div>
  </section>
  <section class="bloque"><p class="mono k">Recorrido · desde 2018</p>{C.recorrido()}</section>
  <section class="bloque"><p class="mono k">Qué hago</p><ol class="servicios">{serv}</ol></section>
</main>"""
    return pagina(cuerpo, "sobre.html", "pg-sobre", f"Perfil · {D.NOMBRE}", D.BIO)


def cv():
    cuerpo = f"""<main class="envol">
  <header class="pag-cab"><p class="mono k">Currículum · A4</p><h1 data-lineas>Currículum</h1></header>
  <div class="a4"><span class="fr-eti mono">Frame · Currículum 2026</span>{C.cv_secciones("mono k")}<span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span></div>
</main>"""
    return pagina(cuerpo, "cv.html", "pg-cv", f"Currículum · {D.NOMBRE}", D.CV_RESUMEN)


def contacto():
    cuerpo = f"""<main class="envol">
  <header class="pag-cab"><p class="mono k">Contacto · {e(D.DISPONIBLE)}</p><h1 data-lineas>Hablemos.</h1></header>
  <section class="contacto">
    <div class="fr ct-fr"><span class="fr-eti mono">Frame · Correo</span>
      <button type="button" class="ct-correo" data-copiar="{e(D.CORREO)}"><b>{e(D.CORREO)}</b><span class="mono" data-copiado>Clic para copiar</span></button>
      <a class="btn" href="mailto:{e(D.CORREO)}">Abrir correo</a>
      <span class="fr-asas" aria-hidden="true"><i></i><i></i><i></i><i></i></span></div>
    <dl class="insp-dl ct-dl">
      <div><dt class="mono">Instagram</dt><dd><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">{e(D.INSTAGRAM_T)} ↗</a></dd></div>
      <div><dt class="mono">Currículum</dt><dd><a href="cv.html">En la web</a> · <a href="{D.CV_PDF}" download>PDF ↓</a></dd></div>
      <div><dt class="mono">Base</dt><dd>{e(D.CIUDAD)} · Origen {e(D.ORIGEN)}</dd></div>
      <div><dt class="mono">Idiomas</dt><dd>{e(' · '.join(a + ' ' + b.lower() for a, b in D.IDIOMAS))}</dd></div>
      <div><dt class="mono">Servicios</dt><dd>{e(' · '.join(t for t, _ in D.SERVICIOS))}</dd></div>
    </dl>
    <span class="nota nota-fija ct-nota" style="--r:3deg">Miami · hora del Este</span>
  </section>
</main>"""
    return pagina(cuerpo, "contacto.html", "pg-contacto", f"Contacto · {D.NOMBRE}", "Escríbeme para tu próximo proyecto.")


def paginas():
    out = {"index.html": inicio(), "trabajo.html": trabajo(), "sobre.html": sobre(), "cv.html": cv(), "contacto.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
