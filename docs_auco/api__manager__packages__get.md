# api/manager/packages/get

> Fuente: https://docs.auco.ai/api/manager/packages/get

`/document`
`puk _`
Este servicio permite consultar paquetes de documentos en Auco.

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Tipo | Descripción ;; package | String opcional | Id del paquete de documentos. Obligatorio si no se incluye code .
⚠️ Si no envías el atributo code o package , recibirás la lista de plantillas automatizadas .
`code`
`package`
Este mismo endpoint servirá para obtener información de un documento en específico, ver mas en consulta procesos y plantillas

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## 🔹 Obtener información general del proceso ​
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/document?code=ID_PACKAGE' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/document" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "package" : "ID_PACKAGE" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/document' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { package : 'ID_PACKAGE' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplo de respuesta ​
`{ "_id" : "ID_PACKAGE" , "codes" : [ "CODEDOC1" , "CODEDOC2" ] , "name" : "Prueba paquete de documentos" , "signers" : [ { "userId" : "AI" , "email" : "example1@auco.ai" , "name" : "Firmante 1" , "phone" : "+573000000000" , "status" : "NOTIFICATION" } , { "userId" : "OR" , "email" : "example2@auco.ai" , "name" : "Firmante 2" , "phone" : "+573000000000" , "status" : "NOTIFICATION" } ] , "signFinish" : false , "createdAt" : "2024-10-18T20:20:34.970Z" , "updatedAt" : "2024-11-15T02:02:12.775Z" , "status" : "CREATED" , "custom" : { "externalId" : "ORDER-123" , "source" : "crm" } }`
El campo custom sólo aparece si fue enviado al crear el paquete (ver POST /document/many ). Contiene exactamente los datos que el integrador envió, sin ninguna transformación por parte de Auco.
`custom`

## 🔄 Estado del documento ( status ) ​
`status`
PARAMETROS: Estado | Descripción ;; CREATED | Cuando el proceso ha sido creado. ;; REJECTED | Proceso rechazado. ;; EXPIRED | Proceso expirado, solo si al momento de crearlo se asigna fecha de expiración. ;; FINISH | Proceso firma o aprobado por todas las partes.

## 🔄 Estado del participante ( status ) ​
`status`
PARAMETROS: Estado | Descripción ;; NOTIFICATION | El participante ha sido notificado para firma. ;; REJECT | El participante ha rechazado la firma o aprobación del proceso. ;; FINISH | El participante ha firmado o aprobado el proceso. ;; BLOCK | El participante ha excedido los intentos fallidos al momento de firmar o aprobar. ;; PENDING | El participante no ha sido notificado, generalmente se debe a un proceso secuencial.

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | proceso no encontrado ( DOCUMENT_NOT_FOUND ) ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de consulta
🧪 Ejemplos de uso 🔹 Obtener información general del proceso
🔹 Obtener información general del proceso
📥 Ejemplo de respuesta
🔄 Estado del documento ( status )
`status`
🔄 Estado del participante ( status )
`status`
⚠️ Respuestas de error