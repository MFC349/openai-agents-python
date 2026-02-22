#!/usr/bin/env bash
# run.sh – convenience wrapper for GrantScout CLI
set -euo pipefail

if ! command -v poetry &>/dev/null; then
    echo "ERROR: Poetry is not installed. Run ./install.sh first."
    exit 1
fi

poetry run grantscout "$@"
