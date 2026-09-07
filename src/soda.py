"""SECOP II via Socrata's SODA (Open Data) API - a genuinely public JSON REST API.

No browser, no impersonation, no login: this is the platform's own documented endpoint,
used the way it is meant to be used. Confirmed live (2026-09-07):

  BASE      https://www.datos.gov.co/resource/p6dx-8zbt.json
  ROWS      ~9.14M and growing (SELECT count(*) via $select)
  AUTH      none required; an optional free "app token" raises the rate limit
  QUERY     SoQL via query params: $select, $where, $order, $q, $limit, $offset
  LIMITS    $limit up to at least 100000 confirmed working; default to something far
            smaller per request (this module defaults callers to 1000) to keep memory
            and single-response size sane - the dataset has 59 columns per row.
  QUIRKS    - Numbers and dates are serialized as JSON strings, not native JSON types.
            - Some columns (e.g. `urlproceso`) are Socrata "url" fields: an object
              `{"url": "..."}` rather than a bare string.
            - Null fields are omitted from the JSON entirely rather than sent as null -
              every accessor must tolerate a missing key.
"""

from __future__ import annotations

from typing import Any

BASE_URL = 'https://www.datos.gov.co/resource/p6dx-8zbt.json'
DEFAULT_PAGE_SIZE = 1000
MAX_PAGE_SIZE = 50000


def _escape_soql_string(value: str) -> str:
    """Escape a value for embedding in a SoQL string literal ('...')."""
    return value.replace("'", "''")


def build_where(
    *,
    entidad: str | None = None,
    departamento: str | None = None,
    estado_resumen: str | None = None,
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
    extra: str | None = None,
) -> str | None:
    """Combine the convenience filters into one SoQL $where clause, ANDed with `extra`."""
    clauses: list[str] = []

    if entidad:
        clauses.append(f"upper(entidad) like upper('%{_escape_soql_string(entidad)}%')")
    if departamento:
        clauses.append(f"departamento_entidad = '{_escape_soql_string(departamento)}'")
    if estado_resumen:
        clauses.append(f"estado_resumen = '{_escape_soql_string(estado_resumen)}'")
    if fecha_desde:
        clauses.append(f"fecha_de_publicacion_del >= '{_escape_soql_string(fecha_desde)}T00:00:00'")
    if fecha_hasta:
        clauses.append(f"fecha_de_publicacion_del <= '{_escape_soql_string(fecha_hasta)}T23:59:59'")
    if extra:
        clauses.append(f'({extra})')

    return ' AND '.join(clauses) if clauses else None


def build_params(
    *,
    keywords: str | None = None,
    where: str | None = None,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = 0,
    # NULLS FIRST is Postgres/SoQL's default on DESC, which would surface incomplete
    # (undated) records ahead of real ones - NULL LAST gives "most recent first" the
    # way a user actually expects it. The trailing :id is a stable tiebreaker: thousands
    # of rows share the same publication date (day-level precision only), and offset
    # pagination over a tied sort key is non-deterministic between requests - it silently
    # duplicates and skips rows as the underlying ~9M-row table keeps getting written to.
    order: str = 'fecha_de_publicacion_del DESC NULL LAST, :id',
) -> dict[str, str]:
    """Build the SoQL query-string params for one page."""
    params: dict[str, str] = {
        '$limit': str(min(limit, MAX_PAGE_SIZE)),
        '$offset': str(offset),
        '$order': order,
    }
    if keywords:
        params['$q'] = keywords
    if where:
        params['$where'] = where
    return params


def unwrap_url(value: Any) -> str | None:
    """Socrata 'url' columns come back as {"url": "...", "description": "..."} or a bare str."""
    if isinstance(value, dict):
        return value.get('url')
    return value if isinstance(value, str) else None


def to_number(value: Any) -> float | None:
    """Socrata serializes numeric columns as JSON strings ("57333333")."""
    if value in (None, '', 'No Definido', 'No Definida'):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: Any) -> int | None:
    n = to_number(value)
    return int(n) if n is not None else None
