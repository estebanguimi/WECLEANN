# -*- coding: utf-8 -*-
"""Línea A · LUZ — la identidad nace de tu fotografía de conciertos.

Negro de escenario, luz ámbar de tungsteno y un foco que el visitante mueve con el cursor.
"""
import comun as C
import datos as D
from comun import e

FUENTES = ("family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600"
           "&family=Manrope:wght@300;400;500;600;700&family=DM+Mono:wght@400;500")

MONOGRAMA = """<svg class="mono-eg" viewBox="0 0 64 64" aria-hidden="true">
<path d="M32 2 L40 12 H24 Z" fill="currentColor"/>
<circle cx="32" cy="38" r="23" fill="none" stroke="currentColor" stroke-width="1.6"/>
<text x="32" y="47" text-anchor="middle" font-family="Cormorant Garamond, serif" font-style="italic" font-weight="500" font-size="27" fill="currentColor">eg</text>
</svg>"""


def nav(activa=""):
    items = [("index.html", "Inicio"), ("trabajo.html", "Trabajo"), ("sobre.html", "Sobre mí"), ("contacto.html", "Contacto")]
    links = "".join(
        f'<a href="{h}" class="nav-l{" es-activa" if h == activa else ""}" data-cursor="ir"><span>{t}</span></a>' for h, t in items)
    return f"""<header class="cab" data-cab>
  <a href="index.html" class="cab-marca" aria-label="{e(D.NOMBRE)}, inicio">{MONOGRAMA}<span class="cab-nombre">Esteban <i>Guillen</i></span></a>
  <nav class="cab-nav" aria-label="Principal">{links}</nav>
  <span class="cab-reloj mono" data-reloj>Miami —:—</span>
</header>"""


def pie():
    return f"""<footer class="pie" data-pie>
  <div class="pie-luz" aria-hidden="true"></div>
  <p class="mono pie-eti">¿Tienes un show, una campaña o una marca?</p>
  <a class="pie-grande" href="contacto.html" data-cursor="escribir"><span>Hablemos</span></a>
  <div class="pie-fila">
    <button type="button" class="pie-correo" data-copiar="{e(D.CORREO)}">{e(D.CORREO)} <span class="mono" data-copiado>Copiar</span></button>
    <nav class="pie-redes" aria-label="Redes">
      <a href="{e(D.BEHANCE)}" target="_blank" rel="noopener">Behance</a>
      <a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a>
    </nav>
  </div>
  <div class="pie-legal mono"><span>© 2026 {e(D.NOMBRE)}</span><span>{e(D.CIUDAD)} · Desde {D.DESDE}</span></div>
</footer>"""


def envoltura(cuerpo, activa=""):
    return f"""<div class="cortina" data-cortina aria-hidden="true"><span class="cortina-linea"></span><span class="cortina-t" data-cortina-t></span></div>
<div class="cursor" data-cursor-el aria-hidden="true"><span data-cursor-t></span></div>
<div class="grano" aria-hidden="true"></div>
{nav(activa)}
<div data-lenis-wrap>
{cuerpo}
{pie()}
</div>"""


def setlist(proyectos, numerar=True):
    filas = []
    for i, p in enumerate(proyectos):
        filas.append(
            f'<a class="set-fila" href="{p["slug"]}.html" data-prev="{C.img(p["slug"], p["portada"])}" data-cursor="ver">'
            f'<span class="set-n mono">{i + 1:02d}</span>'
            f'<span class="set-t">{e(p["corto"])}</span>'
            f'<span class="set-c">{e(D.CATEGORIAS[p["cat"]])}</span>'
            f'<span class="set-cifra mono">{e(p["cifra"])} {e(p["cifra_t"])}</span>'
            f'<span class="set-a mono">{e(p["ano"])}</span></a>')
    return f'<div class="setlist" data-setlist>{"".join(filas)}<div class="set-prev" data-set-prev aria-hidden="true"><img alt=""></div></div>'


def inicio():
    hero_img = C.img("mercyme", "07.jpg")
    sel = [D.por_slug(s) for s in ["gallucci", "mercyme", "nahomi-martinez", "bobby-charles", "for-king-country", "qatar-2022", "crowder", "luis-benites"]]
    vivo = []
    for slug, n in [("mercyme", "19.jpg"), ("crowder", "01.jpg"), ("for-king-country", "06.jpg"), ("mercyme", "21.jpg"),
                    ("crowder", "17.jpg"), ("for-king-country", "05.jpg"), ("mercyme", "03.jpg"), ("crowder", "14.jpg"),
                    ("for-king-country", "01.jpg"), ("mercyme", "08.jpg")]:
        w, h = C.medida(slug, n)
        p = D.por_slug(slug)
        vivo.append(f'<a class="vivo-item{" vivo-v" if h > w else ""}" href="{slug}.html" data-cursor="ver">'
                    f'<span class="vivo-marco"><img src="{C.img(slug, n)}" alt="{e(p["corto"])} en vivo" loading="lazy"></span>'
                    f'<span class="vivo-pie mono">{e(p["corto"])} · {n[:2]}</span></a>')
    videos = []
    for s in ["gallucci", "bobby-charles"]:
        p = D.por_slug(s)
        videos.append(f"""<a class="video-card" href="{s}.html" data-cursor="ver">
  <span class="video-img"><img src="{C.img(s, '02.jpg' if s == 'bobby-charles' else p['portada'])}" alt="{e(p['titulo'])}" loading="lazy"></span>
  <span class="video-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span>
  <span class="video-info"><b class="video-cifra">{e(p['cifra'])}</b><span class="mono">{e(p['cifra_t'])}</span><span class="video-t">{e(p['titulo'])}</span></span>
</a>""")
    servicios = "".join(
        f'<li class="serv"><span class="serv-n mono">{i + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
        for i, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""<main>
  <section class="hero" data-hero>
    <canvas class="hero-gl" data-foco data-src="{hero_img}" aria-hidden="true"></canvas>
    <img class="hero-respaldo" src="{hero_img}" alt="Escenario de MercyMe con haces de luz, fotografía de {e(D.NOMBRE)}">
    <div class="hero-sup">
      <p class="mono">Diseño · Video · Fotografía en vivo</p>
      <p class="mono hero-dato"><b>1,3M+</b> vistas en campañas</p>
    </div>
    <h1 class="hero-t" data-partir><span class="l1">Esteban</span><span class="l2"><i>Guillen</i></span></h1>
    <div class="hero-inf">
      <p class="hero-bio">{e(D.BIO)}</p>
      <p class="mono hero-guia">Mueve el cursor: es la luz</p>
    </div>
  </section>

  <section class="manifiesto envoltura">
    <p class="mono eti">Manifiesto</p>
    <p class="manif-t" data-iluminar>Trabajo donde la luz cambia rápido. Un escenario a oscuras, una campaña que sale mañana, un partido que empieza a las tres. Mi trabajo es estar listo cuando pasa, y que la imagen lo cuente sin explicación.</p>
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">Setlist · Trabajo seleccionado</p><a class="enlace" href="trabajo.html" data-cursor="ir">Ver los 12 proyectos</a></div>
    {setlist(sel)}
  </section>

  <section class="vivo" data-horizontal>
    <div class="vivo-pin">
      <div class="vivo-cab envoltura"><p class="mono eti">En vivo</p><h2>Tres conciertos,<br><i>sesenta fotografías.</i></h2></div>
      <div class="vivo-pista" data-pista>{"".join(vivo)}</div>
      <div class="vivo-barra" aria-hidden="true"><span data-barra></span></div>
    </div>
  </section>

  <section class="envoltura bloque">
    <div class="cifras">
      <div class="cifra"><b data-contar="900">900</b><span>K+ vistas<br>Sam Gallucci & NH Senate</span></div>
      <div class="cifra"><b data-contar="436">436</b><span>K+ vistas<br>Bobby Charles for Maine</span></div>
      <div class="cifra"><b data-contar="60">60</b><span>fotografías<br>de conciertos</span></div>
      <div class="cifra"><b data-contar="53">53</b><span>afiches<br>de fútbol</span></div>
    </div>
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">Video para campañas</p><p class="bloque-nota">Montaje, motion y versiones para redes.</p></div>
    <div class="videos">{"".join(videos)}</div>
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">Qué hago</p></div>
    <ul class="servicios">{servicios}</ul>
  </section>
</main>"""
    return C.documento(f"{D.NOMBRE} · Luz", D.BIO, FUENTES, envoltura(cuerpo, "index.html"), clase="pg-inicio")


def trabajo():
    filtros = [("todo", "Todo", len(D.PROYECTOS))] + [
        (k, v, sum(1 for p in D.PROYECTOS if p["cat"] == k)) for k, v in D.CATEGORIAS.items()]
    botones = "".join(
        f'<button type="button" class="filtro{" activo" if k == "todo" else ""}" data-filtro="{k}" aria-pressed="{"true" if k == "todo" else "false"}">'
        f'{e(t)} <sup class="mono">{n}</sup></button>' for k, t, n in filtros)
    tarjetas = []
    for i, p in enumerate(D.PROYECTOS):
        w, h = C.medida(p["slug"], p["portada"])
        forma = "t-v" if h > w * 1.1 else ("t-a" if w > h * 1.5 else "t-c")
        tarjetas.append(
            f'<a class="tarjeta {forma}" href="{p["slug"]}.html" data-cat="{p["cat"]}" data-cursor="ver">'
            f'<span class="t-img"><img src="{C.img(p["slug"], p["portada"])}" alt="{e(p["titulo"])}" loading="lazy"></span>'
            f'<span class="t-pie"><span class="mono">{i + 1:02d}</span><b>{e(p["corto"])}</b><span class="t-cat">{e(D.CATEGORIAS[p["cat"]])} · {e(p["ano"])}</span></span></a>')
    cuerpo = f"""<main class="envoltura">
  <section class="pag-cab">
    <p class="mono eti">Setlist completo · {len(D.PROYECTOS)} proyectos</p>
    <h1 data-partir>Todo lo que<br><i>pasó en escena.</i></h1>
  </section>
  <div class="filtros" role="group" aria-label="Filtrar por disciplina">{botones}</div>
  <div class="mosaico" data-mosaico>{"".join(tarjetas)}</div>
</main>"""
    return C.documento(f"Trabajo · {D.NOMBRE}", "Proyectos de video, fotografía en vivo y diseño.", FUENTES,
                       envoltura(cuerpo, "trabajo.html"), clase="pg-trabajo")


def proyecto(p):
    sig = D.siguiente(p["slug"])
    datos = "".join(f'<div class="dato"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in p["datos"])
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    video = ""
    if p.get("video"):
        video = (f'<a class="boton-luz" href="{e(D.url_behance(p))}" target="_blank" rel="noopener" data-cursor="ver">'
                 f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>Ver los videos en Behance</a>')
    cuerpo = f"""<main>
  <section class="p-hero" data-p-hero>
    <div class="p-hero-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"></div>
    <div class="p-hero-txt envoltura">
      <p class="mono eti"><a href="trabajo.html">Setlist</a> / {e(D.CATEGORIAS[p['cat']])}</p>
      <h1 data-partir>{e(p['titulo'])}</h1>
    </div>
  </section>
  <section class="envoltura p-intro">
    <dl class="p-meta">
      <div><dt class="mono">Disciplina</dt><dd>{e(D.CATEGORIAS[p['cat']])}</dd></div>
      <div><dt class="mono">Año</dt><dd>{e(p['ano'])}</dd></div>
      <div><dt class="mono">Herramientas</dt><dd>{e(', '.join(p['herr']))}</dd></div>
      <div><dt class="mono">Behance</dt><dd><a href="{e(D.url_behance(p))}" target="_blank" rel="noopener">Ver proyecto original</a></dd></div>
    </dl>
    <div class="p-texto">
      <p class="p-resumen" data-iluminar>{e(p['resumen'])}</p>
      {textos}
      {video}
    </div>
  </section>
  <section class="envoltura"><div class="datos">{datos}</div></section>
  <section class="envoltura p-galeria">{C.galeria(p['slug'])}</section>
  <a class="siguiente" href="{sig['slug']}.html" data-cursor="siguiente">
    <span class="sig-img"><img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></span>
    <span class="mono">Siguiente en el setlist</span>
    <span class="sig-t">{e(sig['titulo'])}</span>
  </a>
</main>
<div class="visor" data-visor hidden>
  <button type="button" class="visor-cerrar mono" data-visor-cerrar>Cerrar</button>
  <button type="button" class="visor-ant" data-visor-ant aria-label="Anterior">←</button>
  <img alt="" data-visor-img>
  <button type="button" class="visor-sig" data-visor-sig aria-label="Siguiente">→</button>
  <span class="visor-n mono" data-visor-n></span>
</div>"""
    return C.documento(f"{p['corto']} · {D.NOMBRE}", p["resumen"], FUENTES, envoltura(cuerpo), clase="pg-proyecto")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    exp = "".join(f'<li><b>{e(a)}</b><span>{e(b)}</span><span class="mono">{e(c)}</span></li>' for a, b, c in D.EXPERIENCIA)
    herr = "".join(f"<li>{e(h)}</li>" for h in D.HERRAMIENTAS)
    cuerpo = f"""<main class="envoltura">
  <section class="sobre">
    <figure class="sobre-foto" data-foco-css>
      <img src="{C.retrato()}" alt="Retrato de {e(D.NOMBRE)}">
      <figcaption class="mono">{e(D.CIUDAD)} · Desde {D.DESDE} en Behance</figcaption>
    </figure>
    <div class="sobre-txt">
      <p class="mono eti">Sobre mí</p>
      <h1 data-partir>Diseño, cámara<br><i>y corte.</i></h1>
      {bio}
      <p class="mono disponible"><span class="punto" aria-hidden="true"></span>{e(D.DISPONIBLE)}</p>
    </div>
  </section>
  <section class="bloque sobre-dos">
    <div><p class="mono eti">Recorrido</p><ul class="exp">{exp}</ul></div>
    <div><p class="mono eti">Herramientas</p><ul class="herr">{herr}</ul></div>
  </section>
</main>"""
    return C.documento(f"Sobre mí · {D.NOMBRE}", D.BIO, FUENTES, envoltura(cuerpo, "sobre.html"), clase="pg-sobre")


def contacto():
    cuerpo = f"""<main class="envoltura">
  <section class="contacto">
    <p class="mono eti">Contacto · {e(D.DISPONIBLE)}</p>
    <h1 data-partir>Enciende<br><i>la próxima.</i></h1>
    <button type="button" class="correo-grande" data-copiar="{e(D.CORREO)}" data-cursor="copiar">{e(D.CORREO)}</button>
    <p class="mono" data-copiado-g role="status">Haz clic para copiar el correo</p>
    <div class="contacto-cols">
      <div><p class="mono eti">Redes</p><a href="{e(D.BEHANCE)}" target="_blank" rel="noopener">Behance</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram · {e(D.INSTAGRAM_T)}</a></div>
      <div><p class="mono eti">Base</p><p>{e(D.CIUDAD)}<br>Origen: {e(D.ORIGEN)}</p></div>
      <div><p class="mono eti">Idiomas</p><p>Español<br>Inglés</p></div>
    </div>
  </section>
</main>"""
    return C.documento(f"Contacto · {D.NOMBRE}", "Escríbeme para tu próximo proyecto.", FUENTES,
                       envoltura(cuerpo, "contacto.html"), clase="pg-contacto")


def paginas():
    out = {"index.html": inicio(), "trabajo.html": trabajo(), "sobre.html": sobre(), "contacto.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
