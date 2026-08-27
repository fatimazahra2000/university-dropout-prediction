FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fixes de compatibilite specifiques a ce conteneur (ne touche pas requirements.txt partage)
RUN pip install --no-cache-dir protobuf==4.25.3 "sqlalchemy<2.0" mlflow==2.14.1

COPY . .

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "sqlite:////app/mlflow_store/mlflow.db", "--default-artifact-root", "/app/mlflow_store/mlartifacts"]