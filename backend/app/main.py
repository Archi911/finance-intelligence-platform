from fastapi import FastAPI
from api.v1.analytics import router as analytics_router
from api.v1.review_queue import router as review_router
from api.v1.export import router as export_router
from api.v1.review_action import router as review_actions_router

from api.v1.ingest import (
    router as ingest_router
)
from api.v1.dashboard import router as dashboard_router

app = FastAPI(
    title=" AI - Invoice system",
    version="1.0"
)

app.include_router(
    review_actions_router,
    prefix="/api/v1"
)

app.include_router(
    dashboard_router,
    prefix="/api/v1"
)

app.include_router(
    export_router,
    prefix="/api/v1"
)

app.include_router(
    review_router,
    prefix="/api/v1",
    tags=["Review Queue"]
)

app.include_router(
    ingest_router,
    prefix="/api/v1",
    tags=["Ingestion"]
)

app.include_router(
    analytics_router,
    prefix="/api/v1",
    tags=["Analytics"]
)


@app.get("/")
def root():

    return {
        "message":
        "AI - Invoice system Backend Running"
    }