# Синхронизация зависимостей через uv (обязательно для создания окружения)
install:
	uv sync

# Сбор статических файлов
collectstatic:
	uv run python manage.py collectstatic --noinput

# Применение миграций
migrate:
	uv run python manage.py migrate

# Цель сборки: запускает скрипт сборки
build:
	./build.sh

# Цель старта: запускает сервер через uv, который гарантирует, что нужное окружение активно
render-start:
	.venv/bin/python -m gunicorn --chdir hexlet-code task_manager.wsgi
