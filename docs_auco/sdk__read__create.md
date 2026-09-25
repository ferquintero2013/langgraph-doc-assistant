# sdk/read/create

> Fuente: https://docs.auco.ai/sdk/read/create

La funcionalidad de Creación de procesos de lectura permite crear procesos de lectura de documentos, ya sean procesos privados en los que solo un grupo selecto de personas puede acceder al documento o documentos públicos en los que cualquier persona con el enlace puede acceder al documento.
Estos procesos de lectura temporizan la interacción del usuario con el documento para reportar los tiempos de lectura de cada página al creador.

## Ejemplo de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'read' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;`
Ejemplo de integración