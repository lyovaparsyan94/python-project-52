#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

make install && make migrate && uv run python manage.py loaddata task_manager/fixtures/data.json && make collectstatic && make create-su

