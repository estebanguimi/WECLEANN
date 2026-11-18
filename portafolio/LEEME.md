# Portafolio · Esteban Guillen

Tres webs completas, cada una con su propia línea gráfica, construidas a partir de los 12 proyectos de
[behance.net/estebanguimi](https://www.behance.net/estebanguimi). Cada línea tiene su manual en PDF.

| Carpeta | Línea | Sale de | Efectos principales | Manual |
|---|---|---|---|---|
| `luz/` | **LUZ** | Fotografía de conciertos (MercyMe, Crowder, for KING & COUNTRY) | Foco WebGL que sigue al cursor, cortina con línea ámbar, galería horizontal fijada, setlist con vista previa | `manuales/01-luz-manual-linea-grafica.pdf` |
| `matchday/` | **MATCHDAY** | Afiches de fútbol (Universitario, Sport Huancayo, selección) | Intro de partido, barrido diagonal, abanico 3D de afiches, marcador odómetro, carrusel con inercia, cromos que giran | `manuales/02-matchday-manual-linea-grafica.pdf` |
| `estudio/` | **ESTUDIO** | Sistemas de marca (Qatar 2022, Physo, Zena Coffee) | Retícula suiza visible (tecla G), visor WebGL con disolución de ruido, índice desplegable, lista ↔ cuadrícula con Flip | `manuales/03-estudio-manual-linea-grafica.pdf` |

Cada web tiene 16 páginas: inicio, trabajo, una página por cada uno de los 12 proyectos, sobre mí y contacto.

## Verlas en tu computadora

```bash
cd portafolio
python3 -m http.server 8000
# http://localhost:8000/luz/   http://localhost:8000/matchday/   http://localhost:8000/estudio/
```

Hay que abrirlas con un servidor (no con doble clic), porque el efecto WebGL carga las imágenes.

## Editar contenido

Todo el texto está en `_fuente/datos.py` (proyectos, bio, correo, redes). Después:

```bash
python3 _fuente/construir.py          # regenera las tres webs
```

Las imágenes de los proyectos están en `img/` (descargadas de tu Behance y optimizadas).

## Subirlas a internet

Para publicar una sola web en GitHub Pages o Netlify, sube su carpeta y también `img/`, porque las webs
cargan las imágenes desde `../img/`.

## Tecnología

HTML, CSS y JavaScript sin frameworks. GSAP 3.12 (ScrollTrigger y Flip) y Lenis van incluidos en `vendor/`.
Los efectos WebGL son shaders escritos para este proyecto. Todas las webs respetan la opción
«reducir movimiento» del sistema.
