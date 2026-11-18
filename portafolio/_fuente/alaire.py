# -*- coding: utf-8 -*-
"""Línea E · AL AIRE — todo lo que hace Esteban sale al aire: spots de campaña, conciertos en vivo,
partidos y transmisiones. La web se comporta como un canal: zapping, rótulos (lower thirds), guía de
programación, ticker, rating y créditos finales.
"""
import json

import comun as C
import datos as D
from comun import e

FUENTES = "family=Big+Shoulders+Display:wght@500;700;800;900&family=Onest:wght@400;500;600;700&family=Chivo+Mono:wght@400;500"

BUG = """<svg class="bug" viewBox="0 0 72 40" aria-hidden="true"><rect x="1" y="1" width="70" height="38" rx="7" fill="none" stroke="currentColor" stroke-width="2"/>
<text x="31" y="29" text-anchor="middle" font-family="Big Shoulders Display, sans-serif" font-weight="900" font-size="26" fill="currentColor">EG</text><circle cx="58" cy="20" r="5" fill="var(--rojo)"/></svg>"""

NAV = [("index.html", "Live"), ("work.html", "Shows"), ("about.html", "About"), ("cv.html", "CV"), ("contact.html", "Contact")]
CANALES = {k: i + 1 for i, k in enumerate(D.CATEGORIAS)}
ZAPPING = ["mercyme", "gallucci", "nahomi-martinez", "qatar-2022", "bobby-charles", "for-king-country", "valorant", "physo"]
HERO_IMG = {"mercyme": "07.jpg", "gallucci": "00.jpg", "nahomi-martinez": "00.jpg", "qatar-2022": "04.jpg", "bobby-charles": "00.jpg",
            "for-king-country": "01.jpg", "valorant": "02.jpg", "physo": "02.jpg"}


def tc(i):
    s = 7 + i * 13
    return f"00:{(s // 60) % 60:02d}:{s % 60:02d}:{(i * 7) % 25:02d}"


def cabecera(activa):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == activa else ""}><span>{t}</span></a>' for h, t in NAV)
    return f"""<header class="cab" data-cab>
  <a class="cab-marca" href="index.html" aria-label="{e(D.NOMBRE)}, home">{BUG}<span><b>Esteban Guillen</b><small>Portfolio channel</small></span></a>
  <nav class="cab-nav" aria-label="Main" data-nav>{links}</nav>
  <div class="cab-der"><span class="vivo"><i></i>LIVE</span><span class="tc mono" data-tc>00:00:00:00</span><a class="cab-cv" href="{D.CV_PDF}" download>CV PDF</a>
  <button type="button" class="cab-menu" data-menu aria-expanded="false" aria-label="Menu"><span></span><span></span></button></div>
</header>"""


def capas_fijas():
    return """<div class="zap" data-zap aria-hidden="true"><canvas data-ruido></canvas><span class="zap-ch" data-zap-ch></span></div>
<div class="crt" data-crt aria-hidden="true"></div>"""


def barras():
    cols = ["#c0c0c0", "#c0c000", "#00c0c0", "#00c000", "#c000c0", "#c00000", "#0000c0"]
    return '<div class="barras" aria-hidden="true">' + "".join(f'<i style="background:{c}"></i>' for c in cols) + "</div>"


def pie():
    return f"""<footer class="pie">
  {barras()}
  <div class="pie-in">
    <p class="mono pie-k">End of broadcast · thanks for tuning in</p>
    <a class="pie-t" href="contact.html"><span>Let's talk</span><span aria-hidden="true">Let's talk</span></a>
    <div class="pie-fila">
      <button type="button" class="pie-correo" data-copiar="{e(D.CORREO)}">{e(D.CORREO)} <span class="mono" data-copiado>Copy</span></button>
      <a href="cv.html">Résumé</a><a href="{D.CV_PDF}" download>CV (PDF)</a><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a>
    </div>
    <div class="pie-legal mono"><span>© 2026 {e(D.NOMBRE)}</span><span>{e(D.CIUDAD)} · {e(D.PUESTO)}</span></div>
  </div>
</footer>"""


def pagina(cuerpo, activa, clase, titulo, desc):
    return C.documento(titulo, desc, FUENTES, f"{capas_fijas()}{cabecera(activa)}<main>{cuerpo}</main>{pie()}", clase=clase)


def tercio(titulo, sub, clase=""):
    return f'<div class="tercio {clase}"><span class="tercio-a">{e(titulo)}</span><span class="tercio-b">{e(sub)}</span></div>'


def ticker(items):
    fila = "".join(f"<span>{e(t)}</span><i></i>" for t in items)
    return f'<div class="ticker"><b class="ticker-k">On air</b><div class="ticker-v"><div class="ticker-in" data-ticker>{fila}{fila}</div></div></div>'


# ------------------------------------------------------------------------------------------------ inicio
def inicio():
    progs = []
    for i, s in enumerate(ZAPPING):
        p = D.por_slug(s)
        progs.append(dict(slug=s, t=p["titulo"], c=D.CATEGORIAS[p["cat"]], ch=CANALES[p["cat"]], cli=p["cliente"],
                          cifra=f'{p["cifra"]} {p["cifra_t"]}', img=C.img(s, HERO_IMG[s])))
    pantallas = "".join(f'<img class="tx-img{" activa" if i == 0 else ""}" src="{x["img"]}" alt="{e(x["t"])}" data-i="{i}"{"" if i == 0 else " loading=\"lazy\""}>' for i, x in enumerate(progs))
    # guía de programación: trayectoria + canales por disciplina, de 2018 a 2026
    anos = list(range(2018, 2027))
    def col(a):
        return a - 2018 + 2
    carriles = []  # trayectoria: cada puesto en el primer carril libre
    for x in sorted(D.EXPERIENCIA, key=lambda x: x["inicio"]):
        for k, fin in enumerate(carriles):
            if fin < x["inicio"]:
                carriles[k] = x["fin"]; x["_c"] = k; break
        else:
            carriles.append(x["fin"]); x["_c"] = len(carriles) - 1
    n_c = len(carriles)
    filas = [f'<div class="epg-ch epg-tray" style="grid-row:2 / span {n_c}"><b>CV</b><span>Career</span></div>']
    for x in D.EXPERIENCIA:
        filas.append(f'<a class="epg-p epg-job" href="cv.html" style="grid-row:{2 + x["_c"]};grid-column:{col(x["inicio"])} / {col(x["fin"]) + 1}" '
                     f'data-pip="{e(x["puesto"])}|{e(x["empresa"])} · {e(x["fechas"])}|{C.retrato()}"><b>{e(x["empresa"])}</b><span>{e(x["puesto"])}</span></a>')
    fila_n = 2 + n_c
    for k, nombre in D.CATEGORIAS.items():
        filas.append(f'<div class="epg-ch" style="grid-row:{fila_n}"><b>{CANALES[k]:02d}</b><span>{e(nombre)}</span></div>')
        por_ano = {}
        for p in D.PROYECTOS:
            if p["cat"] == k:
                por_ano.setdefault(int(p["ano"]), []).append(p)
        for a, ps in por_ano.items():
            links = "".join(f'<a href="{p["slug"]}.html" data-pip="{e(p["titulo"])}|{e(p["cifra"])} {e(p["cifra_t"])} · {e(p["cliente"])}|{C.img(p["slug"], p["portada"])}">'
                            f'<b>{e(p["corto"])}</b><span>{e(p["cifra"])} {e(p["cifra_t"])}</span></a>' for p in ps)
            filas.append(f'<div class="epg-p epg-multi" style="grid-row:{fila_n};grid-column:{col(a)}">{links}</div>')
        fila_n += 1
    cab_anos = "".join(f'<span class="epg-a{" ahora" if a == 2026 else ""}" style="grid-column:{col(a)}">{a}</span>' for a in anos)
    # rating
    rating = [("Sam Gallucci & NH Senate", 900, "gallucci"), ("Bobby Charles for Maine", 436, "bobby-charles")]
    barras_r = "".join(f'<a class="rt-f" href="{s}.html"><span class="rt-t">{e(t)}</span><span class="rt-b"><i style="--v:{v / 900:.3f}"></i></span><b><span data-contar="{v}">{v}</span>K</b></a>' for t, v, s in rating)
    destacados = []
    for i, p in enumerate(D.PROYECTOS):
        destacados.append(f"""<a class="ep" href="{p['slug']}.html">
  <span class="ep-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}" loading="lazy" draggable="false"><span class="ep-tc mono">{tc(i)}</span><span class="ep-play" aria-hidden="true">▶</span></span>
  <span class="ep-ch mono">CH {CANALES[p['cat']]:02d} · {e(D.CATEGORIAS[p['cat']])}</span><b class="ep-t">{e(p['titulo'])}</b><span class="ep-c">{e(p['cifra'])} {e(p['cifra_t'])} · {e(p['ano'])}</span>
</a>""")
    formatos = "".join(f'<li><span class="mono">F{i + 1:02d}</span><b>{e(t)}</b><span>{e(d)}</span></li>' for i, (t, d) in enumerate(D.SERVICIOS))
    cuerpo = f"""<section class="tx" data-tx>
  <div class="tx-pant" data-pant>{pantallas}<div class="tx-scan" aria-hidden="true"></div><div class="tx-vin" aria-hidden="true"></div></div>
  <div class="tx-safe" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="tx-sup"><span class="vivo vivo-g"><i></i>LIVE</span><span class="mono tx-ch" data-ch>CH {progs[0]['ch']:02d}</span></div>
  <div class="tx-inf">
    <div class="tx-tercio" data-tercio>
      <h1 class="tercio tercio-xl"><span class="tercio-a">Esteban Guillen</span><span class="tercio-b">{e(D.PUESTO)} · {e(D.CIUDAD)}</span></h1>
    </div>
    <div class="tx-ahora">
      <span class="mono">Now showing</span>
      <a href="{progs[0]['slug']}.html" class="tx-prog" data-prog><b data-prog-t>{e(progs[0]['t'])}</b><span data-prog-c>{e(progs[0]['c'])} · {e(progs[0]['cifra'])}</span></a>
      <span class="tx-barra"><i data-prog-barra></i></span>
      <div class="tx-ctl"><button type="button" data-zap-btn="-1" aria-label="Previous channel">CH −</button><button type="button" data-zap-btn="1" aria-label="Next channel">CH +</button></div>
    </div>
  </div>
  {ticker(["1.3M+ views on political video", "Video Editor & Videographer at Harris Media Group", "60 concert photos: MercyMe, Crowder, for KING & COUNTRY", "53 posters for Peruvian football", "Qatar 2022: 37 pieces", "Since 2018 · From Lima to Miami", D.DISPONIBLE])}
</section>
<script type="application/json" id="programas">{json.dumps(progs, ensure_ascii=False)}</script>

<section class="sec envol presenta">
  <p class="mono k">Introduction</p>
  <p class="presenta-t" data-revelar>I edit, shoot, design and photograph work that goes on air: campaign spots with hundreds of thousands of views, live concerts, match days and brands that post every day.</p>
  <div class="presenta-acc"><a class="btn" href="work.html">See all 12 shows</a><a class="btn btn-l" href="cv.html">Résumé</a></div>
</section>

<section class="sec envol rating">
  <header class="sec-cab"><p class="mono k">Ratings · political video</p><h2>Measured<br>audience.</h2><p class="sec-nota">Real views on the campaigns I edited and animated at Harris Media Group.</p></header>
  <div class="rt">{barras_r}<p class="rt-tot"><span class="mono">Total</span><b>1.3M+</b><span>views</span></p></div>
</section>

<section class="sec envol">
  <header class="sec-cab"><p class="mono k">TV guide · 2018 — today</p><h2>Eight years<br>on air.</h2><p class="sec-nota">Career and projects by channel. Hover over a show to preview it in the window.</p></header>
  <div class="epg-w" data-epg>
    <div class="epg-pip" data-pip-v aria-hidden="true"><img alt="" data-pip-img><span class="epg-pip-t"><b data-pip-t>Esteban Guillen</b><span data-pip-s>{e(D.PUESTO)}</span></span><i class="vivo"><i></i>PIP</i></div>
    <div class="epg">
      <div class="epg-ch epg-esq">Channel</div>{cab_anos}
      {''.join(filas)}
      <span class="epg-ahora" style="grid-row:1 / {fila_n}" aria-hidden="true"></span>
    </div>
  </div>
</section>

<section class="sec">
  <header class="sec-cab envol"><p class="mono k">Highlights</p><h2>Twelve<br>episodes.</h2><p class="sec-nota">Drag the strip or use the arrows.</p></header>
  <div class="tira" data-tira><div class="tira-in" data-tira-in>{''.join(destacados)}</div></div>
  <div class="tira-ctl envol"><button type="button" data-tira-btn="-1" aria-label="Previous">←</button><span class="tira-barra"><i data-tira-barra></i></span><button type="button" data-tira-btn="1" aria-label="Next">→</button></div>
</section>

<section class="sec envol">
  <header class="sec-cab"><p class="mono k">Formats</p><h2>What I<br>produce.</h2></header>
  <ol class="formatos">{formatos}</ol>
</section>"""
    return pagina(cuerpo, "index.html", "pg-inicio", f"{D.NOMBRE} · On Air", D.BIO)


# ------------------------------------------------------------------------------------------------ programas
def trabajo():
    filas = []
    for k, nombre in D.CATEGORIAS.items():
        ps = [p for p in D.PROYECTOS if p["cat"] == k]
        cards = "".join(f"""<a class="ep" href="{p['slug']}.html">
  <span class="ep-img"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}" loading="lazy"><span class="ep-tc mono">{tc(D.PROYECTOS.index(p))}</span><span class="ep-play" aria-hidden="true">▶</span></span>
  <b class="ep-t">{e(p['titulo'])}</b><span class="ep-c">{e(p['cliente'])}</span><span class="ep-c">{e(p['cifra'])} {e(p['cifra_t'])} · {e(p['ano'])}</span>
</a>""" for p in ps)
        filas.append(f"""<section class="canal" id="ch-{k}">
  <header class="canal-cab"><span class="canal-n">{CANALES[k]:02d}</span><h2>{e(nombre)}</h2><span class="mono">{len(ps)} {"show" if len(ps) == 1 else "shows"}</span></header>
  <div class="canal-fila">{cards}</div>
</section>""")
    indice = "".join(f'<a href="#ch-{k}"><b>{CANALES[k]:02d}</b>{e(n)}</a>' for k, n in D.CATEGORIAS.items())
    cuerpo = f"""<section class="pag-cab envol"><p class="mono k">Shows · {len(D.PROYECTOS)} projects on 6 channels</p><h1 data-golpe>Full<br>schedule</h1>
  <nav class="canales-ix" aria-label="Channels">{indice}</nav></section>
<div class="envol canales">{''.join(filas)}</div>"""
    return pagina(cuerpo, "work.html", "pg-trabajo", f"Work · {D.NOMBRE}", "Twelve projects in video, photography, sports design, branding, web and gaming.")


# ------------------------------------------------------------------------------------------------ episodio
def proyecto(p):
    i = D.PROYECTOS.index(p)
    sig = D.siguiente(p["slug"])
    ims = D.imagenes(p["slug"])
    cuadros = []
    for k, (n, w, h) in enumerate(ims):
        ar = w / h
        cls = "cd-largo" if ar < .45 else ("cd-v" if ar < .9 else ("cd-h" if ar > 1.5 else "cd-c"))
        cuadros.append(f'<figure class="cd {cls}" data-i="{k}"><span class="cd-img"><img src="{C.img(p["slug"], n)}" alt="{e(p["titulo"])}, frame {k + 1}" loading="lazy" width="{w}" height="{h}"></span>'
                       f'<figcaption class="mono"><span>{tc(k)}</span><span>{k + 1:02d}/{len(ims):02d}</span></figcaption></figure>')
    datos = "".join(f'<div><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in p["datos"])
    textos = "".join(f"<p>{e(t)}</p>" for t in p["texto"])
    cuerpo = f"""<section class="ep-hero">
  <div class="ep-pant"><img src="{C.img(p['slug'], p['portada'])}" alt="{e(p['titulo'])}"><div class="tx-scan" aria-hidden="true"></div><div class="tx-vin" aria-hidden="true"></div>
    <div class="tx-safe" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
    <div class="tx-sup"><span class="vivo vivo-g"><i></i>EP {i + 1:02d}</span><span class="mono tx-ch">CH {CANALES[p['cat']]:02d} · {e(D.CATEGORIAS[p['cat']])}</span></div>
    <div class="ep-tercio" data-tercio><h1 class="tercio tercio-xl"><span class="tercio-a">{e(p['titulo'])}</span><span class="tercio-b">{e(p['cliente'])}</span></h1></div>
  </div>
</section>
<section class="envol ficha">
  <dl class="ficha-dl">
    <div><dt class="mono">Client</dt><dd>{e(p['cliente'])}</dd></div>
    <div><dt class="mono">My role</dt><dd>{e(D.ROLES[p['cat']])}</dd></div>
    <div><dt class="mono">Season</dt><dd>{e(p['ano'])}</dd></div>
    <div><dt class="mono">Tools</dt><dd>{e(', '.join(p['herr']))}</dd></div>
  </dl>
  <div class="ficha-txt"><p class="ficha-res">{e(p['resumen'])}</p>{textos}</div>
  <div class="ficha-datos">{datos}</div>
</section>
<section class="envol">{C.bloque_video(p)}</section>
<section class="envol cuadros-sec"><header class="sec-cab sec-cab-c"><p class="mono k">Frames · {len(ims)}</p></header><div class="cuadros" data-galeria>{''.join(cuadros)}</div></section>
<section class="envol">
  <a class="sigue" href="{sig['slug']}.html" data-sigue>
    <span class="sigue-img"><img src="{C.img(sig['slug'], sig['portada'])}" alt="" loading="lazy"></span>
    <span class="sigue-txt"><span class="mono">Up next · EP {D.PROYECTOS.index(sig) + 1:02d}</span><b>{e(sig['titulo'])}</b><span>{e(D.CATEGORIAS[sig['cat']])}</span><span class="sigue-barra"><i data-sigue-barra></i></span></span>
  </a>
</section>
<div class="lb" data-lb hidden><button type="button" class="lb-x mono" data-lb-x>Close · Esc</button><button type="button" class="lb-a" data-lb-a aria-label="Previous">←</button><img alt="" data-lb-img><button type="button" class="lb-s" data-lb-s aria-label="Next">→</button><span class="lb-n mono" data-lb-n></span></div>"""
    return pagina(cuerpo, "", "pg-proyecto", f"{p['corto']} · {D.NOMBRE}", p["resumen"])


# ------------------------------------------------------------------------------------------------ perfil, cv, contacto
def sobre():
    bio = "".join(f"<p>{e(x)}</p>" for x in D.BIO_LARGA)
    cuerpo = f"""<section class="pag-cab envol"><p class="mono k">About</p><h1 data-golpe>Behind<br>the camera</h1></section>
<section class="envol perfil">
  <figure class="perfil-foto"><img src="{C.retrato()}" alt="Portrait of {e(D.NOMBRE)}"><div class="tx-scan" aria-hidden="true"></div>{tercio(D.NOMBRE, D.PUESTO, "tercio-perfil")}</figure>
  <div class="perfil-txt"><p class="lead">{e(D.BIO)}</p>{bio}
    <div class="presenta-acc"><a class="btn" href="cv.html">View résumé</a><a class="btn btn-l" href="{D.CV_PDF}" download>Download PDF</a></div></div>
</section>
<section class="sec envol"><header class="sec-cab"><p class="mono k">Career</p><h2>Since<br>2018.</h2></header>{C.recorrido()}</section>"""
    return pagina(cuerpo, "about.html", "pg-sobre", f"About · {D.NOMBRE}", D.BIO)


def cv():
    creditos = "".join(f'<li><span>{e(x["puesto"])}</span><i></i><b>{e(x["empresa"])}</b><small class="mono">{e(x["fechas"])}</small></li>' for x in D.EXPERIENCIA)
    hab = "".join(f'<li><span>{e(t)}</span><i></i><b>{e(", ".join(l[:3]))}</b></li>' for t, l in D.HABILIDADES)
    cuerpo = f"""<section class="creditos" data-creditos>
  <div class="creditos-pant">
    <div class="creditos-rollo" data-rollo>
      <p class="mono">A portfolio by</p><h1>Esteban Guillen</h1>
      <p class="mono cr-sec">Experience</p><ul>{creditos}</ul>
      <p class="mono cr-sec">Specialties</p><ul>{hab}</ul>
      <p class="mono cr-sec">Tools</p><p class="cr-herr">{e(" · ".join(D.HERRAMIENTAS))}</p>
      <p class="mono cr-sec">Filmed in</p><p class="cr-herr">{e(D.CIUDAD)} · Lima, Peru</p>
      <p class="cr-fin">Full résumé ↓</p>
    </div>
  </div>
</section>
<section class="envol cv-sec">{C.cv_secciones("mono k")}</section>"""
    return pagina(cuerpo, "cv.html", "pg-cv", f"Résumé · {D.NOMBRE}", D.CV_RESUMEN)


def contacto():
    cuerpo = f"""<section class="pag-cab envol"><p class="mono k">Contact · lines are open</p><h1 data-golpe>Let's go<br>on air</h1></section>
<section class="envol contacto">
  <button type="button" class="ct-correo" data-copiar="{e(D.CORREO)}"><span class="mono" data-copiado>Click to copy the email</span><b>{e(D.CORREO)}</b></button>
  <dl class="ficha-dl ct-dl">
    <div><dt class="mono">Status</dt><dd><span class="vivo"><i></i>{e(D.DISPONIBLE)}</span></dd></div>
    <div><dt class="mono">Location</dt><dd>{e(D.CIUDAD)} · From {e(D.ORIGEN)}</dd></div>
    <div><dt class="mono">Languages</dt><dd>{e(' · '.join(a + ' ' + b.lower() for a, b in D.IDIOMAS))}</dd></div>
    <div><dt class="mono">Résumé</dt><dd><a href="cv.html">Online</a> · <a href="{D.CV_PDF}" download>PDF ↓</a></dd></div>
    <div><dt class="mono">Instagram</dt><dd><a href="{e(D.INSTAGRAM)}" target="_blank" rel="noopener">{e(D.INSTAGRAM_T)} ↗</a></dd></div>
  </dl>
</section>"""
    return pagina(cuerpo, "contact.html", "pg-contacto", f"Contact · {D.NOMBRE}", "Get in touch about a role or a project.")


def paginas():
    out = {"index.html": inicio(), "work.html": trabajo(), "about.html": sobre(), "cv.html": cv(), "contact.html": contacto()}
    for p in D.PROYECTOS:
        out[p["slug"] + ".html"] = proyecto(p)
    return out
