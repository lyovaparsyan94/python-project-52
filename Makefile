migrate:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

translate:
	uv run django-admin makemessages --locale ru
	uv run python manage.py compilemessages

collectstatic:
	uv run python manage.py collectstatic --noinput

tests:
	uv run python3 manage.py test

dev:
	uv run python3 manage.py runserver

install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi 
	
