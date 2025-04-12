#!/usr/bin/env bash
set -e

echo "Скачиваем uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# При необходимости расширяем PATH (если требуется для Python)
export PATH=$PATH:/usr/local/python3/bin

echo "Устанавливаем gunicorn..."
pip3 install gunicorn

echo "Синхронизируем зависимости..."
make install

echo "Собираем статику..."
make collectstatic

echo "Применяем миграции..."
make migrate

echo "Build script выполнен успешно."
