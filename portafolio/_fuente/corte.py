# -*- coding: utf-8 -*-
"""Línea 1 · CORTE — la web como una sala de montaje.

Fondo gris de sala de color, un monitor de programa y una línea de tiempo real:
cada proyecto es un clip con su entrada y salida en timecode a 24 fps.
"""
import json

import comun as C
import datos as D
from comun import e

FUENTES = "family=Familjen+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500"
COLORES = {"lavanda": "Lavanda", "caribe": "Caribe", "mango": "Mango", "rosa": "Rosa"}


def cabecera(activa=""):
    items = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == activa else ""}>{e(t)}</a>'
        for href, t in C.PAGINAS_FIJAS)
    return f"""<header class="barra">
  <a class="firma" href="index.html"><span class="firma-nombre">{e(D.NOMBRE)}</span><span class="firma-rol">Editor de video · Desarrollo web</span></a>
  <span class="secuencia mono" aria-hidden="true">Secuencia 01 · Portafolio 2026</span>
  <nav aria-label="Principal">{items}</nav>
</header>"""


def pie():
    clips, total = C.clips()
    return f"""<footer class="pie">
  <div class="pie-fila">
    <p class="pie-fin mono">Fin de secuencia <span>{C.tc(total)}</span></p>
    <a class="pie-correo" href="contacto.html">Escríbeme para tu próximo proyecto</a>
  </div>
  <p class="pie-legal mono">© 2026 {e(D.NOMBRE)} · {e(D.UBICACION)}</p>
</footer>"""


def monitor(img, alt, etiqueta, tcode, extra_cls=""):
    return f"""<figure class="monitor {extra_cls}">
  <div class="monitor-pantalla">
    <img src="assets/{img}" alt="{e(alt)}" data-monitor-img>
    <span class="safe" aria-hidden="true"></span>
    <span class="monitor-clip mono" data-monitor-clip>{e(etiqueta)}</span>
    <span class="monitor-tc mono" data-monitor-tc>{tcode}</span>
  </div>
  <figcaption class="monitor-pie mono"><span>Programa</span><span>1920 × 1080 · 23,976 fps</span></figcaption>
</figure>"""


def linea_tiempo(activo=None, compacta=False):
    clips, total = C.clips()
    pct = lambda s: f"{s / total * 100:.4f}%"
    v1 = "".join(
        f'<a class="clip c-{c["color"]}{" activo" if c["slug"] == activo else ""}" href="{c["slug"]}.html" '
        f'style="left:{pct(c["entrada"])};width:{pct(c["salida"] - c["entrada"])}" data-slug="{c["slug"]}">'
        f'<span class="clip-nombre">{e(c["titulo"])}</span><span class="clip-tc mono">{c["tc_in"]}</span></a>'
        for c in clips)
    # V2: rótulos sobre cada clip (títulos que se ven en el monitor)
    v2 = "".join(
        f'<span class="rotulo" style="left:{pct(c["entrada"] + 2)};width:{pct(10)}">{e(c["tipo"])}</span>'
        for c in clips)
    marcas = ""
    for s in range(0, int(total) + 1, 10):
        marcas += f'<span class="regla-marca" style="left:{pct(s)}"><span class="mono">{C.tc(s)[3:8]}</span></span>'
    datos_js = json.dumps({"total": total, "fps": C.FPS, "clips": clips}, ensure_ascii=False)
    pistas = f"""
    <div class="pista"><span class="pista-n mono">V2</span><div class="pista-c">{v2}</div></div>
    <div class="pista pista-v1"><span class="pista-n mono">V1</span><div class="pista-c">{v1}</div></div>
    <div class="pista pista-a"><span class="pista-n mono">A1</span><div class="pista-c"><canvas class="onda" data-semilla="7"></canvas></div></div>"""
    if not compacta:
        pistas += """
    <div class="pista pista-a"><span class="pista-n mono">A2</span><div class="pista-c"><canvas class="onda" data-semilla="19"></canvas></div></div>"""
    return f"""<section class="timeline{' timeline-compacta' if compacta else ''}" aria-label="Línea de tiempo de proyectos">
  <div class="timeline-cab mono">
    <span>Secuencia 01</span>
    <span class="timeline-tc" data-tl-tc>{C.tc(clips[1]["entrada"]) if not activo else next(c["tc_in"] for c in clips if c["slug"] == activo)}</span>
    <span class="timeline-ayuda">{'Arrastra para revisar · J K L para reproducir' if not compacta else 'Posición de este proyecto en la secuencia'}</span>
  </div>
  <div class="timeline-cuerpo" data-timeline tabindex="0" role="slider" aria-label="Cabezal de reproducción" aria-valuemin="0" aria-valuemax="{int(total)}" aria-valuenow="{int(clips[1]['entrada'])}">
    <div class="regla"><span class="pista-n"></span><div class="pista-c">{marcas}</div></div>
    {pistas}
    <div class="cabezal" data-cabezal aria-hidden="true"></div>
  </div>
  <script type="application/json" data-tl-datos>{datos_js}</script>
</section>"""


def inicio():
    clips, total = C.clips()
    c0 = clips[1]
    p0 = D.proyecto(c0["slug"])
    marcadores = "".join(
        f'<li><span class="marca-tc mono">{C.tc(INI)}</span><span class="marca-punto" aria-hidden="true"></span>'
        f'<span class="marca-t">{e(t)}</span><span class="marca-d">{e(d)}</span></li>'
        for INI, (t, d) in zip([8, 31, 63, 96, 140], D.SERVICIOS))
    bin_filas = "".join(
        f'<a class="bin-fila" href="{c["slug"]}.html"><img src="assets/{c["img"]}" alt="" loading="lazy">'
        f'<span class="bin-nombre"><b>{e(c["titulo"])}</b><span>{e(D.proyecto(c["slug"])["subtitulo"])}</span></span>'
        f'<span class="chip c-{c["color"]}">{e(c["tipo"])}</span><span class="mono bin-dur">{c["dur"]}</span></a>'
        for c in clips)
    cuerpo = f"""{cabecera()}
<main>
  <section class="hero envoltura">
    <div class="hero-texto">
      <p class="eyebrow mono">{e(D.ROL)} · {e(D.EMPRESA)}</p>
      <h1>Edito video para campañas. Programo la web donde se publica.</h1>
      <p class="hero-bio">{e(D.BIO_CORTA)}</p>
      <div class="hero-acciones">
        <a class="boton" href="trabajo.html">Ver proyectos</a>
        <a class="enlace" href="sobre.html">Sobre mí</a>
      </div>
    </div>
    {monitor(c0["img"], p0["imagenes"][0][1], "V1 · " + c0["titulo"], c0["tc_in"])}
  </section>
  <div class="envoltura">{linea_tiempo()}</div>
  <section class="envoltura bloque">
    <div class="bloque-cab"><h2>Proyectos en la secuencia</h2><a class="enlace" href="trabajo.html">Abrir el bin completo</a></div>
    <div class="bin">{bin_filas}</div>
  </section>
  <section class="envoltura bloque marcadores-bloque">
    <div class="bloque-cab"><h2>Marcadores</h2><p class="bloque-nota">Lo que hago, en el orden en que suele llegar.</p></div>
    <ol class="marcadores">{marcadores}</ol>
  </section>
</main>
{pie()}"""
    return C.documento(f"{D.NOMBRE} · Corte", D.BIO_CORTA, FUENTES, cuerpo, clase="pg-inicio")


def pagina_proyecto(p):
    clips, total = C.clips()
    c = next(x for x in clips if x["slug"] == p["slug"])
    sig = D.siguiente(p["slug"])
    hice = "".join(f"<li>{e(x)}</li>" for x in p["hice"])
    dec = "".join(f'<div class="decision"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in p["decisiones"])
    cifras = "".join(f'<div class="cifra"><b>{e(n)}</b><span>{e(t)}</span></div>' for n, t in p["cifras"])
    galeria = "".join(
        f'<figure class="toma"><img src="assets/{img}" alt="{e(alt)}" loading="lazy"><figcaption class="mono">{e(alt)}</figcaption></figure>'
        for img, alt in p["imagenes"][1:])
    nota = f'<p class="nota mono">{e(p["nota"])}</p>' if p.get("nota") else ""
    reel = ""
    if p["slug"] == "edicion":
        reel = (f'<a class="boton" href="{e(D.VIMEO)}" target="_blank" rel="noopener">Ver reel</a>' if D.VIMEO
                else '<p class="reel-pendiente mono">Reel 2026 · en preparación</p>')
    cuerpo = f"""{cabecera()}
<main>
  <div class="envoltura">{linea_tiempo(activo=p["slug"], compacta=True)}</div>
  <article class="envoltura proyecto">
    <header class="proyecto-cab">
      <p class="eyebrow mono"><a href="trabajo.html">Bin</a> / <span class="chip c-{p['color']}">{e(p['tipo'])}</span></p>
      <h1>{e(p['titulo'])}</h1>
      <p class="proyecto-sub">{e(p['subtitulo'])}</p>
    </header>
    <div class="proyecto-grid">
      {monitor(p['imagenes'][0][0], p['imagenes'][0][1], 'V1 · ' + p['titulo'], c['tc_in'], 'monitor-grande')}
      <dl class="info">
        <div><dt>Etiqueta</dt><dd><span class="muestra c-{p['color']}"></span>{COLORES[p['color']]}</dd></div>
        <div><dt>Año</dt><dd>{e(p['ano'])}</dd></div>
        <div><dt>Rol</dt><dd>{e(p['rol'])}</dd></div>
        <div><dt>Herramientas</dt><dd>{e(' · '.join(p['stack']))}</dd></div>
        <div><dt>Entrada</dt><dd class="mono">{c['tc_in']}</dd></div>
        <div><dt>Salida</dt><dd class="mono">{c['tc_out']}</dd></div>
        {reel}
      </dl>
    </div>
    <p class="proyecto-resumen">{e(p['resumen'])}</p>
    <div class="cifras">{cifras}</div>
    <section class="seccion-texto">
      <h2>El encargo</h2>
      <p>{e(p['brief'])}</p>
    </section>
    <section class="seccion-texto">
      <h2>Lo que hice</h2>
      <ul class="lista">{hice}</ul>
    </section>
    <section class="decisiones-bloque">
      <h2>Decisiones de montaje</h2>
      <div class="decisiones">{dec}</div>
    </section>
    {f'<section class="galeria">{galeria}</section>' if galeria else ''}
    {nota}
  </article>
  <a class="envoltura siguiente" href="{sig['slug']}.html">
    <span class="mono">Siguiente clip</span>
    <span class="siguiente-t">{e(sig['titulo'])}</span>
    <span class="chip c-{sig['color']}">{e(sig['tipo'])}</span>
  </a>
</main>
{pie()}"""
    return C.documento(f"{p['titulo']} · {D.NOMBRE}", p["resumen"], FUENTES, cuerpo, clase="pg-proyecto")


def trabajo():
    clips, total = C.clips()
    filas = "".join(
        f'<tr><td><a href="{c["slug"]}.html" class="t-nombre"><img src="assets/{c["img"]}" alt="" loading="lazy">'
        f'<span><b>{e(c["titulo"])}</b><span>{e(D.proyecto(c["slug"])["subtitulo"])}</span></span></a></td>'
        f'<td><span class="muestra c-{c["color"]}"></span>{COLORES[c["color"]]}</td><td>{e(c["tipo"])}</td>'
        f'<td>{e(D.proyecto(c["slug"])["ano"])}</td><td class="mono">{c["tc_in"]}</td><td class="mono">{c["tc_out"]}</td>'
        f'<td class="mono">{c["dur"]}</td></tr>' for c in clips)
    iconos = "".join(
        f'<a class="icono" href="{c["slug"]}.html"><span class="icono-img"><img src="assets/{c["img"]}" alt="" loading="lazy">'
        f'<span class="mono">{c["dur"]}</span></span><span class="icono-t"><span class="muestra c-{c["color"]}"></span>{e(c["titulo"])}</span></a>'
        for c in clips)
    cuerpo = f"""{cabecera('trabajo.html')}
<main class="envoltura">
  <header class="pagina-cab">
    <p class="eyebrow mono">Proyecto: portafolio_2026 · {len(clips)} elementos</p>
    <h1>Trabajo</h1>
    <p class="pagina-intro">Video, web y plataformas. Cada proyecto aparece aquí como un clip del bin, con su duración en la secuencia.</p>
  </header>
  <div class="bin-panel" data-bin>
    <div class="bin-herr">
      <span class="mono">Bin · Proyectos</span>
      <div class="vista" role="group" aria-label="Vista del bin">
        <button type="button" id="vista-lista" data-vista="lista" aria-pressed="true">Lista</button>
        <button type="button" id="vista-iconos" data-vista="iconos" aria-pressed="false">Iconos</button>
      </div>
    </div>
    <div class="bin-lista" data-panel="lista">
      <table>
        <thead><tr><th>Nombre</th><th>Etiqueta</th><th>Tipo</th><th>Año</th><th>Entrada</th><th>Salida</th><th>Duración</th></tr></thead>
        <tbody>{filas}</tbody>
      </table>
    </div>
    <div class="bin-iconos" data-panel="iconos" hidden>{iconos}</div>
  </div>
</main>
{pie()}"""
    return C.documento(f"Trabajo · {D.NOMBRE}", "Proyectos de video, web y plataformas.", FUENTES, cuerpo, clase="pg-trabajo")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    herr = "".join(
        f'<div class="herr"><h3 class="mono">{e(k)}</h3><ul>{"".join(f"<li>{e(i)}</li>" for i in v)}</ul></div>'
        for k, v in D.HERRAMIENTAS.items())
    cuerpo = f"""{cabecera('sobre.html')}
<main class="envoltura">
  <div class="sobre">
    {monitor('retrato.jpg', 'Retrato de ' + D.NOMBRE, 'Fuente · Retrato', '00:00:00:00', 'monitor-retrato')}
    <div class="sobre-texto">
      <p class="eyebrow mono">Notas de la secuencia</p>
      <h1>{e(D.NOMBRE)}</h1>
      <p class="sobre-rol">{e(D.ROL)} en {e(D.EMPRESA)}</p>
      {bio}
      <dl class="info info-corta">
        <div><dt>Base</dt><dd>{e(D.UBICACION)}</dd></div>
        <div><dt>Idiomas</dt><dd>{e(' · '.join(D.IDIOMAS))}</dd></div>
        <div><dt>Experiencia</dt><dd>{e(D.ANOS)} años</dd></div>
      </dl>
    </div>
  </div>
  <section class="bloque">
    <div class="bloque-cab"><h2>Herramientas</h2></div>
    <div class="herrs">{herr}</div>
  </section>
</main>
{pie()}"""
    return C.documento(f"Sobre mí · {D.NOMBRE}", D.BIO_CORTA, FUENTES, cuerpo, clase="pg-sobre")


def contacto():
    links = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in C.contacto_links())
    cuerpo = f"""{cabecera('contacto.html')}
<main class="envoltura">
  <section class="contacto">
    <p class="eyebrow mono">Exportar · Enviar</p>
    <h1>Hablemos de tu próximo corte.</h1>
    <p class="pagina-intro">Campañas, piezas para redes, una web que tu equipo pueda actualizar o una herramienta para tu evento. Respondo en español o en inglés.</p>
    <div class="correo">
      <span class="correo-t" id="correo">{e(D.CORREO)}</span>
      <button type="button" class="boton" data-copiar="correo">Copiar correo</button>
      <span class="copiado mono" data-copiado role="status"></span>
    </div>
    <ul class="links">{links}</ul>
    <dl class="info info-corta">
      <div><dt>Base</dt><dd>{e(D.UBICACION)}</dd></div>
      <div><dt>Idiomas</dt><dd>{e(' · '.join(D.IDIOMAS))}</dd></div>
      <div><dt>Formatos</dt><dd>16:9 · 9:16 · 1:1</dd></div>
    </dl>
  </section>
</main>
{pie()}"""
    return C.documento(f"Contacto · {D.NOMBRE}", "Escríbeme para tu próximo proyecto.", FUENTES, cuerpo, clase="pg-contacto")


def paginas():
    out = {"index.html": inicio(), "trabajo.html": trabajo(), "sobre.html": sobre(), "contacto.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = pagina_proyecto(p)
    return out
