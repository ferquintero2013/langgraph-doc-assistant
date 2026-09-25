# -*- coding: utf-8 -*-
"""PASO 4 — Memoria: checkpointer, thread_id y reducers.

Tres cosas nuevas, y la tercera es la que da mas problemas en la practica.

  1. CHECKPOINTER   el grafo guarda su estado al terminar. La proxima
                    invocacion arranca desde donde quedo, sin que el
                    cliente reenvie nada.

  2. THREAD_ID      identifica la conversacion. Dos clientes distintos,
                    dos hilos; el grafo no los mezcla.

  3. REDUCER        POR DEFECTO, cada nodo SOBRESCRIBE el campo que
                    devuelve. Si el historial es una lista normal, cada
                    turno borra el anterior. Para que se acumule hay que
                    declararlo con un reducer:

                        historial: Annotated[list, add]

                    Ese `add` le dice a LangGraph "suma, no reemplaces".
                    Olvidarlo es el bug clasico: la memoria parece estar
                    y no esta.

Diferencia con el RAG del portafolio: alli la memoria vive en el
navegador y viaja en cada peticion. Si el cliente cierra la pestana, se
perdio. Aqui vive del lado del servidor y sobrevive.
"""

import json
from operator import add
from typing import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

from config import clave_openai

cliente = OpenAI(api_key=clave_openai())

MODELO_BARATO = "gpt-4o-mini"
MODELO_BUENO = "gpt-4o"
MAX_INTENTOS = 2

DOCS = [
    {"titulo": "Reenvio de notificaciones",
     "texto": ("Si el destinatario no recibe el enlace de firma, puede reenviarse "
               "desde el panel en Documentos > Acciones > Reenviar notificacion. "
               "El reenvio no invalida el enlace anterior.")},
    {"titulo": "Requisitos de calidad de imagen",
     "texto": ("La validacion biometrica exige fotos sin reflejos, con los cuatro "
               "bordes del documento visibles y resolucion minima de 1024 px de "
               "ancho. Las capturas de pantalla no son aceptadas.")},
    {"titulo": "Validez juridica de la firma electronica",
     "texto": ("La firma electronica tiene plena validez juridica en Colombia bajo "
               "la Ley 527 de 1999, siempre que se conserve la trazabilidad del "
               "firmante y la integridad del documento.")},
    {"titulo": "Revocacion de documentos",
     "texto": ("Un documento ya firmado por todas las partes no puede revocarse. "
               "Si aun hay firmas pendientes, el emisor puede cancelarlo desde el "
               "panel, lo que anula los enlaces enviados.")},
]


def llm(modelo, sistema, usuario, json_mode=False, max_tokens=400):
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    r = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "system", "content": sistema},
                  {"role": "user", "content": usuario}],
        temperature=0, max_tokens=max_tokens, **kwargs)
    return r.choices[0].message.content


# ---------------------------------------------------------------- ESTADO
class Estado(TypedDict):
    # CON reducer: se acumula turno a turno. Sin el Annotated, cada
    # invocacion borraria el historial anterior.
    historial: Annotated[list, add]

    # SIN reducer: son de este turno y se sobrescriben en cada uno.
    # Que sea asi es deliberado: el numero de intentos de ayer no debe
    # contar para la pregunta de hoy.
    pregunta: str
    consulta: str
    documentos: list
    intentos: int
    sirve: bool
    respuesta: str
    respaldada: bool


# ----------------------------------------------------------------- NODOS
def contextualizar(estado: Estado) -> dict:
    """Resuelve la pregunta contra el historial, ANTES de buscar.

    Es el mismo rewrite_query del RAG, y por la misma razon: "y eso como
    lo hago?" no se parece a ningun documento. Hay que convertirlo en una
    pregunta autonoma antes de la busqueda, no despues.
    """
    historial = estado.get("historial", [])
    if not historial:
        print(f"   [contexto]    primer turno, sin cambios")
        return {"consulta": estado["pregunta"], "intentos": 0}

    conversacion = "\n".join(f"{t['quien']}: {t['texto']}" for t in historial[-4:])
    nueva = llm(
        MODELO_BARATO,
        # Misma leccion que en el RAG del portafolio: no basta con pedir
        # "resuelve las referencias". Hay que exigir que la pregunta
        # reescrita NOMBRE el tema, porque esa frase va a un buscador.
        # La primera version devolvia "¿Que resolucion necesito?" — que
        # esta bien escrito y no encuentra nada.
        ("Reescribe la ultima pregunta del cliente como una pregunta autonoma "
         "usando la conversacion previa.\n"
         "La pregunta reescrita DEBE NOMBRAR el tema de forma explicita. Si el "
         "cliente venia hablando de la foto de la cedula y pregunta '¿y que "
         "resolucion necesito?', la reescritura es '¿Que resolucion necesita la "
         "foto de la cedula para la validacion?' — no '¿Que resolucion "
         "necesito?'. Esa frase se usa para buscar en documentos, y sin el tema "
         "no encuentra nada.\n"
         "Si ya es autonoma, devuelvela igual. Devuelve SOLO la pregunta."),
        f"CONVERSACION:\n{conversacion}\n\nULTIMA PREGUNTA: {estado['pregunta']}",
        max_tokens=60).strip()
    print(f"   [contexto]    {estado['pregunta']!r} -> {nueva[:48]!r}")
    return {"consulta": nueva, "intentos": 0}


def buscar(estado: Estado) -> dict:
    palabras = {p for p in estado["consulta"].lower().split() if len(p) > 3}
    encontrados = [d for d in DOCS
                   if sum(1 for p in palabras
                          if p in (d["titulo"] + " " + d["texto"]).lower()) >= 2]
    print(f"   [buscar]      {len(encontrados)} doc(s)")
    return {"documentos": encontrados, "intentos": estado.get("intentos", 0) + 1}


def evaluar(estado: Estado) -> dict:
    if not estado["documentos"]:
        print("   [evaluar]     sin documentos")
        return {"sirve": False}
    contexto = "\n".join(f"- {d['titulo']}: {d['texto']}" for d in estado["documentos"])
    v = json.loads(llm(
        MODELO_BARATO,
        ("Decides si unos fragmentos permiten dar al cliente una respuesta UTIL. "
         'Responde SOLO JSON: {"sirve": true|false, "razon": "una frase"}. '
         "sirve=true si el cliente sale sabiendo que hacer, aunque el vocabulario "
         "no coincida. Un fragmento que dice que algo NO se puede hacer SI responde."),
        f"PREGUNTA:\n{estado['consulta']}\n\nFRAGMENTOS:\n{contexto}",
        json_mode=True, max_tokens=120))
    print(f"   [evaluar]     sirve={v['sirve']}")
    return {"sirve": bool(v["sirve"])}


def reformular(estado: Estado) -> dict:
    titulos = ", ".join(d["titulo"] for d in DOCS)
    nueva = llm(MODELO_BARATO,
                ("Reescribe la consulta con el vocabulario tecnico de la "
                 f"documentacion. Secciones: {titulos}. Devuelve SOLO la consulta."),
                f"Consulta que no funciono: {estado['consulta']}",
                max_tokens=60).strip()
    print(f"   [reformular]  -> {nueva[:48]!r}")
    return {"consulta": nueva}


def responder(estado: Estado) -> dict:
    if not estado["documentos"]:
        texto = "No encuentro eso en la documentacion. Puedo pasarte con soporte."
        print("   [responder]   declina")
    else:
        contexto = "\n".join(f"[{d['titulo']}]\n{d['texto']}" for d in estado["documentos"])
        texto = llm(MODELO_BUENO,
                    ("Eres el asistente de soporte de un producto de firma electronica. "
                     "Responde en 2-3 frases usando UNICAMENTE la documentacion dada. "
                     "Cierra citando la seccion entre corchetes."),
                    f"PREGUNTA:\n{estado['consulta']}\n\nDOCUMENTACION:\n{contexto}")
        print(f"   [responder]   redactada")

    # Aqui esta la clave de la memoria: se devuelven los DOS turnos y el
    # reducer los suma a lo que ya habia. Sin Annotated[list, add] esto
    # reemplazaria el historial entero.
    return {"respuesta": texto,
            "historial": [{"quien": "cliente", "texto": estado["pregunta"]},
                          {"quien": "bot", "texto": texto}]}


def verificar(estado: Estado) -> dict:
    if not estado["documentos"]:
        return {"respaldada": True}
    contexto = "\n".join(d["texto"] for d in estado["documentos"])
    v = json.loads(llm(
        MODELO_BARATO,
        ('Revisas si una respuesta esta respaldada por la documentacion. '
         'SOLO JSON: {"respaldada": true|false, "razon": "una frase"}.'),
        f"DOCUMENTACION:\n{contexto}\n\nRESPUESTA:\n{estado['respuesta']}",
        json_mode=True, max_tokens=120))
    print(f"   [verificar]   {'OK' if v['respaldada'] else 'NO RESPALDADA'}")
    return {"respaldada": bool(v["respaldada"])}


def declinar(estado: Estado) -> dict:
    texto = "Prefiero no responder eso: no encuentro respaldo en la documentacion."
    print("   [declinar]    descartada")
    return {"respuesta": texto,
            "historial": [{"quien": "cliente", "texto": estado["pregunta"]},
                          {"quien": "bot", "texto": texto}]}


def tras_evaluar(estado: Estado) -> str:
    if estado["sirve"]:
        return "responder"
    if estado["intentos"] >= MAX_INTENTOS:
        return "responder"
    return "reformular"


def tras_verificar(estado: Estado) -> str:
    return "fin" if estado["respaldada"] else "declinar"


# ----------------------------------------------------------------- GRAFO
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

# AQUI ENTRA LA MEMORIA. MemorySaver guarda en RAM: sirve para aprender y
# se pierde al cerrar el proceso. En produccion se cambia por el
# checkpointer de Postgres o Redis — y solo cambia esta linea.
grafo = constructor.compile(checkpointer=MemorySaver())


def conversar(texto, hilo):
    """Una invocacion. El thread_id es lo que hace que haya memoria."""
    print(f"\nCLIENTE [{hilo}]: {texto}")
    estado = grafo.invoke({"pregunta": texto},
                          config={"configurable": {"thread_id": hilo}})
    print(f"   BOT: {estado['respuesta'][:150]}")
    return estado


if __name__ == "__main__":
    print("=" * 74)
    print("CONVERSACION CON SEGUIMIENTO — hilo 'cliente-A'")
    print("=" * 74)
    conversar("la foto de mi cedula no pasa la validacion", "cliente-A")
    # Sin memoria, esta pregunta no se parece a ningun documento:
    conversar("y que resolucion necesito exactamente?", "cliente-A")

    print("\n" + "=" * 74)
    print("OTRO CLIENTE — hilo 'cliente-B', no debe heredar nada de A")
    print("=" * 74)
    conversar("y que resolucion necesito exactamente?", "cliente-B")

    print("\n" + "=" * 74)
    print("EL ESTADO GUARDADO")
    print("=" * 74)
    for hilo in ("cliente-A", "cliente-B"):
        guardado = grafo.get_state({"configurable": {"thread_id": hilo}})
        turnos = guardado.values.get("historial", [])
        print(f"   {hilo}: {len(turnos)} turnos en memoria")
        for t in turnos:
            print(f"      {t['quien']:8} {t['texto'][:58]}")
