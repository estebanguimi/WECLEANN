# -*- coding: utf-8 -*-
"""Currículum en PDF (A4) con la identidad de cada línea gráfica.

    NODE_PATH=$(npm root -g) python3 _fuente/cv.py [linea ...]

Escribe <linea>/esteban-guillen-cv.pdf. El contenido sale de datos.py, igual que la página cv.html de cada web.
"""
import os
import subprocess
import sys
import tempfile

import datos as D
from comun import e

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
IMG = "file://" + os.path.join(RAIZ, "img")

TEMAS = {
    "luz": dict(fuentes="family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Manrope:wght@400;600;700&family=DM+Mono",
                fd="'Cormorant Garamond', serif", ft="Manrope, sans-serif", fm="'DM Mono', monospace",
                cab_bg="#070708", cab_fg="#eee8de", acc="#ffb648", acc_txt="#9a6410", fg="#141414", mut="#77736c", lin="#e4ded3",
                nombre_css="font-style:italic;font-weight:500;font-size:46px;letter-spacing:-.02em",
                logo='<svg viewBox="0 0 64 64" width="44" height="44"><circle cx="32" cy="32" r="30" fill="none" stroke="#ffb648" stroke-width="2"/><text x="32" y="41" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-size="30" fill="#eee8de">eg</text></svg>'),
    "matchday": dict(fuentes="family=Anton&family=Archivo:wdth,wght@62..125,400..900&family=Space+Mono",
                     fd="Anton, sans-serif", ft="Archivo, sans-serif", fm="'Space Mono', monospace",
                     cab_bg="#e4002b", cab_fg="#ffffff", acc="#e4002b", acc_txt="#c10024", fg="#0c0c0c", mut="#66625c", lin="#dcd9d1",
                     nombre_css="text-transform:uppercase;font-size:50px;line-height:.9",
                     logo='<svg viewBox="0 0 60 70" width="40" height="46"><path d="M30 2 56 10v26c0 16-12 26-26 32C16 62 4 52 4 36V10z" fill="#0c0c0c" stroke="#fff" stroke-width="3"/><text x="30" y="44" text-anchor="middle" font-family="Anton" font-size="24" fill="#fff">EG</text></svg>'),
    "estudio": dict(fuentes="family=Geist:wght@400;500;600;700&family=Geist+Mono",
                    fd="Geist, sans-serif", ft="Geist, sans-serif", fm="'Geist Mono', monospace",
                    cab_bg="#f2f2ef", cab_fg="#111111", acc="#ff4d1c", acc_txt="#d83a0e", fg="#111111", mut="#7d7d78", lin="#d6d6d1",
                    nombre_css="font-weight:600;font-size:50px;letter-spacing:-.06em",
                    logo='<svg viewBox="0 0 48 48" width="40" height="40"><rect width="48" height="48" fill="#111"/><text x="24" y="31.5" text-anchor="middle" font-family="Geist" font-weight="700" font-size="20" fill="#f2f2ef">EG</text><rect x="34" y="8" width="6" height="6" fill="#ff4d1c"/></svg>'),
    "mesa": dict(fuentes="family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=IBM+Plex+Mono:wght@400;500",
                 fd="'Bricolage Grotesque', sans-serif", ft="'Bricolage Grotesque', sans-serif", fm="'IBM Plex Mono', monospace",
                 cab_bg="#e6e4de", cab_fg="#151515", acc="#3b30ff", acc_txt="#3b30ff", fg="#151515", mut="#76736d", lin="#dcd9d2",
                 nombre_css="font-weight:800;font-size:48px;letter-spacing:-.045em",
                 logo='<svg viewBox="0 0 56 56" width="42" height="42"><rect x="6" y="6" width="44" height="44" fill="#fff" stroke="#3b30ff" stroke-width="2"/><g fill="#fff" stroke="#3b30ff" stroke-width="2"><rect x="2" y="2" width="8" height="8"/><rect x="46" y="2" width="8" height="8"/><rect x="2" y="46" width="8" height="8"/><rect x="46" y="46" width="8" height="8"/></g><text x="28" y="35" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="19" fill="#151515">EG</text></svg>'),
    "alaire": dict(fuentes="family=Big+Shoulders+Display:wght@700;900&family=Onest:wght@400;500;700&family=Chivo+Mono:wght@400;500",
                   fd="'Big Shoulders Display', sans-serif", ft="Onest, sans-serif", fm="'Chivo Mono', monospace",
                   cab_bg="#05070f", cab_fg="#f4f6ff", acc="#ff2d3d", acc_txt="#e01628", fg="#0b0e1a", mut="#6c7083", lin="#dfe2ec",
                   nombre_css="font-weight:900;text-transform:uppercase;font-size:52px;line-height:.9;letter-spacing:.005em",
                   logo='<svg viewBox="0 0 72 40" width="60" height="34"><rect x="1" y="1" width="70" height="38" rx="7" fill="none" stroke="#f4f6ff" stroke-width="2"/><text x="31" y="29" text-anchor="middle" font-family="Big Shoulders Display" font-weight="900" font-size="26" fill="#f4f6ff">EG</text><circle cx="58" cy="20" r="5" fill="#ff2d3d"/></svg>'),
    "recorte": dict(fuentes="family=DM+Serif+Display&family=Archivo+Black&family=Courier+Prime:wght@400;700&family=Work+Sans:wght@400;500;600",
                    fd="'DM Serif Display', serif", ft="'Work Sans', sans-serif", fm="'Courier Prime', monospace",
                    cab_bg="#efe9dc", cab_fg="#1b1b1b", acc="#ff4fa3", acc_txt="#d61f7a", fg="#1b1b1b", mut="#6f6a60", lin="#d9d1c0",
                    nombre_css="font-size:48px;letter-spacing:-.01em",
                    logo='<svg viewBox="0 0 70 44" width="58" height="36"><rect x="2" y="6" width="32" height="34" fill="#ff4fa3" transform="rotate(-6 18 23)"/><rect x="34" y="4" width="32" height="34" fill="#1f5bd8" transform="rotate(5 50 21)"/><text x="18" y="33" text-anchor="middle" font-family="DM Serif Display" font-size="28" fill="#1b1b1b" transform="rotate(-6 18 23)">E</text><text x="50" y="31" text-anchor="middle" font-family="Archivo Black" font-size="24" fill="#fff" transform="rotate(5 50 21)">G</text></svg>'),
}

DESTACADOS = ["gallucci", "bobby-charles", "mercyme", "matchdays", "qatar-2022", "physo"]


def html_cv(linea):
    T = TEMAS[linea]
    exp = "".join(f"""<div class="exp"><div class="exp-f">{e(x['fechas'])}<br><span>{e(x['lugar'])}</span></div>
<div><h3>{e(x['puesto'])} <span>· {e(x['empresa'])}</span></h3><ul>{''.join(f'<li>{e(p)}</li>' for p in x['puntos'])}</ul></div></div>"""
                  for x in D.EXPERIENCIA)
    hab = "".join(f"<div class='hab'><h4>{e(t)}</h4><p>{e(' · '.join(l))}</p></div>" for t, l in D.HABILIDADES)
    cif = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in D.CIFRAS)
    dest = "".join(f"""<figure><img src="{IMG}/{s}/{D.por_slug(s)['portada']}"><figcaption><b>{e(D.por_slug(s)['corto'])}</b>
<span>{e(D.CATEGORIAS[D.por_slug(s)['cat']])} · {e(D.por_slug(s)['cifra'])} {e(D.por_slug(s)['cifra_t'])}</span></figcaption></figure>""" for s in DESTACADOS)
    idi = "".join(f"<li><b>{e(a)}</b> — {e(b)}</li>" for a, b in D.IDIOMAS)
    her = "".join(f"<li>{e(h)}</li>" for h in D.HERRAMIENTAS)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{T['fuentes']}&display=swap">
<style>
@page{{size:A4;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:210mm;font-family:{T['ft']};color:{T['fg']};font-size:8.7pt;line-height:1.38;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.hoja{{width:210mm;height:297mm;display:flex;flex-direction:column;overflow:hidden}}
.cab{{background:{T['cab_bg']};color:{T['cab_fg']};padding:11mm 14mm 7mm;display:grid;grid-template-columns:auto 1fr auto;gap:7mm;align-items:end;position:relative}}
.cab .r{{width:25mm;height:31mm;object-fit:cover;border-radius:1.5mm}}
.cab h1{{font-family:{T['fd']};white-space:nowrap;{T['nombre_css']};line-height:.95}}
.cab .pu{{font-weight:600;margin-top:2mm;font-size:10.5pt}}
.cab .pu i{{font-style:normal;color:{T['acc']}}}
.cab .ct{{font-family:{T['fm']};font-size:7.6pt;line-height:1.7;text-align:right;text-transform:uppercase;letter-spacing:.04em}}
.cab .lg{{position:absolute;right:14mm;top:10mm}}
.cuerpo{{flex:1;display:grid;grid-template-columns:1fr 58mm;gap:9mm;padding:6.5mm 14mm 0}}
h2{{font-family:{T['fm']};font-size:7.4pt;letter-spacing:.12em;text-transform:uppercase;color:{T['acc_txt']};border-bottom:1px solid {T['lin']};padding-bottom:1.6mm;margin:0 0 3mm}}
.res{{font-size:9.6pt;line-height:1.42;margin-bottom:4.5mm}}
.exp{{display:grid;grid-template-columns:27mm 1fr;gap:4mm;padding:0 0 2.3mm;margin-bottom:2.3mm;border-bottom:1px dashed {T['lin']}}}
.exp:last-child{{border:0}}
.exp-f{{font-family:{T['fm']};font-size:6.9pt;line-height:1.5}} .exp-f span{{color:{T['mut']}}}
.exp h3{{font-size:10pt;font-weight:700}} .exp h3 span{{font-weight:400;color:{T['mut']}}}
.exp ul{{margin:1mm 0 0 3.6mm}} .exp li{{margin:.4mm 0}} .exp li::marker{{color:{T['acc']}}}
.lat section{{margin-bottom:4.5mm}}
.cif{{display:grid;grid-template-columns:1fr 1fr;gap:3mm}}
.cif b{{display:block;font-family:{T['fd']};font-size:21pt;line-height:1;color:{T['fg']}}} .cif span{{font-size:7.6pt;color:{T['mut']}}}
.hab h4{{font-size:8.6pt;margin-bottom:.4mm}} .hab p{{font-size:8.2pt;color:{T['mut']};margin-bottom:2.2mm}}
.lat ul{{list-style:none;font-size:8.6pt}} .her{{display:flex;flex-wrap:wrap;gap:1.4mm}} .her li{{border:1px solid {T['lin']};padding:.6mm 2mm;border-radius:10mm;font-size:7.8pt}}
.dest{{padding:0 14mm 6mm}}
.dest .fi{{display:grid;grid-template-columns:repeat(6,1fr);gap:2.6mm}}
.dest figure img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;border-radius:1mm}}
.dest figcaption{{font-size:7pt;line-height:1.3;margin-top:1.2mm}} .dest figcaption b{{display:block;font-size:7.8pt}} .dest figcaption span{{color:{T['mut']}}}
.pie{{display:flex;justify-content:space-between;font-family:{T['fm']};font-size:7pt;color:{T['mut']};padding:0 14mm 7mm;text-transform:uppercase;letter-spacing:.06em}}
</style></head><body><div class="hoja">
<header class="cab"><img class="r" src="{IMG}/retrato.jpg"><div><h1>{e(D.NOMBRE)}</h1><p class="pu">{e(D.PUESTO)} <i>·</i> {e(D.CIUDAD)}</p></div>
<div class="ct">{e(D.CORREO)}<br>{e(D.INSTAGRAM_T)}<br>{e(D.DISPONIBLE)}</div><div class="lg">{T['logo']}</div></header>
<div class="cuerpo"><main><h2>Profile</h2><p class="res">{e(D.CV_RESUMEN)}</p><h2>Experience</h2>{exp}</main>
<aside class="lat"><section><h2>By the numbers</h2><div class="cif">{cif}</div></section><section><h2>Skills</h2>{hab}</section>
<section><h2>Tools</h2><ul class="her">{her}</ul></section><section><h2>Languages</h2><ul>{idi}</ul></section></aside></div>
<section class="dest"><h2>Featured projects</h2><div class="fi">{dest}</div></section>
<div class="pie"><span>{e(D.NOMBRE)} · Résumé 2026</span><span>Full portfolio online</span></div>
</div></body></html>"""


def imprimir(html, pdf):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        ruta = f.name
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{ruta}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
await p.pdf({{path:'{pdf}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)
    os.unlink(ruta)


def generar(linea, destino=None):
    destino = destino or os.path.join(RAIZ, linea)
    os.makedirs(destino, exist_ok=True)
    pdf = os.path.join(destino, D.CV_PDF)
    imprimir(html_cv(linea), pdf)
    return pdf


if __name__ == "__main__":
    for l in (sys.argv[1:] or list(TEMAS)):
        print("ok", generar(l))
