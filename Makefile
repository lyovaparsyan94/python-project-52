dev:
		uv run manage.py runserver
build:
		./build.sh
render-start:
		uv run gunicorn task_manager.wsgi
lint:
		uv run ruff check
lint-fix:
		uv run ruff check --fix
install:
		uv sync
collectstatic:
		uv run manage.py collectstatic --no-input
migrate:
		uv run manage.py migrate
compilemessages:
		uv run manage.py compilemessages