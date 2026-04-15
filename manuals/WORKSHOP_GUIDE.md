# Workshop Facilitator Guide

## Workshop goal

Help a customer technical audience understand how Hermes Agent can be hosted on Azure with a design that is:

- practical
- governed
- extensible
- workshop-ready

---

## 120-minute agenda

| Section | Time | Goal |
|---|---:|---|
| Architecture overview | 20 min | Explain the Azure-native reference design |
| Hands-on deployment | 40 min | Walk through the staged deployment model |
| Demo and customization | 30 min | Show runtime path, provider options, and invocation flow |
| Q&A and trade-offs | 30 min | Discuss governance, scale, security, and cost |

---

## Section 1: Architecture overview

Talking points:

- the goal is not to clone AWS service-for-service
- the goal is to produce the right Azure operating model
- Container Apps + Blob + Key Vault + APIM is the key translation pattern
- CAF and WAF matter because customers care about platform fit, not just demos

---

## Section 2: Hands-on deployment

Walk through:

- repo structure
- docs-first approach
- Bicep and Terraform scaffolding
- deployment script flow
- where identity, storage, and monitoring fit

Instructor note:

Keep emphasizing why each Azure service is there.
Do not let the workshop collapse into a portal-clicking session.

---

## Section 3: Demo and customization

Demo path:

1. show the HTTP contract
2. show provider mapping in `bridge/azure_provider.py`
3. run demo client against a deployed or mocked endpoint
4. explain how channels would be normalized through APIM

---

## Section 4: Q&A and trade-offs

Useful prompts:

- When should this stay on Container Apps vs move to AKS?
- When should the customer prefer Azure OpenAI vs Foundry?
- What would need to change for production hardening?
- How should platform teams separate shared services vs workload services?
