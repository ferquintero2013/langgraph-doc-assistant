# api/manager/documents/cancel

> Fuente: https://docs.auco.ai/api/manager/documents/cancel

`/document/cancel`
`prk _`
Con este servicio puedes cancelar uno o varios documentos. Este servicio notifica a los firmantes del documento que ha sido cancelado, con un mensaje explicando la cancelación de el o los documentos.
Para poder cancelar un documento este no debe estar firmado en su totalidad o no ser rechazado anteriormente .
Esta acción es notificada también via WEBHOOK.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; codes | Array requerido | Lista de códigos de documentos a cancelar ej: ['TR99AQMY31'] ;; message | String requerido | Parámetro que determina el mensaje que justifica la cancelación, este mensaje se envía a los firmantes ya notificados previamente o que ya han firmado para firma. ;; email | String requerido | Este parámetro se envía cuando se requiera guardar registro del usuario que cancela el documento.

## 🧪 Ejemplos de uso ​

## Cancelación de un proceso ​
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/cancel' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "codes" : [ "DOCUMENTCODE" ] , "email" : "example@auco.ai" , "message" : "Cancelación por error en cláusula II..." } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/cancel" payload = json . dumps ( { "codes" : [ "DOCUMENTCODE" ] , "email" : "example@auco.ai" , "message" : "Cancelación por error en cláusula II..." } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { codes : [ 'DOCUMENTCODE' ] , email : 'example@auco.ai' , message : 'Cancelación por error en cláusula II...' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/cancel' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Ejemplos de respuesta ​

## cancelación de un documento ​
`{ "success" : 1 , "errors" : { "cant" : 0 } }`

## Cancelación de varios documentos ​
`{ "success" : 2 , "errors" : { "cant" : 1 , "documents" : [ "DOCUMENTCODE" ] } }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, o alguna de las validaciones no coinciden con las condiciones de aplicabilidad ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación
🧪 Ejemplos de uso Cancelación de un proceso
Cancelación de un proceso
Ejemplos de respuesta cancelación de un documento Cancelación de varios documentos
cancelación de un documento
Cancelación de varios documentos
⚠️ Respuestas de error