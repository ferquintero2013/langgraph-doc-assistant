# api/aucoface/document-validation

> Fuente: https://docs.auco.ai/api/aucoface/document-validation

`/veriface/check`
`prk _`
Servicio para validar un documento de identidad, determinar si pertenece al número proporcionado, si este es falsificado y extracción de datos mediante OCR.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Descripción ;; country String | Obligatorio. País de la persona a validar. Consulta la lista de documentos y países ;; type String | Obligatorio. Tipo de documento de la persona a validar. Consulta la lista de documentos y países ;; identification String | Obligatorio. Número de identificación de la persona a consultar. ;; image String | Obligatorio. Imagen del documento en base64 o la URL pública para acceder a la imagen. La imagen debe estar en formato JPEG o PNG.

## 🧪 Ejemplos de uso ​
Curl
Python
Node.js
`curl -X POST '{{api_auco}}/veriface/check' \ -H 'Authorization: {{private_key}}' \ -d '{ "country": "CO", "type": "CC", "identification": "1001001010", "image": "https://url.com/document.jpg" }'`
`import requests response = requests . post ( '{{api_auco}}/veriface/check' , headers = { 'Authorization' : '{{private_key}}' } , json = { "country" : "CO" , "type" : "CC" , "identification" : "1001001010" , "image" : "https://url.com/document.jpg" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . post ( '{{api_auco}}/veriface/check' , { country : "CO" , type : "CC" , identification : "1001001010" , image : "https://url.com/document.jpg" } , { headers : { Authorization : '{{private_key}}' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​
Validación exitosa.
Validación fallida.
`{ "code" : "JPJD42IDWP3Z6RXA" , "error" : false , "isFront" : true , "data" : { "bloodGroup" : "O+" , "dateOfBirth" : "1990-01-01" , "dateOfExpiry" : "2030-01-01" , "firstIssueDate" : "01 SEPT 2000 BOGOTÁ D.C. " , "fullName" : "PEREZ PEREZ JUAN ALBERTO" , "givenNames" : "JUAN ALBERTO" , "height" : "170 cm" , "issuingStateName" : "Colombia" , "nationality" : "Colombia" , "nationalityCode" : "COL" , "personalNumber" : "1001001010" , "placeOfBirth" : "BOGOTÁ D.C. (CUNDINAMARCA)" , "sex" : "M" , "surname" : "PEREZ PEREZ" , "documentType" : "Id Card" , "name" : "JUAN ALBERTO PEREZ PEREZ" } }`
`{ "code" : "JPJD42IDWP3Z6RXA" , "error" : true , "message" : "DOCUMENT_FAKE" , "isFront" : false , "data" : { } }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros como country , type , identification o image . Formato incorrecto de imagen. ;; 401 | Autenticación inválida o ausente.
Autenticación
Parámetros de consulta
🧪 Ejemplos de uso
📥 Ejemplos de respuesta
⚠️ Respuestas de error