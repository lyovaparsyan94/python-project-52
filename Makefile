dev:
	uv run python3 manage.py runserver

translate:
	uv run django-admin makemessages --locale ru
	uv run python manage.py compilemessages

migrate:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

test:
	uv run python3 manage.py test

test-coverage:
	uv run coverage run --source='.' manage.py test
	uv run coverage xml

install:
	uv sync

build:
	./build.sh

render-start:
	.venv/bin/gunicorn --bind 0.0.0.0:$$PORT task_manager.wsgi

collectstatic:
	uv run python manage.py collectstatic --noinput

lint:
	uv run ruff check task_manager

check: test lint