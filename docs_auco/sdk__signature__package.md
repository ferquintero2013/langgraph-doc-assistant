# sdk/signature/package

> Fuente: https://docs.auco.ai/sdk/signature/package

El SDK de firma de paquetes permite completar procesos de firma electrónica de varios documentos agrupados en un único flujo, asegurando que sea la misma validación de identidad para todos los documentos incluídos. Esta solución está diseñada para casos en los que se requiere firmar múltiples archivos de manera conjunta, manteniendo la integridad y coherencia del paquete.
Las validaciones del proceso de firma son configuradas en el momento de la creación del proceso, por lo que no pueden ser modificadas ni sobreescritas en la integración del SDK.

## Ejemplo de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'sign' , language : 'es' , // Lenguajes aceptados 'es' | 'en' events : { onSDKReady , onSDKClose , } , sdkData : { document : 'WO0J4L3YWBWE' , // Código del proceso pendiente de firma signFlow : 'package' , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT === 'dev' ? 'DEV' : 'PROD' , } ) ;`
Cada firmante tiene un id de 2 carácteres que lo identifica, en la integración se debe especificar el código de documento concatenado con este id de la siguiente manera:
Código del documento: WO0J4L3YWB
ID de firmante: WE
Codigo de integración: WO0J4L3YWB WE
Ejemplo de integración