
from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def money(value):
    return Decimal(str(value or 0)).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )


def calculate_emi(
    principal: Decimal,
    annual_interest_rate: Decimal,
    tenure_months: int
) -> Decimal:
    """Calculate monthly EMI using the reducing-balance method."""

    principal = Decimal(str(principal))
    annual_interest_rate = Decimal(str(annual_interest_rate))

    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative")

    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero")

    monthly_rate = annual_interest_rate / Decimal("1200")

    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        factor = (Decimal("1") + monthly_rate) ** tenure_months
        emi = principal * monthly_rate * factor / (factor - 1)

    return money(emi)


def calculate_affordability(
    application,
    product,
    income_sources,
    credit_facilities
):
    """
    Calculate affordability using verified income and active
    credit obligations.

    These are demo assessment rules, not a regulated lending policy.
    """

    # 1. Calculate verified monthly income only.
    verified_income = sum(
        (
            Decimal(str(source.monthly_amount or 0))
            for source in income_sources
            if (source.verification_status or "").upper() == "VERIFIED"
        ),
        Decimal("0")
    )

    # 2. Calculate existing monthly obligations.
    existing_obligations = sum(
        (
            Decimal(str(facility.monthly_obligation or 0))
            for facility in credit_facilities
            if (facility.facility_status or "").upper() == "ACTIVE"
        ),
        Decimal("0")
    )

    # 3. Calculate proposed loan EMI.
    proposed_emi = calculate_emi(
        application.requested_amount,
        product.annual_interest_rate,
        application.requested_term_months
    )

    verified_income = money(verified_income)
    existing_obligations = money(existing_obligations)

    # 4. Calculate total monthly obligations.
    total_obligations = money(existing_obligations + proposed_emi)

    # 5. Calculate DTI.
    if verified_income > 0:
        dti_ratio = (
            total_obligations / verified_income
        ) * Decimal("100")
    else:
        dti_ratio = Decimal("0")

    dti_ratio = dti_ratio.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    # 6. Calculate disposable income.
    disposable_income = money(verified_income - total_obligations)

    # 7. Apply initial demonstration assessment rules.
    if verified_income <= 0:
        check_status = "INSUFFICIENT_VERIFIED_INCOME"
    elif dti_ratio > Decimal("50"):
        check_status = "HIGH_DTI"
    elif disposable_income <= 0:
        check_status = "INSUFFICIENT_DISPOSABLE_INCOME"
    else:
        check_status = "PASS"

    return {
        "monthly_income": verified_income,
        "monthly_existing_obligations": existing_obligations,
        "proposed_emi": proposed_emi,
        "debt_to_income_ratio": dti_ratio,
        "disposable_income": disposable_income,
        "check_status": check_status
    }
