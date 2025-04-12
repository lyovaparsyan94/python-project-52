#!/usr/bin/env bash
set -e

echo "Скачиваем uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
# Используем точку вместо source для совместимости во всех POSIX-оболочках
. $HOME/.local/bin/env

#echo "Устанавливаем gunicorn..."
#pip3 install gunicorn

echo "Синхронизируем зависимости..."
make install

echo "Собираем статику..."
make collectstatic

echo "Применяем миграции..."
make migrate

# Если нужны переводы – раскомментируйте следующие строки:
# echo "Компилируем переводы..."
# uv run python manage.py compilemessages

echo "Build script выполнен успешно."
