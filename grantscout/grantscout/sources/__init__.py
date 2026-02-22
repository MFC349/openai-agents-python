"""Source registry – discover and instantiate all grant sources."""

from __future__ import annotations

from grantscout.sources.base import BaseSource
from grantscout.sources.grants_gov import GrantsGovSource
from grantscout.sources.sam_gov import SamGovSource

ALL_SOURCES: list[type[BaseSource]] = [GrantsGovSource, SamGovSource]

SOURCE_MAP: dict[str, type[BaseSource]] = {src.name: src for src in ALL_SOURCES}


def get_source(name: str) -> BaseSource:
    """Instantiate a source by its registered name."""
    cls = SOURCE_MAP.get(name)
    if cls is None:
        raise ValueError(f"Unknown source: {name!r}. Available: {list(SOURCE_MAP)}")
    return cls()


def list_sources() -> list[str]:
    return list(SOURCE_MAP)
