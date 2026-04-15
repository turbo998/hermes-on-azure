# Deployment Guide

This guide explains a more realistic phased deployment model for the **Hermes Agent on Azure Workshop** repository.

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
- storage account and blob container
- key vault
- managed identity
- storage RBAC assignment
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
- workspace environment variables
- readiness and liveness probes

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

## 5. Runtime configuration notes

### Azure OpenAI path

Required environment variables:

- `HERMES_PROVIDER_MODE=azure-openai`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_DEPLOYMENT`

The bridge now validates these at startup.

### Azure AI Foundry path

Required environment variables:

- `HERMES_PROVIDER_MODE=azure-foundry`
- `AZURE_AI_FOUNDRY_ENDPOINT`

### Workspace persistence path

Recommended environment variables:

- `WORKSPACE_STORAGE_ACCOUNT`
- `WORKSPACE_CONTAINER=hermes-workspace`
- `WORKSPACE_NAMESPACE=<stable-namespace>`

The bridge now contains a lightweight recursive Blob restore/save implementation.

---

## 6. Validation checklist

After Phase 1:
- resource group exists
- key vault exists
- storage account exists
- blob container exists
- managed identity exists
- storage RBAC exists

After Phase 2:
- container app exists
- image exists in ACR
- `healthz` returns success
- `readyz` transitions to ready after startup
- environment variables for workspace/provider are visible in the app configuration

After Phase 3:
- APIM route exists
- channel route strategy is defined
- demo client can hit the invocation endpoint

---

## 7. Teardown

```bash
bash scripts/teardown.sh   --subscription-id <subscription-id>   --environment-name dev
```

Add `--force` to skip confirmation.

---

## 8. Current maturity note

This repo is now best described as a **deployable workshop starter repo with real cloud wiring patterns**:

- provider bootstrap validates real Azure configuration
- workspace sync models real Blob restore/save behavior
- storage RBAC and container env wiring are represented in Bicep
- probes and workspace env vars are represented in Container Apps config

It is still not a fully production-hardened landing-zone implementation, but it is substantially closer to something a customer team could adapt into a real internal starter repo.
