# SECOP II - Procesos de Contratación

Extrae en minutos todos los procesos de contratación pública de Colombia publicados en
**SECOP II** (~9,14 millones de procesos y creciendo) filtrando por palabras clave,
entidad, departamento, estado o fechas - sin escribir una sola línea de código.

Ideal para veedurías ciudadanas, áreas comerciales que buscan licitaciones y
oportunidades de negocio con el Estado, periodistas de datos, firmas de consultoría,
proveedores del Estado que monitorean su sector, y cualquier analista que necesite el
dataset de SECOP II en formato limpio y estructurado (JSON, CSV, Excel) en lugar de
navegar la interfaz web de SECOP proceso por proceso.

## ¿Por qué usar este Actor de datos abiertos de SECOP II?

- **Fuente 100% oficial, cero scraping.** Los datos salen directamente de la API
  pública y documentada de [datos.gov.co](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Procesos-de-Contrataci-n/p6dx-8zbt/about_data)
  (Socrata SODA) - la misma que usa el Estado colombiano para publicar su información
  de contratación. No hay navegador, ni impersonación, ni riesgo de bloqueo: es la API
  usada de la forma en que fue diseñada.
- **Búsqueda por múltiples palabras clave, con conteo por cada una.** Agrega varios
  términos de búsqueda (por ejemplo "interventoría vial", "consultoría ambiental",
  "software") y el Actor los busca uno por uno, marca cada registro con el término que
  lo encontró y te entrega cuántos procesos aparecieron por cada palabra clave - perfecto
  para comparar el volumen de oportunidades entre varios sectores o líneas de negocio en
  una sola corrida.
- **Filtros listos para usar sin aprender SoQL.** Entidad, departamento, estado del
  proceso (como lista desplegable con los valores reales del dataset) y rango de fechas
  de publicación, más una cláusula SoQL avanzada para quienes necesiten algo más
  específico.
- **60 campos por registro**, reflejando las propias columnas de SECOP: identidad de la
  entidad y del proceso, todas las fechas de cada fase publicada, economía del contrato
  (precio base, tipo de contrato, duración), niveles de participación de proveedores,
  detalles de adjudicación, proveedor adjudicado y el enlace directo al proceso en SECOP.
- **Seguro para tablas gigantes que se siguen escribiendo en vivo.** Se protege contra
  duplicados y paginación inestable sobre un dataset de 9+ millones de filas en
  constante actualización (ver más abajo).

## Cómo usarlo (tutorial rápido)

1. Haz clic en **Try for free** o **Run**.
2. Escribe una o varias **palabras clave** (opcional) y, si quieres, afina con
   **entidad**, **departamento**, **estado del proceso** (lista desplegable) y un rango
   de **fechas de publicación**.
3. Ajusta **Máximo de registros** según lo que necesites (por defecto 1000; el dataset
   completo tiene ~9,14 millones de filas, así que filtra antes de pedir todo).
4. Pulsa **Start**. En segundos empezarás a ver resultados en el Dataset, listos para
   ver en la tabla, o exportar a JSON, CSV, Excel o Google Sheets.
5. Revisa `RUN_SUMMARY` en el Key-value store al final de la corrida para ver cuántos
   registros trajiste en total y cuántos por cada palabra clave buscada.

No necesitas cuenta, cookie ni API key para correrlo - ver la sección siguiente.

## ¿Necesitas cuenta, cookie o API key?

**No.** Este endpoint es genuinamente público. La única credencial opcional es un
**token de aplicación de Socrata**, gratuito: inicia sesión en datos.gov.co -> Editar
perfil -> Configuración de desarrollador -> Crear nuevo token de aplicación. Es un
token de uso de API asociado a tu cuenta, no una cookie de sesión - solo sube tu límite
de solicitudes si corres este Actor de forma intensiva o muy frecuente. En pruebas,
varias solicitudes rápidas sin ningún token no tuvieron ningún tipo de bloqueo, así que
es opcional para uso ligero.

## Campos de entrada

| Campo | Tipo | Notas |
|---|---|---|
| `keywords` | lista de texto | Una o varias palabras clave; cada una se busca por separado (SoQL `$q`) y se cuenta por separado |
| `entidad` | texto | Coincidencia parcial, sin distinguir mayúsculas, sobre el nombre de la entidad contratante |
| `departamento` | texto | Nombre exacto del departamento tal como lo registra SECOP |
| `estadoResumen` | lista desplegable | Estado exacto del proceso (ej. `Adjudicado`, `Presentación de oferta`), con los valores reales del dataset |
| `fechaDesde` / `fechaHasta` | fecha | Filtran sobre `fecha_de_publicacion_del` |
| `whereClause` | texto | Avanzado: una cláusula SoQL `$where` en crudo, combinada con los filtros de arriba |
| `maxItems` | número | Por defecto 1000. La tabla tiene ~9,14M de filas - filtra antes de subir este valor |
| `pageSize` | número | Registros por solicitud a la API (por defecto 1000, máximo 50000) |
| `appToken` | texto (secreto) | Token opcional y gratuito de Socrata - ver arriba |

Ningún filtro es obligatorio: una consulta vacía trae los procesos publicados más
recientemente.

## Ejemplo de salida

```json
{
  "entidad": "ALCALDIA MUNICIPAL DE YOTOCO",
  "nitEntidad": "890399002",
  "departamentoEntidad": "Valle del Cauca",
  "nombreDelProcedimiento": "PRESTACIÓN DE SERVICIOS PROFESIONALES DE SOPORTE Y MANTENIMIENTO...",
  "fase": "Presentación de oferta",
  "precioBase": 68310000.0,
  "modalidadDeContratacion": "Contratación directa",
  "fechaDePublicacionDel": "2026-09-04",
  "urlProceso": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?...",
  "searchKeywords": "software",
  "scrapedAt": "2026-09-07T19:20:00Z"
}
```

Cada corrida además guarda un resumen en el Key-value store bajo la clave
`RUN_SUMMARY`, con el total de registros y el conteo por cada palabra clave buscada:

```json
{
  "records": 480,
  "byKeyword": { "interventoria vial": 320, "software": 160 },
  "ok": 480,
  "duplicate": 12
}
```

## Precios

Este Actor no usa navegador ni proxies: cada corrida es una simple llamada a una API
JSON pública, así que consume muy pocas Unidades de Cómputo de Apify por registro
comparado con un scraper tradicional. Corre bajo el modelo de precios estándar de la
plataforma Apify (pago por uso), con la posibilidad de probarlo gratis con tu plan de
Apify. En pruebas locales, 3000 registros (con deduplicación) se descargaron en ~11
segundos sin necesidad de ajustar concurrencia ni usar proxy.

## Notas de calidad de datos (aprendidas probando contra la API en vivo)

- **La paginación por offset sobre una tabla en vivo de ~9,14M de filas necesita una
  clave de orden estable.** SECOP registra la fecha de publicación solo con precisión
  de día, así que miles de filas comparten exactamente el mismo valor - un `ORDER BY`
  simple es no determinístico entre solicitudes paginadas y produce filas duplicadas o
  saltadas. Este Actor ordena por `fecha_de_publicacion_del DESC NULL LAST, :id` (el id
  interno de fila de Socrata) para mantener la paginación estable, y además
  **deduplica defensivamente por `id_del_proceso`** - una corrida en vivo de 3000 filas
  sin ambas protecciones contenía entre 129 y 197 filas exactamente duplicadas.
- **`NULL LAST` importa.** El comportamiento por defecto de `DESC` en SoQL/Postgres pone
  los valores `NULL` primero, lo que mostraría registros incompletos o sin fecha antes
  que los reales.
- **Los procesos recientes tienen campos de adjudicación vacíos.** Al ordenar del más
  reciente al más antiguo, los procesos recién publicados todavía están en una fase
  temprana (`Presentación de oferta`, etc.) - `valorTotalAdjudicacion`,
  `nombreDelProveedor` y campos similares están genuinamente vacíos para ellos, no es un
  error. Filtra por `estadoResumen` o `fechaHasta` con una ventana más atrás si
  necesitas específicamente contratos ya adjudicados.
- **Los números y fechas llegan como texto** desde la API (`"57333333"`, no `57333333`)
  y se convierten a los tipos correctos (`float`/`int`/`date`) antes de guardarse.
- Los registros que fallan la validación van a un Dataset separado llamado `INVALID`
  con la fila original adjunta.

## Preguntas frecuentes

**¿Esto es scraping? ¿Puede bloquearme SECOP?**
No. Este Actor solo llama a la API pública y documentada de Socrata que el propio
Estado colombiano expone para reutilización de datos abiertos. No hay navegador, ni
simulación de usuario, ni cookies de sesión que puedan expirar o bloquearse.

**¿Puedo buscar varias palabras clave en una sola corrida?**
Sí. Agrega tantos términos como necesites en el campo de palabras clave: cada uno se
busca por separado y el resumen final (`RUN_SUMMARY.byKeyword`) te muestra cuántos
procesos encontró cada término.

**¿Cómo filtro por estado del proceso sin equivocarme en el texto exacto?**
El campo `estadoResumen` es una lista desplegable con los valores reales que existen
hoy en el dataset (por ejemplo `Adjudicado` o `Presentación de oferta`), así evitas
errores de tipeo o de mayúsculas/minúsculas que harían que el filtro no traiga nada.

**¿Qué pasa si necesito un filtro que no está en la lista?**
Usa el campo avanzado `whereClause` con una cláusula SoQL en crudo; se combina con los
demás filtros usando AND.

**¿Hay límite de resultados?**
El único límite es el que tú definas en `maxItems`. El dataset completo tiene ~9,14
millones de filas - siempre es más rápido y más barato filtrar primero por palabras
clave, entidad, departamento o fechas.

## Desarrollo local

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src/ tests/

echo '{"keywords":["software"],"maxItems":25}' > storage/key_value_stores/default/INPUT.json
.venv/bin/python -m src
```

Despliega con `apify push`.

## Aviso legal

Estos son datos abiertos del gobierno colombiano, publicados explícitamente para reuso
público bajo los términos de datos abiertos de [datos.gov.co](https://www.datos.gov.co).
No hay conflicto con los términos de servicio, ni problemas de datos personales más
allá de lo que el propio gobierno ya publica (nombres de entidades, proveedores
adjudicados, valores de contrato - todo de carácter público por diseño).
