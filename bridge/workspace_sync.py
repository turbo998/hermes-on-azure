"""Azure Blob Storage backed workspace sync placeholder.

This file documents the intended persistence direction for the workshop repo.
A production-ready version will sync `.hermes` workspace state to Blob Storage.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WorkspaceSync:
    account_name: str
    container_name: str

    def restore(self, namespace: str) -> None:
        return None

    def save(self, namespace: str) -> None:
        return None
