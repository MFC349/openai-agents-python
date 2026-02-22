"""Tests for scraper – 6 tests covering merge dedup and filtering."""

from datetime import date

import pytest

from grantscout.models import Grant, GrantStatus, ScrapeResult
from grantscout.scraper import filter_grants, merge_results


def _make_grant(
    id: str = "1",
    title: str = "Test Grant",
    agency: str = "DOE",
    status: GrantStatus = GrantStatus.POSTED,
    award_ceiling: float = 100000,
    award_floor: float = 10000,
    close_date: date | None = None,
    description: str = "",
) -> Grant:
    return Grant(
        id=id,
        title=title,
        agency=agency,
        status=status,
        award_ceiling=award_ceiling,
        award_floor=award_floor,
        close_date=close_date,
        description=description,
    )


# ── Merge dedup ────────────────────────────────────────────────


def test_merge_results_empty():
    merged = merge_results([])
    assert merged.count == 0
    assert merged.source == "empty"


def test_merge_results_dedup():
    r1 = ScrapeResult(source="a", grants=[_make_grant(id="dup"), _make_grant(id="x")])
    r2 = ScrapeResult(source="b", grants=[_make_grant(id="dup"), _make_grant(id="y")])
    merged = merge_results([r1, r2])
    assert merged.count == 3
    ids = {g.id for g in merged.grants}
    assert ids == {"dup", "x", "y"}


# ── Filtering ──────────────────────────────────────────────────


def test_filter_open_only():
    grants = [
        _make_grant(id="open", close_date=date(2099, 1, 1)),
        _make_grant(id="closed", status=GrantStatus.CLOSED),
    ]
    result = filter_grants(grants, open_only=True)
    assert len(result) == 1
    assert result[0].id == "open"


def test_filter_min_award():
    grants = [
        _make_grant(id="big", award_ceiling=500000),
        _make_grant(id="small", award_ceiling=1000),
    ]
    result = filter_grants(grants, min_award=100000)
    assert len(result) == 1
    assert result[0].id == "big"


def test_filter_max_award():
    grants = [
        _make_grant(id="cheap", award_floor=5000),
        _make_grant(id="expensive", award_floor=200000),
    ]
    result = filter_grants(grants, max_award=10000)
    assert len(result) == 1
    assert result[0].id == "cheap"


def test_filter_keywords():
    grants = [
        _make_grant(id="match", title="Health Research Grant"),
        _make_grant(id="miss", title="Transportation Study"),
    ]
    result = filter_grants(grants, keywords=["health"])
    assert len(result) == 1
    assert result[0].id == "match"
