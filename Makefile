dev:
	uv run python3 manage.py runserver

translate:
	uv run django-admin makemessages --locale ru
	uv run python manage.py compilemessages

migrate:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

tests:
	uv run python3 manage.py test

install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi 
	
collectstatic:
	uv run python manage.py collectstatic --noinput

