# -*- coding: utf-8 -*-
"""Un unico sitio donde se resuelve la clave de OpenAI.

Antes cada modulo hacia load_dotenv() contra una ruta absoluta de la
maquina de desarrollo. Eso no filtraba nada —la clave nunca estuvo en
este proyecto— pero esa carpeta no existe en el servidor, asi que la app
habria arrancado sin clave y fallado en la primera pregunta.

Orden de busqueda, del entorno de produccion al de desarrollo:

  1. Variable de entorno OPENAI_API_KEY
     Es lo que usa Streamlit Cloud cuando app.py copia st.secrets al
     entorno antes de importar nada.

  2. .env en esta misma carpeta
     Para desarrollo local y para quien clone el repositorio.

Hubo un tercer candidato, el .env del proyecto del RAG, para no tener dos
copias de la clave en la maquina. Se quito: ataba este demo a la ruta de
otro proyecto, y bastaba mover o renombrar aquella carpeta para romper
este. Una copia mas de la clave es barata; una dependencia invisible
entre dos proyectos, no.

Si no aparece por ningun lado, se falla con un mensaje claro en vez de
dejar que openai lance un 401 diez pasos mas adelante.
"""

import os

from dotenv import load_dotenv

AQUI = os.path.dirname(os.path.abspath(__file__))

_CANDIDATOS = [os.path.join(AQUI, ".env")]


def clave_openai():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]

    for ruta in _CANDIDATOS:
        if os.path.exists(ruta):
            load_dotenv(ruta)
            if os.environ.get("OPENAI_API_KEY"):
                return os.environ["OPENAI_API_KEY"]

    raise RuntimeError(
        "Falta OPENAI_API_KEY.\n"
        "  - En local: crea un archivo .env en esta carpeta con "
        "OPENAI_API_KEY=sk-...\n"
        "  - En Streamlit Cloud: anadela en Settings > Secrets."
    )
