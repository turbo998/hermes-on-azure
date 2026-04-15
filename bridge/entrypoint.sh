#!/usr/bin/env bash
set -euo pipefail

export HERMES_HOME="${HERMES_HOME:-/mnt/workspace/.hermes}"
mkdir -p "${HERMES_HOME}"/{memories,skills,sessions,logs,cache,cron}

exec python -m bridge.contract "$@"
