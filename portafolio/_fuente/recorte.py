# -*- coding: utf-8 -*-
"""Línea F · RECORTE — el portafolio hecho a mano: papel, cinta, recortes, sellos y tintas de risografía.

Nace del collage de los afiches de fútbol de Esteban y lo extiende a todo su trabajo: cada proyecto es
una pieza impresa y pegada en el muro; las cifras son sellos de goma; el currículum está mecanografiado.
"""
import random

import comun as C
import datos as D
from comun import e

FUENTES = ("family=DM+Serif+Display:ital@0;1&family=Archivo+Black&family=Courier+Prime:wght@400;700"
           "&family=Work+Sans:wght@400;500;600;700")

NAV = [("index.html", "Home"), ("work.html", "Archive"), ("about.html", "About"), ("cv.html", "CV"), ("contact.html", "Contact")]
TINTAS = ["rosa", "azul", "amarillo", "negro", "papel"]
LETRAS = ["l-serif", "l-negra", "l-maq"]

LOGO = """<svg class="logo" viewBox="0 0 70 44" aria-hidden="true">
<rect x="2" y="6" width="32" height="34" fill="var(--rosa)" transform="rotate(-6 18 23)"/>
<rect x="34" y="4" width="32" height="34" fill="var(--azul)" transform="rotate(5 50 21)"/>
<text x="18" y="33" text-anchor="middle" font-family="DM Serif Display, serif" font-size="28" fill="var(--tinta)" transform="rotate(-6 18 23)">E</text>
<text x="50" y="31" text-anchor="middle" font-family="Archivo Black, sans-serif" font-size="24" fill="#fff" transform="rotate(5 50 21)">G</text>
</svg>"""


def recortes(texto, semilla, clase="rc"):
    """Texto armado con letras recortadas: cada letra con su papel, su tipografía y su giro."""
    r = random.Random(semilla)
    out = []
    for palabra in texto.split(" "):
        letras = []
        for ch in palabra:
            t = r.choice(TINTAS)
            f = r.choice(LETRAS)
            letras.append(f'<span class="l {f} t-{t}" style="--r:{r.uniform(-7, 7):.1f}deg;--y:{r.uniform(-.06, .06):.2f}em" data-letra>{e(ch)}</span>')
        out.append(f'<span class="palabra">{"".join(letras)}</span>')
    return f'<span class="{clase}" aria-label="{e(texto)}">{" ".join(out)}</span>'


def giro(semilla, a=3.0):
    return f"{random.Random(semilla).uniform(-a, a):.1f}deg"


def cabecera(activa):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == activa else ""}>{t}</a>' for h, t in NAV)
    return f"""<header class="cab" data-cab>
  <a class="cab-marca" href="index.html" aria-label="{e(D.NOMBRE)}, home">{LOGO}<span>Esteban<br>Guillen</span></a>
  <nav class="cab-nav" aria-label="Main" data-nav>{links}</nav>
  <a class="cab-cv" href="{D.CV_PDF}" download><span>CV</span> PDF ↓</a>
  <button type="button" class="cab-menu" data-menu aria-expanded="false" aria-label="Menu"><span></span><span></span></button>
</header>"""


def hoja_transicion():
    return """<div class="hoja-t" data-hoja aria-hidden="true"><svg class="hoja-borde" viewBox="0 0 1200 40" preserveAspectRatio="none"><path d="M0 40 L0 18 L40 24 L80 10 L120 22 L170 8 L210 20 L260 12 L300 26 L350 9 L400 21 L450 11 L490 25 L540 7 L590 19 L630 13 L680 27 L730 10 L770 22 L820 6 L870 20 L910 14 L960 26 L1010 9 L1050 23 L1100 12 L1150 24 L1200 15 L1200 40 Z"/></svg>
<span class="hoja-txt" data-hoja-txt></span></div>"""


def cinta(items, clase=""):
    fila = "".join(f"<span>{e(t)}</span><i>✂</i>" for t in items)
    return f'<div class="cinta {clase}" aria-hidden="true"><div class="cinta-in" data-cinta>{fila}{fila}</div></div>'


def pie():
    return f"""<footer class="pie">
  <div class="pie-borde" aria-hidden="true"></div>
  <div class="pie-in">
    <p class="maq pie-k">End of the archive. Shall we keep going?</p>
    <a class="pie-t" href="contact.html">{recortes("Let's talk", 91, "rc rc-pie")}</a>
    <div class="pie-fila">
      <button type="button" class="pie-correo" data-copiar="{e(D.CORREO)}">{e(D.CORREO)}<span class="maq" data-copiado>copy</span></button>
      <a href="cv.html">Résumé</a><a href="{D.CV_PDF}" download>CV (PDF)</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a>
    </div>
    <div class="pie-legal maq"><span>© 2026 {e(D.NOMBRE)}</span><span>{e(D.CIUDAD)} · {e(D.PUESTO)}</span></div>
  </div>
</footer>"""


def pagina(cuerpo, activa, clase, titulo, desc):
    return C.documento(titulo, desc, FUENTES, f"{hoja_transicion()}{cabecera(activa)}<main>{cuerpo}</main>{pie()}", clase=clase)


def pieza(p, i, img=None, clase="pz"):
    img = img or p["portada"]
    w, h = C.medida(p["slug"], img)
    forma = "v" if h > w * 1.15 else ("h" if w > h * 1.3 else "c")
    cinta_pos = random.Random(i * 7).choice(["c-iz", "c-de", "c-ce"])
    return f"""<a class="{clase} pz-{forma}" href="{p['slug']}.html" data-cat="{p['cat']}" style="--r:{giro(i * 13 + 3)}">
  <span class="pz-cinta {cinta_pos}" aria-hidden="true"></span>
  <span class="pz-img"><img src="{C.img(p['slug'], img)}" alt="{e(p['titulo'])}" loading="lazy" draggable="false"></span>
  <span class="pz-eti" style="--r:{giro(i * 5 + 1, 2.5)}"><b>{e(p['titulo'])}</b><span class="maq">{e(D.CATEGORIAS[p['cat']])} · {e(p['ano'])} · {e(p['cifra'])} {e(p['cifra_t'])}</span></span>
</a>"""


# ------------------------------------------------------------------------------------------------ inicio
def inicio():
    flotantes = [("mercyme", "19.jpg", "f1"), ("nahomi-martinez", "09.jpg", "f2"), ("bobby-charles", "01.jpg", "f3"), ("qatar-2022", "04.jpg", "f4"), ("crowder", "17.jpg", "f5")]
    fl = "".join(f'<a class="flot {c}" href="{s}.html" data-flot style="--r:{giro(k * 31 + 9, 8)}"><span class="pz-cinta c-ce" aria-hidden="true"></span><img src="{C.img(s, n)}" alt="{e(D.por_slug(s)["titulo"])}" draggable="false"></a>'
                 for k, (s, n, c) in enumerate(flotantes))
    muro = "".join(pieza(p, i) for i, p in enumerate(D.PROYECTOS))
    sellos = "".join(f'<div class="sello s-{["rosa", "azul", "negro", "rosa"][k]}" style="--r:{giro(k * 17 + 2, 9)}" data-sello><b>{e(a)}</b><span>{e(b)}</span></div>' for k, (a, b) in enumerate(D.CIFRAS))
    serv = "".join(f'<li class="serv" style="--r:{giro(k * 11 + 4, 2)}"><span class="maq">No. {k + 1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for k, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""<section class="hero">
  <div class="hero-flot" aria-hidden="false">{fl}</div>
  <div class="hero-c">
    <p class="maq hero-k" data-maquina>{e(D.PUESTO)} — {e(D.CIUDAD)}</p>
    <h1 class="hero-t">{recortes("Esteban", 7)}<br>{recortes("Guillen", 12)}</h1>
    <p class="hero-b">{e(D.BIO)}</p>
    <div class="hero-acc"><a class="btn" href="work.html">See the archive</a><a class="btn btn-l" href="cv.html">Résumé</a></div>
  </div>
  <div class="sello-redondo" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="circ" d="M60 60 m-46 0 a46 46 0 1 1 92 0 a46 46 0 1 1 -92 0"/></defs><text><textPath href="#circ">AVAILABLE · FULL-TIME · FREELANCE · HIRE ME ·</textPath></text></svg><b>EG</b></div>
  <p class="hero-guia maq">You can drag the letters</p>
</section>
{cinta(["1.3M+ views on political video", "60 concert photos", "53 football posters", "37 pieces for a World Cup", "Harris Media Group", "Since 2018", "Lima → Miami"])}

<section class="sec envol">
  <header class="sec-cab"><p class="maq k">The wall · selected work</p><h2>{recortes("Twelve", 21, "rc rc-h")} projects taped to the wall.</h2></header>
  <div class="muro">{muro}</div>
</section>

<section class="sec envol cifras">
  <header class="sec-cab"><p class="maq k">Signed and stamped</p><h2>The numbers, in ink.</h2></header>
  <div class="sellos">{sellos}</div>
</section>

<section class="sec envol">
  <header class="sec-cab"><p class="maq k">Experience · typewritten</p><h2>From Lima to Miami, since 2018.</h2></header>
  <div class="hoja-maq" style="--r:-.6deg"><span class="pz-cinta c-iz" aria-hidden="true"></span><span class="pz-cinta c-de" aria-hidden="true"></span>{C.recorrido()}<a class="enl maq" href="cv.html">→ Read the full résumé</a></div>
</section>

<section class="sec envol">
  <header class="sec-cab"><p class="maq k">What I do</p><h2>Five crafts, the same care.</h2></header>
  <ul class="servicios">{serv}</ul>
</section>"""
    return pagina(cuerpo, "index.html", "pg-inicio", f"{D.NOMBRE} · Cutout", D.BIO)


# ------------------------------------------------------------------------------------------------ archivo
def trabajo():
    tabs = [("todo", "All", len(D.PROYECTOS))] + [(k, v, sum(1 for p in D.PROYECTOS if p["cat"] == k)) for k, v in D.CATEGORIAS.items()]
    botones = "".join(f'<button type="button" class="pestana{" activo" if k == "todo" else ""}" data-filtro="{k}" aria-pressed="{"true" if k == "todo" else "false"}" style="--r:{giro(n * 3 + len(t), 1.5)}">{e(t)} <span class="maq">{n}</span></button>' for k, t, n in tabs)
    cuerpo = f"""<section class="pag-cab envol"><p class="maq k">Archive · {len(D.PROYECTOS)} projects</p><h1>{recortes("Archive", 33, "rc rc-xl")}</h1>
  <p class="pag-intro">Campaign video, live photography, sports design, brands, web and gaming. All printed and taped up here.</p></section>
<section class="envol"><div class="pestanas" role="group" aria-label="Filter by discipline">{botones}</div>
  <div class="muro muro-archivo" data-muro>{''.join(pieza(p, i) for i, p in enumerate(D.PROYECTOS))}</div></section>"""
    return pagina(cuerpo, "work.html", "pg-trabajo", f"Work · {D.NOMBRE}", "Twelve projects in video, photography, sports design, branding, web and gaming.")


# ------------------------------------------------------------------------------------------------ proyecto
def proyecto(p):
    i = D.PROYECTOS.index(p)
    sig = D.siguiente(p["slug"])
    ims = D.imagenes(p["slug"])
    piezas = []
    for k, (n, w, h) in enumerate(ims):
        ar = w / h
        cls = "gz-largo" if ar < .45 else ("gz-v" if ar < .9 else ("gz-h" if ar > 1.5 else "gz-c"))
        piezas.append(f'<figure class="gz {cls}" data-i="{k}" style="--r:{giro(k * 19 + i, 1.8)}"><span class="pz-cinta {random.Random(k).choice(["c-iz", "c-de", "c-ce"])}" aria-hidden="true"></span>'
                      f'<span class="gz-img"><img src="{C.img(p["slug"], n)}" alt="{e(p["titulo"])}, piece {k + 1}" loading="lazy" width="{w}" height="{h}"></span>'
                      f'<figcaption class="maq">{k + 1:02d}/{len(ims):02d}</figcaption></figure>')
    datos = "".join(f'<div class="sello s-{["rosa", "azul", "negro"][k % 3]}" style="--r:{giro(k * 23 + i, 7)}" data-sello><b>{e(v)}</b><span>{e(t)}</span></div>' for k, (v, t) in enumerate(p["datos"]))
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    cuerpo = f"""<section class="p-cab envol">
  <p class="maq k"><a href="work.html">Archive</a> / {e(D.CATEGORIAS[p['cat']])} / No. {i + 1:02d}</p>
  <h1>{recortes(p['corto'], 100 + i, "rc rc-p")}</h1>
</section>
<section class="envol p-intro">
  <figure class="p-portada" style="--r:{giro(i, 1.5)}"><span class="pz-cinta c-iz" aria-hidden="true"></span><span class="pz-cinta c-de" aria-hidden="true"></span><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"></figure>
  <div class="ficha" style="--r:{giro(i + 50, 1.2)}">
    <span class="grapa" aria-hidden="true"></span>
    <p class="maq ficha-t">File No. {i + 1:02d}</p>
    <h2>{e(p['titulo'])}</h2>
    <dl>
      <div><dt class="maq">Client</dt><dd>{e(p['cliente'])}</dd></div>
      <div><dt class="maq">My role</dt><dd>{e(D.ROLES[p['cat']])}</dd></div>
      <div><dt class="maq">Year</dt><dd>{e(p['ano'])}</dd></div>
      <div><dt class="maq">Tools</dt><dd>{e(', '.join(p['herr']))}</dd></div>
    </dl>
  </div>
</section>
<section class="envol p-txt"><p class="p-res">{e(p['resumen'])}</p><div class="p-cols">{textos}</div></section>
<section class="envol sellos sellos-p">{datos}</section>
<section class="envol">{C.bloque_video(p)}</section>
<section class="envol"><div class="collage" data-galeria>{''.join(piezas)}</div></section>
<section class="envol"><a class="sig" href="{sig['slug']}.html"><span class="maq">Next in the archive →</span>{recortes(sig['corto'], 200 + i, "rc rc-sig")}<img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></a></section>
<div class="lb" data-lb hidden><button type="button" class="lb-x maq" data-lb-x>Close · Esc</button><button type="button" class="lb-a" data-lb-a aria-label="Previous">←</button><img alt="" data-lb-img><button type="button" class="lb-s" data-lb-s aria-label="Next">→</button><span class="lb-n maq" data-lb-n></span></div>"""
    return pagina(cuerpo, "", "pg-proyecto", f"{p['corto']} · {D.NOMBRE}", p["resumen"])


# ------------------------------------------------------------------------------------------------ perfil, cv, contacto
def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    cuerpo = f"""<section class="pag-cab envol"><p class="maq k">About</p><h1>{recortes("Hello", 44, "rc rc-xl")}</h1></section>
<section class="envol perfil">
  <figure class="polaroid" style="--r:-3deg"><span class="pz-cinta c-ce" aria-hidden="true"></span><img src="{C.retrato()}" alt="Portrait of {e(D.NOMBRE)}"><figcaption>Esteban · {e(D.CIUDAD)}</figcaption>
    <span class="sello s-rosa sello-mini" style="--r:12deg"><b>8</b><span>years on the job</span></span></figure>
  <div class="perfil-txt"><p class="lead">{e(D.BIO)}</p>{bio}
    <div class="hero-acc"><a class="btn" href="cv.html">View résumé</a><a class="btn btn-l" href="{D.CV_PDF}" download>Download PDF</a></div></div>
</section>
<section class="sec envol"><header class="sec-cab"><p class="maq k">Experience</p><h2>Since 2018.</h2></header>
  <div class="hoja-maq" style="--r:.5deg"><span class="pz-cinta c-iz" aria-hidden="true"></span>{C.recorrido()}</div></section>"""
    return pagina(cuerpo, "about.html", "pg-sobre", f"About · {D.NOMBRE}", D.BIO)


def cv():
    cuerpo = f"""<section class="pag-cab envol"><p class="maq k">Résumé · curriculum vitae</p><h1>{recortes("Résumé", 55, "rc rc-xl")}</h1></section>
<section class="envol"><div class="hoja-cv"><span class="pz-cinta c-iz" aria-hidden="true"></span><span class="pz-cinta c-de" aria-hidden="true"></span>
  <span class="sello s-azul sello-cv" style="--r:-11deg" data-sello><b>Available</b><span>full-time · freelance</span></span>{C.cv_secciones("maq k")}</div></section>"""
    return pagina(cuerpo, "cv.html", "pg-cv", f"Résumé · {D.NOMBRE}", D.CV_RESUMEN)


def contacto():
    cuerpo = f"""<section class="pag-cab envol"><p class="maq k">Contact · {e(D.DISPONIBLE)}</p><h1>{recortes("Write me", 66, "rc rc-xl")}</h1></section>
<section class="envol contacto">
  <div class="sobre-carta" style="--r:-1.2deg">
    <span class="estampilla" aria-hidden="true">{LOGO}<span class="maq">Miami · 2026</span></span>
    <p class="maq">To: {e(D.NOMBRE)}</p>
    <button type="button" class="ct-correo" data-copiar="{e(D.CORREO)}"><b>{e(D.CORREO)}</b><span class="maq" data-copiado>click to copy</span></button>
    <a class="btn" href="mailto:{e(D.CORREO)}">Open email</a>
  </div>
  <dl class="ct-dl">
    <div><dt class="maq">Location</dt><dd>{e(D.CIUDAD)} · From {e(D.ORIGEN)}</dd></div>
    <div><dt class="maq">Languages</dt><dd>{e(' · '.join(a + ' ' + b.lower() for a, b in D.IDIOMAS))}</dd></div>
    <div><dt class="maq">Résumé</dt><dd><a href="cv.html">Online</a> · <a href="{D.CV_PDF}" download>PDF ↓</a></dd></div>
    <div><dt class="maq">Instagram</dt><dd><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">{e(D.INSTAGRAM_T)} ↗</a></dd></div>
    <div><dt class="maq">Services</dt><dd>{e(' · '.join(t for t, _ in D.SERVICIOS))}</dd></div>
  </dl>
</section>"""
    return pagina(cuerpo, "contact.html", "pg-contacto", f"Contact · {D.NOMBRE}", "Get in touch about a role or a project.")


def paginas():
    out = {"index.html": inicio(), "work.html": trabajo(), "about.html": sobre(), "cv.html": cv(), "contact.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
