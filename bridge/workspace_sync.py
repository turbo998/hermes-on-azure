"""Azure Blob Storage backed workspace sync.

This version adds a lightweight recursive restore/save implementation so the
workshop repository is closer to a deployable starter.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger('azure.workspace_sync')

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.storage.blob import BlobServiceClient  # type: ignore
except Exception:  # pragma: no cover - optional dependency for workshop environments
    DefaultAzureCredential = None  # type: ignore
    BlobServiceClient = None  # type: ignore

SKIP_SUFFIXES = {'.pyc', '.pyo', '.log', '.tmp'}


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
        service = BlobServiceClient(
            account_url=f'https://{self.account_name}.blob.core.windows.net',
            credential=credential,
        )
        return service.get_container_client(self.container_name)

    def restore(self, namespace: str) -> None:
        client = self._client()
        if client is None:
            return
        base = Path(self.workspace)
        base.mkdir(parents=True, exist_ok=True)
        prefix = f'{namespace}/.hermes/'
        logger.info('Restoring workspace from container=%s prefix=%s', self.container_name, prefix)
        try:
            for blob in client.list_blobs(name_starts_with=prefix):
                relative = blob.name[len(prefix):]
                if not relative:
                    continue
                path = base / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'wb') as handle:
                    handle.write(client.download_blob(blob.name).readall())
        except Exception as exc:
            logger.warning('Workspace restore failed: %s', exc)

    def save(self, namespace: str) -> None:
        client = self._client()
        if client is None:
            return
        base = Path(self.workspace)
        base.mkdir(parents=True, exist_ok=True)
        prefix = f'{namespace}/.hermes/'
        logger.info('Saving workspace to container=%s prefix=%s', self.container_name, prefix)
        try:
            for path in base.rglob('*'):
                if path.is_dir():
                    continue
                if path.suffix in SKIP_SUFFIXES:
                    continue
                relative = str(path.relative_to(base))
                with open(path, 'rb') as handle:
                    client.upload_blob(f'{prefix}{relative}', handle, overwrite=True)
        except Exception as exc:
            logger.warning('Workspace save failed: %s', exc)
