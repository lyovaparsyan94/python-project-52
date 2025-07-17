build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

migrate:
	uv run python manage.py makemigrations
	uv run python3 manage.py migrate

collectstatic:
	uv run python3 manage.py collectstatic --no-input

lint:
	uv run ruff check task_manager

test:
	uv run python manage.py test