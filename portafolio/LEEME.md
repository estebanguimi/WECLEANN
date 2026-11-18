# Portafolio · Esteban Guillen

Tres versiones completas del portafolio, cada una con una línea gráfica distinta:

| Carpeta | Línea | Idea |
|---|---|---|
| `1-corte/` | CORTE | La web como sala de montaje: línea de tiempo con J K L. |
| `2-seccion/` | SECCIÓN | La web como señalética de estadio: plano del arena y entradas. |
| `3-contactos/` | CONTACTOS | La web como hoja de contactos: tiras de película y lupa. |

La investigación y las decisiones de diseño están en [INVESTIGACION.md](INVESTIGACION.md).

## Ver en tu computadora

```bash
cd portafolio
python3 -m http.server 8000
# abre http://localhost:8000/1-corte/  (o 2-seccion/, 3-contactos/)
```

## Cambiar textos, enlaces o imágenes

Todo el contenido está en `_fuente/datos.py`. Después de editarlo:

```bash
python3 _fuente/construir.py
```

Requiere Python 3 y Pillow (`pip install pillow`). Cada carpeta generada es autónoma: se puede subir tal cual a GitHub Pages, Netlify o cualquier hosting estático.
