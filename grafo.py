# -*- coding: utf-8 -*-
"""El grafo, separado de la interfaz.

Es el mismo del paso 5, con un cambio: cada nodo deja constancia de lo
que hizo en `traza`. Esa traza es lo que la interfaz muestra al visitante,
y es el punto del demo — no que responda, sino que se vea COMO decide:
cuando reformula, cuando se rinde, cuando descarta su propia respuesta.

DEMOSTRACION TECNICA construida con documentacion publica de AUCO
(docs.auco.ai). No es un producto ni esta afiliado a AUCO.
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
    traza: list          # se reinicia en cada turno: es de esta pregunta


def contextualizar(estado: Estado) -> dict:
    historial = estado.get("historial", [])
    if not historial:
        return {"consulta": estado["pregunta"], "intentos": 0, "traza": []}

    conversacion = "\n".join(f"{t['quien']}: {t['texto'][:200]}" for t in historial[-4:])
    nueva = llm(MODELO_BARATO,
                ("Reescribe la ultima pregunta como una pregunta autonoma usando la "
                 "conversacion previa. DEBE NOMBRAR el tema explicitamente: esa frase "
                 "se usa para buscar en documentacion tecnica, y sin el tema no "
                 "encuentra nada. Si ya es autonoma, devuelvela igual. Solo la pregunta."),
                f"CONVERSACION:\n{conversacion}\n\nULTIMA: {estado['pregunta']}",
                max_tokens=80).strip()
    cambio = nueva.lower() != estado["pregunta"].lower()
    traza = [{"paso": "Contexto",
              "detalle": f"Resuelta contra la conversacion: “{nueva}”" if cambio
                         else "Pregunta ya autonoma, sin cambios"}]
    return {"consulta": nueva, "intentos": 0, "traza": traza}


# Cuantos fragmentos se le pasan al redactor. Con 4 se perdian respuestas
# por un puesto: la tabla de parametros de /veriface/validate quedaba
# quinta y el bot contestaba que no la encontraba. Se midio, no se adivino.
N_FRAGMENTOS = 6


def buscar(estado: Estado) -> dict:
    docs = buscar_docs(estado["consulta"], n=N_FRAGMENTOS)
    intento = estado.get("intentos", 0) + 1
    return {"documentos": docs, "intentos": intento,
            "traza": estado["traza"] + [{
                "paso": f"Busqueda {intento}",
                "detalle": f"{len(docs)} fragmentos · " +
                           ", ".join(d["seccion"][:26] for d in docs[:3])}]}


def evaluar(estado: Estado) -> dict:
    if not estado["documentos"]:
        return {"sirve": False,
                "traza": estado["traza"] + [{"paso": "Evaluacion", "detalle": "Sin resultados"}]}

    contexto = "\n\n".join(f"[{d['seccion']}]\n{d['texto'][:600]}" for d in estado["documentos"])
    v = json.loads(llm(
        MODELO_BARATO,
        ("Decides si unos fragmentos de documentacion tecnica permiten responder "
         'UTILMENTE. Responde SOLO JSON: {"sirve": true|false, "razon": "una frase"}. '
         "sirve=true si quien pregunta sale sabiendo que hacer, aunque el vocabulario "
         "no coincida. Un fragmento que dice que algo NO se puede hacer SI responde."),
        f"PREGUNTA:\n{estado['consulta']}\n\nFRAGMENTOS:\n{contexto}",
        json_mode=True, max_tokens=120))
    return {"sirve": bool(v["sirve"]),
            "traza": estado["traza"] + [{
                "paso": "Evaluacion",
                "detalle": ("Responden la pregunta" if v["sirve"]
                            else f"No responden — {v.get('razon','')[:70]}")}]}


def reformular(estado: Estado) -> dict:
    nueva = llm(MODELO_BARATO,
                ("Reescribe la consulta con el vocabulario tecnico del producto, para "
                 f"buscar en su documentacion.\nProducto: {DOMINIO}\n"
                 "Usa terminos de API (endpoint, parametros, webhook) SOLO si la "
                 "pregunta es tecnica. Si preguntan por precios, personas, la "
                 "empresa o algo que no es de integracion, reformula en lenguaje "
                 "normal: forzar vocabulario de API ahi produce respuestas absurdas "
                 "del tipo 'no existe un endpoint para consultar quien es el CEO'. "
                 "Devuelve SOLO la consulta."),
                f"No funciono esta busqueda: {estado['consulta']}",
                max_tokens=60).strip()
    return {"consulta": nueva,
            "traza": estado["traza"] + [{
                "paso": "Reformulacion",
                "detalle": f"Al vocabulario del producto: “{nueva}”"}]}


def responder(estado: Estado) -> dict:
    if not estado["documentos"]:
        texto = ("No encuentro eso en la documentacion publica de AUCO. "
                 "Puede que este en el soporte directo del equipo.")
        traza = estado["traza"] + [{"paso": "Respuesta", "detalle": "Declina: sin cobertura"}]
    else:
        contexto = "\n\n".join(f"[{d['seccion']}] ({d['url']})\n{d['texto'][:1200]}"
                               for d in estado["documentos"])
        texto = llm(MODELO_BUENO,
                    ("Eres un asistente sobre la documentacion de AUCO (firma "
                     "electronica y validacion de identidad). Responde en 2-4 frases, "
                     "claro y tecnico, usando UNICAMENTE la documentacion entregada. "
                     "Si hay parametros o endpoints concretos, nombralos. NO incluyas "
                     "la URL en el texto: la interfaz muestra las fuentes aparte.\n\n"
                     "REGLA CRITICA — no confundas 'no lo encontre' con 'no existe'.\n"
                     "Solo recibes los fragmentos que trajo el buscador, no la "
                     "documentacion completa. Si te preguntan por los parametros de un "
                     "endpoint y los fragmentos no los traen, la respuesta es 'no "
                     "aparecen en lo que encontre', NUNCA 'ese endpoint no requiere "
                     "parametros'. Lo segundo es una afirmacion sobre la API que no "
                     "puedes hacer, y para alguien que esta integrando es peor que no "
                     "responder.\n"
                     "Lo mismo con 'no soporta', 'no existe', 'no es posible': solo si "
                     "la documentacion lo dice explicitamente."),
                    f"PREGUNTA:\n{estado['consulta']}\n\nDOCUMENTACION:\n{contexto}")
        traza = estado["traza"] + [{"paso": "Respuesta", "detalle": "Redactada con GPT-4o"}]
    return {"respuesta": texto, "traza": traza,
            "historial": [{"quien": "usuario", "texto": estado["pregunta"]},
                          {"quien": "bot", "texto": texto}]}


def verificar(estado: Estado) -> dict:
    if not estado["documentos"]:
        return {"respaldada": True}
    # El mismo recorte que vio el redactor: si el verificador lee menos,
    # marca como inventado lo que estaba en la parte que no le pasaron.
    contexto = "\n".join(d["texto"][:1200] for d in estado["documentos"])
    v = json.loads(llm(
        MODELO_BARATO,
        ('Revisas si una respuesta esta respaldada por la documentacion. SOLO JSON: '
         '{"respaldada": true|false, "razon": "una frase"}. false si afirma algo que '
         "no esta, aunque suene razonable. Endpoints o parametros inventados son "
         "motivo suficiente.\n"
         "TAMBIEN es false toda afirmacion NEGATIVA sobre el producto que la "
         "documentacion no diga explicitamente: 'no requiere parametros', 'no existe "
         "ese endpoint', 'no soporta X'. Que los fragmentos no mencionen algo no "
         "prueba que no exista — son un extracto, no la documentacion completa. "
         "Negar algo por omision es tan inventado como afirmarlo.\n"
         "EXCEPCION: si la respuesta solo dice que NO ENCONTRO la informacion "
         "('no aparece en lo que encontre', 'no tengo ese dato'), eso es "
         "respaldada=true. Es una afirmacion sobre la busqueda, no sobre el "
         "producto, y siempre es cierta. Rechazarla convierte una respuesta "
         "honesta en un rechazo generico, que es peor."),
        f"DOCUMENTACION:\n{contexto}\n\nRESPUESTA:\n{estado['respuesta']}",
        json_mode=True, max_tokens=120))
    return {"respaldada": bool(v["respaldada"]),
            "traza": estado["traza"] + [{
                "paso": "Verificacion",
                "detalle": ("Respaldada por las fuentes" if v["respaldada"]
                            else f"DESCARTADA — {v.get('razon','')[:70]}")}]}


def declinar(estado: Estado) -> dict:
    texto = ("Prefiero no responder eso: la respuesta que redacte no quedaba "
             "respaldada por la documentacion publica, y prefiero decirlo a "
             "arriesgarme a darte un dato inventado.")
    return {"respuesta": texto,
            "historial": [{"quien": "usuario", "texto": estado["pregunta"]},
                          {"quien": "bot", "texto": texto}]}


def tras_evaluar(estado):
    if estado["sirve"]:
        return "responder"
    return "responder" if estado["intentos"] >= MAX_INTENTOS else "reformular"


def tras_verificar(estado):
    return "fin" if estado["respaldada"] else "declinar"


def construir():
    c = StateGraph(Estado)
    for n, f in [("contextualizar", contextualizar), ("buscar", buscar),
                 ("evaluar", evaluar), ("reformular", reformular),
                 ("responder", responder), ("verificar", verificar),
                 ("declinar", declinar)]:
        c.add_node(n, f)
    c.add_edge(START, "contextualizar")
    c.add_edge("contextualizar", "buscar")
    c.add_edge("buscar", "evaluar")
    c.add_conditional_edges("evaluar", tras_evaluar,
                            {"reformular": "reformular", "responder": "responder"})
    c.add_edge("reformular", "buscar")
    c.add_edge("responder", "verificar")
    c.add_conditional_edges("verificar", tras_verificar,
                            {"fin": END, "declinar": "declinar"})
    c.add_edge("declinar", END)
    return c.compile(checkpointer=MemorySaver())
