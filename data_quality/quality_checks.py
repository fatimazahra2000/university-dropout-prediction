import pandas as pd


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


def run_quality_checks(df: pd.DataFrame) -> dict:
    errors = []

    # 1. Dataset non vide
    if df.empty:
        errors.append("Le dataset est vide.")

    # 2. Colonnes obligatoires
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Colonnes manquantes : {missing_columns}"
        )

    # Les contrôles suivants ne sont possibles
    # que sur les colonnes réellement présentes.
    available_required_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column in df.columns
    ]

    # 3. Valeurs nulles
    null_counts = {
        column: int(df[column].isna().sum())
        for column in available_required_columns
    }

    for column, count in null_counts.items():
        if count > 0:
            errors.append(
                f"{column}: {count} valeur(s) NULL"
            )

    # 4. Valeurs catégorielles
    for column, allowed in ALLOWED_VALUES.items():
        if column not in df.columns:
            continue

        values = set(df[column].dropna().unique())
        invalid = values - allowed

        if invalid:
            errors.append(
                f"{column}: valeurs inattendues {sorted(invalid)}"
            )

    # 5. Plages numériques
    for column, (minimum, maximum) in NUMERIC_RANGES.items():
        if column not in df.columns:
            continue

        invalid_count = int(
            (
                (df[column] < minimum)
                | (df[column] > maximum)
            ).sum()
        )

        if invalid_count > 0:
            errors.append(
                f"{column}: {invalid_count} valeur(s) "
                f"hors de [{minimum}, {maximum}]"
            )

    # 6. Doublons
    duplicates = int(df.duplicated().sum())

    if duplicates > 0:
        errors.append(
            f"{duplicates} ligne(s) dupliquée(s)"
        )

    # 7. Complétude globale
    if len(df.columns) > 0 and len(df) > 0:
        total_cells = df.shape[0] * df.shape[1]
        null_cells = int(df.isna().sum().sum())
        completeness = 1 - (null_cells / total_cells)
    else:
        completeness = 0.0

    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "completeness": round(completeness, 4),
        "duplicates": duplicates,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }