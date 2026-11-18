# -*- coding: utf-8 -*-
"""Línea 2 · SECCIÓN — la web como señalética de un recinto.

Letreros de dirección, un plano del arena donde cada proyecto es una sección,
y cada página de proyecto es una entrada con su talón.
"""
import math

import comun as C
import datos as D
from comun import e

FUENTES = "family=Big+Shoulders+Display:wght@600;800;900&family=Overpass:wght@400;600;700&family=Overpass+Mono:wght@400;600"

SECCIONES = {p["slug"]: 101 + i for i, p in enumerate(D.PROYECTOS)}


def flecha(direccion="der"):
    rot = {"der": 0, "abajo": 90, "izq": 180, "arriba": 270, "diag": -45}[direccion]
    return (f'<svg class="flecha" viewBox="0 0 24 24" aria-hidden="true" style="transform:rotate({rot}deg)">'
            '<path d="M3 10.5h12.2l-4.6-4.6 2.1-2.1 8.2 8.2-8.2 8.2-2.1-2.1 4.6-4.6H3z" fill="currentColor"/></svg>')


def cabecera(activa=""):
    entradas = [("trabajo.html", "100", "Trabajo", "arriba"), ("sobre.html", "200", "Sobre mí", "der"),
                ("contacto.html", "300", "Contacto", "izq")]
    items = "".join(
        f'<a href="{h}" class="nav-letrero"{" aria-current=\"page\"" if h == activa else ""}>{flecha(d)}'
        f'<span class="nav-num">{n}</span><span>{e(t)}</span></a>' for h, n, t, d in entradas)
    return f"""<header class="letrero-sup">
  <a href="index.html" class="marca"><span class="marca-n">{e(D.NOMBRE)}</span><span class="marca-r">Video · Web · Eventos</span></a>
  <nav aria-label="Principal">{items}</nav>
</header>"""


def pie():
    return f"""<footer class="pie">
  <div class="pie-in">
    <a class="salida" href="contacto.html"><span class="salida-pict" aria-hidden="true">{persona()}</span><span><b>Salida</b><span>Taquilla 300 · Contacto</span></span>{flecha('der')}</a>
    <p class="pie-legal">© 2026 {e(D.NOMBRE)} · {e(D.UBICACION)} · Todas las secciones abiertas</p>
  </div>
</footer>"""


def persona():
    # Pictograma de salida simplificado (figura caminando).
    return ('<svg viewBox="0 0 24 24"><circle cx="14" cy="4" r="2.2" fill="currentColor"/>'
            '<path d="M10.5 8.2l3.6-.9 2.2 3.4 3 1-0.6 1.9-3.8-1.2-1-1.4-1 3.6 2.6 2.4 0.8 5.2h-2.1l-0.7-4.2-3.1-2.6-1.4 3.6-3.6 3.2-1.4-1.5 3.1-2.8 2.2-6.3-1.5.5-1.2 2.6-1.9-.8 1.6-3.6z" fill="currentColor"/></svg>')


def _pt(cx, cy, rx, ry, a):
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


def plano(activo=None, compacto=False):
    """Plano SVG del recinto. Anillo 100 (proyectos 101–104 a pie de pista) y anillo 300."""
    cx, cy = 500, 330
    partes = []
    # anillo 300 (decorativo)
    n3 = 24
    for i in range(n3):
        a0 = math.pi / 2 + (i / n3) * 2 * math.pi + 0.012
        a1 = math.pi / 2 + ((i + 1) / n3) * 2 * math.pi - 0.012
        partes.append(("anillo3", 301 + i, a0, a1, (360, 250), (455, 315), None))
    # anillo 100
    n1 = 20
    proyectos = list(D.PROYECTOS)
    for i in range(n1):
        a0 = math.pi / 2 - 0.5 * (2 * math.pi / n1) + (i / n1) * 2 * math.pi + 0.014
        a1 = a0 + (2 * math.pi / n1) - 0.028
        p = None
        # los proyectos van en el lateral largo inferior, centrados frente a la pista
        idx = {1: 0, 0: 1, 19: 2, 18: 3}.get(i)
        if idx is not None:
            p = proyectos[idx]
        num = SECCIONES[p["slug"]] if p else 105 + ((i - 2) % n1)
        partes.append(("anillo1", num, a0, a1, (250, 160), (345, 238), p))

    svg = []
    for clase, num, a0, a1, (rxi, ryi), (rxo, ryo), p in partes:
        x0, y0 = _pt(cx, cy, rxi, ryi, a0)
        x1, y1 = _pt(cx, cy, rxo, ryo, a0)
        x2, y2 = _pt(cx, cy, rxo, ryo, a1)
        x3, y3 = _pt(cx, cy, rxi, ryi, a1)
        d = (f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}A{rxo} {ryo} 0 0 1 {x2:.1f} {y2:.1f}"
             f"L{x3:.1f} {y3:.1f}A{rxi} {ryi} 0 0 0 {x0:.1f} {y0:.1f}Z")
        am = (a0 + a1) / 2
        lx, ly = _pt(cx, cy, (rxi + rxo) / 2, (ryi + ryo) / 2, am)
        if p:
            cls = "sec sec-p" + (" activa" if p["slug"] == activo else "")
            svg.append(f'<a href="{p["slug"]}.html" class="{cls}" data-sec="{p["slug"]}" aria-label="Sección {num}: {e(p["titulo"])}">'
                       f'<path d="{d}"/><text x="{lx:.1f}" y="{ly + 6:.1f}" text-anchor="middle">{num}</text></a>')
        else:
            svg.append(f'<g class="sec {clase}"><path d="{d}"/>'
                       + (f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle">{num}</text>' if clase == "anillo1" else "")
                       + "</g>")
    pista = (f'<g class="pista" aria-hidden="true"><rect x="{cx - 190}" y="{cy - 92}" width="380" height="184" rx="86"/>'
             f'<line x1="{cx}" y1="{cy - 92}" x2="{cx}" y2="{cy + 92}"/><circle cx="{cx}" cy="{cy}" r="30"/>'
             f'<text x="{cx - 110}" y="{cy + 8}" text-anchor="middle">PISTA</text></g>')
    leyenda = '<text class="plano-n" x="500" y="-12" text-anchor="middle">NORTE · ESCENARIO</text>'
    return (f'<svg class="plano{" plano-compacto" if compacto else ""}" viewBox="40 -34 920 694" role="group" '
            f'aria-label="Plano del recinto: las secciones 101 a 104 son proyectos">{leyenda}{"".join(svg)}{pista}</svg>')


def panel_plano(p):
    n = SECCIONES[p["slug"]]
    return f"""<div class="plano-panel" data-panel aria-live="polite">
  <p class="panel-sec">Sección <b data-p-num>{n}</b></p>
  <img src="assets/{p['imagenes'][0][0]}" alt="" data-p-img>
  <h3 data-p-tit>{e(p['titulo'])}</h3>
  <p data-p-sub>{e(p['subtitulo'])}</p>
  <a class="boton" href="{p['slug']}.html" data-p-link>Ir a la sección {flecha('der')}</a>
</div>"""


def datos_plano():
    import json
    return json.dumps({p["slug"]: {"num": SECCIONES[p["slug"]], "titulo": p["titulo"], "sub": p["subtitulo"],
                                   "img": p["imagenes"][0][0]} for p in D.PROYECTOS}, ensure_ascii=False)


def inicio():
    p0 = D.proyecto("arena-pass")
    servicios = "".join(
        f'<li><span class="serv-ic" aria-hidden="true">{flecha("der")}</span><b>{e(t)}</b><span>{e(d)}</span></li>'
        for t, d in D.SERVICIOS)
    cuerpo = f"""{cabecera()}
<main>
  <section class="hero franja">
    <div class="franja-in hero-in">
      <div class="hero-nombre">
        <p class="placa">Puerta A · Acceso general</p>
        <h1><span>Esteban</span><span>Guillen</span></h1>
        <p class="hero-rol">{e(D.ROL)} en {e(D.EMPRESA)}. También construyo la web, el 3D y las plataformas que usan los eventos.</p>
      </div>
      <figure class="hero-foto">
        <img src="assets/retrato.jpg" alt="Retrato de {e(D.NOMBRE)}">
        <figcaption><span>Credencial</span><b>Producción · Video · Web</b></figcaption>
      </figure>
    </div>
  </section>
  <section class="direcciones franja franja-negra" aria-label="Direcciones">
    <div class="franja-in">
      <a class="direccion" href="trabajo.html">{flecha('arriba')}<span class="dir-num">101–104</span><span class="dir-t">Proyectos</span><span class="dir-d">Web, 3D, plataformas y video</span></a>
      <a class="direccion" href="sobre.html">{flecha('der')}<span class="dir-num">200</span><span class="dir-t">Sobre mí</span><span class="dir-d">Trayectoria y herramientas</span></a>
      <a class="direccion" href="contacto.html">{flecha('izq')}<span class="dir-num">300</span><span class="dir-t">Taquilla</span><span class="dir-d">Contacto y disponibilidad</span></a>
    </div>
  </section>
  <section class="franja">
    <div class="franja-in">
      <div class="titulo-sec"><h2>Plano del recinto</h2><p>Las secciones a pie de pista son mis proyectos. Pasa el cursor o toca una para ver qué hay dentro.</p></div>
      <div class="plano-wrap" data-plano>
        {plano()}
        {panel_plano(p0)}
        <script type="application/json" data-plano-datos>{datos_plano()}</script>
      </div>
    </div>
  </section>
  <section class="franja franja-clara">
    <div class="franja-in">
      <div class="titulo-sec"><h2>Servicios</h2><p>{e(D.BIO_CORTA)}</p></div>
      <ul class="servicios">{servicios}</ul>
    </div>
  </section>
</main>
{pie()}"""
    return C.documento(f"{D.NOMBRE} · Sección", D.BIO_CORTA, FUENTES, cuerpo, clase="pg-inicio")


def codigo_barras(semilla):
    import random
    r = random.Random(semilla)
    x, barras = 0, []
    while x < 196:
        w = r.choice([1, 1, 2, 2, 3, 4])
        if r.random() > 0.4:
            barras.append(f'<rect x="{x}" y="0" width="{w}" height="48"/>')
        x += w + r.choice([1, 2])
    return f'<svg class="barras" viewBox="0 0 200 48" preserveAspectRatio="none" aria-hidden="true">{"".join(barras)}</svg>'


def pagina_proyecto(p):
    n = SECCIONES[p["slug"]]
    sig = D.siguiente(p["slug"])
    hice = "".join(f"<li>{e(x)}</li>" for x in p["hice"])
    dec = "".join(f'<div class="panel-dec"><h3>{flecha("der")}{e(t)}</h3><p>{e(d)}</p></div>' for t, d in p["decisiones"])
    cifras = "".join(f'<div class="marcador-c"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in p["cifras"])
    galeria = "".join(f'<figure><img src="assets/{i}" alt="{e(a)}" loading="lazy"><figcaption>{e(a)}</figcaption></figure>'
                      for i, a in p["imagenes"][1:])
    reel = ""
    if p["slug"] == "edicion":
        reel = (f'<a class="boton" href="{e(D.VIMEO)}" target="_blank" rel="noopener">Ver reel {flecha("diag")}</a>' if D.VIMEO
                else '<p class="pendiente">Reel 2026 · próximamente en esta sección</p>')
    nota = f'<p class="nota">{e(p["nota"])}</p>' if p.get("nota") else ""
    cuerpo = f"""{cabecera()}
<main>
  <section class="franja proy-cab">
    <div class="franja-in proy-cab-in">
      <div class="placa-sec"><span>Sección</span><b>{n}</b></div>
      <div>
        <p class="miga"><a href="trabajo.html">Directorio</a> / {e(p['tipo'])}</p>
        <h1>{e(p['titulo'])}</h1>
        <p class="proy-sub">{e(p['subtitulo'])}</p>
      </div>
    </div>
  </section>
  <section class="franja">
    <div class="franja-in">
      <div class="entrada">
        <div class="entrada-cuerpo">
          <img src="assets/{p['imagenes'][0][0]}" alt="{e(p['imagenes'][0][1])}">
          <p class="entrada-resumen">{e(p['resumen'])}</p>
        </div>
        <div class="entrada-talon">
          <dl>
            <div><dt>Evento</dt><dd>{e(p['titulo'])}</dd></div>
            <div class="fila3"><div><dt>Sección</dt><dd>{n}</dd></div><div><dt>Fila</dt><dd>{e(p['ano'])}</dd></div><div><dt>Asiento</dt><dd>{e(p['tipo'])}</dd></div></div>
            <div><dt>Función</dt><dd>{e(p['rol'])}</dd></div>
            <div><dt>Herramientas</dt><dd>{e(' · '.join(p['stack']))}</dd></div>
          </dl>
          {reel}
          {codigo_barras(n)}
          <p class="talon-cod">EG-{n}-{p['ano'][:4]}</p>
        </div>
      </div>
    </div>
  </section>
  <section class="franja franja-negra">
    <div class="franja-in marcador">{cifras}</div>
  </section>
  <section class="franja">
    <div class="franja-in texto-dos">
      <div><h2>El encargo</h2><p>{e(p['brief'])}</p></div>
      <div><h2>Lo que hice</h2><ul class="lista">{hice}</ul></div>
    </div>
  </section>
  <section class="franja franja-clara">
    <div class="franja-in">
      <div class="titulo-sec"><h2>Decisiones</h2></div>
      <div class="decisiones">{dec}</div>
    </div>
  </section>
  {f'<section class="franja"><div class="franja-in galeria">{galeria}</div></section>' if galeria else ''}
  {f'<section class="franja"><div class="franja-in">{nota}</div></section>' if nota else ''}
  <section class="franja franja-negra">
    <a class="franja-in proxima" href="{sig['slug']}.html">
      <span class="proxima-l">Próxima sección</span>
      <span class="proxima-n">{SECCIONES[sig['slug']]}</span>
      <span class="proxima-t">{e(sig['titulo'])}</span>
      {flecha('der')}
    </a>
  </section>
</main>
{pie()}"""
    return C.documento(f"{p['titulo']} · Sección {n}", p["resumen"], FUENTES, cuerpo, clase="pg-proyecto")


def trabajo():
    p0 = D.proyecto("arena-pass")
    filas = "".join(
        f'<a class="dir-fila" href="{p["slug"]}.html"><span class="df-sec">{SECCIONES[p["slug"]]}</span>'
        f'<span class="df-t"><b>{e(p["titulo"])}</b><span>{e(p["subtitulo"])}</span></span>'
        f'<span class="df-tipo">{e(p["tipo"])}</span><span class="df-ano">{e(p["ano"])}</span>{flecha("der")}</a>'
        for p in D.PROYECTOS)
    cuerpo = f"""{cabecera('trabajo.html')}
<main>
  <section class="franja proy-cab">
    <div class="franja-in proy-cab-in">
      <div class="placa-sec"><span>Nivel</span><b>100</b></div>
      <div><p class="miga">Directorio del recinto</p><h1>Trabajo</h1>
      <p class="proy-sub">Cuatro secciones a pie de pista: una web con panel, un arena en 3D, una plataforma para eventos y mi trabajo de edición.</p></div>
    </div>
  </section>
  <section class="franja franja-negra">
    <div class="franja-in directorio">
      <div class="dir-cab"><span>Sec.</span><span>Proyecto</span><span>Tipo</span><span>Año</span><span></span></div>
      {filas}
    </div>
  </section>
  <section class="franja">
    <div class="franja-in">
      <div class="titulo-sec"><h2>Dónde está cada uno</h2></div>
      <div class="plano-wrap" data-plano>
        {plano()}
        {panel_plano(p0)}
        <script type="application/json" data-plano-datos>{datos_plano()}</script>
      </div>
    </div>
  </section>
</main>
{pie()}"""
    return C.documento(f"Trabajo · {D.NOMBRE}", "Directorio de proyectos.", FUENTES, cuerpo, clase="pg-trabajo")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    herr = "".join(
        f'<div class="herr"><h3>{e(k)}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in v)}</ul></div>'
        for k, v in D.HERRAMIENTAS.items())
    cuerpo = f"""{cabecera('sobre.html')}
<main>
  <section class="franja proy-cab">
    <div class="franja-in proy-cab-in">
      <div class="placa-sec"><span>Sección</span><b>200</b></div>
      <div><p class="miga">Sobre mí</p><h1>{e(D.NOMBRE)}</h1><p class="proy-sub">{e(D.ROL)} en {e(D.EMPRESA)}</p></div>
    </div>
  </section>
  <section class="franja">
    <div class="franja-in sobre">
      <div class="credencial">
        <div class="cred-agujero" aria-hidden="true"></div>
        <p class="cred-tipo">Producción</p>
        <img src="assets/retrato.jpg" alt="Retrato de {e(D.NOMBRE)}">
        <p class="cred-nombre">{e(D.NOMBRE)}</p>
        <p class="cred-rol">Video · Web</p>
        <p class="cred-acceso">Todas las áreas</p>
      </div>
      <div class="sobre-texto">
        {bio}
        <dl class="datos">
          <div><dt>Base</dt><dd>{e(D.UBICACION)}</dd></div>
          <div><dt>Idiomas</dt><dd>{e(' · '.join(D.IDIOMAS))}</dd></div>
          <div><dt>Experiencia</dt><dd>{e(D.ANOS)} años</dd></div>
        </dl>
      </div>
    </div>
  </section>
  <section class="franja franja-clara">
    <div class="franja-in">
      <div class="titulo-sec"><h2>Herramientas</h2></div>
      <div class="herrs">{herr}</div>
    </div>
  </section>
</main>
{pie()}"""
    return C.documento(f"Sobre mí · {D.NOMBRE}", D.BIO_CORTA, FUENTES, cuerpo, clase="pg-sobre")


def contacto():
    links = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)} {flecha("diag")}</a></li>'
                    for t, u in C.contacto_links())
    cuerpo = f"""{cabecera('contacto.html')}
<main>
  <section class="franja proy-cab">
    <div class="franja-in proy-cab-in">
      <div class="placa-sec"><span>Taquilla</span><b>300</b></div>
      <div><p class="miga">Contacto</p><h1>Taquilla abierta</h1>
      <p class="proy-sub">Campañas, piezas para redes, una web que tu equipo pueda actualizar o una herramienta para tu evento. Respondo en español o en inglés.</p></div>
    </div>
  </section>
  <section class="franja">
    <div class="franja-in">
      <div class="ventanilla">
        <p class="vent-l">Escríbeme a</p>
        <p class="vent-correo" id="correo">{e(D.CORREO)}</p>
        <div class="vent-acc"><button type="button" class="boton" data-copiar="correo">Copiar correo</button><span class="copiado" data-copiado role="status"></span></div>
      </div>
      <ul class="links">{links}</ul>
      <dl class="datos datos-fila">
        <div><dt>Base</dt><dd>{e(D.UBICACION)}</dd></div>
        <div><dt>Idiomas</dt><dd>{e(' · '.join(D.IDIOMAS))}</dd></div>
        <div><dt>Entregas</dt><dd>16:9 · 9:16 · 1:1 · Web</dd></div>
      </dl>
    </div>
  </section>
</main>
{pie()}"""
    return C.documento(f"Contacto · {D.NOMBRE}", "Escríbeme para tu próximo proyecto.", FUENTES, cuerpo, clase="pg-contacto")


def paginas():
    out = {"index.html": inicio(), "trabajo.html": trabajo(), "sobre.html": sobre(), "contacto.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = pagina_proyecto(p)
    return out
