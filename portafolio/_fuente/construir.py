# -*- coding: utf-8 -*-
"""Construye las tres webs del portafolio.

    python3 _fuente/construir.py

Salida: 1-corte/, 2-seccion/, 3-contactos/ (cada una autónoma, lista para subir a cualquier hosting estático).
"""
import importlib
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

SITIOS = [("corte", "1-corte"), ("seccion", "2-seccion"), ("contactos", "3-contactos")]


def construir(modulo, carpeta):
    try:
        m = importlib.import_module(modulo)
    except ModuleNotFoundError as err:
        if err.name == modulo:
            return False
        raise
    destino = os.path.join(RAIZ, carpeta)
    os.makedirs(destino, exist_ok=True)
    for nombre, html in m.paginas().items():
        with open(os.path.join(destino, nombre), "w", encoding="utf-8") as f:
            f.write(html)
    for nombre in ("estilo.css", "app.js"):
        shutil.copyfile(os.path.join(AQUI, modulo, nombre), os.path.join(destino, nombre))
    shutil.copytree(os.path.join(AQUI, "assets"), os.path.join(destino, "assets"), dirs_exist_ok=True)
    print("ok", carpeta)
    return True


if __name__ == "__main__":
    for mod, carpeta in SITIOS:
        construir(mod, carpeta)
