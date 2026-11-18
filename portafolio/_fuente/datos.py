# -*- coding: utf-8 -*-
"""Contenido del portafolio: proyectos, perfil y currículum de Esteban Guillen.

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
INSTAGRAM = "https://www.instagram.com/estebanguimi_official/"
INSTAGRAM_T = "@estebanguimi_official"
DESDE = "2020"
DISPONIBLE = "Disponible como autónomo y a tiempo completo"

BIO = (
    "Diseñador gráfico y editor de video con base en Miami. Edito y grabo video para campañas políticas en "
    "Harris Media Group, fotografío conciertos y diseño piezas deportivas y de marca. Más de 1,3 millones de vistas en mis videos."
)
BIO_LARGA = [
    "Empecé en 2018 como diseñador gráfico en Perú: logotipos, anuncios y contenido semanal para Soporte Total GUIMI, "
    "Arturo's Burger y Digitalia TEC. Ahí aprendí a trabajar con fechas fijas y a diseñar para que una pieza venda.",
    "Entre 2022 y 2024 trabajé por mi cuenta: matchdays para Universitario, Sport Huancayo y la selección femenina, "
    "la cobertura del Mundial Qatar 2022, el contenido de Physo, la tienda de Zena Coffee y overlays para streaming.",
    "Hoy estoy en Miami. En Harris Media Group edito, animo y grabo video para campañas en EE. UU. "
    "(Sam Gallucci, NH Senate Republicans, Bobby Charles) y además fotografío conciertos de MercyMe, Crowder y for KING & COUNTRY.",
]

# Currículum. Fechas y descripciones salen del currículum publicado y del perfil de Harris Media Group.
PUESTO = "Editor de video y videógrafo · Diseñador gráfico"
ANOS = "8"  # años de experiencia desde 2018
CV_RESUMEN = (
    "Diseñador gráfico y editor de video con 8 años de experiencia. Edito, animo y grabo video para campañas "
    "políticas en EE. UU. (más de 1,3 millones de vistas), diseño sistemas de piezas para redes y marcas, "
    "y hago fotografía de conciertos. Trabajo rápido, con fechas fijas y pensando en resultados."
)
EXPERIENCIA = [
    {"puesto": "Editor de video y videógrafo", "empresa": "Harris Media Group", "lugar": "Miami, FL · EE. UU.",
     "fechas": "2025 — hoy", "inicio": 2025, "fin": 2026,
     "puntos": ["Edición, motion graphics y grabación de video para campañas políticas en EE. UU.",
                "Sam Gallucci y NH Senate Republicans: más de 900K vistas.",
                "Bobby Charles for Maine Governor: 436K+ vistas, más de 20 piezas y 20K+ interacciones."],
     "proyectos": ["gallucci", "bobby-charles"]},
    {"puesto": "Fotógrafo de conciertos", "empresa": "Independiente", "lugar": "Florida · EE. UU.",
     "fechas": "2025 — hoy", "inicio": 2025, "fin": 2026,
     "puntos": ["Cobertura en vivo y edición de MercyMe, Crowder y for KING & COUNTRY.",
                "60 fotografías entregadas en tres conciertos."],
     "proyectos": ["mercyme", "crowder", "for-king-country"]},
    {"puesto": "Diseñador gráfico independiente", "empresa": "Clubes, jugadores y marcas", "lugar": "Lima · Perú",
     "fechas": "2022 — 2024", "inicio": 2022, "fin": 2024,
     "puntos": ["Matchdays y piezas de jugador para Universitario, Sport Huancayo, Nahomi Martínez y Luis Benites.",
                "Sistema de 37 piezas para la cobertura del Mundial Qatar 2022.",
                "Redes de Physo, landing y tienda de Zena Coffee y overlays para streaming."],
     "proyectos": ["matchdays", "nahomi-martinez", "luis-benites", "qatar-2022", "physo", "zena-coffee", "valorant"]},
    {"puesto": "Diseñador gráfico", "empresa": "Digitalia TEC", "lugar": "Perú",
     "fechas": "feb. 2022 — jul. 2022", "inicio": 2022, "fin": 2022,
     "puntos": ["Anuncios para promocionar los productos y la marca de la empresa."], "proyectos": []},
    {"puesto": "Diseñador gráfico", "empresa": "Arturo's Burger", "lugar": "Perú",
     "fechas": "ene. 2020 — jul. 2022", "inicio": 2020, "fin": 2022,
     "puntos": ["Piezas para redes, promociones y publicidad del restaurante."], "proyectos": []},
    {"puesto": "Diseñador gráfico", "empresa": "Soporte Total GUIMI S.A.", "lugar": "Perú",
     "fechas": "mar. 2018 — jul. 2022", "inicio": 2018, "fin": 2022,
     "puntos": ["Diseño del logotipo y de los anuncios de la empresa."], "proyectos": []},
]
HABILIDADES = [
    ("Video", ["Edición", "Motion graphics", "Grabación", "Versiones para redes", "Subtítulos y rótulos"]),
    ("Diseño gráfico", ["Identidad y logotipos", "Piezas para redes", "Publicidad", "Diseño deportivo", "Sistemas de plantillas"]),
    ("Fotografía", ["Conciertos y eventos en vivo", "Edición y revelado", "Selección y entrega"]),
    ("Web y streaming", ["Diseño de interfaces en Figma", "WordPress", "Dominios y hosting", "Overlays para OBS Studio"]),
]
HERRAMIENTAS = ["Premiere Pro", "After Effects", "Photoshop", "Illustrator", "Lightroom", "Figma", "WordPress", "OBS Studio", "Office"]
IDIOMAS = [("Español", "Nativo"), ("Inglés", "Intermedio")]
CIFRAS = [("1,3M+", "vistas en video político"), ("12", "proyectos destacados"), ("196", "piezas publicadas"), ("8", "años de experiencia")]
CV_PDF = "esteban-guillen-cv.pdf"

SERVICIOS = [
    ("Video para campañas", "Edición, motion y versiones para redes de candidatos y causas."),
    ("Fotografía en vivo", "Conciertos y eventos: cobertura completa y entrega editada."),
    ("Diseño deportivo", "Matchdays, fixtures, anuncios de fichaje y piezas de jugador."),
    ("Branding y redes", "Sistemas visuales para marcas y contenido mensual."),
    ("Web y UI", "Landing pages y tiendas diseñadas en Figma."),
]

ROLES = {
    "video": "Edición, motion graphics y grabación",
    "foto": "Fotografía y revelado",
    "deporte": "Diseño gráfico",
    "marca": "Diseño gráfico y sistema para redes",
    "web": "Diseño de interfaz",
    "gaming": "Diseño de overlays",
}

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
        "slug": "gallucci", "cliente": "Harris Media Group · Sam Gallucci y NH Senate Republicans", "titulo": "Sam Gallucci & NH Senate Republicans", "corto": "Sam Gallucci",
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
        "slug": "bobby-charles", "cliente": "Harris Media Group · Bobby Charles for Maine Governor", "titulo": "Bobby Charles for Maine Governor", "corto": "Bobby Charles",
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
        "slug": "mercyme", "cliente": "MercyMe · gira 2025", "titulo": "MercyMe 2025", "corto": "MercyMe",
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
        "slug": "crowder", "cliente": "Crowder · concierto", "titulo": "Crowder Live", "corto": "Crowder",
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
        "slug": "for-king-country", "cliente": "for KING & COUNTRY · concierto", "titulo": "for KING & COUNTRY", "corto": "for KING & COUNTRY",
        "cat": "foto", "ano": "2026", "cifra": "16", "cifra_t": "fotografías",
        "herr": ["Lightroom", "Photoshop"], "portada": "06.jpg",
        "resumen": "Fotografía del concierto de for KING & COUNTRY.",
        "texto": [
            "Movimiento, contraluz y público: la banda en el escenario y entre la gente.",
            "Tratamiento con grano fino y tonos apagados para que la luz de escena sea la protagonista.",
        ],
        "datos": [("16", "fotografías"), ("B/N + color", "tratamiento"), ("Live", "concierto")],
    },
    {
        "slug": "matchdays", "cliente": "Clubes del fútbol peruano", "titulo": "Matchday's 2022–23", "corto": "Matchday's",
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
        "slug": "nahomi-martinez", "cliente": "Nahomi Martínez · futbolista", "titulo": "Nahomi Martínez Matchday's", "corto": "Nahomi Martínez",
        "cat": "deporte", "ano": "2023", "cifra": "16", "cifra_t": "afiches",
        "herr": ["Photoshop", "Illustrator"], "portada": "03.jpg",
        "resumen": "Serie de matchdays para Nahomi Martínez, jugadora de Universitario y de la selección peruana.",
        "texto": [
            "Una temporada completa contada en afiches verticales: crema y granate de Universitario, rojo de la selección.",
            "Texturas de mármol líquido, collage de recortes y tipografía que envuelve a la jugadora.",
        ],
        "datos": [("16", "afiches"), ("2", "camisetas: club y selección"), ("2022–23", "temporada")],
    },
    {
        "slug": "luis-benites", "cliente": "Luis Benites · Sport Huancayo", "titulo": "Luis Benites Matchday's", "corto": "Luis Benites",
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
        "slug": "qatar-2022", "cliente": "Cobertura del Mundial para redes", "titulo": "Qatar 2022", "corto": "Qatar 2022",
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
        "slug": "physo", "cliente": "Physo · Santiago de Surco, Lima", "titulo": "Physo · Centro de fisioterapia", "corto": "Physo",
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
        "slug": "zena-coffee", "cliente": "Café Zena", "titulo": "Zena Coffee Store", "corto": "Zena Coffee",
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
        "slug": "valorant", "cliente": "Transmisiones en Twitch", "titulo": "Overlays Valorant Multicolor", "corto": "Valorant",
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

