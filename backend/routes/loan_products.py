
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database import get_db
from backend.models.loan_product import LoanProduct
from backend.schemas.loan_product import (
    LoanProductCreate,
    LoanProductResponse
)

router = APIRouter(
    prefix="/api/products",
    tags=["Loan Products"]
)


@router.post("/", response_model=LoanProductResponse, status_code=201)
def create_product(
    product_data: LoanProductCreate,
    db: Session = Depends(get_db)
):
    product = LoanProduct(**product_data.model_dump())

    try:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product ID already exists"
        )


@router.get("/", response_model=list[LoanProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(LoanProduct).order_by(
        LoanProduct.product_name
    ).all()


@router.get("/{product_id}", response_model=LoanProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(LoanProduct).filter(
        LoanProduct.product_id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
