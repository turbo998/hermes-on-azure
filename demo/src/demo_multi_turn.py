#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import requests


def invoke(endpoint: str, message: str) -> dict:
    payload = {
        'action': 'chat',
        'userId': 'demo-multi',
        'channel': 'demo-cli',
        'message': message,
    }
    response = requests.post(endpoint, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--endpoint', required=True)
    args = parser.parse_args()

    for prompt in [
        'Hello, my name is Azure Workshop User.',
        'Summarize your Azure architecture.',
        'What is my name?',
    ]:
        print(json.dumps(invoke(args.endpoint, prompt), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
