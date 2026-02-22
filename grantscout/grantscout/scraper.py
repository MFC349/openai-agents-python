"""Scraper engine – multi-source orchestration, merge, and filter."""

from __future__ import annotations

from datetime import datetime

from grantscout.logger import log
from grantscout.models import Grant, ScrapeResult
from grantscout.sources import ALL_SOURCES, get_source, list_sources
from grantscout.sources.base import BaseSource


def scrape_all(
    keywords: list[str] | None = None,
    sources: list[str] | None = None,
    open_only: bool = False,
    min_award: float = 0,
    max_award: float = 0,
) -> ScrapeResult:
    """Run a scrape across the requested (or all) sources and merge results."""
    source_names = sources or list_sources()
    log.info("Starting scrape across sources: %s", source_names)

    combined = ScrapeResult(source="combined", started_at=datetime.now())

    for name in source_names:
        src: BaseSource = get_source(name)
        result = src.scrape(keywords)
        combined = combined.merge(result)

    # Apply filters.
    combined.grants = filter_grants(
        combined.grants,
        open_only=open_only,
        min_award=min_award,
        max_award=max_award,
        keywords=keywords,
    )

    combined.finished_at = datetime.now()
    log.info(
        "Scrape complete: %d grants, %d errors",
        combined.count,
        len(combined.errors),
    )
    return combined


def filter_grants(
    grants: list[Grant],
    *,
    open_only: bool = False,
    min_award: float = 0,
    max_award: float = 0,
    keywords: list[str] | None = None,
) -> list[Grant]:
    """Filter a list of grants by status, award range, and keyword match."""
    filtered = list(grants)

    if open_only:
        filtered = [g for g in filtered if g.is_open]

    if min_award > 0:
        filtered = [g for g in filtered if g.award_ceiling >= min_award]

    if max_award > 0:
        filtered = [g for g in filtered if g.award_floor <= max_award or g.award_floor == 0]

    if keywords:
        kw_lower = [k.lower() for k in keywords]
        filtered = [g for g in filtered if _matches_keywords(g, kw_lower)]

    return filtered


def _matches_keywords(grant: Grant, keywords_lower: list[str]) -> bool:
    """Check if any keyword appears in the grant title or description."""
    text = f"{grant.title} {grant.description}".lower()
    return any(kw in text for kw in keywords_lower)


def merge_results(results: list[ScrapeResult]) -> ScrapeResult:
    """Merge multiple ScrapeResults with deduplication by grant id."""
    if not results:
        return ScrapeResult(source="empty")
    merged = results[0]
    for r in results[1:]:
        merged = merged.merge(r)
    return merged
