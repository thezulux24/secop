"""Regression tests for SoQL query building and SODA row parsing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import soda
from src.models import Process

FIXTURES = Path(__file__).parent / 'fixtures'


def load_rows() -> list[dict]:
    return json.loads((FIXTURES / 'sample_rows.json').read_text())


# --------------------------------------------------------------------- soda.build_where

def test_build_where_empty_when_no_filters():
    assert soda.build_where() is None


def test_build_where_combines_with_and():
    where = soda.build_where(entidad='alcaldia', departamento='Antioquia')
    assert 'AND' in where
    assert "upper(entidad) like upper('%alcaldia%')" in where
    assert "departamento_entidad = 'Antioquia'" in where


def test_build_where_escapes_single_quotes():
    where = soda.build_where(entidad="O'Brien")
    assert "O''Brien" in where
    assert where.count("'") % 2 == 0  # every literal is still properly closed


def test_build_where_date_range():
    where = soda.build_where(fecha_desde='2026-01-01', fecha_hasta='2026-01-31')
    assert "fecha_de_publicacion_del >= '2026-01-01T00:00:00'" in where
    assert "fecha_de_publicacion_del <= '2026-01-31T23:59:59'" in where


def test_build_where_extra_is_parenthesized():
    where = soda.build_where(extra='precio_base > 1000000')
    assert where == '(precio_base > 1000000)'


# --------------------------------------------------------------------- soda.build_params

def test_build_params_defaults():
    params = soda.build_params()
    assert params['$limit'] == str(soda.DEFAULT_PAGE_SIZE)
    assert params['$offset'] == '0'
    assert '$q' not in params
    assert '$where' not in params


def test_build_params_default_order_puts_nulls_last():
    # Regression: SoQL/Postgres DESC defaults to NULLS FIRST, which surfaced undated
    # (incomplete) records ahead of real ones. Must be explicit about NULL LAST.
    params = soda.build_params()
    assert 'NULL LAST' in params['$order']


def test_build_params_caps_page_size():
    params = soda.build_params(limit=soda.MAX_PAGE_SIZE + 50000)
    assert int(params['$limit']) == soda.MAX_PAGE_SIZE


def test_build_params_includes_keywords_and_where():
    params = soda.build_params(keywords='software', where="entidad = 'x'")
    assert params['$q'] == 'software'
    assert params['$where'] == "entidad = 'x'"


# --------------------------------------------------------------------- soda type helpers

@pytest.mark.parametrize(
    ('raw', 'expected'),
    [('57333333', 57333333.0), ('0', 0.0), (None, None), ('', None), ('No Definido', None)],
)
def test_to_number(raw, expected):
    assert soda.to_number(raw) == expected


def test_to_int_truncates():
    assert soda.to_int('344') == 344
    assert soda.to_int(None) is None


def test_unwrap_url_from_socrata_url_field():
    assert soda.unwrap_url({'url': 'https://x.com', 'description': 'x'}) == 'https://x.com'
    assert soda.unwrap_url('https://bare.com') == 'https://bare.com'
    assert soda.unwrap_url(None) is None
    assert soda.unwrap_url(123) is None


# --------------------------------------------------------------------- Process.from_soda_row

def test_parses_real_fixture_rows():
    rows = load_rows()
    assert len(rows) == 5
    for row in rows:
        process = Process.from_soda_row(row, search_keywords='test')
        data = process.to_dataset()
        assert data['entidad'] == row.get('entidad')
        assert len(data) >= 55  # all mapped fields present, even if null


def test_precio_base_is_numeric_not_string():
    rows = load_rows()
    process = Process.from_soda_row(rows[0])
    if rows[0].get('precio_base') is not None:
        assert isinstance(process.precio_base, float)


def test_missing_fields_do_not_crash():
    process = Process.from_soda_row({})
    data = process.to_dataset()
    assert data['entidad'] is None
    assert data['precioBase'] is None
