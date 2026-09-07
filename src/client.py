"""HTTP layer for the SODA API. Plain httpx - no impersonation needed.

This is a genuinely public, unauthenticated, non-hostile JSON API (confirmed live: 0/15
requests blocked in a burst with no app token, no rate-limit headers exposed). The only
resilience this needs is standard transient-fault retry, not anti-bot evasion.
"""

from __future__ import annotations

import asyncio
import random

import httpx

from .soda import BASE_URL

RETRIABLE_STATUS = {408, 429, 500, 502, 503, 504}
TIMEOUT = httpx.Timeout(60.0, connect=15.0)


class SodaClient:
    def __init__(self, *, app_token: str | None = None, logger=None) -> None:
        headers = {'Accept': 'application/json'}
        if app_token:
            headers['X-App-Token'] = app_token
        self._client = httpx.AsyncClient(headers=headers, timeout=TIMEOUT, follow_redirects=True)
        self._log = logger

    async def fetch_page(self, params: dict[str, str], *, attempts: int = 5) -> list[dict]:
        """GET one page of rows. Raises on a non-retriable error or exhausted attempts."""
        last_error: Exception | None = None

        for attempt in range(attempts):
            try:
                response = await self._client.get(BASE_URL, params=params)
            except httpx.TransportError as exc:
                last_error = exc
            else:
                if response.status_code == 200:
                    return response.json()
                if response.status_code not in RETRIABLE_STATUS:
                    response.raise_for_status()
                last_error = httpx.HTTPStatusError(
                    f'HTTP {response.status_code}', request=response.request, response=response
                )
                retry_after = response.headers.get('retry-after')
                if retry_after and retry_after.isdigit():
                    await asyncio.sleep(min(int(retry_after), 60))
                    continue

            if attempt < attempts - 1:
                delay = min(30.0, 1.0 * 2**attempt) * random.uniform(0.5, 1.5)
                if self._log:
                    self._log.warning('retry %s/%s in %.1fs: %s', attempt + 1, attempts, delay, last_error)
                await asyncio.sleep(delay)

        raise last_error or RuntimeError('failed to fetch page')

    async def close(self) -> None:
        await self._client.aclose()
