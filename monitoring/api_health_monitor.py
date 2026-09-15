"""
Monitoring du service (API) — disponibilité, temps de réponse, erreurs.

À distinguer de model_monitor.py / service_monitor.py (monitoring ML,
responsabilité de Wijdane) : ce script surveille la santé technique du
service API, pas les performances du modèle.
"""

import csv
import os
import sys
import time
from datetime import datetime, timezone

import requests

# URL de l'API — surchargeable via variable d'environnement
API_URL = os.environ.get("API_URL", "http://localhost:3501")
HEALTH_ENDPOINT = f"{API_URL}/health"

METRICS_FILE = os.path.join(os.path.dirname(__file__), "service_metrics.csv")

TIMEOUT_SECONDS = 5


def check_health() -> dict:
    """Effectue une requête sur /health et mesure la latence."""
    timestamp = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()

    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=TIMEOUT_SECONDS)
        elapsed_ms = (time.perf_counter() - start) * 1000
        success = response.status_code == 200
        return {
            "timestamp": timestamp,
            "status_code": response.status_code,
            "response_time_ms": round(elapsed_ms, 2),
            "success": success,
            "error": "" if success else f"HTTP {response.status_code}",
        }
    except requests.exceptions.RequestException as exc:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return {
            "timestamp": timestamp,
            "status_code": None,
            "response_time_ms": round(elapsed_ms, 2),
            "success": False,
            "error": str(exc),
        }


def log_result(result: dict) -> None:
    """Ajoute le résultat dans le fichier CSV (créé s'il n'existe pas)."""
    file_exists = os.path.isfile(METRICS_FILE)
    with open(METRICS_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)


def main() -> int:
    result = check_health()
    log_result(result)

    if result["success"]:
        print(
            f"[OK] {result['timestamp']} — "
            f"API disponible ({result['response_time_ms']} ms)"
        )
        return 0
    else:
        print(
            f"[ERREUR] {result['timestamp']} — "
            f"API indisponible : {result['error']}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())