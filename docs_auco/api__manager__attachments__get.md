# api/manager/attachments/get

> Fuente: https://docs.auco.ai/api/manager/attachments/get

`/attachments`
`puk _`
Este servicio permite consultar los anexos cargados por los firmantes dentro de un proceso. El comportamiento de la respuesta varía según se incluya o no el parámetro userId .
`userId`

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Tipo | Descripción ;; package | String condicional | ID del paquete del proceso. Obligatorio si no se incluye code . ;; code | String condicional | Código de documento asociado al proceso. Obligatorio si no se incluye package . ;; userId | String opcional | ID del usuario para obtener sus anexos y estado.
⚠️ Se debe enviar uno y solo uno entre package o code . Si se envían ambos, la petición será rechazada con error 400.
`package`
`code`

## Combinaciones válidas de uso ​
PARAMETROS: Método | Ruta | Descripción ;; GET | /attachments?package={packageId} | Consulta general del proceso ;; GET | /attachments?code={code} | Consulta general del proceso ;; GET | /attachments?package={packageId}&userId={userId} | Consulta de anexos por firmante usando package ;; GET | /attachments?code={code}&userId={userId} | Consulta de anexos por firmante usando código

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## 🔹 Obtener información general del proceso ​
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/attachments?package=package123' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/attachments" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "package" : "package123" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/attachments' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { package : 'package123' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 🔸 Obtener anexos de un firmante con package y userId ​
`package`
`userId`
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/attachments?package=package456&userId=userX' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/attachments" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "package" : "package456" , "userId" : "userX" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/attachments' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { package : 'package456' , userId : 'userX' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 🔸 Obtener anexos de un firmante con code y userId ​
`code`
`userId`
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/attachments?code=codeABC&userId=userY' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/attachments" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "code" : "codeABC" , "userId" : "userY" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/attachments' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { code : 'codeABC' , userId : 'userY' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​

## 🔹 Sin userId ​
`userId`
`{ "package" : "paquete123" , "name" : "Proceso de firma 001" , "finish" : true , "signers" : [ { "userId" : "01" , "email" : "usuario1@dominio.com" , "name" : "Usuario Uno" } ] }`

## 🔸 Con userId ​
`userId`
`{ "package" : "paquete123" , "name" : "Proceso de firma 001" , "finish" : true , "signer" : { "userId" : "01" , "email" : "usuario1@dominio.com" , "name" : "Usuario Uno" , "files" : [ { "name" : "Documento Identidad" , "url" : "https://..." } , { "name" : "Comprobante" , "url" : "https://..." } ] , "status" : "approved" } }`

## 🔄 Estado del firmante ( status ) ​
`status`
PARAMETROS: Estado | Descripción ;; pending | El usuario aún no ha cargado documentos. ;; uploaded | El usuario ya cargó documentos, pero aún no han sido aprobados. ;; approved | Todos los documentos han sido cargados y aprobados.
Los enlaces ( url ) de los archivos se incluyen solo si el status es distinto de pending . Son URLs firmadas temporales con una validez de 5 minutos (300 segundos); una vez expiradas debes consultar de nuevo el endpoint para obtener enlaces vigentes.
`url`
`status`
`pending`

## 🔚 Campo finish ​
`finish`
El campo finish: true indica que el proceso ha sido finalizado completamente y no se esperan más acciones.
`finish: true`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros package o code , o proceso no encontrado ( ATTACHMENT_NOT_FOUND ) ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de consulta
Combinaciones válidas de uso
🧪 Ejemplos de uso 🔹 Obtener información general del proceso 🔸 Obtener anexos de un firmante con package y userId 🔸 Obtener anexos de un firmante con code y userId
🔹 Obtener información general del proceso
🔸 Obtener anexos de un firmante con package y userId
`package`
`userId`
🔸 Obtener anexos de un firmante con code y userId
`code`
`userId`
📥 Ejemplos de respuesta 🔹 Sin userId 🔸 Con userId
🔹 Sin userId
`userId`
🔸 Con userId
`userId`
🔄 Estado del firmante ( status )
`status`
🔚 Campo finish
`finish`
⚠️ Respuestas de error