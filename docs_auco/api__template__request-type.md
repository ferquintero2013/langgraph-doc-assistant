# api/template/request-type

> Fuente: https://docs.auco.ai/api/template/request-type

El tipo de pregunta request permite que tu plantilla consulte un servicio HTTP externo para validar la entrada del usuario y utilizar la respuesta del servicio para prellenar otros campos del documento. Está pensado para escenarios en los que un único dato (un código, una referencia, un identificador tributario) puede resolverse en muchos valores preconocidos que el usuario no debería tener que escribir manualmente.
`request`

## Cuándo usar request ​
`request`
Patrones comunes:
Código promocional / descuento : el usuario escribe un código → el servicio lo valida y devuelve el monto del descuento, la descripción y la fecha de vencimiento, que se autocompletan en el documento.
Búsqueda de referencia o póliza : el usuario escribe un número de póliza → el servicio devuelve el nombre del titular, la dirección y la prima.
Resolución por identificador tributario : el usuario escribe un NIT/RUT → el servicio devuelve la razón social, la dirección y el representante legal.
Búsqueda de reserva / orden : el usuario escribe una referencia de reserva → el servicio devuelve fechas, nombres de participantes y montos.
En todos estos casos, la pregunta request es el campo detonante , y otras preguntas de la misma plantilla se convierten en salidas pobladas por la respuesta del servicio.
`request`
Este tipo requiere que tú (o tu equipo de plataforma) construya y aloje un endpoint HTTP que cumpla el contrato descrito abajo. El SDK de Auco no provee un backend por defecto — simplemente consulta la URL que configures.

## Estructura de la Pregunta ​
`{ "name" : "codigo_promocion" , "description" : "Ingrese su código promocional" , "type" : "request" , "endpoint" : "https://tu-servicio.example.com/promo-validate" }`
PARAMETROS: Propiedad | Tipo | Requerido | Descripción ;; name | string | Requerido | Identificador único de la pregunta. ;; description | string | Requerido | Texto mostrado al usuario describiendo qué debe ingresar. ;; type | string | Requerido | Debe ser "request" . ;; endpoint | string | Requerido | URL HTTPS completa a la que el SDK hará POST.
La UI de entrada para el usuario es un input de texto plano (igual que type: text ). La etiqueta del botón cambia de "Siguiente" a "Validar" para que el usuario sepa que el valor será validado contra un servicio antes de avanzar.
`type: text`

## HTML Correspondiente ​
La pregunta request en sí usa un span estándar — nada especial:
`request`
`< p > Código promocional: < span name = " codigo_promocion " > ___________ </ span > </ p >`
Las preguntas que serán prellenadas por la respuesta también usan spans estándar, y deben existir como preguntas en el config del JSON para que el SDK conozca sus tipos:
`config`
`< p > Monto del descuento: < span name = " monto_descuento " > ___________ </ span > </ p > < p > Descripción de la oferta: < span name = " descripcion_promocion " > ___________ </ span > </ p > < p > Válido hasta: < span name = " vencimiento_promocion " > ___________ </ span > </ p >`

## Contrato del Endpoint ​

## Solicitud ​
El SDK envía una solicitud POST a la URL del endpoint con un cuerpo JSON.
`endpoint`
`POST {endpoint} Content-Type : application/json { "key" : "<nombre_pregunta>" , "value" : "<entrada_usuario>" }`
PARAMETROS: Campo | Tipo | Descripción ;; key | string | El name de la pregunta request (p. ej. "codigo_promocion" ). ;; value | string | El texto que el usuario ingresó.

## Respuesta — Éxito (HTTP 200 ) ​
`200`
El cuerpo debe ser un arreglo JSON de pares {key, value} . Cada par le indica al SDK que pueble una pregunta del documento.
`{key, value}`
`[ { "key" : "monto_descuento" , "value" : "15000" } , { "key" : "descripcion_promocion" , "value" : "Black Friday Special" } , { "key" : "vencimiento_promocion" , "value" : "2026-12-31" } ]`
PARAMETROS: Campo | Tipo | Descripción ;; key | string | El name de la pregunta de la plantilla a actualizar. ;; value | string | La cadena a inyectar. Para date , usar formato ISO ( YYYY-MM-DD ). Para currency / number , usar la cadena numérica cruda.
Qué hace el SDK con la respuesta:
Para cada par {key, value} , busca la pregunta en config por name y establece su valor interno.
`{key, value}`
`config`
`name`
Para cada par {key, value} , actualiza cada <span name="{key}"> del documento renderizado con value como innerHTML.
`{key, value}`
`<span name="{key}">`
`value`
Avanza al usuario a la siguiente pregunta del flujo.

## Respuesta — Error (HTTP 4xx / 5xx o cuerpo que no sea arreglo) ​
`4xx`
`5xx`
El SDK muestra el mensaje de error "Código inválido" debajo del input y bloquea al usuario hasta que ingrese un valor válido.
El SDK muestra un mensaje de error genérico independientemente del código HTTP o del cuerpo de respuesta. Si necesitas diferenciar errores (p. ej., "código vencido" vs. "no encontrado"), considera devolver HTTP 200 con un arreglo vacío y un campo de estado separado, o extender el SDK en tu integración.
`200`

## Ejemplo Completo — Código Promocional ​

## JSON ​
{ "name" : "Suscripción con Código Promocional" , "preBuild" : false , "config" : [ { "name" : "codigo_promocion" , "description" : "Ingrese su código promocional" , "type" : "request" , "endpoint" : "https://api.example.com/promo-validate" } , { "name" : "descripcion_promocion" , "description" : "Descripción de la oferta" , "type" : "text" } , { "name" : "monto_descuento" , "description" : "Monto del descuento" , "type" : "currency" } , { "name" : "vencimiento_promocion" , "description" : "Válido hasta" , "type" : "date" } , { "name" : "nombre_suscriptor" , "description" : "Ingrese su nombre completo" , "type" : "name" } , { "name" : "email_suscriptor" , "description" : "Ingrese su correo electrónico" , "type" : "email" } ] , "signatureProfile" : [ { "name" : "nombre_suscriptor" , "identification" : "email_suscriptor" , "email" : "email_suscriptor" , "phone" : "email_suscriptor" , "type" : "suscriptor" } ] , "sign" : [ "nombre_suscriptor" , "email_suscriptor" ] }

## HTML (fragmento) ​
`< h2 > Código Promocional </ h2 > < p > Código: < span name = " codigo_promocion " > ___________ </ span > </ p > < p > Oferta: < span name = " descripcion_promocion " > ___________ </ span > </ p > < p > Descuento: < span name = " monto_descuento " > ___________ </ span > </ p > < p > Válido hasta: < span name = " vencimiento_promocion " > ___________ </ span > </ p >`

## Ejemplo de Implementación del Servicio (Node.js / Express) ​
const express = require ( 'express' ) ; const app = express ( ) ; app . use ( express . json ( ) ) ; const promos = { BLACK2026 : { descripcion_promocion : 'Black Friday Special' , monto_descuento : '15000' , vencimiento_promocion : '2026-12-31' , } , SPRING10 : { descripcion_promocion : 'Descuento de Primavera' , monto_descuento : '5000' , vencimiento_promocion : '2026-06-30' , } , } ; app . post ( '/promo-validate' , ( req , res ) => { const { value } = req . body ; const promo = promos [ value ?. toUpperCase ( ) ] ; if ( ! promo ) return res . status ( 404 ) . json ( { message : 'Código no encontrado' } ) ; const response = Object . entries ( promo ) . map ( ( [ key , value ] ) => ( { key , value } ) ) ; res . json ( response ) ; } ) ; app . listen ( 3000 ) ;

## Ejemplo de Implementación del Servicio (Python / FastAPI) ​
`from fastapi import FastAPI , HTTPException from pydantic import BaseModel app = FastAPI ( ) promos = { "BLACK2026" : { "descripcion_promocion" : "Black Friday Special" , "monto_descuento" : "15000" , "vencimiento_promocion" : "2026-12-31" , } , } class RequestPayload ( BaseModel ) : key : str value : str @app . post ( "/promo-validate" ) def validate ( payload : RequestPayload ) : promo = promos . get ( payload . value . upper ( ) ) if not promo : raise HTTPException ( status_code = 404 , detail = "Código no encontrado" ) return [ { "key" : k , "value" : v } for k , v in promo . items ( ) ]`

## Lineamientos de Implementación ​

## Para equipos de backend que construyen el servicio ​
Usa HTTPS. El SDK rechaza endpoints http:// .
`http://`
Habilita CORS para el origen del SDK de Auco — la llamada se hace desde el navegador, no de servidor a servidor.
Devuelve solo preguntas que existan en el config de la plantilla. Las claves que no coincidan con ninguna pregunta se ignoran silenciosamente.
`config`
Los valores se inyectan como cadenas HTML-safe. Si necesitas renderizar imágenes o markup, debes usar un tipo de pregunta que lo soporte ( image ) y garantizar que tu valor sea un data URI válido. El HTML plano en value no es sanitizado por el SDK.
`image`
`value`
Respeta los tipos de datos. Si la pregunta destino es type: date , devuelve YYYY-MM-DD . Si es type: currency , devuelve el número crudo sin formato — el SDK lo formateará.
`type: date`
`YYYY-MM-DD`
`type: currency`
No confíes en el cliente. El campo key refleja el nombre de la pregunta pero la lógica real de validación debe usar value . Trata este endpoint como cualquier endpoint público respecto a límites de tasa, autenticación y abuso.
`key`
`value`

## Para autores de plantillas ​
Cada {key} devuelto por tu servicio debe existir como una pregunta en el config del JSON, o será ignorado.
`{key}`
`config`
Las preguntas prellenadas aún deben estar presentes en el HTML como placeholders <span name="{key}"> .
`<span name="{key}">`
Si una pregunta prellenada también aparece en el arreglo sign , el usuario podrá avanzar aunque no haya escrito el valor él mismo — el valor proporcionado por el servicio cuenta como diligenciado.
`sign`
Puedes encadenar múltiples preguntas request en una sola plantilla si distintas entradas resuelven distintos campos.
`request`

## Limitaciones ​
Actualmente el SDK hace la solicitud desde el navegador. No ocurre validación del lado del servidor automáticamente — tu endpoint debe ser accesible por internet desde el navegador del usuario.
La respuesta debe ser un arreglo plano de pares {key, value} . No se soportan objetos anidados.
`{key, value}`
Todos los campos value en la respuesta son strings. Los booleanos o números deben serializarse como strings.
`value`
Las respuestas de error se presentan genéricamente como "Código inválido". No se soportan mensajes de error detallados por campo.
La pregunta request en sí no se almacena de regreso en el servicio como parte del documento final — solo dirige la búsqueda. La entrada del usuario se guarda en el value de la pregunta como cualquier otro campo.
`request`
`value`
Cuándo usar request
`request`
Estructura de la Pregunta
HTML Correspondiente
Contrato del Endpoint Solicitud Respuesta — Éxito (HTTP 200 ) Respuesta — Error (HTTP 4xx / 5xx o cuerpo que no sea arreglo)
Solicitud
Respuesta — Éxito (HTTP 200 )
`200`
Respuesta — Error (HTTP 4xx / 5xx o cuerpo que no sea arreglo)
`4xx`
`5xx`
Ejemplo Completo — Código Promocional JSON HTML (fragmento) Ejemplo de Implementación del Servicio (Node.js / Express) Ejemplo de Implementación del Servicio (Python / FastAPI)
JSON
HTML (fragmento)
Ejemplo de Implementación del Servicio (Node.js / Express)
Ejemplo de Implementación del Servicio (Python / FastAPI)
Lineamientos de Implementación Para equipos de backend que construyen el servicio Para autores de plantillas
Para equipos de backend que construyen el servicio
Para autores de plantillas
Limitaciones