"""Azure provider bootstrap for Hermes Agent on Azure.

This module is still workshop-oriented, but it now models a more realistic
provider bootstrap flow:
- validates Azure OpenAI vs Azure AI Foundry mode
- resolves model aliases
- optionally mints Managed Identity tokens when Azure SDK is available
"""

from __future__ import annotations

import os
from typing import Dict

try:
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider  # type: ignore
except Exception:  # pragma: no cover - optional for workshop environments
    DefaultAzureCredential = None  # type: ignore
    get_bearer_token_provider = None  # type: ignore

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


def _mint_token(scope: str) -> str:
    if not DefaultAzureCredential or not get_bearer_token_provider:
        return ''
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
    provider = get_bearer_token_provider(credential, scope)
    return provider()


def configure_azure_provider() -> dict[str, str]:
    mode = os.environ.get('HERMES_PROVIDER_MODE', 'azure-openai').strip().lower()
    model = os.environ.get('HERMES_MODEL', 'gpt-4o')
    resolved = resolve_model(model, mode)

    if mode == 'azure-foundry':
        endpoint = os.environ.get('AZURE_AI_FOUNDRY_ENDPOINT', '')
        if not endpoint:
            raise RuntimeError('AZURE_AI_FOUNDRY_ENDPOINT is required when HERMES_PROVIDER_MODE=azure-foundry')
        token = _mint_token('https://ai.azure.com/.default')
        return {
            'providerMode': mode,
            'requestedModel': model,
            'resolvedModel': resolved,
            'baseUrl': endpoint.rstrip('/'),
            'authMode': 'managed-identity' if token else 'token-not-minted',
            'tokenPresent': 'true' if token else 'false',
        }

    endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT', '')
    deployment = os.environ.get('AZURE_OPENAI_DEPLOYMENT', resolved)
    api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-10-21')
    if not endpoint:
        raise RuntimeError('AZURE_OPENAI_ENDPOINT is required when HERMES_PROVIDER_MODE=azure-openai')

    token = _mint_token('https://cognitiveservices.azure.com/.default')
    return {
        'providerMode': mode,
        'requestedModel': model,
        'resolvedModel': deployment,
        'baseUrl': f"{endpoint.rstrip('/')}/openai/deployments/{deployment}?api-version={api_version}",
        'authMode': 'managed-identity' if token else 'token-not-minted',
        'tokenPresent': 'true' if token else 'false',
    }
