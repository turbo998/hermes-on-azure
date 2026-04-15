# Hermes Agent on Azure Workshop

English | [中文](README_ZH.md)

Deploy and demonstrate [Hermes Agent](https://github.com/NousResearch/hermes-agent) on **Microsoft Azure** with a workshop-ready repository that includes:

- Azure architecture design aligned to **CAF** and **WAF**
- deployment guidance for **Azure Container Apps**
- integration patterns for **Azure OpenAI** and **Azure AI Foundry**
- demo scripts, workshop manuals, and infrastructure templates
- GitHub delivery flow for customer-facing workshop assets

This repo is the Azure counterpart to the AWS reference sample:
<https://github.com/aws-samples/sample-host-hermesagent-on-amazon-bedrock-agentcore>

---

## What this repository is for

This project is designed for a **120-minute workshop** aimed at platform teams, solution architects, and AI engineering teams that want to host Hermes Agent on Azure in a way that is:

- practical to explain
- aligned with Azure landing zones
- secure enough for enterprise discussion
- concrete enough to demo and extend

---

## Target architecture

```text
Telegram / Slack / Discord / Feishu / DingTalk / WeChat-like channels
                           |
                           v
                Azure API Management (webhook gateway)
                           |
                           v
                 Azure Container Apps ingress
                           |
                           v
               Hermes Agent runtime container
         +-------------------------------------------+
         | bridge/contract.py                        |
         | - /healthz                                |
         | - /readyz                                 |
         | - /invocations                            |
         | Hermes Agent                              |
         | Azure OpenAI / Azure AI Foundry provider  |
         | Blob-backed workspace sync                |
         +-------------------------------------------+
                 |              |               |
                 v              v               v
          Azure Blob      Azure Key Vault   Azure Monitor /
          Storage         + Managed Id      Log Analytics
```

---

## Phase-based delivery approach

This repository is being built and delivered in phases:

### Phase A — foundation docs
- README
- Architecture document
- Deployment guide
- Chinese README

### Phase B — infrastructure
- Bicep templates
- Terraform alternative
- deployment and teardown scripts

### Phase C — runtime and demos
- Azure bridge components
- demo chat clients
- provider integration code

### Phase D — workshop assets
- facilitator guide
- participant guide
- slide outline

---

## Azure mapping from the AWS reference

| AWS reference | Azure equivalent |
|---|---|
| Bedrock AgentCore | Azure Container Apps |
| Bedrock Claude | Azure AI Foundry Claude / Azure OpenAI |
| S3 | Azure Blob Storage |
| Secrets Manager | Azure Key Vault |
| API Gateway + Lambda | Azure API Management + Container Apps ingress |
| CloudWatch | Azure Monitor + Log Analytics + App Insights |
| IAM roles | Managed Identity + RBAC |
| CDK | Bicep + Terraform |

---

## Workshop outcome

By the end of the workshop, participants should understand:

- how to host Hermes Agent on Azure
- how to align the design to CAF and WAF principles
- how to handle identity, secrets, observability, and persistence
- how to prepare an Azure-native workshop/demo repository for customer delivery

---

## Status

Current status: **Phase A complete in progress**

The repository is intentionally being delivered in committed stages so it remains resumable and publishable even if the task is interrupted.
