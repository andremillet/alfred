#!/bin/sh
# Script para executar o Alfred a partir do diretório do projeto

# Encontra o diretório onde o script está e executa o alfred.py a partir de lá
SCRIPT_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
python3 "$SCRIPT_DIR/alfred.py" "$@"
