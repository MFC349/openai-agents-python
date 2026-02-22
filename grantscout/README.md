# GrantScout

Automated grant discovery tool — scrape, filter, alert, and export federal funding opportunities from Grants.gov and SAM.gov.

## Quick Start

```bash
cd grantscout
./install.sh          # installs everything
./run.sh scrape -k technology --open
```

## Commands

| Command   | Description                                         |
|-----------|-----------------------------------------------------|
| `scrape`  | Scrape grants by keyword, filter, and display/export |
| `watch`   | Continuously poll for new grants at an interval      |
| `sources` | List available grant data sources                    |
| `config`  | Show the active configuration (secrets redacted)     |
| `export`  | Re-export a saved JSON file to CSV or table          |

### `scrape`

```bash
grantscout scrape -k health -k research --open --min-award 50000 -o csv
```

**Options:**
- `-k / --keyword` — keywords to search (repeatable)
- `-s / --source` — restrict to specific sources (repeatable)
- `--open` — only show open opportunities
- `--min-award` — minimum award ceiling
- `--max-award` — maximum award floor
- `-o / --output` — `table` (default), `csv`, or `json`
- `--alert` — send email/webhook alerts for results

### `watch`

```bash
grantscout watch -k climate --interval 1800 --alert
```

Polls every `--interval` seconds (default 3600) and alerts on new grants.

### `sources`

```bash
grantscout sources
```

### `config`

```bash
grantscout config
```

### `export`

```bash
grantscout export output/grants.json -f csv
```

## Configuration

Copy `.env.example` to `.env` and fill in your settings:

| Variable                       | Default           | Description                     |
|--------------------------------|-------------------|---------------------------------|
| `GRANTSCOUT_REQUEST_TIMEOUT`   | `30`              | HTTP request timeout (seconds)  |
| `GRANTSCOUT_MAX_RETRIES`       | `3`               | Max retry attempts per request  |
| `GRANTSCOUT_RATE_LIMIT_DELAY`  | `1.0`             | Delay between retries (seconds) |
| `GRANTSCOUT_SMTP_HOST`         | `smtp.gmail.com`  | SMTP server hostname            |
| `GRANTSCOUT_SMTP_PORT`         | `587`             | SMTP server port                |
| `GRANTSCOUT_SMTP_USER`         |                   | SMTP username                   |
| `GRANTSCOUT_SMTP_PASSWORD`     |                   | SMTP password                   |
| `GRANTSCOUT_ALERT_FROM`        |                   | Alert sender address            |
| `GRANTSCOUT_ALERT_TO`          |                   | Alert recipient address         |
| `GRANTSCOUT_WEBHOOK_URL`       |                   | Slack/Discord webhook URL       |
| `GRANTSCOUT_OUTPUT_DIR`        | `./output`        | Output directory for exports    |
| `GRANTSCOUT_LOG_FILE`          | `./grantscout.log`| Log file path                   |

## Data Sources

- **Grants.gov** — Federal grant opportunities via the REST API
- **SAM.gov** — Contract and grant opportunities via the public API

## Project Structure

```
grantscout/
├── __init__.py       # Version
├── __main__.py       # python -m grantscout
├── cli.py            # 5 Typer commands
├── config.py         # Env-driven config
├── logger.py         # Rich + file logging
├── models.py         # Grant + ScrapeResult dataclasses
├── scraper.py        # Multi-source orchestration
├── exporter.py       # CSV, JSON, table output
├── alerter.py        # Email + webhook alerts
└── sources/
    ├── __init__.py   # Source registry
    ├── base.py       # Abstract base with retry logic
    ├── grants_gov.py # Grants.gov API
    └── sam_gov.py    # SAM.gov API
```

## Development

```bash
poetry install
poetry run pytest
```

## License

MIT
