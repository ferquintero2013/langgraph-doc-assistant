# api/webhooks/veriface

> Fuente: https://docs.auco.ai/api/webhooks/veriface

Para cada estado del documento, se genera una petición con el siguiente cuerpo, variando en la descripción del estado (status).
Auco corta la conexión si tu endpoint no responde en 10 segundos. Tanto un timeout como una respuesta 4xx o 5xx se reintentan hasta 3 veces antes de descartar la notificación. Devuelve 200 de inmediato, procesa en segundo plano y haz tu handler idempotente. Ver Tiempo de respuesta y reintentos .
`4xx`
`5xx`
`200`

## Estados notificados ​
PARAMETROS: Nombre | Descripción ;; APPROVED | Este estado se notifica se ha validado el proceso de forma exitosa. ;; BLOCKED | Este estado se notifica cuando el proceso no pudo ser validado de forma automática y se encuentra en estado bloqueado. ;; VALIDATED | Este estado se notifica se valida un proceso de forma manual. ;; INVALIDATED | Este estado se notifica cuando se rechaza un proceso de forma manual.

## 🧪 Ejemplos de notificaciones ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## Parámetros de respuesta ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String | Código del documento. ;; type | String | Tipo del proceso notificado veriface . ;; finish | Boolean | Retorna si el proceso se encuentra en estado finalizado. ;; status | String | Estado actual del proceso (ej. APPROVED , BLOCKED , VALIDATED , INVALIDATED ). ;; message | String | Contenido textual asociado al estado del proceso. Si el estado es BLOCKED , contiene el error motivo de bloqueo. ;; data | Object | Objeto con el OCR extraido del documento enviado por el participante.

## Finalización del proceso ​
JSON
`{ "code" : "XXXXXCODE" , "type" : "veriface" , "status" : "APPROVED" , "finish" : true , "data" : { "name" : "JUAN PEREZ GONZALEZ" , "documentName" : "DNI 12345678" } , "similarity" : 0.92 }`

## Bloqueo de proceso ​
JSON
`{ "code" : "XXXXXCODE" , "type" : "veriface" , "finish" : true , "status" : "BLOCKED" , "message" : "ERROR_IDENTIFICATION_NOT_DOCUMENT" , "data" : { "name" : null , "documentName" : "" } }`

## Proceso validado manualmente ​
JSON
`{ "code" : "XXXXXCODE" , "type" : "veriface" , "finish" : true , "status" : "VALIDATED" , "data" : { "name" : "JUAN PEREZ GONZALEZ" , "documentName" : "DNI 12345678" } }`

## Proceso rechazado manualmente ​
JSON
`{ "code" : "XXXXXCODE" , "type" : "veriface" , "finish" : true , "status" : "INVALIDATED" , "data" : { "name" : null , "documentName" : "" } }`
Estados notificados
🧪 Ejemplos de notificaciones Parámetros de respuesta Finalización del proceso Bloqueo de proceso Proceso validado manualmente Proceso rechazado manualmente
Parámetros de respuesta
Finalización del proceso
Bloqueo de proceso
Proceso validado manualmente
Proceso rechazado manualmente