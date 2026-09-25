# -*- coding: utf-8 -*-
"""PASO 5 — El chatbot con la documentacion real de AUCO.

Es el grafo del paso 4 sin un solo cambio en su estructura. Lo unico que
cambia es de donde salen los documentos: antes cuatro inventados, ahora
501 fragmentos de docs.auco.ai con busqueda hibrida.

Eso es lo que hay que ver: el grafo no se entero. Nodos intercambiables.

DEMOSTRACION TECNICA construida con documentacion publica de AUCO
(docs.auco.ai). No es un producto, ni esta afiliado a AUCO.
"""

import json
import os
from operator import add
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

from config import clave_openai

from buscador import buscar as buscar_docs

cliente = OpenAI(api_key=clave_openai())

MODELO_BARATO = "gpt-4o-mini"
MODELO_BUENO = "gpt-4o"
MAX_INTENTOS = 2

DOMINIO = ("AUCO: firma electronica, validacion de identidad (biometrica y "
           "documental), background check, gestion documental por API y SDK, "
           "webhooks, plantillas de documentos.")


def llm(modelo, sistema, usuario, json_mode=False, max_tokens=500):
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    r = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "system", "content": sistema},
                  {"role": "user", "content": usuario}],
        temperature=0, max_tokens=max_tokens, **kwargs)
    return r.choices[0].message.content


class Estado(TypedDict):
    historial: Annotated[list, add]
    pregunta: str
    consulta: str
    documentos: list
    intentos: int
    sirve: bool
    respuesta: str
    respaldada: bool


def contextualizar(estado: Estado) -> dict:
    historial = estado.get("historial", [])
    if not historial:
        return {"consulta": estado["pregunta"], "intentos": 0}
    conversacion = "\n".join(f"{t['quien']}: {t['texto'][:200]}" for t in historial[-4:])
    nueva = llm(MODELO_BARATO,
                ("Reescribe la ultima pregunta como una pregunta autonoma usando la "
                 "conversacion previa. DEBE NOMBRAR el tema explicitamente: esa frase "
                 "se usa para buscar en documentacion tecnica, y sin el tema no "
                 "encuentra nada. Si ya es autonoma, devuelvela igual. Solo la pregunta."),
                f"CONVERSACION:\n{conversacion}\n\nULTIMA: {estado['pregunta']}",
                max_tokens=80).strip()
    print(f"   [contexto]    -> {nueva[:56]!r}")
    return {"consulta": nueva, "intentos": 0}


def buscar(estado: Estado) -> dict:
    docs = buscar_docs(estado["consulta"], n=4)
    print(f"   [buscar]      {len(docs)} frag. — {docs[0]['seccion'][:36] if docs else '-'}")
    return {"documentos": docs, "intentos": estado.get("intentos", 0) + 1}


def evaluar(estado: Estado) -> dict:
    if not estado["documentos"]:
        return {"sirve": False}
    contexto = "\n\n".join(f"[{d['seccion']}]\n{d['texto'][:600]}" for d in estado["documentos"])
    v = json.loads(llm(
        MODELO_BARATO,
        ("Decides si unos fragmentos de documentacion tecnica permiten responder "
         'UTILMENTE. Responde SOLO JSON: {"sirve": true|false, "razon": "una frase"}. '
         "sirve=true si quien pregunta sale sabiendo que hacer, aunque el vocabulario "
         "no coincida. Un fragmento que dice que algo NO se puede hacer SI responde."),
        f"PREGUNTA:\n{estado['consulta']}\n\nFRAGMENTOS:\n{contexto}",
        json_mode=True, max_tokens=120))
    print(f"   [evaluar]     sirve={v['sirve']}")
    return {"sirve": bool(v["sirve"])}


def reformular(estado: Estado) -> dict:
    nueva = llm(MODELO_BARATO,
                ("Reescribe la consulta con el vocabulario tecnico del producto, para "
                 f"buscar en su documentacion.\nProducto: {DOMINIO}\n"
                 "Usa terminos de API si aplica (endpoint, parametros, webhook). "
                 "Devuelve SOLO la consulta."),
                f"No funciono esta busqueda: {estado['consulta']}",
                max_tokens=60).strip()
    print(f"   [reformular]  -> {nueva[:56]!r}")
    return {"consulta": nueva}


def responder(estado: Estado) -> dict:
    if not estado["documentos"]:
        texto = ("No encuentro eso en la documentacion publica de AUCO. "
                 "Puede que este en el soporte directo del equipo.")
    else:
        contexto = "\n\n".join(
            f"[{d['seccion']}] ({d['url']})\n{d['texto'][:1200]}"
            for d in estado["documentos"])
        texto = llm(MODELO_BUENO,
                    ("Eres un asistente sobre la documentacion de AUCO (firma "
                     "electronica y validacion de identidad). Responde en 2-4 frases, "
                     "claro y tecnico, usando UNICAMENTE la documentacion entregada. "
                     "Si hay parametros o endpoints concretos, nombralos. Cierra con "
                     "la URL de la fuente. Si la documentacion no alcanza, dilo."),
                    f"PREGUNTA:\n{estado['consulta']}\n\nDOCUMENTACION:\n{contexto}")
    print(f"   [responder]   {len(texto)} car")
    return {"respuesta": texto,
            "historial": [{"quien": "usuario", "texto": estado["pregunta"]},
                          {"quien": "bot", "texto": texto}]}


def verificar(estado: Estado) -> dict:
    if not estado["documentos"]:
        return {"respaldada": True}
    contexto = "\n".join(d["texto"][:700] for d in estado["documentos"])
    v = json.loads(llm(
        MODELO_BARATO,
        ('Revisas si una respuesta esta respaldada por la documentacion. SOLO JSON: '
         '{"respaldada": true|false, "razon": "una frase"}. false si afirma algo que '
         "no esta, aunque suene razonable. Nombres de endpoints o parametros "
         "inventados son motivo suficiente."),
        f"DOCUMENTACION:\n{contexto}\n\nRESPUESTA:\n{estado['respuesta']}",
        json_mode=True, max_tokens=120))
    print(f"   [verificar]   {'OK' if v['respaldada'] else 'NO RESPALDADA — ' + v.get('razon','')[:40]}")
    return {"respaldada": bool(v["respaldada"])}


def declinar(estado: Estado) -> dict:
    texto = ("Prefiero no responder eso: no encuentro respaldo suficiente en la "
             "documentacion publica.")
    return {"respuesta": texto,
            "historial": [{"quien": "usuario", "texto": estado["pregunta"]},
                          {"quien": "bot", "texto": texto}]}


def tras_evaluar(estado):
    if estado["sirve"]:
        return "responder"
    return "responder" if estado["intentos"] >= MAX_INTENTOS else "reformular"


def tras_verificar(estado):
    return "fin" if estado["respaldada"] else "declinar"


constructor = StateGraph(Estado)
for n, f in [("contextualizar", contextualizar), ("buscar", buscar), ("evaluar", evaluar),
             ("reformular", reformular), ("responder", responder),
             ("verificar", verificar), ("declinar", declinar)]:
    constructor.add_node(n, f)

constructor.add_edge(START, "contextualizar")
constructor.add_edge("contextualizar", "buscar")
constructor.add_edge("buscar", "evaluar")
constructor.add_conditional_edges("evaluar", tras_evaluar,
                                  {"reformular": "reformular", "responder": "responder"})
constructor.add_edge("reformular", "buscar")
constructor.add_edge("responder", "verificar")
constructor.add_conditional_edges("verificar", tras_verificar,
                                  {"fin": END, "declinar": "declinar"})
constructor.add_edge("declinar", END)

grafo = constructor.compile(checkpointer=MemorySaver())


def preguntar(texto, hilo="demo"):
    print(f"\nUSUARIO: {texto}")
    e = grafo.invoke({"pregunta": texto}, config={"configurable": {"thread_id": hilo}})
    print(f"   BOT: {e['respuesta']}")
    return e


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    preguntar("que necesito para validar la identidad de una persona?", "dev-1")
    preguntar("y que pasa si la foto esta borrosa?", "dev-1")
    preguntar("puedo cancelar un documento que ya envie a firmar?", "dev-2")
    preguntar("tienen integracion con SAP?", "dev-3")
