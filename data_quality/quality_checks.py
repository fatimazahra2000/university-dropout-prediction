from pathlib import Path

import duckdb
import pandas as pd
import yaml


# ============================================================
# Chemins du projet
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONTRACT_PATH = PROJECT_ROOT / "data_quality" / "data_contract.yaml"
DATABASE_PATH = PROJECT_ROOT / "data" / "duckdb" / "university.duckdb"


# ============================================================
# Chargement du contrat
# ============================================================

def load_data_contract() -> dict:
    """
    Charge les règles de qualité depuis data_contract.yaml.
    """

    with open(CONTRACT_PATH, "r", encoding="utf-8") as file:
        contract = yaml.safe_load(file)

    return contract


# ============================================================
# Unicité métier
# ============================================================

def check_business_uniqueness(
    df: pd.DataFrame,
    columns: list[str],
) -> int:
    """
    Retourne le nombre de lignes faisant partie
    de doublons métier.

    Exemple :
        A
        A
        B
        C
        C

    retourne 4 lignes impliquées dans des doublons :
        A, A, C, C
    """

    if not columns:
        return 0

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Colonnes manquantes pour l'unicité métier : "
            f"{missing_columns}"
        )

    duplicate_mask = df.duplicated(
        subset=columns,
        keep=False,
    )

    return int(duplicate_mask.sum())


def count_business_duplicate_groups(
    df: pd.DataFrame,
    columns: list[str],
) -> int:
    """
    Retourne le nombre de groupes de doublons métier.

    Exemple :
        A
        A
        B
        C
        C

    retourne 2 groupes :
        groupe A
        groupe C
    """

    if not columns:
        return 0

    missing_columns = [
        column
        for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Colonnes manquantes pour l'unicité métier : "
            f"{missing_columns}"
        )

    duplicated_rows = df[
        df.duplicated(
            subset=columns,
            keep=False,
        )
    ]

    if duplicated_rows.empty:
        return 0

    return int(
        duplicated_rows
        .drop_duplicates(subset=columns)
        .shape[0]
    )


# ============================================================
# Contrôles qualité
# ============================================================

def run_quality_checks(
    df: pd.DataFrame,
    dataset_type: str = "raw",
) -> dict:
    """
    Exécute les contrôles qualité définis dans
    data_contract.yaml.

    dataset_type:
        - raw
        - prepared

    Les erreurs bloquantes sont placées dans "errors".
    Les problèmes non bloquants sont placés dans "warnings".
    """

    contract = load_data_contract()

    errors = []
    warnings = []

    dataset_config = contract.get("dataset", {})
    columns_config = contract.get("columns", {})
    quality_rules = contract.get("quality_rules", {})

    # Évite une variable inutilisée tout en gardant
    # la structure du contrat disponible.
    _ = dataset_config

    # ========================================================
    # 1. Dataset non vide
    # ========================================================

    if df.empty:
        errors.append(
            "Le dataset est vide."
        )

    # ========================================================
    # 2. Nombre minimum de lignes
    # ========================================================

    minimum_rows = (
        quality_rules
        .get("data_volume", {})
        .get("minimum_rows")
    )

    if (
        minimum_rows is not None
        and len(df) < minimum_rows
    ):
        errors.append(
            f"Nombre de lignes insuffisant : "
            f"{len(df)} < minimum attendu {minimum_rows}"
        )

    # ========================================================
    # 3. Colonnes obligatoires
    # ========================================================

    required_columns = list(
        columns_config.keys()
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Colonnes manquantes : {missing_columns}"
        )

    # ========================================================
    # 4. Valeurs NULL selon nullable:false
    # ========================================================

    for column, config in columns_config.items():

        if column not in df.columns:
            continue

        nullable = config.get(
            "nullable",
            True,
        )

        if not nullable:

            null_count = int(
                df[column].isna().sum()
            )

            if null_count > 0:
                errors.append(
                    f"{column}: {null_count} valeur(s) NULL "
                    f"(colonne non nullable)"
                )

    # ========================================================
    # 5. Valeurs autorisées
    # ========================================================

    for column, config in columns_config.items():

        if column not in df.columns:
            continue

        allowed_values = config.get(
            "allowed_values"
        )

        if not allowed_values:
            continue

        values = set(
            df[column]
            .dropna()
            .unique()
        )

        invalid_values = (
            values - set(allowed_values)
        )

        if invalid_values:
            errors.append(
                f"{column}: valeurs inattendues "
                f"{sorted(invalid_values)}"
            )

    # ========================================================
    # 6. Contraintes numériques
    # ========================================================

    numeric_columns = quality_rules.get(
        "numeric_ranges",
        [],
    )

    for column in numeric_columns:

        if column not in df.columns:
            continue

        config = columns_config.get(
            column,
            {}
        )

        constraints = config.get(
            "constraints",
            {}
        )

        minimum = constraints.get(
            "minimum"
        )

        maximum = constraints.get(
            "maximum"
        )

        if minimum is not None:

            invalid_count = int(
                (df[column] < minimum).sum()
            )

            if invalid_count > 0:
                errors.append(
                    f"{column}: {invalid_count} valeur(s) "
                    f"inférieure(s) à {minimum}"
                )

        if maximum is not None:

            invalid_count = int(
                (df[column] > maximum).sum()
            )

            if invalid_count > 0:
                errors.append(
                    f"{column}: {invalid_count} valeur(s) "
                    f"supérieure(s) à {maximum}"
                )

    # ========================================================
    # 7. Doublons de lignes strictement identiques
    # ========================================================

    duplicates = int(
        df.duplicated().sum()
    )

    if duplicates > 0:
        errors.append(
            f"{duplicates} ligne(s) "
            "strictement dupliquée(s)"
        )

    # ========================================================
    # 8. Unicité technique selon le contrat
    # ========================================================

    duplicate_ids = 0

    uniqueness_columns = quality_rules.get(
        "uniqueness",
        [],
    )

    for column in uniqueness_columns:

        if column not in df.columns:
            continue

        duplicate_count = int(
            df[column].duplicated().sum()
        )

        if duplicate_count > 0:

            errors.append(
                f"{duplicate_count} valeur(s) "
                f"{column} dupliquée(s)"
            )

            if column == "_dlt_id":
                duplicate_ids = duplicate_count

    # ========================================================
    # 9. Unicité métier
    # ========================================================

    business_duplicates = 0
    business_duplicate_groups = 0

    if dataset_type == "raw":

        business_uniqueness = quality_rules.get(
            "raw_business_uniqueness",
            {},
        )

        business_columns = (
            business_uniqueness.get(
                "columns",
                [],
            )
        )

        if business_columns:

            business_duplicates = (
                check_business_uniqueness(
                    df,
                    business_columns,
                )
            )

            business_duplicate_groups = (
                count_business_duplicate_groups(
                    df,
                    business_columns,
                )
            )

            # Les doublons métier RAW sont des WARNING.
            # Ils seront traités par la déduplication dbt.
            if business_duplicates > 0:
                warnings.append(
                    f"{business_duplicates} ligne(s) "
                    f"impliquée(s) dans "
                    f"{business_duplicate_groups} groupe(s) "
                    "de doublons métier RAW. "
                    "Ces doublons seront dédupliqués "
                    "dans prepared_students."
                )

    elif dataset_type == "prepared":

        business_uniqueness = quality_rules.get(
            "prepared_business_uniqueness",
            {},
        )

        business_columns = (
            business_uniqueness.get(
                "columns",
                [],
            )
        )

        if business_columns:

            business_duplicates = (
                check_business_uniqueness(
                    df,
                    business_columns,
                )
            )

            business_duplicate_groups = (
                count_business_duplicate_groups(
                    df,
                    business_columns,
                )
            )

            # Dans PREPARED, les doublons ne sont plus attendus.
            if business_duplicates > 0:
                errors.append(
                    f"{business_duplicates} ligne(s) "
                    f"impliquée(s) dans "
                    f"{business_duplicate_groups} groupe(s) "
                    "de doublons métier dans prepared_students"
                )

    # ========================================================
    # 10. Complétude globale
    # ========================================================

    if (
        len(df.columns) > 0
        and len(df) > 0
    ):

        total_cells = (
            df.shape[0] * df.shape[1]
        )

        null_cells = int(
            df.isna().sum().sum()
        )

        completeness = 1 - (
            null_cells / total_cells
        )

    else:
        completeness = 0.0

    # ========================================================
    # 11. Statut
    # ========================================================

    if errors:
        status = "FAIL"

    elif warnings:
        status = "PASS_WITH_WARNINGS"

    else:
        status = "PASS"

    # ========================================================
    # 12. Rapport
    # ========================================================

    return {
        "row_count": int(len(df)),
        "column_count": int(len(df.columns)),
        "completeness": round(
            completeness,
            4,
        ),
        "duplicates": duplicates,
        "duplicate_ids": duplicate_ids,
        "business_duplicates": business_duplicates,
        "business_duplicate_groups": (
            business_duplicate_groups
        ),
        "errors": errors,
        "warnings": warnings,
        "status": status,
    }


# ============================================================
# Exécution directe
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("        DATA QUALITY REPORT")
    print("=" * 60)

    try:

        print(
            f"Contrat utilisé : {CONTRACT_PATH}"
        )

        print(
            f"Base utilisée   : {DATABASE_PATH}"
        )

        # ----------------------------------------------------
        # Connexion DuckDB
        # ----------------------------------------------------

        conn = duckdb.connect(
            str(DATABASE_PATH)
        )

        # ----------------------------------------------------
        # Lecture des données brutes
        # ----------------------------------------------------

        df = conn.execute(
            "SELECT * FROM raw_data.students_raw"
        ).fetchdf()

        conn.close()

        # ----------------------------------------------------
        # Contrôles qualité
        # ----------------------------------------------------

        report = run_quality_checks(
            df,
            dataset_type="raw",
        )

        print(
            f"Nombre de lignes      : "
            f"{report['row_count']}"
        )

        print(
            f"Nombre de colonnes    : "
            f"{report['column_count']}"
        )

        print(
            f"Complétude            : "
            f"{report['completeness'] * 100:.2f}%"
        )

        print(
            f"Doublons de lignes    : "
            f"{report['duplicates']}"
        )

        print(
            f"IDs DLT dupliqués     : "
            f"{report['duplicate_ids']}"
        )

        print(
            f"Doublons métier       : "
            f"{report['business_duplicates']}"
        )

        print(
            f"Groupes doublons métier : "
            f"{report['business_duplicate_groups']}"
        )

        # ----------------------------------------------------
        # Erreurs
        # ----------------------------------------------------

        if report["errors"]:

            print("\nERREURS :")

            for error in report["errors"]:
                print(
                    f"  - {error}"
                )

        # ----------------------------------------------------
        # Warnings
        # ----------------------------------------------------

        if report["warnings"]:

            print("\nWARNINGS :")

            for warning in report["warnings"]:
                print(
                    f"  - {warning}"
                )

        # ----------------------------------------------------
        # Statut
        # ----------------------------------------------------

        print(
            f"\nStatut                : "
            f"{report['status']}"
        )

        if report["status"] == "PASS":
            print(
                "\nTous les contrôles qualité sont PASS."
            )

        elif report["status"] == "PASS_WITH_WARNINGS":
            print(
                "\nLes contrôles bloquants sont PASS."
            )
            print(
                "Des warnings ont été détectés "
                "et doivent être surveillés."
            )

        else:
            print(
                "\nDes erreurs de qualité "
                "ont été détectées."
            )

        print("=" * 60)

    except Exception as e:

        print(
            "\nERREUR lors de l'exécution "
            "des contrôles qualité :"
        )

        print(e)