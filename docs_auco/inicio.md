# Un proceso de Auco,de principio a fin

> Fuente: https://docs.auco.ai/

API v1.5 · SDK web

## Un proceso de Auco, de principio a fin
Firma electrónica, validación de identidad y automatización de documentos. Acá está el API REST y el SDK web que los conectan con tu producto.
`curl -X POST https://api.auco.ai/v1.5/ext/document/save \ -H "Authorization: prk_tuLlavePrivada" \ -H "Content-Type: application/json" \ -d '{ "email" : "ana@empresa.co" , "document" : "64823dc5ce28a265e02d68f3" , "name" : "Contrato laboral" , "sign" : true, "notification" : false }'`
`await fetch( 'https://api.auco.ai/v1.5/ext/document/save' , { method: 'POST' , headers: { 'Authorization' : 'prk_tuLlavePrivada' , 'Content-Type' : 'application/json' , }, body: JSON.stringify( { email: 'ana@empresa.co' , document: '64823dc5ce28a265e02d68f3' , name: 'Contrato laboral' , sign: true, notification: false, }), });`
`import requests requests.post( "https://api.auco.ai/v1.5/ext/document/save" , headers= { "Authorization" : "prk_tuLlavePrivada" }, json= { "email" : "ana@empresa.co" , "document" : "64823dc5ce28a265e02d68f3" , "name" : "Contrato laboral" , "sign" : True, "notification" : False, }, )`
`{ "document" : "DOCUMENTCODE" , "signProfile" : [ { "id" : "ZR" , "email" : "example@auco.ai" } ] }`
Prueba sin cobros en stage
Llave pública para leer, privada para escribir
Escucha los eventos de tus procesos

## Así se ve una integración

## Creas el proceso
Con una plantilla o tu propio PDF, y la lista de firmantes.

## Firman y se validan
Embebido en tu web o desde el enlace que envía Auco.

## Te avisamos
Cada cambio de estado llega a tu endpoint en tiempo real.

## Descargas y auditas
Documento firmado y trazabilidad completa del proceso.

## ¿Qué necesitas hacer?

## Firmar un documento
Crea el proceso, define dónde firma cada quien y envíalo.
POST Crear desde plantilla
POST Cargar tu propio PDF
GET Consultar el proceso
GET Trazabilidad

## Validar una identidad
Biometría facial, cotejo documental y listas restrictivas.
POST Crear validación
POST Validación biométrica
POST Antecedentes
GET Consultar el resultado

## Recibir eventos
Configura tu webhook y escucha cada fase del proceso.
PUT Configurar el webhook
evento Eventos de un proceso
evento Eventos de un paquete
evento Eventos de AucoFace