# api/manager/documents/roadmap

> Fuente: https://docs.auco.ai/api/manager/documents/roadmap

`/document/roadmap`
`puk _`
Este servicio devuelve la trazabilidad completa de un proceso de firma : quién lo creó, quiénes participan en él y qué ocurrió en cada momento. Es el servicio que usas para auditar un proceso, para reconstruir su historia ante una reclamación o para alimentar un tablero de seguimiento.
La respuesta trae los datos del proceso, la lista de participantes y un registro de actividad ordenado cronológicamente de forma ascendente, del evento más antiguo al más reciente. No tiene paginación ni filtros: se devuelve el proceso completo en una sola llamada.
Esta página documenta la trazabilidad del proceso : los eventos de notificación, recordatorio, lectura, firma, aprobación, rechazo, cancelación y reactivación. Para consultar el estado actual del proceso y de cada participante usa GET /document , y para leer los mensajes concretos de una conversación de WhatsApp usa GET /whatsapp/records .
`GET /document`
`GET /whatsapp/records`

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String requerido | Código del proceso del que quieres la trazabilidad. De 9 o 10 caracteres.
code acepta el código de un contrato (9 caracteres) o de un documento (10 caracteres); es el mismo valor que devuelve GET /document en el campo code .
`code`
`GET /document`
`code`
La consulta está limitada a la organización dueña de la llave pública. Un código que no existe y un código que pertenece a otra organización devuelven el mismo error, DOCUMENT_NOT_FOUND .
`DOCUMENT_NOT_FOUND`

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## 🔹 Obtener la trazabilidad de un proceso ​
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/document/roadmap?code=CODEDOCUM' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/document/roadmap" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "code" : "CODEDOCUM" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/document/roadmap' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { code : 'CODEDOCUM' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​

## 🔹 Proceso firmado por WhatsApp ​
{ "name" : "Contrato de servicios" , "documentCode" : "CODEDOCUM" , "createdAt" : "2026-06-26T21:48:42.755Z" , "author" : { "name" : "Ana Gómez" , "email" : "example@auco.ai" } , "participants" : [ { "id" : "01" , "name" : "Juan Pérez" , "role" : "SIGNER" , "phone" : "+573001234567" } ] , "activityLog" : [ { "action" : "NOTIFICATION_SIGN" , "platform" : "WHATSAPP" , "participant" : "01" , "timestamp" : "2026-06-26T21:48:44.307Z" , "by" : "+573001234567" } , { "action" : "PARTICIPANT_READ" , "platform" : "WHATSAPP" , "participant" : "01" , "timestamp" : "2026-06-26T21:49:47.523Z" , "by" : "+573001234567" } , { "action" : "PARTICIPANT_SIGN" , "platform" : "WHATSAPP" , "participant" : "01" , "timestamp" : "2026-06-26T21:50:10.940Z" , "by" : "+573001234567" } ] }

## 🔸 Proceso con varios participantes, un rechazo y una cancelación ​
{ "name" : "Contrato de servicios" , "documentCode" : "CODEDOCUM" , "createdAt" : "2026-02-10T14:02:11.418Z" , "author" : { "name" : "Ana Gómez" , "email" : "example@auco.ai" } , "participants" : [ { "id" : "01" , "name" : "Juan Pérez" , "role" : "SIGNER" , "email" : "juan.perez@example.com" , "phone" : "+573001234567" , "location" : { "lat" : 4.6533326179999995 , "lng" : -74.05834928765297 , "street" : "Calle 98 15-17, 110221 Bogotá, Colombia" } , "ipAddress" : "190.24.10.55 Bogotá, Bogota D.C., Colombia" } , { "id" : "02" , "name" : "María Rueda" , "role" : "APPROVER" , "email" : "maria.rueda@example.com" } , { "name" : "Auditoría Interna" , "role" : "READER" , "email" : "auditoria@example.com" } ] , "activityLog" : [ { "action" : "NOTIFICATION_SIGN" , "platform" : "EMAIL" , "participant" : "01" , "timestamp" : "2026-02-10T14:02:13.902Z" , "by" : "juan.perez@example.com" } , { "action" : "PARTICIPANT_READ" , "platform" : "EMAIL" , "participant" : "01" , "timestamp" : "2026-02-10T15:31:08.114Z" , "by" : "juan.perez@example.com" , "ip" : "190.24.10.55" } , { "action" : "PARTICIPANT_SIGN" , "platform" : "EMAIL" , "participant" : "01" , "timestamp" : "2026-02-10T15:33:44.660Z" , "by" : "juan.perez@example.com" , "ip" : "190.24.10.55" } , { "action" : "NOTIFICATION_APPROVER" , "platform" : "EMAIL" , "participant" : "02" , "timestamp" : "2026-02-10T15:33:47.201Z" , "by" : "maria.rueda@example.com" } , { "action" : "REMINDER_APPROVE" , "platform" : "EMAIL" , "participant" : "02" , "timestamp" : "2026-02-11T15:33:47.318Z" , "by" : "maria.rueda@example.com" } , { "action" : "PARTICIPANT_REJECT" , "platform" : "EMAIL" , "participant" : "02" , "timestamp" : "2026-02-11T16:10:29.775Z" , "by" : "maria.rueda@example.com" , "message" : "El anexo 2 no corresponde al servicio contratado." } , { "action" : "CANCEL_SIGN" , "platform" : "ARCHIVE" , "participant" : "ARCHIVE" , "timestamp" : "2026-02-11T16:44:02.031Z" , "by" : "example@auco.ai" } ] }

## 🔸 Proceso creado sin notificar ​
Un proceso creado con notification: false existe y tiene participantes, pero todavía no ha generado eventos: activityLog llega vacío.
`notification: false`
`activityLog`
`{ "name" : "Contrato de servicios" , "documentCode" : "CODEDOCUM" , "createdAt" : "2026-02-10T14:02:11.418Z" , "author" : { "name" : "Ana Gómez" , "email" : "example@auco.ai" } , "participants" : [ { "id" : "01" , "name" : "Juan Pérez" , "role" : "SIGNER" , "email" : "juan.perez@example.com" } ] , "activityLog" : [ ] }`

## 📋 Campos de la respuesta ​
PARAMETROS: Campo | Tipo | Descripción ;; name | String | Nombre del proceso, tal como se definió al crearlo. ;; documentCode | String | Código del proceso consultado. Coincide con el code que enviaste. ;; createdAt | String | Fecha y hora de creación del proceso, en formato ISO 8601 y zona UTC. ;; author | Object | Opcional. Usuario de tu organización que creó el proceso. No aparece si el creador ya no existe como usuario. ;; author.name | String | Nombre del creador del proceso. ;; author.email | String | Opcional. Correo electrónico del creador del proceso. ;; participants | Array<Object> | Personas involucradas en el proceso: firmantes, aprobadores y observadores. Llega vacío ( [] ) si el proceso no tiene participantes. ;; participants[].id | String | Opcional. Identificador del participante dentro del proceso. Es el valor al que apunta activityLog[].participant . Los observadores no lo traen, y tampoco los participantes que todavía no tienen actividad registrada. ;; participants[].name | String | Opcional. Nombre del participante. ;; participants[].role | String | Rol del participante en el proceso. Ver Roles . ;; participants[].email | String | Opcional. Correo electrónico del participante. ;; participants[].phone | String | Opcional. Teléfono del participante en formato internacional, con indicativo de país y el signo + . ;; participants[].location | Object | Opcional. Ubicación registrada del participante durante el proceso. Solo aparece si Auco la capturó. ;; participants[].location.lat | Number | Latitud, en grados decimales. ;; participants[].location.lng | Number | Longitud, en grados decimales. ;; participants[].location.street | String | Dirección aproximada derivada de las coordenadas. ;; participants[].ipAddress | String | Opcional. Texto libre con la dirección IP registrada del participante. Puede llegar en varios formatos : solo la IP, o la IP acompañada de la ubicación aproximada derivada de ella. No lo interpretes como una IP limpia. ;; activityLog | Array<Object> | Eventos del proceso, ordenados cronológicamente de forma ascendente : el primer elemento es el más antiguo. Llega vacío ( [] ) si el proceso no tiene actividad. ;; activityLog[].action | String | Evento ocurrido. Ver Acciones . ;; activityLog[].platform | String | Canal por el que ocurrió el evento. Ver Plataformas . ;; activityLog[].participant | String | id del participante al que corresponde el evento, o el valor especial ARCHIVE cuando el evento es del proceso y no de una persona. ;; activityLog[].timestamp | String | Fecha y hora del evento, en formato ISO 8601 y zona UTC. ;; activityLog[].by | String | Opcional. Identificador con el que se ejecutó o recibió la acción: el correo electrónico cuando platform es EMAIL y el teléfono cuando es WHATSAPP . ;; activityLog[].ip | String | Opcional. Dirección IP desde la que se registró el evento. Solo aparece cuando Auco la recibió. ;; activityLog[].message | String | Opcional. Texto asociado al evento, por ejemplo el motivo que el participante escribió al rechazar.
author , id , name , email , phone , location , ipAddress , by , ip y message se omiten de la respuesta cuando no hay valor: no llegan en null ni como cadena vacía . Tu integración debe comprobar la existencia de la clave antes de leerla, en lugar de asumir que el objeto siempre trae la misma forma.
`author`
`name`
`email`
`phone`
`location`
`ipAddress`
`message`
`null`
`participant`
activityLog[].participant normalmente es el id de un elemento de participants[] , pero los eventos que afectan al proceso completo llegan con participant: "ARCHIVE" . Ese valor no cruza con participants[].id : si intentas resolverlo contra la lista de participantes no encontrarás coincidencia. Ver Eventos del proceso .
`activityLog[].participant`
`participants[]`
`participant: "ARCHIVE"`
`participants[].id`

## 📖 Diccionario de trazabilidad ​
Las tres columnas que interpretas de cada evento son action (qué pasó), platform (por dónde) y participant (a quién). Estas tablas recogen los valores que Auco emite hoy.
`action`
`platform`
`participant`
Pueden aparecer valores de action , platform y role que no estén en estas tablas: el catálogo crece con el producto. No construyas tu integración asumiendo que la lista es cerrada. Trata un valor desconocido como un evento que aún no sabes clasificar —muéstralo tal cual, regístralo— en lugar de descartarlo o de hacer fallar el procesamiento.
`action`
`platform`
`role`

## Acciones ( activityLog[].action ) ​
`activityLog[].action`
Notificaciones enviadas por Auco
PARAMETROS: action | Significado ;; NOTIFICATION_SIGN | Invitación a firmar enviada ;; NOTIFICATION_APPROVER | Invitación a aprobar enviada ;; NOTIFICATION_FINISH | Notificación de finalización enviada ;; NOTIFICATION_FAILED_SIGN | Invitación a firmar fallida
Recordatorios
PARAMETROS: action | Significado ;; REMINDER_SIGN | Recordatorio de firma enviado ;; REMINDER_APPROVE | Recordatorio de aprobación enviado ;; REMINDER_UPLOAD | Recordatorio de carga ;; REMINDER_PAYMENT | Recordatorio de pago
Los recordatorios pueden venir de la programación automática del proceso o de un envío manual con POST /document/reminder .
`POST /document/reminder`
Acciones del participante
PARAMETROS: action | Significado ;; PARTICIPANT_READ | Documento visto ;; PARTICIPANT_SIGN | Documento firmado ;; PARTICIPANT_APPROVE | Documento aprobado ;; PARTICIPANT_REJECT | Documento rechazado ;; READ_PARTICIPANT | Documento visto
`READ_PARTICIPANT`
`PARTICIPANT_READ`
Algunos procesos registran el evento de lectura como READ_PARTICIPANT . Significa exactamente lo mismo que PARTICIPANT_READ : el participante abrió el documento. Si clasificas eventos por su valor de action , trata los dos como el mismo evento .
`READ_PARTICIPANT`
`PARTICIPANT_READ`
`action`
Cambios en el proceso
PARAMETROS: action | Significado ;; UPDATE_SIGNER | Participante actualizado ;; UPDATE_SIGN | Firma actualizada ;; CANCEL_SIGN | Proceso cancelado ;; REACTIVATION_SIGN | Proceso reactivado

## Roles ( participants[].role ) ​
`participants[].role`
PARAMETROS: Valor | Significado | Descripción ;; SIGNER | Firmante | Debe firmar el documento. Es el rol por defecto. ;; APPROVER | Aprobador | Debe aprobar o rechazar el documento, sin firmarlo. ;; READER | Observador | Recibe el documento para consultarlo; no firma ni aprueba.
El rol se define al crear el proceso y se devuelve tal cual, así que también puedes encontrar valores propios de tu integración.

## Plataformas ( activityLog[].platform ) ​
`activityLog[].platform`
PARAMETROS: Valor | Descripción ;; EMAIL | El evento ocurrió por correo electrónico. ;; WHATSAPP | El evento ocurrió por WhatsApp. ;; ARCHIVE | El evento se ejecutó desde el archivo web de Auco, no desde un canal al participante.
Cuando platform es WHATSAPP puedes obtener el detalle de la conversación —los mensajes y sus estados de entrega— con GET /whatsapp/records .
`platform`
`WHATSAPP`
`GET /whatsapp/records`

## Eventos del proceso ( participant: "ARCHIVE" ) ​
`participant: "ARCHIVE"`
Algunos eventos no pertenecen a un participante sino al proceso completo: por ejemplo, una cancelación hecha desde el archivo web de Auco. Esos eventos llegan con participant: "ARCHIVE" y su campo by identifica al usuario de tu organización que ejecutó la acción, no a un firmante.
`participant: "ARCHIVE"`
Trátalos como eventos a nivel de proceso: no intentes resolver ARCHIVE contra participants[].id , porque nunca habrá coincidencia.
`ARCHIVE`
`participants[].id`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Error de validación del parámetro code (falta, o su longitud no está entre 9 y 10 caracteres), o proceso no encontrado ( DOCUMENT_NOT_FOUND ). ;; 401 | Autenticación inválida o ausente
DOCUMENT_NOT_FOUND se devuelve cuando el proceso no existe o cuando no pertenece a la organización de la llave pública con la que consultas.
`DOCUMENT_NOT_FOUND`
Autenticación
Parámetros de consulta
🧪 Ejemplos de uso 🔹 Obtener la trazabilidad de un proceso
🔹 Obtener la trazabilidad de un proceso
📥 Ejemplos de respuesta 🔹 Proceso firmado por WhatsApp 🔸 Proceso con varios participantes, un rechazo y una cancelación 🔸 Proceso creado sin notificar
🔹 Proceso firmado por WhatsApp
🔸 Proceso con varios participantes, un rechazo y una cancelación
🔸 Proceso creado sin notificar
📋 Campos de la respuesta
📖 Diccionario de trazabilidad Acciones ( activityLog[].action ) Roles ( participants[].role ) Plataformas ( activityLog[].platform ) Eventos del proceso ( participant: "ARCHIVE" )
Acciones ( activityLog[].action )
`activityLog[].action`
Roles ( participants[].role )
`participants[].role`
Plataformas ( activityLog[].platform )
`activityLog[].platform`
Eventos del proceso ( participant: "ARCHIVE" )
`participant: "ARCHIVE"`
⚠️ Respuestas de error