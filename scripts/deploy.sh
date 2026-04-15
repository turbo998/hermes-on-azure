#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

PHASE="${1:-all}"
shift || true

SUBSCRIPTION_ID=""
LOCATION="eastus2"
ENVIRONMENT_NAME="dev"
RESOURCE_PREFIX="hermes-az"
USE_ACR_BUILD="true"

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
    --local-build)
      USE_ACR_BUILD="false"; shift ;;
    -h|--help)
      echo "Usage: $0 [all|phase1|phase2|phase3] --subscription-id <id> [--location eastus2] [--environment-name dev] [--resource-prefix hermes-az] [--local-build]"
      exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$SUBSCRIPTION_ID" ]]; then
  echo "--subscription-id is required" >&2
  exit 1
fi

RG_NAME="${RESOURCE_PREFIX}-${ENVIRONMENT_NAME}-rg"
SANITIZED_PREFIX="${RESOURCE_PREFIX//-/}"
ACR_NAME="$(echo "${SANITIZED_PREFIX}${ENVIRONMENT_NAME}acr" | tr '[:upper:]' '[:lower:]' | cut -c1-50)"
APP_NAME="${RESOURCE_PREFIX}-${ENVIRONMENT_NAME}-hermes"
DEPLOYMENT_NAME="${RESOURCE_PREFIX}-${ENVIRONMENT_NAME}-${PHASE}-$(date +%Y%m%d%H%M%S)"

info() { printf '[0;32m[INFO][0m %s
' "$*"; }
warn() { printf '[1;33m[WARN][0m %s
' "$*"; }
err()  { printf '[0;31m[ERR ][0m %s
' "$*" >&2; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { err "Required command not found: $1"; exit 1; }
}

need_cmd az
az account set --subscription "$SUBSCRIPTION_ID" >/dev/null

phase1() {
  info "Phase 1 - foundation deployment"
  az deployment sub create     --name "$DEPLOYMENT_NAME"     --location "$LOCATION"     --template-file infra/bicep/main.bicep     --parameters location="$LOCATION" environmentName="$ENVIRONMENT_NAME" resourcePrefix="$RESOURCE_PREFIX"

  info "Phase 1 complete"
  info "Resource group: $RG_NAME"
}

phase2() {
  info "Phase 2 - build and deploy runtime"

  if [[ ! -d "$PROJECT_DIR/bridge" ]]; then
    err "bridge/ directory not found"
    exit 1
  fi

  ACR_LOGIN_SERVER="$(az acr show -n "$ACR_NAME" -g "$RG_NAME" --query loginServer -o tsv 2>/dev/null || true)"
  if [[ -z "$ACR_LOGIN_SERVER" ]]; then
    err "Could not resolve ACR login server. Run phase1 first and verify deployment succeeded."
    exit 1
  fi

  if [[ "$USE_ACR_BUILD" == "true" ]]; then
    info "Building image in ACR"
    az acr build -r "$ACR_NAME" -g "$RG_NAME" -t hermes-agent-on-azure:latest -f bridge/Dockerfile .
  else
    need_cmd docker
    info "Building image locally"
    az acr login -n "$ACR_NAME"
    docker build -f bridge/Dockerfile -t "${ACR_LOGIN_SERVER}/hermes-agent-on-azure:latest" .
    docker push "${ACR_LOGIN_SERVER}/hermes-agent-on-azure:latest"
  fi

  info "Applying infrastructure again to ensure runtime resources are current"
  az deployment sub create     --name "$DEPLOYMENT_NAME"     --location "$LOCATION"     --template-file infra/bicep/main.bicep     --parameters location="$LOCATION" environmentName="$ENVIRONMENT_NAME" resourcePrefix="$RESOURCE_PREFIX"

  info "Phase 2 complete"
  az containerapp show -n "$APP_NAME" -g "$RG_NAME" --query properties.configuration.ingress.fqdn -o tsv 2>/dev/null || true
}

phase3() {
  info "Phase 3 - integration validation"
  az deployment sub create     --name "$DEPLOYMENT_NAME"     --location "$LOCATION"     --template-file infra/bicep/main.bicep     --parameters location="$LOCATION" environmentName="$ENVIRONMENT_NAME" resourcePrefix="$RESOURCE_PREFIX"

  info "Phase 3 complete"
  info "Use docs/CHANNEL_SETUP.md to wire Telegram / Slack / Discord / Feishu / DingTalk routes through APIM"
}

case "$PHASE" in
  all)
    phase1
    phase2
    phase3
    ;;
  phase1)
    phase1
    ;;
  phase2)
    phase2
    ;;
  phase3)
    phase3
    ;;
  *)
    err "Usage: $0 [all|phase1|phase2|phase3] --subscription-id <id> [--location eastus2] [--environment-name dev]"
    exit 1
    ;;
esac
