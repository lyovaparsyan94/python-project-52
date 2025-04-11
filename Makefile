install:
	uv sync --all-packages
build:
	./build.sh
test:
	uv run python manage.py test
lint:
	uv run ruff check
lint-fix:
	uv ruff check --fix
start:
	gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker