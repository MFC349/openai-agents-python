"""CLI – 5 Typer commands: scrape, watch, sources, config, export."""

from __future__ import annotations

import time
from typing import Optional

import typer
from typing_extensions import Annotated

from grantscout import __version__
from grantscout.alerter import send_alerts
from grantscout.exporter import export_csv, export_json, print_table
from grantscout.logger import console, log
from grantscout.scraper import scrape_all
from grantscout.sources import list_sources

app = typer.Typer(
    name="grantscout",
    help="Automated grant discovery – scrape, filter, alert, and export federal funding opportunities.",
    add_completion=False,
)


@app.command()
def scrape(
    keywords: Annotated[
        Optional[list[str]],
        typer.Option("-k", "--keyword", help="Keywords to search for"),
    ] = None,
    sources: Annotated[
        Optional[list[str]],
        typer.Option("-s", "--source", help="Sources to query (default: all)"),
    ] = None,
    open_only: Annotated[
        bool, typer.Option("--open", help="Only show open opportunities")
    ] = False,
    min_award: Annotated[
        float, typer.Option("--min-award", help="Minimum award ceiling")
    ] = 0,
    max_award: Annotated[
        float, typer.Option("--max-award", help="Maximum award floor")
    ] = 0,
    output: Annotated[
        str, typer.Option("-o", "--output", help="Output format: table, csv, json")
    ] = "table",
    alert: Annotated[
        bool, typer.Option("--alert", help="Send alerts for results")
    ] = False,
) -> None:
    """Scrape grant opportunities from configured sources."""
    console.print(f"[bold]GrantScout v{__version__}[/bold] – starting scrape\n")

    result = scrape_all(
        keywords=keywords,
        sources=sources,
        open_only=open_only,
        min_award=min_award,
        max_award=max_award,
    )

    if not result.grants:
        console.print("[yellow]No grants found matching your criteria.[/yellow]")
        return

    if output == "csv":
        path = export_csv(result.grants)
        console.print(f"[green]Exported to {path}[/green]")
    elif output == "json":
        path = export_json(result.grants)
        console.print(f"[green]Exported to {path}[/green]")
    else:
        print_table(result.grants)

    if result.errors:
        console.print(f"\n[red]Encountered {len(result.errors)} error(s)[/red]")

    if alert:
        send_alerts(result.grants)


@app.command()
def watch(
    keywords: Annotated[
        Optional[list[str]],
        typer.Option("-k", "--keyword", help="Keywords to search for"),
    ] = None,
    interval: Annotated[
        int, typer.Option("-i", "--interval", help="Polling interval in seconds"),
    ] = 3600,
    alert: Annotated[
        bool, typer.Option("--alert", help="Send alerts for new results")
    ] = True,
) -> None:
    """Continuously watch for new grants at a fixed interval."""
    console.print(f"[bold]GrantScout v{__version__}[/bold] – watch mode (every {interval}s)\n")
    seen_ids: set[str] = set()

    while True:
        result = scrape_all(keywords=keywords, open_only=True)
        new_grants = [g for g in result.grants if g.id not in seen_ids]
        seen_ids.update(g.id for g in result.grants)

        if new_grants:
            console.print(f"[green]Found {len(new_grants)} new grant(s)[/green]")
            print_table(new_grants, title="New Grants")
            if alert:
                send_alerts(new_grants)
        else:
            console.print("[dim]No new grants found this cycle.[/dim]")

        log.info("Next check in %d seconds", interval)
        time.sleep(interval)


@app.command(name="sources")
def sources_cmd() -> None:
    """List all available grant sources."""
    console.print("[bold]Available sources:[/bold]\n")
    for name in list_sources():
        console.print(f"  • {name}")


@app.command(name="config")
def config_cmd() -> None:
    """Show the current configuration (redacting secrets)."""
    from grantscout.config import config as cfg

    console.print("[bold]Current configuration:[/bold]\n")
    console.print(f"  Output dir      : {cfg.output_dir}")
    console.print(f"  Log file        : {cfg.log_file}")
    console.print(f"  Request timeout : {cfg.scraper.request_timeout}s")
    console.print(f"  Max retries     : {cfg.scraper.max_retries}")
    console.print(f"  Rate-limit delay: {cfg.scraper.rate_limit_delay}s")
    console.print(f"  SMTP configured : {cfg.smtp.is_configured}")
    console.print(f"  Webhook configured: {cfg.webhook.is_configured}")


@app.command()
def export(
    input_file: Annotated[
        str, typer.Argument(help="Path to a JSON file with grant data")
    ],
    fmt: Annotated[
        str, typer.Option("-f", "--format", help="Output format: csv, json, table")
    ] = "table",
) -> None:
    """Re-export a previously saved JSON grant file to another format."""
    import json as json_mod
    from pathlib import Path

    from grantscout.models import Grant

    path = Path(input_file)
    if not path.exists():
        console.print(f"[red]File not found: {input_file}[/red]")
        raise typer.Exit(1)

    data = json_mod.loads(path.read_text(encoding="utf-8"))
    grants = [Grant.from_dict(d) for d in data]

    if fmt == "csv":
        out = export_csv(grants)
        console.print(f"[green]Exported to {out}[/green]")
    elif fmt == "json":
        out = export_json(grants)
        console.print(f"[green]Exported to {out}[/green]")
    else:
        print_table(grants)
