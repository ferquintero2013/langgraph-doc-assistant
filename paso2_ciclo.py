# -*- coding: utf-8 -*-
"""PASO 2 — La decision y el ciclo, que es lo que LangGraph aporta.

Sigue sin LLM: la evaluacion y la reformulacion estan simuladas con
diccionarios. Asi el unico concepto nuevo es el ciclo, no la llamada al
modelo. Eso viene en el paso 3.

El problema que se simula es real: en soporte, el cliente escribe
"no me llega el link al whatsapp" y la documentacion lo llama
"reenvio de notificaciones". No comparten ni una palabra.

Piezas nuevas frente al paso 1:
  ARISTA CONDICIONAL  despues de evaluar, el grafo decide a donde ir
  CICLO               reformular vuelve a buscar
  TOPE                sin el, un tema no documentado gira para siempre
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END

MAX_INTENTOS = 2


# ---------------------------------------------------------------- ESTADO
class Estado(TypedDict):
    pregunta: str        # lo que escribio el cliente, no se toca
    consulta: str        # lo que se busca; esto si cambia en cada vuelta
    documentos: list     # lo que trajo la busqueda
    intentos: int
    sirve: bool          # veredicto del evaluador
    respuesta: str


# ------------------------------------------- documentacion de mentira
# Escrita como la escribiria AUCO: vocabulario tecnico y legal.
DOCS = {
    "reenvio de notificaciones": (
        "Si el destinatario no recibe el enlace de firma, puede reenviarse "
        "desde el panel en Documentos > Acciones > Reenviar notificacion."
    ),
    "requisitos de calidad de imagen": (
        "La validacion biometrica exige imagenes sin reflejos, con los cuatro "
        "bordes del documento visibles y resolucion minima de 1024px."
    ),
    "validez juridica de la firma": (
        "La firma electronica tiene plena validez juridica en Colombia bajo la "
        "Ley 527 de 1999, siempre que se conserve la trazabilidad del firmante."
    ),
}

# Como traduciria un modelo del lenguaje del cliente al de la documentacion.
# En el paso 3 esto lo hara gpt-4o-mini de verdad.
TRADUCCIONES = {
    "no me llega el link al whatsapp": "reenvio de notificaciones",
    "la foto de la cedula sale borrosa": "requisitos de calidad de imagen",
    "esto tiene validez legal": "validez juridica de la firma",
}


# ----------------------------------------------------------------- NODOS
def buscar(estado: Estado) -> dict:
    consulta = estado["consulta"]
    encontrados = [t for clave, t in DOCS.items() if clave in consulta.lower()]
    print(f"   [buscar]      {consulta!r}  ->  {len(encontrados)} doc(s)")
    return {"documentos": encontrados, "intentos": estado.get("intentos", 0) + 1}


def evaluar(estado: Estado) -> dict:
    """El nodo que NO existe en un RAG lineal.

    Aqui se pregunta si lo recuperado responde de verdad. En el paso 3 lo
    decide un modelo; por ahora basta con si vino algo.
    """
    sirve = len(estado["documentos"]) > 0
    print(f"   [evaluar]     sirve lo que encontre? {'si' if sirve else 'NO'}")
    return {"sirve": sirve}


def reformular(estado: Estado) -> dict:
    """Traduce del lenguaje del cliente al de la documentacion."""
    original = estado["pregunta"].lower()
    nueva = next((v for k, v in TRADUCCIONES.items() if k in original),
                 estado["consulta"])
    print(f"   [reformular]  {estado['consulta']!r}  ->  {nueva!r}")
    return {"consulta": nueva}


def responder(estado: Estado) -> dict:
    if estado["documentos"]:
        texto = " ".join(estado["documentos"])
    else:
        # Que declina tras agotar los intentos NO es un fracaso: es la
        # senal de que ese tema no esta documentado.
        texto = ("No encuentro eso en la documentacion. "
                 "[!] Pregunta sin cobertura — revisar.")
    print(f"   [responder]   ({estado['intentos']} busqueda/s)")
    return {"respuesta": texto}


# --------------------------------------------------- LA ARISTA CONDICIONAL
def a_donde_voy(estado: Estado) -> str:
    """Devuelve el NOMBRE del siguiente nodo. Aqui vive la decision."""
    if estado["sirve"]:
        return "responder"
    if estado["intentos"] >= MAX_INTENTOS:
        print(f"   [decidir]     tope de {MAX_INTENTOS} alcanzado, me rindo")
        return "responder"
    return "reformular"


# ----------------------------------------------------------------- GRAFO
constructor = StateGraph(Estado)

constructor.add_node("buscar", buscar)
constructor.add_node("evaluar", evaluar)
constructor.add_node("reformular", reformular)
constructor.add_node("responder", responder)

constructor.add_edge(START, "buscar")
constructor.add_edge("buscar", "evaluar")

# En vez de una arista fija, una funcion decide el destino
constructor.add_conditional_edges(
    "evaluar",
    a_donde_voy,
    {"reformular": "reformular", "responder": "responder"},
)

# EL CICLO: reformular no avanza, retrocede a buscar
constructor.add_edge("reformular", "buscar")
constructor.add_edge("responder", END)

grafo = constructor.compile()


if __name__ == "__main__":
    PREGUNTAS = [
        "no me llega el link al whatsapp",          # falla y se recupera
        "reenvio de notificaciones",                # acierta a la primera
        "puedo pagar con criptomonedas?",           # no existe: agota y declina
    ]

    for p in PREGUNTAS:
        print(f"\nCLIENTE: {p}")
        final = grafo.invoke({"pregunta": p, "consulta": p, "intentos": 0})
        print(f"   BOT: {final['respuesta'][:110]}")
