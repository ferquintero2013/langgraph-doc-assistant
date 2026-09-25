# api/manager/documents/create

> Fuente: https://docs.auco.ai/api/manager/documents/create

`/document/save`
`prk _`
Este servicio permite generar un documento dinámicamente a partir de una plantilla de Auco o de un documento personalizado previamente creado. A diferencia de la carga directa de un archivo PDF, en este flujo no se adjunta el documento como archivo. En su lugar, se envía únicamente la información (variables) requerida por la plantilla o documento base, la cual será utilizada para generar automáticamente el documento y habilitar el flujo de firma.
Antes de integrar este endopint puede necesitar ver cómo definir posiciones de firma y configuraciones de validación de identidad .

## Pasos para crear un documento: ​
Consultar plantillas o documentos personalizados disponibles: Debe iniciar consultando los recursos disponibles (plantillas propias o de Auco) para identificar el documento base que desea utilizar.
Obtener el identificador (_id) del documento base: Una vez identificada la plantilla o documento deseado, obtenga su _id para poder continuar con el proceso.
Consultar variables requeridas del documento seleccionado: Utilice el servicio correspondiente para recuperar la lista de variables que necesita completar. Este paso es esencial para construir correctamente la solicitud de creación del documento.
Construir y enviar el request de creación: Con la información de las variables, puede armar el cuerpo de la solicitud (POST) para generar el documento.
A continuación se describen los parámetros necesarios para este servicio, junto con ejemplos y posibles respuestas del sistema.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Nombre | Tipo | Descripción ;; email | String requerido | Correo electrónico del creador del proceso. ;; document | String requerido | ID del documento personalizado o la plantilla Auco. ;; sign | Boolean requerido | Parámetro que define si el proceso se realizará por medio de firma digital y electrónica. Por defecto es false , en ese caso llegará al correo el documento para su impresión. ;; name | String requerido | Nombre del proceso del documento a firmar, solo si el proceso de adjuntos incluye firma de documento. ;; message | String condicional | Mensaje que llegará en el cuerpo del correo notificando a los firmantes u aprobadores del documento. Requerido cuando algún participante es notificado por correo electrónico. ;; subject | String condicional | Asunto con el que será enviado el correo de notificación a los firmantes u aprobadores. Requerido cuando algún participante es notificado por correo electrónico. ;; folder | String condicional | Si quieres guardar este proceso en una carpeta específica, en este parámetro debes ingresar el path de dicha carpeta; ten en cuenta que la carpeta debe existir y pertenecer al creador del proceso. ;; remember | Number condicional | Parámetro que habilita recordatorios automáticos con el lapso de tiempo (horas) entre cada notificación. ;; expiredDate | Date opcional | Fecha de expiración del documento. Esta debe ser mayor a 3 días de la fecha de creación del proceso y se envia en formato Date JSON. ;; camera | Boolean opcional | Este parámetro indica si es obligatoria la validación con foto , por defecto va en false . ;; otpCode | Boolean opcional | Este parámetro indica si es obligatorio la validación por código OTP , por defecto va en false . ;; options | Object opcional | En este parámetro se indican las especificaciones de la validación de identidad. Ver más ;; notification | Boolean opcional | Define si Auco notifica a los participantes una vez creado el proceso. Por defecto es true . Aplica a todos los firmantes, salvo los que la plantilla marque con su propio notification en el signatureProfile . ;; targetWebhooks | Array[String] opcional | Si tienes varios webhooks, puedes enviar el nombre del webhook al que quieres que se notifiquen las actualizaciones de este proceso. ;; tags | Array[String] opcional | Si deseas clasificar procesos con tags, puedes enviar los nombres de los tags a los que quieres relacionar el proceso (Deben existir). ;; data | Array opcional | En este parámetro se envían todos los datos que necestia la plantilla para generar el documento. ;; data[x].key | String requerido | Nombre del parámetro registrado en la plantilla. ;; data[x].value | String requerido | Valor asignado al parámtro. ;; readers | Array opcional | Este parámetro es una lista de objetos que define los participantes que no hacen parte del proceso de firma, pero que se desea que puedan observar cada fase del proceso de firma. ;; readers[x].name | String requerido | nombre del lector. ;; readers[x].email | String requerido | correo del lector.

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.
Recuerda que los correos electrónticos y números de teléfonos entre firmantes no se deben repetir .
Los lectores van a recibir notificaciones por cada actualización en el proceso de firma.
Formato de fecha: 'DD/MM/AAAA'
`'DD/MM/AAAA'`
Los números de teléfono deben tener el indicativo del país, por ejemplo: +57, +1, +52...
`+57, +1, +52...`

## Proceso de firma base ​
curl
Python
Node.js
curl -- location 'https://api.auco.ai/v1.5/ext/document/save' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "email" : "example@auco.ai" , "name" : "PRUEBA 1" , "notification" : false , "data" : [ { "key" : "name_customer" , "value" : "Frimante 1" } , { "key" : "document_type_customer" , "value" : "cc" } , { "key" : "cedula_customer" , "value" : "1234156" } , { "key" : "email_customer" , "value" : "example@auco.ai" } , { "key" : "phone_customer" , "value" : "+573173654513" } ] , "document" : "64823dc5ce28a265e02d68f3" , "sign" : true } '
import requests import json url = "https://api.auco.ai/v1.5/ext/document/save" payload = json . dumps ( { "email" : "example@auco.ai" , "name" : "PRUEBA 1" , "notification" : False , "data" : [ { "key" : "name_customer" , "value" : "Frimante 1" } , { "key" : "document_type_customer" , "value" : "cc" } , { "key" : "cedula_customer" , "value" : "1234156" } , { "key" : "email_customer" , "value" : "example@auco.ai" } , { "key" : "phone_customer" , "value" : "+573173654513" } ] , "document" : "64823dc5ce28a265e02d68f3" , "sign" : True } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { email : 'example@auco.ai' , name : 'PRUEBA 1' , notification : false , data : [ { key : 'name_customer' , value : 'Frimante 1' , } , { key : 'document_type_customer' , value : 'cc' , } , { key : 'cedula_customer' , value : '1234156' , } , { key : 'email_customer' , value : 'example@auco.ai' , } , { key : 'phone_customer' , value : '+573173654513' , } , ] , document : '64823dc5ce28a265e02d68f3' , sign : true , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/save' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## 📥 Ejemplos de respuesta ​

## creación del proceso ​
`{ "document" : "DOCUMENTCODE" , "signProfile" : [ { "id" : "ZR" , "email" : "example@auco.ai" } ] }`

## 📋 Campos de la respuesta ​
PARAMETROS: Campo | Tipo | Descripción ;; document | String | Código del proceso creado. Es el valor que el resto de servicios recibe como code : GET /document , GET /document/roadmap y los demás. ;; signProfile | Array<Object> | Opcional. Llega cuando algún participante queda sin notificar por Auco. Trae un elemento por participante del proceso; los que Auco sí notifica vienen sin id . ;; signProfile[].id | String | Identificador del participante dentro del proceso. Es el valor que piden como userId servicios como GET /whatsapp/records . ;; signProfile[].email | String | Correo del participante.
`signProfile`
El ejemplo de arriba manda notification: false . Con ese valor Auco no avisa a los
participantes, así que la respuesta te los devuelve con su id para que puedas repartir el
proceso por tu cuenta. Un participante que la plantilla marque con notification: true en su signatureProfile sí lo notifica Auco, y llega sin id . Con notification en true —el valor
por defecto— la respuesta trae solo document .
`notification: false`
`notification: true`
`signatureProfile`
`notification`
`true`
`document`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, o alguna de las validaciones no coinciden con las condiciones de aplicabilidad ;; 401 | Autenticación inválida o ausente
Pasos para crear un documento:
Autenticación
Parámetros de creación
🧪 Ejemplos de uso Proceso de firma base
Proceso de firma base
📥 Ejemplos de respuesta creación del proceso
creación del proceso
📋 Campos de la respuesta
⚠️ Respuestas de error