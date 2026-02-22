"""Export grants to CSV, JSON, and Rich table output."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from rich.table import Table

from grantscout.config import config
from grantscout.logger import console, log
from grantscout.models import Grant


def export_csv(grants: list[Grant], filename: str = "grants.csv") -> Path:
    """Write grants to a CSV file and return the path."""
    out_dir = config.ensure_output_dir()
    path = out_dir / filename
    fieldnames = [
        "id",
        "title",
        "agency",
        "status",
        "award_range",
        "close_date",
        "posted_date",
        "url",
        "source",
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for g in grants:
            writer.writerow(
                {
                    "id": g.id,
                    "title": g.title,
                    "agency": g.agency,
                    "status": g.status.value,
                    "award_range": g.award_range,
                    "close_date": g.close_date.isoformat() if g.close_date else "",
                    "posted_date": g.posted_date.isoformat() if g.posted_date else "",
                    "url": g.url,
                    "source": g.source,
                }
            )
    log.info("Exported %d grants to %s", len(grants), path)
    return path


def export_json(grants: list[Grant], filename: str = "grants.json") -> Path:
    """Write grants to a JSON file and return the path."""
    out_dir = config.ensure_output_dir()
    path = out_dir / filename
    data = [g.to_dict() for g in grants]
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    log.info("Exported %d grants to %s", len(grants), path)
    return path


def print_table(grants: list[Grant], title: str = "Grant Opportunities") -> None:
    """Render grants as a Rich table in the console."""
    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="dim", max_width=25)
    table.add_column("Title", style="bold cyan", max_width=50)
    table.add_column("Agency", max_width=30)
    table.add_column("Status", justify="center")
    table.add_column("Award Range", justify="right")
    table.add_column("Close Date", justify="center")
    table.add_column("Source", style="dim")

    status_style = {
        "posted": "green",
        "forecasted": "yellow",
        "closed": "red",
        "archived": "dim",
    }

    for g in grants:
        style = status_style.get(g.status.value, "")
        close = g.close_date.isoformat() if g.close_date else "—"
        table.add_row(
            g.id,
            g.short_description(50) if not g.title else g.title,
            g.agency,
            f"[{style}]{g.status.value}[/{style}]" if style else g.status.value,
            g.award_range,
            close,
            g.source,
        )

    console.print(table)
