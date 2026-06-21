from services.ocr_engine import OCREngine

from services.extractor import (
    extract_invoice
)

from services.validator import (
    InvoiceValidator
)

from services.invoice_service import (
    InvoiceService
)

raw_text = OCREngine.extract_text(
    "sample_invoice.pdf"
)

invoice = extract_invoice(
    raw_text
)

is_valid = InvoiceValidator.validate(
    invoice
)

from services.review_service import (
    ReviewService
)

if is_valid:

    invoice_id = InvoiceService.save_invoice(
        invoice
    )

    print(
        f"Invoice Saved: {invoice_id}"
    )

else:

    review_id = (
        ReviewService.add_to_review_queue(
            invoice_id=None,
            reason="Financial validation failed"
        )
    )

    print(
        f"Sent To Review Queue: {review_id}"
    )