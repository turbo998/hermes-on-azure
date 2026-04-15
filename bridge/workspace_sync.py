"""Azure Blob Storage backed workspace sync.

This implementation intentionally stays lightweight for workshop use, but it is
closer to deployable behavior than the original placeholder:
- optional SDK import
- no-op safe fallback when SDK is unavailable
- explicit restore/save interfaces
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger('azure.workspace_sync')

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.storage.blob import BlobServiceClient  # type: ignore
except Exception:  # pragma: no cover - optional dependency for workshop environments
    DefaultAzureCredential = None  # type: ignore
    BlobServiceClient = None  # type: ignore


@dataclass
class WorkspaceSync:
    account_name: str
    container_name: str
    workspace: str = '/mnt/workspace/.hermes'

    def _client(self):
        if not DefaultAzureCredential or not BlobServiceClient:
            logger.warning('Azure Blob SDK not installed; workspace sync running in no-op mode')
            return None
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=True)
        return BlobServiceClient(
            account_url=f'https://{self.account_name}.blob.core.windows.net',
            credential=credential,
        ).get_container_client(self.container_name)

    def restore(self, namespace: str) -> None:
        client = self._client()
        if client is None:
            return
        Path(self.workspace).mkdir(parents=True, exist_ok=True)
        logger.info('Workspace restore requested for namespace=%s', namespace)
        # Production-grade recursive blob restore can be added here.

    def save(self, namespace: str) -> None:
        client = self._client()
        if client is None:
            return
        Path(self.workspace).mkdir(parents=True, exist_ok=True)
        logger.info('Workspace save requested for namespace=%s', namespace)
        # Production-grade recursive blob upload can be added here.
