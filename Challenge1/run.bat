@echo off
REM 1) cria o venv se necessário
if not exist ".venv" (
  python -m venv .venv
)

REM 2) ativa o virtualenv
call .venv\Scripts\activate.bat

REM 3) instala/atualiza dependências
pip install --upgrade pip
pip install -r requirements.txt

REM 4) roda o chat
python chat.py

pause
