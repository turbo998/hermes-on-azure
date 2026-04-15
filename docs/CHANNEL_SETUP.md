# Channel Setup Guide

This document explains how messaging channels should connect to Hermes Agent on Azure.

---

## 1. Recommended ingress model

Use **Azure API Management** as the public webhook gateway.

Why:

- stable customer-facing endpoint structure
- throttling and policy support
- cleaner security boundary
- channel-specific request normalization

Recommended paths:

- `/webhook/telegram`
- `/webhook/slack`
- `/webhook/discord`
- `/webhook/feishu`
- `/webhook/dingtalk`
- `/webhook/wechat`
- `/agent/invoke` for demo calls

---

## 2. Telegram

Typical setup:

1. create bot with BotFather
2. store token in Key Vault
3. register webhook to APIM route
4. normalize request into Hermes invocation payload

---

## 3. Slack

Typical setup:

1. create Slack app
2. enable event subscriptions
3. store bot token and signing secret in Key Vault
4. configure APIM request validation and forwarding

---

## 4. Discord

Typical setup:

1. create Discord application
2. configure interaction endpoint to APIM
3. store credentials and public key securely
4. normalize interaction payload to runtime contract

---

## 5. Feishu / DingTalk / WeChat-style bridge

These usually need an adapter layer or payload mapping strategy.

For the workshop, the important point is:

- APIM remains the public entry
- Hermes runtime receives a normalized payload
- secrets and callback config are kept in Key Vault or environment references

---

## 6. Operating principle

The runtime should not care too much about external channel differences.
The gateway layer should absorb most of that complexity.
