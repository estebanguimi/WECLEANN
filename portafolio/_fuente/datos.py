# -*- coding: utf-8 -*-
"""Contenido compartido por las tres webs del portafolio.

Cambia aquí tus datos y vuelve a ejecutar:  python3 _fuente/construir.py
"""

NOMBRE = "Esteban Guillen"
ROL = "Editor de video y videógrafo"
ROL_CORTO = "Video · Web · Experiencias digitales"
EMPRESA = "Harris Media Group"
UBICACION = "Florida, EE. UU."
IDIOMAS = ["Español", "Inglés"]
ANOS = "10+"

# >>> Cambia estas líneas por tus enlaces reales <<<
CORREO = "tucorreo@ejemplo.com"
GITHUB = "https://github.com/estebanguimi"
LINKEDIN = ""   # p. ej. "https://www.linkedin.com/in/tu-usuario"
VIMEO = ""      # enlace a tu reel; mientras esté vacío se muestra "Reel en preparación"

BIO_CORTA = (
    "Edito y grabo video para campañas y marcas en Harris Media Group. "
    "También diseño y programo las herramientas web que esos equipos usan: "
    "sitios con panel propio, venta de entradas en 3D y plataformas de inscripción para eventos."
)

BIO_LARGA = [
    "Llevo más de diez años trabajando en artes visuales. Hoy soy editor de video y videógrafo en "
    "Harris Media Group, una agencia de marketing político y de marca con oficinas en Florida, Texas, "
    "Nueva Inglaterra y Latinoamérica.",
    "Mi trabajo diario es el montaje: elegir la toma, cortar en el fotograma correcto y entregar a tiempo "
    "versiones para televisión, redes y pantallas grandes. Trabajo en español y en inglés, y eso cambia "
    "cómo edito: el ritmo de un spot no es el mismo en los dos idiomas.",
    "Con los años empecé a construir también la parte web. Si una campaña necesita publicar videos sin "
    "depender de un programador, le hago un panel. Si un recinto necesita vender entradas mostrando la "
    "vista real desde el asiento, lo modelo en 3D. Me interesa que la herramienta sea tan clara como el corte.",
]

SERVICIOS = [
    ("Edición de video", "Spots de 15, 30 y 60 segundos, versiones para redes, entrevistas y piezas largas."),
    ("Videografía", "Rodaje en eventos, entrevistas y material de apoyo con equipo ligero."),
    ("Sitios web con panel", "Webs que el equipo actualiza sin tocar código: obras, noticias y perfiles."),
    ("Experiencias 3D", "Mapas interactivos y recorridos en el navegador con Three.js."),
    ("Plataformas para eventos", "Registro, turnos, fotos y gestión de personal con PHP y MySQL."),
]

HERRAMIENTAS = {
    "Video": ["Premiere Pro", "After Effects", "DaVinci Resolve", "Cámara y sonido en rodaje"],
    "Web": ["HTML, CSS y JavaScript", "Three.js", "Python y Flask", "PHP y MySQL", "Tailwind CSS", "Docker"],
}

# Cada proyecto: textos reales de tus repositorios.
PROYECTOS = [
    {
        "slug": "harris-media",
        "titulo": "Harris Media Group",
        "subtitulo": "Sitio web y panel de administración",
        "tipo": "Web",
        "ano": "2026",
        "rol": "Diseño y desarrollo completo",
        "stack": ["Python", "Flask", "Generador estático", "Tailwind CSS", "Docker"],
        "resumen": (
            "El sitio completo de la agencia y un panel propio, más simple que WordPress, "
            "para que el equipo publique obras, noticias y perfiles sin escribir código."
        ),
        "brief": (
            "La agencia necesitaba renovar su web y dejar de depender de un desarrollador para cada cambio. "
            "El equipo creativo sube videos todas las semanas y el sitio tenía que mostrarlos bien en cualquier pantalla."
        ),
        "hice": [
            "Portada, Nuestros clientes con 15 páginas propias, Servicios, Obras, Equipo con un perfil por persona, Empleos, Noticias y Contacto.",
            "Panel en /admin: obras con foto, video subido o enlace de YouTube, Vimeo, Facebook o Instagram.",
            "Editor de noticias con subtítulos, citas, listas e imágenes; borradores y vista previa antes de publicar.",
            "Perfiles del equipo en inglés, español y portugués.",
            "Un botón, Publicar cambios, que reconstruye todo el sitio estático.",
        ],
        "decisiones": [
            ("Sitio estático + panel", "El público ve HTML ya generado: carga rápido y no hay base de datos expuesta."),
            ("Videos hasta 400 MB", "Los MP4 se suben directo; los largos se enlazan y el sitio muestra la portada oficial."),
            ("Fotos optimizadas solas", "El panel recibe JPG o PNG y los comprime sin que nadie lo piense."),
        ],
        "cifras": [("15", "páginas de clientes"), ("3", "idiomas en perfiles"), ("400 MB", "por video subido")],
        "imagenes": [
            ("hmg-home.jpg", "Portada del sitio de Harris Media Group"),
            ("hmg-cifras.jpg", "Sección de trayectoria con cifras de la agencia"),
            ("hmg-servicios.jpg", "Servicios y oficinas de la agencia"),
            ("hmg-obras.jpg", "Galería de obras alimentada desde el panel"),
        ],
        "color": "lavanda",
    },
    {
        "slug": "arena-pass",
        "titulo": "Arena Pass",
        "subtitulo": "Venta de entradas en 3D para el Amerant Bank Arena",
        "tipo": "Web 3D",
        "ano": "2026",
        "rol": "Concepto, modelado y desarrollo",
        "stack": ["Three.js", "JavaScript", "HTML", "CSS"],
        "resumen": (
            "Un arena entero modelado en el navegador. Eliges sección, eliges asiento "
            "y ves la vista real desde ese asiento antes de pagar."
        ),
        "brief": (
            "Comprar una entrada desde un plano plano es adivinar. La idea fue llevar al comprador al lugar: "
            "que vea el escenario desde su fila y compare precio contra vista."
        ),
        "hice": [
            "Vista aérea del arena con estacionamientos, palmeras, lago y autopista.",
            "Unos 18.000 asientos individuales en los niveles 100 y 300, más 16 suites del nivel club.",
            "Tres configuraciones según el evento: hockey, concierto con sillas en pista y baloncesto con courtside.",
            "Clic en un asiento para ver la vista; Ver en 3D baja la cámara a la altura de los ojos.",
            "Filtro de precio, carrito de hasta 8 asientos, impuesto de Florida (7 %) y entradas con QR.",
        ],
        "decisiones": [
            ("Asientos instanciados", "Miles de asientos dibujados como una sola malla para que vaya fluido en un portátil."),
            ("Secciones bloqueadas", "En conciertos se cierran las secciones detrás del escenario automáticamente."),
            ("Sin servidor", "Es un sitio estático; para venta real se conecta inventario y pasarela de pago."),
        ],
        "cifras": [("~18.000", "asientos individuales"), ("16", "suites VIP"), ("3", "configuraciones")],
        "imagenes": [
            ("arena-aerea.jpg", "Vista aérea del arena con el panel de zonas y precios"),
            ("arena-concierto.jpg", "Configuración de concierto con escenario y pista"),
            ("arena-asientos.jpg", "Selección de asientos en el piso frente al escenario"),
        ],
        "color": "caribe",
        "nota": "Demo: eventos, precios y disponibilidad son de ejemplo.",
    },
    {
        "slug": "cleanspace",
        "titulo": "CleanSpace",
        "subtitulo": "Inscripción de personal para eventos en estadios",
        "tipo": "Plataforma",
        "ano": "2026",
        "rol": "Identidad, diseño y desarrollo",
        "stack": ["PHP", "MySQL", "Tailwind CSS", "JavaScript"],
        "resumen": (
            "Una plataforma para reclutar al equipo de limpieza de grandes eventos: "
            "registro, foto de identificación, elección de turnos y un panel para publicar fechas."
        ),
        "brief": (
            "Cada evento en estadio necesita decenas de personas por turno. El registro se hacía por mensajes "
            "y hojas sueltas. Hacía falta un flujo corto que funcionara desde el teléfono."
        ),
        "hice": [
            "Logotipo y estilo de CleanSpace: Tu espacio, limpio y brillante.",
            "Registro con datos de contacto y permiso de trabajo.",
            "Subida de foto con requisitos claros: buena luz, de frente, sin gorra ni lentes.",
            "Lista de turnos paginada con reglas: el mismo día se pueden tomar el 1.º y el 3.º turno, pero no el 2.º junto a ellos.",
            "Panel de administración para crear, editar y publicar eventos y gestionar inscritos.",
        ],
        "decisiones": [
            ("Reglas en la interfaz", "Los turnos incompatibles se bloquean al marcar, no después con un error."),
            ("Borrador y publicado", "El administrador prepara fechas sin que nadie las vea hasta publicarlas."),
            ("Contraseñas seguras", "Acceso con password_hash y consultas preparadas en todas las tablas."),
        ],
        "cifras": [("4", "pasos de registro"), ("3", "turnos por día"), ("2", "roles: persona y admin")],
        "imagenes": [
            ("cs-turnos.jpg", "Selección de turnos con la regla del mismo día"),
            ("cs-registro.jpg", "Formulario de registro"),
            ("cs-admin.jpg", "Panel de gestión de eventos"),
            ("cs-login.jpg", "Pantalla de ingreso con el logotipo de CleanSpace"),
        ],
        "color": "mango",
    },
    {
        "slug": "edicion",
        "titulo": "Edición y video",
        "subtitulo": "Campañas y marcas en Harris Media Group",
        "tipo": "Video",
        "ano": "2024 – hoy",
        "rol": "Editor de video y videógrafo",
        "stack": ["Premiere Pro", "After Effects", "DaVinci Resolve"],
        "resumen": (
            "Montaje y rodaje para campañas políticas y de marca en inglés y en español: "
            "spots, versiones para redes y cobertura de eventos."
        ),
        "brief": (
            "En campaña el material llega tarde y la fecha de salida no se mueve. "
            "Mi trabajo es convertir horas de grabación en piezas cortas que se entiendan sin sonido y funcionen en cada formato."
        ),
        "hice": [
            "Spots de 15, 30 y 60 segundos para televisión y digital.",
            "Versiones verticales y cuadradas para redes, con subtítulos quemados.",
            "Entrevistas y testimonios: selección de respuestas, ritmo y corrección de color.",
            "Rodaje en eventos y material de apoyo para el equipo creativo.",
        ],
        "decisiones": [
            ("Primero sin sonido", "Reviso cada corte en silencio: en redes la mayoría lo ve así."),
            ("Dos idiomas, dos ritmos", "Una frase en español dura más; ajusto el corte en lugar de acelerar la voz."),
            ("Entregas por formato", "Exporto cada pieza en horizontal, vertical y cuadrado desde la misma línea de tiempo."),
        ],
        "cifras": [("10+", "años en artes visuales"), ("2", "idiomas de trabajo"), ("3", "formatos por pieza")],
        "imagenes": [
            ("evento.jpg", "Evento en vivo en un arena"),
        ],
        "color": "rosa",
        "nota": "Agrega aquí tu reel y tus piezas: pega el enlace de Vimeo o YouTube en datos.py.",
    },
]


def proyecto(slug):
    return next(p for p in PROYECTOS if p["slug"] == slug)


def siguiente(slug):
    i = [p["slug"] for p in PROYECTOS].index(slug)
    return PROYECTOS[(i + 1) % len(PROYECTOS)]
