# api/manager/validations

> Fuente: https://docs.auco.ai/api/manager/validations

Combinaciones y Estrategias por Firmante
Al generar un proceso de firma , es fundamental comprender las diferentes combinaciones posibles de validaciones de identidad, así como las estrategias que permiten aplicarlas de forma global o individual por firmante .
Para estructurar dichas validaciones existen reglas que debes tener en cuenta para asegurar que el proceso funcione correctamente.

## 1. Tipos de validaciones disponibles ​
Las validaciones de identidad que puedes combinar en un proceso incluyen:
PARAMETROS: Validación | Tipo | Requerido | Descripción ;; camera | Boolean | Opcional | Solicita una foto del rostro del firmante. ;; otpCode | Boolean | Opcional | Solicita código de verificación. ;; options.camera | String | Condicional | Si quieres cotejar la foto del rostro con el ID del firmante debes enviar en este campo 'identification' , o si quieres solo la foto del participante , enviar 'photo' . ;; options.otpCode | String | Condicional | Este campo acepta los valores 'phone' e 'email' . para indicar por qué medio recibirá el código de firmante en caso de enviar otpCode en true en la base de la data. ;; options.whatsapp | Boolean | Condicional | Envíe este campo en true sólo si desea que el flujo de firma de este firmante se desarrolle a través de WhatsApp, por defecto es false . ;; options.both | Boolean | Condicional | Envíe este campo en true sólo si desea que el flujo de firma de este firmante se desarrolle a través de WhatsApp y correo electrónico , por defecto es false . ;; options.identificationCardBack | Boolean | Condicional | Envíe este campo en true sólo si desea que la validación de identidad adicionalmente solicite la parte posterior del documento solo disponible para WhatsApp .
Aquí puedes ver la lista de países y documentos de identidad que aceptamos
`both`
both no es un parámetro de primer nivel: no existe en la raíz de la petición ni como signProfile[x].both . Solo existe anidado como options.both (o signProfile[x].options.both para validaciones individuales).
`both`
`signProfile[x].both`
`options.both`
`signProfile[x].options.both`

## 2. Validaciones globales e individuales ​
Puedes aplicar las validaciones de dos maneras:
Globales: en la raíz de la petición. Se aplican automáticamente a todos los firmantes.
Individuales: en el objeto signProfile[x], para validar a cada firmante de forma personalizada.
Las validaciones individuales tienen prioridad sobre las globales cuando se declaran ambas.
La creación de paquetes ( POST /document/many ) no tiene soporte para validaciones individuales por firmante : las validaciones se toman únicamente de la raíz de la petición y aplican a todos los participantes del paquete. Lo descrito en esta sección sobre validaciones individuales no aplica a ese endpoint.
`POST /document/many`
Si un signProfile[x] define cualquiera de estos campos: camera , otpCode u options , ese firmante deja de heredar las validaciones globales por completo, incluso para los campos que no incluyó . Los campos que falten en ese signProfile[x] se resuelven como false (para camera / otpCode ) o como objeto vacío (para options ), sin importar lo que digan las validaciones globales.
`signProfile[x]`
`camera`
`otpCode`
`options`
`signProfile[x]`
`false`
`camera`
`otpCode`
`options`
Ejemplo: si en la raíz envías "camera": true pero un firmante individual solo define "options": { "otpCode": "email" } (sin incluir "camera": true en ese mismo signProfile[x] ), ese firmante terminará con camera: false , aunque la validación global lo tenga en true .
`"camera": true`
`"options": { "otpCode": "email" }`
`"camera": true`
`signProfile[x]`
`camera: false`
`true`
Si quieres que un firmante mantenga una validación global y solo personalice otra, debes repetir explícitamente cada campo relevante ( camera , otpCode ) dentro de ese mismo signProfile[x] .
`camera`
`otpCode`
`signProfile[x]`

## 3. Reglas clave ​
options.camera = 'identification' activa comparación biométrica, pero solo funcionará si el firmante tiene identification , country e identificationType definidos.
`options.camera = 'identification'`
options.both = true indica que el firmante debe recibir notificaciones por correo y WhatsApp al mismo tiempo, para que sea efectivo: options.whatsapp = true .
`options.both = true`
`options.whatsapp = true`
options.camera y options.otpCode solo son válidos si, en ese mismo nivel (raíz o dentro del mismo signProfile[x] ), existe camera: true u otpCode: true respectivamente. Por ejemplo, signProfile[x].options.camera requiere signProfile[x].camera: true en ese mismo firmante; no basta con que camera esté en true a nivel global. Si declaras options.camera u options.otpCode sin su contraparte booleana en ese mismo nivel, el proceso no será válido .
`options.camera`
`options.otpCode`
`signProfile[x]`
`camera: true`
`otpCode: true`
`signProfile[x].options.camera`
`signProfile[x].camera: true`
`camera`
`true`
`options.camera`
`options.otpCode`
Las validaciones individuales sobrescriben por completo a las globales para ese firmante: si un signProfile[x] declara camera , otpCode u options , cualquier campo no incluido en ese mismo signProfile[x] se resuelve como false (o {} para options ), sin heredar el valor global. Ver advertencia en la sección 2.
`signProfile[x]`
`camera`
`otpCode`
`options`
`signProfile[x]`
`false`
`options`

## 4. Ejemplos: ​

## Validaciones globales: ​
`{ ... , "camera" : true , "otpCode" : true , "options" : { "camera" : "identification" , "otpCode" : "email" , } "signProfile" : [ { "name" : "Firmante 1" , "email" : "example@auco.ai" , "phone" : "+573000000000" , "identification" : "123456789" , "identificationType" : "CC" , "country" : "CO" } , { "name" : "Firmante 2" , "email" : "example2@auco.ai" , "phone" : "+573000000000" , "identification" : "123456789" , "identificationType" : "CC" , "country" : "CO" } ] , ... }`

## Validaciones individuales: ​
`{ ... , "signProfile" : [ { "name" : "Firmante 1" , "email" : "example@auco.ai" , "phone" : "+573000000000" , "camera" : true , "otpCode" : true , "identification" : "123456789" , "identificationType" : "CC" , "country" : "CO" "options" : { "camera" : "identification" , "whatsapp" : true , "otpCode" : "email" } } ] , ... }`
1. Tipos de validaciones disponibles
2. Validaciones globales e individuales
3. Reglas clave
4. Ejemplos: Validaciones globales: Validaciones individuales:
Validaciones globales:
Validaciones individuales: