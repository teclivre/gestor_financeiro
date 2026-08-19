#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/3] Atualizando código via Git..."
git pull --rebase origin "$(git branch --show-current)"

echo "[2/3] Reconstruindo imagens Docker..."
docker compose build --no-cache

echo "[3/3] Reiniciando containers..."
docker compose up -d

echo "Deploy atualizado com sucesso."
