# sdk/signature/approve

> Fuente: https://docs.auco.ai/sdk/signature/approve

El SDK de Aprobación de Documentos permite integrar flujos en los que un usuario debe revisar y aprobar o rechazar documentos con verificación de su identidad. Esta validación puede incluir métodos como OTP y/o validaciones biométricas, garantizando que solo usuarios autorizados puedan emitir aprobaciones válidas.
Las validaciones del proceso de aprobación son configuradas en el momento de la creación del proceso, por lo que no pueden ser modificadas ni sobreescritas en la integración del SDK.

## Ejemplo de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'sign' , language : 'es' , // Lenguajes aceptados 'es' | 'en' events : { onSDKReady , onSDKClose , } , sdkData : { document : 'WO0J4L3YWBWE' , // Código del proceso pendiente de firma signFlow : 'approve' , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT === 'dev' ? 'DEV' : 'PROD' , } ) ;`
Cada aprobador tiene un id de 2 carácteres que lo identifica, en la integración se debe especificar el código de documento concatenado con este id de la siguiente manera:
Código del documento: WO0J4L3YWB
ID de aprobador: WE
Codigo de integración: WO0J4L3YWB WE
Ejemplo de integración