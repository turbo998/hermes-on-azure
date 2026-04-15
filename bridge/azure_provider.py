"""Azure provider bootstrap for Hermes Agent on Azure.

This workshop repo keeps provider wiring explicit so participants can see how
Azure OpenAI and Azure AI Foundry map into the Hermes runtime.
"""

from __future__ import annotations

import os
from typing import Dict

AZURE_OPENAI_MODEL_MAP: Dict[str, str] = {
    'gpt-4o': 'gpt-4o',
    'gpt-4.1': 'gpt-4.1',
    'o1': 'o1',
    'o3': 'o3',
}

AZURE_FOUNDRY_MODEL_MAP: Dict[str, str] = {
    'claude-sonnet-4-5': 'claude-sonnet-4-5',
    'claude-opus-4-1': 'claude-opus-4-1',
}


def resolve_model(model: str, mode: str) -> str:
    if mode == 'azure-foundry':
        return AZURE_FOUNDRY_MODEL_MAP.get(model, model)
    return AZURE_OPENAI_MODEL_MAP.get(model, model)


def configure_azure_provider() -> dict[str, str]:
    mode = os.environ.get('HERMES_PROVIDER_MODE', 'azure-openai').strip().lower()
    model = os.environ.get('HERMES_MODEL', 'gpt-4o')
    resolved = resolve_model(model, mode)
    return {
        'providerMode': mode,
        'requestedModel': model,
        'resolvedModel': resolved,
        'azureOpenAIEndpoint': os.environ.get('AZURE_OPENAI_ENDPOINT', ''),
        'azureAIFoundryEndpoint': os.environ.get('AZURE_AI_FOUNDRY_ENDPOINT', ''),
    }
