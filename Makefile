build:
    ./build.sh

render-start:
    gunicorn task_manager.wsgi

lint:
    uv run flake8 task_manager

install:
    uv sync

start:
    uv python manage.py runserver

collectstatic:
    uv python manage.py collectstatic --noinput

migrate:
    uv run python manage.py migrate --noinput

test: migrate
    uv run python manage.py test

test-verbose: migrate
    uv run python manage.py test --verbosity=2