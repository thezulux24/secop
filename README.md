# SECOP II - Monitor de Procesos de Contratación Pública de Colombia

**La solución más rápida, completa y rentable para extraer, monitorear y analizar licitaciones y contratos del Estado colombiano en SECOP II.**

Accede en segundos a más de **9,14 millones de procesos de contratación pública**. Filtra por palabras clave, entidad compradora, departamento, estado del proceso y fechas sin configuraciones complejas. Obtén datasets limpios y estructurados listos para exportar a Excel, CSV o conectar a tus sistemas mediante API y Webhooks.

---

## ¿Por qué elegir este Actor de SECOP II?

| Beneficio | Impacto para tu Negocio |
|---|---|
| ⚡ **Extracción Ultrarrápida y Eficiente** | Diseñado con arquitectura ligera (256 MB de RAM), permitiendo descargar miles de registros en segundos con el **mínimo consumo de unidades de cómputo en Apify**. |
| 🔍 **Búsqueda Multi-Término Simultánea** | Consulta múltiples sectores o palabras clave en una sola corrida (ej. *"interventoría vial"*, *"software"*, *"medicamentos"*). Cada registro se etiqueta con el término que lo originó e incluye un resumen analítico de resultados por término. |
| 🛡️ **Conexión Directa y Confiable** | Conectado a la fuente oficial de datos abiertos del Estado colombiano. Cero riesgo de bloqueos, interrupciones o sesiones expiradas. |
| 📊 **60 Campos Estructurados** | Máxima profundidad de datos: identidad de la entidad, presupuesto base, cronograma completo de licitación, oferentes participantes y proveedor adjudicado. |
| 🔄 **Paginación Estable y Deduplicación** | Algoritmo inteligente que garantiza ordenamiento determinístico y elimina duplicados en un dataset gigantesco y en constante actualización en vivo. |
| 🔔 **Alertas Automáticas de Oportunidades** | Programa ejecuciones automáticas diarias para recibir nuevas licitaciones directamente en tu correo, Slack, Google Sheets o CRM. |

---

## Casos de Uso de Alto Rendimiento

- 💼 **Proveedores del Estado y Licitadores (B2G)**: Detecta nuevas licitaciones en tu sector en el instante en que se publican para contar con el máximo tiempo de preparación de pliegos y propuestas.
- 🏢 **Firmas de Consultoría, Ingeniería y Servicios Legales**: Monitorea convocatorias públicas, contratos de interventoría, consultorías ambientales y asesorías jurídicas en todo el país.
- 📈 **Inteligencia Competitiva y Pricing**: Analiza los presupuestos oficiales adjudicados, quiénes son tus competidores ganadores, sus precios de adjudicación y cuotas de mercado por región.
- 🏛️ **Veedurías Ciudadanas, Periodismo de Datos y Compliance**: Audita contrataciones directas, compras en urgencia manifiesta, concentración de proveedores y cumplimiento de cronogramas con trazabilidad total.
- 🤖 **Pipelines de IA y Machine Learning**: Alimenta modelos de lenguaje (LLM), análisis predictivo de contratación pública y asistentes virtuales con datos de compras estatales actualizados diariamente.

---

## 60 Campos de Información Extraídos

Cada registro se entrega normalizado y tipificado, listo para análisis en Excel, PowerBI, SQL o Python:

### 1. Entidad Contratante
- `entidad`: Nombre oficial de la entidad pública contratante.
- `nitEntidad`: NIT de la entidad.
- `departamentoEntidad`: Departamento donde se ubica la entidad.
- `ciudadEntidad`: Ciudad o municipio de la entidad.
- `ordenEntidad`: Orden administrativo (`Nacional`, `Territorial`).
- `codigoPci`: Código de la posición presupuestal o institucional.
- `codigoEntidad`: Identificador único de la entidad en SECOP.

### 2. Identificación y Descripción del Proceso
- `idDelProceso`: Identificador único del proceso en SECOP II.
- `referenciaDelProceso`: Número de referencia asignado por la entidad (ej. *"LP-001-2026"*).
- `nombreDelProcedimiento`: Título u objeto principal del contrato.
- `descripcionDelProcedimiento`: Alcance detallado y especificaciones del objeto a contratar.
- `ppi`: Código del Plan Plurianual de Inversiones (si aplica).
- `idDelPortafolio`: Identificador del portafolio contractual.

### 3. Estado y Fases del Procedimiento
- `fase`: Fase actual del proceso (`Presentación de oferta`, `Fase de ofertas`, `Adjudicado`, etc.).
- `estadoResumen`: Estado consolidado del trámite.
- `estadoDelProcedimiento`: Detalle del estado administrativo.
- `estadoDeAperturaDelProceso`: Estado operativo de la apertura del proceso.

### 4. Cronograma Oficial de Fechas
- `fechaDePublicacionDel`: Fecha en que el proceso fue publicado oficialmente (`AAAA-MM-DD`).
- `fechaDeUltimaPublicacion`: Fecha de la última adenda o modificación.
- `fechaDeRecepcionDe`: Plazo límite para la recepción de ofertas de los proponentes.
- `fechaDeAperturaDeRespuesta`: Fecha de apertura pública de las propuestas recibidas.
- `fechaDeAperturaEfectiva`: Fecha en que efectivamente se abrieron las ofertas.
- `fechaAdjudicacion`: Fecha en que se expidió el acto de adjudicación.
- `fechaDePublicacionFase`, `fechaDePublicacionFase1`, `fechaDePublicacionFase2`, `fechaDePublicacionFase3`: Marcas temporales de cada fase del procedimiento.

### 5. Economía y Condiciones Contractuales
- `precioBase`: Presupuesto oficial estimado en pesos colombianos (formato numérico).
- `modalidadDeContratacion`: Modalidad legal (`Licitación pública`, `Selección abreviada`, `Contratación directa`, `Mínima cuantía`, `Concurso de méritos`).
- `justificacionModalidadDe`: Justificación jurídica de la modalidad empleada.
- `tipoDeContrato`: Clasificación legal (`Obra`, `Consultoría`, `Suministro`, `Prestación de servicios`, etc.).
- `subtipoDeContrato`: Subclasificación del contrato.
- `duracion`: Plazo contractual estipulado.
- `unidadDeDuracion`: Unidad de tiempo (`Días`, `Meses`, `Años`).
- `codigoPrincipalDeCategoria`: Código UNSPSC principal del bien o servicio.
- `categoriasAdicionales`: Categorías complementarias del catálogo.

### 6. Participación y Métricas de Proveedores
- `proveedoresInvitados`: Cantidad de proveedores convocados directamente.
- `visualizacionesDel`: Número de visitas y consultas que ha tenido el proceso.
- `proveedoresQueManifestaron`: Oferentes que presentaron manifestación de interés.
- `respuestasAlProcedimiento`: Propuestas comerciales radicadas.
- `proveedoresUnicosCon`: Número de proveedores únicos que participaron.
- `numeroDeLotes`: Cantidad de lotes o grupos en que se divide el contrato.

### 7. Adjudicación y Proveedor Ganador
- `adjudicado`: Indicador de si el proceso ya fue formalmente adjudicado (`Si` / `No`).
- `idAdjudicacion`: Identificador del acto de adjudicación.
- `valorTotalAdjudicacion`: Monto final adjudicado en pesos colombianos.
- `nombreDelAdjudicador`: Funcionario responsable de la adjudicación.
- `nombreDelProveedor`: Razón social de la empresa o contratista adjudicado.
- `nitDelProveedorAdjudicado`: NIT o documento del contratista ganador.
- `departamentoProveedor` / `ciudadProveedor`: Domicilio comercial del contratista adjudicado.

### 8. Enlace Directo y Trazabilidad
- `urlProceso`: Enlace web directo a la ficha del proceso en el portal de SECOP II.
- `searchKeywords`: Término de búsqueda que descubrió el proceso.
- `scrapedAt`: Fecha y hora exacta de la extracción (ISO 8601).

---

## Ejemplo de Salida

```json
{
  "idDelProceso": "CO1.REQ.4512984",
  "referenciaDelProceso": "LP-004-2026",
  "entidad": "INSTITUTO NACIONAL DE VÍAS - INVIAS",
  "nitEntidad": "800215807",
  "departamentoEntidad": "Distrito Capital de Bogotá",
  "ciudadEntidad": "Bogotá",
  "nombreDelProcedimiento": "INTERVENTORÍA INTEGRAL TÉCNICA, ECONÓMICA, JURÍDICA Y AMBIENTAL PARA EL MEJORAMIENTO DEL CORREDOR VIAL",
  "fase": "Presentación de oferta",
  "estadoResumen": "Presentación de oferta",
  "modalidadDeContratacion": "Concurso de méritos abierto",
  "tipoDeContrato": "Consultoría",
  "precioBase": 3450000000.0,
  "duracion": 18,
  "unidadDeDuracion": "Meses",
  "fechaDePublicacionDel": "2026-09-10",
  "fechaDeRecepcionDe": "2026-10-05",
  "fechaDeAperturaDeRespuesta": "2026-10-06",
  "visualizacionesDel": 312,
  "respuestasAlProcedimiento": 8,
  "adjudicado": "No",
  "urlProceso": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.4512984",
  "searchKeywords": "interventoria vial",
  "scrapedAt": "2026-09-16T12:00:00.000Z"
}
```

Cada ejecución genera automáticamente un informe consolidado en el **Key-Value Store** bajo la clave `RUN_SUMMARY`:
```json
{
  "records": 520,
  "byKeyword": {
    "interventoria vial": 310,
    "consultoria ambiental": 210
  },
  "ok": 520,
  "duplicate": 14
}
```

---

## Guía Rápida de Inicio

Configura y ejecuta tu primera búsqueda en 3 pasos:

1. **Ingresa tus Palabras Clave**: Escribe uno o varios términos de búsqueda (ej. `["software", "interventoria"]`).
2. **Aplica Filtros Estratégicos (Opcional)**: Selecciona el departamento, la entidad compradora, el estado (ej. *"Presentación de oferta"*) o un rango de fechas.
3. **Ejecuta y Descarga**: Haz clic en **Save & Start**. Tu dataset estará listo para exportar a **Excel**, **CSV**, **JSON** o consumir vía API.

---

## Parámetros de Entrada

| Parámetro | Tipo | Por Defecto | Descripción |
|---|---|---|---|
| **`keywords`** | `array` | `["interventoria vial"]` | Lista de palabras clave a consultar. Cada término se busca y cuantifica por separado. Déjalo vacío si prefieres filtrar solo por entidad, estado o fechas. |
| **`entidad`** | `string` | – | Coincidencia parcial (sin distinguir mayúsculas) del nombre de la entidad (ej. `"alcaldia de cali"`, `"ministerio de transporte"`). |
| **`departamento`** | `string` | – | Departamento oficial en Colombia (ej. `"Antioquia"`, `"Cundinamarca"`, `"Santander"`). |
| **`estadoResumen`** | `string` | `""` | Estado exacto del proceso seleccionado desde una lista desplegable con los valores reales del sistema (ej. `Presentación de oferta`, `Adjudicado`). |
| **`fechaDesde`** | `string` | – | Filtra procesos publicados en esta fecha o posterior (`AAAA-MM-DD`). |
| **`fechaHasta`** | `string` | – | Filtra procesos publicados en esta fecha o anterior (`AAAA-MM-DD`). |
| **`maxItems`** | `integer` | `1000` | Límite máximo de registros a extraer. |
| **`pageSize`** | `integer` | `1000` | Cantidad de registros solicitados por página (100 a 50.000). |
| **`appToken`** | `string` | – | Token opcional y gratuito de datos.gov.co para elevar los límites de solicitudes concurrentes. |
| **`whereClause`** | `string` | – | Cláusula avanzada de consulta SoQL `$where` para usuarios expertos. |

---

## Automatizaciones e Integraciones

Conecta SECOP II directamente con el stack tecnológico de tu empresa:

### 1. Alertas Diarias de Nuevas Licitaciones
Configura `fechaDesde` con la fecha de hoy o programa el Actor en la pestaña **Schedules** de Apify para que se ejecute todas las mañanas a las 7:00 AM. Vincula un Webhook para recibir las nuevas licitaciones en tu canal de **Slack**, **Microsoft Teams** o **correo electrónico**.

### 2. Conexión No-Code (Make / Zapier / Google Sheets)
Sincroniza automáticamente los procesos con un CRM (HubSpot, Salesforce) o una base de datos en **Airtable** o **Google Sheets** cada vez que se detecte una oportunidad que coincida con tus criterios comerciales.

### 3. Integración mediante API

#### Python
```python
from apify_client import ApifyClient

client = ApifyClient("TU_API_TOKEN")

run_input = {
    "keywords": ["infraestructura vial", "pavimentacion"],
    "departamento": "Antioquia",
    "estadoResumen": "Presentación de oferta",
    "maxItems": 100
}

run = client.actor("TU_USUARIO/secop-ii-contracting-processes").call(run_input=run_input)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"Proceso: {item['nombreDelProcedimiento']} | Presupuesto: ${item.get('precioBase'):,}")
```

#### Node.js / JavaScript
```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({
    token: 'TU_API_TOKEN',
});

const input = {
    keywords: ["seguridad informatica", "computo en la nube"],
    maxItems: 50
};

const run = await client.actor("TU_USUARIO/secop-ii-contracting-processes").call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();

console.log(`Se descargaron ${items.length} procesos de contratación.`);
console.table(items, ['entidad', 'nombreDelProcedimiento', 'precioBase', 'urlProceso']);
```

---

## Preguntas Frecuentes

#### ¿Necesito cuenta, usuario o cookies de SECOP para usar este Actor?
**No.** Este Actor consulta el repositorio oficial de datos públicos abiertos. No necesitas credenciales de acceso, ni certificados digitales, ni cuentas activas en SECOP.

#### ¿Puedo buscar múltiples sectores a la vez?
**Sí.** Puedes ingresar tantos términos como desees en el campo de palabras clave. El Actor procesará cada término de forma independiente, marcará cada contrato con la palabra clave correspondiente y te entregará el conteo exacto en el resumen `RUN_SUMMARY`.

#### ¿Por qué algunos procesos recientes no tienen proveedor adjudicado?
Los procesos que se encuentran en fases iniciales (como `Presentación de oferta` o `Fase de ofertas`) están abiertos a la recepción de propuestas, por lo que aún no cuentan con adjudicación formal ni contratista asignado. Si buscas contratos finalizados, utiliza el filtro de estado `Adjudicado`.

#### ¿Cómo evito duplicados al paginar miles de registros?
El Actor implementa un mecanismo de ordenamiento determinístico por fecha de publicación e ID único de registro, junto con un filtro de deduplicación en memoria, asegurando que cada proceso aparezca exactamente una vez en tu dataset.

---

## Soporte y Requerimientos a Medida

¿Necesitas análisis personalizados, integraciones directas con tu ERP/CRM o monitoreo continuo de contratación estatal? Escríbenos a través de la pestaña **Issues** en la página del Actor en Apify.
