# api/template/html

> Fuente: https://docs.auco.ai/api/template/html

Referencia completa para la estructura HTML de las plantillas de Auco — marcadores de posición, ubicación de firmas, campos automáticos y restricciones del renderizador.

## Estructura Básica de Campos ​
Cada campo del formulario se representa con un elemento que tiene un atributo name único:
`name`
`< span name = " pregunta_1 " > ___________ </ span >`
¿Cómo funciona?
El SDK detecta los elementos HTML con atributo name .
`name`
Busca la pregunta correspondiente en el JSON según el name .
`name`
Reemplaza el contenido del elemento con el valor que ingresa el usuario.
El contenido inicial ( ___________ arriba) es solo un marcador y será sobrescrito. Puedes usar guiones bajos, guiones o dejarlo vacío — elige lo que se vea mejor en una vista previa.
`___________`

## Campos de Cláusula (Visibilidad Condicional) ​
Para preguntas de tipo clausula , crea un <span> por cada opción en el HTML, usando el patrón de nombres {nombre_pregunta}_{valor_opcion} :
`clausula`
`<span>`
`{nombre_pregunta}_{valor_opcion}`
`< span name = " tipo_documento_cedula " > Cédula </ span > < span name = " tipo_documento_cedula_extranjeria " hidden > Cédula de Extranjería </ span > < span name = " tipo_documento_pasaporte " hidden > Pasaporte </ span >`
El span que coincide con el value por defecto de la pregunta en la configuración JSON no debe tener hidden . Todos los demás spans de opciones deben tener hidden . El SDK alterna la visibilidad a medida que el usuario selecciona opciones distintas.
`value`
`hidden`

## Ubicación de Firmas ​
En el Complete HTML , coloca un <div> con la clase sign-margin donde va cada firma. Hay dos formas de referenciar a un firmante — elige una por firmante y sé consistente :
`<div>`
`sign-margin`

## Opción A — Firma en una sola ubicación ​
Si un firmante firma en un solo lugar, usa id :
`< div id = " comprador " class = " sign-margin " > </ div >`
El id debe coincidir con el valor type en signatureProfile .
`type`
`signatureProfile`

## Opción B — Firmas en múltiples ubicaciones ​
Si el mismo firmante firma en varios lugares del documento, usa name en cada ocurrencia, y no uses id en ninguna parte para ese firmante:
`name`
`<!-- Página 1 --> < div name = " comprador " class = " sign-margin " > </ div > <!-- Página 5 --> < div name = " comprador " class = " sign-margin " > </ div > <!-- Página 12 --> < div name = " comprador " class = " sign-margin " > </ div >`
`name`
Si existe un <div id="comprador"> en cualquier parte del documento, todos los <div name="comprador"> serán ignorados silenciosamente por el renderizador. Elige la Opción A o la Opción B por firmante — nunca ambas.
`<div id="comprador">`
`<div name="comprador">`

## Campos Automáticos al Finalizar la Firma ​
La plataforma rellena automáticamente dos valores reservados de name cuando el documento queda completamente firmado. Agrégalos donde tengan sentido:
`name`

## signDate — se rellena con la fecha de firma ​
`signDate`
`< p > Firmado el < span name = " signDate " > ________ </ span > </ p >`
Cuando el documento se sella, este span se reemplaza con la fecha actual en formato DD de mes de YYYY (localizado).
`DD de mes de YYYY`

## signComplete — muestra un sello/confirmación tras la firma ​
`signComplete`
`< span name = " signComplete " hidden > Documento firmado y verificado </ span >`
Este elemento permanece oculto mientras el documento sigue siendo diligenciado o firmado. Una vez que todos los firmantes han completado su firma, se remueve su atributo hidden para que el contenido se vuelva visible.
`hidden`
No agregues signDate ni signComplete como preguntas en la configuración JSON. Son nombres reservados manejados enteramente por el runtime.
`signDate`
`signComplete`

## Restricciones del Renderizador (PhantomJS) ​
El Complete HTML se renderiza a PDF usando PhantomJS , que tiene un motor CSS limitado. Usar funciones no soportadas resultará en layouts rotos.

## ❌ NO usar ​
display: flex , flex-direction , flex-wrap , ni ninguna propiedad de flexbox
`display: flex`
`flex-direction`
`flex-wrap`
display: grid , grid-template-* , ni ninguna propiedad de CSS Grid
`display: grid`
`grid-template-*`
Propiedades personalizadas de CSS / variables: var(--x)
`var(--x)`
Consultas @media (soporte limitado)
`@media`
Unidades de layout modernas como vw , vh , dvh , cqw
`dvh`
`cqw`

## ✅ Alternativas seguras ​
display: block , display: inline-block , display: table , display: table-cell
`display: block`
`display: inline-block`
`display: table`
`display: table-cell`
float: left / float: right para layouts en columnas
`float: left`
`float: right`
position: absolute / relative para ubicación precisa
`position: absolute`
`relative`
Elementos HTML <table> para layouts complejos de varias columnas
`<table>`
style="..." inline o un bloque <style> en el <head>
`style="..."`
`<style>`
`<head>`
Familias de fuentes seguras para web: Arial, Helvetica, Times New Roman, Georgia

## ✅ Codificación ​
Define <meta charset="UTF-8"> en el <head>
`<meta charset="UTF-8">`
`<head>`
Escribe caracteres acentuados directamente ( á , é , ñ ) — no uses entidades HTML ( &aacute; , &ntilde; )
`&aacute;`
`&ntilde;`

## Principio del Documento Continuo ​
El Complete HTML se renderiza como un flujo continuo , no como una réplica página por página de un documento de origen.
PARAMETROS: Hacer | No hacer ;; Tratar el contenido como una única secuencia larga | Dividir el contenido según las páginas de un PDF original ;; Incluir encabezado/logo una sola vez al inicio | Repetir encabezados en cada página ;; Incluir pie de página una sola vez si aporta contenido real | Repetir pies de página en cada página ;; Dejar que el renderizador maneje los saltos de página | Insertar <div style="page-break-after: always"> ;; Omitir por completo contadores tipo "Página N de M" | Incluir paginaciones como "Pág. 1 de 4"
El CSS manual de salto de página ( page-break-before , page-break-after ) rara vez es necesario y con frecuencia produce peores layouts que dejar al renderizador decidir. Usar con moderación.
`page-break-before`
`page-break-after`

## Ejemplo Completo Básico ​
< div class = " form-container " > < h1 > Formulario de Compra </ h1 > <!-- Campo simple --> < p > Nombre del Comprador: < span name = " nombre_comprador " > ___________ </ span > </ p > <!-- Campo de email --> < p > Correo Electrónico: < span name = " email_comprador " > ___________ </ span > </ p > <!-- Campo de monto --> < p > Valor Total: < span name = " monto_total " > ___________ </ span > </ p > <!-- Cláusula con opciones --> < p > Tipo de Documento: < span name = " tipo_doc_cedula " > Cédula </ span > < span name = " tipo_doc_cedula_extranjeria " hidden > Cédula de Extranjería </ span > </ p > <!-- Ubicación de firma --> < h2 > Firma </ h2 > < div id = " comprador " class = " sign-margin " > </ div > <!-- Fecha automática de firma --> < p > Firmado el < span name = " signDate " > ________ </ span > </ p > </ div >
Para un ejemplo completo de extremo a extremo que cubre Mask HTML, Complete HTML y JSON, consulta la Introducción .
Estructura Básica de Campos
Campos de Cláusula (Visibilidad Condicional)
Ubicación de Firmas Opción A — Firma en una sola ubicación Opción B — Firmas en múltiples ubicaciones
Opción A — Firma en una sola ubicación
Opción B — Firmas en múltiples ubicaciones
Campos Automáticos al Finalizar la Firma signDate — se rellena con la fecha de firma signComplete — muestra un sello/confirmación tras la firma
signDate — se rellena con la fecha de firma
`signDate`
signComplete — muestra un sello/confirmación tras la firma
`signComplete`
Restricciones del Renderizador (PhantomJS) ❌ NO usar ✅ Alternativas seguras ✅ Codificación
❌ NO usar
✅ Alternativas seguras
✅ Codificación
Principio del Documento Continuo
Ejemplo Completo Básico