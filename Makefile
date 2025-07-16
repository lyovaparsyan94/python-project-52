install:
	uv sync

build:
	chmod +x ./build.sh
	./build.sh

render-start:
	gunicorn task_manager.wsgi

update_lang:
	uv run django-admin makemessages -l ru

compile_lang:
	uv run django-admin compilemessages

start-server:
	uv run python3 manage.py runserver

check:
	uv run ruff check

makemigrations:
	uv run python3 manage.py makemigrations

migrate:
	uv run python3 manage.py migrate

setup: install migrate

test:
	uv run python3 manage.py test