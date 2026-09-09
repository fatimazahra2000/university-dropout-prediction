import duckdb


DB_PATH = "data/duckdb/university.duckdb"


def run_business_rules():
    conn = duckdb.connect(DB_PATH)

    # =========================================================
    # 1. absence_risk
    # =========================================================

    absence_risk_query = """
    SELECT COUNT(*)
    FROM main.prepared_students
    WHERE
        (studentabsencedays = 'Under-7' AND absence_risk != 0)
        OR
        (studentabsencedays = 'Above-7' AND absence_risk != 1)
        OR
        studentabsencedays IS NULL
        OR
        absence_risk IS NULL
    """

    absence_risk_violations = conn.execute(
        absence_risk_query
    ).fetchone()[0]

    # =========================================================
    # 2. risk_class
    # =========================================================

    risk_class_query = """
    SELECT COUNT(*)
    FROM main.prepared_students
    WHERE
        risk_class IS NULL
        OR class IS NULL
        OR risk_class != class
    """

    risk_class_violations = conn.execute(
        risk_class_query
    ).fetchone()[0]

    # =========================================================
    # 3. Doublons métier
    # =========================================================

    business_duplicate_query = """
    SELECT COUNT(*)
    FROM (
        SELECT
            gender,
            nationality,
            placeofbirth,
            stageid,
            gradeid,
            sectionid,
            topic,
            semester,
            relation,
            raisedhands,
            visitedresources,
            announcementsview,
            discussion,
            parentansweringsurvey,
            parentschoolsatisfaction,
            studentabsencedays,
            class
        FROM main.prepared_students
        GROUP BY ALL
        HAVING COUNT(*) > 1
    )
    """

    business_duplicate_groups = conn.execute(
        business_duplicate_query
    ).fetchone()[0]

    conn.close()

    return {
        "absence_risk_violations": absence_risk_violations,
        "risk_class_violations": risk_class_violations,
        "business_duplicate_groups": business_duplicate_groups,
    }


if __name__ == "__main__":

    result = run_business_rules()

    print("=" * 60)
    print("        BUSINESS RULE CHECK")
    print("=" * 60)

    print(
        f"Violations absence_risk : "
        f"{result['absence_risk_violations']}"
    )

    print(
        f"Violations risk_class  : "
        f"{result['risk_class_violations']}"
    )

    print(
        f"Groupes doublons métier: "
        f"{result['business_duplicate_groups']}"
    )

    total_violations = (
        result["absence_risk_violations"]
        + result["risk_class_violations"]
        + result["business_duplicate_groups"]
    )

    if total_violations == 0:
        print("Statut                  : PASS")
        print("Toutes les règles métier sont respectées.")
    else:
        print("Statut                  : FAIL")
        print("Des violations métier ont été détectées.")

    print("=" * 60)