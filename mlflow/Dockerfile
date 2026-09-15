FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Same MLflow/protobuf stack as Dagster. One worker is enough for local development
# and uses considerably less RAM than the default multi-worker server.
# `mlflow:5000` is allowed because Dagster reaches this container by its Compose service name.
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--workers", "1", "--allowed-hosts", "localhost:*,127.0.0.1:*,mlflow:5000", "--backend-store-uri", "sqlite:////app/mlflow_store/mlflow.db", "--artifacts-destination", "/app/mlflow_store/mlartifacts"]
