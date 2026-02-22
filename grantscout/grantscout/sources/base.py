"""Abstract base source with retry and rate-limit logic."""

from __future__ import annotations

import abc
import time
from datetime import datetime

import httpx

from grantscout.config import config
from grantscout.logger import log
from grantscout.models import Grant, ScrapeResult


class BaseSource(abc.ABC):
    """Every grant source must subclass this and implement ``fetch``."""

    name: str = "base"
    base_url: str = ""

    def __init__(self) -> None:
        self._cfg = config.scraper

    # ── Public interface ───────────────────────────────────────

    def scrape(self, keywords: list[str] | None = None) -> ScrapeResult:
        """Run a scrape with retry and rate-limit wrapping."""
        result = ScrapeResult(source=self.name, started_at=datetime.now())
        try:
            grants = self._with_retry(lambda: self.fetch(keywords or []))
            result.grants = grants
        except Exception as exc:
            log.error("[%s] scrape failed: %s", self.name, exc)
            result.errors.append(str(exc))
        result.finished_at = datetime.now()
        return result

    # ── Subclass contract ──────────────────────────────────────

    @abc.abstractmethod
    def fetch(self, keywords: list[str]) -> list[Grant]:
        """Fetch grants from the upstream API. Must be implemented by subclasses."""
        ...

    # ── Internals ──────────────────────────────────────────────

    def _with_retry(self, fn: object) -> list[Grant]:
        """Call *fn* up to ``max_retries`` times with rate-limit delay."""
        last_exc: Exception | None = None
        for attempt in range(1, self._cfg.max_retries + 1):
            try:
                return fn()  # type: ignore[operator]
            except (httpx.HTTPStatusError, httpx.RequestError) as exc:
                last_exc = exc
                wait = self._cfg.rate_limit_delay * attempt
                log.warning(
                    "[%s] attempt %d/%d failed (%s), retrying in %.1fs",
                    self.name,
                    attempt,
                    self._cfg.max_retries,
                    exc,
                    wait,
                )
                time.sleep(wait)
        raise RuntimeError(
            f"[{self.name}] all {self._cfg.max_retries} attempts failed"
        ) from last_exc

    def _get_json(self, url: str, params: dict | None = None) -> dict:
        """Issue a GET request and return the JSON body."""
        with httpx.Client(timeout=self._cfg.request_timeout) as client:
            resp = client.get(url, params=params or {})
            resp.raise_for_status()
            return resp.json()
