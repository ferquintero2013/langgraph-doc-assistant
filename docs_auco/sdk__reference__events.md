# sdk/reference/events

> Fuente: https://docs.auco.ai/sdk/reference/events

Al integrar cualquiera de los SDK es necesario configurar los eventos que se requiere para su funcionamiento, estos eventos están documentados a continuación:

## onSDKReady ​
Callback que se ejecuta cuando el SDK carga correctamente , al cargar el SDK correctamente se envía un mensage al iframe con la información de la integración

## Ejemplo de uso ​
`function onSDKReady ( ) { console . log ( 'SDK Inicializado correctamente' ) ; //.... }`

## onSDKClose ​
Callback que se ejecuta cuando el SDK es cerrado por finalización del flujo, no se ejecuta cuando se cierra forzosamente (Ej. Cerrando la pestaña).

## Ejemplo de uso ​
SDK-UPLOAD
SDK-SIGN
SDK-VALIDATION
`/** * @param { string } code - Código del documento creado. */ function onSDKClose ( code ) { console . log ( 'Documento creado:' , code ) ; //.... }`
`/** * @param { string } code - Código del documento creado, no se usa en sdk-sign. * @param { string } redirect - Enlace redirección al terminar proceso de firma. */ function onSDKClose ( code = "" , redirect ) { console . log ( 'Enlace recomendado de redirección:' , redirect ) ; window . open ( redirect ) //.... }`
`/** * @param { string } similarity - Porcentaje de similitud detectado en el proceso. * @param { string } status - Estado del proceso de validación. */ function onSDKClose ( similarity , status ) { console . log ( similarity , status ) ; //.... }`

## onSDKFinish ​
Este evento actualmente solo está disponible en SDK-SIGN .
Callback que se ejecuta cuando el usuario termina el proceso de firma exitosamente , pero antes de que se muestre la pantalla de finalización del SDK. Esto permite ejecutar lógica personalizada (como analytics, notificaciones o actualizaciones de estado) justo después de que la firma fue completada.

## Ejemplo de uso ​
`function onSDKFinish ( ) { console . log ( 'El usuario ha firmado exitosamente' ) ; // Ejecutar lógica antes de que se muestre la pantalla de finalización //.... }`

## onSDKToken ​
Si se incluye la keyPublic en la libreria de integración este evento no es llamado, aunque se recomienda incluirlo y retornar la string de la llave pública
Callback que se ejecuta cuando el SDK necesita token de autorización para extraer información del API.

## Ejemplo de uso ​
`/** * @returns Promise<string> - Esta función debe retornar una promesa que * resuelva la string de la llave de autenticación */ function onSDKToken ( ) { return new Promise ( ( resolve ) => { //.... resolve ( 'authKey' ) ; } ) ; }`
onSDKReady Ejemplo de uso
Ejemplo de uso
onSDKClose Ejemplo de uso
Ejemplo de uso
onSDKFinish Ejemplo de uso
Ejemplo de uso
onSDKToken Ejemplo de uso
Ejemplo de uso