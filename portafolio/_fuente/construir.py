# -*- coding: utf-8 -*-
"""Construye las tres webs:  python3 _fuente/construir.py [luz matchday estudio]"""
import importlib
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import comun  # noqa: E402

SITIOS = ["luz", "matchday", "estudio"]


def construir(nombre, destino=None, prefijo="../img/"):
    comun.IMG["p"] = prefijo
    m = importlib.import_module(nombre)
    destino = destino or os.path.join(RAIZ, nombre)
    os.makedirs(destino, exist_ok=True)
    for archivo, html in m.paginas().items():
        with open(os.path.join(destino, archivo), "w", encoding="utf-8") as f:
            f.write(html)
    for archivo in os.listdir(os.path.join(AQUI, nombre)):
        shutil.copyfile(os.path.join(AQUI, nombre, archivo), os.path.join(destino, archivo))
    shutil.copytree(os.path.join(AQUI, "vendor"), os.path.join(destino, "vendor"), dirs_exist_ok=True)
    print("ok", nombre)


if __name__ == "__main__":
    for s in (sys.argv[1:] or SITIOS):
        construir(s)
