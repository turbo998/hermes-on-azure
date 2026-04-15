#!/usr/bin/env bash
set -euo pipefail

CHANNEL="${1:-}"
APIM_HOST="${2:-}"

if [[ -z "$CHANNEL" || -z "$APIM_HOST" ]]; then
  echo "Usage: $0 <telegram|slack|discord|feishu|dingtalk|wechat> <apim-host>" >&2
  exit 1
fi

case "$CHANNEL" in
  telegram)
    echo "Telegram webhook: https://${APIM_HOST}/webhook/telegram"
    ;;
  slack)
    echo "Slack request URL: https://${APIM_HOST}/webhook/slack"
    ;;
  discord)
    echo "Discord interactions endpoint: https://${APIM_HOST}/webhook/discord"
    ;;
  feishu)
    echo "Feishu callback URL: https://${APIM_HOST}/webhook/feishu"
    ;;
  dingtalk)
    echo "DingTalk callback URL: https://${APIM_HOST}/webhook/dingtalk"
    ;;
  wechat)
    echo "WeChat bridge callback URL: https://${APIM_HOST}/webhook/wechat"
    ;;
  *)
    echo "Unsupported channel: $CHANNEL" >&2
    exit 1
    ;;
esac
