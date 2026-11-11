# LoanIQ Data Dictionary

## Overview

LoanIQ uses PostgreSQL to store applicant, loan, repayment, decision, and anomaly-detection data.

This document is generated from the database schema.

## Tables

### affordability_checks

Stores affordability calculations and assessment outcomes.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `check_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | No | FK → loan_applications.application_id | `—` |
| `monthly_income` | NUMERIC(14, 2) | Yes | — | `—` |
| `monthly_existing_obligations` | NUMERIC(14, 2) | Yes | — | `—` |
| `proposed_emi` | NUMERIC(14, 2) | Yes | — | `—` |
| `debt_to_income_ratio` | NUMERIC(8, 4) | Yes | — | `—` |
| `disposable_income` | NUMERIC(14, 2) | Yes | — | `—` |
| `check_status` | VARCHAR(30) | Yes | — | `—` |
| `checked_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### anomaly_cases

Stores detected anomaly records and their detection status.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `anomaly_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | Yes | FK → loan_applications.application_id | `—` |
| `anomaly_type` | VARCHAR(100) | No | — | `—` |
| `description` | TEXT | Yes | — | `—` |
| `detected` | BOOLEAN | Yes | — | `false` |
| `detected_at` | TIMESTAMP | Yes | — | `—` |

### applicants

Stores applicant personal details and credit profile.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `applicant_id` | VARCHAR(30) | No | PK | `—` |
| `first_name` | VARCHAR(100) | No | — | `—` |
| `last_name` | VARCHAR(100) | Yes | — | `—` |
| `date_of_birth` | DATE | Yes | — | `—` |
| `email` | VARCHAR(255) | Yes | — | `—` |
| `phone` | VARCHAR(30) | Yes | — | `—` |
| `address` | TEXT | Yes | — | `—` |
| `city` | VARCHAR(100) | Yes | — | `—` |
| `state` | VARCHAR(100) | Yes | — | `—` |
| `postal_code` | VARCHAR(20) | Yes | — | `—` |
| `credit_score` | INTEGER | Yes | — | `—` |
| `credit_score_verified` | BOOLEAN | Yes | — | `false` |
| `created_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### application_documents

Tracks documents submitted for applications and their verification.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `document_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | No | FK → loan_applications.application_id | `—` |
| `document_type` | VARCHAR(80) | Yes | — | `—` |
| `file_name` | VARCHAR(255) | Yes | — | `—` |
| `verification_status` | VARCHAR(30) | Yes | — | `'PENDING'::character varying` |
| `uploaded_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |
| `verified_at` | TIMESTAMP | Yes | — | `—` |

### audit_events

Stores audit events for tracking system activity.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `event_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | Yes | FK → loan_applications.application_id | `—` |
| `event_type` | VARCHAR(100) | No | — | `—` |
| `event_description` | TEXT | Yes | — | `—` |
| `event_timestamp` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |
| `actor` | VARCHAR(100) | Yes | — | `—` |
| `metadata` | JSONB | Yes | — | `—` |

### credit_facilities

Stores existing credit accounts and repayment obligations.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `facility_id` | VARCHAR(30) | No | PK | `—` |
| `applicant_id` | VARCHAR(30) | No | FK → applicants.applicant_id | `—` |
| `lender_name` | VARCHAR(200) | Yes | — | `—` |
| `facility_type` | VARCHAR(50) | Yes | — | `—` |
| `outstanding_balance` | NUMERIC(14, 2) | Yes | — | `—` |
| `monthly_obligation` | NUMERIC(14, 2) | Yes | — | `—` |
| `facility_status` | VARCHAR(30) | Yes | — | `—` |
| `reported_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### disbursements

Tracks simulated loan disbursement records.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `disbursement_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | No | FK → loan_applications.application_id | `—` |
| `amount` | NUMERIC(14, 2) | No | — | `—` |
| `disbursement_status` | VARCHAR(30) | Yes | — | `—` |
| `disbursed_at` | TIMESTAMP | Yes | — | `—` |
| `transaction_reference` | VARCHAR(100) | Yes | — | `—` |

### employment

Stores applicant employment and salary information.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `employment_id` | VARCHAR(30) | No | PK | `—` |
| `applicant_id` | VARCHAR(30) | No | FK → applicants.applicant_id | `—` |
| `employer_name` | VARCHAR(200) | Yes | — | `—` |
| `employment_type` | VARCHAR(50) | Yes | — | `—` |
| `job_title` | VARCHAR(100) | Yes | — | `—` |
| `employment_start_date` | DATE | Yes | — | `—` |
| `annual_salary` | NUMERIC(14, 2) | Yes | — | `—` |
| `employment_status` | VARCHAR(30) | Yes | — | `—` |
| `created_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### ground_truth_anomalies

Stores positive and negative labels used to evaluate anomaly detection.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `ground_truth_id` | VARCHAR(30) | No | PK | `—` |
| `anomaly_id` | VARCHAR(30) | Yes | FK → anomaly_cases.anomaly_id | `—` |
| `application_id` | VARCHAR(30) | No | FK → loan_applications.application_id | `—` |
| `expected_anomaly` | BOOLEAN | No | — | `—` |
| `expected_anomaly_type` | VARCHAR(100) | No | — | `—` |
| `notes` | TEXT | Yes | — | `—` |

### income_sources

Stores applicant income sources and verification status.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `income_source_id` | VARCHAR(30) | No | PK | `—` |
| `applicant_id` | VARCHAR(30) | No | FK → applicants.applicant_id | `—` |
| `source_type` | VARCHAR(50) | Yes | — | `—` |
| `source_name` | VARCHAR(200) | Yes | — | `—` |
| `monthly_amount` | NUMERIC(14, 2) | Yes | — | `—` |
| `verification_status` | VARCHAR(30) | Yes | — | `—` |
| `reported_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### loan_applications

Stores loan requests, applicant references and application status.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `application_id` | VARCHAR(30) | No | PK | `—` |
| `applicant_id` | VARCHAR(30) | No | FK → applicants.applicant_id | `—` |
| `product_id` | VARCHAR(30) | No | FK → loan_products.product_id | `—` |
| `requested_amount` | NUMERIC(14, 2) | No | — | `—` |
| `requested_term_months` | INTEGER | No | — | `—` |
| `application_status` | VARCHAR(40) | Yes | — | `'SUBMITTED'::character varying` |
| `submitted_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |
| `updated_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### loan_decisions

Stores loan evaluation decisions and decision history.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `decision_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | No | FK → loan_applications.application_id | `—` |
| `decision` | VARCHAR(30) | No | — | `—` |
| `reason` | TEXT | Yes | — | `—` |
| `decided_by` | VARCHAR(100) | Yes | — | `—` |
| `decision_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### loan_products

Defines available loan products, limits, rates and eligibility rules.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `product_id` | VARCHAR(30) | No | PK | `—` |
| `product_name` | VARCHAR(150) | No | — | `—` |
| `min_loan_amount` | NUMERIC(14, 2) | No | — | `—` |
| `max_loan_amount` | NUMERIC(14, 2) | No | — | `—` |
| `min_term_months` | INTEGER | No | — | `—` |
| `max_term_months` | INTEGER | No | — | `—` |
| `annual_interest_rate` | NUMERIC(7, 4) | No | — | `—` |
| `min_credit_score` | INTEGER | Yes | — | `—` |
| `active` | BOOLEAN | Yes | — | `true` |
| `created_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

### repayment_installments

Stores individual repayment installment details.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `installment_id` | VARCHAR(30) | No | PK | `—` |
| `schedule_id` | VARCHAR(30) | No | FK → repayment_schedules.schedule_id | `—` |
| `installment_number` | INTEGER | No | — | `—` |
| `due_date` | DATE | No | — | `—` |
| `principal_component` | NUMERIC(14, 2) | Yes | — | `—` |
| `interest_component` | NUMERIC(14, 2) | Yes | — | `—` |
| `installment_amount` | NUMERIC(14, 2) | Yes | — | `—` |
| `payment_status` | VARCHAR(30) | Yes | — | `'PENDING'::character varying` |

### repayment_schedules

Stores repayment schedule summaries for loan applications.

| Column | Data type | Nullable | Key | Default |
|---|---|---|---|---|
| `schedule_id` | VARCHAR(30) | No | PK | `—` |
| `application_id` | VARCHAR(30) | No | FK → loan_applications.application_id | `—` |
| `principal_amount` | NUMERIC(14, 2) | No | — | `—` |
| `total_interest` | NUMERIC(14, 2) | Yes | — | `—` |
| `total_payable` | NUMERIC(14, 2) | Yes | — | `—` |
| `expected_installment_count` | INTEGER | Yes | — | `—` |
| `calculated_installment_total` | NUMERIC(14, 2) | Yes | — | `—` |
| `reconciliation_status` | VARCHAR(30) | Yes | — | `—` |
| `generated_at` | TIMESTAMP | Yes | — | `CURRENT_TIMESTAMP` |

## Dataset Scale

| Dataset | Records |
|---|---:|
| Applicants | 10,000 |
| Loan products | 4 |
| Loan applications | 6,000 |
| Employment records | 10,000 |
| Income sources | 10,120 |
| Credit facilities | 6,000 |
| Application documents | 24,000 |
| Affordability checks | 6,000 |
| Loan decisions | 6,000 |
| Repayment schedules | 6,000 |
| Repayment installments | 589,395 |
| Disbursements | 6,120 |
| Anomaly cases | 600 |
| Ground-truth labels | 30,000 |

## Ground Truth

The evaluation dataset contains 600 positive anomaly labels and 29,400 negative labels across five anomaly categories.

## Notes

- `audit_events` is intentionally empty in the synthetic dataset.
- Disbursements are simulated; no real money is transferred.
- Ground-truth labels are separate from detected anomaly records.