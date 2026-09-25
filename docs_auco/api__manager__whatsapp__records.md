# api/manager/whatsapp/records

> Fuente: https://docs.auco.ai/api/manager/whatsapp/records

`/whatsapp/records`
`puk _`
Este servicio devuelve el historial completo de la conversación de WhatsApp de un proceso de Auco: los mensajes que el bot de Auco envió al participante, las respuestas del participante y los estados de entrega reportados por WhatsApp.
La respuesta es un arreglo plano en orden cronológico ascendente , sin paginación ni filtros. Si el proceso no tuvo actividad en WhatsApp, el arreglo llega vacío ( [] ).
Esta página documenta la consulta del historial de mensajes , no la configuración de WhatsApp como canal de firma o notificación. Para activar el flujo de firma por WhatsApp ( options.whatsapp , options.both ) consulta Validaciones de Identidad .
`options.whatsapp`
`options.both`

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String requerido | Código del proceso. Mínimo 9 caracteres. Su longitud determina el tipo de proceso que se consulta. ;; userId | String condicional | Identificador del participante dentro del proceso. Obligatorio en procesos de firma y no admitido en AucoFace.
No existe forma de traer un proceso multifirmante completo en una sola llamada: debes consultar participante a participante y unir los resultados en tu integración.

## 🧩 Tipos de proceso soportados ​
La longitud de code determina el tipo de proceso que Auco consulta y si userId es obligatorio.
`code`
`userId`
PARAMETROS: Longitud | Tipo de proceso | userId | De dónde obtienes los identificadores ;; 9 | Contrato | requerido | code y signProfile[].id de GET /document ;; 10 | Documento | requerido | code y signProfile[].id de GET /document ;; 16 | Validación de identidad (AucoFace) | no admitido | code de GET /veriface ;; 24 | Paquete de documentos | requerido | el id del paquete y signers[].userId
Los procesos de AucoFace tienen un solo participante, por eso no llevan userId .
`userId`

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## 🔹 Proceso de firma ( code y userId ) ​
`code`
`userId`
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/whatsapp/records?code=CODEDOCUM&userId=01' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/whatsapp/records" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "code" : "CODEDOCUM" , "userId" : "01" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/whatsapp/records' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { code : 'CODEDOCUM' , userId : '01' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 🔸 Proceso de AucoFace (solo code ) ​
`code`
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/whatsapp/records?code=VERIFACECODE1234' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/whatsapp/records" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "code" : "VERIFACECODE1234" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/whatsapp/records' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { code : 'VERIFACECODE1234' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​

## 🔹 Conversación con mensajes salientes y entrantes ​
[ { "entity" : "auco" , "phone" : "+573001234567" , "message" : "👋🏼 Hola Juan, has sido invitado a firmar un documento creado por ACME..." , "date" : 1746028800000 , "actions" : [ { "action" : "sent" , "timestamp" : 1746028800000 } , { "action" : "delivered" , "timestamp" : 1746028805000 } , { "action" : "read" , "timestamp" : 1746028860000 } ] } , { "entity" : "signer" , "phone" : "+573001234567" , "message" : "comenzar" , "date" : 1746028900000 } , { "entity" : "auco" , "phone" : "+573001234567" , "message" : "Este es el documento, recuerda que debes leerlo en su *totalidad*." , "date" : 1746028950000 , "actions" : [ { "action" : "sent" , "timestamp" : 1746028950000 } , { "action" : "delivered" , "timestamp" : 1746028952000 } ] } , { "entity" : "signer" , "phone" : "+573001234567" , "message" : "Completo el formulario" , "date" : 1746029050000 } ]
Los mensajes entrantes de este ejemplo muestran los dos casos que puedes encontrar. El segundo registro, comenzar , es el texto de un botón que pulsó el participante. El último, Completo el formulario , no es algo que el participante escribiera: es la referencia con la que se registró una acción suya dentro del flujo. Ese texto es descriptivo y varía según el proceso, así que no lo uses para detectar acciones en tu integración.
`comenzar`
`Completo el formulario`

## 🔸 Mensaje que no se pudo entregar ​
`[ { "entity" : "auco" , "phone" : "+573001234567" , "message" : "👋🏼 Hola Juan, has sido invitado a firmar un documento creado por ACME..." , "date" : 1746028800000 , "actions" : [ { "action" : "sent" , "timestamp" : 1746028800000 } , { "action" : "failed" , "timestamp" : 1746028802000 , "errors" : [ "WHATSAPP_NUMBER_NOT_REGISTERED" ] } ] } ]`

## 🔸 Proceso sin actividad en WhatsApp ​
`[ ]`

## 📋 Campos de la respuesta ​
PARAMETROS: Campo | Tipo | Descripción ;; entity | String | Siempre presente. auco = mensaje saliente enviado por el bot de Auco. signer = mensaje entrante enviado por el participante. ;; phone | String | Siempre presente. Teléfono del participante en formato internacional, con indicativo de país y el signo + . ;; message | String | Siempre presente. Texto plano ya renderizado : las plantillas de WhatsApp llegan con sus variables sustituidas. ;; date | Number | Siempre presente. Timestamp epoch en milisegundos . ;; actions | Array<Object> | Opcional. Solo en mensajes con estados de entrega reportados por WhatsApp. Los mensajes del participante ( entity: "signer" ) no lo incluyen. ;; actions[].action | String | Estado de entrega: sent , delivered , read o failed . ;; actions[].timestamp | Number | Timestamp epoch en milisegundos del momento en que WhatsApp reportó el estado. ;; actions[].errors | Array<String> | Opcional. Solo cuando action es failed . Contiene los motivos del fallo.
Tanto date como actions[].timestamp están en milisegundos, no en segundos. Por ejemplo, 1746028800000 corresponde a 2025-04-30T16:00:00.000Z . Si el lenguaje de tu integración espera segundos, divide el valor entre 1000.
`date`
`actions[].timestamp`
`1746028800000`
`2025-04-30T16:00:00.000Z`
`message`
La respuesta no incluye URLs ni archivos de medios . Cuando el participante envía un adjunto o realiza una acción dentro del flujo, el registro guarda una referencia en texto de esa acción (por ejemplo, algo como Completo el formulario ) en lugar del contenido.
`Completo el formulario`
Ese texto es descriptivo, no un identificador: depende del flujo del proceso, puede estar personalizado y puede cambiar. Si tu integración necesita reaccionar a acciones concretas, no la construyas comparando el contenido de message .
`message`
Para descargar los archivos que el participante cargó usa Consultar Proceso y Anexos .

## 🔄 Estados de entrega ( actions[].action ) ​
`actions[].action`
PARAMETROS: Estado | Descripción ;; sent | Auco entregó el mensaje a WhatsApp y este lo aceptó para su envío. ;; delivered | WhatsApp confirmó que el mensaje llegó al dispositivo del participante. ;; read | El participante abrió el mensaje. ;; failed | WhatsApp no pudo entregar el mensaje; el motivo viene en actions[].errors .
Los estados son acumulativos y llegan en el orden en que WhatsApp los reporta. Un mensaje puede quedarse en sent si el participante tiene desactivadas las confirmaciones de lectura.
`sent`

## 🚫 Motivos de fallo ( actions[].errors ) ​
`actions[].errors`
Estos códigos no son códigos HTTP : la consulta puede devolver 200 y contener mensajes con estado failed .
`200`
`failed`
PARAMETROS: Código | Descripción ;; WHATSAPP_RATE_LIMIT | Se excedió el límite de mensajes que WhatsApp permite en la ventana de tiempo actual. ;; WHATSAPP_NUMBER_NOT_REGISTERED | El número del participante no está registrado en WhatsApp. ;; WHATSAPP_NO_ACTIVE_CONVERSATION | No hay conversación activa; WhatsApp no admite mensajes fuera de plantilla. ;; WHATSAPP_UNSUPPORTED_MESSAGE_TYPE | WhatsApp rechazó el tipo de mensaje. ;; WHATSAPP_TEMPLATE_NOT_FOUND | La plantilla usada no existe. ;; WHATSAPP_TEMPLATE_PAUSED | La plantilla está pausada por WhatsApp. ;; WHATSAPP_TEMPLATE_DISABLED | La plantilla fue deshabilitada por WhatsApp. ;; WHATSAPP_SERVICE_UNAVAILABLE | El servicio de WhatsApp no estaba disponible. ;; WHATSAPP_NUMBER_NOT_ACTIVE | El número emisor de Auco no estaba activo. ;; WHATSAPP_SEND_ERROR | Error de envío no clasificado.

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Error de validación o proceso no encontrado: CODE_REQUIRED (falta code ), CODE_NOT_VALID ( code de menos de 9 caracteres), USER_ID_REQUIRED (falta userId en un proceso de firma), USER_ID_NOT_ALLOWED (se envió userId en un proceso de AucoFace) y PROCESS_NOT_FOUND ;; 401 | Autenticación inválida o ausente
PROCESS_NOT_FOUND se devuelve cuando el proceso no existe, no pertenece a tu organización, el participante no está en el proceso, o el proceso de AucoFace no usó WhatsApp como canal.
`PROCESS_NOT_FOUND`
Un proceso de AucoFace realizado por web, sin canal WhatsApp, devuelve PROCESS_NOT_FOUND en lugar de un arreglo vacío.
`PROCESS_NOT_FOUND`
Autenticación
Parámetros de consulta
🧩 Tipos de proceso soportados
🧪 Ejemplos de uso 🔹 Proceso de firma ( code y userId ) 🔸 Proceso de AucoFace (solo code )
🔹 Proceso de firma ( code y userId )
`code`
`userId`
🔸 Proceso de AucoFace (solo code )
`code`
📥 Ejemplos de respuesta 🔹 Conversación con mensajes salientes y entrantes 🔸 Mensaje que no se pudo entregar 🔸 Proceso sin actividad en WhatsApp
🔹 Conversación con mensajes salientes y entrantes
🔸 Mensaje que no se pudo entregar
🔸 Proceso sin actividad en WhatsApp
📋 Campos de la respuesta
🔄 Estados de entrega ( actions[].action )
`actions[].action`
🚫 Motivos de fallo ( actions[].errors )
`actions[].errors`
⚠️ Respuestas de error