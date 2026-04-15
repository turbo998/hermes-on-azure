# Azure AI Provider Guide

This document explains how Hermes Agent on Azure can use Azure-native model providers.

---

## 1. Provider options

### Azure OpenAI

Recommended when customers want:

- Microsoft-first enterprise positioning
- GPT-family model standardization
- familiar Azure AI operations model
- tighter alignment with existing Azure AI governance

Typical examples:

- `gpt-4o`
- `gpt-4.1`
- `o1`
- `o3`

### Azure AI Foundry / Model Catalog

Recommended when customers want:

- broader model portfolio
- Claude-based workshop narrative
- partner-model comparison discussions
- a more flexible model catalog story

Typical examples:

- `claude-sonnet-4-5`
- `claude-opus-4-1`

---

## 2. Integration pattern

Hermes Agent keeps model choice externalized through environment variables.

Example variables:

```bash
HERMES_PROVIDER_MODE=azure-openai
HERMES_MODEL=gpt-4o
AZURE_OPENAI_ENDPOINT=https://<name>.openai.azure.com/
```

or:

```bash
HERMES_PROVIDER_MODE=azure-foundry
HERMES_MODEL=claude-sonnet-4-5
AZURE_AI_FOUNDRY_ENDPOINT=https://<project>.services.ai.azure.com/models
```

The workshop bridge uses `bridge/azure_provider.py` to resolve aliases and make the provider path explicit.

---

## 3. Model mapping strategy

| Hermes alias | Azure target |
|---|---|
| `gpt-4o` | Azure OpenAI deployment |
| `gpt-4.1` | Azure OpenAI deployment |
| `o1` | Azure OpenAI deployment |
| `o3` | Azure OpenAI deployment |
| `claude-sonnet-4-5` | Azure AI Foundry model route |
| `claude-opus-4-1` | Azure AI Foundry model route |

---

## 4. Governance guidance

For workshop positioning, the most important customer message is:

- model choice should remain a configuration decision
- secrets and endpoints should stay outside application code
- the runtime should log provider and model context for operations visibility

---

## 5. Cost guidance

Recommended workshop framing:

- use `gpt-4o` for the default demo path
- reserve heavier reasoning models for narrow scenarios
- reserve Claude demos for differentiation discussions, not as the default for every step
- put daily budget and usage tracking in the operational backlog from day one
