#!/usr/bin/env bash
set -euo pipefail

SUBSCRIPTION_ID=""
ENVIRONMENT_NAME="dev"
RESOURCE_PREFIX="hermes-az"
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --subscription-id)
      SUBSCRIPTION_ID="$2"; shift 2 ;;
    --environment-name)
      ENVIRONMENT_NAME="$2"; shift 2 ;;
    --resource-prefix)
      RESOURCE_PREFIX="$2"; shift 2 ;;
    --force)
      FORCE="true"; shift ;;
    *)
      echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$SUBSCRIPTION_ID" ]]; then
  echo "--subscription-id is required" >&2
  exit 1
fi

RG_NAME="${RESOURCE_PREFIX}-${ENVIRONMENT_NAME}-rg"
az account set --subscription "$SUBSCRIPTION_ID" >/dev/null

if [[ "$FORCE" != "true" ]]; then
  read -r -p "Delete resource group ${RG_NAME}? Type yes to continue: " ANSWER
  [[ "$ANSWER" == "yes" ]] || { echo "Cancelled"; exit 1; }
fi

az group delete --name "$RG_NAME" --yes --no-wait
echo "Deletion started for ${RG_NAME}"
