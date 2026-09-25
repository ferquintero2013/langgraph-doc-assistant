# api/company/update

> Fuente: https://docs.auco.ai/api/company/update

Servicio para actualizar los datos de tu organización: nombre, logo, personalización visual (marca blanca) y webhooks. Todos los campos son opcionales ; solo se modifican los que envíes.
`/company`
`prk _`

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de actualización ​
PARAMETROS: Nombre | Tipo | Requerido | Descripción ;; name | String | Opcional | Nombre de la organización. ;; image | String | Opcional | URL del logo de la organización. ;; uxOptions | Object | Opcional | Opciones de personalización visual (marca blanca). Solo se actualizan las claves enviadas (ver nota de merge). ;; uxOptions.primaryColor | String | Condicional | Color principal de la marca en formato hexadecimal ( #RGB o #RRGGBB ). No puede ser blanco ( #fff / #ffffff ). ;; uxOptions.alternateColor | String | Condicional | Color secundario de la marca en formato hexadecimal ( #RGB o #RRGGBB ). ;; webhooks | Array | Opcional | Lista completa de webhooks. Reemplaza la configuración existente (mínimo 1, debe incluir el default ). Ver Webhooks .
`uxOptions`
Al enviar uxOptions , solo se modifican las claves incluidas en la petición; el resto de la personalización guardada se conserva. Por ejemplo, enviar solo primaryColor no borra el alternateColor ya configurado.
`uxOptions`
`primaryColor`
`alternateColor`
`webhooks`
A diferencia de uxOptions , el arreglo webhooks sustituye por completo la lista guardada. Para conservar webhooks existentes debes incluirlos en la petición, y la lista siempre debe contener el webhook con id: "default" . Consulta la sección Webhooks para el detalle de cada campo.
`uxOptions`
`webhooks`
`id: "default"`

## 🧪 Ejemplos de uso ​

## Actualizar nombre, logo y colores ​
Curl
Python
Node.js
`curl -X PUT 'https://api.auco.ai/v1.5/ext/company' \ -H 'Authorization: prk_private_key_company' \ -H 'Content-Type: application/json' \ -d '{ "name": "Mi Empresa", "image": "https://miempresa.com/logo.png", "uxOptions": { "primaryColor": "#021C30", "alternateColor": "#A557F2" } }'`
`import requests import json url = "https://api.auco.ai/v1.5/ext/company" payload = json . dumps ( { "name" : "Mi Empresa" , "image" : "https://miempresa.com/logo.png" , "uxOptions" : { "primaryColor" : "#021C30" , "alternateColor" : "#A557F2" } } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "PUT" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; const data = JSON . stringify ( { name : 'Mi Empresa' , image : 'https://miempresa.com/logo.png' , uxOptions : { primaryColor : '#021C30' , alternateColor : '#A557F2' } } ) ; const config = { method : 'put' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/company' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' } , data } ; axios . request ( config ) . then ( ( response ) => console . log ( JSON . stringify ( response . data ) ) ) . catch ( ( error ) => console . log ( error ) ) ;`

## Configurar webhooks ​
Recuerda enviar la lista completa de webhooks, incluyendo siempre el default . Para el detalle de cada campo consulta la sección Webhooks .
`default`
Curl
Python
Node.js
`curl -X PUT 'https://api.auco.ai/v1.5/ext/company' \ -H 'Authorization: prk_private_key_company' \ -H 'Content-Type: application/json' \ -d '{ "webhooks": [ { "id": "default", "description": "Webhook principal", "url": "https://miempresa.com/webhooks/auco", "header": { "key": "Authorization", "value": "Bearer ..." } }, { "id": "billing", "description": "Webhook de facturación", "url": "https://miempresa.com/webhooks/billing" } ] }'`
import requests import json url = "https://api.auco.ai/v1.5/ext/company" payload = json . dumps ( { "webhooks" : [ { "id" : "default" , "description" : "Webhook principal" , "url" : "https://miempresa.com/webhooks/auco" , "header" : { "key" : "Authorization" , "value" : "Bearer ..." } } , { "id" : "billing" , "description" : "Webhook de facturación" , "url" : "https://miempresa.com/webhooks/billing" } ] } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "PUT" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; const data = JSON . stringify ( { webhooks : [ { id : 'default' , description : 'Webhook principal' , url : 'https://miempresa.com/webhooks/auco' , header : { key : 'Authorization' , value : 'Bearer ...' } } , { id : 'billing' , description : 'Webhook de facturación' , url : 'https://miempresa.com/webhooks/billing' } ] } ) ; const config = { method : 'put' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/company' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' } , data } ; axios . request ( config ) . then ( ( response ) => console . log ( JSON . stringify ( response . data ) ) ) . catch ( ( error ) => console . log ( error ) ) ;

## 📥 Ejemplo de respuesta ​
`{ "response" : "OK" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Datos inválidos: color fuera de formato hexadecimal, primaryColor en blanco, o falta el webhook default . ;; 401 | Autenticación inválida o ausente.
Autenticación
Parámetros de actualización
🧪 Ejemplos de uso Actualizar nombre, logo y colores Configurar webhooks
Actualizar nombre, logo y colores
Configurar webhooks
📥 Ejemplo de respuesta
⚠️ Respuestas de error