import duckdb
import sys

DB_PATH = "student_pipeline.duckdb"
TABLE = "raw_data.students_raw"

REQUIRED_COLUMNS = [
    "gender",
    "nationality",
    "placeofbirth",
    "stageid",
    "gradeid",
    "sectionid",
    "topic",
    "semester",
    "relation",
    "raisedhands",
    "visitedresources",
    "announcementsview",
    "discussion",
    "parentansweringsurvey",
    "parentschoolsatisfaction",
    "studentabsencedays",
    "class",
]

ALLOWED_VALUES = {
    "gender": {"M", "F"},
    "stageid": {"lowerlevel", "MiddleSchool", "HighSchool"},
    "sectionid": {"A", "B", "C"},
    "semester": {"F", "S"},
    "relation": {"Father", "Mum"},
    "parentansweringsurvey": {"Yes", "No"},
    "parentschoolsatisfaction": {"Good", "Bad"},
    "studentabsencedays": {"Under-7", "Above-7"},
    "class": {"L", "M", "H"},
}

NUMERIC_RANGES = {
    "raisedhands": (0, 100),
    "visitedresources": (0, 100),
    "announcementsview": (0, 100),
    "discussion": (0, 100),
}


def check(condition, message):
    if condition:
        print(f"[PASS] {message}")
        return True

    print(f"[FAIL] {message}")
    return False


def main():
    con = duckdb.connect(DB_PATH)
    failures = 0

    print("=" * 50)
    print("       DATA QUALITY REPORT")
    print("=" * 50)

    # 1. Dataset non vide
    total_rows = con.execute(
        f"SELECT COUNT(*) FROM {TABLE}"
    ).fetchone()[0]

    if not check(
        total_rows > 0,
        f"Dataset non vide ({total_rows} lignes)"
    ):
        failures += 1

    # 2. Colonnes obligatoires
    columns = {
        row[0]
        for row in con.execute(
            f"DESCRIBE {TABLE}"
        ).fetchall()
    }

    for column in REQUIRED_COLUMNS:
        if not check(
            column in columns,
            f"Colonne présente : {column}"
        ):
            failures += 1

    # 3. Unicité de _dlt_id
    total_ids, distinct_ids = con.execute(
        f"""
        SELECT
            COUNT(_dlt_id),
            COUNT(DISTINCT _dlt_id)
        FROM {TABLE}
        """
    ).fetchone()

    if not check(
        total_ids == distinct_ids,
        "_dlt_id unique"
    ):
        failures += 1

    # 4. Valeurs nulles
    for column in REQUIRED_COLUMNS:
        null_count = con.execute(
            f"""
            SELECT COUNT(*)
            FROM {TABLE}
            WHERE {column} IS NULL
            """
        ).fetchone()[0]

        if not check(
            null_count == 0,
            f"{column}: aucune valeur NULL"
        ):
            failures += 1

    # 5. Valeurs catégorielles
    for column, allowed in ALLOWED_VALUES.items():

        values = {
            row[0]
            for row in con.execute(
                f"""
                SELECT DISTINCT {column}
                FROM {TABLE}
                """
            ).fetchall()
        }

        invalid = values - allowed

        if not check(
            not invalid,
            f"{column}: valeurs valides"
        ):
            print(f"       Valeurs inattendues : {invalid}")
            failures += 1

    # 6. Plages numériques
    for column, (minimum, maximum) in NUMERIC_RANGES.items():

        invalid_count = con.execute(
            f"""
            SELECT COUNT(*)
            FROM {TABLE}
            WHERE {column} < {minimum}
               OR {column} > {maximum}
            """
        ).fetchone()[0]

        if not check(
            invalid_count == 0,
            f"{column}: valeurs dans [{minimum}, {maximum}]"
        ):
            failures += 1

    con.close()

    print("=" * 50)

    if failures == 0:
        print("RESULT: PASS")
        print("Toutes les règles de qualité sont respectées.")
        print("=" * 50)
        sys.exit(0)

    print(f"RESULT: FAIL ({failures} contrôle(s) en échec)")
    print("=" * 50)

    sys.exit(1)


if __name__ == "__main__":
    main()