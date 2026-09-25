# sdk/fill

> Fuente: https://docs.auco.ai/sdk/fill

El SDK de Llenado de plantillas permite la generación dinámica de documentos a partir de plantillas predefinidas con campos editables. Esta herramienta facilita la automatización de contenidos repetitivos como contratos, formularios o cartas, insertando datos específicos.

## Ejemplos de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos

## Integración básica, llenado de plantilla regular ​
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'fill' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { document : '67e714c96b3509c4bf2b44dd' , // ID de la plantilla a llenar uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;`

## Integración con referencia ​
El llenado con referencia estándariza al configuración validaciones y de plataforma de firma y permite que cualquier usuario cree el proceso y quedará asignado a la compañía dueña de la referencia.
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'fill' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { document : '67e714c96b3509c4bf2b44dd' , // ID de la plantilla a llenar reference : 'R3F3R3NC3' , // Referencia uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;`

## Edición de documento ​
La edición de un documento ya creado solo es posible si el documento no ha sido firmado.
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'fill' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { document : '67e714c96b3509c4bf2b44dd' , // ID de la plantilla a llenar code : 'D0CC0D3' , // Código del documento a editar uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;`

## Integración con prellenado ​
Si la plantilla que se va a llenar ya tuvo campos prellenados en el momento de la creación es necesario específicar el código del documento creado con prellenado e indicar que fue prellenado.
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'fill' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'puk_xxxxx' , // Llave pública de la compañía events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { document : '67e714c96b3509c4bf2b44dd' , // ID de la plantilla a llenar code : 'D0CC0D3' , // Código del documento prellenado preBuild : true , // Indica al SDK que debe cargar la parte final de la plantilla uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;
Ejemplos de integración Integración básica, llenado de plantilla regular Integración con referencia Edición de documento Integración con prellenado
Integración básica, llenado de plantilla regular
Integración con referencia
Edición de documento
Integración con prellenado