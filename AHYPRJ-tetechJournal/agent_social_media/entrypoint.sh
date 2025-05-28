#!/bin/sh
echo "🔁 Verificando/Atualizando token Instagram..."
python tokenAutoUpdate.py

echo "🚀 Iniciando API FastAPI..."
exec uvicorn autopostapi:app --host 0.0.0.0 --port 1113
