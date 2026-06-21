from fastapi import APIRouter
from services.sql_engine import SQLEngine

router = APIRouter()

@router.get("/export-all")
def export_all():

    result = SQLEngine.execute(
        """
        SELECT *
        FROM invoices
        """
    )

    rows = [
        list(row)
        for row in result
    ]

    return {
        "data": rows
    }

