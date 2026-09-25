# api/template/introduction

> Fuente: https://docs.auco.ai/api/template/introduction

Guía completa para crear plantillas y/o documentos automatizados con HTML, JSON y el SDK de generación de documentos.
Toda automatización requiere exactamente 3 archivos :
PARAMETROS: Archivo | Descripción ;; Mask HTML | El HTML que ve el usuario mientras completa el formulario a través del SDK ;; Complete HTML | HTML para generar el PDF final, incluye espacios para firmas ;; Objeto JSON | Controla el comportamiento, define firmantes y preguntas

## Flujo General ​
El proceso siempre comienza con la construcción del complete HTML . Este documento debe contener espacios editables
donde el usuario ingresa información, este HTML dependerá de las variables registradas en el JSON donde cada pregunta tiene un identificador.
Por ejemplo:
HTML:
`< p > Descripción: < span name = " pregunta_1 " > ___________ </ span > </ p >`
Pregunta en el JSON:
`[ ... , { "name" : "pregunta_1" , "description" : "Digite el nombre completo del representante legal de la empresa empleadora" , "type" : "text" } , ... ]`
Lo que finalmente ve el usuario:

## Configuración ​
Para iniciar a generar los archivos HTML, conoce todo acerca de su creación en Configuración del HTML .
Para iniciar a generar el archivo JSON, consulta la referencia completa en Configuración JSON — cubre los 17 tipos de pregunta, validaciones y lógica condicional.
Para plantillas que necesitan validar un código o consultar datos prellenados desde tu propio servicio, consulta Tipo Request .

## Tips y Mejores Prácticas ​
Nomenclatura consistente: Usa snake_case descriptivo para las preguntas: nombre_comprador , email_vendedor .
`snake_case`
`nombre_comprador`
`email_vendedor`
Tipos de campo según la semántica: usa identification para documentos de firmantes (no text ni number ), nit para NITs colombianos, currency para dinero, email para correos.
`identification`
`text`
`number`
`nit`
`currency`
`email`
Validación temprana: marca preguntas críticas en el array sign .
`sign`
Aprovecha las validaciones: infiere subYears (edad), maxlength , regex , min / max a partir de los propios requisitos del documento. Consulta Propiedades de Validación .
`subYears`
`maxlength`
`regex`
`min`
`max`
Convención de firmantes: nunca mezcles id y name para el mismo firmante en el Complete HTML. Si una firma aparece en varios lugares, usa name consistentemente — consulta Ubicación de Firmas .
`name`
Campos automáticos: agrega <span name="signDate"> donde deba aparecer la fecha de firma y <span name="signComplete" hidden> para confirmaciones posteriores a la firma. Consulta Campos Automáticos .
`<span name="signDate">`
`<span name="signComplete" hidden>`
Múltiples identificaciones: usa | en signatureProfile.identification para soportar varios tipos de documento para un mismo firmante.
`signatureProfile.identification`
Restricciones de renderizado: el Complete HTML se renderiza con PhantomJS — sin flexbox, CSS Grid ni variables CSS. Consulta Restricciones del Renderizador .
Testing: verifica que cada opción de clausula se oculte/muestre correctamente y que la opción por defecto coincida con el value en config .
`clausula`
`value`
`config`

## Checklist de Validación ​
Antes de desplegar tu automatización, verifica:
Tienes los 3 archivos (Mask HTML, Complete HTML, JSON).
Cada pregunta en JSON tiene name , description y type .
`name`
`description`
`type`
Cada name en HTML coincide con una pregunta en el JSON — y viceversa.
`name`
Las preguntas clausula tienen un <span name="{name}_{value}"> por opción en el HTML.
`clausula`
`<span name="{name}_{value}">`
El value por defecto de una clausula en config coincide con el span sin el atributo hidden .
`value`
`clausula`
`config`
`hidden`
Las preguntas con prereq referencian preguntas de tipo clausula .
`prereq`
`clausula`
Cada firmante en signatureProfile tiene su <div id="X"> o <div name="X"> en el Complete HTML (nunca ambos).
`signatureProfile`
`<div id="X">`
`<div name="X">`
Las preguntas en sign referencian nombres de preguntas reales.
`sign`
Las preguntas de identificación de firmantes usan type: "identification" ; los NITs usan type: "nit" .
`type: "identification"`
`type: "nit"`
Las preguntas check usan un arreglo plano values: [...] (no options ).
`check`
`values: [...]`
`options`
El HTML no usa display: flex , CSS Grid ni variables CSS.
`display: flex`
Los caracteres UTF-8 ( ñ , á ) se escriben directamente, no como entidades HTML.
Si usas preBuild: true , agregaste preBuildData .
`preBuild: true`
`preBuildData`

## Ejemplo Completo Integrado ​

## JSON Completo ​
{ "name" : "Contrato de Compra-Venta" , "price" : 15000 , "preBuild" : false , "username" : "mi_empresa" , "sign" : [ "nombre_comprador" , "email_comprador" ] , "config" : [ { "name" : "nombre_comprador" , "description" : "Ingrese su nombre completo" , "type" : "name" } , { "name" : "tipo_identificacion" , "description" : "Seleccione su tipo de identificación" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de Extranjería" , "value" : "ce" } ] } , { "name" : "cedula_numero" , "description" : "Ingrese su número de identificación" , "type" : "number" , "prereq" : [ { "k" : "tipo_identificacion" , "v" : "cc" } ] } , { "name" : "cedula_extranjeria" , "description" : "Ingrese su número de cédula de extranjería" , "type" : "number" , "prereq" : [ { "k" : "tipo_identificacion" , "v" : "ce" } ] } , { "name" : "email_comprador" , "description" : "Ingrese su correo electrónico" , "type" : "email" } , { "name" : "telefono_comprador" , "description" : "Ingrese su número telefónico" , "type" : "phone" } , { "name" : "valor_transaccion" , "description" : "Ingrese el valor total de la compra" , "type" : "currency" } , { "name" : "fecha_transaccion" , "description" : "Seleccione la fecha de la transacción" , "type" : "date" } , { "name" : "descripcion_producto" , "description" : "Describa brevemente el producto" , "type" : "text" } ] , "signatureProfile" : [ { "name" : "nombre_comprador" , "identification" : "cedula_numero|cedula_extranjeria" , "email" : "email_comprador" , "phone" : "telefono_comprador" , "type" : "comprador" } ] }

## Mask HTML ​
<! DOCTYPE html > < html lang = " es " > < head > < meta charset = " UTF-8 " /> < title > Contrato de Compra-Venta </ title > < style > body { font-family : Arial , sans-serif ; max-width : 800 px ; margin : 40 px auto ; padding : 20 px ; } .section { margin-bottom : 30 px ; padding : 15 px ; border : 1 px solid #ddd ; border-radius : 5 px ; } h1 { text-align : center ; color : #333 ; } label { font-weight : bold ; display : block ; margin-bottom : 5 px ; } span { border-bottom : 1 px solid #000 ; min-width : 200 px ; display : inline-block ; padding : 5 px ; } </ style > </ head > < body > < h1 > Contrato de Compra-Venta </ h1 > < div class = " section " > < h2 > Información del Comprador </ h2 > < label > Nombre Completo: </ label > < span name = " nombre_comprador " > ___________________ </ span > < label > Tipo de Identificación: </ label > < span name = " tipo_identificacion_cc " > C.C. </ span > < span name = " tipo_identificacion_ce " hidden > C.E. </ span > < label > Número de Identificación: </ label > < span name = " cedula_numero " > ___________________ </ span > < span name = " cedula_extranjeria " hidden > ___________________ </ span > < label > Correo Electrónico: </ label > < span name = " email_comprador " > ___________________ </ span > < label > Teléfono de Contacto: </ label > < span name = " telefono_comprador " > ___________________ </ span > </ div > < div class = " section " > < h2 > Información de la Transacción </ h2 > < label > Descripción del Producto: </ label > < span name = " descripcion_producto " > ___________________ </ span > < label > Valor Total: </ label > < span name = " valor_transaccion " > ___________________ </ span > < label > Fecha de Transacción: </ label > < span name = " fecha_transaccion " > ___________________ </ span > </ div > < p style = " margin-top : 50 px ; text-align : center ; " > Firma del Comprador: ______________________ </ p > </ body > </ html >

## Complete HTML ​
<! DOCTYPE html > < html lang = " es " > < head > < meta charset = " UTF-8 " /> < title > Contrato de Compra-Venta </ title > < style > body { font-family : Arial , sans-serif ; max-width : 800 px ; margin : 40 px auto ; padding : 20 px ; } .sign-margin { min-height : 100 px ; margin-top : 30 px ; page-break-inside : avoid ; } </ style > </ head > < body > < h1 > Contrato de Compra-Venta </ h1 > < h2 > Información del Comprador </ h2 > < p > Nombre: < strong > < span name = " nombre_comprador " > ___________________ </ span > </ strong > </ p > < p > Identificación: < strong > < span name = " cedula_numero " > ___________________ </ span > < span name = " cedula_extranjeria " hidden > ___________________ </ span > </ strong > </ p > < p > Correo: < strong > < span name = " email_comprador " > ___________________ </ span > </ strong > </ p > < h2 > Información de la Transacción </ h2 > < p > Producto: < strong > < span name = " descripcion_producto " > ___________________ </ span > </ strong > </ p > < p > Valor: < strong > < span name = " valor_transaccion " > ___________________ </ span > </ strong > </ p > < p > Fecha: < strong > < span name = " fecha_transaccion " > ___________________ </ span > </ strong > </ p > < h2 > Firma </ h2 > < div id = " comprador " class = " sign-margin " > </ div > </ body > </ html >
Flujo General
Configuración
Tips y Mejores Prácticas
Checklist de Validación
Ejemplo Completo Integrado JSON Completo Mask HTML Complete HTML
JSON Completo
Mask HTML
Complete HTML