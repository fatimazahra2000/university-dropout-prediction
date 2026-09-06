FROM python:3.11-slim
WORKDIR /app

# Installer uniquement les dependances necessaires a l'API
# (fichier allege, distinct de requirements.txt qui contient aussi
# dagster/mlflow/dbt pour les autres services)
COPY requirements-api.txt .
RUN pip install --no-cache-dir --default-timeout=120 -r requirements-api.txt

# Copier le code de l'API et les artefacts du modele
COPY api/ ./api/
COPY ml/models/ ./ml/models/
WORKDIR /app/api
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]