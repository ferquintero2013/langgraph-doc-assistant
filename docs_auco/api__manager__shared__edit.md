# api/manager/shared/edit

> Fuente: https://docs.auco.ai/api/manager/shared/edit

`/{resource}/edit`
`prk _`
Con este servicio puedes poner un proceso en estado de edición para volver a enviarlo con cambios: reemplazar el PDF, corregir los datos de un contrato, o agregar y quitar documentos de un paquete.
La edición son dos pasos. Primero marcas el proceso con este servicio, y luego lo sobreescribes reenviando el payload completo al servicio de creación que corresponda. El proceso conserva su identificador.
{resource} indica qué estás editando y acepta dos valores:
`{resource}`
PARAMETROS: Recurso | Qué edita | Identificador ;; document | Un documento o un contrato | code de 9 o 10 caracteres ;; package | Un paquete y todos sus documentos | package de 24 caracteres
Poner un proceso en edición reinicia las firmas . Se descartan las firmas ya recolectadas, las validaciones de identidad y los enlaces enviados a los participantes. Al reenviarlo se notifica de nuevo a todos con enlaces nuevos.
No hay forma de cancelar la edición: un proceso marcado queda a la espera de que lo reenvíes.

## Autenticación ​
Incluye tu llave privada en el encabezado Authorization .
`Authorization`
`Authorization : prk_xxx...`

## Marcar el proceso ​

## Parámetros ​
PARAMETROS: Nombre | Tipo | Descripción ;; code | String condicional | Código del documento o contrato. Solo para /document/edit . ;; package | String condicional | Identificador del paquete, 24 caracteres. Solo para /package/edit .

## Requisitos del proceso ​
Solo puedes editar un proceso que no esté firmado, rechazado, expirado ni ya en edición. Un contrato debe estar además en estado aprobado.
Un documento que pertenece a un paquete no se edita por separado: edita el paquete completo.
curl
Python
Node.js
`curl -- location 'https://api.auco.ai/v1.5/ext/package/edit' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "package" : "6a95b55966dd1c779500b962" } '`
`import requests import json url = "https://api.auco.ai/v1.5/ext/package/edit" payload = json . dumps ( { "package" : "6a95b55966dd1c779500b962" } ) headers = { 'Authorization' : 'prk_private_key_company' , 'Content-Type' : 'application/json' } response = requests . request ( "POST" , url , headers = headers , data = payload ) print ( response . text )`
`const axios = require ( 'axios' ) ; let data = JSON . stringify ( { package : '6a95b55966dd1c779500b962' , } ) ; let config = { method : 'post' , maxBodyLength : Infinity , url : 'https://api.auco.ai/v1.5/ext/package/edit' , headers : { Authorization : 'prk_private_key_company' , 'Content-Type' : 'application/json' , } , data : data , } ; axios . request ( config ) . then ( ( response ) => { console . log ( JSON . stringify ( response . data ) ) ; } ) . catch ( ( error ) => { console . log ( error ) ; } ) ;`

## Respuesta ​
`{ "message" : "PACKAGE_MODIFIED" }`
Para un documento la respuesta es DOCUMENT_MODIFIED .
`DOCUMENT_MODIFIED`

## Consultar el proceso en edición ​
`/{resource}/edit`
`prk _`
Devuelve el proceso marcado, con enlaces de descarga de sus PDFs vigentes por 5 minutos. Sirve para inspeccionar lo que está en edición; el payload que reenvías es el tuyo.
PARAMETROS: Nombre | Tipo | Descripción ;; code | String condicional | Código del documento o contrato. Solo para /document/edit . ;; package | String condicional | Identificador del paquete. Solo para /package/edit .
`curl -- location 'https://api.auco.ai/v1.5/ext/package/edit?package=6a95b55966dd1c779500b962' \ -- header 'Authorization: prk_private_key_company'`
Un paquete devuelve sus datos y el detalle de cada documento en documents :
`documents`
`{ "name" : "Contratos de arrendamiento" , "subject" : "Firma de contratos" , "message" : "Por favor firma los documentos adjuntos" , "signers" : [ { "name" : "Luz Marina López" , "email" : "luz@example.com" , "status" : "pending" } ] , "documents" : [ { "code" : "CRSD8I9AJ1" , "name" : "Contrato de arrendamiento" , "url" : "https://documents.auco.ai/..." , "signProfile" : [ { "name" : "Luz Marina López" , "email" : "luz@example.com" } ] } ] }`

## Sobreescribir el proceso ​
Una vez marcado, reenvía el proceso al servicio de creación con su identificador. El payload es el mismo de una creación normal, más un campo:
PARAMETROS: Proceso | Servicio | Campo del identificador ;; Documento o contrato | Cargar PDF o Crear desde plantilla | code ;; Paquete | Crear paquete | package
Lo que no reenvíes se borra. Si omites folder el proceso se mueve a la raíz, y si omites tags se quedan sin etiquetas. Reenvía el payload completo, no solo lo que cambió.
`folder`
`tags`
Se conservan el identificador y la fecha de creación.
En un paquete, los documentos del envío anterior se eliminan y se generan códigos nuevos: por eso puedes agregar y quitar archivos libremente. Los créditos del paquete anterior se reintegran y se cobran los del nuevo, así que terminas pagando la cantidad final de documentos.
Los id de los firmantes que Auco no notifica también se generan de nuevo al sobreescribir, en documentos y en paquetes. Los accesos que hayas repartido con los anteriores dejan de servir: toma los nuevos de la respuesta o consúltalos con GET /document .
`GET /document`
`curl -- location 'https://api.auco.ai/v1.5/ext/document/many' \ -- header 'Authorization: prk_private_key_company' \ -- header 'Content-Type: application/json' \ -- data - raw ' { "package" : "6a95b55966dd1c779500b962" , "email" : "manager@auco.ai" , "name" : "Contratos de arrendamiento" , "documents" : [ { "name" : "Contrato de arrendamiento" , "signProfile" : [ { "name" : "Luz Marina López" , "email" : "luz@example.com" , "type" : "signature" } ] } ] } '`

## Errores ​
PARAMETROS: Mensaje | Causa ;; DOCUMENT_NOT_FOUND | El documento no existe, no es de tu organización, o no está en un estado editable ;; PACKAGE_NOT_FOUND | Lo mismo para un paquete. Al sobreescribir, también si el paquete no está marcado para edición ;; PACKAGE_ID_INVALID | El identificador del paquete no tiene 24 caracteres hexadecimales ;; INVALID_RESOURCE | El {resource} de la ruta no es document ni package
Autenticación
Marcar el proceso Parámetros Requisitos del proceso Respuesta
Parámetros
Requisitos del proceso
Respuesta
Consultar el proceso en edición
Sobreescribir el proceso
Errores