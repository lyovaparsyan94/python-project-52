install:
	uv sync --dev

dev-start:
	uv run python manage.py runserver

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input

lint:
	uv run flake8 .

test:
	uv run pytest

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

push:
	git add . & git commit -m 'thangs' & git push