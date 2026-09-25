# api/manager/packages/reminder

> Fuente: https://docs.auco.ai/api/manager/packages/reminder

`/document/many/reminder`
`prk _`
Con este servicio puedes enviar recordatorios de firma y/o aprobación a los participantes de tu paquete documental de forma manual, esta es una alternativa a los recordatorios automáticos que defines al momento de la creación.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; package | String requerido | Identificador del paquete de documentos concatenado con el id de firmante ej: ['packageId77'], siendo 77 el di de firmante.

## 🧪 Ejemplo de uso ​

## Recordatorio a participante para firma/aprobación ​
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/many/reminder' \ -- header 'Authorization: prk_public_key_company' \ -- header 'Content-Type: application/json' \ -- data ' { "package" : "packageId77" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/many/reminder" payload = json . dumps ( { "package" : "packageId77" } ) headers = { 'Authorization' : 'prk_public_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { package : 'packageId77' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/many/reminder' , headers : { Authorization : 'prk_public_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Ejemplo de respuesta ​
`{ "message" : "REMINDER_SENT" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | No se logra encontrar el documento o es erróneo el id de firmante. ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación
🧪 Ejemplo de uso
Recordatorio a participante para firma/aprobación
Ejemplo de respuesta
⚠️ Respuestas de error