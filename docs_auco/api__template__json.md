# api/template/json

> Fuente: https://docs.auco.ai/api/template/json

Referencia completa para el archivo de configuración JSON — estructura raíz, tipos de pregunta, validaciones, condicionales y perfiles de firma.

## Localización y defaults ​
La plataforma asume Colombia por defecto en varios tipos. Algunos aceptan override vía el atributo country ; otros están fijos.
`country`
PARAMETROS: Tipo | Default | Override ;; currency | COP | No soportado — siempre formatea en pesos colombianos ;; nit | Colombia | No soportado — formato NIT colombiano fijo ( XXXXXX-X ) ;; identification | CO | country: "MX" | "CL" | "SV" | ... (ver la sección Identificación más abajo) ;; phone | Detecta automáticamente | country: "co" | "mx" | ... (ISO2 en minúscula) ;; department | CO | country: "CO" | "MX" | ... ;; date | Español, calendario gregoriano | No localizable — se renderiza como "15 de enero de 2024"
Si tu caso de uso requiere USD u otro formato monetario, currency no es el tipo indicado — usa number y formatea el prefijo manualmente en el HTML. De forma similar, nit solo aplica a Colombia; para tax IDs de otros países usa text con una regex apropiada.
`currency`
`number`
`nit`
`text`
`regex`

## Propiedades Principales del Objeto Raíz ​
`{ "name" : "Mi Primera Automatización" , "description" : "Contrato de servicios con un firmante, para el equipo comercial" , "preBuild" : false , "username" : "usuario_ejemplo" , "config" : [ ] , "signatureProfile" : [ ] , "sign" : [ ] }`
PARAMETROS: Propiedad | Tipo | Requerido | Descripción ;; name | string | Requerido | Nombre de la automatización ;; description | string | Opcional | Texto que describe la plantilla, máximo 500 caracteres. Solo informativo: lo devuelve GET /template y no afecta el diligenciamiento ;; config | array | Requerido | Array de preguntas para el usuario ;; signatureProfile | array | Requerido | Definición de firmantes y aprobadores ;; sign | array | Requerido | Nombres de preguntas obligatorias ;; preBuild | boolean | Opcional | Si es true , incluye prellenado automático ;; username | string | Opcional | Nombre de usuario dueño de la plantilla ;; build | number | Gestionado por el servidor | Versión de caché del SDK. No lo definas manualmente — el servidor lo incrementa automáticamente cuando actualizas la plantilla para invalidar la caché del SDK en clientes.

## Propiedad preBuild — Prellenado Automático ​
`preBuild`
Cuando preBuild es true , debes incluir preBuildData . Este campo habilita un prellenado automático de la plantilla: algunos campos se completan previamente para que el usuario solo termine de diligenciar el documento.
`preBuild`
`true`
`preBuildData`
En preBuildData se declaran las preguntas que se prellenarán en esta primera instancia. El último elemento del arreglo debe ser el correo del usuario final, quien recibirá la solicitud de diligenciamiento por correo electrónico.
`preBuildData`
`{ "preBuild" : true , "preBuildData" : [ "nombre_comprador" , "email_comprador" , "correo_usuario_final" ] }`

## config y sus tipos de preguntas ​
`config`
En esta sección se agregan todas las preguntas que debe diligenciar el usuario para generar el documento para firma.
Cada pregunta en config es un objeto con propiedades específicas. Siempre requiere name , description y type .
`config`
`name`
`description`
`type`
Las preguntas también pueden tener un valor por defecto añadiendo el atributo value (solo tiene sentido en clausula , select y searchlist ).
`value`
`clausula`
`select`
`searchlist`
`{ "name" : "identificador_unico" , "description" : "Texto que ve el usuario" , "type" : "tipo_pregunta" }`

## Resumen de Tipos de Pregunta ​
PARAMETROS: Tipo | UI de entrada | Valor almacenado | Renderizado en el span ;; text | texto libre | "str" | tal cual ;; name | texto | "str" | EN MAYÚSCULAS ;; email | email | "lower@x.com" | tal cual ;; phone | teléfono internacional | "+573001234567" | tal cual ;; number | entrada numérica | "50000" | "50.000" (o con texto escrito si addText ) ;; currency | entrada numérica | "50000" | "$50.000 (CINCUENTA MIL PESOS)" ;; date | selector de fecha | "2024-01-15" | "15 de enero de 2024" ;; nit | entrada numérica | "9001234567" | "900123456-7" (auto-formateado) ;; identification | país + tipo de doc + número | "CC 1084340519" (dos partes) | cadena completa ;; department | dropdown territorial | "Antioquia" | tal cual ;; select | dropdown simple | "valor_opcion" | options[i].label coincidente ;; searchlist | dropdown con búsqueda | "valor_opcion" | options[i].label coincidente ;; clausula | dropdown con spans condicionales | "valor_opcion" | muestra <span name="pregunta_valor"> ;; check | checkboxes múltiples | select: ["a","b"] arreglo | "a, b" (unidos por coma) ;; image | subida de archivo | data URI base64 | <img src="..." class="object-contain"/> ;; signature | firma dibujada / tipeada | base64 o cadena | <img> o <span class="text-sign"> ;; request | texto + validación externa | "str" | tal cual (más los campos prellenados por el servicio)
request requiere integración adicional con un backend y se cubre en su propia página: consulta Tipo Request .
`request`

## Texto Libre ( text ) ​
`text`
Acepta cualquier texto sin restricciones.
`{ "name" : "descripcion_producto" , "description" : "Describa brevemente el producto" , "type" : "text" }`
Soporta las validaciones maxlength y regex (ver Propiedades de Validación ).
`maxlength`
`regex`

## Nombre ( name ) ​
`name`
Igual a texto, pero convierte a mayúsculas automáticamente en el HTML.
`{ "name" : "nombre_comprador" , "description" : "Ingrese su nombre completo" , "type" : "name" }`
Ejemplo de salida:
Usuario ingresa: juan pérez
`juan pérez`
Se muestra en HTML: JUAN PÉREZ
`JUAN PÉREZ`

## Número ( number ) ​
`number`
Solo acepta valores numéricos. Se renderiza con separadores de miles.
`{ "name" : "cantidad_articulos" , "description" : "¿Cuántos artículos desea?" , "type" : "number" }`
Con texto escrito ( addText ):
`addText`
`{ "name" : "cantidad_articulos" , "description" : "¿Cuántos artículos desea?" , "type" : "number" , "addText" : true }`
Soporta límites numéricos min y max .
`min`
`max`
PARAMETROS: addText | Usuario ingresa 5000 | Se renderiza como ;; (omitir) | 5000 | 5.000 ;; true | 5000 | 5.000 (CINCO MIL)

## Moneda ( currency ) ​
`currency`
Formatea automáticamente como moneda (pesos colombianos por defecto) con el monto escrito en letras .
`{ "name" : "monto_total" , "description" : "Ingrese el valor en pesos" , "type" : "currency" }`
Sin texto escrito ( removeText ):
`removeText`
`{ "name" : "monto_total" , "description" : "Ingrese el valor en pesos" , "type" : "currency" , "removeText" : true }`
PARAMETROS: removeText | Usuario ingresa 50000 | Se renderiza como ;; (omitir) | 50000 | $50.000 (CINCUENTA MIL PESOS) ;; true | 50000 | $50.000

## Correo Electrónico ( email ) ​
`email`
Valida que sea un email correcto.
`{ "name" : "email_comprador" , "description" : "Ingrese su correo electrónico" , "type" : "email" }`

## Teléfono ( phone ) ​
`phone`
Valida el número telefónico según el indicativo seleccionado.
`{ "name" : "telefono_comprador" , "description" : "Ingrese su número telefónico" , "type" : "phone" }`
Limitado a un país específico:
`{ "name" : "telefono_comprador" , "description" : "Ingrese su teléfono colombiano" , "type" : "phone" , "country" : "co" }`
Cuando se define country , el input queda fijado al código de ese país.
`country`

## Fecha ( date ) ​
`date`
Muestra un calendario para seleccionar una fecha.
`{ "name" : "fecha_entrega" , "description" : "Seleccione la fecha de entrega" , "type" : "date" }`
Soporta min , max , subYears , subDays y afterSubYears para restricciones de rango. Consulta Propiedades de Validación .
`min`
`max`
`subYears`
`subDays`
`afterSubYears`

## NIT ( nit ) ​
`nit`
Entrada de NIT colombiano. Se formatea automáticamente como XXXXXX-X en el documento renderizado.
`XXXXXX-X`
`{ "name" : "nit_empresa" , "description" : "Ingrese el NIT de la empresa" , "type" : "nit" }`
PARAMETROS: Usuario ingresa | Se renderiza como ;; 9001234567 | 900123456-7 ;; 8301234 | 830123-4

## Identificación ( identification ) ​
`identification`
Entrada estructurada de identificación del firmante. El usuario elige un país , un tipo de documento e ingresa el número . El valor almacenado tiene dos partes separadas por un espacio : "{TIPO_DOC} {NÚMERO}" .
`"{TIPO_DOC} {NÚMERO}"`
`{ "name" : "cedula_comprador" , "description" : "Ingrese la identificación del comprador" , "type" : "identification" , "country" : "CO" }`
PARAMETROS: Acción del usuario | Valor almacenado | Renderizado en el span ;; Elige CC , ingresa 1084340519 | "CC 1084340519" | CC 1084340519 ;; Elige CE , ingresa A0123456 | "CE A0123456" | CE A0123456
Usa identification para documentos de firmantes en lugar de text o number . El runtime divide el valor en identificationType e identification al componer el perfil del firmante, lo cual es requerido para los flujos de verificación de identidad.
`identification`
`text`
`number`
`identificationType`
`identification`
Países soportados: Colombia (CC, CE, PPT, DL, PASSPORT), México (CURP, PASSPORT), Chile (RUT, RUN, PASSPORT), El Salvador (DUI, PASSPORT), Costa Rica (CCCR, PASSPORT), Perú (DNI, PASSPORT), Uruguay (CI, PASSPORT), Venezuela (CI, PASSPORT), Honduras (DNI, PASSPORT), Panamá (CI, PASSPORT), España (DNI, PASSPORT), Ecuador (CI, PASSPORT), Aruba (CI, PASSPORT).

## Departamento ( department ) ​
`department`
Dropdown de divisiones territoriales (departamentos / estados) para el país configurado. Por defecto Colombia.
`{ "name" : "departamento_comprador" , "description" : "Seleccione el departamento del comprador" , "type" : "department" , "country" : "CO" }`
El valor almacenado es el nombre completo del departamento (p. ej. "Antioquia" ).
`"Antioquia"`

## Lista Simple ( select ) ​
`select`
Dropdown simple. No activa visibilidad condicional de otras preguntas.
`{ "name" : "tipo_documento" , "description" : "Seleccione el tipo de documento" , "type" : "select" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "label" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de Extranjería" , "label" : "Cédula de Extranjería" , "value" : "ce" } ] }`
HTML correspondiente:
`< span name = " tipo_documento " > _______________ </ span >`
El SDK coloca automáticamente el label de la opción en el span.
`label`

## Lista con Búsqueda ( searchlist ) ​
`searchlist`
Dropdown con input de búsqueda. Idéntico a select en el JSON — solo cambia la UX. Úsalo cuando la lista tiene más de ~10 opciones.
`select`
`{ "name" : "pais_nacimiento" , "description" : "Seleccione su país de nacimiento" , "type" : "searchlist" , "options" : [ { "name" : "Argentina" , "label" : "Argentina" , "value" : "AR" } , { "name" : "Brasil" , "label" : "Brasil" , "value" : "BR" } ] }`
El HTML es un único <span name="pais_nacimiento"> igual que select .
`<span name="pais_nacimiento">`
`select`

## Lista de Cláusulas ( clausula ) ​
`clausula`
Dropdown con opciones predefinidas. Permite limitar otras preguntas vía prereq .
`prereq`
`{ "name" : "tipo_documento" , "description" : "Seleccione el tipo de documento" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de Extranjería" , "value" : "ce" } , { "name" : "Pasaporte" , "value" : "pasaporte" } ] }`
HTML correspondiente:
`< span name = " tipo_documento_cc " > C.C. </ span > < span name = " tipo_documento_ce " hidden > C.E. </ span > < span name = " tipo_documento_pasaporte " hidden > PASAPORTE </ span >`
Reglas:
Se crea un <span> por cada opción , con name = {nombre_pregunta}_{valor_opcion} .
`<span>`
`name = {nombre_pregunta}_{valor_opcion}`
El elemento que coincide con el value por defecto no debe tener hidden .
`value`
`hidden`
Todas las demás opciones deben tener hidden .
`hidden`
El SDK alterna la visibilidad a medida que el usuario selecciona distintas opciones.

## Múltiples Opciones ( check ) ​
`check`
Campo de selección múltiple que se renderiza como una lista unida por comas.
`{ "name" : "servicios_incluidos" , "description" : "Seleccione los servicios incluidos" , "type" : "check" , "values" : [ "limpieza" , "mantenimiento" , "seguro" ] }`
`values`
`options`
El tipo check es el único tipo que usa un arreglo plano values: ["a", "b"] en lugar de una estructura options: [{...}] . Usar options aquí no renderizará nada.
`check`
`values: ["a", "b"]`
`options: [{...}]`
`options`
Salida renderizada : <span name="servicios_incluidos">limpieza, mantenimiento</span> (si el usuario marca esas dos).
`<span name="servicios_incluidos">limpieza, mantenimiento</span>`

## Imagen ( image ) ​
`image`
Input de subida de archivo (PNG o JPEG, máx. 8 MB). El valor almacenado es un data URI en base64, y el span se reemplaza por un elemento <img> .
`<img>`
`{ "name" : "foto_documento" , "description" : "Suba una foto de su documento" , "type" : "image" }`
HTML correspondiente:
`< span name = " foto_documento " > ___________ </ span >`
Al diligenciar, el span se convierte en:
`< span name = " foto_documento " > < img src = " data:image/png;base64,... " class = " object-contain " /> </ span >`

## Firma ( signature ) ​
`signature`
Captura una firma dibujada en canvas o tipeada con una fuente tipo firma. Siempre obligatoria (no puede dejarse vacía).
`{ "name" : "firma_comprador" , "description" : "Dibuje su firma" , "type" : "signature" , "allow" : [ "draw" , "font" ] }`
El arreglo allow restringe los modos de captura disponibles para el usuario:
`allow`
["draw"] — solo dibujada a mano en canvas
`["draw"]`
["font"] — solo tipeada en una fuente tipo firma
`["font"]`
["draw", "font"] — ambas permitidas
`["draw", "font"]`
`signature`
Es distinto al placeholder de firma usado por signatureProfile . Usa preguntas signature cuando necesitas una segunda firma inline dentro del cuerpo del documento (p. ej., iniciales en cada cláusula). Para la firma principal del firmante usa <div id="comprador" class="sign-margin"> junto con signatureProfile — consulta Configuración del HTML .
`signatureProfile`
`signature`
`<div id="comprador" class="sign-margin">`
`signatureProfile`

## Request ( request ) ​
`request`
Entrada de texto que valida su valor contra un endpoint HTTP externo y usa la respuesta para prellenar otros campos del documento.
Se cubre en una página dedicada porque requiere integración con backend: Tipo Request → .

## Propiedades de Validación ​
Todos los tipos de pregunta soportan un conjunto de propiedades opcionales de validación para restringir la entrada del usuario.
PARAMETROS: Propiedad | Aplica a | Descripción ;; maxlength | text , name , phone | Número máximo de caracteres. ;; regex | cualquier input de texto | Expresión regular de JavaScript que debe cumplir el valor. Ejemplo: "^[A-Z]{3}\\d{3}$" ;; min | number , currency | Valor numérico mínimo (como string). ;; max | number , currency , date | Valor numérico o de fecha máximo. ;; subYears | date | Edad mínima en años (p. ej. 18 significa que la fecha debe ser ≥ 18 años atrás). ;; subDays | date | Distancia mínima en días desde hoy. ;; afterSubYears | date | La fecha debe estar al menos estos años en el futuro. ;; country | phone , identification , department | Código ISO2 del país (p. ej. "CO" , "MX" ). ;; groupQuestion | number | Valida que un grupo de campos sume hasta un máximo. Ver abajo.

## Ejemplo: fecha de nacimiento solo para mayores de edad ​
`{ "name" : "fecha_nacimiento" , "description" : "Ingrese su fecha de nacimiento" , "type" : "date" , "subYears" : 18 }`

## Ejemplo: código alfanumérico estricto ​
`{ "name" : "codigo_referencia" , "description" : "Ingrese el código de referencia (formato ABC-1234)" , "type" : "text" , "regex" : "^[A-Z]{3}-\\d{4}$" , "maxlength" : 8 }`

## Ejemplo: groupQuestion (los campos deben sumar ≤ 100) ​
`groupQuestion`
`[ { "name" : "porcentaje_propietario" , "description" : "Porcentaje del propietario" , "type" : "number" , "groupQuestion" : { "id" : "participacion" , "max" : 100 , "errorMessage" : "Los porcentajes no deben superar el 100%" } } , { "name" : "porcentaje_socio" , "description" : "Porcentaje del socio" , "type" : "number" , "groupQuestion" : { "id" : "participacion" , "max" : 100 , "errorMessage" : "Los porcentajes no deben superar el 100%" } } ]`
Todas las preguntas que comparten el mismo groupQuestion.id se validan en conjunto: su suma no debe superar max .
`groupQuestion.id`
`max`

## Preguntas Condicionales con prereq ​
`prereq`
La propiedad prereq controla la visibilidad condicional de una pregunta:
`prereq`
k (key): nombre de la pregunta de referencia
v (value): valor requerido en la pregunta de referencia para mostrar la pregunta actual
`"prereq" : [ { "k" : "nombre_pregunta_referencia" , "v" : "valor_requerido" } ]`
Varias entradas se combinan con AND (todas deben cumplirse).
La pregunta referenciada en k debe ser de tipo clausula . Solo clausula dispara visibilidad condicional.
`clausula`
`[ { "name" : "tipo_documento" , "description" : "Seleccione el tipo de documento del comprador" , "type" : "clausula" , "value" : "cc" , "options" : [ { "name" : "Cédula de Ciudadanía" , "value" : "cc" } , { "name" : "Cédula de Extranjería" , "value" : "ce" } ] } , { "name" : "numero_cc" , "description" : "Ingrese el número de cédula de ciudadanía" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento" , "v" : "cc" } ] } , { "name" : "numero_ce" , "description" : "Ingrese el número de cédula de extranjería" , "type" : "number" , "prereq" : [ { "k" : "tipo_documento" , "v" : "ce" } ] } ]`

## prereqOptionals — Lógica OR ​
`prereqOptionals`
Para mostrar una pregunta cuando la referencia coincide con cualquiera de varios valores, usa prereqOptionals junto con prereq . Cada entrada tiene el formato {nombre_pregunta}_{valor_opcion} .
`prereqOptionals`
`prereq`
`{nombre_pregunta}_{valor_opcion}`
`{ "name" : "nit_empresa" , "description" : "NIT de la empresa" , "type" : "nit" , "prereq" : [ { "k" : "tipo_cliente" , "v" : "empresa" } ] , "prereqOptionals" : [ "tipo_cliente_empresa" , "tipo_cliente_consorcio" ] }`
La pregunta aparece cuando tipo_cliente es empresa o consorcio .
`tipo_cliente`
`empresa`
`consorcio`

## Perfiles de Firma ( signatureProfile ) ​
`signatureProfile`
Define quiénes firman el documento y sus datos asociados. Este objeto no guarda los datos crudos del firmante — guarda referencias a las preguntas que contienen la información de cada firmante.
PARAMETROS: Propiedad | Tipo | Requerido | Descripción ;; name | String | String[] | Requerido | Nombre de la pregunta con el nombre del firmante. Puede ser un arreglo de nombres de preguntas a concatenar (ver abajo). ;; identification | String | Requerido | Nombre de la pregunta para la identificación. Puede tener múltiples opciones con | . ;; email | String | Requerido | Nombre de la pregunta para el correo del firmante ;; phone | String | Requerido | Nombre de la pregunta para el teléfono (recomendado para OTP) ;; type | String | Requerido | Identificador único, usado como id (o name ) en el Complete HTML
`{ "name" : "nombre_comprador" , "identification" : "cedula_comprador" , "email" : "email_comprador" , "phone" : "telefono_comprador" , "type" : "comprador" }`
Si tienes varias preguntas de identificación (C.C, C.E, Pasaporte), sepáralas con | (pipe). El runtime toma la que tenga valor.
`{ "name" : "nombre_vendedor" , "identification" : "cedula_vendedor|cedulae_vendedor|pasaporte_vendedor" , "email" : "email_vendedor" , "phone" : "telefono_vendedor" , "type" : "vendedor" }`
`name`
Cuando el documento captura el nombre en varios campos (primer nombre + segundo nombre + apellido), pasa un arreglo de nombres de preguntas . El runtime los concatena con espacios.
`{ "name" : [ "primer_nombre_comprador" , "segundo_nombre_comprador" , "apellido_comprador" ] , "identification" : "cedula_comprador" , "email" : "email_comprador" , "phone" : "telefono_comprador" , "type" : "comprador" }`
Para la ubicación de los elementos <div> en el Complete HTML, consulta Configuración del HTML → Ubicación de Firmas .
`<div>`

## Preguntas Obligatorias ​
La propiedad sign es un arreglo con los nombres de las preguntas que el usuario no puede saltar :
`sign`
`"sign" : [ "nombre_comprador" , "email_comprador" , "cedula_comprador" ]`
El usuario debe completar obligatoriamente las preguntas registradas en sign .
`sign`
Las preguntas de tipo signature son obligatorias automáticamente — no necesitas listarlas en sign .
`signature`
`sign`

## Diferencias Clave: clausula vs select vs searchlist ​
`clausula`
`select`
`searchlist`
PARAMETROS: Característica | Clausula | Select | Searchlist ;; ¿Dropdown? | Sí | Sí | Sí, con input de búsqueda ;; Elementos HTML necesarios | Un <span> por opción | Un <span> | Un <span> ;; ¿Puede limitar otras preguntas? | ✅ Sí | ❌ No | ❌ No ;; ¿Referenciable en prereq.k ? | ✅ Sí | ❌ No | ❌ No ;; Estructura de options | {name, value} | {name, label, value} | {name, label, value} ;; Cantidad recomendada de opciones | 2–8 | 2–10 | 10+
Localización y defaults
Propiedades Principales del Objeto Raíz Propiedad preBuild — Prellenado Automático
Propiedad preBuild — Prellenado Automático
`preBuild`
config y sus tipos de preguntas Resumen de Tipos de Pregunta Texto Libre ( text ) Nombre ( name ) Número ( number ) Moneda ( currency ) Correo Electrónico ( email ) Teléfono ( phone ) Fecha ( date ) NIT ( nit ) Identificación ( identification ) Departamento ( department ) Lista Simple ( select ) Lista con Búsqueda ( searchlist ) Lista de Cláusulas ( clausula ) Múltiples Opciones ( check ) Imagen ( image ) Firma ( signature ) Request ( request )
`config`
Resumen de Tipos de Pregunta
Texto Libre ( text )
`text`
Nombre ( name )
`name`
Número ( number )
`number`
Moneda ( currency )
`currency`
Correo Electrónico ( email )
`email`
Teléfono ( phone )
`phone`
Fecha ( date )
`date`
NIT ( nit )
`nit`
Identificación ( identification )
`identification`
Departamento ( department )
`department`
Lista Simple ( select )
`select`
Lista con Búsqueda ( searchlist )
`searchlist`
Lista de Cláusulas ( clausula )
`clausula`
Múltiples Opciones ( check )
`check`
Imagen ( image )
`image`
Firma ( signature )
`signature`
Request ( request )
`request`
Propiedades de Validación Ejemplo: fecha de nacimiento solo para mayores de edad Ejemplo: código alfanumérico estricto Ejemplo: groupQuestion (los campos deben sumar ≤ 100)
Ejemplo: fecha de nacimiento solo para mayores de edad
Ejemplo: código alfanumérico estricto
Ejemplo: groupQuestion (los campos deben sumar ≤ 100)
`groupQuestion`
Preguntas Condicionales con prereq prereqOptionals — Lógica OR
`prereq`
prereqOptionals — Lógica OR
`prereqOptionals`
Perfiles de Firma ( signatureProfile )
`signatureProfile`
Preguntas Obligatorias
Diferencias Clave: clausula vs select vs searchlist
`clausula`
`select`
`searchlist`