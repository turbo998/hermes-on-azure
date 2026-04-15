"""HTTP contract server for Hermes Agent on Azure Container Apps.

Endpoints:
- GET /healthz   -> liveness probe
- GET /readyz    -> readiness probe
- POST /invocations -> normalized invocation endpoint

This implementation is still workshop-friendly, but now models a more realistic
startup sequence:
- provider configuration is validated at startup
- workspace restore/save hooks are initialized
- readiness reflects provider bootstrap success
"""

from __future__ import annotations

import json
import logging
import os
import signal
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from bridge.azure_provider import configure_azure_provider
from bridge.workspace_sync import WorkspaceSync

logger = logging.getLogger('azure.contract')


class State:
    agent: Any = None
    agent_ready: bool = False
    provider_config: dict[str, str] | None = None
    workspace_sync: WorkspaceSync | None = None
    busy_count: int = 0
    busy_lock = threading.Lock()
    start_time: float = time.time()


S = State()


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self) -> None:
        if self.path == '/healthz':
            self._send_json({'status': 'ok', 'uptimeSeconds': int(time.time() - S.start_time)})
            return
        if self.path == '/readyz':
            self._send_json(
                {
                    'status': 'ready' if S.agent_ready else 'starting',
                    'busyCount': S.busy_count,
                    'providerConfigured': S.provider_config is not None,
                },
                status=200 if S.agent_ready else 503,
            )
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path != '/invocations':
            self.send_error(404)
            return

        raw = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        body = json.loads(raw or b'{}')

        with S.busy_lock:
            S.busy_count += 1
        try:
            action = body.get('action', 'chat')
            if action == 'status':
                self._send_json(_status_payload())
                return

            user_message = body.get('message', '')
            channel = body.get('channel', 'azure')
            user_id = body.get('userId', 'unknown')

            response = {
                'response': f"Hermes Agent on Azure ({S.provider_config.get('providerMode', 'unknown') if S.provider_config else 'unknown'}) received from {channel}/{user_id}: {user_message}",
                'provider': S.provider_config or {},
            }
            self._send_json(response)
        finally:
            with S.busy_lock:
                S.busy_count -= 1

    def _send_json(self, data: dict[str, Any], status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt: str, *args: Any) -> None:
        logger.debug(fmt, *args)


def _status_payload() -> dict[str, Any]:
    return {
        'agentReady': S.agent_ready,
        'providerConfig': S.provider_config or {},
        'busyCount': S.busy_count,
        'uptimeSeconds': int(time.time() - S.start_time),
    }


def _init_runtime() -> None:
    S.provider_config = configure_azure_provider()

    storage_account = os.environ.get('WORKSPACE_STORAGE_ACCOUNT', '')
    storage_container = os.environ.get('WORKSPACE_CONTAINER', 'hermes-workspace')
    workspace_namespace = os.environ.get('WORKSPACE_NAMESPACE', '')
    if storage_account and workspace_namespace:
        S.workspace_sync = WorkspaceSync(
            account_name=storage_account,
            container_name=storage_container,
            workspace=os.environ.get('HERMES_HOME', '/mnt/workspace/.hermes'),
        )
        S.workspace_sync.restore(workspace_namespace)

    S.agent_ready = True
    logger.info('Azure runtime initialized: %s', S.provider_config)


def _sigterm_handler(signum: int, frame: Any) -> None:
    try:
        namespace = os.environ.get('WORKSPACE_NAMESPACE', '')
        if S.workspace_sync and namespace:
            S.workspace_sync.save(namespace)
    finally:
        sys.exit(0)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(levelname)s %(message)s')
    signal.signal(signal.SIGTERM, _sigterm_handler)
    port = int(os.environ.get('PORT', '8080'))
    _init_runtime()
    server = HTTPServer(('0.0.0.0', port), Handler)
    logger.info('Azure contract server listening on %s', port)
    server.serve_forever()


if __name__ == '__main__':
    main()
