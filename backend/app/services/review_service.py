from sqlmodel import Session
from backend.app.database.connection import engine
from backend.app.database.models import ReviewQueue


class ReviewService:
    @staticmethod
    def add_to_review_queue(
    invoice_id,
    reason,
    ocr_confidence,
    file_name=None,
    pdf_path=None,
    extracted_data=None
):

        with Session(engine) as session:
            review_item = ReviewQueue(
            invoice_id=invoice_id,
            reason=reason,
            ocr_confidence=ocr_confidence,
            status="PENDING",
            file_name=file_name,
            pdf_path=pdf_path,
            extracted_data=extracted_data
        )

            session.add(review_item)
            session.commit()
            session.refresh(review_item)
            return review_item.id