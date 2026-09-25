# sdk/upload/attachments

> Fuente: https://docs.auco.ai/sdk/upload/attachments

La funcionalidad de Carga de Documentos con Anexos permite la integración de documentos principales junto con archivos adicionales que actúan como anexos dentro del mismo flujo de firma, así como solicitar documentos adjuntos sin necesidad de un documento principal.

## Ejemplo de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos

## Integración básica ​
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'attachments' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT === 'dev' ? 'DEV' : 'PROD' , } ) ;`

## Integración con firmantes precargados ​
Sigue el siguiente enlace para ver la referencia de los países y tipos de documentos aceptados 👉🏻 Documentos y paises
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'attachments' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { users : [ { name : 'Firmante #1' ; email : 'firmante@auco.ai' ; phone : '+573151234567' ; country : 'CO' ; identification : '1234567890' ; identificationType : 'CC' ; } ] , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT === 'dev' ? 'DEV' : 'PROD' , } ) ;
Ejemplo de integración Integración básica Integración con firmantes precargados
Integración básica
Integración con firmantes precargados