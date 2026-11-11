


import csv
import random
import hashlib
import json
from pathlib import Path
from datetime import date, datetime, timedelta
import hashlib
import json

SEED = 42
random.seed(SEED)

OUTPUT_DIR = Path(__file__).parent / "generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

APPLICANT_COUNT = 10_000
APPLICATION_COUNT = 6_000
ANOMALY_CASES_PER_TYPE = 120

ANOMALY_TYPES = [
    "INVALID_LOAN_TENURE",
    "SCHEDULE_RECONCILIATION_MISMATCH",
    "DECISION_BEFORE_REQUIRED_CHECKS",
    "INCOME_SOURCE_CONFLICT",
    "DUPLICATE_DISBURSEMENT",
]

FIRST_NAMES = [
    "Rahul", "Priya", "Arjun", "Sneha", "Kiran",
    "Ananya", "Vikram", "Meera", "Rohan", "Divya"
]

LAST_NAMES = [
    "Sharma", "Reddy", "Kumar", "Patel", "Rao",
    "Verma", "Singh", "Gupta", "Das", "Nair"
]

CITIES = [
    ("Hyderabad", "Telangana", "500001"),
    ("Bengaluru", "Karnataka", "560001"),
    ("Chennai", "Tamil Nadu", "600001"),
    ("Mumbai", "Maharashtra", "400001"),
    ("Pune", "Maharashtra", "411001"),
    ("Delhi", "Delhi", "110001"),
    ("Visakhapatnam", "Andhra Pradesh", "530001"),
]

EMPLOYERS = [
    "Tech Solutions India",
    "ABC Industries",
    "Global Services",
    "Future Systems",
    "Prime Technologies",
]

PRODUCTS = [
    {
        "product_id": "PROD001",
        "product_name": "Personal Loan",
        "min_loan_amount": 50000,
        "max_loan_amount": 1000000,
        "min_term_months": 12,
        "max_term_months": 60,
        "annual_interest_rate": 12.5,
        "min_credit_score": 650,
        "active": True,
    },
    {
        "product_id": "PROD002",
        "product_name": "Home Loan",
        "min_loan_amount": 500000,
        "max_loan_amount": 10000000,
        "min_term_months": 60,
        "max_term_months": 360,
        "annual_interest_rate": 8.5,
        "min_credit_score": 700,
        "active": True,
    },
    {
        "product_id": "PROD003",
        "product_name": "Vehicle Loan",
        "min_loan_amount": 100000,
        "max_loan_amount": 2500000,
        "min_term_months": 12,
        "max_term_months": 84,
        "annual_interest_rate": 10.0,
        "min_credit_score": 650,
        "active": True,
    },
    {
        "product_id": "PROD004",
        "product_name": "Education Loan",
        "min_loan_amount": 100000,
        "max_loan_amount": 5000000,
        "min_term_months": 12,
        "max_term_months": 180,
        "annual_interest_rate": 9.0,
        "min_credit_score": 600,
        "active": True,
    },
]

BASE_TIME = datetime(2026, 1, 1, 9, 0, 0)


def make_id(prefix, number, width=6):
    return f"{prefix}{number:0{width}d}"


def anomaly_id(application_id, anomaly_type):
    raw = f"{application_id}:{anomaly_type}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"ANM-{digest}"


def timestamp(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")


def write_csv(filename, rows):
    if not rows:
        print(f"Skipping empty file: {filename}")
        return

    path = OUTPUT_DIR / filename

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {filename}: {len(rows):,} rows")


def generate_applicants():
    rows = []

    for i in range(1, APPLICANT_COUNT + 1):
        city, state, postal_code = random.choice(CITIES)
        dob = date(1970, 1, 1) + timedelta(
            days=random.randint(0, 12000)
        )

        rows.append({
            "applicant_id": make_id("APP", i),
            "first_name": random.choice(FIRST_NAMES),
            "last_name": random.choice(LAST_NAMES),
            "date_of_birth": dob.isoformat(),
            "email": f"applicant{i}@example.com",
            "phone": f"9{random.randint(100000000, 999999999)}",
            "address": f"{random.randint(1, 999)} Sample Street",
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "credit_score": random.randint(650, 850),
            "credit_score_verified": True,
        })

    return rows


def generate_employment_and_income(applicants):
    employment = []
    income = []

    for i, applicant in enumerate(applicants, start=1):
        employer = random.choice(EMPLOYERS)
        annual_salary = random.randrange(300000, 2400000, 10000)
        monthly_salary = round(annual_salary / 12, 2)

        employment.append({
            "employment_id": make_id("EMP", i),
            "applicant_id": applicant["applicant_id"],
            "employer_name": employer,
            "employment_type": "FULL_TIME",
            "job_title": "Employee",
            "annual_salary": annual_salary,
            "employment_status": "ACTIVE",
        })

        income.append({
            "income_source_id": make_id("INC", i),
            "applicant_id": applicant["applicant_id"],
            "source_type": "SALARY",
            "source_name": employer,
            "monthly_amount": monthly_salary,
            "verification_status": "VERIFIED",
        })

    return employment, income


def generate_applications(applicants):
    rows = []
    selected = random.sample(applicants, APPLICATION_COUNT)

    for i, applicant in enumerate(selected, start=1):
        product = random.choice(PRODUCTS)

        amount = random.randrange(
            product["min_loan_amount"],
            product["max_loan_amount"] + 1,
            5000
        )

        term = random.randint(
            product["min_term_months"],
            product["max_term_months"]
        )

        rows.append({
            "application_id": make_id("LOAN", i),
            "applicant_id": applicant["applicant_id"],
            "product_id": product["product_id"],
            "requested_amount": amount,
            "requested_term_months": term,
            "application_status": "APPROVED",
            "_interest_rate": product["annual_interest_rate"],
        })

    # Allocate 120 different applications to each anomaly type.
    # The five groups do not overlap.
    groups = {}

    for index, anomaly_type in enumerate(ANOMALY_TYPES):
        start = index * ANOMALY_CASES_PER_TYPE
        end = start + ANOMALY_CASES_PER_TYPE
        groups[anomaly_type] = rows[start:end]

    # 1. Invalid tenure: outside the selected product's limits.
    products_by_id = {p["product_id"]: p for p in PRODUCTS}

    for application in groups["INVALID_LOAN_TENURE"]:
        product = products_by_id[application["product_id"]]
        application["requested_term_months"] = (
            product["max_term_months"] + 1
        )

    return rows, groups


def generate_supporting_records(applications, groups, applicants, income):
    documents = []
    affordability = []
    decisions = []
    credit_facilities = []
    schedules = []
    installments = []
    disbursements = []
    anomaly_cases = []
    ground_truth = []

    conflict_applications = {
        row["application_id"]
        for row in groups["INCOME_SOURCE_CONFLICT"]
    }

    duplicate_applications = {
        row["application_id"]
        for row in groups["DUPLICATE_DISBURSEMENT"]
    }

    schedule_anomaly_applications = {
        row["application_id"]
        for row in groups["SCHEDULE_RECONCILIATION_MISMATCH"]
    }

    decision_anomaly_applications = {
        row["application_id"]
        for row in groups["DECISION_BEFORE_REQUIRED_CHECKS"]
    }

    # 2. Income conflicts: same applicant/source with a different amount.
    applicant_by_id = {
        applicant["applicant_id"]: applicant
        for applicant in applicants
    }

    income_number = len(income) + 1

    for application in groups["INCOME_SOURCE_CONFLICT"]:
        original = next(
            item for item in income
            if item["applicant_id"] == application["applicant_id"]
        )

        income.append({
            "income_source_id": make_id("INC", income_number),
            "applicant_id": original["applicant_id"],
            "source_type": original["source_type"],
            "source_name": original["source_name"],
            "monthly_amount": round(
                float(original["monthly_amount"]) + 5000, 2
            ),
            "verification_status": "PENDING",
        })
        income_number += 1

    # 3. Supporting workflow records for all applications.
    for index, application in enumerate(applications, start=1):
        app_id = application["application_id"]
        applicant_id = application["applicant_id"]
        applicant = applicant_by_id[applicant_id]

        submitted_at = BASE_TIME + timedelta(days=index % 365)
        is_premature = app_id in decision_anomaly_applications

        # Documents: normal cases have all four verified before approval.
        required_docs = [
            "ID_PROOF",
            "ADDRESS_PROOF",
            "BANK_STATEMENT",
            "INCOME_PROOF",
        ]

        for doc_index, doc_type in enumerate(required_docs, start=1):
            if is_premature:
                verification_status = "PENDING"
                verified_at = ""
            else:
                verification_status = "VERIFIED"
                verified_at = timestamp(
                    submitted_at + timedelta(hours=doc_index)
                )

            documents.append({
                "document_id": f"DOC-{index:06d}-{doc_index}",
                "application_id": app_id,
                "document_type": doc_type,
                "file_name": f"{app_id}_{doc_type.lower()}.pdf",
                "verification_status": verification_status,
                "uploaded_at": timestamp(submitted_at),
                "verified_at": verified_at,
            })

        # Affordability: normal cases pass before the decision.
        monthly_income = round(
            float(next(
                item["monthly_amount"] for item in income
                if item["applicant_id"] == applicant_id
                and item["verification_status"] == "VERIFIED"
            )), 2
        )

        monthly_obligations = round(monthly_income * 0.10, 2)
        proposed_emi = round(
            float(application["requested_amount"])
            / application["requested_term_months"] * 1.15,
            2
        )

        dti = round(
            (monthly_obligations + proposed_emi) / monthly_income,
            4
        ) if monthly_income else 0

        affordability_status = "FAIL" if is_premature else "PASS"

        affordability.append({
            "check_id": make_id("CHK", index),
            "application_id": app_id,
            "monthly_income": monthly_income,
            "monthly_existing_obligations": monthly_obligations,
            "proposed_emi": proposed_emi,
            "debt_to_income_ratio": dti,
            "disposable_income": round(
                monthly_income - monthly_obligations - proposed_emi, 2
            ),
            "check_status": affordability_status,
            "checked_at": timestamp(
                submitted_at + timedelta(hours=1)
            ),
        })

        decision_time = submitted_at + timedelta(hours=6)

        decisions.append({
            "decision_id": make_id("DEC", index),
            "application_id": app_id,
            "decision": "APPROVED",
            "reason": (
                "Synthetic premature approval scenario"
                if is_premature
                else "Approved by deterministic synthetic test rules"
            ),
            "decided_by": "SYNTHETIC_RULE_ENGINE",
            "decision_at": timestamp(decision_time),
        })

        # Credit facility.
        credit_facilities.append({
            "facility_id": make_id("FAC", index),
            "applicant_id": applicant_id,
            "lender_name": "Sample Bank",
            "facility_type": "PERSONAL_LOAN",
            "outstanding_balance": 50000,
            "monthly_obligation": 2500,
            "facility_status": "ACTIVE",
            "reported_at": timestamp(submitted_at),
        })

        # Repayment schedule and installments.
        principal = float(application["requested_amount"])
        term = int(application["requested_term_months"])
        rate = float(application["_interest_rate"])

        # Simple-interest synthetic schedule, rounded to cents.
        total_interest = round(principal * rate / 100 * term / 12, 2)
        total_payable = round(principal + total_interest, 2)
        regular_installment = round(total_payable / term, 2)

        schedule_id = make_id("SCH", index)
        actual_total = 0.0

        for installment_number in range(1, term + 1):
            installment_amount = regular_installment

            # Adjust final installment to eliminate rounding drift.
            if installment_number == term:
                installment_amount = round(
                    total_payable - actual_total, 2
                )

            actual_total = round(
                actual_total + installment_amount, 2
            )

            installments.append({
                "installment_id": (
                    f"INS-{index:06d}-{installment_number:03d}"
                ),
                "schedule_id": schedule_id,
                "installment_number": installment_number,
                "due_date": (
                    date(2026, 2, 1)
                    + timedelta(days=30 * (installment_number - 1))
                ).isoformat(),
                "principal_component": round(
                    principal / term, 2
                ),
                "interest_component": round(
                    total_interest / term, 2
                ),
                "installment_amount": installment_amount,
                "payment_status": "PENDING",
            })

        stored_total = total_payable
        reconciliation_status = "RECONCILED"

        if app_id in schedule_anomaly_applications:
            stored_total = round(total_payable + 100, 2)
            reconciliation_status = "MISMATCH"

        schedules.append({
            "schedule_id": schedule_id,
            "application_id": app_id,
            "principal_amount": principal,
            "total_interest": total_interest,
            "total_payable": total_payable,
            "expected_installment_count": term,
            "calculated_installment_total": stored_total,
            "reconciliation_status": reconciliation_status,
            "generated_at": timestamp(submitted_at),
        })

        # Disbursement: one normal successful record, two for duplicates.
        disbursement_count = (
            2 if app_id in duplicate_applications else 1
        )

        for disbursement_number in range(1, disbursement_count + 1):
            disbursements.append({
                "disbursement_id": (
                    f"DIS-{index:06d}-{disbursement_number}"
                ),
                "application_id": app_id,
                "amount": principal,
                "disbursement_status": "DISBURSED",
                "disbursed_at": timestamp(
                    decision_time + timedelta(hours=1)
                ),
                "transaction_reference": (
                    f"SYN-{index:06d}-{disbursement_number}"
                ),
            })

    # 4. Generate matching anomaly_cases and ground truth.
    anomaly_number = 1

    for anomaly_type in ANOMALY_TYPES:
        for application in groups[anomaly_type]:
            app_id = application["application_id"]
            aid = anomaly_id(app_id, anomaly_type)

            anomaly_cases.append({
                "anomaly_id": aid,
                "application_id": app_id,
                "anomaly_type": anomaly_type,
                "description": (
                    f"Controlled synthetic scenario for {anomaly_type}"
                ),
                "detected": False,
                "detected_at": "",
            })

            ground_truth.append({
                "ground_truth_id": make_id("GT-", anomaly_number),
                "anomaly_id": aid,
                "expected_anomaly": True,
                "expected_anomaly_type": anomaly_type,
                "notes": (
                    f"Positive ground-truth case for {anomaly_type}"
                ),
            })
            anomaly_number += 1

    # Remove the internal helper field before exporting applications.
    for application in applications:
        application.pop("_interest_rate", None)

    return {
        "income_sources": income,
        "application_documents": documents,
        "affordability_checks": affordability,
        "loan_decisions": decisions,
        "credit_facilities": credit_facilities,
        "repayment_schedules": schedules,
        "repayment_installments": installments,
        "disbursements": disbursements,
        "anomaly_cases": anomaly_cases,
        "ground_truth": ground_truth,
    }



def write_manifest(counts):
    file_checksums = {}
    file_sizes = {}

    # Generate SHA-256 checksums and file sizes for all CSV files
    for csv_file in sorted(OUTPUT_DIR.glob("*.csv")):
        sha256 = hashlib.sha256()

        with open(csv_file, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                sha256.update(chunk)

        file_checksums[csv_file.name] = sha256.hexdigest()
        file_sizes[csv_file.name] = csv_file.stat().st_size

    manifest = {
        "project": "LoanIQ",
        "generator_version": "2.1",
        "random_seed": SEED,
        "applicant_count": APPLICANT_COUNT,
        "application_count": APPLICATION_COUNT,
        "anomaly_types": ANOMALY_TYPES,
        "anomaly_cases_per_type": ANOMALY_CASES_PER_TYPE,
        "record_counts": counts,
        "file_checksums_sha256": file_checksums,
        "file_sizes_bytes": file_sizes,
        "notes": [
            "Synthetic demonstration data only",
            "Disbursements are simulated records",
            "No real customer or financial information",
            "Generated CSV ground truth contains 600 positive labelled scenarios",
            "Database evaluation ground truth contains 30000 application-anomaly combinations",
            "Database evaluation includes 600 positive and 29400 negative labels",
            "SHA-256 checksums are calculated for generated CSV files"
        ],
    }

    with open(
        OUTPUT_DIR / "manifest.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(manifest, file, indent=4)



def main():
    print("=" * 60)
    print("LOANIQ SYNTHETIC DATA GENERATOR - VERSION 2.0")
    print("=" * 60)

    applicants = generate_applicants()
    employment, income = generate_employment_and_income(applicants)
    applications, groups = generate_applications(applicants)

    records = generate_supporting_records(
        applications, groups, applicants, income
    )

    all_files = {
        "applicants.csv": applicants,
        "loan_products.csv": PRODUCTS,
        "loan_applications.csv": applications,
        "employment.csv": employment,
        "income_sources.csv": records["income_sources"],
        "credit_facilities.csv": records["credit_facilities"],
        "application_documents.csv": records["application_documents"],
        "affordability_checks.csv": records["affordability_checks"],
        "loan_decisions.csv": records["loan_decisions"],
        "repayment_schedules.csv": records["repayment_schedules"],
        "repayment_installments.csv": records["repayment_installments"],
        "disbursements.csv": records["disbursements"],
        "anomaly_cases.csv": records["anomaly_cases"],
        "ground_truth.csv": records["ground_truth"],
    }

    for filename, rows in all_files.items():
        write_csv(filename, rows)

    counts = {
        filename.replace(".csv", ""): len(rows)
        for filename, rows in all_files.items()
    }
    write_manifest(counts)

    print("\nANOMALY DISTRIBUTION")
    for anomaly_type in ANOMALY_TYPES:
        print(
            f"{anomaly_type}: "
            f"{sum(1 for row in records['ground_truth'] if row['expected_anomaly_type'] == anomaly_type)}"
        )

    print("\nTOTAL RECORDS")
    for name, count in counts.items():
        print(f"{name}: {count:,}")

    print(f"\nOutput directory: {OUTPUT_DIR.resolve()}")
    print("Generation completed.")



def refresh_manifest_from_existing_csvs():
    """
    Refresh manifest using existing CSV files.
    Does not regenerate the dataset.
    """
    counts = {}

    for csv_file in sorted(OUTPUT_DIR.glob("*.csv")):
        with open(csv_file, "r", encoding="utf-8", newline="") as file:
            row_count = sum(1 for _ in file) - 1

        counts[csv_file.stem] = max(row_count, 0)

    write_manifest(counts)

    print("\nManifest refreshed successfully.")
    print(f"CSV files processed: {len(counts)}")
    print(f"Manifest location: {OUTPUT_DIR / 'manifest.json'}")


if __name__ == "__main__":
    main()
