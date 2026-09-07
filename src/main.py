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


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}

        keywords = (actor_input.get('keywords') or '').strip() or None
        where = soda.build_where(
            entidad=(actor_input.get('entidad') or '').strip() or None,
            departamento=(actor_input.get('departamento') or '').strip() or None,
            estado_resumen=(actor_input.get('estadoResumen') or '').strip() or None,
            fecha_desde=(actor_input.get('fechaDesde') or '').strip() or None,
            fecha_hasta=(actor_input.get('fechaHasta') or '').strip() or None,
            extra=(actor_input.get('whereClause') or '').strip() or None,
        )

        max_items = int(actor_input.get('maxItems') or 1000)
        page_size = min(int(actor_input.get('pageSize') or soda.DEFAULT_PAGE_SIZE), max_items)
        app_token = actor_input.get('appToken') or None

        state = await Actor.use_state(default_value={'offset': 0, 'pushed': 0})
        stats: Counter = Counter()

        client = SodaClient(app_token=app_token, logger=Actor.log)
        buffer: list[dict] = []
        # Offset pagination over a ~9M-row table that's written to continuously (plus,
        # apparently, some genuine re-published duplicates in the source itself) can hand
        # back the same process more than once across adjacent pages. Dedup defensively
        # by id_del_proceso regardless of the exact cause - confirmed live: without this,
        # a 3000-row pull over a live query contained >100 exact-duplicate rows.
        seen_process_ids: set[str] = set()

        async def flush() -> None:
            if buffer:
                await Actor.push_data(buffer)
                state['pushed'] += len(buffer)
                buffer.clear()

        try:
            offset = state['offset']
            await Actor.set_status_message('Querying SECOP II...')

            while state['pushed'] + len(buffer) < max_items:
                remaining = max_items - (state['pushed'] + len(buffer))
                params = soda.build_params(
                    keywords=keywords,
                    where=where,
                    limit=min(page_size, remaining),
                    offset=offset,
                )

                try:
                    rows = await client.fetch_page(params)
                except Exception:  # noqa: BLE001 - a bad page must stop the run cleanly, not crash it
                    Actor.log.exception('Page fetch failed at offset=%s', offset)
                    stats['page_failed'] += 1
                    break

                if not rows:
                    Actor.log.info('No more rows at offset=%s - query exhausted.', offset)
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
                            Process.from_soda_row(row, search_keywords=keywords).to_dataset()
                        )
                        stats['ok'] += 1
                    except ValidationError as exc:
                        stats['invalid'] += 1
                        Actor.log.warning('Invalid row: %s', exc.errors()[:2])
                        invalid = await Actor.open_dataset(name='INVALID')
                        await invalid.push_data({'raw': row, 'errors': str(exc.errors()[:3])})

                offset += len(rows)
                state['offset'] = offset

                if len(buffer) >= PUSH_BATCH:
                    await flush()
                    await Actor.set_status_message(f'{state["pushed"]} records fetched...')

                if len(rows) < int(params['$limit']):
                    # A short page means the query is exhausted - no point requesting more.
                    break

            await flush()

        finally:
            await client.close()

        if state['pushed'] == 0 and stats['page_failed']:
            await Actor.fail(
                status_message='Could not reach the SECOP II API. It may be temporarily '
                'down - check https://www.datos.gov.co and try again.'
            )
            return

        Actor.log.info('Done. records=%s stats=%s', state['pushed'], dict(stats))
        await Actor.set_value('RUN_SUMMARY', {'records': state['pushed'], **stats})
