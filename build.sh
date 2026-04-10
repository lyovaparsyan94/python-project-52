#!/usr/bin/env bash
set -o errexit

# Устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Устанавливаем зависимости
uv sync --frozen

cd $(dirname $(find . | grep manage.py$))

# Миграции и статика
uv run python manage.py collectstatic --no-input
uv run python manage.py migrate

echo "✅ Build completed!"
