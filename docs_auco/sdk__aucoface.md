# sdk/aucoface

> Fuente: https://docs.auco.ai/sdk/aucoface

El SDK de Validación de identidad permite ejecutar flujos de Aucoface de plataforma web para validar la identidad por medio de la verificación de documento de identidad y selfie del usuario.

## Ejemplos de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos

## Integración básica ​
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'validation' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía events : { onSDKReady , onSDKClose , } , sdkData : { document : 'WO0J4L3YWB' , // Código del proceso de validación uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;`
Ejemplos de integración Integración básica
Integración básica