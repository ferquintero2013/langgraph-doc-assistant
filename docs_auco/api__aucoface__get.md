# api/aucoface/get

> Fuente: https://docs.auco.ai/api/aucoface/get

`/veriface`
`puk _`
Servicio para consultar el estado y resultados de un proceso AucoFace previamente creado.

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Descripción ;; code String | Obligatorio. Código del proceso AucoFace a consultar. Debe tener exactamente 16 caracteres. Este código se obtiene al crear el proceso mediante el endpoint /veriface .

## Estructura de la respuesta ​
La respuesta contiene información del proceso AucoFace organizada en diferentes secciones:

## Campos principales del proceso ​
PARAMETROS: Campo | Tipo | Descripción ;; email | String | Email del creador del proceso ;; createdAt | String | Fecha de creación del proceso en formato Date JSON ;; platform | String | Plataforma utilizada: whatsapp , web ;; status | String | Estado actual del proceso ver estados del proceso ;; emailValidated | String | Email de quien aprobó o rechazó la validación manual ;; name | String | Nombre completo de la persona a validar ;; userEmail | String | Email de la persona a validar ;; phone | String | Número de teléfono de la persona a validar con indicativo de país ;; country | String | País de la persona a validar. Consulta la lista de documentos y países ;; identificationType | String | Tipo de documento de la persona a validar. Consulta la lista de documentos y países ;; identificationNumber | String | Número de documento de identidad de la persona a validar ;; ocrData | Object | Datos extraídos del documento mediante OCR. Consulta Datos OCR para ver algunos datos que se pueden obtener. ;; attempts | Array | Lista de intentos de validación realizados ;; custom | Object | Información adicional que se agregó en la creación del proceso ;; hash | String | Código de autenticidad y seguridad del proceso. Solo se incluye cuando el proceso ha finalizado y permite verificar la integridad del mismo. ;; validationTypes | Array<String> | Tipos de validación solicitados al crear el proceso (solo aplica a procesos creados con platform: web ).

## Estados del proceso ​
PARAMETROS: Estado | Descripción ;; INPROGRESS | Proceso en curso, el usuario está realizando la validación ;; BLOCKED | Usuario excedió el máximo de intentos, requiere validación manual en la plataforma ;; APPROVED | Validación completada exitosamente, documentos y biometría válidos ;; INVALIDATED | Proceso completado, pero la validación no fue exitosa ;; EXPIRED | Proceso expirado sin completarse en el tiempo límite

## Información de intentos (Array attempts ) ​
`attempts`
Cada intento puede contener toda o parte de la siguiente información:
PARAMETROS: Campo | Descripción ;; identificationCardFront | URL temporal de la imagen frontal del documento ;; identificationCardBack | URL temporal de la imagen posterior del documento ;; photo | URL temporal de la fotografía del rostro ;; similarity | Porcentaje de similitud biométrica (0-100) ;; identificationCardData | Datos extraídos del documento mediante OCR ;; date | Timestamp del intento ;; successful | Boolean indicando si el intento fue exitoso ;; errorMessages | Array de errores en caso de fallo

## Datos OCR ( ocrData ) ​
`ocrData`
Información extraída del documento de identidad:
Datos personales : fullName , givenNames , surname , documentNumber
`fullName`
`givenNames`
`surname`
`documentNumber`
Información demográfica : dateOfBirth , sex , bloodGroup , height
`dateOfBirth`
`sex`
`bloodGroup`
`height`
Datos del documento : documentType , firstIssueDate , placeOfIssue
`documentType`
`firstIssueDate`
`placeOfIssue`
Ubicación : issuingStateName , placeOfBirth
`issuingStateName`
`placeOfBirth`
Las URLs de las imágenes ( identificationCardFront , identificationCardBack , photo ) son enlaces temporales de AWS S3 con una validez de 5 minutos . Después de este tiempo, será necesario realizar una nueva consulta para obtener URLs actualizadas.
`identificationCardFront`
`identificationCardBack`
`photo`
El campo ocrData está disponible solo cuando fue posible extraer información del documento
`ocrData`
El array attempts puede contener múltiples intentos si el usuario realizó varias validaciones
`attempts`
Los datos OCR pueden variar según el tipo de documento, país y calidad de la imagen

## 🧪 Ejemplos de uso ​
Curl
Python
Node.js
`curl -X GET '{{api_auco}}/veriface?code=VERIFACE_CODE' \ -H 'Authorization: {{public_key}}'`
`import requests response = requests . get ( '{{api_auco}}/veriface' , params = { 'code' : 'VERIFACE_CODE' } , headers = { 'Authorization' : '{{public_key}}' } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . get ( '{{api_auco}}/veriface' , { params : { code : 'VERIFACE_CODE' } , headers : { Authorization : '{{public_key}}' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​
Proceso aprobado.
Proceso en progreso.
Proceso bloqueado.
Proceso invalidado.
{ "email" : "prueba@auco.ai" , "createdAt" : "2025-05-29T14:53:04.074Z" , "platform" : "whatsapp" , "status" : "APPROVED" , "name" : "Juan Pérez" , "userEmail" : "juan.perez@gmail.com" , "phone" : "+573003003030" , "country" : "CO" , "identificationType" : "CC" , "identificationNumber" : "1001001010" , "hash" : "b1946ac92492d2347c6235b4d2611184a1e2e3b9f3a3a0c1e8f3e0e0e0e0e0e0" , "attempts" : [ { "identificationCardFront" : "https://amazon.url/file/signed-url" , "identificationCardBack" : "https://amazon.url/file/signed-url" , "photo" : "https://amazon.url/file/signed-url" , "similarity" : 91.31532287597656 , "identificationCardData" : { "documentNumber" : "1001001010" , "fullName" : "PÉREZ JUAN" , "givenNames" : "JUAN" , "issuingStateName" : "Colombia" , "surname" : "PÉREZ" , "documentType" : "Id Card" , "name" : "JUAN PÉREZ" } , "date" : "2025-05-29T17:16:51.839Z" , "successful" : true } ] , "ocrData" : { "bloodGroup" : "O+" , "dateOfBirth" : "1990-05-15" , "firstIssueDate" : "2015-03-20" , "height" : "175 cm" , "issuingStateName" : "Colombia" , "placeOfBirth" : "BOGOTÁ (CUNDINAMARCA)" , "sex" : "M" , "documentType" : "Id Card" , "placeOfIssue" : "BOGOTÁ" , "documentNumber" : "1001001010" , "fullName" : "PÉREZ JUAN" , "givenNames" : "JUAN" , "surname" : "PÉREZ" , "name" : "JUAN PÉREZ" } }
`{ "email" : "prueba@auco.ai" , "createdAt" : "2025-05-29T14:53:04.074Z" , "platform" : "whatsapp" , "status" : "INPROGRESS" , "name" : "Juan Pérez" , "userEmail" : "juan.perez@gmail.com" , "phone" : "+573003003030" , "country" : "CO" , "identificationType" : "CC" , "identificationNumber" : "1001001010" , "attempts" : [ ] }`
{ "email" : "prueba@auco.ai" , "createdAt" : "2025-05-29T14:53:04.074Z" , "platform" : "whatsapp" , "status" : "BLOCKED" , "emailValidated" : "supervisor@auco.ai" , "name" : "Juan Pérez" , "phone" : "+573003003030" , "country" : "CO" , "identificationType" : "CC" , "identificationNumber" : "1001001010" , "attempts" : [ { "identificationCardFront" : "https://amazon.url/file/signed-url" , "photo" : "https://amazon.url/file/signed-url" , "similarity" : 45.23456789 , "identificationCardData" : { "documentNumber" : "1001001010" , "fullName" : "PÉREZ JUAN" , "documentType" : "Id Card" } , "date" : "2025-05-29T17:15:31.383Z" , "errorMessages" : [ { "key" : "ID_BACK" , "error" : "error_identification_not_document" } ] , "successful" : false } ] }
{ "email" : "prueba@auco.ai" , "createdAt" : "2025-05-29T14:53:04.074Z" , "platform" : "web" , "status" : "INVALIDATED" , "name" : "Juan Pérez" , "phone" : "+573003003030" , "country" : "CO" , "identificationType" : "CC" , "identificationNumber" : "1001001010" , "hash" : "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" , "attempts" : [ { "identificationCardFront" : "https://amazon.url/file/signed-url" , "photo" : "https://amazon.url/file/signed-url" , "similarity" : 32.15432167891234 , "date" : "2025-05-29T17:15:31.383Z" , "errorMessages" : [ { "key" : "ID_BACK" , "error" : "error_identification_not_document" } ] , "successful" : false } ] }

## ⚠️ Respuestas de error ​
PARAMETROS: C ódigo | Descripción ;; 400 | Código de proceso inválido o malformado. ;; 401 | Autenticación inválida o ausente.
Autenticación
Parámetros de consulta
Estructura de la respuesta Campos principales del proceso Estados del proceso Información de intentos (Array attempts ) Datos OCR ( ocrData )
Campos principales del proceso
Estados del proceso
Información de intentos (Array attempts )
`attempts`
Datos OCR ( ocrData )
`ocrData`
🧪 Ejemplos de uso
📥 Ejemplos de respuesta
⚠️ Respuestas de error