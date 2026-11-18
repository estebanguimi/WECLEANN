# -*- coding: utf-8 -*-
"""Portfolio content: projects, profile and résumé of Esteban Guillen.

Edit here and run:  python3 _fuente/construir.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
MEDIDAS = json.load(open(os.path.join(os.path.dirname(AQUI), "img", "medidas.json")))

NOMBRE = "Esteban Guillen"
NOMBRE_CORTO = "Guillen"
ROL = "Designer, video editor and photographer"
CIUDAD = "Miami, FL"
ORIGEN = "Peru"
CORREO = "estebanguimi@gmail.com"
INSTAGRAM = "https://www.instagram.com/estebanguimi_official/"
INSTAGRAM_T = "@estebanguimi_official"
DESDE = "2020"
DISPONIBLE = "Available for full-time and freelance work"

BIO = (
    "Graphic designer and video editor based in Miami. I edit and shoot video for political campaigns at "
    "Harris Media Group, photograph concerts and design sports and brand content. My videos have passed 1.3 million views."
)
BIO_LARGA = [
    "I started in 2018 as a graphic designer in Peru, making logos, ads and weekly content for Soporte Total GUIMI, "
    "Arturo's Burger and Digitalia TEC. That is where I learned to work to fixed deadlines and to design pieces that sell.",
    "From 2022 to 2024 I worked freelance: matchday posters for Universitario, Sport Huancayo and the Peru women's national team, "
    "social coverage of the Qatar 2022 World Cup, content for Physo, the Zena Coffee online store and streaming overlays.",
    "Today I am based in Miami. At Harris Media Group I edit, animate and shoot video for U.S. campaigns "
    "(Sam Gallucci, NH Senate Republicans, Bobby Charles), and I also photograph concerts for MercyMe, Crowder and for KING & COUNTRY.",
]

# Résumé. Dates and descriptions come from the published résumé and the Harris Media Group profile.
PUESTO = "Video Editor & Videographer · Graphic Designer"
ANOS = "8"  # years of experience since 2018
CV_RESUMEN = (
    "Graphic designer and video editor with 8 years of experience. I edit, animate and shoot video for U.S. "
    "political campaigns (1.3M+ views), design content systems for social media and brands, "
    "and photograph live concerts. I work fast, to fixed deadlines, with results in mind."
)
EXPERIENCIA = [
    {"puesto": "Video Editor & Videographer", "empresa": "Harris Media Group", "lugar": "Miami, FL · USA",
     "fechas": "2025 — Present", "inicio": 2025, "fin": 2026,
     "puntos": ["Video editing, motion graphics and filming for U.S. political campaigns.",
                "Sam Gallucci and NH Senate Republicans: 900K+ views.",
                "Bobby Charles for Maine Governor: 436K+ views, 20+ pieces and 20K+ engagements."],
     "proyectos": ["gallucci", "bobby-charles"]},
    {"puesto": "Concert Photographer", "empresa": "Freelance", "lugar": "Florida · USA",
     "fechas": "2025 — Present", "inicio": 2025, "fin": 2026,
     "puntos": ["Live coverage and editing for MercyMe, Crowder and for KING & COUNTRY.",
                "60 photographs delivered across three concerts."],
     "proyectos": ["mercyme", "crowder", "for-king-country"]},
    {"puesto": "Freelance Graphic Designer", "empresa": "Clubs, players and brands", "lugar": "Lima · Peru",
     "fechas": "2022 — 2024", "inicio": 2022, "fin": 2024,
     "puntos": ["Matchday and player graphics for Universitario, Sport Huancayo, Nahomi Martínez and Luis Benites.",
                "A 37-piece content system for the Qatar 2022 World Cup.",
                "Social media for Physo, landing page and store for Zena Coffee, and streaming overlays."],
     "proyectos": ["matchdays", "nahomi-martinez", "luis-benites", "qatar-2022", "physo", "zena-coffee", "valorant"]},
    {"puesto": "Graphic Designer", "empresa": "Digitalia TEC", "lugar": "Peru",
     "fechas": "Feb 2022 — Jul 2022", "inicio": 2022, "fin": 2022,
     "puntos": ["Ads promoting the company's products and brand."], "proyectos": []},
    {"puesto": "Graphic Designer", "empresa": "Arturo's Burger", "lugar": "Peru",
     "fechas": "Jan 2020 — Jul 2022", "inicio": 2020, "fin": 2022,
     "puntos": ["Social media content, promotions and advertising for the restaurant."], "proyectos": []},
    {"puesto": "Graphic Designer", "empresa": "Soporte Total GUIMI S.A.", "lugar": "Peru",
     "fechas": "Mar 2018 — Jul 2022", "inicio": 2018, "fin": 2022,
     "puntos": ["Designed the company logo and its advertising."], "proyectos": []},
]
HABILIDADES = [
    ("Video", ["Editing", "Motion graphics", "Filming", "Social cut-downs", "Captions and titles"]),
    ("Graphic design", ["Identity and logos", "Social media content", "Advertising", "Sports design", "Template systems"]),
    ("Photography", ["Concerts and live events", "Editing and color grading", "Selection and delivery"]),
    ("Web and streaming", ["UI design in Figma", "WordPress", "Domains and hosting", "OBS Studio overlays"]),
]
HERRAMIENTAS = ["Premiere Pro", "After Effects", "Photoshop", "Illustrator", "Lightroom", "Figma", "WordPress", "OBS Studio", "Office"]
IDIOMAS = [("Spanish", "Native"), ("English", "Intermediate")]
CIFRAS = [("1.3M+", "views on political video"), ("12", "featured projects"), ("196", "published pieces"), ("8", "years of experience")]
CV_PDF = "esteban-guillen-cv.pdf"

SERVICIOS = [
    ("Campaign video", "Editing, motion and social cut-downs for candidates and causes."),
    ("Live photography", "Concerts and events: full coverage, edited and delivered."),
    ("Sports design", "Matchday posters, fixtures, signing announcements and player graphics."),
    ("Branding and social", "Visual systems for brands and monthly content."),
    ("Web and UI", "Landing pages and online stores designed in Figma."),
]

ROLES = {
    "video": "Editing, motion graphics and filming",
    "foto": "Photography and editing",
    "deporte": "Graphic design",
    "marca": "Graphic design and social media system",
    "web": "Interface design",
    "gaming": "Overlay design",
}

CATEGORIAS = {
    "video": "Political video",
    "foto": "Live photography",
    "deporte": "Sports design",
    "marca": "Branding and social",
    "web": "Web and UI",
    "gaming": "Gaming",
}

PROYECTOS = [
    {
        "slug": "gallucci", "cliente": "Harris Media Group · Sam Gallucci and NH Senate Republicans", "titulo": "Sam Gallucci & NH Senate Republicans", "corto": "Sam Gallucci",
        "cat": "video", "ano": "2026", "cifra": "900K+", "cifra_t": "views",
        "herr": ["Premiere Pro", "After Effects"], "portada": "00.jpg",
        "resumen": "Video content for Sam Gallucci's campaign and the New Hampshire Senate Republicans.",
        "texto": [
            "Short social videos with big titles, a fast pace and one message per video.",
            "Two streams of work: Sam Gallucci's videos, with 209K views in Ventura County, and contrast content "
            "for NH Senate Republicans, with 607K views.",
        ],
        "datos": [("209K", "views · Sam Gallucci"), ("607K", "views · NH Senate Republicans"), ("900K+", "total views")],
        "video": True,
    },
    {
        "slug": "bobby-charles", "cliente": "Harris Media Group · Bobby Charles for Maine Governor", "titulo": "Bobby Charles for Maine Governor", "corto": "Bobby Charles",
        "cat": "video", "ano": "2026", "cifra": "436K+", "cifra_t": "views",
        "herr": ["Photoshop", "Premiere Pro", "After Effects"], "portada": "00.jpg",
        "resumen": "Video, motion and social design for Bobby Charles's campaign for Governor of Maine.",
        "texto": [
            "A campaign look in navy, red and white: short lines in condensed type, "
            "portraits of the candidate and direct comparisons.",
            "More than twenty video and graphic pieces: Cut crime, Cut taxes, Not a career politician and The choice is clear.",
        ],
        "datos": [("436K+", "video views"), ("20+", "pieces produced"), ("20K+", "social engagements")],
        "video": True,
    },
    {
        "slug": "mercyme", "cliente": "MercyMe · 2025 tour", "titulo": "MercyMe 2025", "corto": "MercyMe",
        "cat": "foto", "ano": "2026", "cifra": "22", "cifra_t": "photos",
        "herr": ["Lightroom", "Photoshop"], "portada": "19.jpg",
        "resumen": "Concert photography of MercyMe on their 2025 tour.",
        "texto": [
            "From the acoustic set under warm light to the confetti finale: the whole night in a single series.",
            "Edited in Lightroom for deep blacks while keeping the color of every lighting cue.",
        ],
        "datos": [("22", "photos"), ("2025", "tour"), ("Live", "concert")],
    },
    {
        "slug": "crowder", "cliente": "Crowder · concert", "titulo": "Crowder Live", "corto": "Crowder",
        "cat": "foto", "ano": "2026", "cifra": "22", "cifra_t": "photos",
        "herr": ["Lightroom", "Photoshop"], "portada": "17.jpg",
        "resumen": "Concert photography of Crowder.",
        "texto": [
            "The series follows the show's lighting changes: amber, red, blue and a black-and-white ending.",
            "The lyrics projected on screen stay inside the frame and become part of the photo.",
        ],
        "datos": [("22", "photos"), ("4", "lighting moods"), ("B&W", "finale")],
    },
    {
        "slug": "for-king-country", "cliente": "for KING & COUNTRY · concert", "titulo": "for KING & COUNTRY", "corto": "for KING & COUNTRY",
        "cat": "foto", "ano": "2026", "cifra": "16", "cifra_t": "photos",
        "herr": ["Lightroom", "Photoshop"], "portada": "06.jpg",
        "resumen": "Concert photography of for KING & COUNTRY.",
        "texto": [
            "Movement, backlight and crowd: the band on stage and among the audience.",
            "Fine grain and muted tones so the stage lighting takes the lead.",
        ],
        "datos": [("16", "photos"), ("B&W + color", "treatment"), ("Live", "concert")],
    },
    {
        "slug": "matchdays", "cliente": "Peruvian football clubs", "titulo": "Matchday's 2022–23", "corto": "Matchday's",
        "cat": "deporte", "ano": "2023", "cifra": "22", "cifra_t": "posters",
        "herr": ["Photoshop", "Illustrator"], "portada": "02.jpg",
        "resumen": "Match posters, fixtures and player graphics for Peruvian football in the 2022–23 season.",
        "texto": [
            "Universitario, Alianza Lima, Sport Huancayo, Sporting Cristal, Atlético Grau and the Peru women's national team.",
            "Every poster chases a different idea: an F1 podium, a Polaroid collage, fire, pink skies or a red-and-white diagonal.",
        ],
        "datos": [("22", "posters"), ("6+", "clubs"), ("2022–23", "season")],
    },
    {
        "slug": "nahomi-martinez", "cliente": "Nahomi Martínez · footballer", "titulo": "Nahomi Martínez Matchday's", "corto": "Nahomi Martínez",
        "cat": "deporte", "ano": "2023", "cifra": "16", "cifra_t": "posters",
        "herr": ["Photoshop", "Illustrator"], "portada": "03.jpg",
        "resumen": "A matchday series for Nahomi Martínez, who plays for Universitario and the Peru national team.",
        "texto": [
            "A full season told in vertical posters: Universitario's cream and maroon, the national team's red.",
            "Liquid marble textures, cutout collage and type that wraps around the player.",
        ],
        "datos": [("16", "posters"), ("2", "kits: club and country"), ("2022–23", "season")],
    },
    {
        "slug": "luis-benites", "cliente": "Luis Benites · Sport Huancayo", "titulo": "Luis Benites Matchday's", "corto": "Luis Benites",
        "cat": "deporte", "ano": "2023", "cifra": "15", "cifra_t": "posters",
        "herr": ["Photoshop", "Illustrator"], "portada": "05.jpg",
        "resumen": "Matchday posters for Luis Benites, Sport Huancayo's number 21.",
        "texto": [
            "All red: the player's name repeated as a texture, diagonals and composites with the Copa Libertadores.",
            "A piece for every match of the 2022–23 season, from Estadio Huancayo to the Libertadores.",
        ],
        "datos": [("15", "posters"), ("21", "shirt number"), ("2022–23", "season")],
    },
    {
        "slug": "qatar-2022", "cliente": "World Cup social media coverage", "titulo": "Qatar 2022", "corto": "Qatar 2022",
        "cat": "marca", "ano": "2022", "cifra": "37", "cifra_t": "pieces",
        "herr": ["Photoshop", "Illustrator"], "portada": "04.jpg",
        "resumen": "A social media content system for the FIFA World Cup Qatar 2022.",
        "texto": [
            "Groups, venues, line-ups, results and the final bracket, all in one maroon system.",
            "Diamond-shaped flags, big scores and match photography, ready to publish on the day of each game.",
        ],
        "datos": [("37", "pieces"), ("8", "venues"), ("32", "national teams")],
    },
    {
        "slug": "physo", "cliente": "Physo · Santiago de Surco, Lima", "titulo": "Physo · Physical therapy center", "corto": "Physo",
        "cat": "marca", "ano": "2024", "cifra": "30", "cifra_t": "posts",
        "herr": ["Photoshop", "Figma"], "portada": "02.jpg",
        "resumen": "Social media content for Physo, a physical therapy center in Santiago de Surco, Lima.",
        "texto": [
            "Orange, midnight blue and cream: a system that explains methods, assessment steps and exercises.",
            "The center's own photography with clear labels: stretching, flexibility, strength and virtual reality.",
        ],
        "datos": [("30", "posts"), ("5", "assessment steps"), ("3", "brand colors")],
    },
    {
        "slug": "zena-coffee", "cliente": "Café Zena", "titulo": "Zena Coffee Store", "corto": "Zena Coffee",
        "cat": "web", "ano": "2024", "cifra": "2", "cifra_t": "screens",
        "herr": ["Photoshop", "Figma"], "portada": "01.jpg",
        "resumen": "Landing page and online store for Café Zena.",
        "texto": [
            "A style guide with colors taken from four coffee roasts and a classic serif typeface.",
            "A landing page with the brand's story and a store with filters by type of coffee.",
        ],
        "datos": [("2", "screens"), ("4", "coffee tones"), ("Figma", "design")],
    },
    {
        "slug": "valorant", "cliente": "Twitch streams", "titulo": "Valorant Multicolor Overlays", "corto": "Valorant",
        "cat": "gaming", "ano": "2022", "cifra": "3", "cifra_t": "screens",
        "herr": ["Photoshop"], "portada": "02.jpg",
        "resumen": "An overlay pack for Valorant streams.",
        "texto": [
            "Starting screen, in-game scene with camera and chat, and a waiting screen.",
            "Black background with brush strokes and color accents on the edges.",
        ],
        "datos": [("3", "scenes"), ("16:9", "format"), ("Twitch", "use")],
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

