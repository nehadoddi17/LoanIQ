
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect


ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

TABLE_DESCRIPTIONS = {
    "applicants": "Stores applicant personal details and credit profile.",
    "employment": "Stores applicant employment and salary information.",
    "income_sources": "Stores applicant income sources and verification status.",
    "loan_products": "Defines available loan products, limits, rates and eligibility rules.",
    "loan_applications": "Stores loan requests, applicant references and application status.",
    "credit_facilities": "Stores existing credit accounts and repayment obligations.",
    "application_documents": "Tracks documents submitted for applications and their verification.",
    "affordability_checks": "Stores affordability calculations and assessment outcomes.",
    "loan_decisions": "Stores loan evaluation decisions and decision history.",
    "repayment_schedules": "Stores repayment schedule summaries for loan applications.",
    "repayment_installments": "Stores individual repayment installment details.",
    "disbursements": "Tracks simulated loan disbursement records.",
    "anomaly_cases": "Stores detected anomaly records and their detection status.",
    "ground_truth_anomalies": "Stores positive and negative labels used to evaluate anomaly detection.",
    "audit_events": "Stores audit events for tracking system activity.",
}

output_file = ROOT / "docs" / "data_dictionary.md"
output_file.parent.mkdir(parents=True, exist_ok=True)

lines = [
    "# LoanIQ Data Dictionary",
    "",
    "## Overview",
    "",
    "LoanIQ uses PostgreSQL to store applicant, loan, repayment, "
    "decision, and anomaly-detection data.",
    "",
    "This document is generated from the database schema.",
    "",
    "## Tables",
    "",
]

table_names = sorted(inspector.get_table_names())

for table_name in table_names:
    columns = inspector.get_columns(table_name)
    pk = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
    foreign_keys = inspector.get_foreign_keys(table_name)

    lines.extend([
        f"### {table_name}",
        "",
        TABLE_DESCRIPTIONS.get(table_name, "Database table."),
        "",
        "| Column | Data type | Nullable | Key | Default |",
        "|---|---|---|---|---|",
    ])

    fk_columns = {}
    for fk in foreign_keys:
        for column, referred_column in zip(
            fk["constrained_columns"], fk["referred_columns"]
        ):
            fk_columns[column] = (
                f"FK → {fk['referred_table']}.{referred_column}"
            )

    for column in columns:
        name = column["name"]
        data_type = str(column["type"])
        nullable = "Yes" if column["nullable"] else "No"
        key = []

        if name in pk:
            key.append("PK")
        if name in fk_columns:
            key.append(fk_columns[name])

        default = column.get("default")
        default = str(default) if default is not None else "—"
        key_text = ", ".join(key) if key else "—"

        lines.append(
            f"| `{name}` | {data_type} | {nullable} | "
            f"{key_text} | `{default}` |"
        )

    lines.append("")

lines.extend([
    "## Dataset Scale",
    "",
    "| Dataset | Records |",
    "|---|---:|",
    "| Applicants | 10,000 |",
    "| Loan products | 4 |",
    "| Loan applications | 6,000 |",
    "| Employment records | 10,000 |",
    "| Income sources | 10,120 |",
    "| Credit facilities | 6,000 |",
    "| Application documents | 24,000 |",
    "| Affordability checks | 6,000 |",
    "| Loan decisions | 6,000 |",
    "| Repayment schedules | 6,000 |",
    "| Repayment installments | 589,395 |",
    "| Disbursements | 6,120 |",
    "| Anomaly cases | 600 |",
    "| Ground-truth labels | 30,000 |",
    "",
    "## Ground Truth",
    "",
    "The evaluation dataset contains 600 positive anomaly labels "
    "and 29,400 negative labels across five anomaly categories.",
    "",
    "## Notes",
    "",
    "- `audit_events` is intentionally empty in the synthetic dataset.",
    "- Disbursements are simulated; no real money is transferred.",
    "- Ground-truth labels are separate from detected anomaly records.",
])

output_file.write_text("\n".join(lines), encoding="utf-8")

print(f"SUCCESS: Data dictionary created at {output_file}")
print(f"Tables documented: {len(table_names)}")

engine.dispose()
