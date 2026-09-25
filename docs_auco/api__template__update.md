# api/template/update

> Fuente: https://docs.auco.ai/api/template/update

Este servicio permite actualizar plantillas personalizadas que posteriormente se pueden utilizar para
diligenciar de documentos para firma.
`/template`
`prk _`

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de actualización ​
PARAMETROS: Propiedad | Tipo | Requerido | Descripción ;; id | string | Requerido | Identificador de la plantilla ;; name | string | Opcional | Nombre de la automatización ;; description | string | Opcional | Texto que describe la plantilla, máximo 500 caracteres ;; config | array | Opcional | Array de preguntas para el usuario ;; signatureProfile | array | Opcional | Definición de firmantes y aprobadores ;; sign | array | Opcional | Nombres de preguntas obligatorias ;; preBuild | boolean | Opcional | Si es true , incluye prellenado automático
`description`
Omitir description en el PUT no borra la descripción que ya tiene la plantilla: se queda la
anterior. Para cambiarla, envía el nuevo texto —máximo 500 caracteres, o la API responde 400 —.
`description`
`PUT`
`400`
Hoy no hay forma de dejar una plantilla sin descripción una vez que la tiene: la validación rechaza
tanto el string vacío ( "" ) como null , y omitir el campo conserva el valor anterior. Si necesitas
que el texto deje de mostrarse, reemplázalo por el que corresponda.
`null`

## Ejemplos de Actualización ​
curl
Python
Node.js
curl - X PUT https : / / api . auco . ai / v1 . 5 / ext / template \ - H "Content-Type: application/json" \ - H "Authorization: your_private_key" \ - d ' { "id" : "your_template_id" , "name" : "Documento de prueba modificación variables" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "config" : [ { "name" : "nueva_pregunta" , "type" : "name" , "description" : "Ejemplo de nueva pregunta" } , { "name" : "nombre_cliente" , "type" : "name" , "description" : "Ingrese el nombre del cliente" } , { "description" : "Seleccione el tipo de documento para el cliente" , "name" : "tipo_documento_cliente" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de extranjería" , "value" : "ce" } ] } , { "description" : "Digite el número de cédula de ciudadanía para el cliente" , "name" : "cedula_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "cc" } ] } , { "description" : "Digite el número de cédula de extranjería para el cliente" , "name" : "cedula_extranjeria_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "ce" } ] } , { "name" : "correo_cliente" , "type" : "email" , "description" : "Ingrese el correo del cliente" } , { "name" : "telefono_cliente" , "type" : "phone" , "description" : "Ingrese el teléfono del cliente" } ] , "sign" : [ "nombre_cliente" , "cedula_cliente" , "cedula_extranjeria_cliente" , "correo_cliente" , "telefono_cliente" , "nueva_pregunta" ] } '
import requests import json template_data = { "id" : "your_template_id" , "name" : "Documento de prueba modificación variables" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "config" : [ { "name" : "nueva_pregunta" , "type" : "name" , "description" : "Ejemplo de nueva pregunta" } , { "name" : "nombre_cliente" , "type" : "name" , "description" : "Ingrese el nombre del cliente" } , { "description" : "Seleccione el tipo de documento para el cliente" , "name" : "tipo_documento_cliente" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de extranjería" , "value" : "ce" } ] } , { "description" : "Digite el número de cédula de ciudadanía para el cliente" , "name" : "cedula_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "cc" } ] } , { "description" : "Digite el número de cédula de extranjería para el cliente" , "name" : "cedula_extranjeria_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "ce" } ] } , { "name" : "correo_cliente" , "type" : "email" , "description" : "Ingrese el correo del cliente" } , { "name" : "telefono_cliente" , "type" : "phone" , "description" : "Ingrese el teléfono del cliente" } ] , "sign" : [ "nombre_cliente" , "cedula_cliente" , "cedula_extranjeria_cliente" , "correo_cliente" , "telefono_cliente" , "nueva_pregunta" ] } def update_template ( ) : url = "https://api.auco.ai/v1.5/ext/template" headers = { "Content-Type" : "application/json" , "Authorization" : "your_private_key" } try : response = requests . put ( url , json = template_data , headers = headers ) response . raise_for_status ( ) result = response . json ( ) print ( "Template actualizado correctamente!" ) print ( f"Template ID: { result [ 'id' ] } " ) print ( f"Mask URL: { result [ 'urls' ] [ 'mask' ] } " ) print ( f"Complete URL: { result [ 'urls' ] [ 'complete' ] } " ) return result except requests . exceptions . RequestException as error : print ( f"Error actualizando template: { error . response . json ( ) if hasattr ( error , 'response' ) else error } " ) if __name__ == "__main__" : update_template ( )
const axios = require ( 'axios' ) ; const templateData = { id : 'your_template_id' , name : 'Documento de prueba modificación variables' , description : 'Contrato de servicios con un firmante, para el equipo comercial' , config : [ { name : 'nueva_pregunta' , type : 'name' , description : 'Ejemplo de nueva pregunta' , } , { name : 'nombre_cliente' , type : 'name' , description : 'Ingrese el nombre del cliente' , } , { description : 'Seleccione el tipo de documento para el cliente' , name : 'tipo_documento_cliente' , type : 'clausula' , value : 'cc' , options : [ { name : 'Cédula de Ciudadanía' , value : 'cc' , } , { name : 'Cédula de extranjería' , value : 'ce' , } , ] , } , { description : 'Digite el número de cédula de ciudadanía para el cliente' , name : 'cedula_cliente' , type : 'number' , prereq : [ { k : 'tipo_documento_cliente' , v : 'cc' , } , ] , } , { description : 'Digite el número de cédula de extranjería para el cliente' , name : 'cedula_extranjeria_cliente' , type : 'number' , prereq : [ { k : 'tipo_documento_cliente' , v : 'ce' , } , ] , } , { name : 'correo_cliente' , type : 'email' , description : 'Ingrese el correo del cliente' , } , { name : 'telefono_cliente' , type : 'phone' , description : 'Ingrese el teléfono del cliente' , } , ] , sign : [ 'nombre_cliente' , 'cedula_cliente' , 'cedula_extranjeria_cliente' , 'correo_cliente' , 'telefono_cliente' , 'nueva_pregunta' , ] , } ; async function updateTemplate ( ) { try { const response = await axios . put ( 'https://api.auco.ai/v1.5/ext/template' , templateData , { headers : { 'Content-Type' : 'application/json' , Authorization : 'your_private_key' , } , } ) ; console . log ( 'Template actualizado correctamente!' ) ; console . log ( 'Template ID:' , response . data . id ) ; console . log ( 'Mask URL:' , response . data . urls . mask ) ; console . log ( 'Complete URL:' , response . data . urls . complete ) ; return response . data ; } catch ( error ) { console . error ( 'Error actualizando template:' , error . response ?. data || error . message ) ; } } updateTemplate ( ) ;

## Ejemplo de respuesta ​
`{ "id" : "template_id" , "urls" : { "mask" : "https://signed_url_mask" , "complete" : "https://signed_url_complete" } }`

## Carga de HTML Complete y HTML Mask: ​
Nuevamente deberás cargar los archivos HTML. En la respuesta del servicio de actualización encontrarás dos URLs de respuesta; estas tienen una vida útil de
5 minutos, después de este tiempo ya no serán válidas. Para este punto debes tener listos los archivos HTML Complete y HTML Mask y cargar los binarios de estos archivos
en peticiones de tipo PUT a cada una de estas URLs.
curl
Python
Node.js
`# Cargar HTML Mask curl -X PUT https://signed_url_mask \ -H "Content-Type: text/html" \ -d @mask.html # Cargar HTML Complete curl -X PUT https://signed_url_complete \ -H "Content-Type: text/html" \ -d @complete.html`
import requests def upload_html_files ( mask_url , complete_url ) : """ Carga los archivos HTML en las URLs firmadas Args: mask_url (str): URL firmada para el HTML Mask complete_url (str): URL firmada para el HTML Complete """ try : # Leer archivos HTML with open ( 'mask.html' , 'r' , encoding = 'utf-8' ) as f : mask_html = f . read ( ) with open ( 'complete.html' , 'r' , encoding = 'utf-8' ) as f : complete_html = f . read ( ) headers = { 'Content-Type' : 'text/html' } # Cargar Mask HTML response_mask = requests . put ( mask_url , data = mask_html , headers = headers ) print ( f"Mask HTML cargado: { response_mask . status_code } " ) # Cargar Complete HTML response_complete = requests . put ( complete_url , data = complete_html , headers = headers ) print ( f"Complete HTML cargado: { response_complete . status_code } " ) except requests . exceptions . RequestException as error : print ( f"Error al cargar: { error } " ) # Uso desde la respuesta anterior mask_url = "https://signed_url_mask" complete_url = "https://signed_url_complete" upload_html_files ( mask_url , complete_url )
const fs = require ( 'fs' ) ; const axios = require ( 'axios' ) ; /** * Carga los archivos HTML en las URLs firmadas * @param { string } maskUrl - URL firmada para el HTML Mask * @param { string } completeUrl - URL firmada para el HTML Complete */ async function uploadHtmlFiles ( maskUrl , completeUrl ) { try { // Leer archivos HTML const maskHtml = fs . readFileSync ( 'mask.html' , 'utf-8' ) ; const completeHtml = fs . readFileSync ( 'complete.html' , 'utf-8' ) ; const headers = { 'Content-Type' : 'text/html' } ; // Cargar Mask HTML await axios . put ( maskUrl , maskHtml , { headers } ) ; console . log ( 'Mask HTML cargado correctamente' ) ; // Cargar Complete HTML await axios . put ( completeUrl , completeHtml , { headers } ) ; console . log ( 'Complete HTML cargado correctamente' ) ; } catch ( error ) { console . error ( 'Error al cargar archivos:' , error . message ) ; } } // Uso desde la respuesta anterior const maskUrl = 'https://signed_url_mask' ; const completeUrl = 'https://signed_url_complete' ; uploadHtmlFiles ( maskUrl , completeUrl ) ;
Las URLs firmadas expiran en 5 minutos . Debe completar la carga antes de este tiempo vencer. Si expiran, no hay forma de regenerarlas — deberás volver a llamar PUT /template .
`PUT /template`
Si solo estás actualizando config , sign o signatureProfile y el HTML sigue igual, puedes ignorar las URLs devueltas y no subir nada. El servidor conservará los HTMLs de la versión anterior.
`config`
`sign`
`signatureProfile`
Autenticación
Parámetros de actualización
Ejemplos de Actualización
Ejemplo de respuesta
Carga de HTML Complete y HTML Mask: