# api/company/get

> Fuente: https://docs.auco.ai/api/company/get

Servicio para consultar los datos de tu organización: nombre, logo, opciones de personalización visual (marca blanca) y los webhooks configurados.
`/company`
`puk _`

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
Este servicio no recibe parámetros. La organización se identifica a partir de la llave pública enviada en el encabezado Authorization .
`Authorization`

## Estructura de la respuesta ​
PARAMETROS: Campo | Tipo | Descripción ;; id | String | Identificador de la organización. ;; name | String | Nombre de la organización. ;; webhooks | Array | Lista de webhooks configurados. Cada elemento contiene id , description , url y header . Ver Webhooks . ;; uxOptions | Object | Opciones de personalización visual (marca blanca), por ejemplo primaryColor y alternateColor . ;; image | String | URL del logo de la organización. ;; webhook | String | (Legacy) URL del webhook único. Se mantiene por compatibilidad; usa webhooks . ;; webhookHeader | Object | (Legacy) Header { key, value } del webhook único. Se mantiene por compatibilidad; usa webhooks .
webhook y webhookHeader se devuelven solo para integraciones antiguas. La configuración actual de notificaciones se realiza mediante el arreglo webhooks (ver Webhooks ).
`webhook`
`webhookHeader`
`webhooks`

## 🧪 Ejemplo de uso ​
Curl
Python
Node.js
`curl -X GET 'https://api.auco.ai/v1.5/ext/company' \ -H 'Authorization: puk_public_key_company'`
`import requests response = requests . get ( 'https://api.auco.ai/v1.5/ext/company' , headers = { 'Authorization' : 'puk_public_key_company' } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/company' , { headers : { Authorization : 'puk_public_key_company' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplo de respuesta ​
`{ "id" : "61ba073970df523d9d232a27" , "name" : "Auco" , "webhooks" : [ { "id" : "default" , "description" : "Webhook principal" , "url" : "https://miempresa.com/webhooks/auco" , "header" : { "key" : "Authorization" , "value" : "Bearer ..." } } ] , "uxOptions" : { "primaryColor" : "#021C30" , "alternateColor" : "#A557F2" } , "image" : "https://static.micontrato.co/companies/61ba073970df523d9d232a27/logo.png" , "webhook" : "" , "webhookHeader" : { } }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de consulta
Estructura de la respuesta
🧪 Ejemplo de uso
📥 Ejemplo de respuesta
⚠️ Respuestas de error