import mlflow
import matplotlib.pyplot as plt

mlflow.set_tracking_uri("http://localhost:5001")

# Récupérer tous les runs de monitoring loggés jusqu'ici
experiment = mlflow.get_experiment_by_name("university-dropout-prediction")
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="tags.mlflow.runName = 'monitoring-check'"
)

if runs.empty:
    print("Aucun run de monitoring trouvé. Lance d'abord model_monitor.py plusieurs fois.")
else:
    fig, axes = plt.subplots(2, 1, figsize=(8, 8))

    axes[0].plot(runs["start_time"], runs["metrics.monitoring_accuracy"], marker="o", label="Accuracy")
    axes[0].plot(runs["start_time"], runs["metrics.monitoring_f1_macro"], marker="o", label="F1-macro")
    axes[0].set_title("Performance du modèle dans le temps")
    axes[0].legend()
    axes[0].tick_params(axis="x", rotation=45)

    axes[1].plot(runs["start_time"], runs["metrics.max_feature_drift"], marker="o", color="red")
    axes[1].set_title("Dérive maximale détectée (drift)")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig("monitoring/dashboard.png", dpi=150)
    print("✅ Dashboard sauvegardé dans monitoring/dashboard.png")