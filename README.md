\# LoanIQ — Intelligent Lending \& Risk Intelligence Platform



\*\*An end-to-end lending operations platform with automated affordability assessment, rule-based loan decisions, repayment management, and anomaly detection.\*\*



!\[Python](https://img.shields.io/badge/Python-3.11+-blue)

!\[React](https://img.shields.io/badge/Frontend-React-61DAFB)

!\[FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)

!\[PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)

!\[Dataset](https://img.shields.io/badge/Synthetic%20Applicants-10%2C000-purple)

!\[Applications](https://img.shields.io/badge/Loan%20Applications-6%2C000-orange)



\---



\## 1. Project Overview



LoanIQ is an intelligent lending operations platform designed to streamline the loan lifecycle, from applicant onboarding to loan evaluation, approval, repayment scheduling, and risk monitoring.



Traditional lending workflows involve multiple manual activities, including applicant verification, income assessment, credit evaluation, document validation, affordability calculations, and repayment tracking.



LoanIQ brings these activities into a centralized platform and combines deterministic lending rules with automated anomaly detection to improve operational efficiency, transparency, and risk visibility.



The platform uses a synthetic dataset containing 10,000 applicants and 6,000 loan applications to demonstrate lending workflows and evaluate anomaly detection capabilities.



\## 2. Problem Statement



Financial institutions process large volumes of loan applications and associated financial records. Managing these records manually can introduce several operational challenges:



\- Inconsistent applicant and financial information.

\- Incorrect loan tenure or requested amounts.

\- Incomplete or unverified documentation.

\- Incorrect affordability assessments.

\- Loan approvals performed before mandatory checks.

\- Repayment schedule inconsistencies.

\- Duplicate disbursement records.

\- Conflicting income information.



LoanIQ addresses these challenges through automated validations, centralized data management, rule-based decisions, and risk intelligence.



\## 3. Key Features



\### Applicant Management

\- Register and manage loan applicants.

\- Maintain personal and contact information.

\- Store credit scores and verification status.

\- Retrieve applicant records through REST APIs.



\### Loan Product Management

\- Maintain multiple loan products.

\- Configure minimum and maximum loan amounts.

\- Define interest rates and eligible repayment tenures.

\- Enforce product-specific eligibility criteria.



\### Loan Application Management

\- Create and manage loan applications.

\- Associate applicants with loan products.

\- Validate requested amounts and repayment tenures.

\- Track application decision statuses.



\### Document Management

\- Manage application documents.

\- Track document verification statuses.

\- Validate mandatory documentation before approval.



\### Affordability Assessment

\- Calculate verified monthly income.

\- Consider existing financial obligations.

\- Calculate estimated monthly loan EMI.

\- Evaluate debt-to-income ratio.

\- Calculate disposable income.

\- Generate affordability assessment results.



\### Automated Loan Decision Engine

\- Validate loan product eligibility.

\- Verify credit score requirements.

\- Validate loan amount and tenure.

\- Check mandatory document verification.

\- Evaluate affordability results.

\- Generate approval or rejection decisions with decision history.



\*\*Important:\*\* Authoritative loan decisions are based on deterministic business rules. AI-generated explanations, if added in future iterations, are not intended to independently approve or reject loans.



\### Repayment Management

\- Generate repayment schedules for approved applications.

\- Calculate installment amounts.

\- Maintain repayment installment records.

\- Reconcile scheduled and payable amounts.



\### Disbursement Management

\- Maintain disbursement records.

\- Validate application eligibility before disbursement.

\- Detect duplicate disbursement records.



Disbursement functionality is simulated; the platform does not transfer actual funds.



\### Anomaly Detection \& Risk Intelligence



LoanIQ implements five anomaly detection scenarios:



| Anomaly Type | Description |

|---|---|

| INVALID\_LOAN\_TENURE | Loan tenure outside the permitted product range |

| SCHEDULE\_RECONCILIATION\_MISMATCH | Repayment schedule totals do not reconcile |

| DECISION\_BEFORE\_REQUIRED\_CHECKS | Loan approval occurs without mandatory checks passing |

| INCOME\_SOURCE\_CONFLICT | Conflicting records exist for the same income source |

| DUPLICATE\_DISBURSEMENT | Multiple disbursement records exist for the same application |



The anomaly detection engine:

\- Identifies suspicious records.

\- Generates deterministic anomaly identifiers.

\- Maintains anomaly detection history.

\- Updates previously detected cases.

\- Compares detection results against ground-truth labels.



\## 4. System Architecture



```mermaid

flowchart TD

&#x20;   A\[Administrator / Loan Operations User]

&#x20;   B\[React Frontend]

&#x20;   C\[FastAPI REST API]

&#x20;   D\[Business Logic Services]

&#x20;   E\[PostgreSQL Database]

&#x20;   F\[Anomaly Detection Engine]

&#x20;   G\[Ground Truth Evaluation]



&#x20;   A --> B

&#x20;   B --> C

&#x20;   C --> D

&#x20;   D --> E

&#x20;   D --> F

&#x20;   F --> E

&#x20;   F --> G

```



\### Architecture Components



| Component | Technology | Responsibility |

|---|---|---|

| Frontend | React + Vite | Dashboard and user interface |

| Styling | CSS + Tailwind CSS | Responsive UI |

| Charts | Recharts | Dashboard visualizations |

| API Communication | Axios | Frontend-to-backend requests |

| Backend | FastAPI | REST API and application orchestration |

| ORM | SQLAlchemy | Database operations |

| Validation | Pydantic | Request and response validation |

| Database | PostgreSQL | Persistent lending data |

| Data Generation | Python, Pandas | Synthetic dataset generation |

| Data Loading | Psycopg2 | Bulk CSV loading |

| Documentation | Markdown | Project and data documentation |



The frontend communicates with FastAPI through REST APIs. FastAPI interacts with PostgreSQL through SQLAlchemy and the configured database connection.



\## 5. Technology Stack



\*\*Frontend\*\*

\- React

\- Vite

\- JavaScript

\- Tailwind CSS

\- Axios

\- React Router

\- Lucide React

\- Recharts



\*\*Backend\*\*

\- Python

\- FastAPI

\- SQLAlchemy

\- Pydantic

\- Uvicorn



\*\*Database\*\*

\- PostgreSQL

\- SQL



\*\*Data Engineering\*\*

\- Python

\- Pandas

\- Psycopg2

\- CSV and JSONL

\- SHA-256 checksums



\## 6. Synthetic Dataset



LoanIQ includes a reproducible synthetic lending dataset.



\*\*Dataset configuration\*\*

\- Random seed: 42

\- Generator version: 2.1

\- Applicants: 10,000

\- Loan applications: 6,000

\- Loan products: 4

\- Ground-truth records: 30,000



\### Dataset Statistics



| Entity | Records |

|---|---:|

| Applicants | 10,000 |

| Employment | 10,000 |

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



\### Dataset Design



The dataset includes both normal lending records and deliberately generated anomaly scenarios.



There are 120 positive anomaly cases for each of the five anomaly categories, giving 600 positive cases.



The ground-truth dataset contains:

\- 600 positive anomaly labels.

\- 29,400 negative anomaly labels.



All records use deterministic identifiers and reproducible generation logic.



\### Data Validation



The dataset validation process checks:



\- Primary key uniqueness.

\- Foreign key integrity.

\- Record counts.

\- Business rule consistency.

\- Loan amount and tenure constraints.

\- Repayment schedule reconciliation.

\- Anomaly label consistency.

\- Anomaly identifier consistency.

\- Actual anomaly conditions.



\*\*Latest validation result: 63 checks passed, 0 failed.\*\*



\## 7. Anomaly Detection Evaluation



The anomaly detection engine was evaluated against the generated ground-truth dataset.



| Metric | Result |

|---|---:|

| Ground Truth Cases | 30,000 |

| True Positives | 600 |

| False Positives | 0 |

| False Negatives | 0 |

| True Negatives | 29,400 |

| Precision | 100% |

| Recall | 100% |

| Accuracy | 100% |



These results demonstrate that the detection engine correctly identifies the deliberately constructed synthetic anomaly scenarios.



\*\*Evaluation limitation:\*\* These metrics are based on controlled synthetic data and should not be interpreted as evidence of equivalent performance on real-world lending data.



\## 8. Database Design



The PostgreSQL database contains 15 tables:



1\. applicants

2\. employment

3\. income\_sources

4\. loan\_products

5\. loan\_applications

6\. credit\_facilities

7\. application\_documents

8\. affordability\_checks

9\. loan\_decisions

10\. repayment\_schedules

11\. repayment\_installments

12\. disbursements

13\. anomaly\_cases

14\. ground\_truth\_anomalies

15\. audit\_events



Database schema: `database/schema.sql`



Data dictionary: `docs/data\_dictionary.md`



\## 9. Project Structure



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

│   │   ├── \*.csv

│   │   └── manifest.json

│   ├── generate\_dataset.py

│   ├── validate\_dataset.py

│   ├── load\_postgres.py

│   ├── export\_json.py

│   └── create\_data\_dictionary.py

│

├── database/

│   └── schema.sql

│

├── docs/

│   └── data\_dictionary.md

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



\## 10. Installation and Setup



\### Prerequisites



\- Python 3.11 or later

\- Node.js and npm

\- PostgreSQL

\- Git



\### Step 1: Clone the Repository



```bash

git clone https://github.com/nehadoddi17/LoanIQ.git

cd LoanIQ

```



\### Step 2: Configure Python Environment



```bash

python -m venv .venv

```



Activate the environment.



Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```bash

pip install -r requirements.txt

```



\### Step 3: Configure Environment Variables



Create a `.env` file in the project root using `.env.example` as a reference.



Configure your PostgreSQL connection:



```env

DATABASE\_URL=postgresql+psycopg2://postgres:YOUR\_PASSWORD@localhost:5432/loaniq

```



Use your own database credentials. Never commit `.env` or expose database passwords.



\### Step 4: Create the Database



Create a PostgreSQL database named `loaniq`.



Execute the schema:



```powershell

psql -U postgres -d loaniq -f database/schema.sql

```



\### Step 5: Generate Synthetic Data



From the project root:



```bash

python data/generate\_dataset.py

```



\### Step 6: Validate the Dataset



```bash

python data/validate\_dataset.py

```



\### Step 7: Load Data into PostgreSQL



Use a fresh, empty database with the schema already created.



```bash

python data/load\_postgres.py

```



The loader populates the operational tables and ground-truth labels.



\*\*Note:\*\* The loader is designed for a fresh database. Do not run it repeatedly against an already populated database without resetting it.



\### Step 8: Start the Backend



```bash

uvicorn backend.main:app --reload

```



Backend:



`http://127.0.0.1:8000`



Interactive API documentation:



`http://127.0.0.1:8000/docs`



\### Step 9: Start the Frontend



Open another terminal:



```bash

cd frontend

npm install

npm run dev

```



Frontend:



`http://localhost:5173`



Configure the frontend API URL in `frontend/.env.local`:



```env

VITE\_API\_BASE\_URL=http://127.0.0.1:8000

```



Ensure the FastAPI CORS configuration allows your frontend origin.



\## 11. API Endpoints



The platform exposes REST APIs for its major lending workflows.



| Module | Endpoint | Method |

|---|---|---|

| Health | `/api/health` | GET |

| Applicants | `/api/applicants/` | GET, POST |

| Applicant Details | `/api/applicants/{applicant\_id}` | GET |

| Applications | `/api/applications/` | GET |

| Anomaly Scan | `/api/anomalies/scan` | POST |

| Anomaly Records | `/api/anomalies/` | GET |

| Application Anomalies | `/api/anomalies/{application\_id}` | GET |

| Evaluation Metrics | `/api/anomaly-evaluation/metrics` | GET |



Additional endpoints support loan products, employment, income sources, credit facilities, documents, affordability, decisions, repayment schedules, and disbursements.



For complete request and response schemas, visit:



`http://127.0.0.1:8000/docs`



\## 12. Reproducibility and Data Exports



The project supports reproducible synthetic data generation and data validation.



Available outputs include:



\- CSV datasets.

\- JSONL exports.

\- PostgreSQL schema.

\- Dataset manifest.

\- SHA-256 file checksums.

\- Data dictionary.



JSONL exports can be generated using:



```bash

python data/export\_json.py

```



The manifest can be refreshed using:



```bash

python -c "from data.generate\_dataset import refresh\_manifest\_from\_existing\_csvs; refresh\_manifest\_from\_existing\_csvs()"

```



Large duplicate exports are excluded from GitHub to keep the repository manageable. The generated CSV dataset is retained.



\## 13. Security and Responsible Lending



LoanIQ is a demonstration platform using synthetic data.



Key design considerations:



\- Database credentials are stored in environment variables.

\- The frontend does not directly access PostgreSQL.

\- Loan decisions use deterministic business rules.

\- Anomaly detection supports investigation and review.

\- Disbursement is simulated.

\- Synthetic evaluation metrics are not presented as real-world model performance.



The platform is not intended to replace regulatory, legal, credit-risk, or human review processes.



\## 14. Future Enhancements



Potential future improvements include:



\- AI-powered loan policy assistant.

\- Retrieval-Augmented Generation (RAG) for lending policy documentation.

\- Explainable anomaly investigation.

\- Interactive applicant and application detail pages.

\- Advanced portfolio analytics.

\- Authentication and role-based access control.

\- Audit trail visualization.

\- Cloud deployment and CI/CD.

\- Integration with external credit bureaus and document verification services.



\## 15. Demo Workflow



A typical LoanIQ demonstration can follow this sequence:



1\. Open the lending operations dashboard.

2\. Explore registered applicants.

3\. Review loan applications and product eligibility.

4\. Examine document verification.

5\. Run affordability calculations.

6\. Evaluate loan decisions.

7\. Generate repayment schedules.

8\. Review simulated disbursement records.

9\. Run the anomaly detection engine.

10\. Compare detection results with ground-truth metrics.



\## 16. Repository



\*\*GitHub:\*\* https://github.com/nehadoddi17/LoanIQ



\---



\## License



This project is developed as a hackathon and technical demonstration project. A formal open-source license can be added separately.



\---



\*\*LoanIQ — Making Lending Operations More Transparent, Automated, and Risk-Aware.\*\*

