# -*- coding: utf-8 -*-
"""Línea C · ESTUDIO — la identidad nace de tus sistemas de marca (Qatar 2022, Physo, Zena).

Papel blanco, tinta negra, un naranja señal; retícula suiza de 12 columnas visible, tipografía grotesca
grande y un visor WebGL que pasa de un proyecto a otro con una disolución de ruido.
"""
import json

import comun as C
import datos as D
from comun import e

FUENTES = "family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500"

LOGO = """<svg class="logo" viewBox="0 0 48 48" aria-hidden="true">
<rect width="48" height="48" fill="currentColor"/>
<text x="24" y="31.5" text-anchor="middle" font-family="Geist, Helvetica, Arial, sans-serif" font-weight="700" font-size="20" letter-spacing="-1" fill="var(--papel)">EG</text>
<rect x="34" y="8" width="6" height="6" fill="var(--senal)"/>
</svg>"""


def nav(activa=""):
    items = [("index.html", "Home", "01"), ("work.html", "Index", "02"), ("about.html", "About", "03"), ("cv.html", "CV", "04"), ("contact.html", "Contact", "05")]
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == activa else ""} data-n="{n}"><sup>{n}</sup>{t}</a>' for h, t, n in items)
    return f"""<header class="cab" data-cab>
  <a href="index.html" class="cab-marca" aria-label="{e(D.NOMBRE)}, home">{LOGO}<span>Esteban Guillen<br><em>Design, video and photo</em></span></a>
  <span class="cab-dato mono">{e(D.CIUDAD)}<br><span data-reloj>—</span></span>
  <span class="cab-dato mono">Available<br>Full-time · Freelance</span>
  <nav class="cab-nav" aria-label="Main">{links}</nav>
</header>"""


def pie():
    return f"""<footer class="pie">
  <div class="pie-cab"><p class="mono">06 — Contact</p><button type="button" class="mono reticula-btn" data-reticula>Show grid (G)</button></div>
  <a class="pie-correo" href="contact.html" data-roll><span>Get in touch</span></a>
  <div class="pie-cols">
    <div><p class="mono">Email</p><button type="button" class="copiar" data-copiar="{e(D.CORREO)}">{e(D.CORREO)}</button></div>
    <div><p class="mono">Profile</p><a href="cv.html">Résumé</a><a href="{e(D.CV_PDF)}" download>CV (PDF) ↓</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram ↗</a></div>
    <div><p class="mono">Location</p><p>{e(D.CIUDAD)}<br>From {e(D.ORIGEN)}</p></div>
    <div><p class="mono">Status</p><p><span class="punto"></span> {e(D.DISPONIBLE)}</p></div>
  </div>
  <div class="pie-legal mono"><span>© 2026 Esteban Guillen</span><span>12-column grid · Geist</span><span>{e(D.PUESTO)}</span></div>
</footer>"""


def envoltura(cuerpo, activa="", numero="01", titulo="Home"):
    cols = "".join("<i></i>" for _ in range(12))
    return f"""<div class="reticula" data-reticula-el aria-hidden="true">{cols}</div>
<div class="panel" data-panel aria-hidden="true"><span class="panel-n" data-panel-n>{numero}</span><span class="panel-t" data-panel-t>{e(titulo)}</span></div>
{nav(activa)}
{cuerpo}
{pie()}"""


def visor_datos():
    return json.dumps([{"slug": p["slug"], "t": p["corto"], "c": D.CATEGORIAS[p["cat"]], "a": p["ano"],
                        "src": C.img(p["slug"], p["portada"])} for p in D.PROYECTOS], ensure_ascii=False)


def inicio():
    lista = "".join(
        f'<li><a href="{p["slug"]}.html" data-slide="{i}"><span class="mono">{i + 1:02d}</span><span>{e(p["corto"])}</span><span class="mono li-c">{e(D.CATEGORIAS[p["cat"]])}</span></a></li>'
        for i, p in enumerate(D.PROYECTOS))
    indice = []
    for i, p in enumerate(D.PROYECTOS):
        miniaturas = "".join(f'<img src="{C.img(p["slug"], n)}" alt="" loading="lazy">' for n, w, h in D.imagenes(p["slug"])[:5])
        indice.append(f"""<div class="ix-fila" data-ix>
  <a class="ix-cab" href="{p['slug']}.html">
    <span class="mono">{i + 1:02d}</span><span class="ix-t">{e(p['titulo'])}</span><span class="ix-c">{e(D.CATEGORIAS[p['cat']])}</span>
    <span class="ix-cifra">{e(p['cifra'])} <small>{e(p['cifra_t'])}</small></span><span class="mono">{e(p['ano'])}</span>
  </a>
  <div class="ix-tira" data-ix-tira><div class="ix-tira-in">{miniaturas}</div></div>
</div>""")
    paletas = []
    for p in D.PROYECTOS[:8] + D.PROYECTOS[8:]:
        sw = "".join(f'<button type="button" class="sw" style="--c:{c}" data-copiar="{c}" title="Copy {c}"><span class="mono">{c}</span></button>' for c in C.paleta(p["slug"]))
        paletas.append(f'<a class="pal-f" href="{p["slug"]}.html"><span class="pal-t">{e(p["corto"])}</span></a><div class="pal-sw">{sw}</div>')
    servicios = "".join(f'<li><span class="mono">0{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""<main>
  <section class="hero rj">
    <h1 class="hero-t" data-lineas><span>Esteban</span><span>Guillen<sup class="mono">(EG)</sup></span></h1>
    <div class="hero-meta">
      <p class="hero-bio">{e(D.BIO)}</p>
      <dl class="hero-cifras">
        <div><dt class="mono">Campaign views</dt><dd>1.3M</dd></div>
        <div><dt class="mono">Years of experience</dt><dd data-contar="8">8</dd></div>
        <div><dt class="mono">Published pieces</dt><dd data-contar="{sum(len(D.imagenes(p['slug'])) for p in D.PROYECTOS)}">{sum(len(D.imagenes(p['slug'])) for p in D.PROYECTOS)}</dd></div>
      </dl>
    </div>
    <div class="visor-wrap">
      <ol class="visor-lista" data-visor-lista>{lista}</ol>
      <figure class="visor" data-visor>
        <canvas data-gl aria-hidden="true"></canvas>
        <img class="visor-respaldo" src="{C.img(D.PROYECTOS[0]['slug'], D.PROYECTOS[0]['portada'])}" alt="Cover of {e(D.PROYECTOS[0]['titulo'])}" data-respaldo>
        <figcaption class="visor-pie"><span class="mono" data-v-n>01 / 12</span><span data-v-t>{e(D.PROYECTOS[0]['corto'])}</span><span class="mono" data-v-c>{e(D.CATEGORIAS[D.PROYECTOS[0]['cat']])}</span></figcaption>
        <span class="visor-barra" aria-hidden="true"><i data-v-barra></i></span>
      </figure>
      <script type="application/json" data-visor-datos>{visor_datos()}</script>
    </div>
  </section>

  <section class="sec rj" id="indice">
    <header class="sec-cab"><p class="mono">02 — Index</p><h2 data-lineas>Twelve projects,<br>six disciplines.</h2></header>
    <div class="ix">{"".join(indice)}</div>
  </section>

  <section class="sec rj sec-negra">
    <header class="sec-cab"><p class="mono">03 — Color</p><h2 data-lineas>The real palette<br>of every project.</h2><p class="sec-nota">Colors sampled from the published pieces. Tap one to copy its code.</p></header>
    <div class="paletas">{"".join(paletas)}</div>
  </section>

  <section class="sec rj">
    <header class="sec-cab"><p class="mono">04 — Experience</p><h2 data-lineas>Eight years,<br>from Lima to Miami.</h2><p class="sec-nota"><a class="subraya" href="cv.html">Full résumé →</a></p></header>
    {C.recorrido()}
  </section>

  <section class="sec rj">
    <header class="sec-cab"><p class="mono">05 — Disciplines</p><h2 data-lineas>What I do.</h2></header>
    <ol class="servicios">{servicios}</ol>
  </section>
</main>"""
    return C.documento(f"{D.NOMBRE} · Studio", D.BIO, FUENTES, envoltura(cuerpo, "index.html", "01", "Home"), clase="pg-inicio")


def trabajo():
    filtros = [("todo", "All", len(D.PROYECTOS))] + [(k, v, sum(1 for p in D.PROYECTOS if p["cat"] == k)) for k, v in D.CATEGORIAS.items()]
    botones = "".join(f'<button type="button" data-filtro="{k}" class="{"activo" if k == "todo" else ""}" aria-pressed="{"true" if k == "todo" else "false"}">{e(t)} <sup>{n}</sup></button>' for k, t, n in filtros)
    items = []
    for i, p in enumerate(D.PROYECTOS):
        items.append(f"""<a class="it" href="{p['slug']}.html" data-cat="{p['cat']}">
  <span class="it-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}" loading="lazy"></span>
  <span class="it-n mono">{i + 1:02d}</span><span class="it-t">{e(p['titulo'])}</span><span class="it-c">{e(D.CATEGORIAS[p['cat']])}</span><span class="it-a mono">{e(p['ano'])}</span>
</a>""")
    cuerpo = f"""<main>
  <section class="pag-cab rj">
    <p class="mono">02 — Index</p>
    <h1 data-lineas>Index</h1>
    <p class="pag-intro">Twelve projects from 2022 to 2026: video, photography, sports, brand, web and gaming. Switch between list and grid.</p>
  </section>
  <div class="herr-barra rj">
    <div class="filtros" role="group" aria-label="Filter">{botones}</div>
    <div class="vistas" role="group" aria-label="View"><button type="button" data-vista="lista" class="activo" aria-pressed="true">List</button><button type="button" data-vista="cuadricula" aria-pressed="false">Grid</button></div>
  </div>
  <section class="items rj vista-lista" data-items>{"".join(items)}</section>
</main>"""
    return C.documento(f"Work · {D.NOMBRE}", "Project index.", FUENTES, envoltura(cuerpo, "work.html", "02", "Index"), clase="pg-trabajo")


def proyecto(p):
    i = D.PROYECTOS.index(p)
    sig = D.siguiente(p["slug"])
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    datos = "".join(f'<div><dd>{e(v)}</dd><dt class="mono">{e(t)}</dt></div>' for v, t in p["datos"])
    sw = "".join(f'<button type="button" class="sw" style="--c:{c}" data-copiar="{c}" title="Copy {c}"><span class="mono">{c}</span></button>' for c in C.paleta(p["slug"]))
    # cuadrícula modular: cada imagen ocupa columnas según su proporción
    modulos = []
    for k, (n, w, h) in enumerate(D.imagenes(p["slug"])):
        ar = w / h
        if ar > 1.6:
            span = 12
        elif ar > 1.15:
            span = 8 if k % 3 == 0 else 6
        elif ar > 0.8:
            span = 6 if k % 2 == 0 else 4
        else:
            span = 4 if ar > 0.45 else 4
        largo = " largo" if ar < 0.45 else ""
        modulos.append(f'<figure class="mod{largo}" style="--s:{span}" data-i="{k}"><img src="{C.img(p["slug"], n)}" alt="" loading="lazy" width="{w}" height="{h}"><figcaption class="mono">{k + 1:02d}</figcaption></figure>')
    video = C.bloque_video(p)
    cuerpo = f"""<main>
  <section class="p-cab rj">
    <p class="mono p-miga"><a href="work.html">Index</a> / {i + 1:02d} / {e(D.CATEGORIAS[p['cat']])}</p>
    <h1 data-lineas>{e(p['titulo'])}</h1>
  </section>
  <figure class="p-portada rj" data-portada><span><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"></span></figure>
  <section class="p-cuerpo rj">
    <aside class="p-meta">
      <dl>
        <div><dt class="mono">Number</dt><dd>{i + 1:02d} of {len(D.PROYECTOS)}</dd></div>
        <div><dt class="mono">Client</dt><dd>{e(p['cliente'])}</dd></div>
        <div><dt class="mono">My role</dt><dd>{e(D.ROLES[p['cat']])}</dd></div>
        <div><dt class="mono">Discipline</dt><dd>{e(D.CATEGORIAS[p['cat']])}</dd></div>
        <div><dt class="mono">Year</dt><dd>{e(p['ano'])}</dd></div>
        <div><dt class="mono">Tools</dt><dd>{e(', '.join(p['herr']))}</dd></div>
      </dl>
      <p class="mono p-pal-t">Sampled palette</p>
      <div class="p-pal">{sw}</div>
    </aside>
    <div class="p-txt">
      <p class="p-res" data-lineas>{e(p['resumen'])}</p>
      {textos}
      <dl class="p-datos">{datos}</dl>
    </div>
  </section>
  {f'<section class="rj">{video}</section>' if video else ''}
  <section class="mods rj" data-galeria>{"".join(modulos)}</section>
  <a class="sig rj" href="{sig['slug']}.html" data-roll>
    <span class="mono">Next — {D.PROYECTOS.index(sig) + 1:02d}</span>
    <span class="sig-t"><span>{e(sig['titulo'])}</span></span>
    <span class="sig-img"><img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></span>
  </a>
</main>
<div class="lb" data-lb hidden><button type="button" class="mono lb-x" data-lb-x>Close [Esc]</button><img alt="" data-lb-img><span class="mono lb-n" data-lb-n></span><button type="button" class="lb-a" data-lb-a aria-label="Previous">←</button><button type="button" class="lb-s" data-lb-s aria-label="Next">→</button></div>"""
    return C.documento(f"{p['corto']} · {D.NOMBRE}", p["resumen"], FUENTES, envoltura(cuerpo, "", f"{i + 1:02d}", p["corto"]), clase="pg-proyecto")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    herr = "".join(f"<li>{e(h)}</li>" for h in D.HERRAMIENTAS)
    cuerpo = f"""<main>
  <section class="pag-cab rj"><p class="mono">03 — About</p><h1 data-lineas>About</h1></section>
  <section class="perfil rj">
    <figure class="perfil-foto" data-portada><span><img src="{C.retrato()}" alt="Portrait of {e(D.NOMBRE)}"></span><figcaption class="mono">Esteban Guillen · {e(D.CIUDAD)}</figcaption></figure>
    <div class="perfil-txt"><p class="p-res" data-lineas>{e(D.BIO)}</p><div class="perfil-cols">{bio}</div></div>
  </section>
  <section class="sec rj">
    <header class="sec-cab"><p class="mono">Experience</p><p class="sec-nota"><a class="subraya" href="cv.html">Full résumé →</a> · <a class="subraya" href="{e(D.CV_PDF)}" download>PDF ↓</a></p></header>
    {C.recorrido()}
    <header class="sec-cab" style="margin-top:72px"><p class="mono">Tools</p></header>
    <ul class="herrs">{herr}</ul>
  </section>
</main>"""
    return C.documento(f"About · {D.NOMBRE}", D.BIO, FUENTES, envoltura(cuerpo, "about.html", "03", "About"), clase="pg-sobre")


def contacto():
    cuerpo = f"""<main>
  <section class="pag-cab rj"><p class="mono">05 — Contact</p><h1 data-lineas>Let's talk<br>about your team.</h1></section>
  <section class="ct rj">
    <button type="button" class="ct-correo" data-copiar="{e(D.CORREO)}"><span class="mono" data-copiado>Email — click to copy</span><b>{e(D.CORREO)}</b></button>
    <dl class="ct-tabla">
      <div><dt class="mono">Résumé</dt><dd><a href="cv.html">View online</a> · <a href="{e(D.CV_PDF)}" download>Download PDF ↓</a></dd></div>
      <div><dt class="mono">Instagram</dt><dd><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">{e(D.INSTAGRAM_T)} ↗</a></dd></div>
      <div><dt class="mono">Location</dt><dd>{e(D.CIUDAD)}</dd></div>
      <div><dt class="mono">Status</dt><dd><span class="punto"></span> {e(D.DISPONIBLE)}</dd></div>
      <div><dt class="mono">Services</dt><dd>{e(' · '.join(t for t, _ in D.SERVICIOS))}</dd></div>
    </dl>
  </section>
</main>"""
    return C.documento(f"Contact · {D.NOMBRE}", "Get in touch about a role or a project.", FUENTES, envoltura(cuerpo, "contact.html", "05", "Contact"), clase="pg-contacto")


def cv():
    cuerpo = f"""<main>
  <section class="pag-cab rj"><p class="mono">04 — Résumé</p><h1 data-lineas>Résumé</h1></section>
  <section class="rj">{C.cv_secciones("mono cv-h")}</section>
</main>"""
    return C.documento(f"Résumé · {D.NOMBRE}", D.CV_RESUMEN, FUENTES, envoltura(cuerpo, "cv.html", "04", "Résumé"), clase="pg-cv")


def paginas():
    out = {"index.html": inicio(), "work.html": trabajo(), "about.html": sobre(), "cv.html": cv(), "contact.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
