#!/usr/bin/env bash
# 1. Cria/ativa venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Atualiza pip e instala deps
pip install --upgrade pip
pip install -r requirements.txt

# 3. Roda o servidor Flask via chat.py
exec python3 chat.py
