import dlt
import pandas as pd

def ingest_student_data(database_path="data/duckdb/university.duckdb"):
    # 1. Charger le fichier CSV avec pandas
    # On précise le nom exact de ton fichier
    file_path = "data/raw/xAPI-Edu-Data.csv"
    df = pd.read_csv(file_path)
    
    # Nettoyage rapide des noms de colonnes (pour éviter les problèmes de SQL plus tard)
    df.columns = [c.replace('-', '_').replace(' ', '_').lower() for c in df.columns]

    # 2. Configurer le pipeline dlt
    # Destination : duckdb | Nom de la base : 'student_data'
    pipeline = dlt.pipeline(
        pipeline_name="student_pipeline",
        destination=dlt.destinations.duckdb(database_path),
        dataset_name="raw_data"
    )
    # 3. Lancer l'ingestion vers la table 'students_raw'
    load_info = pipeline.run(
        df.to_dict(orient="records"), 
        table_name="students_raw", 
        write_disposition="replace"
    )

    print("--- Ingestion terminée avec succès ! ---")
    print(load_info)

if __name__ == "__main__":
    ingest_student_data()