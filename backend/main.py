

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.routes.applicants import router as applicant_router
from backend.routes.loan_products import router as product_router
from backend.routes.loan_applications import router as application_router

from backend.database import get_db
from backend.routes.employment import router as employment_router
from backend.routes.income_sources import router as income_router
from backend.routes.credit_facilities import router as credit_router
from backend.routes.application_documents import router as documents_router
from backend.routes.affordability import router as affordability_router
from backend.routes.loan_decisions import router as decision_router
from backend.routes.repayment import router as repayment_router
from backend.routes.disbursement import router as disbursement_router
from backend.routes.anomalies import router as anomaly_router
from backend.routes.anomaly_evaluation import router as evaluation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="LoanIQ API",
    description="Loan origination and anomaly detection platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(applicant_router)
app.include_router(product_router)
app.include_router(application_router)
app.include_router(employment_router)
app.include_router(income_router)
app.include_router(credit_router)
app.include_router(documents_router)
app.include_router(affordability_router)
app.include_router(decision_router)
app.include_router(repayment_router)
app.include_router(disbursement_router)
app.include_router(anomaly_router)
app.include_router(evaluation_router)


@app.get("/")
def root():
    return {"message": "Welcome to LoanIQ"}


@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT current_database()")).scalar()

        return {
            "status": "healthy",
            "database": result,
            "message": "FastAPI connected to PostgreSQL successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )