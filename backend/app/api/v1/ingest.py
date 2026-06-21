from fastapi import (
    APIRouter,
    UploadFile,
    File
)
import os
from uuid import uuid4
import tempfile

from services.ocr_engine import OCREngine
from services.extractor import extract_invoice

from services.validator import (
    InvoiceValidator,
    get_confidence
)

from services.invoice_service import (
    InvoiceService
)

from services.review_service import (
    ReviewService
)

router = APIRouter()


@router.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@router.post("/ingest")
async def ingest_invoice(
    file: UploadFile = File(...)
):

    # =====================================
    # SAVE PDF TEMPORARILY
    # =====================================


    UPLOAD_DIR = "uploads"

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    unique_name = (
        f"{uuid4()}_{file.filename}"
    )

    pdf_path = os.path.join(
        UPLOAD_DIR,
        unique_name
    )

    content = await file.read()

    with open(
        pdf_path,
        "wb"
    ) as f:

        f.write(content)

    # =====================================
    # OCR
    # =====================================

    try:

        raw_text = OCREngine.extract_text(
            pdf_path
        )

    except Exception as e:

        review_id = (
            ReviewService.add_to_review_queue(
                invoice_id=None,
                reason=reason,
                ocr_confidence=confidence_score,
                file_name=file.filename,
                pdf_path=pdf_path,
                extracted_data=invoice.model_dump()
            )
        )

        return {
            "status": "review_required",
            "review_id": review_id,
            "confidence_score": 0.30,
            "reason": "OCR Extraction Failed"
        }

    # =====================================
    # EMPTY OCR OUTPUT
    # =====================================

    if not raw_text or not raw_text.strip():

        review_id = (
            ReviewService.add_to_review_queue(
                invoice_id=None,
                reason="OCR Extraction Failed",
                ocr_confidence=0.30,
                file_name=file.filename,
                pdf_path=pdf_path
            )
        )

        return {
            "status": "review_required",
            "review_id": review_id,
            "confidence_score": 0.30,
            "reason": "OCR Extraction Failed"
        }

    # =====================================
    # AI EXTRACTION
    # =====================================

    try:

        invoice = extract_invoice(
            raw_text
        )

    except Exception as e:

        print("\n========== EXTRACTION ERROR ==========")
        print(str(e))
        print("======================================\n")

        review_id = (
            ReviewService.add_to_review_queue(
                invoice_id=None,
                reason="AI Extraction Failed",
                ocr_confidence=0.30,
                file_name=file.filename,
                pdf_path=pdf_path
            )
        )

        return {
            "status": "review_required",
            "review_id": review_id,
            "confidence_score": 0.30,
            "reason": "AI Extraction Failed"
        }

    # =====================================
    # VALIDATION
    # =====================================

    is_valid, reason = (
        InvoiceValidator.validate(
            invoice
        )
    )

    confidence_score = (
        get_confidence(reason)
    )

    print("\n========== EXTRACTED ==========")
    print(invoice.model_dump())
    print("===============================\n")

    print(
        f"VALID={is_valid} | "
        f"REASON={reason} | "
        f"CONFIDENCE={confidence_score}"
    )

    # =====================================
    # APPROVED
    # =====================================

    if is_valid:

        invoice_id = (
            InvoiceService.save_invoice(
                invoice,
                confidence_score
            )
        )

        return {

            "status": "approved",

            "invoice_id":
                invoice_id,

            "confidence_score":
                confidence_score,

            "invoice":
                invoice.model_dump()
        }

    # =====================================
    # REVIEW REQUIRED
    # =====================================

    review_id = (
        ReviewService.add_to_review_queue(
            invoice_id=None,
            reason=reason,
            ocr_confidence=confidence_score,
            file_name=file.filename,
            pdf_path=pdf_path
        )
    )

    return {

        "status":
            "review_required",

        "review_id":
            review_id,

        "confidence_score":
            confidence_score,

        "reason":
            reason
    }