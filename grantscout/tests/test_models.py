"""Tests for Grant and ScrapeResult models – 10 tests."""

from datetime import date, datetime

import pytest

from grantscout.models import Grant, GrantStatus, ScrapeResult


# ── Grant creation and defaults ────────────────────────────────


def test_grant_defaults():
    g = Grant(id="1", title="Test", agency="DOE")
    assert g.status == GrantStatus.POSTED
    assert g.award_ceiling == 0.0
    assert g.keywords == []


def test_grant_status_is_open():
    assert GrantStatus.POSTED.is_open is True
    assert GrantStatus.FORECASTED.is_open is True
    assert GrantStatus.CLOSED.is_open is False
    assert GrantStatus.ARCHIVED.is_open is False


# ── Display helpers ────────────────────────────────────────────


def test_award_range_both():
    g = Grant(id="1", title="T", agency="A", award_floor=10000, award_ceiling=50000)
    assert g.award_range == "$10,000 – $50,000"


def test_award_range_ceiling_only():
    g = Grant(id="1", title="T", agency="A", award_ceiling=100000)
    assert g.award_range == "up to $100,000"


def test_award_range_none():
    g = Grant(id="1", title="T", agency="A")
    assert g.award_range == "N/A"


def test_short_description_truncation():
    desc = "A" * 200
    g = Grant(id="1", title="T", agency="A", description=desc)
    short = g.short_description(50)
    assert len(short) == 50
    assert short.endswith("...")


def test_is_open_with_future_close():
    g = Grant(id="1", title="T", agency="A", close_date=date(2099, 12, 31))
    assert g.is_open is True


def test_is_open_with_past_close():
    g = Grant(id="1", title="T", agency="A", close_date=date(2020, 1, 1))
    assert g.is_open is False


# ── Serialization round-trip ───────────────────────────────────


def test_grant_to_dict_and_back():
    g = Grant(
        id="g1",
        title="Climate Grant",
        agency="EPA",
        status=GrantStatus.FORECASTED,
        close_date=date(2025, 6, 15),
        posted_date=date(2025, 1, 1),
    )
    d = g.to_dict()
    assert d["status"] == "forecasted"
    assert d["close_date"] == "2025-06-15"

    g2 = Grant.from_dict(d)
    assert g2.id == g.id
    assert g2.status == GrantStatus.FORECASTED
    assert g2.close_date == date(2025, 6, 15)


def test_grant_to_json():
    g = Grant(id="1", title="T", agency="A")
    j = g.to_json()
    assert '"id": "1"' in j


# ── ScrapeResult ───────────────────────────────────────────────


def test_scrape_result_merge_dedup():
    g1 = Grant(id="dup", title="Same", agency="A")
    g2 = Grant(id="dup", title="Same", agency="A")
    g3 = Grant(id="unique", title="Other", agency="B")

    r1 = ScrapeResult(source="s1", grants=[g1])
    r2 = ScrapeResult(source="s2", grants=[g2, g3])
    merged = r1.merge(r2)
    assert merged.count == 2
    ids = [g.id for g in merged.grants]
    assert ids == ["dup", "unique"]
