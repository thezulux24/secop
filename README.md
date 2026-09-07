# SECOP II - Contracting Processes

Query Colombia's public procurement dataset (SECOP II, ~9.14 million contracting
processes) via its official Socrata API. Filter by keywords, entity, department, dates,
or a raw SoQL clause.

**This is not a scraper.** SECOP II's data is published through
[datos.gov.co](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Procesos-de-Contrataci-n/p6dx-8zbt/about_data)'s
own documented, public, unauthenticated REST API (Socrata SODA). No browser, no
impersonation, no cookies, no rate-limit games - this Actor just calls the API the way
it's meant to be called.

## What you get

Every record has **60 fields**, mirroring SECOP's own columns: entity identity, process
identity and status, every published-phase date, economics (base price, contract type,
duration), participation counts (invited/responding providers), award details, the
awarded provider, and a link to the process on SECOP's own site.

### Example record (trimmed)

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

## Input

| Field | Type | Notes |
|---|---|---|
| `keywords` | string | Full-text search (SoQL `$q`) across process name/description/entity |
| `entidad` | string | Partial, case-insensitive match on the contracting entity's name |
| `departamento` | string | Exact department name as SECOP records it |
| `estadoResumen` | string | Exact process status (e.g. `Adjudicado`, `Presentación de oferta`) |
| `fechaDesde` / `fechaHasta` | date | Filters on `fecha_de_publicacion_del` |
| `whereClause` | string | Advanced: a raw SoQL `$where` clause, ANDed with the filters above |
| `maxItems` | integer | Default 1000. The table has ~9.14M rows - filter before raising this |
| `pageSize` | integer | Records per API request (default 1000, max 50000) |
| `appToken` | string (secret) | Optional free Socrata app token - see below |

No filter is required; an empty query returns the most recently published processes.

## Do you need an account / cookie / API key?

**No login, no cookie.** This endpoint is genuinely public. The only optional credential
is a free **Socrata app token**: sign in at datos.gov.co -> Edit Profile -> Developer
Settings -> Create New App Token. It's an API usage token tied to your account, not a
session cookie - it just raises your rate limit for heavy/repeated use. In testing,
several rapid requests with no token at all returned zero throttling, so it's optional
for light use.

## Data quality notes (learned by testing against the live API)

- **Offset pagination over a live, ~9.14M-row table needs a stable sort key.** SECOP
  records publication dates at day precision only, so thousands of rows share the exact
  same value - `ORDER BY ... DESC` alone is non-deterministic across paginated requests
  and produces duplicate and skipped rows. This Actor orders by
  `fecha_de_publicacion_del DESC NULL LAST, :id` (Socrata's internal row id) to keep
  pagination stable, and **also deduplicates by `id_del_proceso` defensively** - a live
  3000-row pull without both fixes contained 129-197 exact-duplicate rows.
- **`NULL LAST` matters.** SoQL/Postgres's default `DESC` puts `NULL` values *first*,
  which would surface undated/incomplete records ahead of real ones.
- **Recent processes have empty award fields.** Sorted most-recent-first, freshly
  published processes are still in an early phase (`Presentación de oferta`, etc.) -
  `valorTotalAdjudicacion`, `nombreDelProveedor` and similar award fields are genuinely
  empty for them, not a bug. Filter `estadoResumen` or `fechaHasta` for a window further
  back if you need awarded contracts specifically.
- **Numbers and dates arrive as JSON strings** from the API (`"57333333"`, not `57333333`)
  and are cast to proper types (`float`/`int`/`date`) before being pushed.
- Records that fail validation go to a separate `INVALID` dataset with the raw row
  attached.

## Performance

Measured locally: **3000 records (with dedup) in ~11 s**, no proxy, no concurrency tuning
needed - the bottleneck is a handful of large sequential page requests, not a rate limit.
This is dramatically simpler and faster than an anti-bot-constrained scraper, because
there is no anti-bot to route around.

## Development

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src/ tests/

echo '{"keywords":"software","maxItems":25}' > storage/key_value_stores/default/INPUT.json
.venv/bin/python -m src
```

Deploy with `apify push`.

## Legal

This is Colombian government open data, published explicitly for public reuse under
[datos.gov.co](https://www.datos.gov.co)'s open data terms. No ToS conflict, no personal
data concerns beyond what the government itself already publishes (entity names, awarded
providers, contract values - all public record by design).
