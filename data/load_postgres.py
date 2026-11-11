
import os
from pathlib import Path
from urllib.parse import urlparse, unquote

import psycopg2
from dotenv import load_dotenv
import csv
from psycopg2 import sql


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "generated"
SCHEMA_FILE = ROOT / "database" / "schema.sql"

# Load CSVs in foreign-key dependency order.
CSV_TABLES = [
    ("applicants", "applicants.csv"),
    ("loan_products", "loan_products.csv"),
    ("employment", "employment.csv"),
    ("income_sources", "income_sources.csv"),
    ("loan_applications", "loan_applications.csv"),
    ("credit_facilities", "credit_facilities.csv"),
    ("application_documents", "application_documents.csv"),
    ("affordability_checks", "affordability_checks.csv"),
    ("loan_decisions", "loan_decisions.csv"),
    ("repayment_schedules", "repayment_schedules.csv"),
    ("repayment_installments", "repayment_installments.csv"),
    ("disbursements", "disbursements.csv"),
    ("anomaly_cases", "anomaly_cases.csv"),
]


def get_connection():
    load_dotenv(ROOT / ".env")
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is missing from .env")

    # Support SQLAlchemy-style PostgreSQL URLs.
    database_url = database_url.replace(
        "postgresql+psycopg2://", "postgresql://", 1
    )

    parsed = urlparse(database_url)

    return psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path.lstrip("/"),
        user=unquote(parsed.username or ""),
        password=unquote(parsed.password or ""),
    )



def copy_csv(cursor, table_name, csv_path):
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")

    # Read the CSV header to identify the available columns.
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        columns = next(reader)

    if not columns:
        raise ValueError(f"No columns found in {csv_path}")

    # Import only the columns present in the CSV.
    copy_query = sql.SQL(
        'COPY {} ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
    ).format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(sql.Identifier(column) for column in columns)
    )

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        cursor.copy_expert(copy_query.as_string(cursor), file)

    print(f"Loaded: {table_name}")



def load_ground_truth(cursor):
    csv_path = DATA_DIR / "ground_truth.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")

    cursor.execute("""
        CREATE TEMP TABLE ground_truth_staging (
            ground_truth_id VARCHAR(30),
            anomaly_id VARCHAR(30),
            expected_anomaly BOOLEAN,
            expected_anomaly_type VARCHAR(100),
            notes TEXT
        )
    """)

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        cursor.copy_expert(
            """
            COPY ground_truth_staging
            FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
            """,
            file,
        )

    cursor.execute("""
        INSERT INTO ground_truth_anomalies (
            ground_truth_id,
            anomaly_id,
            application_id,
            expected_anomaly,
            expected_anomaly_type,
            notes
        )
        SELECT
            s.ground_truth_id,
            s.anomaly_id,
            a.application_id,
            s.expected_anomaly,
            s.expected_anomaly_type,
            s.notes
        FROM ground_truth_staging s
        JOIN anomaly_cases a
          ON a.anomaly_id = s.anomaly_id
    """)

    # Add a negative label for each normal application and anomaly type.
    cursor.execute("""
        INSERT INTO ground_truth_anomalies (
            ground_truth_id,
            anomaly_id,
            application_id,
            expected_anomaly,
            expected_anomaly_type,
            notes
        )
        SELECT
            'GT-' || LPAD(
                (600 + ROW_NUMBER() OVER (
                    ORDER BY la.application_id, types.anomaly_type
                ))::TEXT,
                6,
                '0'
            ),
            NULL,
            la.application_id,
            FALSE,
            types.anomaly_type,
            'Normal application: no injected anomaly for this anomaly type'
        FROM loan_applications la
        CROSS JOIN (
            VALUES
                ('INVALID_LOAN_TENURE'),
                ('SCHEDULE_RECONCILIATION_MISMATCH'),
                ('DECISION_BEFORE_REQUIRED_CHECKS'),
                ('INCOME_SOURCE_CONFLICT'),
                ('DUPLICATE_DISBURSEMENT')
        ) AS types(anomaly_type)
        WHERE NOT EXISTS (
            SELECT 1
            FROM ground_truth_anomalies gt
            WHERE gt.application_id = la.application_id
              AND gt.expected_anomaly_type = types.anomaly_type
        )
    """)

    print("Loaded: ground_truth_anomalies (positive and negative labels)")


def main():
    connection = get_connection()

    try:
        connection.autocommit = False

        with connection.cursor() as cursor:
            # Create all tables and indexes.
            schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
            cursor.execute(schema_sql)
            print("Database schema created.")

            for table_name, filename in CSV_TABLES:
                copy_csv(cursor, table_name, DATA_DIR / filename)

            load_ground_truth(cursor)

        connection.commit()
        print("\nSUCCESS: Synthetic dataset loaded successfully.")

    except Exception:
        connection.rollback()
        print("\nERROR: Loading failed. Transaction rolled back.")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
