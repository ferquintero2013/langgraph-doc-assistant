# -*- coding: utf-8 -*-
"""PASO 1 — Las tres piezas de LangGraph, sin LLM de por medio.

La idea aqui no es hacer nada util, es ver como se mueve el estado.
Sin modelos, sin red: asi el unico concepto nuevo es el grafo.

Las tres piezas:

  ESTADO   un diccionario que viaja por todo el grafo. Cada nodo lo lee
           y devuelve los campos que quiere cambiar.

  NODO     una funcion normal. Recibe el estado, devuelve un dict con lo
           que cambia. NO devuelve el estado entero: solo el trozo suyo,
           y LangGraph lo fusiona.

  ARISTA   quien va despues de quien. START y END son los extremos.
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ---------------------------------------------------------------- ESTADO
# TypedDict, no una clase. LangGraph necesita saber que campos existen
# para poder fusionar lo que devuelve cada nodo.
class Estado(TypedDict):
    pregunta: str
    consulta: str
    resultado: str
    intentos: int


# ----------------------------------------------------------------- NODOS
def limpiar(estado: Estado) -> dict:
    """Primer nodo: normaliza la pregunta."""
    print(f"   [limpiar]  entra: {estado['pregunta']!r}")
    consulta = estado["pregunta"].strip().lower()
    # Fijate en lo que se devuelve: SOLO los campos que este nodo cambia.
    return {"consulta": consulta, "intentos": estado.get("intentos", 0) + 1}


def buscar(estado: Estado) -> dict:
    """Segundo nodo: usa lo que dejo el anterior."""
    print(f"   [buscar]   recibe consulta: {estado['consulta']!r}")
    # Un "indice" de mentira, para no depender de nada externo
    indice = {"python": "Construyo un sistema de diagnostico en Python.",
              "odoo": "Implemento Odoo en tres paises."}
    encontrado = next((v for k, v in indice.items() if k in estado["consulta"]), "")
    return {"resultado": encontrado or "(sin resultados)"}


# ----------------------------------------------------------------- GRAFO
constructor = StateGraph(Estado)

constructor.add_node("limpiar", limpiar)
constructor.add_node("buscar", buscar)

# El flujo: empieza -> limpiar -> buscar -> termina
constructor.add_edge(START, "limpiar")
constructor.add_edge("limpiar", "buscar")
constructor.add_edge("buscar", END)

grafo = constructor.compile()


if __name__ == "__main__":
    print("\nEJECUCION 1 — algo que si esta en el indice")
    final = grafo.invoke({"pregunta": "  Que sabe de PYTHON?  "})
    print(f"   estado final: {final}\n")

    print("EJECUCION 2 — algo que no esta")
    final = grafo.invoke({"pregunta": "sabe kubernetes?"})
    print(f"   estado final: {final}\n")
