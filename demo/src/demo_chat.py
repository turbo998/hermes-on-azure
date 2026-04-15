#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import requests


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', required=True)
    parser.add_argument('--message', required=True)
    args = parser.parse_args()

    payload = {
        'action': 'chat',
        'userId': 'demo-user',
        'channel': 'demo-cli',
        'message': args.message,
    }
    response = requests.post(args.endpoint, json=payload, timeout=120)
    response.raise_for_status()
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
