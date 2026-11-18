# -*- coding: utf-8 -*-
"""Genera el manual de línea gráfica (PDF) de cada web.

    python3 _fuente/manual.py <carpeta-capturas>

Necesita las capturas de las webs (las genera capturas_pdf.js) y Playwright para imprimir el PDF.
"""
import os
import subprocess
import sys

import datos as D
from comun import e

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
IMG = "file://" + os.path.join(RAIZ, "img")


def foto(slug, n):
    return f"{IMG}/{slug}/{n}"


def cmyk(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    k = 1 - max(r, g, b)
    if k >= 1:
        return "0 · 0 · 0 · 100"
    c, m, y = ((1 - x - k) / (1 - k) for x in (r, g, b))
    return " · ".join(str(round(v * 100)) for v in (c, m, y, k))


def rgb(hx):
    return " · ".join(str(int(hx[i:i + 2], 16)) for i in (1, 3, 5))


# --------------------------------------------------------------------------------------------
LINEAS = {
    "luz": {
        "titulo": "LUZ", "sub": "Línea gráfica 01 · Fotografía en vivo, video y diseño",
        "fuentes": "family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Manrope:wght@400;500;600&family=DM+Mono",
        "bg": "#070708", "fg": "#eee8de", "acc": "#ffb648", "mut": "#8d8a85", "lin": "#2a2a31", "sup": "#121216",
        "fd": "'Cormorant Garamond', serif", "ft": "Manrope, sans-serif", "fm": "'DM Mono', monospace",
        "d_peso": "400", "d_trk": "-0.035em", "d_case": "none", "d_italic": True,
        "concepto": [
            "LUZ nace de la fotografía de conciertos de Esteban: escenarios a oscuras donde un solo haz decide qué se ve y qué no.",
            "La identidad trabaja igual. Fondo negro de escenario, una sola luz ámbar de tungsteno y una serif clásica en itálica que se comporta como el nombre de una gira.",
            "Es la línea para presentarse como fotógrafo y editor: sobria, cinematográfica y centrada en la imagen.",
        ],
        "origen": [("mercyme", "07.jpg", "MercyMe 2025"), ("crowder", "17.jpg", "Crowder Live"), ("for-king-country", "06.jpg", "for KING & COUNTRY")],
        "colores": [("Noche", "#070708", "Fondo principal", 64), ("Hueso", "#EEE8DE", "Texto y titulares", 18), ("Humo", "#1A1A1F", "Superficies y filetes", 10),
                    ("Ámbar tungsteno", "#FFB648", "Acento único: luz, cifras, estados", 6), ("Azul escena", "#3D5AFE", "Uso puntual en foto", 2)],
        "tipos": [("Cormorant Garamond", "Display · titulares, nombres, cifras", "400 · 500 · Itálica", "'Cormorant Garamond', serif", "Esteban Guillen"),
                  ("Manrope", "Texto · párrafos, navegación, botones", "400 · 500 · 600", "Manrope, sans-serif", "Diseño, video y fotografía en vivo."),
                  ("DM Mono", "Datos · etiquetas, hora, contadores", "400 · mayúsculas +6%", "'DM Mono', monospace", "MIAMI 22:18 · 1,3M+ VISTAS")],
        "escala": [("Display", "clamp(4.2rem, 15.5vw, 16.5rem)", "0.82", "Cormorant 400"), ("H1", "9.5rem", "0.86", "Cormorant 400"), ("H2", "4.8rem", "0.95", "Cormorant 400 / itálica"),
                   ("Resumen", "3.2rem", "1.06", "Cormorant 400"), ("Texto", "1.0625rem", "1.6", "Manrope 400"), ("Etiqueta", "0.75rem", "1.2", "DM Mono · mayúsculas")],
        "reticula": "12 columnas · margen lateral 4vw (16–64 px) · ancho máximo 1600 px · canal 20–36 px",
        "elementos": [("Haz de luz", "El cursor es un foco. En el hero se dibuja un cono que baja desde arriba hasta el puntero y revela la foto."),
                      ("Grano de película", "Ruido fino al 7 % animado a 4 cuadros por segundo sobre toda la página."),
                      ("Filete ámbar", "Una línea de 18 px antecede a cada etiqueta en mono. Es la firma mínima de la línea."),
                      ("Setlist numerado", "Los proyectos se listan como canciones: número, título en serif, disciplina y cifra en ámbar.")],
        "foto": ["Negros profundos: el escenario debe leerse oscuro, nunca gris.", "Respetar el color real de la luz de escena; no agregar filtros de color.",
                 "Preferir contraluces, humo y siluetas frente al público.", "Encuadres amplios con el público en primer plano para dar escala."],
        "movimiento": [("Foco WebGL", "Shader propio: la luz sigue al cursor con inercia 0,07 y deriva sola si nadie lo mueve.", "Continuo"),
                       ("Cortina", "Telón negro que sube con una línea ámbar al cambiar de página.", "1,0 s · expo.inOut"),
                       ("Palabras que suben", "Los titulares entran palabra por palabra desde una máscara.", "1,3 s · expo.out · 0,06 s"),
                       ("Manifiesto iluminado", "Cada palabra pasa de 14 % a 100 % de opacidad al hacer scroll.", "Ligado al scroll"),
                       ("Setlist", "Al pasar por un título aparece la portada del proyecto siguiendo al cursor.", "0,6 s · power3"),
                       ("Galería en vivo", "La sección se fija y las fotos avanzan en horizontal con parallax interno.", "Ligado al scroll"),
                       ("Scroll suave", "Lenis con interpolación 0,085 para un desplazamiento de cine.", "Continuo")],
        "incorrectos": ["Cambiar el ámbar por otro color", "Poner el logotipo sobre fotos claras sin contraste", "Deformar o comprimir el wordmark", "Usar la serif en texto corrido pequeño"],
    },
    "matchday": {
        "titulo": "MATCHDAY", "sub": "Línea gráfica 02 · Diseño deportivo, video y fotografía",
        "fuentes": "family=Anton&family=Archivo:wdth,wght@62..125,400..900&family=Space+Mono",
        "bg": "#eceae4", "fg": "#0c0c0c", "acc": "#e4002b", "mut": "#6f6c66", "lin": "#0c0c0c", "sup": "#e0ddd5",
        "fd": "Anton, Impact, sans-serif", "ft": "Archivo, sans-serif", "fm": "'Space Mono', monospace",
        "d_peso": "400", "d_trk": "0", "d_case": "uppercase", "d_italic": False,
        "concepto": [
            "MATCHDAY nace de los afiches de partido que Esteban diseñó para Universitario, Sport Huancayo y la selección femenina de Perú.",
            "La identidad se comporta como un día de partido: rojo de camiseta, papel de afiche con semitono, tipografía condensada que ocupa todo el ancho y diagonales que dan velocidad.",
            "Es la línea más enérgica: para clubes, marcas deportivas y campañas que necesitan impacto inmediato.",
        ],
        "origen": [("nahomi-martinez", "03.jpg", "Nahomi Martínez"), ("luis-benites", "05.jpg", "Luis Benites"), ("matchdays", "02.jpg", "Matchday's 2022–23")],
        "colores": [("Papel", "#ECEAE4", "Fondo de afiche", 46), ("Negro tinta", "#0C0C0C", "Texto, bloques, sombras duras", 26), ("Rojo camiseta", "#E4002B", "Color de marca", 20),
                    ("Amarillo fixture", "#FFD60A", "Ticker, números, llamadas", 6), ("Granate", "#7A1F2B", "Uso de apoyo", 2)],
        "tipos": [("Anton", "Display · titulares, nombres, cifras", "400 · siempre en mayúsculas", "Anton, sans-serif", "ESTEBAN GUILLEN"),
                  ("Archivo", "Texto y etiquetas · ancho variable 62–125", "400 – 900 · ancho 62 para etiquetas", "Archivo, sans-serif", "Diseño que entra a la cancha."),
                  ("Space Mono", "Datos técnicos", "400", "'Space Mono', monospace", "2023 · Photoshop, Illustrator")],
        "escala": [("Display", "clamp(4.6rem, 12.5vw, 13rem)", "0.84", "Anton"), ("H2", "8.5rem", "0.84", "Anton"), ("Cifra", "8rem", "0.85", "Anton"),
                   ("Subtítulo", "2.2rem", "1.0", "Anton"), ("Texto", "1.0625rem", "1.55", "Archivo 500"), ("Etiqueta", "0.875rem", "1.2", "Archivo 800 · ancho 62 · mayúsculas")],
        "reticula": "Bloques a sangre · margen 3,6vw (16–56 px) · ancho máximo 1680 px · diagonales a 18°",
        "elementos": [("Escudo EG", "Escudo con franja diagonal. MMXX = 2020, año de debut de Esteban en Behance. El dorsal #20 sale del mismo año."),
                      ("Diagonal 18°", "Franjas, barridos y cortes de sección siempre a 18 grados, como las piezas de Universitario."),
                      ("Semitono y rasgado", "Puntos de 5 px sobre todo el papel y bordes rasgados para cerrar bloques."),
                      ("Sombra dura", "Desplazamiento negro de 0,08 em sin difuminar en titulares y tarjetas.")],
        "foto": ["Jugador recortado sobre fondos de color plano o texturas.", "Movimiento: patadas, celebraciones, saltos; nunca poses estáticas.",
                 "Contraste alto y saturación del color del club.", "El nombre del jugador puede repetirse como textura de fondo."],
        "movimiento": [("Intro de partido", "MATCHDAY golpea letra por letra, vibra y se rasga hacia arriba.", "≈2,4 s · back.out(2)"),
                       ("Barrido diagonal", "Tres franjas (amarillo, rojo, negro) cruzan la pantalla al cambiar de página.", "0,75 s · expo.inOut"),
                       ("Golpe de texto", "Los titulares caen desde escala 2,4 con giro y la página tiembla al llegar.", "0,55 s · back.out(1.7)"),
                       ("Marquesinas", "El nombre en contorno se mueve más rápido cuanto más rápido se hace scroll.", "Ligado a la velocidad"),
                       ("Abanico 3D", "Cinco afiches se abren en abanico y se inclinan con el cursor.", "1,1 s · expo.out"),
                       ("Marcador odómetro", "Cada dígito rueda como un marcador de estadio.", "1,6 s + 0,25 s por dígito"),
                       ("Carrusel y cromos", "Afiches arrastrables con inercia; los cromos giran 180° para mostrar el dorso.", "0,8 s")],
        "incorrectos": ["Usar Anton en minúsculas", "Cambiar la diagonal de 18°", "Rellenar el escudo con degradados", "Sumar más de dos colores de acento"],
    },
    "estudio": {
        "titulo": "ESTUDIO", "sub": "Línea gráfica 03 · Branding, redes y web",
        "fuentes": "family=Geist:wght@300;400;500;600;700&family=Geist+Mono",
        "bg": "#f2f2ef", "fg": "#111111", "acc": "#ff4d1c", "mut": "#8a8a86", "lin": "#d6d6d1", "sup": "#e8e8e4",
        "fd": "Geist, Helvetica, sans-serif", "ft": "Geist, Helvetica, sans-serif", "fm": "'Geist Mono', monospace",
        "d_peso": "600", "d_trk": "-0.06em", "d_case": "none", "d_italic": False,
        "concepto": [
            "ESTUDIO nace de los sistemas de marca de Esteban: Qatar 2022, Physo y Zena Coffee. Piezas que funcionan porque repiten una estructura clara.",
            "La identidad es un estudio editorial suizo: papel blanco, tinta negra y un único naranja señal, todo alineado a una retícula de 12 columnas que se puede mostrar en la web con la tecla G.",
            "Es la línea más corporativa: para agencias, marcas y equipos que contratan a un diseñador por su criterio y su orden.",
        ],
        "origen": [("qatar-2022", "04.jpg", "Qatar 2022"), ("physo", "01.jpg", "Physo"), ("zena-coffee", "01.jpg", "Zena Coffee")],
        "colores": [("Papel", "#F2F2EF", "Fondo", 62), ("Tinta", "#111111", "Texto y bloques", 26), ("Línea", "#D6D6D1", "Filetes y divisiones", 6),
                    ("Gris", "#8A8A86", "Metadatos", 4), ("Naranja señal", "#FF4D1C", "Acento único", 2)],
        "tipos": [("Geist", "Display y texto · una sola familia", "300 – 700 · display 600 con -6 % de interletra", "Geist, sans-serif", "Esteban Guillen"),
                  ("Geist Mono", "Numeración, metadatos, hora", "400 · mayúsculas", "'Geist Mono', monospace", "02 — ÍNDICE · 22:33:53 EST")],
        "escala": [("Display", "clamp(4.4rem, 15.8vw, 18rem)", "0.80", "Geist 600 · -6,5 %"), ("H1", "10rem", "0.86", "Geist 600 · -6 %"), ("H2", "6.4rem", "0.90", "Geist 500 · -5,5 %"),
                   ("Resumen", "3rem", "1.05", "Geist 500 · -4,5 %"), ("Texto", "1rem", "1.5", "Geist 400"), ("Metadato", "0.75rem", "1.3", "Geist Mono · mayúsculas")],
        "reticula": "12 columnas · canal 20 px · margen 2,6vw (16–40 px) · todo empieza en una columna",
        "elementos": [("Retícula visible", "Las 12 columnas se dibujan al entrar y pueden mostrarse con la tecla G: el sistema queda a la vista."),
                      ("Numeración", "Cada sección y página tiene número (01 — Inicio, 02 — Índice). Ordena y sirve de navegación."),
                      ("Paleta medida", "Cada proyecto muestra sus 5 colores reales, medidos de las piezas publicadas."),
                      ("Cuadrado señal", "Un cuadrado naranja de 1/8 del logo marca el punto de atención.")],
        "foto": ["Imágenes completas, sin recortes forzados: la pieza es la protagonista.", "Fondos limpios y luz uniforme para fotografía de producto o personas.",
                 "El retrato va en blanco y negro sobre naranja y recupera su color al pasar el cursor.", "Las páginas largas de web se muestran desde arriba."],
        "movimiento": [("Panel numerado", "Al cambiar de página sube un panel negro con el número y el nombre de destino.", "0,8 s · expo.inOut"),
                       ("Retícula que se dibuja", "Las 12 columnas bajan una tras otra al entrar.", "1,0 s · 0,04 s entre columnas"),
                       ("Texto por líneas", "Cada línea sube desde una máscara.", "1,2 s · expo.out · 0,07 s"),
                       ("Visor WebGL", "Las portadas pasan con una disolución de ruido y un borde naranja.", "1,3 s · cada 4,2 s"),
                       ("Índice desplegable", "Al pasar por un proyecto se abre una tira con sus piezas.", "0,6 s · expo.out"),
                       ("Lista ↔ cuadrícula", "La misma colección cambia de diseño con Flip, sin cortes.", "0,9 s · expo.inOut"),
                       ("Rodillo", "Los enlaces grandes cambian de texto girando hacia arriba.", "0,55 s")],
        "incorrectos": ["Añadir un segundo color de acento", "Salir de la retícula de 12 columnas", "Usar Geist con interletra positiva en titulares", "Centrar los textos largos"],
    },
}


# --------------------------------------------------------------------------------------------
def logo_html(linea, modo="pos", tam=1.0):
    """modo: pos (sobre fondo de la línea), neg (invertido), mono (un color), mini (solo símbolo)."""
    L = LINEAS[linea]
    if linea == "luz":
        col = {"pos": L["fg"], "neg": L["bg"], "mono": L["acc"], "mini": L["fg"]}[modo]
        sim = f"""<svg viewBox="0 0 64 64" style="width:{90 * tam}px;height:{90 * tam}px;color:{col}"><path d="M32 2 L40 12 H24 Z" fill="currentColor"/><circle cx="32" cy="38" r="23" fill="none" stroke="currentColor" stroke-width="1.6"/><text x="32" y="47" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-weight="500" font-size="27" fill="currentColor">eg</text></svg>"""
        if modo == "mini":
            return sim
        return f"""<div style="display:flex;align-items:center;gap:{24 * tam}px;color:{col}">{sim}<span style="font-family:'Cormorant Garamond';font-size:{86 * tam}px;line-height:1;letter-spacing:-0.02em">Esteban <i style="color:{L['acc'] if modo == 'pos' else col}">Guillen</i></span></div>"""
    if linea == "matchday":
        rojo = {"pos": "#e4002b", "neg": "#e4002b", "mono": "#0c0c0c", "mini": "#e4002b"}[modo]
        tx = {"pos": "#0c0c0c", "neg": "#eceae4", "mono": "#0c0c0c", "mini": "#0c0c0c"}[modo]
        franja = "#eceae4" if modo != "mono" else "#eceae4"
        sim = f"""<svg viewBox="0 0 80 92" style="width:{100 * tam}px;height:{115 * tam}px"><path d="M40 2 L76 12 V44 C76 68 60 82 40 90 C20 82 4 68 4 44 V12 Z" fill="{rojo}" stroke="{tx}" stroke-width="3"/><path d="M4 58 L76 26 V36 L4 68 Z" fill="{franja}"/><text x="40" y="48" text-anchor="middle" font-family="Anton" font-size="30" fill="#0c0c0c">EG</text><text x="40" y="80" text-anchor="middle" font-family="Archivo" font-weight="800" font-size="7" fill="#eceae4" letter-spacing="1.5">MMXX</text></svg>"""
        if modo == "mini":
            return sim
        return f"""<div style="display:flex;align-items:center;gap:{22 * tam}px;color:{tx}">{sim}<span style="display:flex;flex-direction:column;font-family:Anton;line-height:.86"><small style="font-family:Archivo;font-weight:800;font-stretch:62%;font-size:{18 * tam}px;letter-spacing:.3em;color:{'#ffd60a' if modo == 'neg' else rojo}">ESTEBAN</small><span style="font-size:{96 * tam}px">GUILLEN</span></span></div>"""
    col = {"pos": "#111111", "neg": "#f2f2ef", "mono": "#111111", "mini": "#111111"}[modo]
    fondo = {"pos": "#f2f2ef", "neg": "#111111", "mono": "#f2f2ef", "mini": "#f2f2ef"}[modo]
    punto = "#ff4d1c" if modo != "mono" else fondo
    sim = f"""<svg viewBox="0 0 48 48" style="width:{96 * tam}px;height:{96 * tam}px"><rect width="48" height="48" fill="{col}"/><text x="24" y="31.5" text-anchor="middle" font-family="Geist" font-weight="700" font-size="20" letter-spacing="-1" fill="{fondo}">EG</text><rect x="34" y="8" width="6" height="6" fill="{punto}"/></svg>"""
    if modo == "mini":
        return sim
    return f"""<div style="display:flex;align-items:center;gap:{22 * tam}px;color:{col}">{sim}<span style="font-family:Geist;font-weight:600;font-size:{70 * tam}px;letter-spacing:-0.055em;line-height:.95">Esteban<br>Guillen</span></div>"""


def manual(linea, capturas):
    L = LINEAS[linea]
    cap = lambda n: "file://" + os.path.join(capturas, f"{linea}_{n}.jpg")
    disp = f"font-family:{L['fd']};font-weight:{L['d_peso']};letter-spacing:{L['d_trk']};text-transform:{L['d_case']}"
    paginas = []

    def pag(n, titulo, cuerpo, clase=""):
        paginas.append(f"""<section class="pg {clase}"><header class="pg-cab"><span>{e(D.NOMBRE)} — {L['titulo']}</span><span>{n:02d} · {e(titulo)}</span></header>{cuerpo}</section>""")

    # 1 Portada
    paginas.append(f"""<section class="pg portada">
  <div class="port-img" style="background-image:url('{foto(*L['origen'][0][:2])}')"></div>
  <div class="port-txt">
    <p class="mono">Manual de línea gráfica · Noviembre 2026</p>
    <h1 style="{disp}">{L['titulo']}</h1>
    <p class="port-sub">{e(L['sub'])}</p>
    <div class="port-logo">{logo_html(linea, 'neg' if linea != 'luz' else 'pos', .8)}</div>
  </div>
</section>""")
    # 2 Índice
    secciones = ["Concepto", "Logotipo", "Construcción", "Versiones", "Color", "Tipografía", "Retícula", "Elementos gráficos",
                 "Fotografía", "Movimiento", "Web · escritorio", "Web · móvil y páginas", "Aplicaciones", "Usos incorrectos"]
    pag(2, "Índice", f"""<div class="indice"><h2 style="{disp}">Contenido</h2><ol>{''.join(f'<li><span class="mono">{i + 3:02d}</span>{s}</li>' for i, s in enumerate(secciones))}</ol></div>""")
    # 3 Concepto
    ori = "".join(f'<figure><img src="{foto(s, n)}"><figcaption class="mono">{e(t)} · Behance</figcaption></figure>' for s, n, t in L["origen"])
    pag(3, "Concepto", f"""<div class="concepto"><div><p class="mono">De dónde sale</p><h2 style="{disp}">{L['titulo'].capitalize() if L['d_case'] == 'none' else L['titulo']}</h2>{''.join(f'<p>{e(t)}</p>' for t in L['concepto'])}</div><div class="origen">{ori}</div></div>""")
    # 4 Logotipo
    pag(4, "Logotipo", f"""<div class="logo-grande">{logo_html(linea, 'pos', 1.9)}</div><p class="nota-pie">Logotipo principal: símbolo + nombre. Se usa en la cabecera de la web, portadas y firmas.</p>""", "centrada")
    # 5 Construcción
    pag(5, "Construcción", f"""<div class="construccion"><div class="cons-caja"><div class="cons-grid"></div><div class="cons-zona"></div>{logo_html(linea, 'pos', 1.4)}</div>
<ul class="lista"><li><b>Unidad X</b> = altura del símbolo ÷ 4.</li><li><b>Área de protección</b>: 1X libre alrededor del logotipo (línea discontinua).</li><li><b>Tamaño mínimo</b>: 120 px de ancho en pantalla · 30 mm en impresión. El símbolo solo: 24 px · 8 mm.</li><li>El símbolo y el nombre mantienen siempre la misma proporción.</li></ul></div>""")
    # 6 Versiones
    pag(6, "Versiones", f"""<div class="versiones">
<div class="ver" style="background:{L['bg']}">{logo_html(linea, 'pos', .7)}<span class="mono">Principal · sobre fondo de marca</span></div>
<div class="ver" style="background:{L['fg']}">{logo_html(linea, 'neg', .7)}<span class="mono" style="color:{L['bg']}">Negativo</span></div>
<div class="ver" style="background:{L['acc'] if linea != 'luz' else L['fg']}">{logo_html(linea, 'mono', .7)}<span class="mono" style="color:{L['bg'] if linea == 'luz' else '#0c0c0c'}">Una tinta</span></div>
<div class="ver" style="background:{L['sup']}">{logo_html(linea, 'mini', 1.2)}<span class="mono">Símbolo · favicon, avatar, marca de agua</span></div></div>""")
    # 7 Color
    total = "".join(f'<span style="flex:{p};background:{h}"></span>' for _, h, _, p in L["colores"])
    sw = "".join(f"""<div class="sw"><span class="sw-c" style="background:{h}"></span><b>{e(n)}</b><span class="mono">HEX {h}<br>RGB {rgb(h)}<br>CMYK {cmyk(h)}</span><span class="sw-uso">{e(u)} · {p} %</span></div>""" for n, h, u, p in L["colores"])
    pag(7, "Color", f"""<div class="color"><div class="swatches">{sw}</div><p class="mono">Proporción de uso</p><div class="proporcion">{total}</div></div>""")
    # 8 Tipografía
    tp = "".join(f"""<div class="tipo"><p class="mono">{e(r)} · {e(p)}</p><p class="tipo-n" style="font-family:{f}">{e(n)}</p><p class="tipo-m" style="font-family:{f}">{e(m)}</p><p class="tipo-abc" style="font-family:{f}">Aa Bb Cc Ññ 0123456789 ¿?!</p></div>""" for n, r, p, f, m in L["tipos"])
    esc = "".join(f'<tr><td>{e(a)}</td><td class="mono">{e(b)}</td><td class="mono">{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in L["escala"])
    pag(8, "Tipografía", f"""<div class="tipografia"><div class="tipos">{tp}</div><table class="escala"><thead><tr><th class="mono">Nivel</th><th class="mono">Tamaño</th><th class="mono">Interlínea</th><th class="mono">Familia</th></tr></thead><tbody>{esc}</tbody></table></div>""")
    # 9 Retícula
    pag(9, "Retícula", f"""<div class="reticula-p"><div class="ret-demo"><img src="{cap('index_d')}"><div class="ret-cols">{''.join('<i></i>' for _ in range(12))}</div></div><div><h2 style="{disp}">12 columnas</h2><p>{e(L['reticula'])}</p><p>Todos los bloques empiezan y terminan en una columna. En móvil la retícula pasa a una columna con el mismo margen lateral mínimo de 16 px.</p></div></div>""")
    # 10 Elementos
    el = "".join(f'<div class="elem"><span class="mono">{i + 1:02d}</span><h3 style="{disp}">{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(L["elementos"]))
    pag(10, "Elementos gráficos", f'<div class="elementos">{el}</div><div class="elem-img"><img src="{cap("index3_d" if linea == "estudio" else "index2_d")}"></div>')
    # 11 Fotografía
    imgs = "".join(f'<img src="{foto(s, n)}">' for s, n, _ in L["origen"])
    pag(11, "Fotografía", f"""<div class="fotografia"><div class="foto-imgs">{imgs}</div><ul class="lista">{''.join(f'<li>{e(x)}</li>' for x in L['foto'])}</ul></div>""")
    # 12 Movimiento
    mv = "".join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td class="mono">{e(c)}</td></tr>' for a, b, c in L["movimiento"])
    pag(12, "Movimiento", f"""<div class="movimiento"><div><h2 style="{disp}">La web se mueve así</h2><p>Todos los efectos están escritos a mano con GSAP, Lenis y WebGL propio. Ninguno es una plantilla: cada uno sale de un oficio que Esteban practica. Con «reducir movimiento» activado, la web se muestra sin animaciones.</p></div><table class="mov">{mv}</table></div>""")
    # 13 Web escritorio
    pag(13, "Web · escritorio", f"""<div class="web-d"><div class="nav-sim"><img src="{cap('index_d')}"></div><div class="web-d-2"><img src="{cap('index3_d')}"><img src="{cap('trabajo_d')}"></div></div>""")
    # 14 Web móvil + páginas
    tel = "".join(f'<div class="tel"><img src="{cap(n + "_m")}"></div>' for n in ["index", "trabajo", D.PROYECTOS[0]["slug"] if False else ("mercyme" if linea == "luz" else "luis-benites" if linea == "matchday" else "qatar-2022")])
    pag(14, "Web · móvil y páginas", f"""<div class="web-m"><div class="tels">{tel}</div><div class="web-m-d"><img src="{cap(('mercyme' if linea == 'luz' else 'luis-benites' if linea == 'matchday' else 'qatar-2022') + '_d')}"><img src="{cap('sobre_d')}"><p class="mono">16 páginas por web: inicio, trabajo, 12 proyectos, sobre mí y contacto.</p></div></div>""")
    # 15 Aplicaciones
    pag(15, "Aplicaciones", aplicaciones(linea, disp))
    # 16 Usos incorrectos
    inc = []
    for i, t in enumerate(L["incorrectos"]):
        estilo = ["filter:hue-rotate(160deg)", "opacity:.35", "transform:scaleX(1.5) scaleY(.75)", "filter:blur(1.5px)"][i]
        fondo = [L["bg"], "#cfcfcf" if linea == "luz" else "#777", L["bg"], L["bg"]][i]
        inc.append(f'<div class="inc"><div class="inc-caja" style="background:{fondo}"><div style="{estilo}">{logo_html(linea, "pos", .55)}</div><span class="x">×</span></div><p>{e(t)}</p></div>')
    pag(16, "Usos incorrectos", f'<div class="incorrectos">{"".join(inc)}</div>')
    # 17 Contraportada
    paginas.append(f"""<section class="pg contra"><div>{logo_html(linea, 'neg' if linea != 'luz' else 'pos', 1.0)}</div><div class="contra-datos"><p>{e(D.CORREO)}</p><p>behance.net/estebanguimi</p><p>{e(D.INSTAGRAM_T)}</p><p class="mono">{e(D.CIUDAD)} · 2026</p></div></section>""")

    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{L['titulo']} · Manual de línea gráfica</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{L['fuentes']}&display=swap">
<style>{css(L, linea)}</style></head><body>{''.join(paginas)}</body></html>"""


def aplicaciones(linea, disp):
    L = LINEAS[linea]
    p = {"luz": D.por_slug("mercyme"), "matchday": D.por_slug("nahomi-martinez"), "estudio": D.por_slug("qatar-2022")}[linea]
    img = foto(p["slug"], p["portada"])
    tarjeta_f = f'<div class="tarj" style="background:{L["bg"]};color:{L["fg"]}">{logo_html(linea, "pos", .6)}</div>'
    tarjeta_d = f"""<div class="tarj tarj-d" style="background:{L['acc'] if linea != 'estudio' else L['fg']};color:{'#0c0c0c' if linea != 'estudio' else L['bg']}">
<b style="{disp};font-size:30px">{e(D.NOMBRE)}</b><span>Diseño · Video · Fotografía</span><span class="mono" style="color:inherit">{e(D.CORREO)}<br>behance.net/estebanguimi<br>{e(D.CIUDAD)}</span></div>"""
    post = f"""<div class="post" style="background:{L['bg']};color:{L['fg']}"><div class="post-img" style="background-image:url('{img}')"></div>
<div class="post-txt"><span class="mono" style="color:{L['acc']}">Nuevo proyecto</span><b style="{disp};font-size:46px;line-height:.9;{'font-style:italic' if L['d_italic'] else ''}">{e(p['corto'])}</b><span class="mono">{e(D.CATEGORIAS[p['cat']])} · {e(p['cifra'])} {e(p['cifra_t'])}</span></div></div>"""
    portada = f"""<div class="bh" style="background:{L['bg']};color:{L['fg']}"><div class="bh-img" style="background-image:url('{foto(*LINEAS[linea]['origen'][1][:2])}')"></div>
<div class="bh-txt"><b style="{disp};font-size:50px;line-height:.86;{'font-style:italic' if L['d_italic'] else ''}">Esteban Guillen</b><span class="mono" style="color:{L['acc']}">Diseño · Video · Fotografía en vivo — Miami</span></div></div>"""
    firma = f"""<div class="firma" style="background:#fff;color:#111"><div style="transform:scale(.55);transform-origin:left center;width:200px;height:60px;display:flex;align-items:center">{logo_html(linea, 'mini', .6)}</div>
<div><b>{e(D.NOMBRE)}</b><br><span>Diseñador, editor de video y fotógrafo</span><br><span style="color:{L['acc'] if linea != 'luz' else '#b07a1f'}">{e(D.CORREO)}</span> · behance.net/estebanguimi</div></div>"""
    return f"""<div class="apps"><div class="app"><div class="tarjetas">{tarjeta_f}{tarjeta_d}</div><p class="mono">Tarjeta de presentación · 85 × 55 mm</p></div>
<div class="app">{post}<p class="mono">Publicación de Instagram · 1080 × 1350</p></div>
<div class="app app-ancha">{portada}<p class="mono">Portada de perfil · Behance y LinkedIn</p></div>
<div class="app app-ancha">{firma}<p class="mono">Firma de correo</p></div></div>"""


def css(L, linea):
    return f"""
@page {{ size: 1920px 1080px; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: {L['bg']}; }}
body {{ font-family: {L['ft']}; color: {L['fg']}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
img {{ display: block; max-width: 100%; }}
h1, h2, h3, p {{ margin: 0; }}
.mono {{ font-family: {L['fm']}; font-size: 15px; text-transform: uppercase; letter-spacing: .06em; color: {L['mut']}; }}
.pg {{ width: 1920px; height: 1080px; overflow: hidden; position: relative; padding: 120px 110px 90px; page-break-after: always; break-after: page; background: {L['bg']}; }}
.pg-cab {{ position: absolute; top: 44px; left: 110px; right: 110px; display: flex; justify-content: space-between; font-family: {L['fm']}; font-size: 15px; text-transform: uppercase; letter-spacing: .06em; color: {L['mut']}; border-bottom: 1px solid {L['lin']}; padding-bottom: 14px; }}
.pg h2 {{ font-size: 110px; line-height: .9; margin-bottom: 36px; {'font-style: italic;' if L['d_italic'] else ''} }}
.pg p {{ font-size: 24px; line-height: 1.5; }}
.portada {{ padding: 0; display: grid; grid-template-columns: 1fr 1fr; }}
.port-img {{ background-size: cover; background-position: center; {'filter: brightness(.85);' if linea == 'luz' else ''} }}
.port-txt {{ padding: 110px; display: flex; flex-direction: column; justify-content: space-between; background: {L['bg'] if linea == 'luz' else (L['acc'] if linea == 'matchday' else L['fg'])}; color: {L['fg'] if linea == 'luz' else L['bg']}; }}
.port-txt .mono {{ color: inherit; opacity: .8; }}
.port-txt h1 {{ font-size: {260 if linea != 'matchday' else 220}px; line-height: .82; {'font-style: italic; color:' + L['acc'] + ';' if L['d_italic'] else ''} }}
.port-sub {{ font-size: 30px !important; max-width: 20ch; }}
.indice {{ display: grid; grid-template-columns: 1fr 1.3fr; gap: 80px; padding-top: 60px; }}
.indice ol {{ list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 60px; }}
.indice li {{ font-size: 32px; padding: 18px 0; border-bottom: 1px solid {L['lin']}; display: flex; gap: 22px; align-items: baseline; break-inside: avoid; }}
.indice li .mono {{ color: {L['acc']}; }}
.concepto {{ display: grid; grid-template-columns: 1fr 1.25fr; gap: 80px; padding-top: 40px; height: 100%; }}
.concepto > div:first-child {{ display: grid; gap: 22px; align-content: start; }}
.concepto p {{ font-size: 26px; max-width: 34ch; }}
.origen {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 18px; }}
.origen figure {{ margin: 0; display: grid; gap: 10px; align-content: start; }}
.origen img {{ width: 100%; height: 700px; object-fit: cover; }}
.centrada {{ display: grid; place-items: center; }}
.logo-grande {{ padding: 100px; }}
.nota-pie {{ position: absolute; bottom: 70px; left: 110px; color: {L['mut']}; }}
.construccion {{ display: grid; grid-template-columns: 1.4fr 1fr; gap: 70px; align-items: center; height: 100%; }}
.cons-caja {{ position: relative; padding: 90px; border: 1px solid {L['lin']}; display: grid; place-items: center; height: 640px; }}
.cons-grid {{ position: absolute; inset: 0; background-image: linear-gradient({L['acc']}33 1px, transparent 1px), linear-gradient(90deg, {L['acc']}33 1px, transparent 1px); background-size: 40px 40px; }}
.cons-zona {{ position: absolute; inset: 60px; border: 2px dashed {L['acc']}; }}
.cons-caja > div:last-child {{ position: relative; }}
.lista {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 0; }}
.lista li {{ font-size: 25px; line-height: 1.45; padding: 18px 0; border-bottom: 1px solid {L['lin']}; }}
.versiones {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 100%; }}
.ver {{ display: grid; place-items: center; position: relative; border: 1px solid {L['lin']}; }}
.ver .mono {{ position: absolute; left: 22px; bottom: 18px; }}
.color {{ display: grid; gap: 22px; padding-top: 40px; }}
.swatches {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 18px; }}
.sw {{ display: grid; gap: 10px; align-content: start; }}
.sw-c {{ height: 430px; border: 1px solid {L['lin']}; }}
.sw b {{ font-size: 28px; }}
.sw .mono {{ line-height: 1.5; color: {L['fg']}; opacity: .8; }}
.sw-uso {{ font-size: 19px; color: {L['mut']}; }}
.proporcion {{ display: flex; height: 60px; border: 1px solid {L['lin']}; }}
.tipografia {{ display: grid; grid-template-columns: 1.3fr 1fr; gap: 60px; padding-top: 30px; }}
.tipos {{ display: grid; gap: 26px; align-content: start; }}
.tipo {{ border-top: 1px solid {L['lin']}; padding-top: 16px; display: grid; gap: 6px; }}
.tipo-n {{ font-size: 64px !important; line-height: 1 !important; }}
.tipo-m {{ font-size: 34px !important; line-height: 1.1 !important; }}
.tipo-abc {{ font-size: 22px !important; color: {L['mut']}; }}
.escala {{ width: 100%; border-collapse: collapse; align-self: start; }}
.escala th {{ text-align: left; padding: 12px 12px 12px 0; border-bottom: 2px solid {L['fg']}; }}
.escala td {{ padding: 16px 8px 16px 0; border-bottom: 1px solid {L['lin']}; font-size: 22px; }}
.reticula-p {{ display: grid; grid-template-columns: 1.6fr 1fr; gap: 60px; align-items: center; height: 100%; }}
.reticula-p p {{ margin-bottom: 18px; }}
.ret-demo {{ position: relative; }}
.ret-demo img {{ width: 100%; border: 1px solid {L['lin']}; }}
.ret-cols {{ position: absolute; inset: 0 3.6%; display: grid; grid-template-columns: repeat(12, 1fr); gap: 1.4%; }}
.ret-cols i {{ background: {L['acc']}26; border-left: 1px solid {L['acc']}99; border-right: 1px solid {L['acc']}99; }}
.elementos {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 26px; padding-top: 24px; }}
.elem {{ border-top: 2px solid {L['fg']}; padding-top: 16px; display: grid; gap: 12px; align-content: start; }}
.elem .mono {{ color: {L['acc']}; }}
.elem h3 {{ font-size: 44px; line-height: .95; {'font-style: italic;' if L['d_italic'] else ''} }}
.elem p {{ font-size: 21px; }}
.elem-img {{ margin-top: 34px; height: 420px; overflow: hidden; border: 1px solid {L['lin']}; }}
.elem-img img {{ width: 100%; }}
.fotografia {{ display: grid; grid-template-columns: 1.5fr 1fr; gap: 60px; height: 100%; }}
.foto-imgs {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }}
.foto-imgs img {{ width: 100%; height: 100%; object-fit: cover; }}
.movimiento {{ display: grid; grid-template-columns: 1fr 1.5fr; gap: 70px; padding-top: 30px; }}
.movimiento h2 {{ font-size: 90px; }}
.mov {{ border-collapse: collapse; width: 100%; }}
.mov td {{ padding: 16px 14px 16px 0; border-bottom: 1px solid {L['lin']}; font-size: 20px; vertical-align: top; line-height: 1.4; }}
.mov td:first-child {{ width: 26%; font-size: 23px; }}
.mov td:last-child {{ width: 24%; color: {L['acc']}; }}
.web-d {{ display: grid; grid-template-columns: 1.55fr 1fr; gap: 24px; height: 100%; }}
.web-d img, .web-m-d img {{ width: 100%; border: 1px solid {L['lin']}; box-shadow: 0 30px 60px -30px rgba(0,0,0,.5); }}
.nav-sim {{ align-self: center; }}
.web-d-2 {{ display: grid; gap: 24px; align-content: center; }}
.web-m {{ display: grid; grid-template-columns: 1.2fr 1fr; gap: 50px; height: 100%; align-items: center; }}
.tels {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; }}
.tel {{ border: 12px solid #111; border-radius: 44px; overflow: hidden; background: #111; aspect-ratio: 390 / 844; }}
.tel img {{ width: 100%; height: 100%; object-fit: cover; object-position: top; }}
.web-m-d {{ display: grid; gap: 22px; }}
.apps {{ display: grid; grid-template-columns: 1.25fr 1fr 1.1fr; grid-template-rows: auto auto; gap: 26px 40px; padding-top: 20px; }}
.app {{ display: grid; gap: 12px; align-content: start; }}
.app-ancha {{ grid-column: 3; }}
.apps .app:nth-child(1) {{ grid-row: 1 / 3; }}
.apps .app:nth-child(2) {{ grid-row: 1 / 3; }}
.tarjetas {{ display: grid; gap: 22px; }}
.tarj {{ width: 100%; aspect-ratio: 85 / 55; display: grid; place-items: center; box-shadow: 0 24px 50px -24px rgba(0,0,0,.6); border: 1px solid {L['lin']}; }}
.tarj-d {{ place-items: start; align-content: space-between; padding: 30px; display: grid; gap: 8px; }}
.tarj-d span {{ font-size: 18px; }}
.post {{ aspect-ratio: 4 / 5; display: grid; grid-template-rows: 1fr auto; box-shadow: 0 24px 50px -24px rgba(0,0,0,.6); border: 1px solid {L['lin']}; }}
.post-img {{ background-size: cover; background-position: center; }}
.post-txt {{ padding: 24px; display: grid; gap: 10px; }}
.bh {{ aspect-ratio: 3.2 / 1; position: relative; overflow: hidden; display: grid; align-items: end; border: 1px solid {L['lin']}; }}
.bh-img {{ position: absolute; inset: 0 0 0 58%; background-size: cover; background-position: center; }}
.bh-txt {{ position: relative; padding: 24px; display: grid; gap: 8px; max-width: 58%; }}
.firma {{ padding: 22px; display: flex; gap: 6px; align-items: center; font-family: Arial, sans-serif; font-size: 17px; line-height: 1.5; border: 1px solid {L['lin']}; }}
.incorrectos {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 26px; padding-top: 60px; }}
.inc {{ display: grid; gap: 16px; }}
.inc-caja {{ height: 480px; display: grid; place-items: center; position: relative; border: 1px solid {L['lin']}; overflow: hidden; }}
.inc-caja .x {{ position: absolute; top: 12px; right: 18px; font-size: 64px; line-height: 1; color: #e5322d; font-family: Arial, sans-serif; }}
.inc p {{ font-size: 23px; }}
.contra {{ display: flex; flex-direction: column; justify-content: space-between; background: {L['bg'] if linea == 'luz' else (L['acc'] if linea == 'matchday' else L['fg'])}; color: {L['fg'] if linea == 'luz' else L['bg']}; }}
.contra-datos p {{ font-size: 34px; }}
.contra-datos .mono {{ color: inherit; opacity: .75; margin-top: 18px; }}
"""


def imprimir(html_path, pdf_path):
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1920,height:1080}}}});
await p.goto('file://{html_path}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
await p.pdf({{path:'{pdf_path}',width:'1920px',height:'1080px',printBackground:true,preferCSSPageSize:true}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)


if __name__ == "__main__":
    capturas = os.path.abspath(sys.argv[1])
    salida = os.path.join(RAIZ, "manuales")
    os.makedirs(salida, exist_ok=True)
    for i, linea in enumerate(["luz", "matchday", "estudio"], 1):
        html = manual(linea, capturas)
        hp = os.path.join(capturas, f"manual_{linea}.html")
        open(hp, "w", encoding="utf-8").write(html)
        pdf = os.path.join(salida, f"0{i}-{linea}-manual-linea-grafica.pdf")
        imprimir(hp, pdf)
        print("ok", pdf)
