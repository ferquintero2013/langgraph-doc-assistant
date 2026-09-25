# api/environment

> Fuente: https://docs.auco.ai/api/environment

Esta sección explica los entornos disponibles en Auco y cómo realizar la autenticación para consumir la API de forma segura.

## Versionado de la API ​
Todas las peticiones deben incluir la versión actual del API en la URL base. Actualmente usamos la versión v1.5 , con el sufijo /ext indicando endpoints para integraciones externas.
`v1.5`
`/ext`

## Entornos disponibles ​
Auco ofrece dos entornos diferenciados:

## 🔧 Entorno de pruebas (stage) ​
URL base: https://dev.auco.ai/v1.5/ext
`https://dev.auco.ai/v1.5/ext`
Pensado para realizar integraciones, pruebas y desarrollo.
No se generan cobros ni movimientos reales.
Puedes solicitar acceso creando una cuenta en stage.auco.ai .

## 🚀 Entorno de producción ​
URL base: https://api.auco.ai/v1.5/ext
`https://api.auco.ai/v1.5/ext`
Entorno en el que se ejecutan los flujos reales y se contabilizan los documentos firmados o enviados.
Requiere créditos activos y una cuenta configurada en producción.

## Autenticación ​
La API de Auco utiliza autenticación mediante dos tipos de claves: pública y privada . Estas claves deben ser incluidas en los encabezados de cada petición, dependiendo del tipo de operación:
Lectura (GET): usa la llave pública ( puk_... )
`puk_...`
Escritura (POST, PUT, DELETE): usa la llave privada ( prk_... )
`prk_...`

## 🔑 Cabecera requerida ​
`Authorization : TU_LLAVE_PUBLICA_O_PRIVADA`

## 📘 Ejemplo de uso en curl para lectura (GET) ​
`curl`
`curl -X GET https://dev.auco.ai/v1.5/ext/document \ -H "Authorization: puk_ocG0ODMlBlAN4NOi4GxVJjmC7Examaple" \ -H "Content-Type: application/json"`

## 📘 Ejemplo de uso en curl para escritura (POST) ​
`curl`
`curl -X POST https://dev.auco.ai/v1.5/ext/document/save \ -H "Authorization: prk_ocG0ODMlBlAN4NOi4GxVJjmC7Examaple" \ -H "Content-Type: application/json" \ -d '{ "name": "documento.pdf" }'`
Nota: Mantén tus llaves privadas seguras. Nunca las compartas públicamente ni las incluyas en clientes públicos como navegadores.

## Recomendaciones ​
Usa el entorno stage para todas tus pruebas iniciales antes de pasar a producción.
Asegúrate de usar la llave pública para GET y la llave privada para POST, PUT y DELETE .
Cambia la URL base y las llaves cuando pases al entorno de producción.
Protege tus llaves privadas: nunca las compartas públicamente ni las incluyas en clientes públicos (como navegadores o aplicaciones móviles).
Si automatizas procesos, considera mecanismos de rotación periódica de llaves.

## Código de error común ​
401 Unauthorized: No se incluyó una clave válida en la cabecera Authorization , o se usó una clave incorrecta para el tipo de operación (lectura/escritura).
`Authorization`
Versionado de la API
Entornos disponibles 🔧 Entorno de pruebas (stage) 🚀 Entorno de producción
🔧 Entorno de pruebas (stage)
🚀 Entorno de producción
Autenticación 🔑 Cabecera requerida 📘 Ejemplo de uso en curl para lectura (GET) 📘 Ejemplo de uso en curl para escritura (POST)
🔑 Cabecera requerida
📘 Ejemplo de uso en curl para lectura (GET)
`curl`
📘 Ejemplo de uso en curl para escritura (POST)
`curl`
Recomendaciones
Código de error común