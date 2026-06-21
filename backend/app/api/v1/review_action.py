
from fastapi import APIRouter
from sqlmodel import Session

from database.connection import engine
from database.models import ReviewQueue

router = APIRouter()


@router.post("/review/{review_id}/approve")
def approve_review(review_id: int):

    with Session(engine) as session:

        review = session.get(
            ReviewQueue,
            review_id
        )

        if not review:

            return {
                "error": "Review not found"
            }

        review.status = "APPROVED"

        session.add(review)
        session.commit()

        return {
            "message": "Review approved"
        }


@router.post("/review/{review_id}/reject")
def reject_review(review_id: int):

    with Session(engine) as session:

        review = session.get(
            ReviewQueue,
            review_id
        )

        if not review:

            return {
                "error": "Review not found"
            }

        review.status = "REJECTED"

        session.add(review)
        session.commit()

        return {
            "message": "Review rejected"
        }