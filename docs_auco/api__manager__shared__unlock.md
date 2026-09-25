# api/manager/shared/unlock

> Fuente: https://docs.auco.ai/api/manager/shared/unlock

`/document/unlock`
`prk _`
Con este servicio puedes gestionar firmantes bloqueados durante el proceso de validación de identidad, tanto en documentos como en paquetes . Este servicio permite aprobar, rechazar, reiniciar o cancelar el proceso para firmantes que han sido bloqueados por el sistema de seguridad.
Este servicio solo aplica para firmantes que se encuentren en estado bloqueado durante la validación de identidad.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String requerido | Código del documento o paquete concatenado al ID del firmante (ej: DOCUMENTCODEID o PACKAGECODEID ) ;; email | String requerido | Email del usuario de la organización que aprueba o rechaza el participante bloqueado ;; status | String requerido | Acción a realizar: approve , reject , reset , cancel ;; message | String condicional | Nota del aprobador o motivo. Es requerido cuando status es approve o cancel . No se acepta en reject ni reset
El campo code identifica tanto documentos como paquetes: corresponde al código del documento (o del paquete) concatenado con el ID del firmante bloqueado. El sistema detecta automáticamente el tipo de proceso.
`code`

## Acciones disponibles ​
approve : Aprueba la validación de identidad del firmante (requiere campo message )
`message`
reject : Rechaza la validación de identidad del firmante
reset : Reinicia el proceso (Solo aplica para firma por WhatsApp, en caso contrario funciona igual que reject)
cancel : Cancela el proceso de firma (requiere campo message )
`message`

## 🧪 Ejemplos de uso ​

## Aprobar firmante bloqueado ​
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/unlock' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "code" : "DOCUMENTCODEID" , "email" : "approver@auco.ai" , "status" : "approve" , "message" : "Identidad verificada correctamente" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/unlock" payload = json . dumps ( { "code" : "DOCUMENTCODEID" , "email" : "approver@auco.ai" , "status" : "approve" , "message" : "Identidad verificada correctamente" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { code : 'DOCUMENTCODEID' , email : 'approver@auco.ai' , status : 'approve' , message : 'Identidad verificada correctamente' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/unlock' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## Aprobar firmante de un paquete ​
Para paquetes, el campo code corresponde al código del paquete concatenado con el ID del firmante.
`code`
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/unlock' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "code" : "PACKAGECODEID" , "email" : "approver@auco.ai" , "status" : "approve" , "message" : "Identidad verificada correctamente" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/unlock" payload = json . dumps ( { "code" : "PACKAGECODEID" , "email" : "approver@auco.ai" , "status" : "approve" , "message" : "Identidad verificada correctamente" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { code : 'PACKAGECODEID' , email : 'approver@auco.ai' , status : 'approve' , message : 'Identidad verificada correctamente' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/unlock' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## Cancelar proceso con motivo ​
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/unlock' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "code" : "DOCUMENTCODEID" , "email" : "approver@auco.ai" , "status" : "cancel" , "message" : "Intento de fraude detectado" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/document/unlock" payload = json . dumps ( { "code" : "DOCUMENTCODEID" , "email" : "approver@auco.ai" , "status" : "cancel" , "message" : "Intento de fraude detectado" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { code : 'DOCUMENTCODEID' , email : 'approver@auco.ai' , status : 'cancel' , message : 'Intento de fraude detectado' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/unlock' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Ejemplos de respuesta ​

## Respuesta exitosa ​
`{ "message" : "OK" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, validaciones no aplicables, falta ID del firmante en el código ( MISSING_SIGNER_ID ) o el proceso no está bloqueado ( NOT_BLOCKED_PROCESS ) ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación Acciones disponibles
Acciones disponibles
🧪 Ejemplos de uso Aprobar firmante bloqueado Aprobar firmante de un paquete Cancelar proceso con motivo
Aprobar firmante bloqueado
Aprobar firmante de un paquete
Cancelar proceso con motivo
Ejemplos de respuesta Respuesta exitosa
Respuesta exitosa
⚠️ Respuestas de error