# -*- coding: utf-8 -*-
"""Busqueda hibrida sobre el indice de AUCO.

Identico en espiritu al retriever del portafolio:

  BM25        encuentra el termino literal. Imprescindible aqui, donde
              se pregunta por nombres exactos: "veriface", "prebuild",
              "documentImage". Un embedding difumina eso.

  VECTORIAL   encuentra por significado. Cubre al cliente que pregunta
              "como valido que la foto sea de la misma persona" sin usar
              ninguna palabra de la documentacion.

  RRF         fusiona los dos rankings sumando 1/(k+posicion). No compara
              puntajes entre si —son escalas distintas e incomparables—
              sino el lugar que ocupa cada documento en cada lista.
"""

import json
import os
import re

import numpy as np
from openai import OpenAI

from config import clave_openai
from rank_bm25 import BM25Okapi

_cliente = OpenAI(api_key=clave_openai())

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = "text-embedding-3-small"
K_RRF = 60

with open(os.path.join(AQUI, "indice_auco.json"), encoding="utf-8") as f:
    _meta = json.load(f)
_CHUNKS = _meta["chunks"]
_VECTORES = np.load(os.path.join(AQUI, "indice_auco.npy"))

_BM25 = BM25Okapi([re.findall(r"\w+", c["texto"].lower()) for c in _CHUNKS])


def _embedding(texto):
    return _cliente.embeddings.create(model=MODELO, input=[texto]).data[0].embedding


def semantica(consulta, n=10):
    q = np.array(_embedding(consulta), dtype=np.float32)
    q /= np.linalg.norm(q)
    # Vectores ya normalizados al indexar: coseno == producto punto
    puntajes = _VECTORES @ q
    return list(np.argsort(-puntajes)[:n])


def literal(consulta, n=10):
    puntajes = _BM25.get_scores(re.findall(r"\w+", consulta.lower()))
    return list(np.argsort(-puntajes)[:n])


def buscar(consulta, n=4):
    """Fusion por Reciprocal Rank Fusion."""
    puntos = {}
    for ranking in (semantica(consulta), literal(consulta)):
        for posicion, idx in enumerate(ranking):
            puntos[idx] = puntos.get(idx, 0) + 1.0 / (K_RRF + posicion + 1)

    mejores = sorted(puntos, key=puntos.get, reverse=True)[:n]
    return [dict(_CHUNKS[i], score=puntos[i]) for i in mejores]


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print(f"  indice: {_meta['total']} fragmentos\n")
    for q in ["que parametros necesita la validacion biometrica?",
              "como valido que la foto sea de la misma persona del documento?",
              "puedo cancelar un documento ya enviado?"]:
        print(f"  {q}")
        for c in buscar(q, n=3):
            print(f"     {c['score']:.4f} [{c['fuente'][:34]}] {c['seccion'][:40]}")
        print()
