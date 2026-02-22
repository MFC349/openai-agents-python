"""Tests for exporter – 7 tests covering CSV/JSON file creation and validation."""

import csv
import json
import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from grantscout.exporter import export_csv, export_json, print_table
from grantscout.models import Grant, GrantStatus


@pytest.fixture()
def sample_grants():
    return [
        Grant(
            id="g1",
            title="Health Research",
            agency="NIH",
            status=GrantStatus.POSTED,
            award_ceiling=500000,
            award_floor=50000,
            close_date=date(2025, 12, 31),
            posted_date=date(2025, 1, 15),
            url="https://example.com/g1",
            source="grants_gov",
        ),
        Grant(
            id="g2",
            title="Climate Study",
            agency="EPA",
            status=GrantStatus.FORECASTED,
            award_ceiling=100000,
            source="sam_gov",
        ),
    ]


@pytest.fixture()
def tmp_output(tmp_path):
    with patch("grantscout.exporter.config") as mock_cfg:
        mock_cfg.ensure_output_dir.return_value = tmp_path
        yield tmp_path


# ── CSV tests ──────────────────────────────────────────────────


def test_export_csv_creates_file(sample_grants, tmp_output):
    path = export_csv(sample_grants)
    assert path.exists()
    assert path.suffix == ".csv"


def test_export_csv_has_header(sample_grants, tmp_output):
    path = export_csv(sample_grants)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert "title" in reader.fieldnames
        assert "agency" in reader.fieldnames


def test_export_csv_row_count(sample_grants, tmp_output):
    path = export_csv(sample_grants)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2


def test_export_csv_content(sample_grants, tmp_output):
    path = export_csv(sample_grants)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows[0]["title"] == "Health Research"
    assert rows[0]["agency"] == "NIH"


# ── JSON tests ─────────────────────────────────────────────────


def test_export_json_creates_file(sample_grants, tmp_output):
    path = export_json(sample_grants)
    assert path.exists()
    assert path.suffix == ".json"


def test_export_json_valid(sample_grants, tmp_output):
    path = export_json(sample_grants)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 2


def test_export_json_content(sample_grants, tmp_output):
    path = export_json(sample_grants)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data[0]["id"] == "g1"
    assert data[1]["status"] == "forecasted"
