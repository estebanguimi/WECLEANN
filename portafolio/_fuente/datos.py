# -*- coding: utf-8 -*-
"""Contenido del portafolio, tomado de behance.net/estebanguimi.

Edita aquí y ejecuta:  python3 _fuente/construir.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
MEDIDAS = json.load(open(os.path.join(os.path.dirname(AQUI), "img", "medidas.json")))

NOMBRE = "Esteban Guillen"
NOMBRE_CORTO = "Guillen"
ROL = "Diseñador, editor de video y fotógrafo"
CIUDAD = "Miami, FL"
ORIGEN = "Perú"
CORREO = "estebanguimi@gmail.com"
BEHANCE = "https://www.behance.net/estebanguimi"
INSTAGRAM = "https://www.instagram.com/estebanguimi_official/"
INSTAGRAM_T = "@estebanguimi_official"
DESDE = "2020"
DISPONIBLE = "Disponible como autónomo y a tiempo completo"

BIO = (
    "Diseñador y editor de video en Miami. Hago contenido político que supera el millón de vistas, "
    "fotografía conciertos en vivo y diseño piezas deportivas para clubes y jugadoras del fútbol peruano."
)
BIO_LARGA = [
    "Empecé como diseñador gráfico en Perú, en Digitalia TEC, Arturo's Burger y Soporte Total GUIMI. "
    "Ahí aprendí lo que pide el día a día: piezas para redes cada semana, fechas que no se mueven y clientes que necesitan resultados.",
    "En el fútbol encontré mi lenguaje: matchdays, fixtures y piezas de jugador para Universitario, Sport Huancayo, "
    "Alianza Lima y la selección femenina. Collage, textura, tipografía gigante y una sola idea fuerte por afiche.",
    "Hoy trabajo en Miami entre el video y la cámara. Edito campañas políticas que suman más de 1,3 millones de vistas "
    "y fotografío conciertos de MercyMe, Crowder y for KING & COUNTRY.",
]
EXPERIENCIA = [
    ("Video y diseño político", "Campañas en EE. UU.", "2025 — hoy"),
    ("Fotografía de conciertos", "Giras en Florida", "2025 — hoy"),
    ("Diseñador gráfico", "Digitalia TEC · Perú", ""),
    ("Diseñador gráfico", "Arturo's Burger · Perú", ""),
    ("Diseñador gráfico", "Soporte Total GUIMI · Perú", ""),
]
HERRAMIENTAS = ["Photoshop", "Illustrator", "Lightroom", "Premiere Pro", "After Effects", "Figma"]

SERVICIOS = [
    ("Video para campañas", "Edición, motion y versiones para redes de candidatos y causas."),
    ("Fotografía en vivo", "Conciertos y eventos: cobertura completa y entrega editada."),
    ("Diseño deportivo", "Matchdays, fixtures, anuncios de fichaje y piezas de jugador."),
    ("Branding y redes", "Sistemas visuales para marcas y contenido mensual."),
    ("Web y UI", "Landing pages y tiendas diseñadas en Figma."),
]

CATEGORIAS = {
    "video": "Video político",
    "foto": "Fotografía en vivo",
    "deporte": "Diseño deportivo",
    "marca": "Branding y redes",
    "web": "Web y UI",
    "gaming": "Gaming",
}

PROYECTOS = [
    {
        "slug": "gallucci", "behance": "258616689/Sam-Gallucci-NH-Senate-republicans-900K-Views",
        "titulo": "Sam Gallucci & NH Senate Republicans", "corto": "Sam Gallucci",
        "cat": "video", "ano": "2026", "cifra": "900K+", "cifra_t": "vistas",
        "herr": ["Premiere Pro", "After Effects"], "portada": "00.jpg",
        "resumen": "Contenido de video para la campaña de Sam Gallucci y los republicanos del Senado de New Hampshire.",
        "texto": [
            "Piezas cortas para redes con rótulos grandes, ritmo rápido y un mensaje por video.",
            "Dos líneas de trabajo: los videos de Sam Gallucci, con 209K vistas en Ventura County, y el contenido "
            "de contraste para NH Senate Republicans, con 607K vistas.",
        ],
        "datos": [("209K", "vistas · Sam Gallucci"), ("607K", "vistas · NH Senate Republicans"), ("900K+", "vistas en total")],
        "video": True,
    },
    {
        "slug": "bobby-charles", "behance": "258610673/Bobby-Charles-Political-content-436k-views",
        "titulo": "Bobby Charles for Maine Governor", "corto": "Bobby Charles",
        "cat": "video", "ano": "2026", "cifra": "436K+", "cifra_t": "vistas",
        "herr": ["Photoshop", "Premiere Pro", "After Effects"], "portada": "00.jpg",
        "resumen": "Video, motion y diseño para redes de la campaña de Bobby Charles a gobernador de Maine.",
        "texto": [
            "Una línea gráfica de campaña en azul marino, rojo y blanco: frases cortas en tipografía condensada, "
            "retratos del candidato y comparaciones directas.",
            "Más de veinte piezas producidas entre video y gráficas: Cut crime, Cut taxes, Not a career politician y The choice is clear.",
        ],
        "datos": [("436K+", "vistas de video"), ("+20", "piezas producidas"), ("20K+", "interacciones en redes")],
        "video": True,
    },
    {
        "slug": "mercyme", "behance": "248361057/Mercyme-2025-Live-Concert-Photography",
        "titulo": "MercyMe 2025", "corto": "MercyMe",
        "cat": "foto", "ano": "2026", "cifra": "22", "cifra_t": "fotografías",
        "herr": ["Lightroom", "Photoshop"], "portada": "19.jpg",
        "resumen": "Fotografía del concierto de MercyMe en su gira 2025.",
        "texto": [
            "Del set acústico con luces cálidas al cierre con confeti: la noche completa en una sola serie.",
            "Edición en Lightroom buscando negros profundos y conservando el color de cada momento de luz.",
        ],
        "datos": [("22", "fotografías"), ("2025", "gira"), ("Live", "concierto")],
    },
    {
        "slug": "crowder", "behance": "248194803/CROWDER-Live-Concert-Photography",
        "titulo": "Crowder Live", "corto": "Crowder",
        "cat": "foto", "ano": "2026", "cifra": "22", "cifra_t": "fotografías",
        "herr": ["Lightroom", "Photoshop"], "portada": "17.jpg",
        "resumen": "Fotografía del concierto de Crowder.",
        "texto": [
            "La serie sigue los cambios de luz del show: ámbar, rojo, azul y un final en blanco y negro.",
            "Las letras proyectadas en pantalla quedan dentro del encuadre y se vuelven parte de la foto.",
        ],
        "datos": [("22", "fotografías"), ("4", "atmósferas de luz"), ("B/N", "cierre")],
    },
    {
        "slug": "for-king-country", "behance": "248012185/For-King-Country-Live-Concert-Photography",
        "titulo": "for KING & COUNTRY", "corto": "for KING & COUNTRY",
        "cat": "foto", "ano": "2026", "cifra": "16", "cifra_t": "fotografías",
        "herr": ["Lightroom", "Photoshop"], "portada": "06.jpg",
        "resumen": "Fotografía del concierto de for KING & COUNTRY.",
        "texto": [
            "Movimiento, contraluz y público: la banda en el escenario y entre la gente.",
            "Tratamiento con grano fino y tonos apagados para que la luz de escena sea la protagonista.",
        ],
        "datos": [("16", "fotografías"), ("61", "visualizaciones en Behance"), ("Live", "concierto")],
    },
    {
        "slug": "matchdays", "behance": "176711337/Matchdays-2022-23",
        "titulo": "Matchday's 2022–23", "corto": "Matchday's",
        "cat": "deporte", "ano": "2023", "cifra": "22", "cifra_t": "afiches",
        "herr": ["Photoshop", "Illustrator"], "portada": "02.jpg",
        "resumen": "Afiches de partido, fixtures y piezas de jugador para el fútbol peruano en la temporada 2022–23.",
        "texto": [
            "Universitario, Alianza Lima, Sport Huancayo, Sporting Cristal, Atlético Grau y la selección femenina de Perú.",
            "Cada afiche busca una idea distinta: un podio de F1, un collage de Polaroids, fuego, cielos rosados o una diagonal roja y blanca.",
        ],
        "datos": [("22", "afiches"), ("6+", "clubes"), ("2022–23", "temporada")],
    },
    {
        "slug": "nahomi-martinez", "behance": "173785229/Nahomi-Martinez-Matchdays",
        "titulo": "Nahomi Martínez Matchday's", "corto": "Nahomi Martínez",
        "cat": "deporte", "ano": "2023", "cifra": "16", "cifra_t": "afiches",
        "herr": ["Photoshop", "Illustrator"], "portada": "03.jpg",
        "resumen": "Serie de matchdays para Nahomi Martínez, jugadora de Universitario y de la selección peruana.",
        "texto": [
            "Una temporada completa contada en afiches verticales: crema y granate de Universitario, rojo de la selección.",
            "Texturas de mármol líquido, collage de recortes y tipografía que envuelve a la jugadora.",
        ],
        "datos": [("16", "afiches"), ("67", "visualizaciones en Behance"), ("2022–23", "temporada")],
    },
    {
        "slug": "luis-benites", "behance": "176681361/Luis-Benites-Matchdays",
        "titulo": "Luis Benites Matchday's", "corto": "Luis Benites",
        "cat": "deporte", "ano": "2023", "cifra": "15", "cifra_t": "afiches",
        "herr": ["Photoshop", "Illustrator"], "portada": "05.jpg",
        "resumen": "Matchdays para Luis Benites, el número 21 de Sport Huancayo.",
        "texto": [
            "Rojo total: el nombre del jugador repetido como textura, diagonales y montajes con la Copa Libertadores.",
            "Piezas para cada partido de la temporada 2022–23, desde el Estadio Huancayo hasta Libertadores.",
        ],
        "datos": [("15", "afiches"), ("21", "dorsal"), ("2022–23", "temporada")],
    },
    {
        "slug": "qatar-2022", "behance": "159083101/QATAR-2022-branding",
        "titulo": "Qatar 2022", "corto": "Qatar 2022",
        "cat": "marca", "ano": "2022", "cifra": "37", "cifra_t": "piezas",
        "herr": ["Photoshop", "Illustrator"], "portada": "04.jpg",
        "resumen": "Sistema de piezas para redes durante la Copa Mundial de la FIFA Qatar 2022.",
        "texto": [
            "Grupos, sedes, alineaciones, resultados y cuadro final con un mismo sistema en granate.",
            "Banderas en rombo, marcadores grandes y fotografía de partido para publicar el mismo día de cada juego.",
        ],
        "datos": [("37", "piezas"), ("8", "sedes"), ("32", "selecciones")],
    },
    {
        "slug": "physo", "behance": "192119917/Physiotherapy-Center-Social-Media",
        "titulo": "Physo · Centro de fisioterapia", "corto": "Physo",
        "cat": "marca", "ano": "2024", "cifra": "30", "cifra_t": "publicaciones",
        "herr": ["Photoshop", "Figma"], "portada": "02.jpg",
        "resumen": "Contenido para redes de Physo, un centro de fisioterapia en Santiago de Surco, Lima.",
        "texto": [
            "Naranja, azul noche y crema: un sistema que explica métodos, pasos de evaluación y ejercicios.",
            "Fotografía propia del centro con etiquetas claras: estiramiento, flexibilidad, fuerza y realidad virtual.",
        ],
        "datos": [("30", "publicaciones"), ("5", "pasos de evaluación"), ("3", "colores de marca")],
    },
    {
        "slug": "zena-coffee", "behance": "214200871/Landing-page-for-Zena-Coffee-Store",
        "titulo": "Zena Coffee Store", "corto": "Zena Coffee",
        "cat": "web", "ano": "2024", "cifra": "2", "cifra_t": "pantallas",
        "herr": ["Photoshop", "Figma"], "portada": "01.jpg",
        "resumen": "Landing page y tienda para Café Zena.",
        "texto": [
            "Guía de estilo con colores tomados de cuatro tonos de café y una tipografía serif clásica.",
            "Landing con la historia de la marca y una tienda con filtros por tipo de café.",
        ],
        "datos": [("2", "pantallas"), ("4", "tonos de café"), ("Figma", "diseño")],
    },
    {
        "slug": "valorant", "behance": "141295547/Overlays-Valorant-Multicolor",
        "titulo": "Overlays Valorant Multicolor", "corto": "Valorant",
        "cat": "gaming", "ano": "2022", "cifra": "3", "cifra_t": "pantallas",
        "herr": ["Photoshop"], "portada": "02.jpg",
        "resumen": "Paquete de overlays para transmisiones de Valorant.",
        "texto": [
            "Pantalla de inicio, escena de juego con cámara y chat, y pantalla de espera.",
            "Fondo negro con trazos de pincel y acentos de color en los bordes.",
        ],
        "datos": [("3", "escenas"), ("16:9", "formato"), ("Twitch", "uso")],
    },
]


def imagenes(slug):
    return MEDIDAS[slug]


def por_slug(s):
    return next(p for p in PROYECTOS if p["slug"] == s)


def siguiente(s):
    i = [p["slug"] for p in PROYECTOS].index(s)
    return PROYECTOS[(i + 1) % len(PROYECTOS)]


def anterior(s):
    i = [p["slug"] for p in PROYECTOS].index(s)
    return PROYECTOS[i - 1]


def url_behance(p):
    return "https://www.behance.net/gallery/" + p["behance"]
