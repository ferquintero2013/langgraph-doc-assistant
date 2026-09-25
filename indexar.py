# -*- coding: utf-8 -*-
"""Trocea la documentacion de AUCO y construye el indice.

Mismo patron que el RAG del portafolio, a proposito: si ya entendiste
aquel, aqui no hay nada nuevo salvo el corpus.

  CHUNKING ESTRUCTURAL   se corta por encabezados, no cada N caracteres.
                         Una seccion "Parametros de consulta" es una
                         unidad de sentido; partirla por la mitad deja
                         fragmentos que no responden nada.

  VECTORES NORMALIZADOS  se normalizan al indexar, una sola vez. Asi la
                         similitud coseno se reduce a un producto punto
                         y la busqueda es una multiplicacion de matrices.

  SIN BASE VECTORIAL     con este volumen no hace falta. Igual que en el
                         portafolio: se midio antes de decidir.
"""

import json
import os
import re

import numpy as np
from openai import OpenAI

from config import clave_openai

cliente = OpenAI(api_key=clave_openai())

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, "docs_auco")
INDICE = os.path.join(AQUI, "indice_auco.json")
VECTORES = os.path.join(AQUI, "indice_auco.npy")

MODELO = "text-embedding-3-small"
LOTE = 100
MAX_CHUNK = 1800   # caracteres; por encima de esto se parte la seccion


def encabezado(texto):
    """De que trata la pagina: su titulo y el endpoint que documenta.

    Hace falta porque el troceado por '##' separa cada seccion de la
    identidad de su pagina. El fragmento 'Parametros de consulta' de la
    validacion biometrica queda, por si solo, indistinguible de los otros
    treinta fragmentos titulados igual en el corpus: no contiene la
    palabra 'biometrica' ni el endpoint, esos viven en la intro.

    Ese fue un error real: el bot respondio que /veriface/validate "no
    requiere parametros" porque el buscador nunca le trajo la tabla.
    """
    titulo, endpoint = "", ""
    for linea in texto.split("\n"):
        linea = linea.strip()
        if not titulo and linea.startswith("# "):
            titulo = linea[2:].strip().replace("_", "/")
        # El endpoint aparece como una linea suelta entre backticks: `/veriface/validate`
        elif not endpoint and re.fullmatch(r"`/[\w/{}.-]+`", linea):
            endpoint = linea.strip("`")
        if titulo and endpoint:
            break
    return " · ".join(p for p in (titulo, endpoint) if p)


def trocear(texto, fuente, url):
    """Corta por encabezados '##' y parte las secciones demasiado largas."""
    contexto = encabezado(texto)
    bloques = re.split(r"\n(?=## )", texto)
    chunks = []
    for b in bloques:
        b = b.strip()
        if len(b) < 60:                     # fragmento sin sustancia
            continue
        titulo = b.split("\n")[0].lstrip("# ").strip() if b.startswith("##") else "(intro)"
        # Cada fragmento se lleva de que pagina y endpoint salio. Va en el
        # texto, no en los metadatos, porque tiene que entrar al embedding
        # y al indice BM25: es justo lo que se busca.
        if contexto:
            b = f"[{contexto}]\n{b}"

        if len(b) <= MAX_CHUNK:
            partes = [b]
        else:
            # Corta por parrafos hasta llenar, para no romper a mitad de frase
            cabecera = f"[{contexto}]\n{titulo}" if contexto else titulo
            partes, actual = [], ""
            for parrafo in b.split("\n"):
                if len(actual) + len(parrafo) > MAX_CHUNK and actual:
                    partes.append(actual)
                    actual = cabecera + "\n" + parrafo    # cada parte se ubica sola
                else:
                    actual += "\n" + parrafo
            if actual.strip():
                partes.append(actual)

        for p in partes:
            chunks.append({"fuente": fuente, "url": url,
                           "seccion": titulo, "texto": p.strip()})
    return chunks


def embeddings(textos):
    salida = []
    for i in range(0, len(textos), LOTE):
        lote = textos[i:i + LOTE]
        r = cliente.embeddings.create(model=MODELO, input=lote)
        salida.extend(d.embedding for d in r.data)
        print(f"     embebidos {min(i + LOTE, len(textos))}/{len(textos)}")
    return salida


def main():
    archivos = sorted(f for f in os.listdir(ORIGEN) if f.endswith(".md"))
    print(f"  {len(archivos)} archivos en {ORIGEN}\n")

    chunks = []
    for nombre in archivos:
        with open(os.path.join(ORIGEN, nombre), encoding="utf-8") as f:
            contenido = f.read()
        m = re.search(r"^> Fuente: (.+)$", contenido, re.M)
        url = m.group(1).strip() if m else ""
        cuerpo = re.sub(r"^> Fuente: .+$", "", contenido, flags=re.M)
        chunks.extend(trocear(cuerpo, nombre, url))

    print(f"  {len(chunks)} fragmentos\n")

    vectores = np.array(embeddings([c["texto"] for c in chunks]), dtype=np.float32)
    # Normalizar aqui, una vez, en lugar de en cada busqueda
    vectores /= np.linalg.norm(vectores, axis=1, keepdims=True)

    np.save(VECTORES, vectores)
    with open(INDICE, "w", encoding="utf-8") as f:
        json.dump({"modelo": MODELO, "dimensiones": int(vectores.shape[1]),
                   "total": len(chunks), "chunks": chunks}, f, ensure_ascii=False)

    kb = (os.path.getsize(VECTORES) + os.path.getsize(INDICE)) / 1024
    print(f"\n  indice: {len(chunks)} fragmentos, {vectores.shape[1]} dims, {kb:.0f} KB")


if __name__ == "__main__":
    main()
