# Deployment Guide

This guide explains a more deployable phased model for the **Hermes Agent on Azure Workshop** repository.

---

## 1. Prerequisites

### Tooling

Install and verify:

```bash
az version
bicep --version
terraform version
docker --version
python3 --version
```

### Azure prerequisites

You should have access to create or manage:

- resource groups
- networking resources
- Managed Identity
- Azure Container Registry
- Azure Container Apps
- Azure Key Vault
- Blob Storage
- API Management
- Log Analytics / Monitor

---

## 2. Phase 1 — Foundation

Goal:
- deploy the shared Azure building blocks

Expected components:
- resource group
- network layout
- storage account
- key vault
- managed identity
- container registry
- monitoring workspace

Run:

```bash
bash scripts/deploy.sh phase1   --subscription-id <subscription-id>   --location eastus2   --environment-name dev
```

---

## 3. Phase 2 — Runtime

Goal:
- build and deploy the Hermes runtime container

Expected components:
- ACR image build
- Container Apps environment
- Container App runtime
- ingress endpoint

Run:

```bash
bash scripts/deploy.sh phase2   --subscription-id <subscription-id>   --location eastus2   --environment-name dev
```

If you prefer local Docker build instead of ACR build:

```bash
bash scripts/deploy.sh phase2   --subscription-id <subscription-id>   --location eastus2   --environment-name dev   --local-build
```

---

## 4. Phase 3 — Integration

Goal:
- finalize APIM-backed invocation path
- prepare webhook setup
- validate operational readiness

Run:

```bash
bash scripts/deploy.sh phase3   --subscription-id <subscription-id>   --location eastus2   --environment-name dev
```

Then use:

```bash
bash scripts/setup_channels.sh telegram <apim-host>
bash scripts/setup_channels.sh slack <apim-host>
```

---

## 5. Validation checklist

After Phase 1:
- resource group exists
- key vault exists
- storage account exists
- managed identity exists

After Phase 2:
- container app exists
- image exists in ACR
- `healthz` returns success
- `readyz` transitions to ready after startup

After Phase 3:
- APIM route exists
- channel route strategy is defined
- demo client can hit the invocation endpoint

---

## 6. Runtime configuration notes

### Azure OpenAI path

Required environment variables:

- `HERMES_PROVIDER_MODE=azure-openai`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`

### Azure AI Foundry path

Required environment variables:

- `HERMES_PROVIDER_MODE=azure-foundry`
- `AZURE_AI_FOUNDRY_ENDPOINT`

### Workspace persistence path

Recommended environment variables:

- `WORKSPACE_STORAGE_ACCOUNT`
- `WORKSPACE_CONTAINER=hermes-workspace`
- `WORKSPACE_NAMESPACE=<stable-namespace>`

---

## 7. Teardown

```bash
bash scripts/teardown.sh   --subscription-id <subscription-id>   --environment-name dev
```

Add `--force` to skip confirmation.

---

## 8. Current maturity note

This repo is now closer to deployable than the first draft:

- the deployment script now models real phase execution
- the provider layer validates required configuration
- the workspace sync layer has Azure Blob SDK hooks
- the channel setup helper is included

It is still best described as a **deployable workshop starter repo**, not a fully production-hardened landing-zone implementation.
