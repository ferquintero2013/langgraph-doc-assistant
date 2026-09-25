# api/manager/documents/upload

> Fuente: https://docs.auco.ai/api/manager/documents/upload

`/document/upload`
`prk _`
Este servicio permite iniciar un proceso para solicitar anexos para firma o simplemente anexos sin firma. Cada anexo puede configurarse como obligatorio u opcional.
Si deseas incluir un proceso de firma, puedes enviar directamente un documento PDF en formato base64 , si deseas que la firma y solicitud de anexos hagan parte de una plantilla , ten en cuenta que este flujo no puede configurarse directamente mediante el endpoint ; debes realizar una solicitud a nuestro equipo de soporte.
Antes de integrar este endopint puede necesitar ver cómo definir posiciones de firma y configuraciones de validación de identidad .

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; email | String requerido | Correo electrónico del creador del proceso. ;; code | String opcional | Código de un documento previamente puesto en edición. Al enviarlo, en vez de crear un proceso nuevo se sobreescribe ese, conservando su código. Reenvía el payload completo: lo que omitas se borra. Ver más ;; document | String condicional | Si quieres crear el proceso por medio de una plantilla, debes enviar el id de dicha plantilla en este campo. Para ver y obtener plantillas accede a esta documentación. ;; name | String requerido | Nombre del proceso del documento a firmar, solo si el proceso de adjuntos incluye firma de documento. ;; message | String condicional | Mensaje que llegará en el cuerpo del correo notificando a los firmantes u aprobadores del documento. Requerido cuando algún participante es notificado por correo electrónico. ;; subject | String condicional | Asunto con el que será enviado el correo de notificación a los firmantes u aprobadores. Requerido cuando algún participante es notificado por correo electrónico. ;; file | String condicional | En caso de querer cargar el documento en la misma petición, en éste parámetro se envía el archivo PDF en Base64. (Sólo para archivos pequeños) ;; compress | Boolean condicional | Si el archivo PDF que quieres cargar es demasiado grande , se recomienda no enviar el parámetro file , en su lugar, se debe usar compress: true , de esta forma el servicio retorna una url firmada para cargar el archivo PDF en formato binario mediante una petición de tipo PUT. ;; folder | String condicional | Si quieres guardar este proceso en una carpeta específica, en este parámetro debes ingresar el path de dicha carpeta; ten en cuenta que la carpeta debe existir y pertenecer al creador del proceso. ;; remember | Number condicional | Parámetro que habilita recordatorios automáticos con el lapso de tiempo (horas) entre cada notificación. ;; expiredDate | Date opcional | Fecha de expiración del documento. Esta debe ser mayor a 3 días de la fecha de creación del proceso y se envia en formato Date JSON. ;; camera | Boolean opcional | Este parámetro indica si es obligatoria la validación con foto , por defecto va en false . ;; otpCode | Boolean opcional | Este parámetro indica si es obligatorio la validación por código OTP , por defecto va en false . ;; options | Object opcional | En este parámetro se indican las especificaciones de la validación de identidad. Ver más ;; notification | Boolean opcional | Define si Auco notifica a los participantes una vez creado el proceso. Por defecto es true . Es el valor por defecto de todos los firmantes; cada uno puede sobreescribirlo con signProfile[x].notification . ;; targetWebhooks | Array[String] opcional | Si tienes varios webhooks, puedes enviar el nombre del webhook al que quieres que se notifiquen las actualizaciones de este proceso. ;; tags | Array[String] opcional | Si deseas clasificar procesos con tags, puedes enviar los nombres de los tags a los que quieres relacionar el proceso (Deben existir). ;; custom | Object opcional | Objeto libre para enviar parámetros propios del integrador (por ejemplo, identificadores internos o metadatos). Auco lo almacena tal cual y lo reenvía en las notificaciones de webhook y en la respuesta del GET /document , sin interpretarlo ni validar su contenido. ;; readers | Array opcional | Este parámetro es una lista de objetos que define los participantes que no hacen parte del proceso de firma, pero que se desea que puedan observar cada fase del proceso de firma. ;; readers[x].name | String requerido | nombre del lector. ;; readers[x].email | String requerido | correo del lector. ;; signProfile | Array requerido | Este campo es una lista de objetos, donde se encuentra la información de cada firmante o aprobador para su notificación y firma. ;; signProfile[x].name | String requerido | nombre del firmante. ;; signProfile[x].email | String requerido | correo del firmante. ;; signProfile[x].phone | String requerido | número de teléfono del firmante. ;; signProfile[x].role | String condicional | Este parámetro define el role del participante, puede ser 'APPROVER' o 'SIGNER' . ;; signProfile[x].order | String condicional | Este parámetro define el orden en que se realizará el proceso de notificación para firma o aprobación. ;; signProfile[x].label | Boolean(true) | String condicional | Parámetro que indica si se realizará el posicionamiento de firmas por medio de labels en el pdf. ;; signProfile[x].position | Array condicional | En este parámetro se envían las posiciones de firma de este firmante en cada página. Las posiciones de firma pueden estar previamente cargadas en plantillas, obtenga mas informacion en . ;; signProfile[x].type | String condicional | Nombre con el que se identifica el tipo de firmante en caso de estar pre guardadas en una plantilla, por ejemplo: 'codeudor' . ;; signProfile[x].options | Object opcional | Permite definir validaciones personalizadas para un firmante específico. Si se desea aplicar validaciones de forma individual por firmante, Ver más . ;; signProfile[x].camera | Boolean opcional | Si se desea tener validaciones individuales por firmante y se requiere validación con foto, se debe enviar este parametro en true por defecto es false . ;; signProfile[x].otpCode | Boolean opcional | Si se desea tener validaciones individuales por firmante y se requiere validación con otp, se debe enviar este parametro en true por defecto es false . ;; signProfile[x].notification | Boolean opcional | Sobreescribe el notification global para este firmante, en cualquier dirección: false lo silencia aunque el global esté en true , y true hace que Auco lo notifique aunque el global esté en false . Los firmantes silenciados reciben id en la respuesta.

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.
Recuerda que los correos electrónticos y números de teléfonos entre firmantes no se deben repetir .
Los lectores van a recibir notificaciones por cada actualización en el proceso de firma.

## Proceso de firma con recordatorios automáticos (PDF Base64) ​
En este caso, los recordatorios se enviarán cada 3 horas.
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/upload' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "name" : "Documento de prueba" , "subject" : "prueba auco" , "message" : "prueba auco" , "remember" : 3 , "email" : "example@auco.ai" , "signProfile" : [ { "name" : "Jhon Firma" , "email" : "example@auco.ai" , "label" : true } ] , "readers" : [ { "email" : "example2@auco.ai" , "name" : "Frimante 1" } ] , "file" : Base64 } '`
import requests import json url = "https://api.auco.ai/v1.5/ext/document/upload" payload = json . dumps ( { "name" : "Documento de prueba" , "subject" : "prueba auco" , "message" : "prueba auco" , "remember" : 3 , "email" : "example@auco.ai" , "signProfile" : [ { "name" : "Jhon Firma" , "email" : "example@auco.ai" , "label" : True } ] , "readers" : [ { "email" : "example2@auco.ai" , "name" : "Frimante 1" } ] , "file" : Base64 } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { name : 'Documento de prueba' , subject : 'prueba auco' , message : 'prueba auco' , remember : 3 , email : 'example@auco.ai' , signProfile : [ { name : 'Jhon Firma' , email : 'example@auco.ai' , label : true , } , ] , readers : [ { email : 'eyvasquezt30@gmail.com' , name : 'Frimante 1' , } , ] , file : Base64 , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/upload' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## Firma de documento con validaciones individuales (compress - PDF binario) ​
curl
Python
Node.js
curl -- location 'https://api.auco.ai/v1.5/ext/document/upload' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "name" : "Prueba de Anexos Compress y validaciones individuales" , "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "signProfile" : [ { "type" : "firmante1" , "name" : "Nombre Firmante 1" , "email" : "example @auco.ai" , "camera" : true , "otpCode" : true , "options" : { "camera" : "identification" , "whatsapp" : true , "otpCode" : "email" } , "phone" : "+573000000000" , } , { "type" : "firmante2" , "name" : "Nombre Firmante 2" , "email" : "example2@auco.ai" , "phone" : "+573000000000" , "otpCode" : true , "options" : { "otpCode" : "email" } , } ] , "compress" : true } '
import requests import json url = "https://api.auco.ai/v1.5/ext/document/upload" payload = json . dumps ( { "name" : "Prueba de Anexos Compress y validaciones individuales" , "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "signProfile" : [ { "type" : "firmante1" , "name" : "Nombre Firmante 1" , "email" : "example @auco.ai" , "camera" : True , "otpCode" : True , "options" : { "camera" : "identification" , "whatsapp" : True , "otpCode" : "email" } , "phone" : "+573000000000" , } , { "type" : "firmante2" , "name" : "Nombre Firmante 2" , "email" : "example2@auco.ai" , "phone" : "+573000000000" , "otpCode" : True , "options" : { "otpCode" : "email" } } ] , "compress" : True } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { name : 'Prueba de Anexos Compress y validaciones individuales' , email : 'owner@auco.ai' , message : 'Cargar adjuntos de prueba' , subject : 'Solicitud de adjuntos' , signProfile : [ { type : 'firmante1' , name : 'Nombre Firmante 1' , email : 'example @auco.ai' , camera : true , otpCode : true , options : { camera : 'identification' , whatsapp : true , otpCode : 'email' , } , phone : '+573000000000' , files : [ { name : 'cedula de ciudadanía' , } , { name : 'hoja de vida' , } , { name : 'pasaporte' , optional : true , } , ] , } , { type : 'firmante2' , name : 'Nombre Firmante 2' , email : 'example2@auco.ai' , phone : '+573000000000' , otpCode : true , options : { otpCode : 'whatsapp' , } , } , ] , compress : true , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/upload' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## 📥 Ejemplos de respuesta ​

## 🔹 Modo normal (sin compress o compress: false ) ​
`compress`
`compress: false`
`{ "document" : "ABCDEF1234" }`
PARAMETROS: Campo | Tipo | Descripción ;; document | String | Código único del documento creado.

## 🔸 Modo compress ( compress: true ) ​
`compress: true`
La URL pre-firmada proporcionada en la respuesta es de un solo uso y estará disponible únicamente durante 300 segundos (5 minutos) .
Debe utilizarse para cargar el documento PDF en formato binario mediante una solicitud HTTP PUT .
`{ "document" : "ABCDEF1234" , "url" : "https://s3.amazonaws.com/...signed-url..." }`
PARAMETROS: Campo | Tipo | Descripción ;; document | String | Código único del documento creado. ;; url | String | URL pre-firmada de S3 para subir el PDF (expira en 300s).

## 🔹 Firmantes que Auco no notifica ​
La respuesta incluye signProfile cuando algún firmante queda silenciado, es decir, cuando su notification efectivo es false : el suyo si lo trae, y si no, el global. Cada firmante silenciado trae un id con el que el integrador lo lleva a firmar por su cuenta. Los que Auco sí notifica aparecen sin id : su acceso se genera al notificarlos.
`signProfile`
`notification`
`false`
`{ "document" : "ABCDEF1234" , "signProfile" : [ { "id" : "abc123" , "name" : "Juan" , "email" : "juan@email.com" , "phone" : "+57300..." } ] }`
PARAMETROS: Campo | Tipo | Descripción ;; document | String | Código único del documento creado. ;; signProfile | Array | Lista de firmantes del proceso. ;; signProfile[x].id | String | Identificador único del firmante. ;; signProfile[x].name | String | Nombre del firmante. ;; signProfile[x].email | String | Correo electrónico del firmante. ;; signProfile[x].phone | String | Número de teléfono del firmante.
Este campo también se incluye en modo compress junto con la url .
`url`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, o alguna de las validaciones no coinciden con las condiciones de aplicabilidad ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación
🧪 Ejemplos de uso Proceso de firma con recordatorios automáticos (PDF Base64) Firma de documento con validaciones individuales (compress - PDF binario)
Proceso de firma con recordatorios automáticos (PDF Base64)
Firma de documento con validaciones individuales (compress - PDF binario)
📥 Ejemplos de respuesta 🔹 Modo normal (sin compress o compress: false ) 🔸 Modo compress ( compress: true ) 🔹 Firmantes que Auco no notifica
🔹 Modo normal (sin compress o compress: false )
`compress`
`compress: false`
🔸 Modo compress ( compress: true )
`compress: true`
🔹 Firmantes que Auco no notifica
⚠️ Respuestas de error