#!/usr/bin/env bash
# install.sh – one-command setup for GrantScout
set -euo pipefail

MIN_PYTHON="3.10"

echo "=== GrantScout Installer ==="
echo

# ── Check Python ───────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is not installed. Please install Python >= $MIN_PYTHON"
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python $PY_VERSION found"

# ── Check / install Poetry ────────────────────────────────────
if ! command -v poetry &>/dev/null; then
    echo "Poetry not found – installing via pip…"
    python3 -m pip install --user poetry
fi
echo "✓ Poetry $(poetry --version 2>/dev/null || echo 'installed')"

# ── Install dependencies ──────────────────────────────────────
echo
echo "Installing project dependencies…"
poetry install
echo "✓ Dependencies installed"

# ── Create .env if needed ─────────────────────────────────────
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env from .env.example – edit it with your settings"
else
    echo "✓ .env already exists"
fi

echo
echo "=== Setup complete! ==="
echo "Run:  ./run.sh scrape -k health"
echo " or:  poetry run grantscout scrape -k technology --open"
