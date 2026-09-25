# api/template/get-template

> Fuente: https://docs.auco.ai/api/template/get-template

Este servicio permite obtener los detalles completos de una plantilla específica usando su id . Es útil para consultar la configuración, campos, perfiles de firma y metadatos de una plantilla antes de usarla en procesos de firma o modificaciones.
`/template?id={templateId}`
`puk _`

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de creación ​
PARAMETROS: Propiedad | Tipo | Requerido | Descripción ;; id | string | Requerido | Identificador único de la plantilla

## Ejemplos de Creación ​
curl
Python
Node.js
`curl - X GET "https://api.auco.ai/v1.5/ext/template?id=template_id" \ - H "Authorization: your_public_key"`
import requests def get_template ( template_id ) : """ Obtiene los detalles de una plantilla específica Args: template_id (str): ID de la plantilla a obtener """ url = "https://api.auco.ai/v1.5/ext/template" params = { "id" : template_id } headers = { "Authorization" : "your_public_key" } try : response = requests . get ( url , params = params , headers = headers ) response . raise_for_status ( ) data = response . json ( ) print ( f"Template obtenido: { data [ 'name' ] } " ) print ( f"Estado: { data [ 'status' ] } " ) print ( f"Campos: { len ( data [ 'config' ] ) } " ) return data except requests . exceptions . RequestException as error : detalle = ( error . response . json ( ) if hasattr ( error , "response" ) and error . response is not None else error ) print ( f"Error obteniendo template: { detalle } " ) if __name__ == "__main__" : # Reemplaza con tu template_id get_template ( "template_id" )
const axios = require ( 'axios' ) ; /** * Obtiene los detalles de una plantilla específica * @param { string } templateId - ID de la plantilla a obtener */ async function getTemplate ( templateId ) { try { const response = await axios . get ( 'https://api.auco.ai/v1.5/ext/template' , { params : { id : templateId , } , headers : { Authorization : 'your_public_key' , } , } ) ; const data = response . data ; console . log ( ` Template obtenido: ${ data . name } ` ) ; console . log ( ` Estado: ${ data . status } ` ) ; console . log ( ` Campos: ${ data . config . length } ` ) ; return data ; } catch ( error ) { console . error ( 'Error obteniendo template:' , error . response ?. data || error . message ) ; } } // Reemplaza con tu template_id getTemplate ( 'template_id' ) ;

## Ejemplo de respuesta ​
{ "id" : "template_id" , "name" : "Documento de prueba modificación variables" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "created_at" : "2025-11-26T20:48:00.000Z" , "updated_at" : "2025-11-26T20:48:00.000Z" , "status" : "active" , "config" : [ { "name" : "nombre_cliente" , "type" : "name" , "description" : "Ingrese el nombre del cliente" } , { "description" : "Seleccione el tipo de documento para el cliente" , "name" : "tipo_documento_cliente" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de extranjería" , "value" : "ce" } ] } , { "description" : "Digite el número de cédula de ciudadanía para el cliente" , "name" : "cedula_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "cc" } ] } , { "description" : "Digite el número de cédula de extranjería para el cliente" , "name" : "cedula_extranjeria_cliente" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento_cliente" , "v" : "ce" } ] } , { "name" : "correo_cliente" , "type" : "email" , "description" : "Ingrese el correo del cliente" } , { "name" : "telefono_cliente" , "type" : "phone" , "description" : "Ingrese el teléfono del cliente" } ] , "sign" : [ "nombre_cliente" , "cedula_cliente" , "cedula_extranjeria_cliente" , "correo_cliente" , "telefono_cliente" ] , "signatureProfile" : [ { "email" : "correo_cliente" , "phone" : "telefono_cliente" , "identification" : "cedula_cliente|cedula_extranjeria_cliente" , "name" : "nombre_cliente" , "type" : "cliente" } ] , "preBuild" : false }

## Propiedades de la respuesta ​
PARAMETROS: Propiedad | Tipo | Descripción ;; id | string | Identificador único de la plantilla ;; name | string | Nombre de la plantilla ;; description | string | Opcional. Texto que describe la plantilla, hasta 500 caracteres. Solo aparece si la plantilla lo tiene definido ;; status | string | Estado de la plantilla ( active , inactive ) ;; created_at | string (ISO 8601) | Fecha de creación ;; updated_at | string (ISO 8601) | Última fecha de actualización ;; config | array | Array de preguntas/campos de la plantilla ;; config[].name | string | Identificador único del campo ;; config[].type | string | Tipo de pregunta ( text , name , email , etc.) ;; config[].description | string | Texto que ve el usuario ;; config[].value | string | Valor por defecto (opcional) ;; config[].options | array | Opciones disponibles para campos clausula / select ;; config[].prereq | array | Condiciones para mostrar el campo (opcional) ;; sign | array | Nombres de preguntas obligatorias ;; signatureProfile | array | Configuración de firmantes ;; signatureProfile[].name | string | Campo con el nombre del firmante ;; signatureProfile[].identification | string | Campo(s) de identificación (separados por | ) ;; signatureProfile[].email | string | Campo con el correo del firmante ;; signatureProfile[].phone | string | Campo con el teléfono del firmante ;; signatureProfile[].type | string | Identificador de la firma (ej: cliente , vendedor ) ;; preBuild | boolean | Si la plantilla incluye prellenado automático
`description`
description es texto libre que defines al crear o actualizar la plantilla, y solo viene en la respuesta cuando la plantilla lo
tiene definido. No lo uses como identificador: para eso está el id .
`description`

## Códigos de error ​
PARAMETROS: Código | Descripción ;; 400 | Solicitud inválida (parámetro id faltante) ;; 401 | No autorizado (llave inválida o ausente) ;; 404 | Template no encontrado ;; 500 | Error interno del servidor
Autenticación
Parámetros de creación
Ejemplos de Creación
Ejemplo de respuesta Propiedades de la respuesta
Propiedades de la respuesta
Códigos de error