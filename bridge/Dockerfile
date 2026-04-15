FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     curl ca-certificates     && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir azure-identity azure-storage-blob requests

COPY bridge/ /app/bridge/

ENV PYTHONPATH="/app"     PORT=8080     PYTHONUNBUFFERED=1

EXPOSE 8080
RUN chmod +x /app/bridge/entrypoint.sh
ENTRYPOINT ["/app/bridge/entrypoint.sh"]
