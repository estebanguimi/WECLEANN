# -*- coding: utf-8 -*-
"""Línea 3 · CONTACTOS — la web como hoja de contactos de laboratorio.

Cada proyecto es una tira de película. Los fotogramas elegidos van marcados a lápiz graso,
y una lupa permite revisar cualquier fotograma como sobre una mesa de luz.
"""
import math
import os
import random

from PIL import Image

import comun as C
import datos as D
from comun import e

FUENTES = "family=Schibsted+Grotesk:wght@400;500;700;800&family=DM+Mono:wght@400;500&family=Reenie+Beanie"
AQUI = os.path.dirname(os.path.abspath(__file__))
_AR = {}


def ar(img):
    if img not in _AR:
        w, h = Image.open(os.path.join(AQUI, "assets", img)).size
        _AR[img] = w / h
    return _AR[img]


ROLLOS = {p["slug"]: i + 1 for i, p in enumerate(D.PROYECTOS)}

# Fotogramas por proyecto: (imagen, zoom, x%, y%). El zoom recorta como lo haría una ampliación.
FOTOGRAMAS = {
    "harris-media": [("hmg-home.jpg", 1, 50, 50), ("hmg-home.jpg", 2.2, 40, 42), ("hmg-cifras.jpg", 1, 50, 50),
                     ("hmg-servicios.jpg", 1.6, 20, 50), ("hmg-obras.jpg", 1, 50, 60), ("hmg-obras.jpg", 2.4, 30, 50)],
    "arena-pass": [("arena-aerea.jpg", 1, 50, 50), ("arena-aerea.jpg", 2.0, 45, 55), ("arena-concierto.jpg", 1.4, 30, 60),
                   ("arena-asientos.jpg", 1, 50, 50), ("arena-asientos.jpg", 1.8, 40, 80), ("arena-aerea.jpg", 2.6, 90, 40)],
    "cleanspace": [("cs-login.jpg", 1.8, 25, 50), ("cs-registro.jpg", 1.8, 60, 40), ("cs-turnos.jpg", 1.8, 50, 45),
                   ("cs-turnos.jpg", 2.6, 45, 40), ("cs-admin.jpg", 1.8, 55, 45), ("cs-login.jpg", 3.2, 12, 50)],
    "edicion": [("evento.jpg", 1, 50, 50), ("evento.jpg", 2.2, 50, 15), ("evento.jpg", 2.0, 20, 70),
                ("evento.jpg", 2.6, 75, 35), ("evento.jpg", 1.5, 50, 90), ("evento.jpg", 3.0, 52, 62)],
}
ELEGIDO = {"harris-media": 0, "arena-pass": 0, "cleanspace": 2, "edicion": 1}
DESCARTE = {"harris-media": 4, "arena-pass": 5, "cleanspace": 5, "edicion": 4}


# ---------- trazos a mano (lápiz graso) ----------

def trazo_circulo(semilla, w=100, h=70):
    r = random.Random(semilla)
    cx, cy = w / 2, h / 2
    rx, ry = w / 2 - 5, h / 2 - 5
    a0 = r.uniform(-2.6, -2.0)
    giro = 2 * math.pi + r.uniform(0.35, 0.7)
    pts = []
    n = 28
    for i in range(n + 1):
        a = a0 + giro * i / n
        k = 1 + r.uniform(-0.035, 0.035) + 0.05 * i / n
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1, 2):
        d += f" Q{pts[i][0]:.1f} {pts[i][1]:.1f} {pts[i + 1][0]:.1f} {pts[i + 1][1]:.1f}"
    return (f'<svg class="lapiz lapiz-circulo" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="{d}" vector-effect="non-scaling-stroke"/></svg>')


def trazo_x(semilla):
    r = random.Random(semilla)
    j = lambda: r.uniform(-4, 4)
    return ('<svg class="lapiz lapiz-x" viewBox="0 0 100 70" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="M{12 + j():.0f} {10 + j():.0f} Q50 {36 + j():.0f} {88 + j():.0f} {60 + j():.0f}" vector-effect="non-scaling-stroke"/>'
            f'<path d="M{86 + j():.0f} {8 + j():.0f} Q{50 + j():.0f} 34 {14 + j():.0f} {62 + j():.0f}" vector-effect="non-scaling-stroke"/></svg>')


def trazo_flecha(semilla, clase=""):
    r = random.Random(semilla)
    y = r.uniform(18, 26)
    return (f'<svg class="lapiz lapiz-flecha {clase}" viewBox="0 0 120 40" aria-hidden="true">'
            f'<path d="M4 {y:.0f} C 40 {y - 10:.0f}, 80 {y + 8:.0f}, 112 {y - 2:.0f}"/>'
            f'<path d="M98 {y - 13:.0f} L113 {y - 2:.0f} L99 {y + 10:.0f}"/></svg>')


def trazo_subrayado(semilla):
    r = random.Random(semilla)
    return ('<svg class="lapiz lapiz-sub" viewBox="0 0 200 14" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="M3 {r.uniform(8, 10):.0f} C 60 {r.uniform(3, 6):.0f}, 130 {r.uniform(10, 13):.0f}, 197 {r.uniform(5, 8):.0f}" vector-effect="non-scaling-stroke"/></svg>')


# ---------- piezas ----------

def cuadro(img, zoom, x, y, extra="", alt=""):
    tam = max(1, ar(img) / 1.5) * zoom * 100
    return (f'<span class="cuadro" role="img" aria-label="{e(alt)}" data-lupa data-img="assets/{img}" data-sz="{tam / 100:.4f}" data-ar="{ar(img):.4f}" '
            f'data-px="{x}" data-py="{y}" style="background-image:url(assets/{img});background-size:{tam:.1f}% auto;'
            f'background-position:{x}% {y}%">{extra}</span>')


def tira(p, con_nota=True, enlace=True):
    rollo = ROLLOS[p["slug"]]
    fr = FOTOGRAMAS[p["slug"]]
    base = rollo * 6
    celdas = []
    for i, (img, z, x, y) in enumerate(fr):
        extra = ""
        if i == ELEGIDO[p["slug"]]:
            extra = trazo_circulo(rollo * 11 + i)
        elif i == DESCARTE[p["slug"]]:
            extra = trazo_x(rollo * 7 + i)
        num = base + i
        celdas.append(f'<span class="fot"><span class="borde-num">{num} <i>▸{num}A</i></span>'
                      f'{cuadro(img, z, x, y, extra, p["titulo"] + ", fotograma " + str(num))}</span>')
    nota = ""
    if con_nota:
        nota = f'<span class="nota-tira mano">{e(p["titulo"])} {trazo_flecha(rollo, "flecha-nota")}</span>'
    etiqueta = f'<span class="borde-txt">EG 2026 · ROLLO {rollo:02d} · {e(p["tipo"].upper())}</span>'
    tag = "a" if enlace else "div"
    href = f' href="{p["slug"]}.html"' if enlace else ""
    return (f'<{tag} class="tira"{href} aria-label="{e(p["titulo"])}: {e(p["subtitulo"])}">{nota}'
            f'<span class="pelicula">{etiqueta}<span class="cuadros">{"".join(celdas)}</span></span></{tag}>')


def cabecera(activa=""):
    items = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == activa else ""}>{e(t)}</a>' for h, t in C.PAGINAS_FIJAS)
    return f"""<header class="cab">
  <a class="cab-nombre" href="index.html">{e(D.NOMBRE)}</a>
  <span class="cab-sobre mono">Laboratorio · Hoja de contactos 2026</span>
  <nav aria-label="Principal">{items}</nav>
</header>"""


def pie():
    return f"""<footer class="pie">
  <div class="pie-in">
    <p class="pie-mano mano">¿Imprimimos algo juntos?</p>
    <a class="pie-link" href="contacto.html">Pedir copias · Contacto</a>
    <p class="pie-legal mono">© 2026 {e(D.NOMBRE)} · {e(D.UBICACION)} · Revelado a mano en HTML y CSS</p>
  </div>
</footer>"""


def lupa():
    return '<div class="lupa" data-lupa-el aria-hidden="true" hidden></div>'


def inicio():
    tiras = "".join(tira(p) for p in D.PROYECTOS)
    servicios = "".join(
        f'<li><span class="check" aria-hidden="true">{trazo_subrayado(i + 3)}</span><b>{e(t)}</b><span>{e(d)}</span></li>'
        for i, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""{cabecera()}
<main>
  <section class="hero">
    <div class="hero-txt">
      <p class="mono hero-eti">{e(D.ROL)} · {e(D.EMPRESA)}</p>
      <h1>Reviso todo el material. Marco lo que vale.</h1>
      <p class="hero-bio">{e(D.BIO_CORTA)}</p>
    </div>
    <figure class="copia copia-retrato">
      <img src="assets/retrato.jpg" alt="Retrato de {e(D.NOMBRE)}">
      <figcaption class="mano">Esteban, 2026</figcaption>
    </figure>
  </section>
  <section class="hoja" aria-label="Hoja de contactos de proyectos">
    <div class="hoja-cab">
      <p class="mono">Hoja 01 · {len(D.PROYECTOS)} rollos · 35 mm</p>
      <p class="mano hoja-instr">pasa la lupa sobre los fotogramas · toca un rollo para ampliarlo</p>
    </div>
    <div class="tiras">{tiras}</div>
  </section>
  <section class="notas">
    <h2>Lo que hago</h2>
    <ul class="servicios">{servicios}</ul>
  </section>
</main>
{lupa()}
{pie()}"""
    return C.documento(f"{D.NOMBRE} · Contactos", D.BIO_CORTA, FUENTES, cuerpo, clase="pg-inicio")


def pagina_proyecto(p):
    rollo = ROLLOS[p["slug"]]
    sig = D.siguiente(p["slug"])
    img0, alt0 = p["imagenes"][0]
    hice = "".join(f"<li>{e(x)}</li>" for x in p["hice"])
    dec = "".join(
        f'<div class="decision"><span class="dec-n mano">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(p["decisiones"]))
    cifras = "".join(f'<li><b>{e(v)}</b><span>{e(t)}</span></li>' for v, t in p["cifras"])
    galeria = "".join(
        f'<figure class="copia copia-chica"><img src="assets/{i}" alt="{e(a)}" loading="lazy"><figcaption class="mono">{e(a)}</figcaption></figure>'
        for i, a in p["imagenes"][1:])
    reel = ""
    if p["slug"] == "edicion":
        reel = (f'<p><a class="boton" href="{e(D.VIMEO)}" target="_blank" rel="noopener">Ver reel</a></p>' if D.VIMEO
                else '<p class="pendiente mano">reel 2026 → en el revelador</p>')
    nota = f'<p class="nota-pie mono">{e(p["nota"])}</p>' if p.get("nota") else ""
    cuerpo = f"""{cabecera()}
<main>
  <section class="proy-cab">
    <p class="mono"><a href="trabajo.html">Hoja de contactos</a> / Rollo {rollo:02d}</p>
    <h1>{e(p['titulo'])}</h1>
    <p class="proy-sub">{e(p['subtitulo'])}</p>
  </section>
  <section class="ampliacion">
    <figure class="copia copia-grande">
      <img src="assets/{img0}" alt="{e(alt0)}">
      <figcaption class="mono">{rollo * 6 + ELEGIDO[p['slug']]} · {e(alt0)}</figcaption>
    </figure>
    <aside class="margen">
      <p class="mano nota-margen">{e(p['decisiones'][0][0].lower())}</p>
      {trazo_flecha(rollo + 40, 'flecha-margen')}
      <dl class="ficha">
        <div><dt>Rol</dt><dd>{e(p['rol'])}</dd></div>
        <div><dt>Año</dt><dd>{e(p['ano'])}</dd></div>
        <div><dt>Tipo</dt><dd>{e(p['tipo'])}</dd></div>
        <div><dt>Herramientas</dt><dd>{e(', '.join(p['stack']))}</dd></div>
      </dl>
      {reel}
    </aside>
  </section>
  <section class="resumen-proy">
    <p>{e(p['resumen'])}</p>
    <ul class="cifras">{cifras}</ul>
  </section>
  <section class="texto">
    <div><h2>El encargo</h2><p>{e(p['brief'])}</p></div>
    <div><h2>Lo que hice</h2><ul class="lista">{hice}</ul></div>
  </section>
  <section class="decisiones-sec">
    <h2>Decisiones</h2>
    <div class="decisiones">{dec}</div>
  </section>
  <section class="hoja hoja-proy" aria-label="Tira del rollo {rollo}">
    <div class="hoja-cab"><p class="mono">Rollo {rollo:02d} completo</p><p class="mano hoja-instr">pasa la lupa</p></div>
    <div class="tiras">{tira(p, con_nota=False, enlace=False)}</div>
  </section>
  {f'<section class="galeria">{galeria}</section>' if galeria else ''}
  {nota}
  <a class="siguiente" href="{sig['slug']}.html"><span class="mono">Siguiente rollo · {ROLLOS[sig['slug']]:02d}</span><span class="sig-t">{e(sig['titulo'])}</span>{trazo_flecha(ROLLOS[sig['slug']] + 60, 'flecha-sig')}</a>
</main>
{lupa()}
{pie()}"""
    return C.documento(f"{p['titulo']} · {D.NOMBRE}", p["resumen"], FUENTES, cuerpo, clase="pg-proyecto")


def trabajo():
    indice = "".join(
        f'<a class="ind-fila" href="{p["slug"]}.html"><span class="mono">Rollo {ROLLOS[p["slug"]]:02d}</span>'
        f'<span class="ind-t">{e(p["titulo"])}</span><span class="ind-s">{e(p["subtitulo"])}</span>'
        f'<span class="mono">{e(p["tipo"])} · {e(p["ano"])}</span></a>' for p in D.PROYECTOS)
    tiras = "".join(tira(p) for p in D.PROYECTOS)
    cuerpo = f"""{cabecera('trabajo.html')}
<main>
  <section class="proy-cab">
    <p class="mono">Índice de rollos</p>
    <h1>Trabajo</h1>
    <p class="proy-sub">Cuatro rollos: una web con panel propio, un arena en 3D, una plataforma para eventos y mi trabajo de edición.</p>
  </section>
  <nav class="indice" aria-label="Proyectos">{indice}</nav>
  <section class="hoja" aria-label="Hoja de contactos">
    <div class="hoja-cab"><p class="mono">Hoja completa</p><p class="mano hoja-instr">círculo = fotograma elegido · X = descarte</p></div>
    <div class="tiras">{tiras}</div>
  </section>
</main>
{lupa()}
{pie()}"""
    return C.documento(f"Trabajo · {D.NOMBRE}", "Índice de proyectos.", FUENTES, cuerpo, clase="pg-trabajo")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    herr = "".join(
        f'<div class="herr"><h3 class="mono">{e(k)}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in v)}</ul></div>'
        for k, v in D.HERRAMIENTAS.items())
    cuerpo = f"""{cabecera('sobre.html')}
<main>
  <section class="sobre">
    <figure class="copia copia-sobre">
      <img src="assets/retrato.jpg" alt="Retrato de {e(D.NOMBRE)}">
      <figcaption class="mano">Esteban · 2026</figcaption>
    </figure>
    <div class="sobre-txt">
      <p class="mono">Sobre mí</p>
      <h1>{e(D.NOMBRE)}</h1>
      <p class="proy-sub">{e(D.ROL)} en {e(D.EMPRESA)}</p>
      {bio}
      <dl class="ficha ficha-fila">
        <div><dt>Base</dt><dd>{e(D.UBICACION)}</dd></div>
        <div><dt>Idiomas</dt><dd>{e(', '.join(D.IDIOMAS))}</dd></div>
        <div><dt>Experiencia</dt><dd>{e(D.ANOS)} años</dd></div>
      </dl>
    </div>
  </section>
  <section class="herrs-sec">
    <h2>En la mesa de trabajo</h2>
    <div class="herrs">{herr}</div>
  </section>
</main>
{pie()}"""
    return C.documento(f"Sobre mí · {D.NOMBRE}", D.BIO_CORTA, FUENTES, cuerpo, clase="pg-sobre")


def contacto():
    links = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in C.contacto_links())
    cuerpo = f"""{cabecera('contacto.html')}
<main>
  <section class="proy-cab">
    <p class="mono">Contacto</p>
    <h1>Pedido de copias</h1>
    <p class="proy-sub">Campañas, piezas para redes, una web que tu equipo pueda actualizar o una herramienta para tu evento. Respondo en español o en inglés.</p>
  </section>
  <section class="sobre-lab">
    <p class="sobre-lab-tit mono">Sobre de laboratorio · Nº 2026-EG</p>
    <div class="campo"><span class="mono">Nombre</span><span class="campo-v">{e(D.NOMBRE)}</span></div>
    <div class="campo"><span class="mono">Correo</span><span class="campo-v mano campo-correo" id="correo">{e(D.CORREO)}</span>
      <button type="button" class="boton" data-copiar="correo">Copiar</button><span class="copiado mono" data-copiado role="status"></span></div>
    <div class="campo"><span class="mono">Idiomas</span><span class="campo-v">{e(', '.join(D.IDIOMAS))}</span></div>
    <div class="campo"><span class="mono">Base</span><span class="campo-v">{e(D.UBICACION)}</span></div>
    <div class="campo campo-casillas"><span class="mono">Servicio</span>
      <span class="casillas">{''.join(f'<span class="casilla"><span class="caja" aria-hidden="true"></span>{e(t)}</span>' for t, _ in D.SERVICIOS)}</span></div>
    <ul class="links">{links}</ul>
  </section>
</main>
{pie()}"""
    return C.documento(f"Contacto · {D.NOMBRE}", "Escríbeme para tu próximo proyecto.", FUENTES, cuerpo, clase="pg-contacto")


def paginas():
    out = {"index.html": inicio(), "trabajo.html": trabajo(), "sobre.html": sobre(), "contacto.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = pagina_proyecto(p)
    return out
