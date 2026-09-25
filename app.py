# -*- coding: utf-8 -*-
"""Interfaz del demo.

Lo que distingue este demo de cualquier chatbot: ademas de responder,
ENSENA SU RAZONAMIENTO. Cada respuesta trae el recorrido que hizo el
grafo — cuando reformulo la busqueda, cuando se rindio, cuando descarto
su propia respuesta por no estar respaldada.

Ese es el punto. Un chatbot que responde bien no se distingue de uno que
responde bien por casualidad; uno que muestra por donde paso, si.
"""

import os
import uuid

import streamlit as st

st.set_page_config(page_title="Asistente sobre la documentación de AUCO",
                   page_icon="📄", layout="centered")

# En Streamlit Cloud la clave vive en Settings > Secrets. Se copia al
# entorno ANTES de importar el grafo, porque config.py la busca ahi
# primero. En local no hay secrets y se cae al .env, que es lo que se
# quiere. Nunca se imprime ni se muestra.
try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass          # sin secrets configurados: config.py probara el .env

# Tope por sesion: cada pregunta dispara entre 4 y 6 llamadas al modelo,
# asi que un demo publico sin limite es una factura esperando a ocurrir.
MAX_PREGUNTAS = 12


@st.cache_resource(show_spinner=False)
def cargar():
    """Se construye una vez por proceso, no en cada mensaje."""
    from grafo import construir
    return construir()


st.title("📄 Asistente sobre la documentación de AUCO")
st.caption(
    "Demostración técnica construida sobre la documentación pública de "
    "[docs.auco.ai](https://docs.auco.ai) · **No es un producto de AUCO ni está "
    "afiliado a AUCO** · Construido por "
    "[Ferney Quintero](https://ferney-portfolio.vercel.app)"
)

with st.sidebar:
    st.header("Cómo está construido")
    st.markdown("""
Un grafo de **LangGraph** con cuatro decisiones, no un RAG lineal:

1. **Contexto** — resuelve la pregunta contra la conversación previa
2. **Búsqueda** — híbrida: BM25 + embeddings, fusionados con RRF
3. **Evaluación** — ¿lo encontrado responde de verdad?
4. **Reformulación** — si no, traduce al vocabulario técnico y reintenta
5. **Verificación** — revisa la respuesta **antes** de entregarla

Si la respuesta no queda respaldada por las fuentes, **se descarta**.
Eso no es una instrucción en el prompt: es una compuerta del grafo.
""")
    st.divider()
    st.caption("**Índice**: 501 fragmentos de 64 páginas de documentación")
    st.caption("**Modelos**: GPT-4o para redactar · GPT-4o-mini para decidir")
    st.markdown("[Código en GitHub](https://github.com/ferquintero2013)")

st.info(
    "Pregunta sobre la API o los SDK de AUCO: validación biométrica, firma "
    "electrónica, webhooks, cancelación de documentos, background check…",
    icon="💡",
)

# Un hilo por sesion del navegador: el checkpointer guarda su estado aparte
if "hilo" not in st.session_state:
    st.session_state.hilo = str(uuid.uuid4())
    st.session_state.mensajes = []

for m in st.session_state.mensajes:
    with st.chat_message(m["rol"]):
        st.markdown(m["texto"])
        if m.get("traza"):
            with st.expander("Ver cómo lo resolvió"):
                for p in m["traza"]:
                    st.markdown(f"**{p['paso']}** · {p['detalle']}")
        if m.get("fuentes"):
            st.caption("Fuentes: " + " · ".join(
                f"[{f['seccion'][:36]}]({f['url']})" for f in m["fuentes"]))

usadas = sum(1 for m in st.session_state.mensajes if m["rol"] == "user")

if usadas >= MAX_PREGUNTAS:
    st.warning(
        f"Límite de {MAX_PREGUNTAS} preguntas por sesión alcanzado — es una "
        "demostración, no un servicio. Recarga la página para empezar de nuevo.",
        icon="🔒")
elif pregunta := st.chat_input("¿Qué quieres saber de la documentación?"):
    st.session_state.mensajes.append({"rol": "user", "texto": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en la documentación…"):
            try:
                estado = cargar().invoke(
                    {"pregunta": pregunta},
                    config={"configurable": {"thread_id": st.session_state.hilo}})
            except Exception as e:
                st.error(f"Algo falló: {type(e).__name__}")
                st.stop()

        st.markdown(estado["respuesta"])

        traza = estado.get("traza", [])
        if traza:
            with st.expander("Ver cómo lo resolvió"):
                for p in traza:
                    st.markdown(f"**{p['paso']}** · {p['detalle']}")

        # Solo se muestran fuentes si la respuesta salio de ellas
        fuentes = []
        if estado.get("respaldada") and estado.get("documentos"):
            vistas = set()
            for d in estado["documentos"]:
                if d["url"] in vistas:
                    continue
                vistas.add(d["url"])
                # "(intro)" no le dice nada a nadie: cuando la seccion no
                # tiene nombre util, se usa la ruta de la pagina.
                etiqueta = d["seccion"].strip()
                if etiqueta in ("(intro)", "") or len(etiqueta) < 4:
                    etiqueta = (d["url"].replace("https://docs.auco.ai/", "")
                                .replace("/", " / ") or "documentación")
                fuentes.append({"seccion": etiqueta, "url": d["url"]})
            st.caption("Fuentes: " + " · ".join(
                f"[{f['seccion'][:36]}]({f['url']})" for f in fuentes))

    st.session_state.mensajes.append({"rol": "assistant", "texto": estado["respuesta"],
                                      "traza": traza, "fuentes": fuentes})
