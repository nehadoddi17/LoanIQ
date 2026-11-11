
-- LoanIQ: Core PostgreSQL schema

CREATE TABLE IF NOT EXISTS applicants (
    applicant_id VARCHAR(30) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    date_of_birth DATE,
    email VARCHAR(255),
    phone VARCHAR(30),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    credit_score INTEGER,
    credit_score_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employment (
    employment_id VARCHAR(30) PRIMARY KEY,
    applicant_id VARCHAR(30) NOT NULL REFERENCES applicants(applicant_id),
    employer_name VARCHAR(200),
    employment_type VARCHAR(50),
    job_title VARCHAR(100),
    employment_start_date DATE,
    annual_salary NUMERIC(14,2),
    employment_status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS income_sources (
    income_source_id VARCHAR(30) PRIMARY KEY,
    applicant_id VARCHAR(30) NOT NULL REFERENCES applicants(applicant_id),
    source_type VARCHAR(50),
    source_name VARCHAR(200),
    monthly_amount NUMERIC(14,2),
    verification_status VARCHAR(30),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loan_products (
    product_id VARCHAR(30) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    min_loan_amount NUMERIC(14,2) NOT NULL,
    max_loan_amount NUMERIC(14,2) NOT NULL,
    min_term_months INTEGER NOT NULL,
    max_term_months INTEGER NOT NULL,
    annual_interest_rate NUMERIC(7,4) NOT NULL,
    min_credit_score INTEGER,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loan_applications (
    application_id VARCHAR(30) PRIMARY KEY,
    applicant_id VARCHAR(30) NOT NULL REFERENCES applicants(applicant_id),
    product_id VARCHAR(30) NOT NULL REFERENCES loan_products(product_id),
    requested_amount NUMERIC(14,2) NOT NULL,
    requested_term_months INTEGER NOT NULL,
    application_status VARCHAR(40) DEFAULT 'SUBMITTED',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS credit_facilities (
    facility_id VARCHAR(30) PRIMARY KEY,
    applicant_id VARCHAR(30) NOT NULL REFERENCES applicants(applicant_id),
    lender_name VARCHAR(200),
    facility_type VARCHAR(50),
    outstanding_balance NUMERIC(14,2),
    monthly_obligation NUMERIC(14,2),
    facility_status VARCHAR(30),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS application_documents (
    document_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) NOT NULL REFERENCES loan_applications(application_id),
    document_type VARCHAR(80),
    file_name VARCHAR(255),
    verification_status VARCHAR(30) DEFAULT 'PENDING',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS affordability_checks (
    check_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) NOT NULL REFERENCES loan_applications(application_id),
    monthly_income NUMERIC(14,2),
    monthly_existing_obligations NUMERIC(14,2),
    proposed_emi NUMERIC(14,2),
    debt_to_income_ratio NUMERIC(8,4),
    disposable_income NUMERIC(14,2),
    check_status VARCHAR(30),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loan_decisions (
    decision_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) NOT NULL REFERENCES loan_applications(application_id),
    decision VARCHAR(30) NOT NULL,
    reason TEXT,
    decided_by VARCHAR(100),
    decision_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS repayment_schedules (
    schedule_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) NOT NULL REFERENCES loan_applications(application_id),
    principal_amount NUMERIC(14,2) NOT NULL,
    total_interest NUMERIC(14,2),
    total_payable NUMERIC(14,2),
    expected_installment_count INTEGER,
    calculated_installment_total NUMERIC(14,2),
    reconciliation_status VARCHAR(30),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS repayment_installments (
    installment_id VARCHAR(30) PRIMARY KEY,
    schedule_id VARCHAR(30) NOT NULL REFERENCES repayment_schedules(schedule_id),
    installment_number INTEGER NOT NULL,
    due_date DATE NOT NULL,
    principal_component NUMERIC(14,2),
    interest_component NUMERIC(14,2),
    installment_amount NUMERIC(14,2),
    payment_status VARCHAR(30) DEFAULT 'PENDING',
    UNIQUE(schedule_id, installment_number)
);

CREATE TABLE IF NOT EXISTS disbursements (
    disbursement_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) NOT NULL REFERENCES loan_applications(application_id),
    amount NUMERIC(14,2) NOT NULL,
    disbursement_status VARCHAR(30),
    disbursed_at TIMESTAMP,
    transaction_reference VARCHAR(100)
);

-- Keep anomaly labels separate from operational records.
CREATE TABLE IF NOT EXISTS anomaly_cases (
    anomaly_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) REFERENCES loan_applications(application_id),
    anomaly_type VARCHAR(100) NOT NULL,
    description TEXT,
    detected BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMP
);

-- Ground truth is kept separate to avoid leaking labels into detection logic.
CREATE TABLE IF NOT EXISTS ground_truth_anomalies (
    ground_truth_id VARCHAR(30) PRIMARY KEY,
    anomaly_id VARCHAR(30)
        REFERENCES anomaly_cases(anomaly_id),
    application_id VARCHAR(30) NOT NULL
        REFERENCES loan_applications(application_id),
    expected_anomaly BOOLEAN NOT NULL,
    expected_anomaly_type VARCHAR(100) NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id VARCHAR(30) PRIMARY KEY,
    application_id VARCHAR(30) REFERENCES loan_applications(application_id),
    event_type VARCHAR(100) NOT NULL,
    event_description TEXT,
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actor VARCHAR(100),
    metadata JSONB
);

-- Indexes for common dashboard and API queries.
CREATE INDEX IF NOT EXISTS idx_applications_applicant
    ON loan_applications(applicant_id);

CREATE INDEX IF NOT EXISTS idx_applications_status
    ON loan_applications(application_status);

CREATE INDEX IF NOT EXISTS idx_applications_product
    ON loan_applications(product_id);

CREATE INDEX IF NOT EXISTS idx_employment_applicant
    ON employment(applicant_id);

CREATE INDEX IF NOT EXISTS idx_income_applicant
    ON income_sources(applicant_id);

CREATE INDEX IF NOT EXISTS idx_documents_application
    ON application_documents(application_id);

CREATE INDEX IF NOT EXISTS idx_decisions_application
    ON loan_decisions(application_id);

CREATE INDEX IF NOT EXISTS idx_disbursements_application
    ON disbursements(application_id);

CREATE INDEX IF NOT EXISTS idx_audit_application
    ON audit_events(application_id);
