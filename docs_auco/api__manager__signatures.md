# api/manager/signatures

> Fuente: https://docs.auco.ai/api/manager/signatures

Existen tres formas de definir la sposiciones de firma en Auco, puedes escoger la que mas se acomode a tus necesidades y facilidades.

## 1. Especificación de coordenadas ​
Puedes incluir el parámetro position dentro de cada objeto de signProfile para definir manualmente las coordenadas de la firma en el documento. Este parámetro debe ser un array de objetos, donde cada objeto representa una firma en una página específica.
Cada posición debe incluir las siguientes propiedades:
page : número de la página donde se ubicará la firma (comenzando desde 1).
x : posición horizontal relativa (entre 0 y 1), calculada como: (firmaX + anchoFirma) ÷ anchoPágina
`(firmaX + anchoFirma) ÷ anchoPágina`
y : posición vertical relativa (entre 0 y 1), calculada como: (firmaY + altoFirma) ÷ altoPágina
`(firmaY + altoFirma) ÷ altoPágina`
w : ancho de la firma en puntos (PDF units).
h : alto de la firma en puntos (PDF units).
`"signProfile" : [ { "name" : "Firmante 1" , "email" : "example@auco.ai" , "position" : [ { "page" : 1 , "x" : 0.65 , "y" : 0.80 , "w" : 150 , "h" : 50 } ] } ]`

## 2. Por medio de una plantilla en Auco ​
Si trabajas con un documento PDF estándar donde la ubicación de las firmas no cambia, puedes crear una plantilla en Auco con la ayuda de uno de nuestros asesores. Esta plantilla almacenará las posiciones de firma asociadas a tipos de firmantes predefinidos (por ejemplo: gerente, candidato, etc.).
Una vez creada la plantilla, solo necesitas referenciar su identificador mediante el campo document y especificar los firmantes usando el campo type correspondiente. Esto simplifica el proceso y evita definir manualmente las coordenadas de firma.
`{ "document" : "TEMPLATE_ID" , // ID de la plantilla que contiene las posiciones de firma "signProfile" : [ { "type" : "gerente" , // Tipo de firmante definido en la plantilla "name" : "Firmante 1" , "email" : "example@auco.ai" , "phone" : "+573123456789" } , { "type" : "candidato" , // Otro tipo de firmante definido en la plantilla "name" : "Firmante 2" , "email" : "example@auco.ai" , "phone" : "+573123456789" } ] }`

## 3. Uso de tags de firma en el documento PDF ​
Auco permite posicionar firmas directamente dentro del contenido del PDF mediante etiquetas (tags) especiales. Esta funcionalidad está disponible únicamente cuando se envía el documento PDF codificado en Base64 dentro de la petición (campo file).

## ¿Cómo funciona? ​
En el documento PDF, debes insertar el tag {{signature:signerPosition}} donde deseas que aparezca la firma.
`{{signature:signerPosition}}`
signerPosition corresponde a la posición del firmante en el array signProfile. Por ejemplo, {{signature:0}} insertará la firma del primer firmante, {{signature:1}} la del segundo, y así sucesivamente.
`{{signature:0}}`
`{{signature:1}}`
En la petición, cada objeto del array signProfile debe incluir el parámetro "label": true para activar el uso del tag en lugar de coordenadas manuales (position).
`{ "file" : "base64-encoded-pdf" , "signProfile" : [ { "name" : "Firmante 1" , "email" : "example@auco.ai" , "phone" : "+573123456789" , "label" : true } , { "name" : "Firmante 2" , "email" : "example@auco.ai" , "phone" : "+573123456789" , "label" : true } ] }`
Descargar ejemplo
Este enfoque es ideal cuando necesitas un control visual sobre la ubicación de las firmas directamente desde el editor del documento. Asegúrate de que las etiquetas no estén dentro de cuadros de texto o elementos gráficos que impidan su lectura por el sistema.
1. Especificación de coordenadas
2. Por medio de una plantilla en Auco
3. Uso de tags de firma en el documento PDF ¿Cómo funciona?
¿Cómo funciona?