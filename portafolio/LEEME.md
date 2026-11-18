# Portafolio · Esteban Guillen

Seis webs completas, cada una con su propia línea gráfica. Todas muestran los mismos 12 proyectos (video
político, fotografía en vivo, diseño deportivo, branding, web y gaming) y el currículum completo dentro de la
web. Ninguna enlaza a otra plataforma: todo el trabajo se ve en el propio portafolio. Cada línea tiene su
manual en PDF y su currículum en PDF.

| Carpeta | Línea | Idea | Efectos principales | Manual |
|---|---|---|---|---|
| `luz/` | **LUZ** | Escenario a oscuras, una sola luz ámbar | Foco WebGL que sigue al cursor, cortina, galería horizontal fijada, setlist con vista previa | `manuales/01-luz-…pdf` |
| `matchday/` | **MATCHDAY** | Día de partido: afiche, rojo y diagonales | Intro de partido, barrido diagonal, abanico 3D, marcador odómetro, carrusel con inercia, cromos | `manuales/02-matchday-…pdf` |
| `estudio/` | **ESTUDIO** | Estudio editorial suizo | Retícula visible (tecla G), visor WebGL con disolución, índice desplegable, lista ↔ cuadrícula | `manuales/03-estudio-…pdf` |
| `mesa/` | **MESA** | La mesa de trabajo de un diseñador | Lienzo infinito con zoom, minimapa, reglas, capas, inspector, notas adhesivas, cursor de Esteban | `manuales/04-mesa-…pdf` |
| `alaire/` | **AL AIRE** | El portafolio como un canal en vivo | Zapping con estática, encendido de tubo, rótulos, ticker, guía de programación con PIP, créditos | `manuales/05-alaire-…pdf` |
| `recorte/` | **RECORTE** | Hecho a mano: papel, cinta y tinta | Letras recortadas que caen y se arrastran, sellos de goma, hoja rasgada, máquina de escribir | `manuales/06-recorte-…pdf` |

Cada web tiene 17 páginas: inicio, trabajo, una página por cada uno de los 12 proyectos, perfil, currículum
(`cv.html`) y contacto. En cada carpeta está `esteban-guillen-cv.pdf`, el currículum A4 con esa identidad.

## Verlas en tu computadora

```bash
cd portafolio
python3 -m http.server 8000
# http://localhost:8000/luz/  /matchday/  /estudio/  /mesa/  /alaire/  /recorte/
```

Hay que abrirlas con un servidor (no con doble clic), porque los efectos WebGL cargan las imágenes.

## Editar contenido

Todo el texto está en `_fuente/datos.py`: proyectos, clientes, bio, currículum (experiencia, habilidades,
herramientas, idiomas), correo y redes. Después:

```bash
NODE_PATH=$(npm root -g) python3 _fuente/construir.py     # regenera las seis webs y sus CV en PDF
SIN_PDF=1 python3 _fuente/construir.py mesa               # solo una web, sin el PDF
```

## Videos

Los videos de campaña se muestran dentro de la página del proyecto si están en `img/video/` con este nombre:
`gallucci-1.mp4`, `gallucci-2.mp4`, `bobby-charles-1.mp4`… Copia ahí tus archivos y vuelve a construir.

## Manuales

```bash
NODE_PATH=$(npm root -g) python3 _fuente/manual.py <carpeta-de-capturas> [luz matchday …]
```

## Subirlas a internet

Para publicar una sola web en GitHub Pages o Netlify, sube su carpeta y también `img/`, porque las webs
cargan las imágenes desde `../img/`.

## Tecnología

HTML, CSS y JavaScript sin frameworks. GSAP 3.12 (ScrollTrigger y Flip) y Lenis van incluidos en `vendor/`.
Los efectos WebGL y de lienzo están escritos para este proyecto. Todas las webs respetan la opción
«reducir movimiento» del sistema.
