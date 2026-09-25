# api/manager/attachments/create

> Fuente: https://docs.auco.ai/api/manager/attachments/create

`/package/upload`
`prk _`
Este servicio permite iniciar un proceso para solicitar anexos para firma o simplemente anexos sin firma. Cada anexo puede configurarse como obligatorio u opcional.
Si deseas incluir un proceso de firma, puedes cargar el documento PDF en la misma petición: en Base64 con file , o en binario (vía URL firmada con PUT ) usando compress . Si quieres que la firma y la solicitud de anexos formen parte de una plantilla de flujo preguardada , esta debe configurarse previamente con nuestro equipo de soporte; una vez creada, la referencias por su id en el campo document .
`file`
`PUT`
`compress`
`document`
Antes de integrar este endopint puede necesitar ver cómo definir posiciones de firma y configuraciones de validación de identidad .

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
Los campos file , compress y document son mutuamente excluyentes : puedes enviar como máximo uno . Si no envías ninguno, se crea un proceso de solo recolección de anexos sin firma (no se genera ningún documento) y en ese caso name tampoco es necesario.
`file`
`compress`
`document`
`name`
Cada objeto de signProfile debe incluir exactamente uno de type , label o position (mutuamente excluyentes y uno obligatorio), incluso en procesos de solo anexos sin firma.
`signProfile`
`type`
`label`
`position`
PARAMETROS: Nombre | Tipo | Descripción ;; email | String requerido | Correo electrónico del creador del proceso. ;; document | String condicional | Id de una plantilla de flujo preguardada (creada previamente con el equipo de soporte) con la que se desea crear el proceso. ;; name | String condicional | Nombre del documento a firmar. Solo es obligatorio si el proceso incluye un documento ( file , compress o document ). En un proceso de solo anexos sin firma no es necesario enviarlo. ;; packageName | String requerido | Nombre con que será creada la carpeta contenedora de los archivos adjuntos y el documento a firmar (Si contiene). ;; message | String opcional | Mensaje que llegará en el cuerpo del correo notificando a los firmantes u aprobadores del documento. Si no se envía, Auco usa un valor por defecto. ;; subject | String opcional | Asunto con el que será enviado el correo de notificación a los firmantes u aprobadores. Si no se envía, Auco usa un valor por defecto. ;; file | String condicional | En caso de querer cargar el documento en la misma petición, en éste parámetro se envía el archivo PDF en Base64. (Sólo para archivos pequeños) ;; compress | Boolean condicional | Si el archivo PDF que quieres cargar es demasiado grande , se recomienda no enviar el parámetro file , en su lugar, se debe usar compress: true , de esta forma el servicio retorna una url firmada para cargar el archivo PDF en formato binario mediante una petición de tipo PUT. ;; folder | String condicional | Si quieres guardar este proceso en una carpeta específica, en este parámetro debes ingresar el path de dicha carpeta; ten en cuenta que la carpeta debe existir y pertenecer al creador del proceso. ;; remember | Number condicional | Parámetro que habilita recordatorios automáticos con el lapso de tiempo (horas) entre cada notificación. Debe ser múltiplo de 3 ;; expiredDate | Date opcional | Fecha de expiración del documento. Esta debe ser mayor a 3 días de la fecha de creación del proceso y se envia en formato Date JSON. ;; camera | Boolean opcional | Este parámetro indica si es obligatoria la validación con foto , por defecto va en false . ;; otpCode | Boolean opcional | Este parámetro indica si es obligatorio la validación por código OTP , por defecto va en false . ;; options | Object opcional | En este parámetro se indican las especificaciones de la validación de identidad. ;; signProfile | Array requerido | Este campo es una lista de objetos, donde se encuentra la información de cada firmante o aprobador para su notificación y firma. ;; signProfile[x].name | String requerido | nombre del usuario anexador. ;; signProfile[x].email | String requerido | correo del usuario anexador. ;; signProfile[x].phone | String requerido | número de teléfono del usuario anexador. ;; signProfile[x].role | String condicional | Este parámetro define el role del participante, puede ser 'APPROVER' o 'SIGNER' . ;; signProfile[x].order | String condicional | Este parámetro define el orden en que se realizará el proceso de notificación para firma o aprobación. ;; signProfile[x].label | Boolean condicional | Parámetro que indica si se realizará el posicionamiento de firmas por medio de labels en el pdf. ;; signProfile[x].position | Array condicional | En este parámetro se envían las posiciones de firma de este firmante en cada página. Las posiciones de firma pueden estar previamente cargadas en plantillas, obtenga mas informacion en . ;; signProfile[x].type | String condicional | Nombre con el que se identifica el tipo de firmante en caso de estar pre guardadas en una plantilla, por ejemplo: 'codeudor' . ;; signProfile[x].options | Object opcional | Permite definir validaciones personalizadas para un firmante específico. Si se desea aplicar validaciones de forma individual por firmante, este parámetro acepta los mismos campos definidos en options a nivel global. Es posible combinar validaciones globales e individuales, aplicando las generales por defecto y las individuales donde se requiera un tratamiento particular. ;; signProfile[x].camera | Boolean opcional | Si se desea tener validaciones individuales por firmante y se requiere validación con foto, se debe enviar este parametro en true por defecto es false . ;; signProfile[x].otpCode | Boolean opcional | Si se desea tener validaciones individuales por firmante y se requiere validación con otp, se debe enviar este parametro en true por defecto es false . ;; signProfile[x].files | Array requerido | En este parámetro se especifica la lista de archivos adjuntos que se le solicitará al firmante. ;; signProfile[x].files[x].name | String requerido | Nombre del archivo adjunto. ;; signProfile[x].files[x].optional | Boolean opcional | En caso de ser opcional algún archivo adjunto es importante enviar este parámetro en true , por defecto es false .
A diferencia de POST /document/many y POST /document/upload , aquí no se puede apagar la notificación: Auco le escribe a todos los participantes para pedirles sus archivos. Enviar notification en la raíz o dentro de signProfile[x] devuelve un error — el de firmante, SIGNER_NOTIFICATION_NOT_SUPPORTED .
`POST /document/many`
`POST /document/upload`
`notification`
`signProfile[x]`
`SIGNER_NOTIFICATION_NOT_SUPPORTED`

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.

## Solo recolección de anexos (sin documento ni firma) ​
No se envía file , compress , document ni name : el proceso solo solicita anexos a los participantes.
`file`
`compress`
`document`
`name`
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/package/upload' \ -- header 'Authorization: prk_prk_tuLlavePrivada' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "packageName" : "Adjuntos sin firma" , "signProfile" : [ { "type" : "anexador1" , "name" : "Nombre Anexador 1" , "email" : "example@auco.ai" , "phone" : "+573000000000" , "files" : [ { "name" : "cedula de ciudadanía" } , { "name" : "hoja de vida" , "optional" : true } ] } ] } '`
import requests import json url = "https://api.auco.ai/v1.5/ext/package/upload" payload = json . dumps ( { "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "packageName" : "Adjuntos sin firma" , "signProfile" : [ { "type" : "anexador1" , "name" : "Nombre Anexador 1" , "email" : "example@auco.ai" , "phone" : "+573000000000" , "files" : [ { "name" : "cedula de ciudadanía" } , { "name" : "hoja de vida" , "optional" : True } ] } ] } ) headers = { 'Authorization' : 'prk_prk_tuLlavePrivada' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { email : 'owner@auco.ai' , message : 'Cargar adjuntos de prueba' , subject : 'Solicitud de adjuntos' , packageName : 'Adjuntos sin firma' , signProfile : [ { type : 'anexador1' , name : 'Nombre Anexador 1' , email : 'example@auco.ai' , phone : '+573000000000' , files : [ { name : 'cedula de ciudadanía' , } , { name : 'hoja de vida' , optional : true , } , ] , } , ] , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/package/upload' , headers : { Authorization : 'prk_tuLlavePrivada' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## Anexos opcionales con firma de documento (PDF Base64) ​
curl
Python
Node.js
curl -- location 'https://api.auco.ai/v1.5/ext/package/upload' \ -- header 'Authorization: prk_prk_tuLlavePrivada' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "name" : "Contratación de prueba upload 1" , "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "packageName" : "Adjuntos api prueba" , "file" : Base64 , "signProfile" : [ { "name" : "Nombre Firmante 1" , "email" : "example@auco.ai" , "phone" : "+573000000000" , "position" : [ { "page" : 1 , "x" : 0.5854166461564629 , "y" : 0.8034861200774693 , "w" : 100 , "h" : 50 } ] , "files" : [ { "name" : "cedula de ciudadanía" } , { "name" : "hoja de vida" } , { "name" : "pasaporte" , "optional" : true } ] } ] , } '
import requests import json url = "https://api.auco.ai/v1.5/ext/package/upload" payload = json . dumps ( { "name" : "Contratación de prueba upload 1" , "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "packageName" : "Adjuntos api prueba" , "file" : Base64 , "signProfile" : [ { "name" : "Nombre Firmante 1" , "email" : "example@auco.ai" , "phone" : "+573000000000" , "position" : [ { "page" : 1 , "x" : 0.5854166461564629 , "y" : 0.8034861200774693 , "w" : 100 , "h" : 50 } ] , "files" : [ { "name" : "cedula de ciudadanía" } , { "name" : "hoja de vida" } , { "name" : "pasaporte" , "optional" : True } ] } ] , } ) headers = { 'Authorization' : 'prk_prk_tuLlavePrivada' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { name : 'Contratación de prueba upload 1' , email : 'owner@auco.ai' , message : 'Cargar adjuntos de prueba' , subject : 'Solicitud de adjuntos' , packageName : 'Adjuntos api prueba' , file : Base64 , signProfile : [ { name : 'Nombre Firmante 1' , email : 'example@auco.ai' , phone : '+573000000000' , position : [ { page : 1 , x : 0.5854166461564629 , y : 0.8034861200774693 , w : 100 , h : 50 , } , ] , files : [ { name : 'cedula de ciudadanía' , } , { name : 'hoja de vida' , } , { name : 'pasaporte' , optional : true , } , ] , } , ] , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/package/upload' , headers : { Authorization : 'prk_tuLlavePrivada' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## Anexos opcionales con firma de documento (PDF compress y validaciones individuales) ​
curl
Python
Node.js
curl -- location 'https://api.auco.ai/v1.5/ext/package/upload' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "name" : "Prueba de Anexos Compress y validaciones individuales" , "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "packageName" : "Adjuntos api prueba 2" , "signProfile" : [ { "type" : "firmante1" , "name" : "Nombre Firmante 1" , "email" : "example @auco.ai" , "camera" : true , "otpCode" : true , "options" : { "camera" : "identification" , "whatsapp" : true , "otpCode" : "email" } , "phone" : "+573000000000" , "files" : [ { "name" : "cedula de ciudadanía" } , { "name" : "hoja de vida" } , { "name" : "pasaporte" , "optional" : true } ] } , { "type" : "firmante2" , "name" : "Nombre Firmante 2" , "email" : "example2@auco.ai" , "phone" : "+573000000000" , "otpCode" : true , "options" : { "otpCode" : "email" } , "files" : [ { "name" : "certificado" } ] } ] , "compress" : true } '
import requests import json url = "https://api.auco.ai/v1.5/ext/package/upload" payload = json . dumps ( { "name" : "Prueba de Anexos Compress y validaciones individuales" , "email" : "owner@auco.ai" , "message" : "Cargar adjuntos de prueba" , "subject" : "Solicitud de adjuntos" , "packageName" : "Adjuntos api prueba 2" , "signProfile" : [ { "type" : "firmante1" , "name" : "Nombre Firmante 1" , "email" : "example @auco.ai" , "camera" : True , "otpCode" : True , "options" : { "camera" : "identification" , "whatsapp" : True , "otpCode" : "email" } , "phone" : "+573000000000" , "files" : [ { "name" : "cedula de ciudadanía" } , { "name" : "hoja de vida" } , { "name" : "pasaporte" , "optional" : True } ] } , { "type" : "firmante2" , "name" : "Nombre Firmante 2" , "email" : "example2@auco.ai" , "phone" : "+573000000000" , "otpCode" : True , "options" : { "otpCode" : "email" } , "files" : [ { "name" : "certificado" } ] } ] , "compress" : True } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { name : 'Prueba de Anexos Compress y validaciones individuales' , email : 'owner@auco.ai' , message : 'Cargar adjuntos de prueba' , subject : 'Solicitud de adjuntos' , packageName : 'Adjuntos api prueba 2' , signProfile : [ { type : 'firmante1' , name : 'Nombre Firmante 1' , email : 'example @auco.ai' , camera : true , otpCode : true , options : { camera : 'identification' , whatsapp : true , otpCode : 'email' , } , phone : '+573000000000' , files : [ { name : 'cedula de ciudadanía' , } , { name : 'hoja de vida' , } , { name : 'pasaporte' , optional : true , } , ] , } , { type : 'firmante2' , name : 'Nombre Firmante 2' , email : 'example2@auco.ai' , phone : '+573000000000' , otpCode : true , options : { otpCode : 'email' , } , files : [ { name : 'certificado' , } , ] , } , ] , compress : true , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/package/upload' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## 📥 Ejemplos de respuesta ​

## 🔹 Enviando PDF en Base64 en el atributo file ​
`file`
`{ "package" : "PROCESSID" , "code" : "DOCUMENTCODE" }`

## 🔹 Proceso de solo anexos (sin documento) ​
Al no crearse un documento, la respuesta solo incluye el package .
`package`
`{ "package" : "PROCESSID" }`

## 🔸 Enviando el atributo compress ​
`compress`
La URL firmada proporcionada en la respuesta es de un solo uso y estará disponible únicamente durante 5 segundos .
Debe utilizarse para cargar el documento PDF en formato binario mediante una solicitud HTTP PUT .
`{ "package" : "PROCESSID" , "code" : "DOCUMENTCODE" , "url" : "signed_url" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, o alguna de las validaciones no coinciden con las condiciones de aplicabilidad ;; 401 | Autenticación inválida o ausente
Autenticación
Parámetros de creación
🧪 Ejemplos de uso Solo recolección de anexos (sin documento ni firma) Anexos opcionales con firma de documento (PDF Base64) Anexos opcionales con firma de documento (PDF compress y validaciones individuales)
Solo recolección de anexos (sin documento ni firma)
Anexos opcionales con firma de documento (PDF Base64)
Anexos opcionales con firma de documento (PDF compress y validaciones individuales)
📥 Ejemplos de respuesta 🔹 Enviando PDF en Base64 en el atributo file 🔹 Proceso de solo anexos (sin documento) 🔸 Enviando el atributo compress
🔹 Enviando PDF en Base64 en el atributo file
`file`
🔹 Proceso de solo anexos (sin documento)
🔸 Enviando el atributo compress
`compress`
⚠️ Respuestas de error