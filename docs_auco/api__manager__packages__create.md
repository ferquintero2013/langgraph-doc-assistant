# api/manager/packages/create

> Fuente: https://docs.auco.ai/api/manager/packages/create

`/document/many`
`prk _`
Este servicio permite generar paquete de documentos a partir de una plantilla de Auco o de un archivo PDF. Al terminar el proceso, obtendras cada documento con su propio certificado de firma.
Antes de integrar este endopint puede necesitar ver cómo definir posiciones de firma y configuraciones de validación de identidad a nivel de paquete .
El array documents debe contener al menos 2 elementos . Si solo necesita un documento, use el endpoint POST /document/upload .
`documents`

## Pasos para crear un paquete de documento a través de una plantilla automatizada: ​
Consultar plantillas o documentos personalizados disponibles: Debe iniciar consultando los recursos disponibles (plantillas propias o de Auco) para identificar el documento base que desea utilizar.
Obtener el identificador (_id) del documento base: Una vez identificada la plantilla o documento deseado, obtenga su _id para poder continuar con el proceso.
Consultar variables requeridas del documento seleccionado: Utilice el servicio correspondiente para recuperar la lista de variables que necesita completar. Este paso es esencial para construir correctamente la solicitud de creación del documento.
Construir y enviar el request de creación: Con la información de las variables, puede armar el cuerpo de la solicitud (POST) para generar el documento.
Si quieres hacerlo por medio de PDF, no es necesario enviar el archivo en la petición inicial. Al final, se te retornará una URL firmada por cada documento del paquete
A continuación se describen los parámetros necesarios para este servicio, junto con ejemplos y posibles respuestas del sistema.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; email | String requerido | Correo electrónico del creador del proceso. ;; package | String opcional | Identificador de un paquete previamente puesto en edición. Al enviarlo, en vez de crear un paquete nuevo se sobreescribe ese, conservando su identificador. Reenvía el payload completo: lo que omitas se borra. Ver más ;; document | String condicional | ID del documento personalizado o la plantilla Auco Sólo si se desea realizar por medio de plantilla . ;; name | String requerido | Nombre del proceso del documento a firmar, solo si el proceso de adjuntos incluye firma de documento. ;; message | String opcional | Mensaje que llegará en el cuerpo del correo notificando a los firmantes u aprobadores del documento. ;; subject | String opcional | Asunto con el que será enviado el correo de notificación a los firmantes u aprobadores. ;; folder | String condicional | Si quieres guardar este proceso en una carpeta específica, en este parámetro debes ingresar el path de dicha carpeta; ten en cuenta que la carpeta debe existir y pertenecer al creador del proceso. ;; remember | Number condicional | Parámetro que habilita recordatorios automáticos con el lapso de tiempo (horas) entre cada notificación. Debe ser múltiplo de 3 ;; expiredDate | Date opcional | Fecha de expiración del documento. Esta debe ser mayor a 3 días de la fecha de creación del proceso y se envia en formato Date JSON. ;; camera | Boolean opcional | Este parámetro indica si es obligatoria la validación con foto , por defecto va en false . ;; otpCode | Boolean opcional | Este parámetro indica si es obligatorio la validación por código OTP , por defecto va en false . ;; options | Object opcional | En este parámetro se indican las especificaciones de la validación de identidad. Ver más ;; notification | Boolean opcional | Define si Auco notifica a los participantes una vez creado el proceso. Por defecto es true . Es el valor por defecto de todos los firmantes; cada uno puede sobreescribirlo con signProfile[x].notification . Los firmantes que Auco no notifica reciben un id en la respuesta, agrupado por correo entre todos los documentos, para que el integrador los lleve a firmar por su cuenta. ;; readers | Array opcional | Lista de lectores del paquete. Cada lector recibirá notificaciones por cada actualización en el proceso de firma. Los correos de los lectores no pueden coincidir con los de los firmantes. ;; readers[x].name | String requerido | Nombre del lector. ;; readers[x].email | String requerido | Correo del lector. Debe ser diferente al correo de cualquier firmante del paquete. ;; custom | Object opcional | Objeto libre para enviar parámetros propios del integrador (por ejemplo, identificadores internos o metadatos). Auco lo almacena tal cual y lo reenvía en las notificaciones de webhook y en la respuesta del GET /document , sin interpretarlo ni validar su contenido. Aplica al paquete completo. ;; data | Array condicional | En este parámetro se envían todos los datos que necestia la plantilla para generar el documento. Sólo si se desea realizar por medio de plantilla . ;; data[x].key | String requerido | Nombre del parámetro registrado en la plantilla. ;; data[x].value | String requerido | Valor asignado al parámtro. ;; documents * | Array requerido | En este cambo se envía una lista de tipo objeto que contiene cada documento. ;; documents[0].name | String opcional | Nombre del documento dentro del paquete. ;; documents[0].document.signProfile | Array requerido | Este campo es una lista de objetos, donde se encuentra la información de cada firmante o aprobador para su notificación y firma. ;; documents[0].signProfile[x].name | String requerido | nombre del firmante. ;; documents[0].signProfile[x].email | String requerido | Correo del firmante. Es con lo que Auco lo relaciona con cada documento del paquete, así que es obligatorio incluso cuando lo notificas por WhatsApp. Omitirlo devuelve SIGNER_EMAIL_REQUIRED . ;; documents[0].signProfile[x].phone | String opcional | Número de teléfono del firmante, con indicativo del país. Obligatorio si el paquete usa WhatsApp como canal. ;; documents[0].signProfile[x].position | Array condicional | En este parámetro se envían las posiciones de firma de este firmante en cada página. Las posiciones de firma pueden estar previamente cargadas en plantillas, obtenga mas informacion en . ;; documents[0].signProfile[x].type | Array condicional | Nombre con el que se identifica el tipo de firmante en caso de estar pre guardadas en una plantilla, por ejemplo: 'codeudor' . ;; documents[0].signProfile[x].label | Boolean condicional | Parámetro que indica si se realizará el posicionamiento de firmas por medio de labels en el pdf. ;; documents[0].signProfile[x].notification | Boolean opcional | Sobreescribe el notification global para este firmante, en cualquier dirección: false lo silencia aunque el global esté en true , y true hace que Auco lo notifique aunque el global esté en false . Si el mismo correo aparece en varios documentos con valores distintos, gana false . Solo aplica a documentos PDF; en los de plantilla el flag por firmante viene definido en el signatureProfile de la plantilla.
En este servicio la validación de identidad y el canal de firma se configuran una sola vez para todo el paquete , con camera , otpCode y options en la raíz de la petición, y aplican por igual a todos los participantes.
`camera`
`otpCode`
`options`
La creación de paquetes no tiene soporte para validaciones de identidad ni selección de canal individuales por participante . Enviar camera , otpCode u options dentro de signProfile[x] devuelve el error SIGNER_VALIDATIONS_NOT_SUPPORTED . Si necesitas validaciones distintas por participante, crea procesos independientes con POST /document/upload .
`camera`
`otpCode`
`options`
`signProfile[x]`
`SIGNER_VALIDATIONS_NOT_SUPPORTED`
`POST /document/upload`
Todos los participantes de un paquete son notificados al mismo tiempo : no hay turnos ni etapas de aprobación. Enviar role u order dentro de signProfile[x] devuelve el error SIGNER_SEQUENCE_NOT_SUPPORTED .
`role`
`order`
`signProfile[x]`
`SIGNER_SEQUENCE_NOT_SUPPORTED`
Si necesitas que unos firmen antes que otros, o que alguien apruebe antes de que se firme, crea procesos independientes con POST /document/upload , que sí soporta order y role .
`POST /document/upload`
`order`
`role`

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.
Recuerda que los correos electrónticos y números de teléfonos entre firmantes no se deben repetir .
Los lectores van a recibir notificaciones por cada actualización en el proceso de firma.
Formato de fecha: 'DD/MM/AAAA'
`'DD/MM/AAAA'`
Los números de teléfono deben tener el indicativo del país, por ejemplo: +57, +1, +52...
`+57, +1, +52...`

## Paquete de documentos por medio de PDF ​
curl
Python
Node.js
curl -- location 'https://api.auco.ai/v1.5/ext/document/many' \ -- header 'Authorization: prk_e1cd6a01ecdb4b4ea72ec118e33b18de' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "name" : "Prueba paquete 2 documentos" , "email" : "example@auco.ai" , "message" : "Hola a todos, les comparto el paquete de documentos para la firma" , "options" : { "camera" : "identification" , "whatsapp" : true } , "camera" : true , "otpCode" : false , "documents" : [ { "name" : "Documento 1" , "signProfile" : [ { "type" : "solicitante" , "name" : "Firmante 1" , "phone" : "+573000000000" , "email" : "example1@auco.ai" } ] } , { "name" : "Documento 2" , "signProfile" : [ { "type" : "solicitante" , "name" : "Firmante 1" , "phone" : "+573000000000" , "email" : "example2@auco.ai" } ] } ] }
import requests import json url = "https://api.auco.ai/v1.5/ext/document/many" payload = json . dumps ( { "name" : "Paquete de contratos" , "email" : "example@auco.ai" , "message" : "Hola a todos, les comparto el paquete de documentos para la firma" , "options" : { "camera" : "identification" , "whatsapp" : True } , "camera" : True , "otpCode" : False , "documents" : [ { "name" : "Documento 1" , "signProfile" : [ { "type" : "solicitante" , "name" : "Firmante 1" , "phone" : "+573000000000" , "email" : "example1@auco.ai" } ] } , { "name" : "Documento 2" , "signProfile" : [ { "type" : "solicitante" , "name" : "Firmante 1" , "phone" : "+573000000000" , "email" : "example2@auco.ai" } ] } ] } ) headers = { 'Authorization' : 'prk_e1cd6a01ecdb4b4ea72ec118e33b18de' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { name : 'Paquete de contratos' , email : 'example@auco.ai' , message : 'Hola a todos, les comparto el paquete de documentos para la firma' , options : { camera : 'identification' , whatsapp : true , } , camera : true , otpCode : false , documents : [ { name : 'Documento 1' , signProfile : [ { type : 'solicitante' , name : 'Firmante 1' , phone : '+573000000000' , email : 'example1@auco.ai' , } , ] , } , { name : 'Documento 2' , signProfile : [ { type : 'solicitante' , name : 'Firmante 1' , phone : '+573000000000' , email : 'example2@auco.ai' , } , ] , } , ] , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/many' , headers : { Authorization : 'prk_e1cd6a01ecdb4b4ea72ec118e33b18de' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## Paquete de documentos por medio de plantillas personalizadas ​
curl
Python
Node.js
curl -- location 'https://api.auco.ai/v1.5/ext/document/many' \ -- header 'Authorization: prk_e1cd6a01ecdb4b4ea72ec118e33b18de' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "name" : "Paquete de contratos" , "email" : "example@auco.ai" , "message" : "Hola a todos, les comparto el paquete de documentos para la firma" , "options" : { "camera" : "identification" , "whatsapp" : true } , "camera" : true , "otpCode" : false , "documents" : [ { "name" : "Documento 1" , "document" : "documentId" , "data" : [ { "key" : "signer_nombre" , "value" : "firmante 1" } , { "key" : "signer_identification" , "value" : "cc" } , { "key" : "signer_phone" , "value" : "+573000000000" } , { "key" : "manager_name" , "value" : "manager 1" } ] } , { "name" : "Documento 2" , "document" : "documentId" , "data" : [ { "key" : "signer_nombre" , "value" : "firmante 1" } , { "key" : "signer_identification" , "value" : "cc" } , { "key" : "signer_phone" , "value" : "+573000000000" } , { "key" : "manager_name" , "value" : "manager 1" } ] } ] } '
import requests import json url = "https://api.auco.ai/v1.5/ext/document/many" payload = json . dumps ( { "name" : "Paquete de contratos" , "email" : "example@auco.ai" , "message" : "Hola a todos, les comparto el paquete de documentos para la firma" , "options" : { "camera" : "identification" , "whatsapp" : True } , "camera" : True , "otpCode" : False , "documents" : [ { "name" : "Documento 1" , "document" : "documentId" , "data" : [ { "key" : "signer_nombre" , "value" : "firmante 1" } , { "key" : "signer_identification" , "value" : "cc" } , { "key" : "signer_phone" , "value" : "+573000000000" } , { "key" : "manager_name" , "value" : "manager 1" } ] } , { "name" : "Documento 2" , "document" : "documentId" , "data" : [ { "key" : "signer_nombre" , "value" : "firmante 1" } , { "key" : "signer_identification" , "value" : "cc" } , { "key" : "signer_phone" , "value" : "+573000000000" } , { "key" : "manager_name" , "value" : "manager 1" } ] } ] } ) headers = { 'Authorization' : 'prk_e1cd6a01ecdb4b4ea72ec118e33b18de' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { name : 'Paquete de contratos' , email : 'example@auco.ai' , message : 'Hola a todos, les comparto el paquete de documentos para la firma' , options : { camera : 'identification' , whatsapp : true , } , camera : true , otpCode : false , documents : [ { name : 'Documento 1' , document : 'documentId' , data : [ { key : 'signer_nombre' , value : 'firmante 1' , } , { key : 'signer_identification' , value : 'cc' , } , { key : 'signer_phone' , value : '+573000000000' , } , { key : 'manager_name' , value : 'manager 1' , } , ] , } , { name : 'Documento 2' , document : 'documentId' , data : [ { key : 'signer_nombre' , value : 'firmante 1' , } , { key : 'signer_identification' , value : 'cc' , } , { key : 'signer_phone' , value : '+573000000000' , } , { key : 'manager_name' , value : 'manager 1' , } , ] , } , ] , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/many' , headers : { Authorization : 'prk_e1cd6a01ecdb4b4ea72ec118e33b18de' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## 📥 Ejemplos de respuesta ​

## Paquede de documentos a través de PDF ​
`{ "id" : "packageId" , "documents" : [ { "url" : "https://signed_url_to_upload_PDF" , "name" : "Documento 1" , "code" : "GNAZED5HTR" , "signProfile" : [ { "name" : "Firmante 1" , "email" : "example1@auco.ai" } ] } , { "url" : "https://signed_url_to_upload_PDF" , "name" : "Documento 2" , "code" : "RC0OO75VL7" , "signProfile" : [ { "name" : "Firmante 1" , "email" : "example2@auco.ai" } ] } ] }`
La URL firmada proporcionada en la respuesta estará disponible únicamente durante 300 segundos (5 minutos) .
Debe utilizarse para cargar el documento PDF en formato binario mediante una solicitud HTTP PUT .

## A través de plantillas personalizadas ​
`{ "id" : "packageId" , "documents" : [ { "name" : "Documento 1" , "code" : "GNAZED5HTR" , "signProfile" : [ { "name" : "Firmante 1" , "email" : "example1@auco.ai" } ] } , { "name" : "Documento 2" , "code" : "RC0OO75VL7" , "signProfile" : [ { "name" : "Firmante 1" , "email" : "example2@auco.ai" } ] } ] }`

## 🔹 Firmantes que Auco no notifica ​
Un firmante queda silenciado cuando su notification efectivo es false : el suyo si lo trae, y si no, el global. signProfile siempre viene en la respuesta; lo que cambia es que los silenciados traen id y los que Auco notifica no, porque a esos su acceso se les genera al enviarles el correo.
`notification`
`false`
`signProfile`
Este ejemplo apaga la notificación de todo el paquete y la vuelve a encender solo para example2@auco.ai :
`example2@auco.ai`
`{ "name" : "Paquete de contratos" , "email" : "example@auco.ai" , "notification" : false , "documents" : [ { "name" : "Documento 1" , "signProfile" : [ { "type" : "solicitante" , "name" : "Firmante 1" , "email" : "example1@auco.ai" } , { "type" : "aprobador" , "name" : "Firmante 2" , "email" : "example2@auco.ai" , "notification" : true } ] } , { "name" : "Documento 2" , "signProfile" : [ { "type" : "solicitante" , "name" : "Firmante 1" , "email" : "example1@auco.ai" } ] } ] }`
Firmante 1 aparece en los dos documentos, así que recibe el mismo id en ambos: es una sola persona dentro del paquete. Firmante 2 no trae id porque de él se encarga Auco.
`Firmante 1`
`Firmante 2`
`{ "id" : "packageId" , "documents" : [ { "url" : "https://signed_url_to_upload_PDF" , "name" : "Documento 1" , "code" : "GNAZED5HTR" , "signProfile" : [ { "id" : "0Q" , "name" : "Firmante 1" , "email" : "example1@auco.ai" } , { "name" : "Firmante 2" , "email" : "example2@auco.ai" } ] } , { "url" : "https://signed_url_to_upload_PDF" , "name" : "Documento 2" , "code" : "RC0OO75VL7" , "signProfile" : [ { "id" : "0Q" , "name" : "Firmante 1" , "email" : "example1@auco.ai" } ] } ] }`
PARAMETROS: Campo | Tipo | Descripción ;; documents[x].signProfile | Array | Lista de firmantes del documento. ;; documents[x].signProfile[y].id | String | Identificador del firmante dentro del paquete. Solo presente cuando Auco no lo notifica; se regenera si sobreescribes el paquete. ;; documents[x].signProfile[y].name | String | Nombre del firmante. ;; documents[x].signProfile[y].email | String | Correo del firmante.

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, o alguna de las validaciones no coinciden con las condiciones de aplicabilidad ;; 400 | DOCUMENTS_MIN_TWO — El array documents debe tener al menos 2 elementos. Use /document/upload para un solo documento. ;; 401 | Autenticación inválida o ausente
Pasos para crear un paquete de documento a través de una plantilla automatizada:
Autenticación
Parámetros de creación
🧪 Ejemplos de uso Paquete de documentos por medio de PDF Paquete de documentos por medio de plantillas personalizadas
Paquete de documentos por medio de PDF
Paquete de documentos por medio de plantillas personalizadas
📥 Ejemplos de respuesta Paquede de documentos a través de PDF A través de plantillas personalizadas 🔹 Firmantes que Auco no notifica
Paquede de documentos a través de PDF
A través de plantillas personalizadas
🔹 Firmantes que Auco no notifica
⚠️ Respuestas de error