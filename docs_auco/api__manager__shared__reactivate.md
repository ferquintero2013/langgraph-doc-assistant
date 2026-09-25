# api/manager/shared/reactivate

> Fuente: https://docs.auco.ai/api/manager/shared/reactivate

`/document/reactivate`
`prk _`
Con este servicio puedes reactivar un proceso de firma que haya sido rechazado o que haya expirado. Al reactivarse, el sistema notifica a los firmantes pendientes y a quienes rechazaron, permitiéndoles continuar con el proceso. Si el proceso contaba con una fecha de expiración vencida, esta se recalcula automáticamente según la configuración de la organización.
Este servicio aplica para procesos que se encuentren en estado rechazado o expirado . Si el proceso estaba expirado, la fecha de vencimiento se recalcula automáticamente según la configuración de la organización.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String condicional | Código del documento a reactivar. Requerido si no se envía package . ;; package | String condicional | Código del paquete a reactivar. Requerido si no se envía code . ;; email | String requerido | Email del usuario que realiza la reactivación. Se guarda como registro de la acción.
Los campos code y package son mutuamente excluyentes: debes enviar uno y solo uno de los dos.
`code`
`package`

## 🧪 Ejemplos de uso ​

## Reactivar un documento ​
curl
Python
Node.js
`curl -- location -- request PUT 'https://api.auco.ai/v1.5/ext/document/reactivate' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "code" : "DOCUMENTCODE" , "email" : "manager@auco.ai" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/reactivate" payload = json . dumps ( { "code" : "DOCUMENTCODE" , "email" : "manager@auco.ai" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "PUT" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { code : 'DOCUMENTCODE' , email : 'manager@auco.ai' , } ) ; let config = { method : 'put' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/reactivate' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Reactivar un paquete ​
curl
Python
Node.js
`curl -- location -- request PUT 'https://api.auco.ai/v1.5/ext/document/reactivate' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "package" : "PACKAGECODE" , "email" : "manager@auco.ai" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/reactivate" payload = json . dumps ( { "package" : "PACKAGECODE" , "email" : "manager@auco.ai" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "PUT" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { package : 'PACKAGECODE' , email : 'manager@auco.ai' , } ) ; let config = { method : 'put' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/reactivate' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Ejemplos de respuesta ​

## Respuesta exitosa ​
`{ "notifications" : 2 , "users" : [ "Juan Pérez" , "María García" ] }`
PARAMETROS: Campo | Tipo | Descripción ;; notifications | number | Cantidad de notificaciones enviadas a los firmantes ;; users | Array | Nombres de los firmantes que recibieron notificación

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, o alguna de las validaciones no coinciden con las condiciones de aplicabilidad ;; 401 | Autenticación inválida o ausente ;; 400 | PROCESS_NOT_FOUND — El proceso no fue encontrado
Autenticación
Parámetros de creación
🧪 Ejemplos de uso Reactivar un documento Reactivar un paquete
Reactivar un documento
Reactivar un paquete
Ejemplos de respuesta Respuesta exitosa
Respuesta exitosa
⚠️ Respuestas de error