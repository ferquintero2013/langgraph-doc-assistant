# api/manager/documents/reminder

> Fuente: https://docs.auco.ai/api/manager/documents/reminder

`/document/reminder`
`prk _`
Con este servicio puedes enviar recordatorios de firma y/o aprobación a los participantes de tu flujo documental de forma manual, esta es una alternativa a los recordatorios automáticos que defines al momento de la creación.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String requerido | Código del documento concatenado con el id de firmante ej: ['DOCUMENTCODEID']

## 🧪 Ejemplo de uso ​

## Recordatorio a participante para firma/aprobación ​
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/reminder' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data ' { "code" : "DCUMENTCODEID" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/reminder" payload = json . dumps ( { "code" : "NV97C00ZBC67" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { code : 'NV97C00ZBC67' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/reminder' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Ejemplos de respuesta ​
`{ "message" : "OK" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | No se logra encontrar el documento o es erróneo el id de firmante. ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación
🧪 Ejemplo de uso
Recordatorio a participante para firma/aprobación
Ejemplos de respuesta
⚠️ Respuestas de error