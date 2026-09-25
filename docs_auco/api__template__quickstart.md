# api/template/quickstart

> Fuente: https://docs.auco.ai/api/template/quickstart

Esta guía te lleva de cero a una plantilla firmable funcional. Al final vas a tener un contrato simple con un firmante que el SDK puede abrir, diligenciar y firmar.
Tu private key y public key de Auco (panel → Developers ).
curl o un cliente HTTP equivalente.
`curl`

## Paso 1 — Define el JSON ​
Una plantilla mínima necesita: tres preguntas (nombre, cédula, correo) y un firmante que las referencia.
{ "name" : "Mi Primera Plantilla" , "sign" : [ "nombre_firmante" , "cedula_firmante" , "correo_firmante" ] , "config" : [ { "name" : "nombre_firmante" , "description" : "Ingrese su nombre completo" , "type" : "name" } , { "name" : "cedula_firmante" , "description" : "Ingrese su cédula" , "type" : "identification" , "country" : "CO" } , { "name" : "correo_firmante" , "description" : "Ingrese su correo electrónico" , "type" : "email" } ] , "signatureProfile" : [ { "name" : "nombre_firmante" , "identification" : "cedula_firmante" , "email" : "correo_firmante" , "phone" : "correo_firmante" , "type" : "firmante" } ] }

## Paso 2 — Escribe el Mask HTML ​
El Mask HTML es lo que el usuario ve mientras diligencia el formulario. Un <span name="..."> por cada pregunta del JSON.
`<span name="...">`
`<! DOCTYPE html > < html lang = " es " > < head > < meta charset = " UTF-8 " /> < title > Mi Primera Plantilla </ title > </ head > < body > < h1 > Acuerdo Simple </ h1 > < p > Yo, < span name = " nombre_firmante " > _____ </ span > , identificado con < span name = " cedula_firmante " > _____ </ span > , confirmo mi identidad con el correo < span name = " correo_firmante " > _____ </ span > . </ p > </ body > </ html >`

## Paso 3 — Escribe el Complete HTML ​
El Complete HTML es lo que se imprime al PDF final. Mismos spans que Mask, más un <div class="sign-margin"> donde irá la firma.
`<div class="sign-margin">`
<! DOCTYPE html > < html lang = " es " > < head > < meta charset = " UTF-8 " /> < title > Mi Primera Plantilla </ title > </ head > < body > < h1 > Acuerdo Simple </ h1 > < p > Yo, < strong > < span name = " nombre_firmante " > _____ </ span > </ strong > , identificado con < strong > < span name = " cedula_firmante " > _____ </ span > </ strong > , confirmo mi identidad con el correo < strong > < span name = " correo_firmante " > _____ </ span > </ strong > . </ p > < p > Firmado el < span name = " signDate " > _____ </ span > . </ p > < div id = " firmante " class = " sign-margin " > </ div > </ body > </ html >
El id="firmante" del <div> debe coincidir con el type del signatureProfile del JSON.
`id="firmante"`
`<div>`
`type`
`signatureProfile`

## Paso 4 — Crea la plantilla ​
Envía el JSON a la API. La respuesta trae dos URLs firmadas (válidas 5 minutos ) donde subirás los HTMLs.
`curl -X POST https://api.auco.ai/v1.5/ext/template \ -H "Content-Type: application/json" \ -H "Authorization: tu_private_key" \ -d @plantilla.json`
Respuesta:
`{ "id" : "template_id" , "urls" : { "mask" : "https://...signed_mask" , "complete" : "https://...signed_complete" } }`
Guarda el id — lo usarás desde el SDK.

## Paso 5 — Sube los HTMLs ​
Ambos archivos se cargan como binarios con PUT a las URLs firmadas del paso anterior.
`PUT`
`curl -X PUT "https://...signed_mask" \ -H "Content-Type: text/html" \ --data-binary @mask.html curl -X PUT "https://...signed_complete" \ -H "Content-Type: text/html" \ --data-binary @complete.html`
Si las URLs expiran antes de subir, toca volver a llamar POST /template (no hay endpoint para regenerarlas).
`POST /template`

## Paso 6 — Pruébala desde el SDK ​
Con el id que recibiste, abre la plantilla en el SDK. Consulta la documentación del SDK para la integración completa.

## Siguientes pasos ​
Configuración JSON — los 17 tipos de pregunta, validaciones y condicionales.
Configuración del HTML — cláusulas condicionales, múltiples firmantes, campos automáticos como signDate .
`signDate`
Tipo Request — prellenar campos desde tu propio servicio.
Actualizar una plantilla — cambiar preguntas o HTML sin recrearla.
Paso 1 — Define el JSON
Paso 2 — Escribe el Mask HTML
Paso 3 — Escribe el Complete HTML
Paso 4 — Crea la plantilla
Paso 5 — Sube los HTMLs
Paso 6 — Pruébala desde el SDK
Siguientes pasos