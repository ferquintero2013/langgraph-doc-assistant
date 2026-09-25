# -*- coding: utf-8 -*-
"""PASO 3 — El chatbot completo, ya con modelo de lenguaje.

Que cambia respecto al paso 2: los tres nodos que antes eran diccionarios
de mentira ahora llaman a un modelo. La estructura del grafo NO cambia —
es la misma de antes. Eso es justamente lo que se quiere ver: el grafo es
el esqueleto, los nodos son intercambiables.

Lo nuevo que hay que aprender aqui:

  1. Llamar a un LLM dentro de un nodo no tiene nada especial. Un nodo es
     una funcion; dentro puede pasar lo que sea.

  2. SALIDA ESTRUCTURADA para las decisiones. El nodo evaluar tiene que
     devolver si/no, y de eso depende por donde sigue el grafo. Pedirle
     texto libre al modelo y buscar "si" con un if seria fragil — es el
     mismo error de buscar subcadenas. Se le pide JSON.

  3. Un nodo NUEVO: verificar. Revisa la respuesta ANTES de entregarla.
     Esa es la diferencia entre pedirle al modelo que se porte bien (una
     regla de prompt, que es una peticion) y comprobarlo (una compuerta
     del grafo, que es una garantia).

La documentacion sigue siendo falsa, escrita al estilo de un producto de
firma electronica y validacion de identidad.
"""

import json
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from openai import OpenAI

from config import clave_openai

cliente = OpenAI(api_key=clave_openai())

MODELO_BARATO = "gpt-4o-mini"   # decisiones mecanicas
MODELO_BUENO = "gpt-4o"         # redactar la respuesta al cliente
MAX_INTENTOS = 2


# ------------------------------------------ documentacion de mentira
DOCS = [
    {
        "titulo": "Reenvio de notificaciones",
        "texto": ("Si el destinatario no recibe el enlace de firma, puede reenviarse "
                  "desde el panel en Documentos > Acciones > Reenviar notificacion. "
                  "El reenvio no invalida el enlace anterior."),
    },
    {
        "titulo": "Requisitos de calidad de imagen",
        "texto": ("La validacion biometrica exige fotos sin reflejos, con los cuatro "
                  "bordes del documento visibles y resolucion minima de 1024 px de "
                  "ancho. Las capturas de pantalla no son aceptadas."),
    },
    {
        "titulo": "Validez juridica de la firma electronica",
        "texto": ("La firma electronica tiene plena validez juridica en Colombia bajo "
                  "la Ley 527 de 1999, siempre que se conserve la trazabilidad del "
                  "firmante y la integridad del documento."),
    },
    {
        "titulo": "Revocacion de documentos",
        "texto": ("Un documento ya firmado por todas las partes no puede revocarse. "
                  "Si aun hay firmas pendientes, el emisor puede cancelarlo desde el "
                  "panel, lo que anula los enlaces enviados."),
    },
]


def llm(modelo, sistema, usuario, json_mode=False, max_tokens=400):
    """Envoltorio minimo para no repetir la llamada en cada nodo."""
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    r = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "system", "content": sistema},
                  {"role": "user", "content": usuario}],
        temperature=0,
        max_tokens=max_tokens,
        **kwargs,
    )
    return r.choices[0].message.content


# ---------------------------------------------------------------- ESTADO
class Estado(TypedDict):
    pregunta: str        # lo que escribio el cliente; nunca se modifica
    consulta: str        # lo que se busca; cambia en cada vuelta del ciclo
    documentos: list
    intentos: int
    sirve: bool
    respuesta: str
    respaldada: bool     # veredicto del verificador
    traza: list          # por donde paso, para poder explicarlo despues


# ----------------------------------------------------------------- NODOS
def buscar(estado: Estado) -> dict:
    """Busqueda a proposito simple: por palabras.

    En produccion seria hibrida (BM25 + embeddings). Se deja simple aqui
    porque el objetivo es ver el ciclo: con busqueda por palabras, la
    brecha de vocabulario entre cliente y documentacion es visible.
    """
    palabras = {p for p in estado["consulta"].lower().split() if len(p) > 3}
    encontrados = []
    for d in DOCS:
        texto = (d["titulo"] + " " + d["texto"]).lower()
        if sum(1 for p in palabras if p in texto) >= 2:
            encontrados.append(d)

    traza = estado.get("traza", []) + [f"buscar({estado['consulta'][:40]!r}) -> {len(encontrados)}"]
    print(f"   [buscar]      {estado['consulta'][:52]!r} -> {len(encontrados)} doc(s)")
    return {"documentos": encontrados,
            "intentos": estado.get("intentos", 0) + 1,
            "traza": traza}


def evaluar(estado: Estado) -> dict:
    """Decide si lo recuperado responde de verdad.

    SALIDA ESTRUCTURADA: se pide JSON porque de este veredicto depende el
    camino del grafo. Parsear texto libre para decidir un flujo es como
    buscar subcadenas para decidir si una frase afirma o niega: funciona
    hasta que no.
    """
    if not estado["documentos"]:
        print("   [evaluar]     sin documentos -> no sirve")
        return {"sirve": False, "traza": estado["traza"] + ["evaluar -> no (vacio)"]}

    contexto = "\n".join(f"- {d['titulo']}: {d['texto']}" for d in estado["documentos"])
    bruto = llm(
        MODELO_BARATO,
        # Calibrar este prompt es lo mas delicado del grafo: de aqui sale el
        # camino que se toma. La primera version decia "solo si la respuesta
        # esta contenida en los fragmentos", y era demasiado literal —
        # rechazaba el documento de reenvio porque el cliente dijo "WhatsApp"
        # y la documentacion dice "enlace de firma". Tecnicamente cierto,
        # practicamente inservible.
        ("Decides si unos fragmentos de documentacion permiten dar al cliente "
         "una respuesta UTIL. Responde SOLO un JSON: "
         '{"sirve": true|false, "razon": "una frase"}.\n'
         "sirve=true si con esos fragmentos el cliente sale sabiendo que hacer, "
         "aunque no usen sus mismas palabras: el cliente escribe coloquial y la "
         "documentacion es formal.\n"
         "sirve=false solo si el tema simplemente no esta cubierto.\n"
         "Ojo: un fragmento que dice que algo NO se puede hacer SI responde la "
         "pregunta de si se puede."),
        f"PREGUNTA DEL CLIENTE:\n{estado['pregunta']}\n\nFRAGMENTOS:\n{contexto}",
        json_mode=True, max_tokens=120,
    )
    veredicto = json.loads(bruto)
    print(f"   [evaluar]     sirve={veredicto['sirve']} — {veredicto.get('razon','')[:58]}")
    return {"sirve": bool(veredicto["sirve"]),
            "traza": estado["traza"] + [f"evaluar -> {veredicto['sirve']}"]}


def reformular(estado: Estado) -> dict:
    """Traduce del lenguaje del cliente al de la documentacion."""
    titulos = ", ".join(d["titulo"] for d in DOCS)
    nueva = llm(
        MODELO_BARATO,
        ("Reescribe la pregunta de un cliente usando el vocabulario tecnico de "
         "la documentacion del producto. El cliente escribe coloquial; la "
         "documentacion usa terminos formales. Devuelve SOLO la consulta "
         "reescrita, sin comillas ni explicacion.\n"
         f"Secciones disponibles en la documentacion: {titulos}"),
        f"Pregunta del cliente: {estado['pregunta']}\n"
        f"Ya se busco esto y no funciono: {estado['consulta']}",
        max_tokens=60,
    ).strip()
    print(f"   [reformular]  -> {nueva[:56]!r}")
    return {"consulta": nueva, "traza": estado["traza"] + [f"reformular -> {nueva[:30]}"]}


def responder(estado: Estado) -> dict:
    """Redacta la respuesta al cliente. Aqui si vale el modelo bueno."""
    if not estado["documentos"]:
        texto = ("No encuentro eso en la documentacion. Puedo pasarte con el "
                 "equipo de soporte si lo necesitas.")
        print("   [responder]   declina (sin cobertura)")
        return {"respuesta": texto, "respaldada": True,
                "traza": estado["traza"] + ["responder -> declina"]}

    contexto = "\n".join(f"[{d['titulo']}]\n{d['texto']}" for d in estado["documentos"])
    texto = llm(
        MODELO_BUENO,
        ("Eres el asistente de soporte de un producto de firma electronica y "
         "validacion de identidad. Responde al cliente en 2-3 frases, claro y "
         "directo, usando UNICAMENTE la documentacion que se te entrega. "
         "Cierra citando la seccion entre corchetes. Si la documentacion no "
         "alcanza, dilo en vez de completar."),
        f"PREGUNTA:\n{estado['pregunta']}\n\nDOCUMENTACION:\n{contexto}",
    )
    print(f"   [responder]   redactada ({len(texto)} car)")
    return {"respuesta": texto, "traza": estado["traza"] + ["responder"]}


def verificar(estado: Estado) -> dict:
    """NODO NUEVO — revisa la respuesta antes de entregarla.

    Esta es la diferencia entre pedir y comprobar. En el RAG del portafolio
    la regla "no inventes" vive en el prompt: es una peticion al modelo. Un
    nodo que revisa la salida es una compuerta.

    En un producto de KYC importa: una respuesta inventada sobre validez
    legal no es una molestia, es un problema para el cliente del cliente.
    """
    if not estado["documentos"]:
        return {"respaldada": True}

    contexto = "\n".join(d["texto"] for d in estado["documentos"])
    bruto = llm(
        MODELO_BARATO,
        ('Revisas si una respuesta esta respaldada por la documentacion. '
         'Responde SOLO JSON: {"respaldada": true|false, "razon": "una frase"}. '
         "respaldada=false si la respuesta afirma algo que no esta en la "
         "documentacion, aunque suene razonable."),
        f"DOCUMENTACION:\n{contexto}\n\nRESPUESTA A REVISAR:\n{estado['respuesta']}",
        json_mode=True, max_tokens=120,
    )
    v = json.loads(bruto)
    marca = "OK" if v["respaldada"] else "NO RESPALDADA"
    print(f"   [verificar]   {marca} — {v.get('razon','')[:52]}")
    return {"respaldada": bool(v["respaldada"]),
            "traza": estado["traza"] + [f"verificar -> {v['respaldada']}"]}


# ------------------------------------------------- ARISTAS CONDICIONALES
def tras_evaluar(estado: Estado) -> str:
    if estado["sirve"]:
        return "responder"
    if estado["intentos"] >= MAX_INTENTOS:
        print(f"   [decidir]     tope de {MAX_INTENTOS}, declina")
        return "responder"
    return "reformular"


def tras_verificar(estado: Estado) -> str:
    """Si la respuesta no esta respaldada, se descarta y se declina.

    Se podria reintentar la redaccion, pero declinar es mas honesto: si el
    modelo se invento algo con esta documentacion, con la misma es probable
    que lo repita.
    """
    return "fin" if estado["respaldada"] else "declinar"


def declinar(estado: Estado) -> dict:
    print("   [declinar]    respuesta descartada por el verificador")
    return {"respuesta": ("Prefiero no responder eso: no encuentro respaldo suficiente "
                          "en la documentacion. Te paso con soporte."),
            "traza": estado["traza"] + ["DESCARTADA"]}


# ----------------------------------------------------------------- GRAFO
constructor = StateGraph(Estado)
for nombre, fn in [("buscar", buscar), ("evaluar", evaluar), ("reformular", reformular),
                   ("responder", responder), ("verificar", verificar), ("declinar", declinar)]:
    constructor.add_node(nombre, fn)

constructor.add_edge(START, "buscar")
constructor.add_edge("buscar", "evaluar")
constructor.add_conditional_edges("evaluar", tras_evaluar,
                                  {"reformular": "reformular", "responder": "responder"})
constructor.add_edge("reformular", "buscar")          # ciclo 1: volver a buscar
constructor.add_edge("responder", "verificar")
constructor.add_conditional_edges("verificar", tras_verificar,
                                  {"fin": END, "declinar": "declinar"})
constructor.add_edge("declinar", END)

grafo = constructor.compile()


if __name__ == "__main__":
    PREGUNTAS = [
        "no me llega el link al whatsapp",
        "la foto de la cedula sale borrosa y no me deja continuar",
        "puedo echar para atras un documento que ya firmaron todos?",
        "ustedes aceptan pagos con criptomonedas?",
    ]

    for p in PREGUNTAS:
        print(f"\n{'='*74}\nCLIENTE: {p}")
        final = grafo.invoke({"pregunta": p, "consulta": p, "intentos": 0, "traza": []})
        print(f"\n   BOT: {final['respuesta']}")
        print(f"   traza: {' -> '.join(final['traza'])}")
