# api/manager/documents/prebuild

> Fuente: https://docs.auco.ai/api/manager/documents/prebuild

`/document/prebuild`
`prk _`
Este servicio permite crear un proceso de firma a partir de un documento personalizado precargando solo una parte de la información, y enviarlo a un destinatario para que complete los datos restantes. A diferencia de la creación de documento , donde se envían todos los valores necesarios para generar el documento de inmediato, aquí el proceso se crea en estado en progreso con los campos precargados y queda a la espera de que el destinatario diligencie la información pendiente.
Es útil cuando una parte (por ejemplo, tu organización) conoce de antemano algunos datos del documento y desea dejarlos completados, mientras que la otra parte (el destinatario) debe aportar el resto antes de firmar.
Los campos que pueden precargarse están definidos en la configuración del documento personalizado. Antes de integrar este endpoint puede necesitar consultar las variables del documento y, si aplica, cómo definir posiciones de firma y configuraciones de validación de identidad .

## Pasos para precargar un documento: ​
Consultar el documento personalizado: Identifique el documento personalizado que desea utilizar y obtenga su _id .
`_id`
Identificar las variables precargables: Consulta las variables del documento para conocer cuáles puedes precargar.
Construir el arreglo preBuild : Arme la lista de pares key / value con los datos que desea dejar diligenciados.
`preBuild`
`key`
`value`
Enviar el request: Realice la solicitud (POST) indicando el destinatario ( emailTo ) que completará la información restante.
`emailTo`
A continuación se describen los parámetros necesarios para este servicio, junto con ejemplos y posibles respuestas del sistema.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de precarga ​
PARAMETROS: Nombre | Tipo | Descripción ;; email | String requerido | Correo electrónico del creador del proceso. ;; name | String requerido | Nombre del proceso del documento. ;; document | String requerido | ID del documento personalizado a partir del cual se crea el proceso. ;; preBuild | Array requerido | Lista de objetos con los datos que se precargan en el documento. Solo se aceptan las variables habilitadas para precarga en la configuración del documento. ;; preBuild[x].key | String requerido | Nombre de la variable registrada en el documento. ;; preBuild[x].value | String requerido | Valor asignado a la variable. ;; sign | Boolean requerido | Define si el proceso se realizará por medio de firma. Si es false , el documento llegará al correo para su impresión. ;; notification | Boolean requerido | Define si se notifica al destinatario ( emailTo ) una vez creado el proceso para que complete la información. ;; emailTo | String requerido | Correo electrónico del destinatario que debe completar los datos restantes del documento. ;; folder | String condicional | Path de la carpeta donde se guardará el proceso. La carpeta debe existir y pertenecer al creador del proceso. ;; camera | Boolean opcional | Indica si es obligatoria la validación con foto , por defecto false . ;; otpCode | Boolean opcional | Indica si es obligatoria la validación por código OTP , por defecto false . ;; options | Object opcional | Especificaciones de la validación de identidad. Ver más ;; expiredDate | Date opcional | Fecha de expiración del documento. Debe ser mayor a 3 días respecto a la fecha de creación y se envía en formato Date JSON.

## 🧪 Ejemplos de uso ​
Puedes copiar cualquiera de los ejemplos según el lenguaje de tu preferencia.
En preBuild solo debes enviar las variables que deseas dejar precargadas; el destinatario completará las restantes.
`preBuild`
Los números de teléfono deben tener el indicativo del país, por ejemplo: +57, +1, +52...
`+57, +1, +52...`

## Precarga de datos ​
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/document/prebuild' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "email" : "example@auco.ai" , "name" : "Contrato laboral - Juan Pérez" , "document" : "64823dc5ce28a265e02d68f3" , "sign" : true , "notification" : true , "emailTo" : "juan.perez@example.com" , "preBuild" : [ { "key" : "company_name" , "value" : "Auco SAS" } , { "key" : "position" , "value" : "Backend Developer" } ] } '`
import requests import json url = "https://api.auco.ai/v1.5/ext/document/prebuild" payload = json . dumps ( { "email" : "example@auco.ai" , "name" : "Contrato laboral - Juan Pérez" , "document" : "64823dc5ce28a265e02d68f3" , "sign" : True , "notification" : True , "emailTo" : "juan.perez@example.com" , "preBuild" : [ { "key" : "company_name" , "value" : "Auco SAS" } , { "key" : "position" , "value" : "Backend Developer" } ] } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )
const axios = require ( 'axios' ) ; let data = JSON . stringify ( { email : 'example@auco.ai' , name : 'Contrato laboral - Juan Pérez' , document : '64823dc5ce28a265e02d68f3' , sign : true , notification : true , emailTo : 'juan.perez@example.com' , preBuild : [ { key : 'company_name' , value : 'Auco SAS' , } , { key : 'position' , value : 'Backend Developer' , } , ] , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/document/prebuild' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;

## 📥 Ejemplos de respuesta ​

## Creación del proceso ​
`{ "document" : "DOCUMENTCODE" }`

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros, el documento no existe, o alguna variable no coincide con la configuración del documento ;; 401 | Autenticación inválida o ausente
Pasos para precargar un documento:
Autenticación
Parámetros de precarga
🧪 Ejemplos de uso Precarga de datos
Precarga de datos
📥 Ejemplos de respuesta Creación del proceso
Creación del proceso
⚠️ Respuestas de error