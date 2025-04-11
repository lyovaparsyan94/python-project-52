#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
uv sync --all-packages

# Convert static asset files
uv run python manage.py collectstatic --no-input

# Apply any outstanding database migrations
uv run python manage.py migrate