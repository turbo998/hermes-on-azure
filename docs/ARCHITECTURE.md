# Architecture Design

This document defines the Azure-native target architecture for hosting **Hermes Agent on Azure**.

It is designed for workshop delivery, but it follows production-oriented thinking and explicitly maps to:

- **Azure Cloud Adoption Framework (CAF)**
- **Azure Well-Architected Framework (WAF)**

---

## 1. Design goals

The architecture should be:

- simple enough to explain in a 120-minute workshop
- structured enough for enterprise discussion
- modular enough to evolve into a customer starter repo
- aligned to Azure landing-zone thinking

---

## 2. High-level architecture

```mermaid
flowchart TD
    U[Users / Channels] --> APIM[Azure API Management]
    APIM --> ACA[Azure Container Apps]
    ACA --> H[Hermes Agent Runtime]
    H --> KV[Azure Key Vault]
    H --> BLOB[Azure Blob Storage]
    H --> AOAI[Azure OpenAI]
    H --> AIF[Azure AI Foundry / Model Catalog]
    H --> MON[Azure Monitor / Log Analytics]
    MI[Managed Identity] --> H
```

### Component summary

#### Azure API Management
Used as the governed public ingress layer for webhook-style channels.

Responsibilities:
- normalize public endpoints
- apply throttling and policy
- isolate external channel concerns from the runtime

#### Azure Container Apps
Used as the runtime platform for Hermes Agent.

Responsibilities:
- host Hermes Agent in a serverless container model
- expose HTTP ingress
- support health and readiness checks
- support revision-based deployment

#### Azure Blob Storage
Used for workspace persistence.

Responsibilities:
- persist `.hermes` workspace state
- replace S3-style state sync from the AWS sample
- support memory/session continuity across revisions

#### Azure Key Vault
Used for secrets and configuration references.

Responsibilities:
- store bot tokens and endpoint secrets
- reduce hard-coded credential usage
- align to enterprise secret management expectations

#### Azure OpenAI / Azure AI Foundry
Used as the model provider layer.

Responsibilities:
- support GPT-family path through Azure OpenAI
- support multi-model / Claude path through Azure AI Foundry

#### Azure Monitor / Log Analytics
Used for observability.

Responsibilities:
- runtime logging
- health and failure investigation
- workshop demo telemetry and operations visibility

---

## 3. Data flow

### Inbound request flow

1. External channel sends request to APIM
2. APIM applies policy, route mapping, and throttling
3. Request is forwarded to Container Apps ingress
4. Hermes bridge endpoint receives `/invocations`
5. Hermes loads runtime context and provider config
6. Hermes calls Azure OpenAI or Azure AI Foundry
7. Response returns through the same chain

### Persistence flow

1. Container starts
2. Blob-backed workspace state is restored
3. Hermes runtime processes messages
4. Periodic sync writes updated workspace state back to Blob Storage

---

## 4. CAF alignment

| CAF area | Architecture decision | Why it matters |
|---|---|---|
| Identity | Managed Identity + RBAC | avoids static credentials and supports enterprise access control |
| Networking | APIM + Container Apps + private-access ready pattern | supports landing-zone friendly ingress design |
| Management | Log Analytics + operational scripts | supports repeatable deployment and supportability |
| Governance | phase-based IaC and explicit resource structure | supports policy-driven enterprise rollout |
| Security | Key Vault, MI, segmented ingress, future private endpoint support | improves control over secrets and exposure |
| Platform Automation | Bicep + Terraform + deployment scripts | makes the repo reusable as a platform asset |

---

## 5. WAF alignment

| WAF pillar | Current architecture choice | Intent |
|---|---|---|
| Reliability | healthz / readyz, staged runtime loading, workspace restore | keep runtime available and observable |
| Security | Managed Identity, Key Vault, governed ingress | reduce credential sprawl and improve boundary control |
| Cost Optimization | Container Apps serverless model, APIM tier selection, model routing | control workshop and PoC spend |
| Operational Excellence | modular docs + scripts + IaC | improve handoff and repeatability |
| Performance Efficiency | HTTP ingress, lightweight runtime bridge, scalable container model | support bursty agent interactions |

---

## 6. Why this Azure design is the right translation of the AWS sample

The AWS sample is fundamentally about:

- running Hermes in a managed runtime
- exposing it safely to messaging channels
- persisting workspace state
- integrating with native cloud AI services

On Azure, the closest practical workshop-ready translation is:

- **Container Apps** instead of AgentCore
- **Blob Storage** instead of S3
- **Key Vault + Managed Identity** instead of Secrets Manager + IAM-only flow
- **API Management** instead of API Gateway + Lambda fronting
- **Azure OpenAI / Azure AI Foundry** instead of Bedrock

This is not a 1:1 service clone. It is an **Azure-native operating model translation**.
