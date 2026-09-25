# api/template/get-list-template

> Fuente: https://docs.auco.ai/api/template/get-list-template

Este servicio permite crear plantillas personalizadas que posteriormente se pueden utilizar para
diligenciar de documentos para firma.
`/template`
`puk _`

## Autenticación ​
Incluye tu llave publica en el encabezado Authorization .
`Authorization`
`Authorization : puk_xxx...`

## Parámetros de la petición ​
Este endpoint no recibe parámetros en el body ni query params. Solo requiere el encabezado de autenticación.

## Ejemplos de Creación ​
curl
Python
Node.js
`curl - X GET "https://api.auco.ai/v1.5/ext/template" \ - H "Authorization: your_public_key"`
import requests def get_templates ( ) : url = "https://api.auco.ai/v1.5/ext/template" headers = { "Authorization" : "your_public_key" } try : response = requests . get ( url , headers = headers ) response . raise_for_status ( ) data = response . json ( ) print ( "Templates obtenidos correctamente" ) for tpl in data . get ( "data" , [ ] ) : print ( f"- ID: { tpl [ 'id' ] } | Nombre: { tpl [ 'name' ] } " ) return data except requests . exceptions . RequestException as error : detalle = ( error . response . json ( ) if hasattr ( error , "response" ) and error . response is not None else error ) print ( f"Error obteniendo templates: { detalle } " ) if __name__ == "__main__" : get_templates ( )
const axios = require ( 'axios' ) ; async function getTemplates ( ) { try { const response = await axios . get ( 'https://api.auco.ai/v1.5/ext/template' , { headers : { Authorization : 'your_public_key' , } , } ) ; console . log ( 'Templates obtenidos correctamente' ) ; const data = response . data ; if ( Array . isArray ( data . data ) ) { data . data . forEach ( ( tpl ) => { console . log ( ` - ID: ${ tpl . id } | Nombre: ${ tpl . name } ` ) ; } ) ; } return data ; } catch ( error ) { console . error ( 'Error obteniendo templates:' , error . response ?. data || error . message ) ; } } getTemplates ( ) ;

## Ejemplo de respuesta ​
`{ "data" : [ { "id" : "template_id" , "name" : "Documento de prueba modificación variables" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "created_at" : "2025-11-26T20:48:00.000Z" , "updated_at" : "2025-11-26T20:48:00.000Z" , "status" : "active" } , { "id" : "template_id" , "name" : "Contrato de compraventa" , "created_at" : "2025-11-20T15:10:00.000Z" , "updated_at" : "2025-11-21T09:30:00.000Z" , "status" : "active" } ] }`

## Propiedades de la respuesta ​
PARAMETROS: Propiedad | Tipo | Descripción ;; data | array | Lista de plantillas ;; data[].id | string | Identificador único de la plantilla ;; data[].name | string | Nombre legible de la plantilla ;; data[].description | string | Opcional. Texto que describe la plantilla, hasta 500 caracteres. Solo aparece en las plantillas que lo tienen definido ;; data[].status | string | Estado de la plantilla (ej. active , inactive ) ;; data[].created_at | string (ISO 8601) | Fecha de creación de la plantilla ;; data[].updated_at | string (ISO 8601) | Última fecha de actualización

## Códigos de error ​
PARAMETROS: Código | Descripción ;; 401 | No autorizado (llave inválida o ausente) ;; 500 | Error interno del servidor

## Notas importantes ​
⚠️ Solo verás las plantillas creadas con tu llave pública
⚠️ La llave de autenticación debe ser tu public key , no la private key
⚠️ Las plantillas inactivas ( status: inactive ) también se devuelven en el listado
`status: inactive`
⚠️ description no viene en las plantillas que no tienen descripción: no asumas que la clave está siempre presente
`description`
ℹ️ Usa los id devueltos para futuras operaciones con templates
ℹ️ La descripción se define al crear o actualizar la plantilla
Autenticación
Parámetros de la petición
Ejemplos de Creación
Ejemplo de respuesta Propiedades de la respuesta
Propiedades de la respuesta
Códigos de error
Notas importantes