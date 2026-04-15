#!/usr/bin/env bash
set -euo pipefail

PHASE="${1:-all}"
shift || true

SUBSCRIPTION_ID=""
LOCATION="eastus2"
ENVIRONMENT_NAME="dev"
RESOURCE_PREFIX="hermes-az"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --subscription-id)
      SUBSCRIPTION_ID="$2"; shift 2 ;;
    --location)
      LOCATION="$2"; shift 2 ;;
    --environment-name)
      ENVIRONMENT_NAME="$2"; shift 2 ;;
    --resource-prefix)
      RESOURCE_PREFIX="$2"; shift 2 ;;
    *)
      echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$SUBSCRIPTION_ID" ]]; then
  echo "--subscription-id is required" >&2
  exit 1
fi

az account set --subscription "$SUBSCRIPTION_ID" >/dev/null

echo "Phase: $PHASE"
echo "Location: $LOCATION"
echo "Environment: $ENVIRONMENT_NAME"
echo "Resource prefix: $RESOURCE_PREFIX"

echo "This repo is currently in staged delivery."
echo "Use Bicep under infra/bicep and extend this script as runtime files land."
