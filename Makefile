build:
	./build.sh

lint:
	uv run ruff check task_manager

compilemessages:
	django-admin compilemessages

makemessages:
	django-admin makemessages -l ru

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

install:
	uv sync

dev:
	uv run python manage.py runserver

start:
	uv run gunicorn -w 2 -b 0.0.0.0:8000 task_manager.wsgi

test:
	uv run ./manage.py test