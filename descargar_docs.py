# -*- coding: utf-8 -*-
"""Descarga la documentacion publica de docs.auco.ai para el demo.

Condiciones que se respetan, y conviene dejarlas escritas:

  - Solo contenido PUBLICO. Nada detras de login.
  - robots.txt dice "Allow: /" y el sitio publica un sitemap: exactamente
    lo que un sitio ofrece cuando quiere ser indexado.
  - Una peticion por segundo. 65 paginas en poco mas de un minuto no le
    hacen cosquillas a nadie, pero no hay razon para ir mas rapido.
  - User-Agent identificable, no disfrazado de navegador.

El resultado es un demo tecnico, no un producto ni algo afiliado a AUCO,
y asi debe decirlo la pagina donde se publique.
"""

import os
import re
import time
import urllib.request

from bs4 import BeautifulSoup

SITEMAP = "https://docs.auco.ai/sitemap.xml"
DESTINO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs_auco")
PAUSA = 1.0
UA = "demo-portafolio-ferney (+https://ferney-portfolio.vercel.app)"


def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def extraer(html):
    """Saca el contenido util y descarta la cascara del sitio."""
    sopa = BeautifulSoup(html, "lxml")

    # Fuera lo que no es contenido: menus, scripts, barra lateral
    for tag in sopa(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # La documentacion suele vivir en <main> o <article>
    cuerpo = sopa.find("main") or sopa.find("article") or sopa.body
    if cuerpo is None:
        return "", ""

    h1 = cuerpo.find("h1")
    titulo = h1.get_text(strip=True) if h1 else ""

    # Las TABLAS son lo mas valioso de una documentacion de API: ahi viven
    # los parametros, sus tipos y si son obligatorios. La primera version
    # las perdia y dejaba secciones como "Parametros de consulta" vacias,
    # que es justo lo que un desarrollador viene a preguntar.
    for tabla in cuerpo.find_all("table"):
        filas = []
        for tr in tabla.find_all("tr"):
            celdas = [td.get_text(" ", strip=True) for td in tr.find_all(["th", "td"])]
            if any(celdas):
                filas.append(" | ".join(celdas))
        # Ojo con el detalle: hay que reemplazarla por una ETIQUETA, no por
        # texto suelto. El bucle de abajo recorre tags concretos, asi que
        # una cadena plana queda en el arbol y no la recoge nadie. Es el
        # bug que dejaba "Parametros de consulta" vacio.
        if filas:
            nuevo = sopa.new_tag("p")
            nuevo.string = "PARAMETROS: " + " ;; ".join(filas)
            tabla.replace_with(nuevo)
        else:
            tabla.decompose()

    partes = []
    for el in cuerpo.find_all(["h1", "h2", "h3", "p", "li", "code", "pre"]):
        # Un <code> dentro de un <pre> ya lo capturo el <pre>: evita el doble
        if el.name == "code" and el.find_parent("pre"):
            continue
        t = el.get_text(" ", strip=True)
        if not t or len(t) < 3:
            continue
        if el.name in ("h1", "h2", "h3"):
            partes.append(f"\n## {t}")
        elif el.name in ("code", "pre") and len(t) < 600:
            partes.append(f"`{t}`")
        else:
            partes.append(t)

    # Las pestanas de la documentacion (Curl / Python / Node) repiten el
    # mismo bloque; se quitan las lineas identicas consecutivas.
    limpias, anterior = [], None
    for linea in partes:
        if linea != anterior:
            limpias.append(linea)
        anterior = linea

    texto = "\n".join(limpias)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return titulo, texto.strip()


def main():
    os.makedirs(DESTINO, exist_ok=True)

    xml = bajar(SITEMAP)
    urls = [u for u in re.findall(r"<loc>(.*?)</loc>", xml) if "/search" not in u]
    print(f"  {len(urls)} paginas en el sitemap\n")

    guardadas, vacias = 0, 0
    for i, url in enumerate(urls, 1):
        ruta = url.replace("https://docs.auco.ai/", "").strip("/") or "inicio"
        nombre = ruta.replace("/", "__") + ".md"
        try:
            titulo, texto = extraer(bajar(url))
        except Exception as e:
            print(f"  [{i:2}/{len(urls)}] ERROR {ruta}: {str(e)[:40]}")
            continue

        if len(texto) < 120:          # pagina sin contenido util
            vacias += 1
            print(f"  [{i:2}/{len(urls)}] vacia  {ruta}")
        else:
            with open(os.path.join(DESTINO, nombre), "w", encoding="utf-8") as f:
                f.write(f"# {titulo or ruta}\n\n")
                f.write(f"> Fuente: {url}\n\n")
                f.write(texto)
            guardadas += 1
            print(f"  [{i:2}/{len(urls)}] ok     {ruta[:46]:46} {len(texto):5} car")

        time.sleep(PAUSA)

    print(f"\n  guardadas: {guardadas}   sin contenido: {vacias}")
    print(f"  destino: {DESTINO}")


if __name__ == "__main__":
    main()
