# Asistente sobre documentación técnica — demo con LangGraph

Chatbot que responde preguntas sobre la documentación pública de
[AUCO](https://docs.auco.ai) (firma electrónica y validación de identidad),
y que **muestra cómo llegó a cada respuesta**.

> **Demostración técnica independiente.** No es un producto de AUCO, no está
> afiliado a AUCO y no tiene relación comercial con AUCO. Se construyó sobre
> su documentación pública como ejercicio de ingeniería. Cualquier error en
> las respuestas es del sistema, no de AUCO: para información oficial,
> consulta [docs.auco.ai](https://docs.auco.ai).
>
> El contenido de `docs_auco/` y del índice es documentación de AUCO y les
> pertenece. Se incluye únicamente para que el demo sea reproducible. Si AUCO
> prefiere que no esté publicado, se retira.

Construido por [Ferney Quintero](https://ferney-portfolio.vercel.app).

---

## Qué tiene de distinto

La mayoría de los RAG son lineales: buscar → responder. Si la búsqueda falla,
el modelo responde igual, y responde mal con toda confianza.

Aquí hay un **grafo con decisiones**:

```
        pregunta
           │
      contextualizar        ¿de qué habla, dado lo que ya se dijo?
           │
        buscar ◄──────┐     híbrida: BM25 + embeddings, fusión RRF
           │          │
        evaluar ──────┘     ¿esto responde de verdad? si no: reformular y reintentar
           │
        responder           redacta solo con lo recuperado
           │
        verificar           ¿la respuesta está respaldada?
           │
      ┌────┴────┐
     fin     declinar       si no lo está, se descarta
```

Dos cosas importan:

1. **El ciclo.** Si lo recuperado no sirve, reformula la consulta al vocabulario
   del producto y busca otra vez, hasta dos intentos.
2. **La verificación es una compuerta del grafo, no una instrucción del prompt.**
   Pedirle a un modelo "no inventes" es una sugerencia. Un nodo que revisa la
   respuesta contra las fuentes y la descarta es un control.

La interfaz muestra ese recorrido en cada respuesta.

## Cómo está hecho

| | |
|---|---|
| Orquestación | LangGraph (`StateGraph`, ciclos, `MemorySaver`) |
| Recuperación | BM25 + `text-embedding-3-small`, fusión por RRF (k=60) |
| Generación | `gpt-4o` para redactar · `gpt-4o-mini` para decidir |
| Interfaz | Streamlit |
| Índice | 503 fragmentos de 64 páginas, en numpy — sin base vectorial |

Sin base vectorial a propósito: con 503 fragmentos los vectores caben en un
array normalizado y la búsqueda es una multiplicación de matrices. Una base
vectorial aquí es infraestructura que no paga su costo.

## Correrlo

```bash
python -m venv venv && venv\Scripts\activate     # Windows
pip install -r requirements.txt

copy .env.example .env                           # y pon tu OPENAI_API_KEY
streamlit run app.py
```

Para reconstruir el índice desde cero:

```bash
python descargar_docs.py     # 1 petición/segundo, respeta el sitio
python indexar.py
```

## Los pasos

`paso1` … `paso5` son la construcción incremental, de un grafo de dos nodos al
sistema completo. Se dejaron en el repositorio porque el recorrido explica el
diseño mejor que el resultado final.

| | |
|---|---|
| `paso1_estado.py` | estado y nodos: qué es un `StateGraph` |
| `paso2_ciclo.py` | aristas condicionales y ciclos |
| `paso3_chatbot.py` | el grafo completo con documentos de prueba |
| `paso4_memoria.py` | checkpointer, `thread_id` y reducers |
| `paso5_auco.py` | el mismo grafo, contra la documentación real |
