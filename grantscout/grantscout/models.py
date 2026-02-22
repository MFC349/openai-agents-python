"""Grant and ScrapeResult dataclasses."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class GrantStatus(str, Enum):
    """Lifecycle status for a grant opportunity."""

    FORECASTED = "forecasted"
    POSTED = "posted"
    CLOSED = "closed"
    ARCHIVED = "archived"

    @property
    def is_open(self) -> bool:
        return self in (GrantStatus.FORECASTED, GrantStatus.POSTED)


@dataclass
class Grant:
    """A single funding opportunity."""

    id: str
    title: str
    agency: str
    description: str = ""
    status: GrantStatus = GrantStatus.POSTED
    award_ceiling: float = 0.0
    award_floor: float = 0.0
    close_date: date | None = None
    posted_date: date | None = None
    url: str = ""
    source: str = ""
    keywords: list[str] = field(default_factory=list)

    # ── Display helpers ────────────────────────────────────────

    @property
    def award_range(self) -> str:
        if self.award_ceiling and self.award_floor:
            return f"${self.award_floor:,.0f} – ${self.award_ceiling:,.0f}"
        if self.award_ceiling:
            return f"up to ${self.award_ceiling:,.0f}"
        return "N/A"

    @property
    def days_until_close(self) -> int | None:
        if self.close_date is None:
            return None
        return (self.close_date - date.today()).days

    @property
    def is_open(self) -> bool:
        if self.status and not self.status.is_open:
            return False
        if self.close_date and self.close_date < date.today():
            return False
        return True

    def short_description(self, max_len: int = 120) -> str:
        if len(self.description) <= max_len:
            return self.description
        return self.description[: max_len - 3] + "..."

    # ── Serialization ──────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        for key in ("close_date", "posted_date"):
            val = d.get(key)
            if isinstance(val, date):
                d[key] = val.isoformat()
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Grant:
        data = dict(data)
        if "status" in data and isinstance(data["status"], str):
            data["status"] = GrantStatus(data["status"])
        for key in ("close_date", "posted_date"):
            val = data.get(key)
            if isinstance(val, str):
                data[key] = date.fromisoformat(val)
        return cls(**data)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class ScrapeResult:
    """Outcome of a single scraping run."""

    source: str
    grants: list[Grant] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    finished_at: datetime | None = None

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    @property
    def count(self) -> int:
        return len(self.grants)

    def merge(self, other: ScrapeResult) -> ScrapeResult:
        """Combine two results, deduplicating grants by id."""
        seen: set[str] = set()
        merged: list[Grant] = []
        for g in self.grants + other.grants:
            if g.id not in seen:
                seen.add(g.id)
                merged.append(g)
        return ScrapeResult(
            source=f"{self.source}+{other.source}",
            grants=merged,
            errors=self.errors + other.errors,
            started_at=min(self.started_at, other.started_at),
            finished_at=max(
                self.finished_at or self.started_at,
                other.finished_at or other.started_at,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "grants": [g.to_dict() for g in self.grants],
            "errors": self.errors,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "count": self.count,
            "success": self.success,
        }
