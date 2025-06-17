dev:
		uv run python manage.py runserver

install:
		uv sync


build:
		./build.sh

check:
	 	uv run ruff check .

render-start:
		gunicorn task_manager.wsgi

start:
	uv run manage.py runserver 0.0.0.0:8000

start2:
		uv run gunicorn task_manager.wsgi

migrations:
		uv run python manage.py makemigrations

migrate:
		uv run python manage.py migrate

create-su:
		uv run python manage.py make_su

collectstatic:
		uv run python manage.py collectstatic --noinput --clear

test:
		uv run python manage.py test

write-fixture:
		uv run python manage.py dumpdata > task_manager/fixtures/data.json


