"""
Dashboard du monitoring du service (API) — disponibilite et latence.

A distinguer de monitoring/service_monitor.py (dashboard ML de Wijdane,
genere depuis MLflow). Ce script lit service_metrics.csv, genere par
api_health_monitor.py.
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

METRICS_FILE = os.path.join(os.path.dirname(__file__), "service_metrics.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "service_dashboard.png")


def main() -> None:
    if not os.path.isfile(METRICS_FILE):
        print(
            "Aucune donnee trouvee. Lance d'abord api_health_monitor.py "
            "plusieurs fois."
        )
        return

    df = pd.read_csv(METRICS_FILE, parse_dates=["timestamp"])

    fig, axes = plt.subplots(2, 1, figsize=(8, 8))

    # Graphique 1 : temps de reponse dans le temps
    axes[0].plot(
        df["timestamp"], df["response_time_ms"], marker="o", color="steelblue"
    )
    axes[0].set_title("Temps de reponse de l'API (ms)")
    axes[0].set_ylabel("ms")
    axes[0].tick_params(axis="x", rotation=45)

    # Graphique 2 : disponibilite (taux de succes glissant)
    availability_pct = df["success"].astype(int) * 100
    axes[1].plot(
        df["timestamp"], availability_pct, marker="o", color="green",
        drawstyle="steps-post",
    )
    axes[1].set_title("Disponibilite (200 = OK, 0 = echec)")
    axes[1].set_ylim(-10, 110)
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)

    total = len(df)
    successes = df["success"].sum()
    uptime_pct = (successes / total) * 100 if total else 0
    avg_latency = df["response_time_ms"].mean()

    print(f"Dashboard sauvegarde dans {OUTPUT_FILE}")
    print(f"Disponibilite mesuree : {uptime_pct:.1f}% ({successes}/{total} checks)")
    print(f"Latence moyenne : {avg_latency:.2f} ms")


if __name__ == "__main__":
    main()