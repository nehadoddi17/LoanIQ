
import calendar
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def money(value):
    return Decimal(str(value)).quantize(
        CENT,
        rounding=ROUND_HALF_UP
    )


def add_months(original_date: date, months: int) -> date:
    """Add months while preserving the day where possible."""

    month_index = original_date.month - 1 + months
    year = original_date.year + month_index // 12
    month = month_index % 12 + 1

    day = min(
        original_date.day,
        calendar.monthrange(year, month)[1]
    )

    return date(year, month, day)


def generate_repayment_schedule(
    principal: Decimal,
    annual_interest_rate: Decimal,
    tenure_months: int,
    first_due_date: date | None = None
):
    principal = Decimal(str(principal))
    annual_interest_rate = Decimal(str(annual_interest_rate))

    if principal <= 0:
        raise ValueError("Principal must be greater than zero")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative")

    if tenure_months <= 0:
        raise ValueError("Tenure must be greater than zero")

    monthly_rate = annual_interest_rate / Decimal("1200")

    if first_due_date is None:
        first_due_date = add_months(date.today(), 1)

    # Calculate the regular EMI.
    if monthly_rate == 0:
        emi = money(principal / tenure_months)
    else:
        factor = (1 + monthly_rate) ** tenure_months
        emi = money(
            principal * monthly_rate * factor / (factor - 1)
        )

    outstanding = money(principal)
    installments = []

    total_interest = Decimal("0.00")
    total_installments = Decimal("0.00")

    for number in range(1, tenure_months + 1):

        interest = money(outstanding * monthly_rate)

        if number == tenure_months:
            # Clear the remaining principal in the final installment.
            principal_component = outstanding
        else:
            principal_component = money(emi - interest)

            if principal_component <= 0:
                raise ValueError(
                    "Calculated EMI does not reduce the principal"
                )

            if principal_component > outstanding:
                principal_component = outstanding

        installment_amount = money(
            principal_component + interest
        )

        outstanding = money(outstanding - principal_component)

        due_date = add_months(first_due_date, number - 1)

        installments.append({
            "installment_number": number,
            "due_date": due_date,
            "principal_component": principal_component,
            "interest_component": interest,
            "installment_amount": installment_amount
        })

        total_interest += interest
        total_installments += installment_amount

    total_interest = money(total_interest)
    total_installments = money(total_installments)
    total_payable = money(principal + total_interest)

    reconciled = (
        outstanding == Decimal("0.00")
        and total_installments == total_payable
        and len(installments) == tenure_months
    )

    return {
        "principal_amount": money(principal),
        "regular_emi": emi,
        "total_interest": total_interest,
        "total_payable": total_payable,
        "expected_installment_count": tenure_months,
        "calculated_installment_total": total_installments,
        "reconciliation_status": (
            "RECONCILED" if reconciled else "MISMATCH"
        ),
        "installments": installments
    }
