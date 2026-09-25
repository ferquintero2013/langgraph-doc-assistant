# Creación desde app.auco.ai:

> Fuente: https://docs.auco.ai/api/webhooks/introduction

En Auco, para darte control total de la integración con cada uno de los procesos creados, contamos con un sistema webhook en el que podrás recibir notificaciones en cada etapa de cada uno de los flujos creados, de inicio a fin.
Para configurar el webhook existen dos caminos, desde el API y la plataforma web:

## Creación desde app.auco.ai:
Es importante que para realizar esta configuración seas admin o tengas permisos admin, desde la plataforma solo podrás crear un webhook, que será el webhook 'default' .
`'default'`
Ingresa con tu correo y contraseña.
Dirígete al perfil www.auco.ai/profile
ingresa a opciones de desarrollo
En la parte inferior encontrarás las opciones para modificar tu webhook y headers de autenticación si requieres.

## Creación desde Auco API
🆕 Si! Desde el API es posible crear diferentes webhook , cada webhook debe tener un id, tu primer webhook debe tener el id 'default' , que es donde por defecto se van a enviar todas las notificaciones; los siguientes webhooks pueden tener el id que prefieras.
`'default'`
Para definir a qué webhooks se notificarán los estados del proceso, en la creación del documento , debes guardar la lista de ids de los webhooks a los que se debe notificar.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación de webhooks ​
PARAMETROS: Nombre | Tipo | Descripción ;; id | String requerido | Nombre identificador del webhook, el primer webhook debe ser default . ;; description | String opcional | Descripción del propósito del webhook. ;; url | String requerido | URL (URI válida) a la que se enviarán las notificaciones del webhook. ;; header | Object opcional | Objeto { key, value } con el header de autenticación a enviar. ;; header.key | String condicional | Subcampo de header . Requerido si se envía header : clave del header. ;; header.value | String condicional | Subcampo de header . Requerido si se envía header : valor del header.

## ¿Dónde se configuran? ​
Los webhooks se guardan mediante el endpoint Actualizar organización ( PUT /v1.5/ext/company ), en el parámetro webhooks . Allí encontrarás los ejemplos completos de la petición en Curl, Python y Node.js.
`PUT /v1.5/ext/company`
`webhooks`
👉 Ver Actualizar organización .
El parámetro webhooks reemplaza la configuración existente: debes enviar la lista completa e incluir siempre el webhook con id: "default" . Para conservar webhooks ya creados, inclúyelos en la petición.
`webhooks`
`id: "default"`

## Tiempo de respuesta y reintentos ​
Auco espera máximo 10 segundos la respuesta de tu endpoint. Si tu servidor no responde dentro de esa ventana, Auco corta la conexión y la notificación queda registrada como timeout.
Esos 10 segundos cubren la petición completa: resolución DNS, handshake TLS y el tiempo que tarde tu servidor en responder. Un endpoint que en promedio tarda 8 segundos ya está al límite.
Devuelve 200 apenas recibas la notificación y encola el trabajo pesado —guardar en base de datos, descargar el PDF, llamar a otro servicio— en segundo plano.
`200`
Un handler que descarga archivos o consulta a un tercero de forma síncrona antes de responder supera los 10 segundos con facilidad, y la notificación se corta aunque tu código haya terminado bien.

## Reintentos ​
Una notificación cuenta como entregada solo si tu endpoint responde con un código 2xx . Si falla —por timeout, o porque respondes 4xx o 5xx — Auco la reintenta hasta 3 veces , esperando cada vez un poco más:
`2xx`
`4xx`
`5xx`
PARAMETROS: Reintento | Cuándo ;; 1.º | 2 minutos después del intento fallido ;; 2.º | 4 minutos después del anterior ;; 3.º | 6 minutos después del anterior
Después del tercer reintento Auco deja de intentar y esa notificación se descarta: no vuelve a enviarse.
`4xx`
Responder con un código de error no le dice a Auco que descarte el evento: dispara la misma cadena de reintentos que un timeout. Si tu integración decide ignorar un status , respóndele 200 igual y descártalo de tu lado.
`status`
`200`
Un reintento repite la misma notificación. Si tu servidor alcanzó a procesarla pero respondió tarde, vas a recibirla otra vez. Usa el code del proceso junto con el status para reconocer una repetición, en lugar de crear un registro nuevo en cada llegada.
`code`
`status`
Como una notificación descartada no se reenvía, no dependas solo del webhook para saber en qué va un proceso. Puedes consultar su estado cuando lo necesites con Consultar proceso .

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Falta el webhook default ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación de webhooks
¿Dónde se configuran?
Tiempo de respuesta y reintentos Reintentos
Reintentos
⚠️ Respuestas de error