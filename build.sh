#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

export PATH=$PATH:/usr/local/python3/bin && pip3 install gunicorn && make install && make collectstatic && make migrate