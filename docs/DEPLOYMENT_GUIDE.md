# Deployment Guide

This guide explains the phased deployment model for the **Hermes Agent on Azure Workshop** repository.

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

## 2. Deployment phases

This repo is intentionally deployed in phases.

### Phase 1 — Foundation

Goal:
- create the core Azure platform building blocks

Expected components:
- resource group
- network layout
- storage account
- key vault
- managed identity
- container registry
- monitoring workspace

### Phase 2 — Runtime

Goal:
- build and deploy the Hermes runtime container

Expected components:
- runtime container image
- container app / managed environment
- ingress endpoint
- provider configuration wiring

### Phase 3 — Integration

Goal:
- expose governed public routes and complete operational integration

Expected components:
- APIM routes and policies
- diagnostics configuration
- demo invocation path

---

## 3. Recommended execution order

### Step A
Review:
- `README.md`
- `docs/ARCHITECTURE.md`

### Step B
Deploy foundation layer first.

### Step C
Build and deploy the runtime layer.

### Step D
Enable APIM integration and test the public invocation path.

---

## 4. Validation checklist

After Phase 1:
- resource group exists
- key vault exists
- storage account exists
- managed identity exists

After Phase 2:
- container app exists
- `healthz` returns success
- `readyz` shows runtime readiness once startup completes

After Phase 3:
- APIM route exists
- demo chat request reaches runtime successfully

---

## 5. Deployment philosophy for this repo

This workshop repo is deliberately being built with a **resumable delivery model**:

- docs first
- infra next
- runtime next
- manuals last

That approach is intentional. It avoids a fragile “all-at-once” build and keeps the repository publishable at every phase.

---

## 6. Next planned files

The next phases of this repository will add:

- `infra/bicep/main.bicep`
- modular Bicep under `infra/bicep/modules/`
- Terraform equivalent under `infra/terraform/`
- Azure runtime bridge under `bridge/`
- workshop manuals under `manuals/`
- demo clients under `demo/src/`
