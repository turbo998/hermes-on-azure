"""HTTP contract server for Hermes Agent on Azure Container Apps.

Endpoints:
- GET /healthz   -> liveness probe
- GET /readyz    -> readiness probe
- POST /invocations -> normalized invocation endpoint

This version introduces a basic runtime adapter seam so the workshop repo can
show how a real Hermes runtime would be plugged in later without rewriting the
HTTP contract layer.
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


class RuntimeAdapter:
    """Workshop runtime adapter seam.

    Today this remains a placeholder implementation, but the surrounding code now
    treats it as an injectable runtime boundary.
    """

    def __init__(self, provider_config: dict[str, str]) -> None:
        self.provider_config = provider_config

    def chat(self, message: str, channel: str, user_id: str) -> str:
        provider_mode = self.provider_config.get('providerMode', 'unknown')
        return f'Hermes Agent on Azure ({provider_mode}) received from {channel}/{user_id}: {message}'

    def cron(self, prompt: str) -> str:
        return f'Cron execution placeholder: {prompt}'


class State:
    agent_ready: bool = False
    lightweight_ready: bool = True
    provider_config: dict[str, str] | None = None
    workspace_sync: WorkspaceSync | None = None
    runtime_adapter: RuntimeAdapter | None = None
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
            self._send_json(_status_payload(), status=200 if S.agent_ready else 503)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path != '/invocations':
            self.send_error(404)
            return

        raw = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        body = json.loads(raw or b'{}')
        action = body.get('action', 'chat')

        with S.busy_lock:
            S.busy_count += 1
        try:
            if action == 'status':
                self._send_json(_status_payload())
                return
            if action == 'warmup':
                self._send_json({'status': 'ready' if S.agent_ready else 'warming'})
                return
            if action == 'cron':
                self._send_json(_handle_cron(body))
                return
            self._send_json(_handle_chat(body))
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
        'status': 'ready' if S.agent_ready else 'starting',
        'agentReady': S.agent_ready,
        'lightweightReady': S.lightweight_ready,
        'providerConfig': S.provider_config or {},
        'busyCount': S.busy_count,
        'uptimeSeconds': int(time.time() - S.start_time),
    }


def _handle_chat(body: dict[str, Any]) -> dict[str, Any]:
    message = body.get('message', '')
    channel = body.get('channel', 'azure')
    user_id = body.get('userId', 'unknown')
    response_text = S.runtime_adapter.chat(message, channel, user_id) if S.runtime_adapter else message
    return {
        'response': response_text,
        'provider': S.provider_config or {},
    }


def _handle_cron(body: dict[str, Any]) -> dict[str, Any]:
    prompt = body.get('config', {}).get('prompt', body.get('message', ''))
    response_text = S.runtime_adapter.cron(prompt) if S.runtime_adapter else prompt
    return {
        'ready': S.agent_ready,
        'jobId': body.get('jobId', ''),
        'response': response_text,
        'provider': S.provider_config or {},
    }


def _init_runtime() -> None:
    S.provider_config = configure_azure_provider()

    storage_account = os.environ.get('WORKSPACE_STORAGE_ACCOUNT', '')
    storage_container = os.environ.get('WORKSPACE_CONTAINER', 'hermes-workspace')
    workspace_namespace = os.environ.get('WORKSPACE_NAMESPACE', '')
    if storage_account and workspace_namespace:
        sync = WorkspaceSync(
            account_name=storage_account,
            container_name=storage_container,
            workspace=os.environ.get('HERMES_HOME', '/mnt/workspace/.hermes'),
            sync_interval=int(os.environ.get('WORKSPACE_SYNC_INTERVAL', '300')),
        )
        sync.restore(workspace_namespace)
        sync.start_periodic_save(workspace_namespace)
        S.workspace_sync = sync

    S.runtime_adapter = RuntimeAdapter(S.provider_config)
    S.agent_ready = True
    logger.info('Azure runtime initialized: %s', S.provider_config)


def _sigterm_handler(signum: int, frame: Any) -> None:
    try:
        namespace = os.environ.get('WORKSPACE_NAMESPACE', '')
        if S.workspace_sync and namespace:
            S.workspace_sync.save(namespace)
            S.workspace_sync.stop()
    finally:
        sys.exit(0)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(levelname)s %(message)s')
    signal.signal(signal.SIGTERM, _sigterm_handler)
    port = int(os.environ.get('PORT', '8080'))
    _init_runtime()
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.request_queue_size = 32
    logger.info('Azure contract server listening on %s', port)
    server.serve_forever()


if __name__ == '__main__':
    main()
