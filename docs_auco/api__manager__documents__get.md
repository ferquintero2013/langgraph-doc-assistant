# api/manager/documents/get

> Fuente: https://docs.auco.ai/api/manager/documents/get

`/document`
`puk _`
Este servicio permite consultar sus procesos de firma, plantillas automatizadas o tus plantillas automatizadas en Auco.

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String opcional | Código de documento asociado al proceso. Obligatorio si no se incluye package . ;; image | String opcional | Si es "true" , incluye las imágenes de identificación y foto de los firmantes en la respuesta.
⚠️ Si no envías el atributo code , recibirás la lista de plantillas automatizadas .
`code`
Este mismo endpoint servirá para obtener paquete de documentos, ver mas en consultar paquetes de documentos

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## 🔹 Obtener información general del proceso ​
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/document?code=CODEDOCUM' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/document" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "code" : "CODEDOCUM" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/document' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { code : 'CODEDOCUM' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 🔹 Obtener proceso con imágenes de firmantes ​
Al incluir el parámetro image=true , la respuesta incluirá las imágenes de identificación y foto de los firmantes cuando estén disponibles.
`image=true`
curl
Python
Node.js
`curl --location 'https://api.auco.ai/v1.5/ext/document?code=CODEDOCUM&image=true' \ --header 'Authorization: puk_tuClavePublica'`
`import requests response = requests . get ( "https://api.auco.ai/v1.5/ext/document" , headers = { "Authorization" : "puk_tuClavePublica" } , params = { "code" : "CODEDOCUM" , "image" : "true" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( 'https://api.auco.ai/v1.5/ext/document' , { headers : { Authorization : 'puk_tuClavePublica' } , params : { code : 'CODEDOCUM' , image : 'true' } , } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplo de respuesta ​
{ "url" : "https://signed_url" , "name" : "prueba firma garabato" , "code" : "CODEDOCUM" , "status" : "CREATED" , "data" : { "code" : "CODEDOCUM" , "name" : "prueba firma garabato" , "camera" : false , "otpCode" : false , "signFinish" : false , "signProfile" : [ { "name" : "Firmante de prueba" , "email" : "example@auco.ai" , "id" : "G8" , "status" : "NOTIFICATION" } ] , "createdAt" : "2025-01-02T16:54:00.297Z" , "updatedAt" : "2025-01-02T16:54:03.105Z" } , "signProfile" : [ { "name" : "Mauricio Lopez" , "email" : "example@auco.ai" , "id" : "G8" , "status" : "NOTIFICATION" } ] , "custom" : { "externalId" : "ORDER-123" , "source" : "crm" } }
El campo custom sólo aparece si fue enviado al crear el proceso (ver POST /document/upload ). Contiene exactamente los datos que el integrador envió, sin ninguna transformación por parte de Auco.
`custom`

## 🔄 Estado del documento ( status ) ​
`status`
PARAMETROS: Estado | Descripción ;; CREATED | Cuando el proceso ha sido creado. ;; REJECTED | Proceso rechazado. ;; EXPIRED | Proceso expirado, solo si al momento de crearlo se asigna fecha de expiración. ;; FINISH | Proceso firma o aprobado por todas las partes.

## 🔄 Estado del participante ( status ) ​
`status`
PARAMETROS: Estado | Descripción ;; NOTIFICATION | El participante ha sido notificado para firma. ;; REJECT | El participante ha rechazado la firma o aprobación del proceso. ;; FINISH | El participante ha firmado o aprobado el proceso. ;; BLOCK | El participante ha excedido los intentos fallidos al momento de firmar o aprobar. ;; PENDING | El participante no ha sido notificado, generalmente se debe a un proceso secuencial.

## 🖼️ Imágenes de firmantes ​
Cuando se envía el parámetro image=true , cada objeto en signProfile puede incluir los siguientes campos de imagen:
`image=true`
`signProfile`
PARAMETROS: Campo | Descripción ;; identificationCard | Foto frontal del documento de identidad ;; identificationCardBack | Foto trasera del documento de identidad ;; photo | Selfie/foto del firmante

## Formato de imagen ​
Cada campo de imagen tiene la siguiente estructura:
`{ "type" : "base64 | presigned" , "data" : "..." }`
PARAMETROS: Tipo | Contenido de data | Descripción ;; base64 | data:image/jpeg;base64,... | La imagen está codificada en base64 ;; presigned | URL de S3 (ej: https://s3... ) | URL firmada válida por 5 minutos

## Ejemplo de respuesta con imágenes ​
`{ "url" : "https://signed_url" , "name" : "Contrato de servicios" , "code" : "CODEDOCUM" , "status" : "FINISH" , "signProfile" : [ { "name" : "Juan Pérez" , "email" : "juan@ejemplo.com" , "id" : "G8" , "status" : "FINISH" , "identificationCard" : { "type" : "presigned" , "data" : "https://s3.amazonaws.com/bucket/..." } , "identificationCardBack" : { "type" : "presigned" , "data" : "https://s3.amazonaws.com/bucket/..." } , "photo" : { "type" : "base64" , "data" : "data:image/jpeg;base64,/9j/4AAQSkZJRg..." } } ] }`
Las URLs presignadas tienen una validez de 5 minutos . Asegúrate de descargar las imágenes antes de que expiren.

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | proceso no encontrado ( DOCUMENT_NOT_FOUND ) ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de consulta
🧪 Ejemplos de uso 🔹 Obtener información general del proceso 🔹 Obtener proceso con imágenes de firmantes
🔹 Obtener información general del proceso
🔹 Obtener proceso con imágenes de firmantes
📥 Ejemplo de respuesta
🔄 Estado del documento ( status )
`status`
🔄 Estado del participante ( status )
`status`
🖼️ Imágenes de firmantes Formato de imagen Ejemplo de respuesta con imágenes
Formato de imagen
Ejemplo de respuesta con imágenes
⚠️ Respuestas de error