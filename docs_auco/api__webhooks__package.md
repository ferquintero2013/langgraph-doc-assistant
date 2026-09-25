# api/webhooks/package

> Fuente: https://docs.auco.ai/api/webhooks/package

Para cada estado del paquete de documentos, se genera una petición con el siguiente cuerpo, variando en la descripción del estado (status).
Auco corta la conexión si tu endpoint no responde en 10 segundos. Tanto un timeout como una respuesta 4xx o 5xx se reintentan hasta 3 veces antes de descartar la notificación. Devuelve 200 de inmediato, procesa en segundo plano y haz tu handler idempotente. Ver Tiempo de respuesta y reintentos .
`4xx`
`5xx`
`200`

## Estados notificados ​
PARAMETROS: Nombre | Descripción ;; CREATE | Este estado se notifica cuando se crea un paquete de documentos. ;; NOTIFICATION | Este estado se notifica cuando un participante del paquete ha realizado su firma. ;; SIGNED_PACKAGE | Este estado se notifica cuando todas las partes firmaron el paquete de documentos. ;; DOCUMENT_REJECT | Este estado se notifica cuando uno de los documentos del paquete ha sido rechazado. ;; REJECTED | Este estado se notifica con el detalle del participante que rechazó el paquete. ;; BLOCKED | Este estado es notificado cuando uno de los firmantes a excedido el número de intentos de validación de identidad (3) y requiere de una validación manual.

## 🧪 Ejemplos de notificaciones ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## Parámetros de notificación ​
PARAMETROS: Nombre | Tipo | Descripción ;; package | String | Identificador del paquete de documentos. ;; name | String | Nombre del paquete de documentos. ;; status | String | Estado actual del paquete ( CREATE , NOTIFICATION , SIGNED_PACKAGE , DOCUMENT_REJECT , REJECTED o BLOCKED ). ;; signer | Object | Información del firmante, presente cuando el estado es NOTIFICATION , REJECTED o BLOCKED . ;; message | String | Mensaje asociado al estado del firmante. Si el estado es REJECTED , contiene el mensaje escrito por el participante al rechazar; si es BLOCKED , contiene el motivo del bloqueo. ;; documents | Array | Lista de documentos que hacen parte del paquete (ausente en los estados NOTIFICATION y REJECTED ). ;; documents.code | String | Código del documento. ;; documents.name | String | Nombre del documento. ;; documents.status | String | Estado del documento individual ( CREATE , FINISH , REJECT o EXPIRED ). ;; documents.url | String | url del documento. ;; tags | Array | Lista de etiquetas o campos personalizados asignados al paquete, si fueron definidos.

## Creación de proceso ​
JSON
`{ "package" : "idPackage" , //Identificador del paquete "name" : "Documentos de prueba del API" , //Nombre del paquete de documentos "status" : "CREATE" , //Estado del paquete de documentos "documents" : [ { "code" : "DOCUMENTCODE" , "name" : "Documento de prueba 1" , "status" : "CREATE" , "url" : "https://test.auco.ai/contrato-de-prueba1.pdf" } , { "code" : "DOCUMENTCODE" , "name" : "Documento de prueba 2" , "status" : "CREATE" , "url" : "https://test.auco.ai/contrato-de-prueba2.pdf" } ] }`

## Firma de un participante ​
JSON
`{ "package" : "idPackage" , "name" : "Documentos de prueba del API" , "signer" : { "id" : "participant_id" , "name" : "participant name" , "email" : "email" , "phone" : "phone" } , "status" : "NOTIFICATION" }`

## Finalización del proceso ón del proceso" translate="no">​
JSON
`{ "package" : "idPackage" , "name" : "Documentos de prueba del API" , "status" : "SIGNED_PACKAGE" , "documents" : [ { "code" : "DOCUMENTCODE" , "name" : "Documento de prueba 1" , "status" : "FINISH" , "url" : "https://test.auco.ai/contrato-de-prueba1.pdf" } , { "code" : "DOCUMENTCODE" , "name" : "Documento de prueba 2" , "status" : "FINISH" , "url" : "https://test.auco.ai/contrato-de-prueba2.pdf" } ] }`

## Rechazo de documento ​
JSON
`{ "package" : "idPackage" , "name" : "Documentos de prueba del API" , "status" : "DOCUMENT_REJECT" , "documents" : [ { "code" : "DOCUMENTCODE" , "name" : "Documento de prueba 1" , "status" : "REJECT" , "url" : "https://test.auco.ai/contrato-de-prueba1.pdf" } , { "code" : "DOCUMENTCODE" , "name" : "Documento de prueba 2" , "status" : "CREATE" , "url" : "https://test.auco.ai/contrato-de-prueba2.pdf" } ] }`

## Rechazo de un participante ​
JSON
`{ "package" : "idPackage" , "name" : "Documentos de prueba del API" , "signer" : { "id" : "participant_id" , "name" : "participant name" , "email" : "email" , "phone" : "phone" } , "status" : "REJECTED" , "message" : "message" }`

## Bloqueo de firmante ​
JSON
`{ "package" : "idPackage" , "name" : "Documentos de prueba del API" , "signer" : { "id" : "participant_id" , "name" : "participant name" , "email" : "email" , "phone" : "phone" } , "status" : "BLOCKED" , "message" : "OTP_CODE_INVALID" }`
Estados notificados
🧪 Ejemplos de notificaciones Parámetros de notificación Creación de proceso Firma de un participante Finalización del proceso Rechazo de documento Rechazo de un participante Bloqueo de firmante
Parámetros de notificación
Creación de proceso
Firma de un participante
Finalización del proceso
Rechazo de documento
Rechazo de un participante
Bloqueo de firmante