from fastapi import APIRouter
from sqlmodel import Session, select

from backend.app.database.connection import engine
from backend.app.database.models import ReviewQueue

router = APIRouter()


@router.get("/review-queue")
def get_review_queue():

    with Session(engine) as session:

        reviews = session.exec(
            select(ReviewQueue)
            .where(
                ReviewQueue.status == "PENDING"
            )
        ).all()

        return reviews