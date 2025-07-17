#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# команды установки зависимостей, сборки статики, применения миграций
make install && make collectstatic && make migrate