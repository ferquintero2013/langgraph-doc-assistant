# api/aucoface/create

> Fuente: https://docs.auco.ai/api/aucoface/create

`/veriface`
`prk _`
Servicio para la creación de un proceso que permite validar mediante las fotografias de documento y rostro de la persona, notificando al usuario mediante email o WhatsApp.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`
La notificacion por email solo esta disponible mediante la integración del modulo auco-sdk-integration

## Parámetros de consulta ​
PARAMETROS: Nombre | Descripción ;; email String | Obligatorio. Correo electrónico del creador del proceso. Este correo debe estar registrado en la plataforma de Auco y debe pertenecer a la organización. ;; platform String | Obligatorio. Plataforma por la cual se realizará la validación. Valores aceptados: whatsapp , web ;; name String | Obligatorio. Nombre de la persona a validar. ;; phone String | Condicional. Obligatorio solo cuando platform es whatsapp . Telefono con indicativo de país de la persona a validar. El formato aceptado es +[Código de País][Número de Teléfono] Ejemplo: +573003003030 ;; country String | Obligatorio. País de la persona a validar. Consulta la lista de documentos y países ;; type String | Obligatorio. Tipo de documento de la persona a validar. Consulta la lista de documentos y países ;; identification String | Obligatorio. Número de identificación de la persona a validar. ;; userEmail String | Opcional. Correo electrónico de la persona a validar. ;; custom Object | Opcional. Acá puedes guardar información adicional que requieras agregar a la notificación via webhook en cada etapa del flujo. Ejemplo: {"reference": "RF-XXXXXXX"} ;; expiredDate Date | Opcional. Fecha de expiración del documento. Esta debe ser mayor a 3 días de la fecha de creación del proceso y se envia en formato Date JSON . ;; targetWebhooks Array<String> | Opcional. Lista de webhooks a ser notificados. En caso de no definir se envia al webhook "default". ;; tags Array<String> | Opcional. Lista de tags que se envian cuando notifique al los webhooks configurados. ;; validationTypes Array<String> | Opcional. Solo disponible cuando platform es web . Tipos de validación a solicitar. Valores aceptados: photo , identification , identificationBack (mínimo 1, sin duplicados). Si se incluye identificationBack también debe incluirse identification .

## 🧪 Ejemplos de uso ​
Curl
Python
Node.js
`curl -X POST '{{api_auco}}/veriface' \ -H 'Authorization: {{private_key}}' \ -d '{ "email": "prueba@auco.ai", "platform": "whatsapp", "name": "Juan Pérez", "phone": "+573003003030", "country": "CO", "type": "CC", "identification": "1001001010" }'`
`import requests response = requests . post ( '{{api_auco}}/veriface' , headers = { 'Authorization' : '{{private_key}}' } , json = { "email" : "prueba@auco.ai" , "platform" : "whatsapp" , "name" : "Juan Pérez" , "phone" : "+573003003030" , "country" : "CO" , "type" : "CC" , "identification" : "1001001010" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . post ( '{{api_auco}}/veriface' , { email : "prueba@auco.ai" , platform : "whatsapp" , name : "Juan Pérez" , phone : "+573003003030" , country : "CO" , type : "CC" , identification : "1001001010" } , { headers : { Authorization : '{{private_key}}' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​
Creación exitosa.
Fecha de expiración incorrecta.
`{ "code" : "VERIFACE_CODE" }`
`{ "message" : "EXPIRED_DATE_INVALID" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros obligatorios como email , platform , name , phone , country , type o identification . Formato incorrecto de phone o expiredDate . ;; 401 | Autenticación inválida o ausente.
Autenticación
Parámetros de consulta
🧪 Ejemplos de uso
📥 Ejemplos de respuesta
⚠️ Respuestas de error