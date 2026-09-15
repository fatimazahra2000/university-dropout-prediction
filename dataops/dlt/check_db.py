import duckdb

# Connexion à la base de données que tu viens de créer
con = duckdb.connect("student_pipeline.duckdb")

# Afficher les tables disponibles
print("--- Tables dans la base ---")
print(con.execute("SHOW TABLES").fetchall())

# Afficher les 5 premières lignes
print("\n--- Aperçu des données (5 lignes) ---")
df = con.execute("SELECT * FROM raw_data.students_raw LIMIT 5").df()
print(df)

con.close()