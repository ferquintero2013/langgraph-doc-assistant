# api/webhooks/document

> Fuente: https://docs.auco.ai/api/webhooks/document

Para cada estado del documento, se genera una petición con el siguiente cuerpo, variando en la descripción del estado (status).
Auco corta la conexión si tu endpoint no responde en 10 segundos. Tanto un timeout como una respuesta 4xx o 5xx se reintentan hasta 3 veces antes de descartar la notificación. Devuelve 200 de inmediato, procesa en segundo plano y haz tu handler idempotente. Ver Tiempo de respuesta y reintentos .
`4xx`
`5xx`
`200`

## Estados notificados ​
PARAMETROS: Nombre | Descripción ;; CREATE | Este estado se notifica cuando se crea un documento o se carga un PDF a la plataforma. ;; FINISH | Este estado se notifica cuando todas las partes firmaron el documento. ;; NOTIFICATION | Este estado se notificará cuando un participante del documento ha realizado el proceso de firma. ;; REJECT | Este estado se notifica cuando al menos un firmante ha rechazado la firma del documento. ;; REJECTED | Este evento muestra el detalle de la cancelación del proceso. ;; BLOCKED | Este estado es notificado cuando uno de los firmantes a excedido el número de intentos de validación de identidad (3) y requiere de una validación manual. ;; EXPIRED | Este estado se notificará cuando el documento haya expirado, solo si tiene fecha de expiración; esta fecha es definida en la creación del mismo.

## 🧪 Ejemplos de notificaciones ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## Parámetros de respuesta ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String | Código del documento. ;; name | String | Nombre del documento. ;; signer | Object | Información del firmante, presente únicamente cuando el estado es NOTIFICATION , BLOCKED o REJECTED . ;; url | String | url del documento. ;; status | String | Estado actual del proceso de firma ( CREATE , FINISH , NOTIFICATION , REJECT , REJECTED , BLOCKED o EXPIRED ). ;; message | String | Contenido textual asociado al estado del firmante. Si el estado es REJECTED , contiene el mensaje individual escrito por el participante. En caso de BLOCKED . ;; similarity | Number | Porcentaje de similitud de la validación de identidad facial, presente cuando aplica. ;; scores | Object | Detalle de puntajes de la validación de identidad, presente cuando aplica. ;; tags | Array | Lista de etiquetas asignadas al documento, si fueron definidas durante su creación. ;; custom | Array | Lista de campos personalizados registrados en el documento, si fueron especificados.

## Creación de proceso ​
JSON
`{ "code" : "DOCUMENTCODE" , //Código del documento "name" : "Contrato de prueba del API" , //Nombre del documento "status" : "CREATE" , //Estado del documento "url" : "https://test.auco.ai/contrato-de-prueba-id-98-DOCUMENTCODE.pdf" // url del documento }`

## Finalización del proceso ​
JSON
`{ "code" : "DOCUMENTCODE" , "name" : "Contrato de prueba del API" , "status" : "FINISH" , "url" : "https://test.auco.ai/contrato-de-prueba-id-98-DOCUMENTCODE.pdf" // url del documento }`

## Firma de un participante ​
JSON
`{ "code" : "DOCUMENTCODE" , "name" : "Contrato de prueba del API" , "signer" : { "id" : "participant_id" , "name" : "participant name" , "email" : "email" , "phone" : "phone" } , "status" : "NOTIFICATION" }`

## Bloqueo de firmante ​
JSON
`{ "name" : "document name" , "signer" : { "id" : "participan_id" , "name" : "participant name" , "email" : "email" , "phone" : "phone" } , "status" : "BLOCKED" , "message" : "OTP_CODE_INVALID" , "tags" : [ "document tag" ] , "custom" : [ "{'info':'required', 'definition': 'urgent'}" ] }`

## Detalle de rechazo ​
JSON
`{ "name" : "document name" , "signer" : { "id" : "participan_id" , "name" : "participant name" , "email" : "email" , "phone" : "phone" } , "status" : "REJECTED" , "message" : "message" , "tags" : [ "document tags" ] }`

## Expiración de proceso ​
JSON
`{ "code" : "DOCUMENTCODE" , "name" : "Contrato de prueba del API" , "status" : "EXPIRED" , "url" : "https://test.auco.ai/contrato-de-prueba-id-98-DOCUMENTCODE.pdf" , "tags" : [ "document tag" ] , "custom" : [ "{'info':'required', 'definition': 'urgent'}" ] }`
Estados notificados
🧪 Ejemplos de notificaciones Parámetros de respuesta Creación de proceso Finalización del proceso Firma de un participante Bloqueo de firmante Detalle de rechazo Expiración de proceso
Parámetros de respuesta
Creación de proceso
Finalización del proceso
Firma de un participante
Bloqueo de firmante
Detalle de rechazo
Expiración de proceso