# sdk/upload/documents

> Fuente: https://docs.auco.ai/sdk/upload/documents

La funcionalidad de Carga de Documentos para Firma permite integrar, a través del SDK, la subida segura de documentos que deben ser firmados electrónicamente.

## Ejemplos de integración ​
Para la integración es necesario tener un elemento <iframe id='iframeId'> donde se renderizará el SDK y a la funcion AucoSDK se le debe indicar el id de este elemento
`<iframe id='iframeId'>`
Sigue el siguiente enlace para ver la referencia de los eventos que se requieren en una integración de SDK 👉🏻 Eventos

## Integración básica ​
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;

## Integración con datos personalizados (custom) ​
El atributo custom permite enviar un objeto con información adicional personalizada dentro de sdkData . Este objeto se almacena en la base de datos asociado al proceso y se incluye en el payload del webhook si está configurado.
`custom`
`sdkData`
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , custom : { // (opcional) Objeto con datos personalizados, se guarda en BD y se envía en el webhook internalId : 'ORD-12345' , department : 'legal' , priority : 'high' , } , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;

## Integración con firmantes precargados (ESTABLE) ​
Este método será deprecado en un futuro, se recomienda utilizar el método detallado en el siguiente item.
Sigue el siguiente enlace para ver la referencia de los países y tipos de documentos aceptados 👉🏻 Documentos y paises
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , users : [ { name : 'Firmante' ; email : 'firmante@auco.ai' ; phone : '+573151234567' ; country : 'CO' ; identification : '1234567890' ; identificationType : 'CC' ; } ] , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : process . env . PUBLIC_ENVIRONMENT == 'dev' ? 'DEV' : 'PROD' , } ) ;

## Integración con firmantes precargados ​
Esta función solo está disponible desde v1.0.0 en adelante
Sigue el siguiente enlace para ver la referencia de los países y tipos de documentos aceptados 👉🏻 Documentos y paises
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , flowData : { type : 'participants' , participants : [ { id : 'id1' , type : 'signer' , name : 'Firmante' , email : 'firmante@auco.ai' , phone : '+573161979572' , country : 'CO' , identification : '123' , identificationType : 'CC' , locked : true , // Este participante no podrá ser editado ni eliminado disableAutoSign : true , // (opcional) Deshabilita la firma automática para este participante } , { id : 'id2' , type : 'approver' , name : 'Aprobador' , email : 'aprobador@auco.ai' , phone : '+573161979572' , country : 'CO' , identification : '1234' , identificationType : 'CC' , } , { id : 'id3' , type : 'reader' , name : 'Lector' , email : 'lector@auco.ai' , locked : true , // Este participante no podrá ser editado ni eliminado } , ] , } , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : 'DEV' , } ) ;

## Integración con flujo precargado ​
En este tipo de integración al abrir el SDK el usuario solo deberá posicionar las firmas
Esta función solo está disponible desde v1.0.0 en adelante
Sigue el siguiente enlace para ver la referencia de los países y tipos de documentos aceptados 👉🏻 Documentos y paises
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , flowData : { type : 'complete' , files : [ file1 , file2 ] , // Array de documentos a cargar (tipo File), Auco se encargará de unirlos en un solo PDF emailData : { name : 'Flujo precargado' , message : 'Mensaje' , subject : 'Sujeto' , expire : new Date ( ) , // (opcional) Fecha de expiración del flujo remember : '48' , // (opcional) Cada cuantas horas se enviará recordatorio notificationOff : true , // Auco no le enviará correos a los participantes } , platform : 'whatsapp' , // Plataforma donde se harán los procesos de firma ('auco' | 'whatsapp') validations : { otpCode : 'phone' , // (opcional) Medio por donde se enviará OTP  ('phone' | 'email') identification : true , // Validación de documento de identidad identificationCardBack : true , // Validación de documento de identidad trasero selfie : true , // Validación con foto del rostro } , participants : [ { id : 'id_1' , type : 'signer' , name : 'Firmante' , email : 'firmante@auco.ai' , phone : '+573151234567' , country : 'CO' , identificationType : 'CC' , identification : '1234' , disableAutoSign : true , // (opcional) Deshabilita la firma automática para este participante } , { id : 'id_2' , type : 'approver' , name : 'Aprobador' , email : 'aprobador@auco.ai' , phone : '+573151234567' , country : 'CO' , identificationType : 'CC' , identification : '1234' , } , { id : 'id_3' , type : 'reader' , email : 'lector@auco.ai' , name : 'Lector' , } , ] , } , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : 'DEV' , } ) ;

## Integración para edición básica ​
En este tipo de integración se puede editar un documento que aún no se ha firmado, la información del documento original será autocompletada
Esta función solo está disponible desde v1.0.3 en adelante
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , flowData : { type : 'edit' , code : 'CODEDOCUM' , keepPositions : true , // Opcional - Mantiene las posiciones de firma del documento original } , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : 'DEV' , } ) ;

## Integración para edición con sobreescritura ​
En este tipo de integración se puede editar un documento que aún no se ha firmado y sobreescribir la información del documento original en la integración
Esta función solo está disponible desde v1.0.3 en adelante
Si en la integración se sobreescribe toda la información del documento original (files, emailData, platform, validations y participants), al abrir el SDK el usuario solo deberá posicionar las firmas
import { AucoSDK } from 'auco-sdk-integration' ; const unsubscribe = AucoSDK ( { iframeId : 'iframeId' , sdkType : 'upload' , language : 'es' , // Lenguajes aceptados 'es' | 'en' keyPublic : 'prk_xxxxx' , // Llave privada de la compañía necesaria para la creación del proceso events : { onSDKReady , onSDKClose , onSDKToken , } , sdkData : { userAttributes : { email : 'admin@company.com' , // Email de usuario registrado en Auco, se recomienda usar el correo del admin de la compañía } , flowData : { type : 'edit' , code : 'CODEDOCUM' , files : [ file1 ] , // Opcional - Array de documentos (tipo File) a cargar emailData : { ... } , // Opcional - Configuración del correo y/o recordatorios platform : 'whatsapp' , // Opcional - Plataforma donde se harán la firma ('auco' | 'whatsapp') validations : { ... } , // Opcional - Validaciones participants : [ ... ] , // Opcional - Lista de participantes para sobreescribir los originales keepPositions : true , // Opcional - Mantiene las posiciones de firma del documento original } , uxOptions : { primaryColor : '#021c30' , alternateColor : '#a557f2' , } , } , env : 'DEV' , } ) ;
Ejemplos de integración Integración básica Integración con datos personalizados (custom) Integración con firmantes precargados (ESTABLE) Integración con firmantes precargados Integración con flujo precargado Integración para edición básica Integración para edición con sobreescritura
Integración básica
Integración con datos personalizados (custom)
Integración con firmantes precargados (ESTABLE)
Integración con firmantes precargados
Integración con flujo precargado
Integración para edición básica
Integración para edición con sobreescritura