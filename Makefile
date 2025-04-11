dev:
		uv run python manage.py runserver 0.0.0.0:9000
build:
		./build.sh
render-start:
		gunicorn task_manager.wsgi
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