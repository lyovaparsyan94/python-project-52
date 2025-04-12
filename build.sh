#!/usr/bin/env bash
set -e

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Дополнительно расширяем PATH при необходимости
export PATH=$PATH:/usr/local/python3/bin

# Устанавливаем gunicorn, если не установлен через зависимости
pip3 install gunicorn

# Синхронизация зависимостей
make install

# Сбор статики и применение миграций
make collectstatic
make migrate

echo "Build script выполнен успешно."
