# -*- coding: utf-8 -*-
"""Línea B · MATCHDAY — la identidad nace de tus afiches de fútbol.

Rojo de camiseta, papel de afiche, tipografía condensada gigante, collage y energía de día de partido.
"""
import comun as C
import datos as D
from comun import e

FUENTES = "family=Anton&family=Archivo:ital,wdth,wght@0,62..125,300..900;1,62..125,300..900&family=Space+Mono:wght@400;700"

ESCUDO = """<svg class="escudo" viewBox="0 0 80 92" aria-hidden="true">
<path d="M40 2 L76 12 V44 C76 68 60 82 40 90 C20 82 4 68 4 44 V12 Z" fill="var(--rojo)"/>
<path d="M40 2 L76 12 V44 C76 68 60 82 40 90 C20 82 4 68 4 44 V12 Z" fill="none" stroke="var(--negro)" stroke-width="3"/>
<path d="M4 58 L76 26 V36 L4 68 Z" fill="var(--papel)"/>
<text x="40" y="48" text-anchor="middle" font-family="Anton, Impact, sans-serif" font-size="30" fill="var(--negro)" letter-spacing="1">EG</text>
<text x="40" y="80" text-anchor="middle" font-family="Archivo, sans-serif" font-weight="800" font-size="7" fill="var(--papel)" letter-spacing="1.5">MMXX</text>
</svg>"""

ESTRELLA = '<svg class="estrella" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1.5l3.1 7 7.6.6-5.8 5 1.8 7.4L12 17.6 5.3 21.5l1.8-7.4-5.8-5 7.6-.6z" fill="currentColor"/></svg>'


def iniciales(p):
    pal = [w for w in p["corto"].replace("&", " ").split() if w[0].isalnum()]
    return (pal[0][0] + (pal[1][0] if len(pal) > 1 else pal[0][1])).upper()


def nav(activa=""):
    items = [("index.html", "Inicio"), ("trabajo.html", "Trabajo"), ("sobre.html", "Perfil"), ("cv.html", "CV"), ("contacto.html", "Contacto")]
    links = "".join(f'<a href="{h}"{" class=\"activa\"" if h == activa else ""}>{t}</a>' for h, t in items)
    return f"""<header class="cab" data-cab>
  <a href="index.html" class="cab-marca" aria-label="{e(D.NOMBRE)}, inicio">{ESCUDO}<span class="cab-nombre"><small>Esteban</small>GUILLEN</span></a>
  <nav class="cab-nav" aria-label="Principal">{links}</nav>
  <a class="cab-cta" href="{e(D.CV_PDF)}" download>CV · PDF ↓</a>
</header>"""


def ticker():
    items = ["900K+ vistas · Sam Gallucci", "436K+ vistas · Bobby Charles", "53 afiches de fútbol", "60 fotos de conciertos",
             "Qatar 2022 · 37 piezas", "Harris Media Group", "Miami, FL", "8 años de oficio"]
    fila = "".join(f"<span>{e(t)}</span>{ESTRELLA}" for t in items)
    return f'<div class="ticker" aria-hidden="true"><div class="ticker-in" data-ticker>{fila}{fila}</div></div>'


def pie():
    return f"""<footer class="pie">
  <div class="pie-rasgado" aria-hidden="true"></div>
  <div class="pie-in">
    <p class="kicker">Mercado abierto · {e(D.DISPONIBLE)}</p>
    <a class="pie-grande" href="contacto.html" data-magnetico><span>¿Jugamos?</span></a>
    <div class="pie-fila">
      <button type="button" class="pie-correo" data-copiar="{e(D.CORREO)}"><span>{e(D.CORREO)}</span><b data-copiado>Copiar</b></button>
      <nav class="pie-redes" aria-label="Redes"><a href="cv.html">Currículum</a><a href="{e(D.CV_PDF)}" download>CV en PDF</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a></nav>
    </div>
    <div class="pie-legal"><span>© 2026 {e(D.NOMBRE)}</span><span>{e(D.CIUDAD)}</span><span>Hecho a mano, sin plantillas</span></div>
  </div>
</footer>"""


def envoltura(cuerpo, activa=""):
    return f"""<div class="barrido" data-barrido aria-hidden="true"><i></i><i></i><i></i><span data-barrido-t></span></div>
<div class="intro" data-intro aria-hidden="true"><span class="intro-t" data-intro-t>MATCHDAY</span><span class="intro-sub">Esteban Guillen · Temporada 2026</span></div>
<div class="semitono" aria-hidden="true"></div>
{nav(activa)}
{cuerpo}
{pie()}"""


def inicio():
    abanico = []
    for slug, n in [("mercyme", "05.jpg"), ("nahomi-martinez", "09.jpg"), ("bobby-charles", "01.jpg"), ("luis-benites", "05.jpg"), ("crowder", "01.jpg")]:
        abanico.append(f'<span class="carta"><img src="{C.img(slug, n)}" alt="{e(D.por_slug(slug)["titulo"])}"></span>')
    fixture = []
    for i, p in enumerate(D.PROYECTOS):
        fixture.append(
            f'<a class="partido" href="{p["slug"]}.html" data-prev="{C.img(p["slug"], p["portada"])}">'
            f'<span class="p-fecha">Fecha {i + 1:02d}</span>'
            f'<span class="p-local"><span class="p-esc">EG</span>Guillen</span>'
            f'<span class="p-vs">vs</span>'
            f'<span class="p-visita"><span class="p-esc p-esc-v">{iniciales(p)}</span>{e(p["corto"])}</span>'
            f'<span class="p-cat">{e(D.CATEGORIAS[p["cat"]])}</span>'
            f'<span class="p-res">{e(p["cifra"])}<small>{e(p["cifra_t"])}</small></span></a>')
    carrusel = []
    for slug in ["nahomi-martinez", "mercyme", "bobby-charles", "luis-benites", "crowder", "qatar-2022", "matchdays", "physo"]:
        for n, w, h in D.imagenes(slug)[:7]:
            if h >= w * 0.98:
                carrusel.append(f'<figure class="afiche"><img src="{C.img(slug, n)}" alt="{e(D.por_slug(slug)["titulo"])}" loading="lazy" draggable="false"></figure>')
    posiciones = [(50, 14), (20, 40), (80, 40), (32, 74), (68, 74)]
    jugadores = "".join(
        f'<button type="button" class="jugador" style="left:{x}%;top:{y}%" data-pos="{i}"><span class="j-n">{i + 1}</span><span class="j-t">{e(t)}</span></button>'
        for i, ((t, d), (x, y)) in enumerate(zip(D.SERVICIOS, posiciones)))
    detalles = "".join(
        f'<div class="pos-det{" activo" if i == 0 else ""}" data-det="{i}"><span class="pos-n">{i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>'
        for i, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""<main>
  <section class="hero" data-hero>
    <div class="hero-fondo" aria-hidden="true">
      <div class="fila-nombre" data-vel="1"><span>Esteban Guillen Esteban Guillen Esteban Guillen Esteban Guillen&nbsp;</span><span>Esteban Guillen Esteban Guillen Esteban Guillen Esteban Guillen&nbsp;</span></div>
      <div class="fila-nombre" data-vel="-1"><span>Diseño Video Foto Diseño Video Foto Diseño Video Foto&nbsp;</span><span>Diseño Video Foto Diseño Video Foto Diseño Video Foto&nbsp;</span></div>
      <div class="fila-nombre" data-vel="1"><span>Portafolio 2026 Portafolio 2026 Portafolio 2026&nbsp;</span><span>Portafolio 2026 Portafolio 2026 Portafolio 2026&nbsp;</span></div>
    </div>
    <div class="hero-in">
      <div class="hero-txt">
        <p class="kicker">Temporada 2026 · {e(D.CIUDAD)} · Origen {e(D.ORIGEN)}</p>
        <h1 class="hero-t"><span class="ht-a" data-golpe>Esteban</span><span class="ht-b" data-golpe><em>Guillen</em></span></h1>
        <p class="hero-bio">{e(D.BIO)}</p>
        <div class="hero-acc"><a class="boton" href="trabajo.html" data-magnetico>Ver la plantilla</a><a class="boton boton-l" href="contacto.html">Convocar</a></div>
      </div>
      <div class="abanico" data-abanico>{"".join(abanico)}</div>
    </div>
    <div class="hero-firma" aria-hidden="true">#20</div>
  </section>
  {ticker()}

  <section class="bloque envoltura">
    <div class="titulo-sec"><h2>Fixture</h2><p>Doce partidos jugados. Cada proyecto es un encuentro con su resultado.</p></div>
    <div class="fixture" data-fixture>{"".join(fixture)}<span class="fx-prev" data-fx-prev aria-hidden="true"><img alt=""></span></div>
  </section>

  <section class="marcador-sec">
    <div class="envoltura marcador">
      <div class="mc"><span class="mc-n" data-odo="900">900</span><span class="mc-u">K+</span><p>vistas · Sam Gallucci & NH Senate Republicans</p></div>
      <div class="mc"><span class="mc-n" data-odo="436">436</span><span class="mc-u">K+</span><p>vistas · Bobby Charles for Maine</p></div>
      <div class="mc"><span class="mc-n" data-odo="53">53</span><span class="mc-u"></span><p>afiches de fútbol peruano</p></div>
      <div class="mc"><span class="mc-n" data-odo="60">60</span><span class="mc-u"></span><p>fotos de conciertos en vivo</p></div>
    </div>
  </section>

  <section class="bloque carrusel-sec">
    <div class="envoltura titulo-sec"><h2>Piezas</h2><p>Campañas, conciertos, fútbol y marcas en una sola tira. Arrastra para recorrerla.</p></div>
    <div class="carrusel" data-carrusel><div class="carrusel-pista" data-pista>{"".join(carrusel)}</div></div>
    <div class="envoltura carrusel-pie"><span data-car-n>01</span> / {len(carrusel):02d}<span class="carrusel-ayuda">← Arrastra →</span></div>
  </section>

  <section class="bloque envoltura">
    <div class="titulo-sec"><h2>Trayectoria</h2><p>Ocho años de oficio, de Lima a Miami. <a class="subraya" href="cv.html">Ver currículum completo →</a></p></div>
    {C.recorrido()}
  </section>

  <section class="bloque envoltura alineacion-sec">
    <div class="titulo-sec"><h2>Servicios</h2><p>Lo que pongo en la cancha. Toca cada posición.</p></div>
    <div class="alineacion">
      <div class="cancha" data-cancha>
        <svg class="cancha-lineas" viewBox="0 0 100 130" preserveAspectRatio="none" aria-hidden="true">
          <rect x="2" y="2" width="96" height="126" fill="none"/><line x1="2" y1="65" x2="98" y2="65"/><circle cx="50" cy="65" r="11" fill="none"/>
          <rect x="25" y="2" width="50" height="20" fill="none"/><rect x="25" y="108" width="50" height="20" fill="none"/>
        </svg>
        {jugadores}
      </div>
      <div class="pos-dets">{detalles}</div>
    </div>
  </section>
</main>"""
    return C.documento(f"{D.NOMBRE} · Matchday", D.BIO, FUENTES, envoltura(cuerpo, "index.html"), clase="pg-inicio")


def trabajo():
    filtros = [("todo", "Todos", len(D.PROYECTOS))] + [
        (k, v, sum(1 for p in D.PROYECTOS if p["cat"] == k)) for k, v in D.CATEGORIAS.items()]
    botones = "".join(
        f'<button type="button" class="tab{" activo" if k == "todo" else ""}" data-filtro="{k}" aria-pressed="{"true" if k == "todo" else "false"}">{e(t)}<b>{n}</b></button>'
        for k, t, n in filtros)
    cartas = []
    for i, p in enumerate(D.PROYECTOS):
        cartas.append(f"""<a class="cromo" href="{p['slug']}.html" data-cat="{p['cat']}">
  <span class="cromo-in">
    <span class="cromo-frente">
      <span class="cromo-num">{i + 1:02d}</span>
      <img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}" loading="lazy">
      <span class="cromo-banda"><b>{e(p['corto'])}</b><span>{e(D.CATEGORIAS[p['cat']])}</span></span>
    </span>
    <span class="cromo-dorso">
      <span class="cromo-num">{i + 1:02d}</span>
      <b class="cromo-cifra">{e(p['cifra'])}</b><span class="cromo-cifra-t">{e(p['cifra_t'])}</span>
      <span class="cromo-res">{e(p['resumen'])}</span>
      <span class="cromo-meta">{e(p['ano'])} · {e(', '.join(p['herr']))}</span>
      <span class="cromo-ver">Ver partido →</span>
    </span>
  </span>
</a>""")
    cuerpo = f"""<main>
  <section class="pag-cab envoltura">
    <p class="kicker">Trabajo · {len(D.PROYECTOS)} proyectos · 6 disciplinas</p>
    <h1 class="pag-t"><span data-golpe>Todo</span> <span data-golpe><em>el trabajo</em></span></h1>
    <p class="pag-intro">Pasa el cursor sobre un cromo para darle la vuelta.</p>
  </section>
  <div class="tabs envoltura" role="group" aria-label="Filtrar por disciplina">{botones}</div>
  <section class="album envoltura" data-album>{"".join(cartas)}</section>
</main>"""
    return C.documento(f"Trabajo · {D.NOMBRE}", "Proyectos de diseño deportivo, video político y fotografía en vivo.", FUENTES,
                       envoltura(cuerpo, "trabajo.html"), clase="pg-trabajo")


def proyecto(p):
    i = D.PROYECTOS.index(p)
    sig = D.siguiente(p["slug"])
    datos = "".join(f'<div class="ficha-fila"><span>{e(t)}</span><b>{e(v)}</b></div>' for v, t in p["datos"])
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    video = C.bloque_video(p)
    cuerpo = f"""<main>
  <section class="ph" data-ph>
    <div class="ph-num" aria-hidden="true">{i + 1:02d}</div>
    <div class="envoltura ph-in">
      <div class="ph-txt">
        <p class="kicker"><a href="trabajo.html">Trabajo</a> · Fecha {i + 1:02d} · {e(D.CATEGORIAS[p['cat']])}</p>
        <h1 class="ph-t" data-golpe>{e(p['corto'])}</h1>
        <p class="ph-res">{e(p['resumen'])}</p>
      </div>
      <figure class="ph-afiche" data-tilt><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"></figure>
    </div>
  </section>
  <section class="envoltura p-cuerpo">
    <div class="ficha">
      <p class="ficha-t">Ficha técnica</p>
      <div class="ficha-fila"><span>Proyecto</span><b>{e(p['titulo'])}</b></div>
      <div class="ficha-fila"><span>Cliente</span><b>{e(p['cliente'])}</b></div>
      <div class="ficha-fila"><span>Mi rol</span><b>{e(D.ROLES[p['cat']])}</b></div>
      <div class="ficha-fila"><span>Año</span><b>{e(p['ano'])}</b></div>
      <div class="ficha-fila"><span>Herramientas</span><b>{e(', '.join(p['herr']))}</b></div>
      {datos}
    </div>
    <div class="p-txt">{textos}</div>
  </section>
  {f'<section class="envoltura">{video}</section>' if video else ''}
  <section class="envoltura p-gal">{C.galeria(p['slug'])}</section>
  <a class="proximo" href="{sig['slug']}.html">
    <span class="kicker">Próximo partido</span>
    <span class="proximo-vs"><span class="p-esc">EG</span><i>vs</i><span class="p-esc p-esc-v">{iniciales(sig)}</span></span>
    <span class="proximo-t">{e(sig['corto'])}</span>
    <span class="proximo-img"><img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></span>
  </a>
</main>
<div class="visor" data-visor hidden>
  <button type="button" class="visor-cerrar" data-visor-cerrar>Cerrar ✕</button>
  <button type="button" class="visor-ant" data-visor-ant aria-label="Anterior">←</button>
  <img alt="" data-visor-img>
  <button type="button" class="visor-sig" data-visor-sig aria-label="Siguiente">→</button>
  <span class="visor-n" data-visor-n></span>
</div>"""
    return C.documento(f"{p['corto']} · {D.NOMBRE}", p["resumen"], FUENTES, envoltura(cuerpo), clase="pg-proyecto")


def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    tray = "".join(
        f'<li><span class="tr-ano">{e(x["fechas"])}</span><span class="tr-club">{e(x["empresa"])}</span><span class="tr-pos">{e(x["puesto"])}</span></li>'
        for x in D.EXPERIENCIA)
    herr = "".join(f"<li>{e(h)}</li>" for h in D.HERRAMIENTAS)
    cuerpo = f"""<main>
  <section class="ficha-jug envoltura">
    <div class="fj-afiche" data-tilt>
      <span class="fj-num" aria-hidden="true">20</span>
      <img src="{C.retrato()}" alt="Retrato de {e(D.NOMBRE)}">
      <span class="fj-banda"><b>Esteban Guillen</b><span>Diseñador · Editor · Fotógrafo</span></span>
    </div>
    <div class="fj-txt">
      <p class="kicker">Perfil · {e(D.PUESTO)}</p>
      <h1 class="pag-t"><span data-golpe>Esteban</span> <span data-golpe><em>Guillen</em></span></h1>
      <dl class="fj-datos">
        <div><dt>Hoy</dt><dd>Harris Media Group</dd></div>
        <div><dt>Base</dt><dd>{e(D.CIUDAD)}</dd></div>
        <div><dt>Origen</dt><dd>{e(D.ORIGEN)}</dd></div>
        <div><dt>Experiencia</dt><dd>Desde 2018</dd></div>
      </dl>
      {bio}
    </div>
  </section>
  <section class="bloque envoltura sobre-dos">
    <div><div class="titulo-sec"><h2>Trayectoria</h2></div><ul class="tray">{tray}</ul></div>
    <div><div class="titulo-sec"><h2>Herramientas</h2></div><ul class="herr">{herr}</ul><p class="estado"><span></span>{e(D.DISPONIBLE)}</p>
      <p class="sobre-acc"><a class="boton" href="cv.html" data-magnetico>Ver currículum →</a><a class="boton boton-b" href="{e(D.CV_PDF)}" download>Descargar PDF ↓</a></p></div>
  </section>
</main>"""
    return C.documento(f"Perfil · {D.NOMBRE}", D.BIO, FUENTES, envoltura(cuerpo, "sobre.html"), clase="pg-sobre")


def contacto():
    cuerpo = f"""<main>
  <section class="conv envoltura">
    <p class="kicker">Contacto · {e(D.DISPONIBLE)}</p>
    <h1 class="pag-t"><span data-golpe>Hablemos</span> <span data-golpe><em>hoy</em></span></h1>
    <button type="button" class="conv-correo" data-copiar="{e(D.CORREO)}"><span>{e(D.CORREO)}</span><b data-copiado>Toca para copiar</b></button>
    <div class="conv-cols">
      <div><p class="kicker">Perfil</p><a href="cv.html">Currículum →</a><a href="{e(D.CV_PDF)}" download>CV en PDF ↓</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram ↗</a></div>
      <div><p class="kicker">Sede</p><p>{e(D.CIUDAD)}<br>Origen: {e(D.ORIGEN)}</p></div>
      <div><p class="kicker">Formatos</p><p>Video 16:9 · 9:16 · 1:1<br>Afiches, redes y web</p></div>
    </div>
  </section>
</main>"""
    return C.documento(f"Contacto · {D.NOMBRE}", "Escríbeme para tu próximo proyecto.", FUENTES,
                       envoltura(cuerpo, "contacto.html"), clase="pg-contacto")


def cv():
    cuerpo = f"""<main>
  <section class="pag-cab envoltura">
    <p class="kicker">Currículum · {e(D.NOMBRE)}</p>
    <h1 class="pag-t"><span data-golpe>Hoja</span> <span data-golpe><em>de vida</em></span></h1>
  </section>
  <section class="envoltura">{C.cv_secciones("cv-h")}</section>
</main>"""
    return C.documento(f"Currículum · {D.NOMBRE}", D.CV_RESUMEN, FUENTES, envoltura(cuerpo, "cv.html"), clase="pg-cv")


def paginas():
    out = {"index.html": inicio(), "trabajo.html": trabajo(), "sobre.html": sobre(), "cv.html": cv(), "contacto.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
