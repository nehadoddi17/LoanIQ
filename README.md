# LoanIQ
### Intelligent Lending & Risk Intelligence Platform

**Automating loan operations. Strengthening financial risk intelligence.**

LoanIQ is an end-to-end intelligent lending operations platform that streamlines the loan lifecycle, from applicant onboarding and document verification to affordability assessment, loan decisions, repayment management and anomaly detection.

It combines rule-based lending workflows, structured financial data, automated validations and risk intelligence to help financial institutions improve operational efficiency, data quality and lending transparency.

---

## 1. 🧩 Problem Statement

Financial institutions process thousands of loan applications involving applicant information, employment details, income sources, existing credit obligations, financial documents and repayment records.

Managing these interconnected processes creates several operational challenges:

- Manual verification of applicant and financial information.
- Incomplete or inconsistent application documents.
- Incorrect loan amount and tenure validation.
- Inaccurate affordability assessments.
- Loan approvals performed before mandatory verification.
- Repayment schedule reconciliation errors.
- Conflicting income information.
- Duplicate disbursement records.
- Limited visibility into suspicious lending activities.

**LoanIQ addresses these challenges by providing a centralized lending workflow with automated business validations, deterministic loan decisions and anomaly detection.**

## 2. 🏦 Real-World Business Use Cases

LoanIQ demonstrates workflows that are relevant to:

| Business Domain | Use Case |
|---|---|
| Retail Banking | Personal, home and other retail loan processing |
| Digital Lending | Automated applicant onboarding and loan evaluation |
| Credit Risk Management | Credit score and affordability validation |
| Loan Operations | Document verification and application tracking |
| Financial Auditing | Repayment reconciliation and duplicate detection |
| Risk & Compliance | Identifying suspicious or inconsistent financial records |

### Intended Users and Actors

| Actor | Responsibilities |
|---|---|
| Loan Applicant | Submits personal, employment and financial information |
| Loan Officer | Reviews applications and applicant documents |
| Credit Risk Analyst | Evaluates affordability, creditworthiness and risk indicators |
| Loan Operations Team | Manages loan processing, repayment schedules and disbursement records |
| Risk & Compliance Team | Investigates anomalies and data inconsistencies |
| System Administrator | Monitors system activity, application records and system health |

## 3. 🔄 End-to-End Loan Lifecycle

LoanIQ covers the following lending workflow:

1. **Applicant Onboarding** – Register applicants and maintain personal information.
2. **Employment & Income Verification** – Capture employment details and verified income sources.
3. **Loan Product Selection** – Associate applications with eligible loan products.
4. **Application Submission** – Record requested loan amount and repayment tenure.
5. **Document Verification** – Track mandatory identity, address, bank and income documents.
6. **Affordability Assessment** – Calculate EMI, existing obligations, debt-to-income ratio and disposable income.
7. **Loan Decisioning** – Apply deterministic business rules to evaluate loan eligibility.
8. **Repayment Scheduling** – Generate and reconcile repayment installments for approved applications.
9. **Disbursement Management** – Maintain simulated disbursement records.
10. **Risk Intelligence** – Identify anomalies and compare detection results against ground truth.

## 4. ✨ Key Features

### Applicant Management
- Maintain applicant profiles and contact information.
- Store credit scores and verification status.
- Retrieve applicant information through REST APIs.

### Loan Product & Application Management
- Configure multiple loan products.
- Define minimum and maximum loan amounts.
- Configure interest rates and eligible repayment tenures.
- Validate application amounts and repayment terms.
- Track application statuses.

### Document Verification
- Maintain application-level document records.
- Track verification statuses.
- Validate mandatory documentation before loan approval.

### Affordability Assessment
- Calculate verified monthly income.
- Consider existing financial obligations.
- Calculate reducing-balance EMI.
- Evaluate debt-to-income ratio.
- Calculate disposable income.
- Generate affordability assessment results.

### Deterministic Loan Decision Engine

The decision engine evaluates applications using predefined business rules:

- Product availability and eligibility.
- Requested loan amount and tenure.
- Credit score requirements and verification.
- Mandatory document verification.
- Affordability assessment results.

It generates approval or rejection decisions and maintains decision history.

**Responsible lending principle:** Authoritative loan decisions are determined by predefined business rules. AI-generated recommendations or explanations, where introduced, should support human review and must not independently authorize loan approval or disbursement.

### Repayment & Disbursement Management
- Generate repayment schedules.
- Calculate monthly installments.
- Reconcile installment totals.
- Maintain disbursement records.
- Identify duplicate disbursement entries.

Disbursement is simulated; no actual financial transactions are performed.

### Anomaly Detection & Risk Intelligence

LoanIQ implements five anomaly detection scenarios:

| Anomaly Type | Business Scenario |
|---|---|
| `INVALID_LOAN_TENURE` | Requested tenure exceeds the permitted loan product range |
| `SCHEDULE_RECONCILIATION_MISMATCH` | Repayment schedule totals do not reconcile |
| `DECISION_BEFORE_REQUIRED_CHECKS` | Loan approval occurs before mandatory checks pass |
| `INCOME_SOURCE_CONFLICT` | Conflicting amounts exist for the same income source |
| `DUPLICATE_DISBURSEMENT` | Multiple disbursement records exist for one application |

The detection engine supports:
- Deterministic anomaly identifiers using SHA-256.
- Detection record creation and updates.
- Active anomaly tracking.
- Ground-truth comparison.
- Precision, recall and accuracy evaluation.

## 5. 🏗️ System Architecture

```mermaid
flowchart TB
    U[Loan Officers / Risk Analysts / Administrators]

    subgraph Frontend
        R[React + Vite Dashboard]
        C[Axios REST API Client]
    end

    subgraph Backend
        F[FastAPI REST API]
        S[Business Logic Services]
        V[Pydantic Validation]
        O[SQLAlchemy ORM]
        A[Anomaly Detection Engine]
        D[Decision & Affordability Engine]
    end

    subgraph Data Layer
        P[(PostgreSQL)]
        G[Ground Truth Dataset]
    end

    U --> R
    R --> C
    C <--> F
    F --> V
    F --> S
    S --> D
    S --> A
    S --> O
    O <--> P
    A --> G
    A --> P
```

### Architecture Responsibilities

| Layer | Technology | Responsibility |
|---|---|---|
| Presentation | React + Vite | Lending operations dashboard |
| Styling | CSS + Tailwind CSS | Responsive user interface |
| Visualization | Recharts | Dashboard charts and metrics |
| API Communication | Axios | REST API integration |
| API Layer | FastAPI | Request handling and API orchestration |
| Validation | Pydantic | Request and response validation |
| Business Logic | Python | Affordability, decision and anomaly services |
| ORM | SQLAlchemy | Database interaction |
| Database | PostgreSQL | Persistent lending data |
| Data Engineering | Python, Pandas, Psycopg2 | Synthetic data generation, validation and loading |

The React frontend communicates with FastAPI through REST endpoints. FastAPI handles business logic and accesses PostgreSQL through SQLAlchemy. The frontend never connects directly to the database.

## 6.  🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, JavaScript |
| UI & Styling | CSS, Tailwind CSS, Lucide React |
| Charts | Recharts |
| API Integration | Axios |
| Backend | Python, FastAPI |
| Data Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Data Processing | Pandas |
| Bulk Data Loading | Psycopg2 |
| Data Formats | CSV, JSONL, SQL |
| Version Control | Git, GitHub |

## 7. 📊 Synthetic Dataset

LoanIQ includes a reproducible synthetic lending dataset designed to simulate realistic lending operations at scale.

### Dataset Overview

| Entity | Records |
|---|---:|
| Applicants | 10,000 |
| Employment Records | 10,000 |
| Income Sources | 10,120 |
| Loan Products | 4 |
| Loan Applications | 6,000 |
| Credit Facilities | 6,000 |
| Application Documents | 24,000 |
| Affordability Checks | 6,000 |
| Loan Decisions | 6,000 |
| Repayment Schedules | 6,000 |
| Repayment Installments | 589,395 |
| Disbursements | 6,120 |
| Anomaly Cases | 600 |
| Ground Truth Labels | 30,000 |

### Dataset Characteristics

- Generator version: 2.1
- Random seed: 42
- Deterministic record identifiers.
- Relational consistency across entities.
- Normal operational records and deliberately injected anomaly scenarios.
- Separate ground-truth labels for evaluation.
- CSV exports with manifest and SHA-256 checksums.

### Ground Truth Design

The dataset includes 600 deliberately generated positive anomaly cases:

- 120 invalid loan tenure cases.
- 120 repayment schedule mismatch cases.
- 120 premature approval cases.
- 120 income source conflict cases.
- 120 duplicate disbursement cases.

The evaluation dataset contains 30,000 labels:
- 600 positive cases.
- 29,400 negative cases.

## 8. Anomaly Detection Evaluation

The anomaly detection engine was evaluated against the synthetic ground-truth dataset.

| Evaluation Metric | Result |
|---|---:|
| Ground Truth Cases | 30,000 |
| True Positives | 600 |
| False Positives | 0 |
| False Negatives | 0 |
| True Negatives | 29,400 |
| Precision | 100% |
| Recall | 100% |
| Accuracy | 100% |

These results demonstrate correct identification of the deliberately constructed synthetic anomaly scenarios.

**Evaluation limitation:** The results are based on controlled synthetic data. They do not establish equivalent performance on real-world lending data.

## 9. 🗄️ Database Design

The PostgreSQL database consists of 15 relational tables:

| # | Table | Purpose |
|---:|---|---|
| 1 | applicants | Applicant personal and credit information |
| 2 | employment | Employment details |
| 3 | income_sources | Applicant income records |
| 4 | loan_products | Loan product configurations |
| 5 | loan_applications | Loan application information |
| 6 | credit_facilities | Existing credit obligations |
| 7 | application_documents | Application document verification |
| 8 | affordability_checks | Affordability assessment results |
| 9 | loan_decisions | Loan decision history |
| 10 | repayment_schedules | Repayment schedule information |
| 11 | repayment_installments | Individual repayment installments |
| 12 | disbursements | Disbursement records |
| 13 | anomaly_cases | Detected anomaly records |
| 14 | ground_truth_anomalies | Expected anomaly labels |
| 15 | audit_events | Audit event records |

**Database schema:** `database/schema.sql`

**Data dictionary:** `docs/data_dictionary.md`

## 10. Project Structure

```text
LoanIQ/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
│
├── data/
│   ├── generated/
│   │   ├── *.csv
│   │   └── manifest.json
│   ├── generate_dataset.py
│   ├── validate_dataset.py
│   ├── load_postgres.py
│   ├── export_json.py
│   └── create_data_dictionary.py
│
├── database/
│   └── schema.sql
│
├── docs/
│   └── data_dictionary.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 11. Installation & Execution

### Prerequisites

- Python 3.11+
- Node.js and npm
- PostgreSQL
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/nehadoddi17/LoanIQ.git
cd LoanIQ
```

### Step 2: Set Up Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

Configure your PostgreSQL connection:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/loaniq
```

Replace the placeholder with your local database credentials. Never commit the actual `.env` file.

### Step 4: Create the Database

Create a PostgreSQL database named `loaniq`.

Execute the schema:

```powershell
psql -U postgres -d loaniq -f database/schema.sql
```

### Step 5: Generate Synthetic Data

```powershell
python data/generate_dataset.py
```

### Step 6: Validate the Dataset

```powershell
python data/validate_dataset.py
```

Latest validation result: **63 passed, 0 failed.**

### Step 7: Load Data into PostgreSQL

```powershell
python data/load_postgres.py
```

**Important:** The loader is designed for a fresh database with the schema already created. Use a clean database for a new load rather than running it repeatedly against populated tables.

### Step 8: Start FastAPI Backend

```powershell
uvicorn backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### Step 9: Start React Frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

`http://localhost:5173`

Create `frontend/.env.local`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Ensure FastAPI CORS configuration permits the frontend origin.

## 12. API Reference

The backend exposes REST APIs for lending operations.

| Module | Endpoint | Method |
|---|---|---|
| Health Check | `/api/health` | GET |
| Applicants | `/api/applicants/` | GET, POST |
| Applicant Details | `/api/applicants/{applicant_id}` | GET |
| Loan Applications | `/api/applications/` | GET |
| Anomaly Scan | `/api/anomalies/scan` | POST |
| Anomaly Records | `/api/anomalies/` | GET |
| Application Anomalies | `/api/anomalies/{application_id}` | GET |
| Evaluation Metrics | `/api/anomaly-evaluation/metrics` | GET |

Additional APIs support loan products, employment, income sources, credit facilities, application documents, affordability checks, loan decisions, repayment schedules and disbursement records.

For complete endpoint documentation, request schemas and response examples, visit:

`http://127.0.0.1:8000/docs`

## 13. Data Reproducibility & Validation

The data generation pipeline supports reproducible dataset creation and validation.

Available scripts:

| Script | Purpose |
|---|---|
| `generate_dataset.py` | Generates synthetic lending data |
| `validate_dataset.py` | Validates records and business rules |
| `load_postgres.py` | Loads generated data into PostgreSQL |
| `export_json.py` | Exports datasets into JSONL |
| `create_data_dictionary.py` | Generates database documentation |

The generated manifest records file sizes and SHA-256 checksums for CSV exports.

## 14. Security & Responsible Lending

LoanIQ is a technical demonstration using synthetic data.

Key considerations:

- Database credentials are maintained in environment variables.
- The frontend does not access PostgreSQL directly.
- Loan decisions use deterministic business rules.
- Anomaly detection supports investigation rather than automatically declaring fraud.
- Disbursement records are simulated.
- Synthetic evaluation metrics are not presented as real-world performance.
- Human review remains important for consequential lending decisions.

## 15. Future Enhancements

Potential improvements include:

- AI-powered lending policy assistant.
- Retrieval-Augmented Generation (RAG) for policy documentation.
- Explainable anomaly investigation.
- Interactive applicant and loan application detail views.
- Advanced lending portfolio analytics.
- Authentication and role-based access control.
- Audit trail visualization.
- Cloud deployment and CI/CD integration.
- External credit bureau and document verification integrations.


## 🎬 Project Demo

Watch the complete LoanIQ walkthrough:

[▶ Watch LoanIQ Demo Video](https://drive.google.com/file/d/17jphuQK5bwol40dx4ggrwbWNOMvjMzgi/view?usp=sharing)

This demo covers:
- Loan application management
- Applicant and employment details
- Affordability assessment
- Automated loan decision engine
- Risk intelligence and anomaly detection
- Dashboard and analytics


## 16. Repository

**GitHub:** https://github.com/nehadoddi17/LoanIQ

---

**LoanIQ — Intelligent Lending Operations with Built-in Risk Intelligence.**
