#!/usr/bin/env bash
set -euo pipefail

export HERMES_HOME="${HERMES_HOME:-/mnt/workspace/.hermes}"
mkdir -p "${HERMES_HOME}"/{memories,skills,sessions,logs,cache,cron}

# Default a stable workspace namespace if one was not supplied externally.
export WORKSPACE_NAMESPACE="${WORKSPACE_NAMESPACE:-default}"

exec python -m bridge.contract "$@"
