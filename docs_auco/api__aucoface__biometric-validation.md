# api/aucoface/biometric-validation

> Fuente: https://docs.auco.ai/api/aucoface/biometric-validation

`/veriface/validate`
`prk _`
Servicio para obtener la similitud entre un documento de identidad y la fotografia de la persona mediante algoritmos de IA, validando la autenticidad de las fotos.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de consulta ​
PARAMETROS: Nombre | Descripción ;; country String | Obligatorio. País de la persona a validar. Consulta la lista de documentos y países ;; type String | Obligatorio. Tipo de documento de la persona a validar. Consulta la lista de documentos y países ;; identification String | Obligatorio. Número de identificación de la persona a consultar. ;; documentImage String | Obligatorio. Imagen del documento en base64 o la URL pública para acceder a la imagen. La imagen debe estar en formato JPEG o PNG. ;; photo String | Obligatorio. Imagen del rostro de la persona en base64 o la URL pública para acceder a la imagen. La imagen debe estar en formato JPEG o PNG.

## 🧪 Ejemplos de uso ​
Curl
Python
Node.js
`curl -X POST '{{api_auco}}/veriface/validate' \ -H 'Authorization: {{private_key}}' \ -d '{ "country": "CO", "type": "CC", "identification": "1001001010", "photo": "https://url.com/photo.jpg", "documentImage": "https://url.com/document.jpg" }'`
`import requests response = requests . post ( '{{api_auco}}/veriface/validate' , headers = { 'Authorization' : '{{private_key}}' } , json = { "country" : "CO" , "type" : "CC" , "identification" : "1001001010" , "photo" : "https://url.com/photo.jpg" , "documentImage" : "https://url.com/document.jpg" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . post ( '{{api_auco}}/veriface/validate' , { country : "CO" , type : "CC" , identification : "1001001010" , photo : 'https://url.com/photo.jpg' , documentImage : 'https://url.com/document.jpg' } , { headers : { Authorization : '{{private_key}}' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​
Validación exitosa.
Validación fallida.
{ "error" : false , "similarity" : 89.46871185302734 , "code" : "JPJD42IDWP3Z6RXA" , "identificationCard" : { "error" : false , "isFront" : true , "data" : { "bloodGroup" : "O+" , "dateOfBirth" : "1990-01-01" , "dateOfExpiry" : "2030-01-01" , "firstIssueDate" : "01 SEPT 2000 BOGOTÁ D.C. " , "fullName" : "PEREZ PEREZ JUAN ALBERTO" , "givenNames" : "JUAN ALBERTO" , "height" : "170 cm" , "issuingStateName" : "Colombia" , "nationality" : "Colombia" , "nationalityCode" : "COL" , "personalNumber" : "1001001010" , "placeOfBirth" : "BOGOTÁ D.C. (CUNDINAMARCA)" , "sex" : "M" , "surname" : "PEREZ PEREZ" , "documentType" : "Id Card" , "name" : "JUAN ALBERTO PEREZ PEREZ" } } }
`{ "error" : true , "similarity" : 49.4231344 , "code" : "JPJD42IDWP3Z6RXA" , "identificationCard" : { "error" : true , "message" : "DOCUMENT_FAKE" , "isFront" : false , "data" : { } } }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros como photo o documentImage . Formato incorrecto de imagen. ;; 401 | Autenticación inválida o ausente.
Autenticación
Parámetros de consulta
🧪 Ejemplos de uso
📥 Ejemplos de respuesta
⚠️ Respuestas de error