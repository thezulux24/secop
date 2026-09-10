"""SECOP II Actor: query the official Socrata API and push validated records.

Plain JSON API, no anti-bot concerns. The interesting parts of this Actor are query
building (see src/soda.py) and staying memory-safe over a ~9.14M-row table.
"""

from __future__ import annotations

from collections import Counter

from apify import Actor
from pydantic import ValidationError

from . import soda
from .client import SodaClient
from .models import Process

PUSH_BATCH = 500


def _keyword_terms(raw: object) -> list[str]:
    """Normalize the `keywords` input into a deduped list of non-empty terms.

    Accepts the new list-of-strings shape as well as a bare string (older saved inputs,
    or a user typing one term directly), so existing input JSON keeps working.
    """
    if isinstance(raw, str):
        raw = [raw]
    terms: list[str] = []
    for item in raw or []:
        term = (item or '').strip() if isinstance(item, str) else ''
        if term and term not in terms:
            terms.append(term)
    return terms


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}

        terms = _keyword_terms(actor_input.get('keywords'))
        where = soda.build_where(
            entidad=(actor_input.get('entidad') or '').strip() or None,
            departamento=(actor_input.get('departamento') or '').strip() or None,
            estado_resumen=(actor_input.get('estadoResumen') or '').strip() or None,
            fecha_desde=(actor_input.get('fechaDesde') or '').strip() or None,
            fecha_hasta=(actor_input.get('fechaHasta') or '').strip() or None,
            extra=(actor_input.get('whereClause') or '').strip() or None,
        )

        max_items = int(actor_input.get('maxItems') or 1000)
        page_size = int(actor_input.get('pageSize') or soda.DEFAULT_PAGE_SIZE)
        app_token = actor_input.get('appToken') or None

        # One search run per keyword term, each tagged and counted on its own, so "which
        # term found what" is visible in the output and in RUN_SUMMARY. No terms at all
        # means a single untagged run (browse by the other filters, or most recent first).
        runs: list[str | None] = terms if terms else [None]

        state = await Actor.use_state(
            default_value={'run_index': 0, 'offset': 0, 'pushed': 0, 'counts': {}}
        )
        stats: Counter = Counter()

        client = SodaClient(app_token=app_token, logger=Actor.log)
        buffer: list[dict] = []
        # Offset pagination over a ~9M-row table that's written to continuously (plus,
        # apparently, some genuine re-published duplicates in the source itself) can hand
        # back the same process more than once across adjacent pages. Dedup defensively
        # by id_del_proceso regardless of the exact cause - confirmed live: without this,
        # a 3000-row pull over a live query contained >100 exact-duplicate rows. This dedup
        # is global across terms too, so a process matching two search terms is only pushed
        # once (tagged with whichever term surfaced it first).
        seen_process_ids: set[str] = set()

        async def flush() -> None:
            if buffer:
                await Actor.push_data(buffer)
                state['pushed'] += len(buffer)
                buffer.clear()

        def budget_left() -> int:
            return max_items - (state['pushed'] + len(buffer))

        aborted = False

        try:
            await Actor.set_status_message('Consultando SECOP II...')

            while state['run_index'] < len(runs) and budget_left() > 0:
                term = runs[state['run_index']]
                label = term or '(no keyword)'

                while budget_left() > 0:
                    params = soda.build_params(
                        keywords=term,
                        where=where,
                        limit=min(page_size, budget_left()),
                        offset=state['offset'],
                    )

                    try:
                        rows = await client.fetch_page(params)
                    except Exception:  # noqa: BLE001 - a bad page must stop the run cleanly, not crash it
                        Actor.log.exception(
                            'Fallo al consultar la página en offset=%s (término=%s)', state['offset'], label
                        )
                        stats['page_failed'] += 1
                        aborted = True
                        break

                    if not rows:
                        Actor.log.info(
                            'No hay más filas en offset=%s (término=%s) - consulta agotada.',
                            state['offset'], label,
                        )
                        break

                    for row in rows:
                        process_id = row.get('id_del_proceso')
                        if process_id and process_id in seen_process_ids:
                            stats['duplicate'] += 1
                            continue
                        if process_id:
                            seen_process_ids.add(process_id)

                        try:
                            buffer.append(
                                Process.from_soda_row(row, search_keywords=term).to_dataset()
                            )
                            stats['ok'] += 1
                            state['counts'][label] = state['counts'].get(label, 0) + 1
                        except ValidationError as exc:
                            stats['invalid'] += 1
                            Actor.log.warning('Fila inválida: %s', exc.errors()[:2])
                            invalid = await Actor.open_dataset(name='INVALID')
                            await invalid.push_data({'raw': row, 'errors': str(exc.errors()[:3])})

                    page_len = len(rows)
                    state['offset'] += page_len

                    if len(buffer) >= PUSH_BATCH:
                        await flush()
                        await Actor.set_status_message(
                            f'"{label}": {state["counts"].get(label, 0)} encontrados - '
                            f'{state["pushed"]} en total...'
                        )

                    if page_len < int(params['$limit']):
                        # A short page means this term's query is exhausted.
                        break

                state['run_index'] += 1
                state['offset'] = 0
                if aborted:
                    break

            await flush()

        finally:
            await client.close()

        if state['pushed'] == 0 and stats['page_failed']:
            await Actor.fail(
                status_message='No se pudo conectar con la API de SECOP II. Puede estar '
                'caída temporalmente - revisa https://www.datos.gov.co e inténtalo de nuevo.'
            )
            return

        Actor.log.info(
            'Listo. registros=%s por_termino=%s stats=%s', state['pushed'], state['counts'], dict(stats)
        )
        await Actor.set_value(
            'RUN_SUMMARY', {'records': state['pushed'], 'byKeyword': state['counts'], **stats}
        )
