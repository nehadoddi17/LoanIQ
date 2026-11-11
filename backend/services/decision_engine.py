
from decimal import Decimal


REQUIRED_DOCUMENTS = {
    "ID_PROOF",
    "ADDRESS_PROOF",
    "BANK_STATEMENT",
    "INCOME_PROOF"
}


def evaluate_loan_application(
    application,
    product,
    applicant,
    documents,
    affordability_check
):
    """
    Deterministic loan decision engine.

    Returns APPROVED, REJECTED, or NEEDS_REVIEW.
    """

    # Rule 1: Product must be active.
    if not product.active:
        return {
            "decision": "REJECTED",
            "reason": "Selected loan product is inactive"
        }

    # Rule 2: Requested loan amount must be within product limits.
    amount = Decimal(str(application.requested_amount))

    if not (
        product.min_loan_amount
        <= amount
        <= product.max_loan_amount
    ):
        return {
            "decision": "REJECTED",
            "reason": "Requested loan amount is outside product limits"
        }

    # Rule 3: Requested tenure must be within product limits.
    if not (
        product.min_term_months
        <= application.requested_term_months
        <= product.max_term_months
    ):
        return {
            "decision": "REJECTED",
            "reason": "Requested loan tenure is outside product limits"
        }

    # Rule 4: Credit score must be available and verified.
    if applicant.credit_score is None:
        return {
            "decision": "NEEDS_REVIEW",
            "reason": "Applicant credit score is missing"
        }

    if not applicant.credit_score_verified:
        return {
            "decision": "NEEDS_REVIEW",
            "reason": "Applicant credit score is not verified"
        }

    # Rule 5: Credit score must meet the product minimum.
    if (
        product.min_credit_score is not None
        and applicant.credit_score < product.min_credit_score
    ):
        return {
            "decision": "REJECTED",
            "reason": "Applicant credit score is below product minimum"
        }

    # Rule 6: Required documents must be present and verified.
    document_status = {}

    for document in documents:
        doc_type = (document.document_type or "").upper()
        status = (document.verification_status or "").upper()

        document_status.setdefault(doc_type, []).append(status)

    missing_documents = [
        doc for doc in REQUIRED_DOCUMENTS
        if doc not in document_status
    ]

    if missing_documents:
        return {
            "decision": "NEEDS_REVIEW",
            "reason": (
                "Required documents missing: "
                + ", ".join(sorted(missing_documents))
            )
        }

    unverified_documents = [
        doc for doc in REQUIRED_DOCUMENTS
        if not all(
            status == "VERIFIED"
            for status in document_status[doc]
        )
    ]

    if unverified_documents:
        return {
            "decision": "NEEDS_REVIEW",
            "reason": (
                "Required documents are not fully verified: "
                + ", ".join(sorted(unverified_documents))
            )
        }

    # Rule 7: An affordability check must exist.
    if affordability_check is None:
        return {
            "decision": "NEEDS_REVIEW",
            "reason": "Affordability assessment has not been completed"
        }

    # Rule 8: Affordability must pass.
    if affordability_check.check_status != "PASS":
        return {
            "decision": "REJECTED",
            "reason": (
                "Affordability assessment failed: "
                + affordability_check.check_status
            )
        }

    # All configured demo rules passed.
    return {
        "decision": "APPROVED",
        "reason": "All configured eligibility and verification checks passed"
    }
