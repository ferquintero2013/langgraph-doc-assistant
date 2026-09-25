# sdk/read/doc-read

> Fuente: https://docs.auco.ai/sdk/read/doc-read

El SDK de lectura de documentos permite acceder a procesos de lectura de documentos y temporizar las interacciones del usuario con el documento para reportar los tiempos de lectura de cada página individualmente.
Este SDK tiene medidas de seguridad que prohiben el acceso al documento en caso de ser privado por medio de validación por código otp al método de distribución seleccionado al momento de la creación del proceso, ya sea WhatsApp o Correo electrónico.
Si el proceso es público cualquier persona podrá acceder al documento si tiene el enlace, el único paso necesario que el usuario debe completar antes de acceder a lectura es ingresar su correo electrónico, el cual lo identificará en las métricas de lectura.

## Ejemplo de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos
`import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'sign' , language : 'es' , // Lenguajes aceptados 'es' | 'en' events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { document : 'WO0J4L3YWB' , // Código del proceso de lectura signFlow : 'read' , email : 'lector@auco.ai' , // Opcional: Correo del lector si es necesario saltar el paso de validación OTP uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT === 'dev' ? 'DEV' : 'PROD' , } ) ;`
Si se configura el correo del lector en un proceso privado este será validado contra la lista de personas que tienen acceso, si se configura un correo de una persona que no tiene acceso al documento el SDK mostrará un mensaje de error y no podrá acceder
El campo de correo del lector está diseñado con el manejo de sesión en app.auco.ai en mente, por tanto, si se incluye el correo también es necesario configurar el evento de onSDKToken que deberá retornar un token válido del usuario
Ejemplo de integración