from fastapi import APIRouter
from backend.app.services.sql_engine import SQLEngine

router = APIRouter()


@router.get("/dashboard-metrics")
def dashboard_metrics():

    invoices = SQLEngine.execute("""
        SELECT COUNT(*)
        FROM invoices
    """)[0][0]

    vendors = SQLEngine.execute("""
        SELECT COUNT(*)
        FROM vendors
    """)[0][0]

    gst = SQLEngine.execute("""
        SELECT COALESCE(SUM(gst_amount),0)
        FROM invoices
    """)[0][0]

    spend = SQLEngine.execute("""
        SELECT COALESCE(SUM(total_amount),0)
        FROM invoices
    """)[0][0]

    return {
        "invoices": invoices,
        "vendors": vendors,
        "gst": round(gst, 2),
        "spend": round(spend, 2)
    }