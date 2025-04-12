#!/usr/bin/env bash
# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Обновляем pip, устанавливаем gunicorn системно
pip install --upgrade pip
pip install gunicorn

# Делаем make-процедуры: установка, статика, миграции
make install
make collectstatic
make migrate
make compilemessages
