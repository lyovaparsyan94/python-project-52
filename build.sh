#!/usr/bin/env bash
set -o errexit

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

pip install --upgrade pip
pip install gunicorn

# ХАК: скопировать gunicorn туда, где Render его ищет
mkdir -p .venv/bin
cp $(which gunicorn) .venv/bin/gunicorn

make install
make collectstatic
make migrate
make compilemessages
