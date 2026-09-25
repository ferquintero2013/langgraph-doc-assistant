# api/background-check/company

> Fuente: https://docs.auco.ai/api/background-check/company

Servicio para validar por NIT registrado en Colombia o número de documento de Estados Unidos y devuelve información de la compañía y registro mercantil.
`/validate/company/representatives`
`prk _`
Este servicio usa la llave privada de la organización
PARAMETROS: Nombre | Descripción ;; email String | Obligatorio. Correo electrónico del creador del proceso. Este correo debe estar registrado en la plataforma de Auco y debe pertenecer a la organización. ;; documentNumber String | Obligatorio. NIT sin digito de verificacion de la empresa a consultar para el caso de Colombia o numero de documento para el caso de Estados Unidos. Para Colombia ( CO ) debe tener exactamente 9 dígitos. ;; country String | Obligatorio. País donde se encuentra registrada la empresa a consultar. Valores aceptados: CO ;; targetWebhooks Array<String> | Opcional. Lista de webhooks a ser notificados. En caso de no definir se envia al webhook "default". ;; tags Array<String> | Opcional. Lista de tags que se envian cuando notifique al los webhooks configurados. ;; complete Boolean | Opcional. Solo para Colombia ( CO ). Indica si se solicita el detalle completo del registro mercantil.

## 🧪 Ejemplos de uso ​
Curl
Python
Node.js
`curl -X POST '{{api_auco}}/validate/company/representatives' \ -H 'Authorization: {{private_key}}' \ -d '{ "email": "prueba@auco.ai", "documentNumber": "901431536", "country": "CO" }'`
`import requests response = requests . post ( '{{api_auco}}/validate/company/representatives' , headers = { 'Authorization' : '{{private_key}}' } , json = { "email" : "prueba@auco.ai" , "documentNumber" : "901431536" , "country" : "CO" } ) print ( response . json ( ) )`
`const axios = require ( 'axios' ) ; axios . post ( '{{api_auco}}/validate/company/representatives' , { email : 'prueba@auco.ai' , documentNumber : '901431536' , country : 'CO' } , { headers : { Authorization : '{{private_key}}' } } ) . then ( ( response ) => console . log ( response . data ) ) ;`

## 📥 Ejemplos de respuesta ​
200: Consulta exitosa en Colombia.
{ "code" : "XXXXXXXX" , "codigo_camara" : "21" , "camara_comercio" : "MEDELLIN PARA ANTIOQUIA" , "matricula" : "68393312" , "inscripcion_proponente" : "000000000000" , "razon_social" : "MICONTRATO S.A.S." , "codigo_clase_identificacion" : "02" , "clase_identificacion" : "NIT" , "numero_identificacion" : "901431536" , "nit" : "901431536" , "digito_verificacion" : "3" , "cod_ciiu_act_econ_pri" : "6201" , "cod_ciiu_act_econ_sec" : "6202" , "ciiu3" : "5820" , "fecha_matricula" : "20201118" , "fecha_renovacion" : "20250328" , "ultimo_ano_renovado" : "2025" , "fecha_vigencia" : "99991231" , "codigo_tipo_sociedad" : "02" , "tipo_sociedad" : "SOCIEDAD COMERCIAL" , "codigo_organizacion_juridica" : "16" , "organizacion_juridica" : "SOCIEDADES POR ACCIONES SIMPLIFICADAS SAS" , "codigo_categoria_matricula" : "01" , "categoria_matricula" : "SOCIEDAD ó PERSONA JURIDICA PRINCIPAL ó ESAL" , "codigo_estado_matricula" : "01" , "estado_matricula" : "ACTIVA" , "clase_identificacion_rl" : "CEDULA DE CIUDADANIA" , "num_identificacion_representante_legal" : "1037644437" , "representante_legal" : "SANTIAGO  MONTOYA GIRALDO" , "fecha_actualizacion" : "2025/03/28 17:30:59.340000000" , "detailRM" : { "id" : "210068393312" , "cod_camara" : "21" , "camara" : "MEDELLIN PARA ANTIOQUIA" , "matricula" : "0068393312" , "razon_social" : "MICONTRATO S.A.S." , "sigla" : null , "clase_identificacion" : "NIT" , "numero_identificacion" : "901431536" , "numero_identificacion_2" : "00000901431536" , "dv" : "3" , "dir_comercial" : null , ... "cod_ciiu_act_econ_pri" : "6201" , "desc_ciiu_act_econ_pri" : "Actividades de desarrollo de sistemas informáticos (planificación, análisis, diseño, programación, pruebas)" , "cod_ciiu_act_econ_sec" : "6202" , "desc_ciiu_act_econ_sec" : "Actividades de consultoría informática y actividades de administración de instalaciones informáticas" , "ciiu3" : "5820" , "desc_ciiu3" : "Edición de programas de informática (software)" , "ciiu4" : "" , "desc_ciiu4" : "" , "fecha_matricula" : "20201118" , "fecha_renovacion" : "20250328" , "ultimo_ano_renovado" : "2025" , "fecha_vigencia" : "99991231" , "fecha_cancelacion" : "" , "motivo_cancelacion" : "" , "cod_tipo_sociedad" : "02" , "tipo_sociedad" : "SOCIEDAD COMERCIAL" , "organizacion_juridica" : "SOCIEDADES POR ACCIONES SIMPLIFICADAS SAS" , "categoria_matricula" : "SOCIEDAD ó PERSONA JURIDICA PRINCIPAL ó ESAL" , "indicador_emprendimiento_social" : "N" , "extincion_dominio" : "N" , "estado" : "ACTIVA" , "fecha_actualizacion" : "20251014" , "control_inactivacion_sipref" : null , ... "url_venta_certificados" : "http://virtuales.camaramedellin.com.co/e-cer/" } }

## ⚠️ Respuestas de error ​
PARAMETROS: Código | Descripción ;; 400 | Faltan parámetros como email , documentNumber , country o state . Formato incorrecto de imagen. ;; 401 | Autenticación inválida o ausente.
🧪 Ejemplos de uso
📥 Ejemplos de respuesta
⚠️ Respuestas de error