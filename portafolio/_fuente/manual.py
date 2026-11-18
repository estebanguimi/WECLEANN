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
        "titulo": "SPOTLIGHT", "sub": "Brand identity 01 · Live photography, video and design",
        "fuentes": "family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Manrope:wght@400;500;600&family=DM+Mono",
        "bg": "#070708", "fg": "#eee8de", "acc": "#ffb648", "mut": "#8d8a85", "lin": "#2a2a31", "sup": "#121216",
        "fd": "'Cormorant Garamond', serif", "ft": "Manrope, sans-serif", "fm": "'DM Mono', monospace",
        "d_peso": "400", "d_trk": "-0.035em", "d_case": "none", "d_italic": True,
        "port_bg": "#070708", "port_fg": "#eee8de", "logo_port": "pos", "port_tam": 170, "proy": "mercyme", "post": "mercyme", "mono_bg": "#eee8de", "oscura": True,
        "concepto": [
            "SPOTLIGHT comes from Esteban's concert photography: dark stages where a single beam decides what is seen and what is not.",
            "The identity works the same way. A black stage background, a single amber tungsten light and a classic italic serif that behaves like the name of a tour.",
            "This is the line for introducing himself as a photographer and editor: restrained, cinematic and focused on the image.",
        ],
        "origen": [("mercyme", "07.jpg", "MercyMe 2025"), ("crowder", "17.jpg", "Crowder Live"), ("for-king-country", "06.jpg", "for KING & COUNTRY")],
        "colores": [("Night", "#070708", "Main background", 64), ("Bone", "#EEE8DE", "Text and headlines", 18), ("Smoke", "#1A1A1F", "Surfaces and rules", 10),
                    ("Tungsten amber", "#FFB648", "Single accent: light, figures, states", 6), ("Stage blue", "#3D5AFE", "Occasional use in photos", 2)],
        "tipos": [("Cormorant Garamond", "Display · headlines, names, figures", "400 · 500 · Italic", "'Cormorant Garamond', serif", "Esteban Guillen"),
                  ("Manrope", "Text · paragraphs, navigation, buttons", "400 · 500 · 600", "Manrope, sans-serif", "Design, video and live photography."),
                  ("DM Mono", "Data · labels, clock, counters", "400 · uppercase +6%", "'DM Mono', monospace", "MIAMI 10:18 PM · 1.3M+ VIEWS")],
        "escala": [("Display", "clamp(4.2rem, 15.5vw, 16.5rem)", "0.82", "Cormorant 400"), ("H1", "9.5rem", "0.86", "Cormorant 400"), ("H2", "4.8rem", "0.95", "Cormorant 400 / italic"),
                   ("Summary", "3.2rem", "1.06", "Cormorant 400"), ("Body", "1.0625rem", "1.6", "Manrope 400"), ("Label", "0.75rem", "1.2", "DM Mono · uppercase")],
        "reticula": "12 columns · 4vw side margin (16–64 px) · 1600 px max width · 20–36 px gutter",
        "ret_t": "12 columns",
        "elementos": [("Light beam", "The cursor is a spotlight. In the hero, a cone falls from the top down to the pointer and reveals the photo."),
                      ("Film grain", "Fine 7% noise, animated at 4 frames per second over the whole page."),
                      ("Amber rule", "An 18 px line precedes every mono label. It is the line's minimal signature."),
                      ("Numbered setlist", "Projects are listed like songs: number, serif title, discipline and figure in amber.")],
        "foto": ["Deep blacks: the stage must read dark, never grey.", "Keep the real color of the stage lighting; no added color filters.",
                 "Favor backlight, haze and silhouettes in front of the crowd.", "Wide frames with the crowd in the foreground to give scale."],
        "movimiento": [("WebGL spotlight", "Custom shader: the light follows the cursor with 0.07 inertia and drifts on its own when idle.", "Continuous"),
                       ("Curtain", "A black curtain rises with an amber line on every page change.", "1.0 s · expo.inOut"),
                       ("Rising words", "Headlines come in word by word from behind a mask.", "1.3 s · expo.out · 0.06 s"),
                       ("Lit-up statement", "Each word goes from 14% to 100% opacity as you scroll.", "Scroll-linked"),
                       ("Setlist", "Hovering a title shows the project cover following the cursor.", "0.6 s · power3"),
                       ("Live gallery", "The section pins and the photos move sideways with inner parallax.", "Scroll-linked"),
                       ("Smooth scroll", "Lenis with 0.085 interpolation for cinematic scrolling.", "Continuous")],
        "incorrectos": ["Swapping the amber for another color", "Placing the logo on light photos without contrast", "Distorting or squashing the wordmark", "Using the serif for small body text"],
    },
    "matchday": {
        "titulo": "MATCHDAY", "sub": "Brand identity 02 · Sports design, video and photography",
        "fuentes": "family=Anton&family=Archivo:wdth,wght@62..125,400..900&family=Space+Mono",
        "bg": "#eceae4", "fg": "#0c0c0c", "acc": "#e4002b", "mut": "#6f6c66", "lin": "#0c0c0c", "sup": "#e0ddd5",
        "fd": "Anton, Impact, sans-serif", "ft": "Archivo, sans-serif", "fm": "'Space Mono', monospace",
        "d_peso": "400", "d_trk": "0", "d_case": "uppercase", "d_italic": False,
        "port_bg": "#e4002b", "port_fg": "#eceae4", "logo_port": "neg", "port_tam": 200, "proy": "luis-benites", "post": "nahomi-martinez", "mono_bg": "#e4002b",
        "concepto": [
            "MATCHDAY comes from the match posters Esteban designed for Universitario, Sport Huancayo and the Peru women's national team.",
            "The identity behaves like match day: kit red, poster paper with halftone, condensed type that fills the full width and diagonals that add speed.",
            "It is the most energetic line: for clubs, sports brands and campaigns that need instant impact.",
        ],
        "origen": [("nahomi-martinez", "03.jpg", "Nahomi Martínez"), ("luis-benites", "05.jpg", "Luis Benites"), ("matchdays", "02.jpg", "Matchday's 2022–23")],
        "colores": [("Paper", "#ECEAE4", "Poster background", 46), ("Ink black", "#0C0C0C", "Text, blocks, hard shadows", 26), ("Kit red", "#E4002B", "Brand color", 20),
                    ("Fixture yellow", "#FFD60A", "Ticker, numbers, callouts", 6), ("Maroon", "#7A1F2B", "Supporting color", 2)],
        "tipos": [("Anton", "Display · headlines, names, figures", "400 · always uppercase", "Anton, sans-serif", "ESTEBAN GUILLEN"),
                  ("Archivo", "Text and labels · variable width 62–125", "400 – 900 · width 62 for labels", "Archivo, sans-serif", "Design that takes the pitch."),
                  ("Space Mono", "Technical data", "400", "'Space Mono', monospace", "2023 · Photoshop, Illustrator")],
        "escala": [("Display", "clamp(4.6rem, 12.5vw, 13rem)", "0.84", "Anton"), ("H2", "8.5rem", "0.84", "Anton"), ("Figure", "8rem", "0.85", "Anton"),
                   ("Subtitle", "2.2rem", "1.0", "Anton"), ("Body", "1.0625rem", "1.55", "Archivo 500"), ("Label", "0.875rem", "1.2", "Archivo 800 · width 62 · uppercase")],
        "reticula": "Full-bleed blocks · 3.6vw margin (16–56 px) · 1680 px max width · diagonals at 18°",
        "ret_t": "12 columns",
        "elementos": [("EG crest", "A crest with a diagonal stripe. MMXX = 2020, the year Esteban started publishing his portfolio. The #20 shirt number comes from the same year."),
                      ("18° diagonal", "Stripes, wipes and section cuts always at 18 degrees, like the Universitario pieces."),
                      ("Halftone and tear", "5 px dots over the whole sheet and torn edges to close blocks."),
                      ("Hard shadow", "A 0.08 em black offset with no blur on headlines and cards.")],
        "foto": ["Player cut out over flat color backgrounds or textures.", "Movement: kicks, celebrations, jumps; never static poses.",
                 "High contrast and saturated club colors.", "The player's name can repeat as a background texture."],
        "movimiento": [("Kick-off intro", "MATCHDAY slams in letter by letter, shakes and tears upward.", "≈2.4 s · back.out(2)"),
                       ("Diagonal wipe", "Three stripes (yellow, red, black) cross the screen on page change.", "0.75 s · expo.inOut"),
                       ("Type slam", "Headlines drop from 2.4× scale with a twist and the page shakes on impact.", "0.55 s · back.out(1.7)"),
                       ("Marquees", "The outlined name moves faster the faster you scroll.", "Velocity-linked"),
                       ("3D fan", "Five posters fan out and tilt with the cursor.", "1.1 s · expo.out"),
                       ("Odometer scoreboard", "Each digit rolls like a stadium scoreboard.", "1.6 s + 0.25 s per digit"),
                       ("Carousel and trading cards", "Draggable posters with inertia; cards flip 180° to show the back.", "0.8 s")],
        "incorrectos": ["Using Anton in lowercase", "Changing the 18° diagonal", "Filling the crest with gradients", "Adding more than two accent colors"],
    },
    "estudio": {
        "titulo": "STUDIO", "sub": "Brand identity 03 · Branding, social media and web",
        "fuentes": "family=Geist:wght@300;400;500;600;700&family=Geist+Mono",
        "bg": "#f2f2ef", "fg": "#111111", "acc": "#ff4d1c", "mut": "#8a8a86", "lin": "#d6d6d1", "sup": "#e8e8e4",
        "fd": "Geist, Helvetica, sans-serif", "ft": "Geist, Helvetica, sans-serif", "fm": "'Geist Mono', monospace",
        "d_peso": "600", "d_trk": "-0.06em", "d_case": "none", "d_italic": False,
        "port_bg": "#111111", "port_fg": "#f2f2ef", "logo_port": "neg", "port_tam": 200, "proy": "qatar-2022", "post": "qatar-2022", "mono_bg": "#ff4d1c",
        "concepto": [
            "STUDIO comes from Esteban's brand systems: Qatar 2022, Physo and Zena Coffee. Work that succeeds because it repeats a clear structure.",
            "The identity is a Swiss editorial studio: white paper, black ink and a single signal orange, all aligned to a 12-column grid that can be revealed on the site with the G key.",
            "It is the most corporate line: for agencies, brands and teams that hire a designer for judgment and order.",
        ],
        "origen": [("qatar-2022", "04.jpg", "Qatar 2022"), ("physo", "01.jpg", "Physo"), ("zena-coffee", "01.jpg", "Zena Coffee")],
        "colores": [("Paper", "#F2F2EF", "Background", 62), ("Ink", "#111111", "Text and blocks", 26), ("Rule", "#D6D6D1", "Rules and dividers", 6),
                    ("Grey", "#8A8A86", "Metadata", 4), ("Signal orange", "#FF4D1C", "Single accent", 2)],
        "tipos": [("Geist", "Display and text · one family", "300 – 700 · display 600 at -6% tracking", "Geist, sans-serif", "Esteban Guillen"),
                  ("Geist Mono", "Numbering, metadata, clock", "400 · uppercase", "'Geist Mono', monospace", "02 — INDEX · 10:33:53 PM EST")],
        "escala": [("Display", "clamp(4.4rem, 15.8vw, 18rem)", "0.80", "Geist 600 · -6.5%"), ("H1", "10rem", "0.86", "Geist 600 · -6%"), ("H2", "6.4rem", "0.90", "Geist 500 · -5.5%"),
                   ("Summary", "3rem", "1.05", "Geist 500 · -4.5%"), ("Body", "1rem", "1.5", "Geist 400"), ("Metadata", "0.75rem", "1.3", "Geist Mono · uppercase")],
        "reticula": "12 columns · 20 px gutter · 2.6vw margin (16–40 px) · everything starts on a column",
        "ret_t": "12 columns",
        "elementos": [("Visible grid", "The 12 columns draw in on load and can be shown with the G key: the system stays in sight."),
                      ("Numbering", "Every section and page has a number (01 — Home, 02 — Index). It orders content and doubles as navigation."),
                      ("Sampled palette", "Each project shows its 5 real colors, sampled from the published pieces."),
                      ("Signal square", "An orange square, 1/8 of the logo, marks the point of attention.")],
        "foto": ["Full images, no forced crops: the piece is the hero.", "Clean backgrounds and even light for product or people photography.",
                 "The portrait is black and white over orange and regains its color on hover.", "Long web pages are shown from the top."],
        "movimiento": [("Numbered panel", "On page change a black panel rises with the destination's number and name.", "0.8 s · expo.inOut"),
                       ("Grid draw-in", "The 12 columns drop in one after another on load.", "1.0 s · 0.04 s between columns"),
                       ("Line-by-line text", "Each line rises from behind a mask.", "1.2 s · expo.out · 0.07 s"),
                       ("WebGL viewer", "Covers change with a noise dissolve and an orange edge.", "1.3 s · every 4.2 s"),
                       ("Expanding index", "Hovering a project opens a strip with its pieces.", "0.6 s · expo.out"),
                       ("List ↔ grid", "The same collection changes layout with Flip, seamlessly.", "0.9 s · expo.inOut"),
                       ("Roll", "Large links swap their text by rolling upward.", "0.55 s")],
        "incorrectos": ["Adding a second accent color", "Breaking the 12-column grid", "Using Geist with positive tracking in headlines", "Centering long text"],
    },
    "mesa": {
        "titulo": "CANVAS", "sub": "Brand identity 04 · All the work on a designer's desk",
        "fuentes": "family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=IBM+Plex+Mono:wght@400;500&family=Caveat:wght@700",
        "bg": "#e6e4de", "fg": "#151515", "acc": "#3b30ff", "mut": "#8b877e", "lin": "#d9d6ce", "sup": "#f6f5f1",
        "fd": "'Bricolage Grotesque', sans-serif", "ft": "'Bricolage Grotesque', sans-serif", "fm": "'IBM Plex Mono', monospace",
        "d_peso": "800", "d_trk": "-0.05em", "d_case": "none", "d_italic": False,
        "port_bg": "#151515", "port_fg": "#e6e4de", "logo_port": "neg", "port_tam": 190, "proy": "physo", "post": "physo", "mono_bg": "#3b30ff",
        "concepto": [
            "CANVAS turns the portfolio into a designer's working file: an infinite canvas with rulers, layers, an inspector and sticky notes.",
            "Every project is a frame with its name and its real pixel dimensions. Video, photography, football, brand, web and gaming share the same desk, organized by page.",
            "It is the line that shows process and judgment: ideal for studios, agencies and product teams that want to see how Esteban thinks.",
        ],
        "origen": [("physo", "02.jpg", "Physo"), ("zena-coffee", "00.jpg", "Zena Coffee"), ("qatar-2022", "01.jpg", "Qatar 2022")],
        "colores": [("Canvas", "#E6E4DE", "Background with dot grid", 54), ("Ink", "#151515", "Text and toolbar", 22), ("Sheet", "#FBFAF7", "Frames and panels", 14),
                    ("Selection blue", "#3B30FF", "Selection, links and actions", 7), ("Note", "#FFE45C", "Sticky notes", 3)],
        "tipos": [("Bricolage Grotesque", "Display and text", "400 – 800 · display 800 at -5%", "'Bricolage Grotesque', sans-serif", "Esteban Guillen"),
                  ("IBM Plex Mono", "Frame labels, dimensions, rulers", "400 · 500", "'IBM Plex Mono', monospace", "Frame · Physo · 1600 × 1600"),
                  ("Caveat", "Handwritten sticky notes", "700", "Caveat, cursive", "60 photos across 3 concerts")],
        "escala": [("Display", "clamp(3.2rem, 9.5vw, 9rem)", "0.88", "Bricolage 800 · -5.5%"), ("Project H1", "6.6rem", "0.90", "Bricolage 800"), ("Summary", "1.55rem", "1.35", "Bricolage 400"),
                   ("Body", "1.0625rem", "1.55", "Bricolage 400"), ("Label", "0.75rem", "1.3", "IBM Plex Mono"), ("Note", "38 px on canvas", "1.05", "Caveat 700")],
        "reticula": "7,000 × 4,800 px canvas with dots every 24 px · inner pages on 12 columns · 232 and 300 px panels",
        "ret_t": "Canvas and panels",
        "elementos": [("Frame", "Every piece carries its name on top, its dimensions below and four blue selection handles."),
                      ("Rulers", "Horizontal and vertical rulers with the real canvas or scroll position and a marker that follows the cursor."),
                      ("Sticky note", "Yellow or pink, handwritten, with translucent tape. It can be dragged."),
                      ("Inspector", "Properties panel: client, role, year, tools, results and sampled palette.")],
        "foto": ["Pieces are shown whole, in their original proportion.", "The real size of each file is part of the design.",
                 "Clean product backgrounds for brand photography.", "The portrait is black and white in frames and full color in the inspector."],
        "movimiento": [("Canvas", "Drag with inertia; zoom with wheel, pinch or buttons; minimap and keyboard.", "Continuous"),
                       ("Fly to a frame", "The camera frames the selected project.", "1.1 s · expo.inOut"),
                       ("Esteban's cursor", "A cursor with his name roams the desk and selects frames until the visitor touches something.", "1.6 s per leg"),
                       ("Zoom transition", "The tapped frame grows to fill the screen and opens the page.", "0.6 s · expo.inOut"),
                       ("Canvas entrance", "Frames appear in random order and the camera flies to the introduction.", "0.7 s + 1.6 s"),
                       ("Filter by page", "The board reorders itself with Flip when switching discipline.", "0.7 s · expo.inOut")],
        "incorrectos": ["Changing the selection blue", "Removing a frame's handles or dimensions", "Distorting the symbol", "Using the handwriting outside sticky notes"],
    },
    "alaire": {
        "titulo": "ON AIR", "sub": "Brand identity 05 · The portfolio as a live channel",
        "fuentes": "family=Big+Shoulders+Display:wght@700;800;900&family=Onest:wght@400;500;600&family=Chivo+Mono",
        "bg": "#05070f", "fg": "#f4f6ff", "acc": "#ff2d3d", "mut": "#8a90a8", "lin": "#1f2640", "sup": "#0e1324",
        "fd": "'Big Shoulders Display', sans-serif", "ft": "Onest, sans-serif", "fm": "'Chivo Mono', monospace",
        "d_peso": "900", "d_trk": "0", "d_case": "uppercase", "d_italic": False,
        "port_bg": "#05070f", "port_fg": "#f4f6ff", "logo_port": "pos", "port_tam": 240, "proy": "gallucci", "post": "bobby-charles", "mono_bg": "#ff2d3d", "oscura": True,
        "concepto": [
            "ON AIR starts from a simple idea: everything Esteban makes goes on air. Campaign spots, live concerts, match days, brands that post daily and gaming streams.",
            "The identity uses the language of television: lower thirds, a ticker, timecode, a TV guide, ratings and end credits. The site is a channel and every project is an episode.",
            "It is the line closest to his current role as video editor and videographer: direct, fast and measurable.",
        ],
        "origen": [("gallucci", "00.jpg", "Sam Gallucci"), ("mercyme", "07.jpg", "MercyMe 2025"), ("valorant", "02.jpg", "Valorant Overlays")],
        "colores": [("Studio black", "#05070F", "Background", 58), ("Caption white", "#F4F6FF", "Text and lower thirds", 20), ("Panel", "#0E1324", "Surfaces", 12),
                    ("Live red", "#FF2D3D", "Live, accents, figures", 6), ("Signal blue", "#2A5CFF", "Selection and bars", 4)],
        "tipos": [("Big Shoulders Display", "Display · lower thirds, titles, figures", "700 – 900 · always uppercase", "'Big Shoulders Display', sans-serif", "ESTEBAN GUILLEN"),
                  ("Onest", "Text and navigation", "400 – 600", "Onest, sans-serif", "I edit, shoot and design work that goes on air."),
                  ("Chivo Mono", "Timecode and metadata", "400 · uppercase", "'Chivo Mono', monospace", "LIVE · 00:12:44:08")],
        "escala": [("Lower third XL", "clamp(2.9rem, 7.2vw, 8rem)", "0.86", "Big Shoulders 900"), ("H1", "13rem", "0.82", "Big Shoulders 900"), ("H2", "8rem", "0.84", "Big Shoulders 900"),
                   ("Figure", "8.5rem", "0.90", "Big Shoulders 900"), ("Body", "1.0625rem", "1.55", "Onest 400"), ("Metadata", "0.75rem", "1.3", "Chivo Mono · uppercase")],
        "reticula": "TV safe area at 90% · 4vw margin (16–64 px) · 1520 px max width · guide in 10 columns (channel + 9 years)",
        "ret_t": "Safe area",
        "elementos": [("Lower third", "A white block with the name and a red strip with the title, like a newscast."),
                      ("Ticker", "A bottom band with Esteban's numbers. It speeds up with scroll."),
                      ("Channel bug", "EG in a rounded rectangle with the red live dot."),
                      ("Color bars", "Test bars close every page before the footer.")],
        "foto": ["Full-screen images with a vignette and soft scan lines.", "Text always sits in lower thirds, never straight on the photo.",
                 "Video frames carry their timecode.", "16:9 format for covers and episode cards."],
        "movimiento": [("Channel surfing", "Static and the channel number on page change.", "0.38 s"),
                       ("CRT power-on", "A white line opens up when the page loads.", "0.3 s + 0.45 s"),
                       ("Shows on the home page", "They change on their own every 6 s with static; also with CH −/+ or the arrow keys.", "6 s"),
                       ("Lower thirds", "They wipe in with a mask from left to right.", "0.7 s · expo.inOut"),
                       ("Timecode", "Runs at 25 frames per second and carries over between pages.", "Continuous"),
                       ("Guide with PIP", "Hovering a show plays it in a picture-in-picture window.", "0.3 s"),
                       ("Credits", "The résumé rolls up like end credits as you scroll.", "Scroll-linked")],
        "incorrectos": ["Setting text on a photo without a lower third", "Using Big Shoulders in lowercase", "Changing the live red", "Removing the red dot from the bug"],
    },
    "recorte": {
        "titulo": "CUTOUT", "sub": "Brand identity 06 · Handmade: paper, tape and ink",
        "fuentes": "family=DM+Serif+Display&family=Archivo+Black&family=Courier+Prime:wght@400;700&family=Work+Sans:wght@400;500;600",
        "bg": "#efe9dc", "fg": "#1b1b1b", "acc": "#ff4fa3", "mut": "#807a6d", "lin": "#d6cdb8", "sup": "#fbf8f1",
        "fd": "'DM Serif Display', serif", "ft": "'Work Sans', sans-serif", "fm": "'Courier Prime', monospace",
        "d_peso": "400", "d_trk": "-0.01em", "d_case": "none", "d_italic": False,
        "port_bg": "#1b1b1b", "port_fg": "#efe9dc", "logo_port": "neg", "port_tam": 180, "proy": "nahomi-martinez", "post": "matchdays", "mono_bg": "#ffd23f",
        "concepto": [
            "CUTOUT grows out of the collage in Esteban's football posters (cutouts, textures, mixed type) and carries it across all of his work.",
            "The portfolio looks handmade: newsprint, printed pieces taped to the wall, letters cut from different magazines, rubber stamps and a typewritten résumé.",
            "It is the warmest, most human line, designed so a recruiter remembers the person behind the work.",
        ],
        "origen": [("nahomi-martinez", "03.jpg", "Nahomi Martínez"), ("matchdays", "21.jpg", "Matchday's 2022–23"), ("luis-benites", "05.jpg", "Luis Benites")],
        "colores": [("Paper", "#EFE9DC", "Grainy background", 52), ("Ink", "#1B1B1B", "Text and footer", 24), ("Riso pink", "#FF4FA3", "Accent, stamps, scissors", 10),
                    ("Riso blue", "#1F5BD8", "Accent, stamps", 8), ("Tape yellow", "#FFD23F", "Tape and marquee", 6)],
        "tipos": [("DM Serif Display", "Headlines and cutout letters", "400 · regular and italic", "'DM Serif Display', serif", "Esteban Guillen"),
                  ("Archivo Black", "Cutout letters, buttons, stamps", "400 · uppercase", "'Archivo Black', sans-serif", "1.3M+ VIEWS"),
                  ("Courier Prime", "Typewriter: file cards and résumé", "400 · 700", "'Courier Prime', monospace", "File No. 07 · Client"),
                  ("Work Sans", "Body text", "400 – 600", "'Work Sans', sans-serif", "Graphic designer and video editor in Miami.")],
        "escala": [("Cutout letters", "clamp(3.4rem, 11vw, 11.5rem)", "1.02", "Mix of three families"), ("H2", "6.4rem", "0.98", "DM Serif Display"), ("Stamp", "5.6rem", "0.90", "Archivo Black"),
                   ("Summary", "3rem", "1.05", "DM Serif Display"), ("Body", "1.0625rem", "1.6", "Work Sans 400"), ("File card", "0.875rem", "1.5", "Courier Prime 700")],
        "reticula": "12 columns with pieces rotated ±3° · 4vw margin (16–64 px) · 1480 px max width · vertical offset every 4 and 5 pieces",
        "ret_t": "12 loose columns",
        "elementos": [("Cutout letters", "Each letter with its own paper, typeface and tilt. On the home page they can be dragged."),
                      ("Tape and staple", "Translucent yellow or pink tape on the corners; a staple on file cards."),
                      ("Rubber stamps", "Figures in a double border with pink, blue or black ink that hit the paper."),
                      ("Torn sheet", "The torn edge closes the header, the footer and the page transition.")],
        "foto": ["Every image is printed with a white border and taped down.", "A soft halftone screen that disappears on hover.",
                 "On hover, a pink and blue misregistration.", "The portrait is a Polaroid."],
        "movimiento": [("Falling letters", "The headline letters fall and bounce in random order.", "0.9 s · bounce.out"),
                       ("Torn sheet", "A black sheet with a torn edge rises and covers the page while navigating.", "0.65 s · expo.inOut"),
                       ("Loose photos", "The home page photos move with the cursor at three depths.", "1 s · power3"),
                       ("Typewriter", "The job title is typed letter by letter.", "28–68 ms per letter"),
                       ("Stamps", "Figures drop from 2.6× scale and shake on impact.", "0.22 s + 0.2 s"),
                       ("Experience", "Each line of the résumé is typed out as it enters.", "0.9 s · steps(22)"),
                       ("Tape", "The yellow marquee speeds up with scroll.", "Continuous")],
        "incorrectos": ["Using a single typeface for the cutout letters", "Showing photos without a border or tape", "Using gradients", "Rotating pieces more than 8°"],
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
    if linea == "mesa":
        col = {"pos": "#151515", "neg": "#fbfaf7", "mono": "#151515", "mini": "#151515"}[modo]
        hoja = {"pos": "#fbfaf7", "neg": "#151515", "mono": "#3b30ff", "mini": "#fbfaf7"}[modo]
        sel = "#151515" if modo == "mono" else "#3b30ff"
        sim = f"""<svg viewBox="0 0 56 56" style="width:{96 * tam}px;height:{96 * tam}px"><rect x="6" y="6" width="44" height="44" fill="{hoja}" stroke="{sel}" stroke-width="2"/><g fill="{hoja}" stroke="{sel}" stroke-width="2"><rect x="2" y="2" width="8" height="8"/><rect x="46" y="2" width="8" height="8"/><rect x="2" y="46" width="8" height="8"/><rect x="46" y="46" width="8" height="8"/></g><text x="28" y="35" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="19" fill="{col}">EG</text></svg>"""
        if modo == "mini":
            return sim
        return f"""<div style="display:flex;align-items:center;gap:{22 * tam}px;color:{col}">{sim}<span style="font-family:'Bricolage Grotesque';font-weight:800;font-size:{76 * tam}px;letter-spacing:-0.05em;line-height:.92">Esteban<br>Guillen</span></div>"""
    if linea == "alaire":
        col = {"pos": "#f4f6ff", "neg": "#05070f", "mono": "#05070f", "mini": "#f4f6ff"}[modo]
        punto = "#05070f" if modo == "mono" else "#ff2d3d"
        sim = f"""<svg viewBox="0 0 72 40" style="width:{150 * tam}px;height:{84 * tam}px"><rect x="1" y="1" width="70" height="38" rx="7" fill="none" stroke="{col}" stroke-width="2"/><text x="31" y="29" text-anchor="middle" font-family="Big Shoulders Display" font-weight="900" font-size="26" fill="{col}">EG</text><circle cx="58" cy="20" r="5" fill="{punto}"/></svg>"""
        if modo == "mini":
            return sim
        return f"""<div style="display:flex;align-items:center;gap:{22 * tam}px;color:{col}">{sim}<span style="display:flex;flex-direction:column;font-family:'Big Shoulders Display';font-weight:900;text-transform:uppercase;line-height:.86"><span style="font-size:{92 * tam}px">Esteban Guillen</span><small style="font-family:'Chivo Mono';font-weight:400;font-size:{17 * tam}px;letter-spacing:.14em;margin-top:{10 * tam}px;color:{punto if modo != 'mono' else col}">PORTFOLIO CHANNEL</small></span></div>"""
    if linea == "recorte":
        tinta = "#1b1b1b"
        pal = ["#ffd23f", "#fbf8f1", "#ff4fa3", "#1f5bd8", "#1b1b1b"] if modo != "mono" else ["#fbf8f1"] * 5
        fuentes = ["'DM Serif Display'", "'Archivo Black'", "'Courier Prime'"]
        letras = []
        for k, ch in enumerate("Esteban Guillen"):
            if ch == " ":
                letras.append("<br>"); continue
            bg = pal[(k * 3) % 5]; fg = "#fff" if bg in ("#1f5bd8", "#1b1b1b") else tinta
            letras.append(f'<span style="display:inline-block;background:{bg};color:{fg};font-family:{fuentes[k % 3]};font-weight:700;padding:0 .08em;margin:0 .01em;transform:rotate({((k * 37) % 11) - 5}deg);box-shadow:0 2px 4px rgba(0,0,0,.18)">{ch}</span>')
        a1, a2 = ("#ff4fa3", "#1f5bd8") if modo != "mono" else ("#1b1b1b", "#1b1b1b")
        sim = f"""<svg viewBox="0 0 70 44" style="width:{150 * tam}px;height:{94 * tam}px"><rect x="2" y="6" width="32" height="34" fill="{a1}" transform="rotate(-6 18 23)"/><rect x="34" y="4" width="32" height="34" fill="{a2}" transform="rotate(5 50 21)"/><text x="18" y="33" text-anchor="middle" font-family="DM Serif Display" font-size="28" fill="{'#1b1b1b' if modo != 'mono' else '#ffd23f'}" transform="rotate(-6 18 23)">E</text><text x="50" y="31" text-anchor="middle" font-family="Archivo Black" font-size="24" fill="{'#fff' if modo != 'mono' else '#ffd23f'}" transform="rotate(5 50 21)">G</text></svg>"""
        if modo == "mini":
            return sim
        return f"""<div style="display:flex;align-items:center;gap:{26 * tam}px">{sim}<span style="font-size:{64 * tam}px;line-height:1.08">{''.join(letras)}</span></div>"""
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
    <p class="mono">Brand guidelines · November 2026</p>
    <h1 style="{disp}">{L['titulo']}</h1>
    <p class="port-sub">{e(L['sub'])}</p>
    <div class="port-logo">{logo_html(linea, L['logo_port'], .8)}</div>
  </div>
</section>""")
    # 2 Índice
    secciones = ["Concept", "Logo", "Construction", "Versions", "Color", "Typography", "Grid", "Graphic elements",
                 "Photography", "Motion", "Web · desktop", "Web · mobile and pages", "Résumé", "Applications", "Incorrect use"]
    pag(2, "Contents", f"""<div class="indice"><h2 style="{disp}">Contents</h2><ol>{''.join(f'<li><span class="mono">{i + 3:02d}</span>{s}</li>' for i, s in enumerate(secciones))}</ol></div>""")
    # 3 Concepto
    ori = "".join(f'<figure><img src="{foto(s, n)}"><figcaption class="mono">{e(t)}</figcaption></figure>' for s, n, t in L["origen"])
    pag(3, "Concept", f"""<div class="concepto"><div><p class="mono">Where it comes from</p><h2 style="{disp}">{L['titulo'].capitalize() if L['d_case'] == 'none' else L['titulo']}</h2>{''.join(f'<p>{e(t)}</p>' for t in L['concepto'])}</div><div class="origen">{ori}</div></div>""")
    # 4 Logotipo
    pag(4, "Logo", f"""<div class="logo-grande">{logo_html(linea, 'pos', 1.9)}</div><p class="nota-pie">Primary logo: symbol + name. Used in the site header, covers and signatures.</p>""", "centrada")
    # 5 Construcción
    pag(5, "Construction", f"""<div class="construccion"><div class="cons-caja"><div class="cons-grid"></div><div class="cons-zona"></div>{logo_html(linea, 'pos', 1.4)}</div>
<ul class="lista"><li><b>Unit X</b> = symbol height ÷ 4.</li><li><b>Clear space</b>: 1X free around the logo (dashed line).</li><li><b>Minimum size</b>: 120 px wide on screen · 30 mm in print. Symbol alone: 24 px · 8 mm.</li><li>The symbol and the name always keep the same proportion.</li></ul></div>""")
    # 6 Versiones
    pag(6, "Versions", f"""<div class="versiones">
<div class="ver" style="background:{L['bg']}">{logo_html(linea, 'pos', .7)}<span class="mono">Primary · on brand background</span></div>
<div class="ver" style="background:{L['fg']}">{logo_html(linea, 'neg', .7)}<span class="mono" style="color:{L['bg']}">Reversed</span></div>
<div class="ver" style="background:{L['mono_bg']}">{logo_html(linea, 'mono', .7)}<span class="mono" style="color:{L['bg'] if linea == 'luz' else '#0c0c0c'}">One color</span></div>
<div class="ver" style="background:{L['sup']}">{logo_html(linea, 'mini', 1.2)}<span class="mono">Symbol · favicon, avatar, watermark</span></div></div>""")
    # 7 Color
    total = "".join(f'<span style="flex:{p};background:{h}"></span>' for _, h, _, p in L["colores"])
    sw = "".join(f"""<div class="sw"><span class="sw-c" style="background:{h}"></span><b>{e(n)}</b><span class="mono">HEX {h}<br>RGB {rgb(h)}<br>CMYK {cmyk(h)}</span><span class="sw-uso">{e(u)} · {p} %</span></div>""" for n, h, u, p in L["colores"])
    pag(7, "Color", f"""<div class="color"><div class="swatches">{sw}</div><p class="mono">Usage proportion</p><div class="proporcion">{total}</div></div>""")
    # 8 Tipografía
    tp = "".join(f"""<div class="tipo"><p class="mono">{e(r)} · {e(p)}</p><p class="tipo-n" style="font-family:{f}">{e(n)}</p><p class="tipo-m" style="font-family:{f}">{e(m)}</p><p class="tipo-abc" style="font-family:{f}">Aa Bb Cc Ññ 0123456789 ?!&</p></div>""" for n, r, p, f, m in L["tipos"])
    esc = "".join(f'<tr><td>{e(a)}</td><td class="mono">{e(b)}</td><td class="mono">{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in L["escala"])
    pag(8, "Typography", f"""<div class="tipografia"><div class="tipos">{tp}</div><table class="escala"><thead><tr><th class="mono">Level</th><th class="mono">Size</th><th class="mono">Leading</th><th class="mono">Family</th></tr></thead><tbody>{esc}</tbody></table></div>""")
    # 9 Retícula
    pag(9, "Grid", f"""<div class="reticula-p"><div class="ret-demo"><img src="{cap('index_d')}"><div class="ret-cols">{''.join('<i></i>' for _ in range(12))}</div></div><div><h2 style="{disp}">{e(L.get('ret_t', '12 columns'))}</h2><p>{e(L['reticula'])}</p><p>Every block starts and ends on a column. On mobile the grid collapses to a single column with the same 16 px minimum side margin.</p></div></div>""")
    # 10 Elementos
    el = "".join(f'<div class="elem"><span class="mono">{i + 1:02d}</span><h3 style="{disp}">{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(L["elementos"]))
    pag(10, "Graphic elements", f'<div class="elementos">{el}</div><div class="elem-img"><img src="{cap("index3_d" if linea in ("estudio", "mesa") else "index2_d")}"></div>')
    # 11 Fotografía
    imgs = "".join(f'<img src="{foto(s, n)}">' for s, n, _ in L["origen"])
    pag(11, "Photography", f"""<div class="fotografia"><div class="foto-imgs">{imgs}</div><ul class="lista">{''.join(f'<li>{e(x)}</li>' for x in L['foto'])}</ul></div>""")
    # 12 Movimiento
    mv = "".join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td class="mono">{e(c)}</td></tr>' for a, b, c in L["movimiento"])
    pag(12, "Motion", f"""<div class="movimiento"><div><h2 style="{disp}">How the site moves</h2><p>Every effect is hand-written with GSAP, Lenis and custom WebGL. None of them is a template: each one comes from a craft Esteban practices. With "reduce motion" turned on, the site shows without animation.</p></div><table class="mov">{mv}</table></div>""")
    # 13 Web escritorio
    pag(13, "Web · desktop", f"""<div class="web-d"><div class="nav-sim"><img src="{cap('index_d')}"></div><div class="web-d-2"><img src="{cap('index3_d')}"><img src="{cap('trabajo_d')}"></div></div>""")
    # 14 Web móvil + páginas
    tel = "".join(f'<div class="tel"><img src="{cap(n + "_m")}"></div>' for n in ["index", "trabajo", L["proy"]])
    pag(14, "Web · mobile and pages", f"""<div class="web-m"><div class="tels">{tel}</div><div class="web-m-d"><img src="{cap(L['proy'] + '_d')}"><img src="{cap('sobre_d')}"><p class="mono">17 pages per site: home, work, 12 projects, about, résumé and contact.</p></div></div>""")
    # 15 Currículum
    pag(15, "Résumé", f"""<div class="cvp"><div class="cvp-hoja"><img src="{cap('cvpdf')}"></div><div class="cvp-web"><img src="{cap('cv_d')}">
<div><h2 style="{disp}">Résumé</h2><p>The résumé lives inside the site (CV page) and downloads as an A4 PDF with the same identity. Both are generated from the same data, so they always match.</p></div></div></div>""")
    # 16 Aplicaciones
    pag(16, "Applications", aplicaciones(linea, disp))
    # 16 Usos incorrectos
    inc = []
    for i, t in enumerate(L["incorrectos"]):
        estilo = ["filter:hue-rotate(160deg)", "opacity:.35", "transform:scaleX(1.5) scaleY(.75)", "filter:blur(1.5px)"][i]
        fondo = [L["bg"], "#cfcfcf" if L.get("oscura") else "#777", L["bg"], L["bg"]][i]
        inc.append(f'<div class="inc"><div class="inc-caja" style="background:{fondo}"><div style="{estilo}">{logo_html(linea, "pos", .55)}</div><span class="x">×</span></div><p>{e(t)}</p></div>')
    pag(17, "Incorrect use", f'<div class="incorrectos">{"".join(inc)}</div>')
    # 17 Contraportada
    paginas.append(f"""<section class="pg contra"><div>{logo_html(linea, L['logo_port'], 1.0)}</div><div class="contra-datos"><p>{e(D.CORREO)}</p><p>{e(D.PUESTO)}</p><p>{e(D.INSTAGRAM_T)}</p><p class="mono">{e(D.CIUDAD)} · 2026</p></div></section>""")

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{L['titulo']} · Brand guidelines</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{L['fuentes']}&display=swap">
<style>{css(L, linea)}</style></head><body>{''.join(paginas)}</body></html>"""


def aplicaciones(linea, disp):
    L = LINEAS[linea]
    p = D.por_slug(L["post"])
    img = foto(p["slug"], p["portada"])
    tarjeta_f = f'<div class="tarj" style="background:{L["bg"]};color:{L["fg"]}">{logo_html(linea, "pos", .6)}</div>'
    tarjeta_d = f"""<div class="tarj tarj-d" style="background:{L['acc'] if linea not in ('estudio', 'mesa') else L['fg']};color:{'#0c0c0c' if linea not in ('estudio', 'mesa') else L['bg']}">
<b style="{disp};font-size:30px">{e(D.NOMBRE)}</b><span>Design · Video · Photography</span><span class="mono" style="color:inherit">{e(D.CORREO)}<br>{e(D.INSTAGRAM_T)}<br>{e(D.CIUDAD)}</span></div>"""
    post = f"""<div class="post" style="background:{L['bg']};color:{L['fg']}"><div class="post-img" style="background-image:url('{img}')"></div>
<div class="post-txt"><span class="mono" style="color:{L['acc']}">New project</span><b style="{disp};font-size:46px;line-height:.9;{'font-style:italic' if L['d_italic'] else ''}">{e(p['corto'])}</b><span class="mono">{e(D.CATEGORIAS[p['cat']])} · {e(p['cifra'])} {e(p['cifra_t'])}</span></div></div>"""
    portada = f"""<div class="bh" style="background:{L['bg']};color:{L['fg']}"><div class="bh-img" style="background-image:url('{foto(*LINEAS[linea]['origen'][1][:2])}')"></div>
<div class="bh-txt"><b style="{disp};font-size:50px;line-height:.86;{'font-style:italic' if L['d_italic'] else ''}">Esteban Guillen</b><span class="mono" style="color:{L['acc']}">Design · Video · Live photography — Miami</span></div></div>"""
    firma = f"""<div class="firma" style="background:#fff;color:#111"><div style="transform:scale(.55);transform-origin:left center;width:200px;height:60px;display:flex;align-items:center">{logo_html(linea, 'mini', .6)}</div>
<div><b>{e(D.NOMBRE)}</b><br><span>{e(D.PUESTO)}</span><br><span style="color:{L['acc'] if linea != 'luz' else '#b07a1f'}">{e(D.CORREO)}</span> · {e(D.INSTAGRAM_T)}</div></div>"""
    return f"""<div class="apps"><div class="app"><div class="tarjetas">{tarjeta_f}{tarjeta_d}</div><p class="mono">Business card · 85 × 55 mm</p></div>
<div class="app">{post}<p class="mono">Instagram post · 1080 × 1350</p></div>
<div class="app app-ancha">{portada}<p class="mono">Profile banner · LinkedIn and social</p></div>
<div class="app app-ancha">{firma}<p class="mono">Email signature</p></div></div>"""


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
.port-img {{ background-size: cover; background-position: center; {'filter: brightness(.85);' if L.get('oscura') else ''} }}
.port-txt {{ padding: 110px; display: flex; flex-direction: column; justify-content: space-between; background: {L['port_bg']}; color: {L['port_fg']}; }}
.port-txt .mono {{ color: inherit; opacity: .8; }}
.port-txt h1 {{ font-size: {L['port_tam']}px; line-height: .82; {'font-style: italic; color:' + L['acc'] + ';' if L['d_italic'] else ''} }}
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
.contra {{ display: flex; flex-direction: column; justify-content: space-between; background: {L['port_bg']}; color: {L['port_fg']}; }}
.cvp {{ display: grid; grid-template-columns: 560px 1fr; gap: 70px; padding-top: 40px; align-items: start; }}
.cvp-hoja img {{ width: 100%; box-shadow: 0 30px 60px -30px rgba(0,0,0,.5); border: 1px solid {L['lin']}; }}
.cvp-web {{ display: grid; gap: 40px; }}
.cvp-web > img {{ width: 100%; height: 470px; object-fit: cover; object-position: top; border: 1px solid {L['lin']}; }}
.cvp-web h2 {{ font-size: 80px !important; margin-bottom: 20px !important; }}
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
    lineas = sys.argv[2:] or list(LINEAS)
    for linea in lineas:
        i = list(LINEAS).index(linea) + 1
        html = manual(linea, capturas)
        hp = os.path.join(capturas, f"manual_{linea}.html")
        open(hp, "w", encoding="utf-8").write(html)
        nombre = LINEAS[linea]["titulo"].lower().replace(" ", "-")
        pdf = os.path.join(salida, f"0{i}-{nombre}-brand-guidelines.pdf")
        imprimir(hp, pdf)
        print("ok", pdf)
