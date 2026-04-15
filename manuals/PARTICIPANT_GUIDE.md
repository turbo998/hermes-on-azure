# Participant Guide

## Before the workshop

Please have access to:

- Azure subscription or sandbox
- Azure CLI
- Bicep CLI
- Terraform
- Docker
- Python 3.11+

---

## What you will learn

By the end of the session, you should understand:

- how Hermes Agent maps onto Azure services
- how provider choice affects the design
- how identity, storage, and observability are handled
- how to structure a reusable Azure workshop repository

---

## Lab flow

### Lab 1 — Read the architecture

Review:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEPLOYMENT_GUIDE.md`

### Lab 2 — Inspect infrastructure layout

Review:

- `infra/bicep/main.bicep`
- `infra/bicep/modules/`
- `infra/terraform/`

### Lab 3 — Inspect runtime bridge

Review:

- `bridge/contract.py`
- `bridge/azure_provider.py`
- `bridge/workspace_sync.py`

### Lab 4 — Run demo client

Try:

```bash
python demo/src/demo_chat.py --endpoint https://example/agent/invoke --message "Hello"
```

---

## FAQ

### Is this repo production-ready?

It is a workshop-quality starter repository with production-oriented structure, not a fully hardened production platform.

### Why Container Apps instead of AKS?

Because it is easier to explain and deploy for a workshop while still mapping well to Azure-native hosting.

### Why both OpenAI and Foundry?

Because customer conversations usually split between Microsoft-first standardization and multi-model flexibility.
