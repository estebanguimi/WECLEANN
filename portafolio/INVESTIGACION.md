# Portafolio de Esteban Guillen: investigación y tres líneas gráficas

## 1. Punto de partida: quién eres según tus proyectos

Revisé tus repositorios para no inventar nada:

| Fuente | Qué dice de ti |
|---|---|
| Perfil en el sitio de Harris Media Group | Editor de video y videógrafo, más de 10 años en artes visuales, trabaja en inglés y español. |
| `harris-media-website` | Sitio completo de la agencia + panel propio (Flask) para obras, noticias y equipo en 3 idiomas, videos de hasta 400 MB, publicación con un botón. |
| `stadium-website-tickets` (Arena Pass) | Arena modelado en Three.js: ~18.000 asientos, 16 suites, 3 configuraciones, vista desde el asiento, carrito con impuesto de Florida y QR. |
| `WECLEANN` (CleanSpace) | Plataforma PHP/MySQL para reclutar personal de limpieza en eventos: registro, foto con requisitos, turnos con reglas, panel de administración. Incluye logotipo propio. |

Conclusión: tu perfil no es "desarrollador" ni "videógrafo" por separado. Eres alguien del mundo del video y de los eventos en vivo que además construye las herramientas. Esa mezcla es lo que diferencia tu portafolio, así que las tres líneas salen de ahí.

Todas las imágenes de proyectos son **capturas reales** de tus proyectos funcionando (los rendericé localmente). Nada de imágenes de banco ni generadas.

## 2. Qué valora quien revisa un portafolio

Resumen de guías para editores de video y de lo que piden reclutadores:

1. **Pocos proyectos y bien elegidos.** Entre 5 y 7 piezas relevantes es mejor que veinte sueltas. Aquí hay 4, cada uno con su página.
2. **Contexto en cada proyecto.** Qué te pidieron, qué hiciste tú y qué decisiones tomaste. Cada página de proyecto tiene *El encargo*, *Lo que hice* y *Decisiones*.
3. **Resultados y cifras verificables.** Solo usé cifras que están en tus repos (18.000 asientos, 15 páginas de clientes, 400 MB). No inventé métricas de audiencia.
4. **El reel arriba, si lo hay.** Para video, el reel es lo primero que se busca. Dejé el espacio preparado: pega tu enlace en `datos.py` (`VIMEO = "..."`) y aparece el botón.
5. **Contacto evidente y fácil de copiar.** Correo visible con botón de copiar en las tres webs.
6. **Rápido y legible en el teléfono.** Sitios estáticos, sin librerías, imágenes comprimidas (~1,4 MB en total), revisados a 390, 768 y 1440 px.

## 3. Cómo evitar que se vea hecho por IA

La tendencia más citada en 2026 es el rechazo a la estética genérica de IA (*anti-AI crafting*): texturas, cosas hechas a mano, estructuras con carácter pero legibles. Lo que hoy delata una web generada, y por eso **no está** en ninguna de las tres:

- Degradados morado-azul, "blobs" y fondos con brillo o *glassmorphism*.
- Cursor personalizado que persigue al ratón, texto que se escribe solo, marquesinas infinitas.
- Todo apareciendo con *fade-up* al hacer scroll.
- Tarjetas con la misma esquina redondeada y sombra en todas partes.
- Números 01 / 02 / 03 decorativos que no significan nada.
- Efectos de "radar", "láser" o "telemetría". (Tu sitio de HMG ya los usa; aquí los evité a propósito para que el portafolio no se parezca.)
- Paleta crema + serif + terracota, o negro con un solo verde ácido.

La regla que seguí: **cada efecto tiene que venir de un oficio real**. Si un editor, un señalista de estadio o un laboratorista no lo reconocería, no entra.

## 4. Las tres líneas

### Línea 1 · CORTE (`1-corte/`)
**Idea:** la web es tu sala de montaje.

- **Color:** gris de sala de corrección de color (el gris neutro que se usa para no contaminar la percepción) y los colores de etiqueta de clip de un editor: lavanda, caribe, mango, rosa. El cabezal en rojo.
- **Tipografía:** Familjen Grotesk (titulares y texto) + JetBrains Mono para timecode.
- **Interacción principal:** una **línea de tiempo real** con pistas V1, V2, A1 y A2. Cada proyecto es un clip con entrada y salida en timecode a 24 fps. Arrastras el cabezal y el monitor de programa muestra el proyecto que está debajo. Con el foco en la línea de tiempo funcionan **J, K y L** como en Premiere o Resolve (atrás, parar, adelante, y más rápido si repites), flechas para avanzar un cuadro y Enter para abrir el clip.
- **Detalles de oficio:** márgenes de seguridad de título dibujados en el monitor; el trabajo como *bin* con vista lista o iconos; servicios como *marcadores*; el pie dice "Fin de secuencia" con el timecode total.

### Línea 2 · SECCIÓN (`2-seccion/`)
**Idea:** la web es la señalética de un recinto, porque tus proyectos viven en estadios y eventos.

- **Color:** azul cobalto de asiento de estadio, negro de letrero, amarillo de señal, gris concreto y el verde de las salidas de emergencia.
- **Tipografía:** Big Shoulders Display (diseñada originalmente para señalética urbana) + Overpass (derivada de la tipografía de carreteras) + Overpass Mono.
- **Interacción principal:** el índice de proyectos es un **plano del arena**. Las secciones 101 a 104, a pie de pista, son tus proyectos. Al pasar o tocar una sección, el panel muestra qué hay dentro.
- **Detalles de oficio:** la navegación son letreros con flecha y número de sección (100 Trabajo, 200 Sobre mí, 300 Taquilla); cada proyecto es una **entrada** con talón perforado, sección, fila, asiento y código de barras; las cifras van como marcador; "Sobre mí" es una **credencial de producción**; el pie es un letrero de **Salida**.

### Línea 3 · CONTACTOS (`3-contactos/`)
**Idea:** la web es una hoja de contactos de laboratorio, la forma clásica de revisar material y elegir qué se amplía.

- **Color:** mesa gris neutra, papel fotográfico blanco, película negra con números de borde en ámbar, **lápiz graso rojo** para las marcas y **bolígrafo azul** para las notas.
- **Tipografía:** Schibsted Grotesk + DM Mono + Reenie Beanie (solo para notas a mano, con moderación).
- **Interacción principal:** una **lupa** de laboratorio. Pasas el ratón por cualquier fotograma y la lupa lo amplía 2,6 veces con el recorte exacto. En el teléfono las tiras se desplazan de lado como una tira real.
- **Detalles de oficio:** cada proyecto es un rollo de 6 fotogramas numerados (12, ▸12A…); el fotograma elegido va **encerrado en un círculo** y el descarte **tachado con X**, dibujados a mano y distintos en cada uno; la página de proyecto es una **ampliación** con notas al margen; el contacto es un **sobre de laboratorio** con casillas.

## 5. Estructura de cada web

Las tres tienen las mismas 8 páginas, así puedes compararlas igual:

```
index.html          Inicio
trabajo.html        Índice de proyectos
harris-media.html   Proyecto
arena-pass.html     Proyecto
cleanspace.html     Proyecto
edicion.html        Proyecto (edición y video)
sobre.html          Sobre mí
contacto.html       Contacto
```

## 6. Pendiente de tu parte

1. **Correo:** cambia `CORREO` en `_fuente/datos.py` (ahora dice `tucorreo@ejemplo.com`).
2. **Reel y LinkedIn:** pega los enlaces en `VIMEO` y `LINKEDIN`.
3. **Edición y video:** esta página usa por ahora una foto de concierto que venía en CleanSpace como imagen de ejemplo. Cámbiala por fotogramas tuyos (guárdalos en `_fuente/assets/` y ajusta `imagenes` en `datos.py`).
4. **Ubicación:** puse "Florida, EE. UU." por los proyectos; corrígela si no es así.

Luego ejecuta `python3 _fuente/construir.py` y las tres webs se regeneran.

## Fuentes consultadas

- [What Should a Video Editing Portfolio Include? (Fueler)](https://www.fueler.io/blog/what-should-a-video-editing-portfolio-include-complete-guide)
- [How to Evaluate a Video Editor Without Watching 20 Reels (Fueler)](https://www.fueler.io/blog/how-to-evaluate-a-video-editor-without-watching-20-reels)
- [How to make a video editor portfolio (Vimeo)](https://vimeo.com/blog/post/video-editor-portfolio)
- [How to Make a Video Editor Portfolio (Backstage)](https://www.backstage.com/magazine/article/video-editor-portfolio-76062/)
- [Awwwards: Portfolio Honors](https://www.awwwards.com/inspiration_search/winner_category_portfolio/)
- [Texture, warmth and tactile rebellion: graphic design trends 2026 (Creative Bloq)](https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026)
- [17 Web Design Trends for 2026 (DesignRush)](https://www.designrush.com/agency/website-design-development/trends/web-design-trends)
- [Filmmaker website examples (HubSpot)](https://blog.hubspot.com/website/filmmaker-website-examples)
