#!/usr/bin/env bash
set -o errexit

# Устанавливаем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Устанавливаем gunicorn в system PATH (доступен для startCommand)
pip install --upgrade pip
pip install gunicorn

# Остальная сборка проекта
make install
make collectstatic
make migrate
make compilemessages  # если используется локализация
