"""HTTP contract server for Hermes Agent on Azure Container Apps.

Endpoints:
- GET /healthz
- GET /readyz
- POST /invocations
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

logger = logging.getLogger('azure.contract')


class State:
    agent: Any = None
    agent_ready: bool = False
    lightweight_ready: bool = False
    busy_count: int = 0
    busy_lock = threading.Lock()
    start_time: float = time.time()


S = State()


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self) -> None:
        if self.path == '/healthz':
            self._send_json({'status': 'ok'})
            return
        if self.path == '/readyz':
            self._send_json({'status': 'ready' if S.agent_ready else 'starting', 'busyCount': S.busy_count}, status=200 if S.agent_ready else 503)
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
            message = body.get('message', '')
            result = {
                'response': f'Hermes Agent on Azure placeholder response: {message}'
            }
            self._send_json(result)
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


def _sigterm_handler(signum: int, frame: Any) -> None:
    sys.exit(0)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(levelname)s %(message)s')
    signal.signal(signal.SIGTERM, _sigterm_handler)
    port = int(os.environ.get('PORT', '8080'))
    S.agent_ready = True
    server = HTTPServer(('0.0.0.0', port), Handler)
    logger.info('Azure contract server listening on %s', port)
    server.serve_forever()


if __name__ == '__main__':
    main()
