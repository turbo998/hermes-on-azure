"""Azure Blob Storage backed workspace sync.

This version adds:
- recursive restore/save
- skip filtering
- periodic save loop
- sqlite backup copy for safer upload of `.db` files
"""

from __future__ import annotations

import logging
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger('azure.workspace_sync')

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.storage.blob import BlobServiceClient  # type: ignore
except Exception:  # pragma: no cover - optional dependency for workshop environments
    DefaultAzureCredential = None  # type: ignore
    BlobServiceClient = None  # type: ignore

SKIP_SUFFIXES = {'.pyc', '.pyo', '.log', '.tmp', '.db-wal', '.db-shm', '.db-journal'}


@dataclass
class WorkspaceSync:
    account_name: str
    container_name: str
    workspace: str = '/mnt/workspace/.hermes'
    sync_interval: int = 300

    def __post_init__(self) -> None:
        self._stop = threading.Event()
        self._save_lock = threading.Lock()

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
            with self._save_lock:
                for path in base.rglob('*'):
                    if path.is_dir():
                        continue
                    if path.suffix in SKIP_SUFFIXES:
                        continue
                    relative = str(path.relative_to(base))
                    upload_path = path
                    if path.suffix == '.db':
                        backup_path = path.with_suffix('.db.azbak')
                        self._sqlite_backup(path, backup_path)
                        upload_path = backup_path
                    with open(upload_path, 'rb') as handle:
                        client.upload_blob(f'{prefix}{relative}', handle, overwrite=True)
                    if upload_path != path:
                        upload_path.unlink(missing_ok=True)
        except Exception as exc:
            logger.warning('Workspace save failed: %s', exc)

    def start_periodic_save(self, namespace: str) -> None:
        def _loop() -> None:
            while not self._stop.is_set():
                self._stop.wait(self.sync_interval)
                if self._stop.is_set():
                    break
                self.save(namespace)
        threading.Thread(target=_loop, daemon=True, name='workspace-sync').start()
        logger.info('Periodic workspace save started (%ss)', self.sync_interval)

    def stop(self) -> None:
        self._stop.set()

    @staticmethod
    def _sqlite_backup(src: Path, dst: Path) -> None:
        src_conn = sqlite3.connect(str(src))
        dst_conn = sqlite3.connect(str(dst))
        try:
            src_conn.backup(dst_conn)
        finally:
            dst_conn.close()
            src_conn.close()
