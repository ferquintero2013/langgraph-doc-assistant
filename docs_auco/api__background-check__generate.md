# api/background-check/generate

> Fuente: https://docs.auco.ai/api/background-check/generate

`/validate/background`
`prk _`
Servicio para realizar generar la validación de antecedentes de un usuario. La validación generada puede tardar hasta 1 minuto en estar lista para poder ser consultada mediante el servicio de consulta .

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Descripción ;; email String | Obligatorio. Correo electrónico del creador del proceso. Este correo debe estar registrado en la plataforma de Auco y debe pertenecer a la organización. ;; identification String | Obligatorio. Número de identificación de la persona a consultar. ;; type String | Obligatorio. Tipo de documento de identificación de la persona a consultar. Ver Tipos de documento aceptados . ;; name String | Condicional. Nombre completo de la persona a consultar. Requerido según el type (ver tabla). ;; expeditionDate String | Condicional. Fecha de expedicion del documento de identificación. Requerida según el type (ver tabla). Formato aceptado: 01/01/1995 ;; targetWebhooks Array<String> | Opcional. Lista de webhooks a ser notificados. En caso de no definir se envia al webhook "default". ;; tags Array<String> | Opcional. Lista de tags que se envian cuando notifique al los webhooks configurados. ;; custom Object | Opcional. Objeto libre que se almacena junto al proceso y se reenvía en las notificaciones de webhook.

## Tipos de documento aceptados ​
El valor de type determina qué campos adicionales son obligatorios.
`type`
PARAMETROS: type | Documento | Campos adicionales requeridos ;; CC | Cédula de ciudadanía | — ;; CE | Cédula de extranjería | — ;; NIT | NIT | — ;; PPT | Permiso por Protección Temporal | expeditionDate ;; PP | Pasaporte | name ;; INT | Internacional | name

## 🧪 Ejemplos de uso ​
Curl
Python
Node.js
Pasaporte (PP)
Internacional (INT)
`curl -X POST '{{api_auco}}/validate/background' \ -H 'Authorization: {{private_key}}' \ -d '{ "email": "prueba@auco.ai", "type": "CC", "identification": "1001001010", "expeditionDate": "01/01/1995" }'`
`import requests response = requests . post ( '{{api_auco}}/validate/background' , headers = { 'Authorization' : '{{private_key}}' } , json = { "email" : "prueba@auco.ai" , "type" : "CC" , "identification" : "1001001010" , "expeditionDate" : "01/01/1995" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . post ( '{{api_auco}}/validate/background' , { email : "prueba@auco.ai" , type : "CC" , identification : "1001001010" , expeditionDate : "01/01/1995" } , { headers : { Authorization : '{{private_key}}' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`
`curl -X POST '{{api_auco}}/validate/background' \ -H 'Authorization: {{private_key}}' \ -d '{ "email": "prueba@auco.ai", "type": "PP", "identification": "AB123456", "name": "NOMBRE COMPLETO" }'`
`curl -X POST '{{api_auco}}/validate/background' \ -H 'Authorization: {{private_key}}' \ -d '{ "email": "prueba@auco.ai", "type": "INT", "identification": "AB123456", "name": "NOMBRE COMPLETO" }'`

## 📥 Ejemplos de respuesta ​
Validación exitosa.
`{ "name" : "NOMBRE" , "code" : "XXXXXXXXX" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros como email , type o identification . Falta name cuando type es PP o INT , o expeditionDate cuando type es PPT . Formato incorrecto de expeditionDate . ;; 401 | Autenticación inválida o ausente.
Autenticación
Parámetros de consulta
Tipos de documento aceptados
🧪 Ejemplos de uso
📥 Ejemplos de respuesta
⚠️ Respuestas de error