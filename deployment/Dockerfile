FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances d'abord (meilleur cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'API et les artefacts du modèle
COPY api/ ./api/
COPY ml/models/ ./ml/models/

WORKDIR /app/api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]