# api/template/create

> Fuente: https://docs.auco.ai/api/template/create

Este servicio permite crear plantillas personalizadas que posteriormente se pueden utilizar para
diligenciar de documentos para firma.
`/template`
`prk _`

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Parámetros de creación ​
PARAMETROS: Propiedad | Tipo | Requerido | Descripción ;; name | string | Requerido | Nombre de la automatización ;; description | string | Opcional | Texto que describe la plantilla, máximo 500 caracteres ;; config | array | Requerido | Array de preguntas para el usuario ;; signatureProfile | array | Requerido | Definición de firmantes y aprobadores ;; sign | array | Requerido | Nombres de preguntas obligatorias ;; preBuild | boolean | Requerido | Si es true , incluye prellenado automático
`description`
description es informativo: no cambia el comportamiento de la plantilla y sirve para que tu equipo
reconozca para qué es cada una. Si no lo envías, la plantilla queda sin descripción. Si el texto pasa
de 500 caracteres, la API responde 400 y no crea la plantilla.
`description`
`400`
El campo lo devuelve GET /template , tanto en el listado como en
el detalle por id .
`GET /template`

## Ejemplos de Creación ​
curl
Python
Node.js
curl - X POST https : / / api . auco . ai / v1 . 5 / ext / template \ - H "Content-Type: application/json" \ - H "Authorization: your_private_key" \ - d ' { "name" : "Documento de prueba modificación variables" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "config" : [ { "name" : "nombre_cliente" , "type" : "name" , "description" : "Ingrese el nombre del cliente" } , { "description" : "Seleccione el tipo de documento para el cliente" , "name" : "tipo_documento_cliente" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de extranjería" , "value" : "ce" } ] } , { "description" : "Digite el número de cédula de ciudadanía para el cliente" , "name" : "cedula_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "cc" } ] } , { "description" : "Digite el número de cédula de extranjería para el cliente" , "name" : "cedula_extranjeria_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "ce" } ] } , { "name" : "correo_cliente" , "type" : "email" , "description" : "Ingrese el correo del cliente" } , { "name" : "telefono_cliente" , "type" : "phone" , "description" : "Ingrese el teléfono del cliente" } ] , "sign" : [ "nombre_cliente" , "cedula_cliente" , "cedula_extranjeria_cliente" , "correo_cliente" , "telefono_cliente" ] , "signatureProfile" : [ { "email" : "correo_cliente" , "phone" : "telefono_cliente" , "identification" : "cedula_cliente|cedula_extranjeria_cliente" , "name" : "nombre_cliente" , "type" : "cliente" } ] } '
import requests import json template_data = { "name" : "Documento de prueba modificación variables" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "config" : [ { "name" : "nombre_cliente" , "type" : "name" , "description" : "Ingrese el nombre del cliente" } , { "description" : "Seleccione el tipo de documento para el cliente" , "name" : "tipo_documento_cliente" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de extranjería" , "value" : "ce" } ] } , { "description" : "Digite el número de cédula de ciudadanía para el cliente" , "name" : "cedula_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "cc" } ] } , { "description" : "Digite el número de cédula de extranjería para el cliente" , "name" : "cedula_extranjeria_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "ce" } ] } , { "name" : "correo_cliente" , "type" : "email" , "description" : "Ingrese el correo del cliente" } , { "name" : "telefono_cliente" , "type" : "phone" , "description" : "Ingrese el teléfono del cliente" } ] , "sign" : [ "nombre_cliente" , "cedula_cliente" , "cedula_extranjeria_cliente" , "correo_cliente" , "telefono_cliente" ] , "signatureProfile" : [ { "email" : "correo_cliente" , "phone" : "telefono_cliente" , "identification" : "cedula_cliente|cedula_extranjeria_cliente" , "name" : "nombre_cliente" , "type" : "cliente" } ] } def create_template ( ) : url = "https://api.auco.ai/v1.5/ext/template" headers = { "Content-Type" : "application/json" , "Authorization" : "your_private_key" } try : response = requests . post ( url , json = template_data , headers = headers ) response . raise_for_status ( ) result = response . json ( ) print ( "Template created successfully!" ) print ( f"Template ID: { result [ 'data' ] [ 'template_id' ] } " ) print ( f"Signed URL: { result [ 'data' ] [ 'signed_url' ] } " ) return result [ 'data' ] except requests . exceptions . RequestException as error : print ( f"Error creating template: { error . response . json ( ) if hasattr ( error , 'response' ) else error } " ) if __name__ == "__main__" : create_template ( )
const axios = require ( 'axios' ) ; const templateData = { name : 'Documento de prueba modificación variables' , description : 'Contrato de servicios con un firmante, para el equipo comercial' , config : [ { name : 'nombre_cliente' , type : 'name' , description : 'Ingrese el nombre del cliente' , } , { description : 'Seleccione el tipo de documento para el cliente' , name : 'tipo_documento_cliente' , type : 'clausula' , value : 'cc' , options : [ { name : 'Cédula de Ciudadanía' , value : 'cc' , } , { name : 'Cédula de extranjería' , value : 'ce' , } , ] , } , { description : 'Digite el número de cédula de ciudadanía para el cliente' , name : 'cedula_cliente' , type : 'number' , prereq : [ { k : 'tipo_documento_cliente' , v : 'cc' , } , ] , } , { description : 'Digite el número de cédula de extranjería para el cliente' , name : 'cedula_extranjeria_cliente' , type : 'number' , prereq : [ { k : 'tipo_documento_cliente' , v : 'ce' , } , ] , } , { name : 'correo_cliente' , type : 'email' , description : 'Ingrese el correo del cliente' , } , { name : 'telefono_cliente' , type : 'phone' , description : 'Ingrese el teléfono del cliente' , } , ] , sign : [ 'nombre_cliente' , 'cedula_cliente' , 'cedula_extranjeria_cliente' , 'correo_cliente' , 'telefono_cliente' ] , signatureProfile : [ { email : 'correo_cliente' , phone : 'telefono_cliente' , identification : 'cedula_cliente|cedula_extranjeria_cliente' , name : 'nombre_cliente' , type : 'cliente' , } , ] , } ; async function createTemplate ( ) { try { const response = await axios . post ( 'https://api.auco.ai/v1.5/ext/template' , templateData , { headers : { 'Content-Type' : 'application/json' , Authorization : 'your_private_key' , } , } ) ; console . log ( 'Template created successfully!' ) ; console . log ( 'Template ID:' , response . data . data . template_id ) ; console . log ( 'Signed URL:' , response . data . data . signed_url ) ; return response . data . data ; } catch ( error ) { console . error ( 'Error creating template:' , error . response ?. data || error . message ) ; } } createTemplate ( ) ;

## Ejemplo de respuesta ​
`{ "id" : "template_id" , "urls" : { "mask" : "https://signed_url_mask" , "complete" : "https://signed_url_complete" } }`

## Carga de HTML Complete y HTML Mask: ​
En la respuesta del servicio de creación encontrarás dos url de respuesta, estas tienen una vida util de
5 minutos, después de este tiempo ya no serán válidas. Para este punto ya debe tener listos los archivos HTML Complete y HTML Mask y cargar los binarios de estos archivos
en peticiones de tipo PUT a cada una de estas url.
curl
Python
Node.js
`# Cargar HTML Mask curl -X PUT https://signed_url_mask \ -H "Content-Type: text/html" \ -d @mask.html # Cargar HTML Complete curl -X PUT https://signed_url_complete \ -H "Content-Type: text/html" \ -d @complete.html`
import requests def upload_html_files ( mask_url , complete_url ) : """ Carga los archivos HTML en las URLs firmadas Args: mask_url (str): URL firmada para el HTML Mask complete_url (str): URL firmada para el HTML Complete """ try : # Leer archivos HTML with open ( 'mask.html' , 'r' , encoding = 'utf-8' ) as f : mask_html = f . read ( ) with open ( 'complete.html' , 'r' , encoding = 'utf-8' ) as f : complete_html = f . read ( ) headers = { 'Content-Type' : 'text/html' } # Cargar Mask HTML response_mask = requests . put ( mask_url , data = mask_html , headers = headers ) print ( f"Mask HTML cargado: { response_mask . status_code } " ) # Cargar Complete HTML response_complete = requests . put ( complete_url , data = complete_html , headers = headers ) print ( f"Complete HTML cargado: { response_complete . status_code } " ) except requests . exceptions . RequestException as error : print ( f"Error al cargar: { error } " ) # Uso desde la respuesta anterior mask_url = "https://signed_url_mask" complete_url = "https://signed_url_complete" upload_html_files ( mask_url , complete_url )
const fs = require ( 'fs' ) ; const axios = require ( 'axios' ) ; /** * Carga los archivos HTML en las URLs firmadas * @param { string } maskUrl - URL firmada para el HTML Mask * @param { string } completeUrl - URL firmada para el HTML Complete */ async function uploadHtmlFiles ( maskUrl , completeUrl ) { try { // Leer archivos HTML const maskHtml = fs . readFileSync ( 'mask.html' , 'utf-8' ) ; const completeHtml = fs . readFileSync ( 'complete.html' , 'utf-8' ) ; const headers = { 'Content-Type' : 'text/html' } ; // Cargar Mask HTML await axios . put ( maskUrl , maskHtml , { headers } ) ; console . log ( 'Mask HTML cargado correctamente' ) ; // Cargar Complete HTML await axios . put ( completeUrl , completeHtml , { headers } ) ; console . log ( 'Complete HTML cargado correctamente' ) ; } catch ( error ) { console . error ( 'Error al cargar archivos:' , error . message ) ; } } // Uso desde la respuesta anterior const maskUrl = 'https://signed_url_mask' ; const completeUrl = 'https://signed_url_complete' ; uploadHtmlFiles ( maskUrl , completeUrl ) ;
Las URLs firmadas expiran en 5 minutos . Debe completar la carga antes de este tiempo vencer.
Autenticación
Parámetros de creación
Ejemplos de Creación
Ejemplo de respuesta
Carga de HTML Complete y HTML Mask: