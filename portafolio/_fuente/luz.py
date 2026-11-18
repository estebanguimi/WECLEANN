# -*- coding: utf-8 -*-
"""Línea A · SPOTLIGHT (LUZ) — la identidad nace de tu fotografía de conciertos.

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
    items = [("index.html", "Home"), ("work.html", "Work"), ("about.html", "About"), ("cv.html", "CV"), ("contact.html", "Contact")]
    links = "".join(
        f'<a href="{h}" class="nav-l{" es-activa" if h == activa else ""}" data-cursor="ir"><span>{t}</span></a>' for h, t in items)
    return f"""<header class="cab" data-cab>
  <a href="index.html" class="cab-marca" aria-label="{e(D.NOMBRE)}, home">{MONOGRAMA}<span class="cab-nombre">Esteban <i>Guillen</i></span></a>
  <nav class="cab-nav" aria-label="Main">{links}</nav>
  <span class="cab-reloj mono" data-reloj>Miami —:—</span>
</header>"""


def pie():
    return f"""<footer class="pie" data-pie>
  <div class="pie-luz" aria-hidden="true"></div>
  <p class="mono pie-eti">Hiring for a team, a campaign or a show?</p>
  <a class="pie-grande" href="contact.html" data-cursor="escribir"><span>Let's talk</span></a>
  <div class="pie-fila">
    <button type="button" class="pie-correo" data-copiar="{e(D.CORREO)}">{e(D.CORREO)} <span class="mono" data-copiado>Copy</span></button>
    <nav class="pie-redes" aria-label="Links">
      <a href="cv.html">Résumé</a>
      <a href="{e(D.CV_PDF)}" download>CV (PDF)</a>
      <a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a>
    </nav>
  </div>
  <div class="pie-legal mono"><span>© 2026 {e(D.NOMBRE)}</span><span>{e(D.CIUDAD)} · {e(D.PUESTO)}</span></div>
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
    for slug, n in [("mercyme", "19.jpg"), ("bobby-charles", "01.jpg"), ("nahomi-martinez", "03.jpg"), ("crowder", "17.jpg"),
                    ("qatar-2022", "04.jpg"), ("gallucci", "00.jpg"), ("luis-benites", "05.jpg"), ("physo", "02.jpg"),
                    ("for-king-country", "06.jpg"), ("matchdays", "02.jpg"), ("zena-coffee", "00.jpg"), ("valorant", "02.jpg")]:
        w, h = C.medida(slug, n)
        p = D.por_slug(slug)
        vivo.append(f'<a class="vivo-item{" vivo-v" if h > w else ""}" href="{slug}.html" data-cursor="ver">'
                    f'<span class="vivo-marco"><img src="{C.img(slug, n)}" alt="{e(p["titulo"])}" loading="lazy"></span>'
                    f'<span class="vivo-pie mono">{e(p["corto"])} · {e(D.CATEGORIAS[p["cat"]])}</span></a>')
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
    <img class="hero-respaldo" src="{hero_img}" alt="MercyMe on stage with beams of light, photographed by {e(D.NOMBRE)}">
    <div class="hero-sup">
      <p class="mono">Design · Video · Live photography</p>
      <p class="mono hero-dato"><b>1.3M+</b> campaign views</p>
    </div>
    <h1 class="hero-t" data-partir><span class="l1">Esteban</span><span class="l2"><i>Guillen</i></span></h1>
    <div class="hero-inf">
      <p class="hero-bio">{e(D.BIO)}</p>
      <p class="mono hero-guia">Move the cursor: it's the light</p>
    </div>
  </section>

  <section class="manifiesto envoltura">
    <p class="mono eti">Approach</p>
    <p class="manif-t" data-iluminar>I work where things move fast. A campaign that goes out tomorrow, a concert in the dark, a match that kicks off at three, a brand that posts every day. My job is to be ready, and to make the image tell the story without explanation.</p>
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">Setlist · Selected work</p><a class="enlace" href="work.html" data-cursor="ir">See all 12 projects</a></div>
    {setlist(sel)}
  </section>

  <section class="vivo" data-horizontal>
    <div class="vivo-pin">
      <div class="vivo-cab envoltura"><p class="mono eti">Six disciplines</p><h2>Video, photo, sports,<br><i>brand, web and gaming.</i></h2></div>
      <div class="vivo-pista" data-pista>{"".join(vivo)}</div>
      <div class="vivo-barra" aria-hidden="true"><span data-barra></span></div>
    </div>
  </section>

  <section class="envoltura bloque">
    <div class="cifras">
      <div class="cifra"><b data-contar="900">900</b><span>K+ views<br>Sam Gallucci & NH Senate</span></div>
      <div class="cifra"><b data-contar="436">436</b><span>K+ views<br>Bobby Charles for Maine</span></div>
      <div class="cifra"><b data-contar="60">60</b><span>concert<br>photographs</span></div>
      <div class="cifra"><b data-contar="53">53</b><span>football<br>posters</span></div>
    </div>
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">Campaign video</p><p class="bloque-nota">Editing, motion and social cut-downs.</p></div>
    <div class="videos">{"".join(videos)}</div>
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">Experience · since 2018</p><a class="enlace" href="cv.html" data-cursor="ir">View full résumé</a></div>
    {C.recorrido()}
  </section>

  <section class="envoltura bloque">
    <div class="bloque-cab"><p class="mono eti">What I do</p></div>
    <ul class="servicios">{servicios}</ul>
  </section>
</main>"""
    return C.documento(f"{D.NOMBRE} · Spotlight", D.BIO, FUENTES, envoltura(cuerpo, "index.html"), clase="pg-inicio")


def trabajo():
    filtros = [("todo", "All", len(D.PROYECTOS))] + [
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
    <p class="mono eti">Full setlist · {len(D.PROYECTOS)} projects</p>
    <h1 data-partir>Everything that<br><i>happened on stage.</i></h1>
  </section>
  <div class="filtros" role="group" aria-label="Filter by discipline">{botones}</div>
  <div class="mosaico" data-mosaico>{"".join(tarjetas)}</div>
</main>"""
    return C.documento(f"Work · {D.NOMBRE}", "Video, live photography and design projects.", FUENTES,
                       envoltura(cuerpo, "work.html"), clase="pg-trabajo")


def proyecto(p):
    sig = D.siguiente(p["slug"])
    datos = "".join(f'<div class="dato"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in p["datos"])
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    video = C.bloque_video(p)
    cuerpo = f"""<main>
  <section class="p-hero" data-p-hero>
    <div class="p-hero-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"></div>
    <div class="p-hero-txt envoltura">
      <p class="mono eti"><a href="work.html">Setlist</a> / {e(D.CATEGORIAS[p['cat']])}</p>
      <h1 data-partir>{e(p['titulo'])}</h1>
    </div>
  </section>
  <section class="envoltura p-intro">
    <dl class="p-meta">
      <div><dt class="mono">Client</dt><dd>{e(p['cliente'])}</dd></div>
      <div><dt class="mono">My role</dt><dd>{e(D.ROLES[p['cat']])}</dd></div>
      <div><dt class="mono">Discipline</dt><dd>{e(D.CATEGORIAS[p['cat']])}</dd></div>
      <div><dt class="mono">Year</dt><dd>{e(p['ano'])}</dd></div>
      <div><dt class="mono">Tools</dt><dd>{e(', '.join(p['herr']))}</dd></div>
    </dl>
    <div class="p-texto">
      <p class="p-resumen" data-iluminar>{e(p['resumen'])}</p>
      {textos}
    </div>
  </section>
  {f'<section class="envoltura">{video}</section>' if video else ''}
  <section class="envoltura"><div class="datos">{datos}</div></section>
  <section class="envoltura p-galeria">{C.galeria(p['slug'])}</section>
  <a class="siguiente" href="{sig['slug']}.html" data-cursor="siguiente">
    <span class="sig-img"><img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></span>
    <span class="mono">Next on the setlist</span>
    <span class="sig-t">{e(sig['titulo'])}</span>
  </a>
</main>
<div class="visor" data-visor hidden>
  <button type="button" class="visor-cerrar mono" data-visor-cerrar>Close</button>
  <button type="button" class="visor-ant" data-visor-ant aria-label="Previous">←</button>
  <img alt="" data-visor-img>
  <button type="button" class="visor-sig" data-visor-sig aria-label="Next">→</button>
  <span class="visor-n mono" data-visor-n></span>
</div>"""
    return C.documento(f"{p['corto']} · {D.NOMBRE}", p["resumen"], FUENTES, envoltura(cuerpo), clase="pg-proyecto")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    exp = "".join(f'<li><b>{e(x["puesto"])}</b><span>{e(x["empresa"])}</span><span class="mono">{e(x["fechas"])}</span></li>' for x in D.EXPERIENCIA)
    herr = "".join(f"<li>{e(h)}</li>" for h in D.HERRAMIENTAS)
    cuerpo = f"""<main class="envoltura">
  <section class="sobre">
    <figure class="sobre-foto" data-foco-css>
      <img src="{C.retrato()}" alt="Portrait of {e(D.NOMBRE)}">
      <figcaption class="mono">{e(D.CIUDAD)} · From {e(D.ORIGEN)}</figcaption>
    </figure>
    <div class="sobre-txt">
      <p class="mono eti">About</p>
      <h1 data-partir>Design, camera<br><i>and cut.</i></h1>
      {bio}
      <p class="mono disponible"><span class="punto" aria-hidden="true"></span>{e(D.DISPONIBLE)}</p>
      <p class="sobre-acc"><a class="boton-luz" href="cv.html" data-cursor="ir">View résumé</a><a class="boton-luz fantasma" href="{e(D.CV_PDF)}" download>Download PDF</a></p>
    </div>
  </section>
  <section class="bloque sobre-dos">
    <div><p class="mono eti">Experience</p><ul class="exp">{exp}</ul></div>
    <div><p class="mono eti">Tools</p><ul class="herr">{herr}</ul></div>
  </section>
</main>"""
    return C.documento(f"About · {D.NOMBRE}", D.BIO, FUENTES, envoltura(cuerpo, "about.html"), clase="pg-sobre")


def contacto():
    cuerpo = f"""<main class="envoltura">
  <section class="contacto">
    <p class="mono eti">Contact · {e(D.DISPONIBLE)}</p>
    <h1 data-partir>Light up<br><i>the next one.</i></h1>
    <button type="button" class="correo-grande" data-copiar="{e(D.CORREO)}" data-cursor="copiar">{e(D.CORREO)}</button>
    <p class="mono" data-copiado-g role="status">Click to copy the email</p>
    <div class="contacto-cols">
      <div><p class="mono eti">Profile</p><a href="cv.html">Résumé</a><a href="{e(D.CV_PDF)}" download>CV (PDF)</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram · {e(D.INSTAGRAM_T)}</a></div>
      <div><p class="mono eti">Location</p><p>{e(D.CIUDAD)}<br>From: {e(D.ORIGEN)}</p></div>
      <div><p class="mono eti">Languages</p><p>{"<br>".join(e(a + " · " + b) for a, b in D.IDIOMAS)}</p></div>
    </div>
  </section>
</main>"""
    return C.documento(f"Contact · {D.NOMBRE}", "Get in touch about a role or a project.", FUENTES,
                       envoltura(cuerpo, "contact.html"), clase="pg-contacto")


def cv():
    cuerpo = f"""<main class="envoltura">
  <section class="pag-cab">
    <p class="mono eti">Résumé · {e(D.NOMBRE)}</p>
    <h1 data-partir>Eight years<br><i>of craft.</i></h1>
  </section>
  {C.cv_secciones("mono eti")}
</main>"""
    return C.documento(f"Résumé · {D.NOMBRE}", D.CV_RESUMEN, FUENTES, envoltura(cuerpo, "cv.html"), clase="pg-cv")


def paginas():
    out = {"index.html": inicio(), "work.html": trabajo(), "about.html": sobre(), "cv.html": cv(), "contact.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
