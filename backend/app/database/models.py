from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, date

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


# ==========================================
# VENDOR
# ==========================================

class Vendor(SQLModel, table=True):
    __tablename__ = "vendors"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    vendor_name: str

    vendor_gstin: Optional[str] = None

    vendor_email: Optional[str] = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==========================================
# INVOICE
# ==========================================

class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    invoice_number: str

    invoice_date: date

    vendor_id: int = Field(
        foreign_key="vendors.id"
    )

    subtotal: float

    gst_amount: float

    total_amount: float

    confidence_score: float

    status: str = "approved"

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


# ==========================================
# LINE ITEMS
# ==========================================

class InvoiceLineItem(SQLModel, table=True):
    __tablename__ = "invoice_line_items"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    invoice_id: int = Field(
        foreign_key="invoices.id"
    )

    description: str

    quantity: float

    unit_price: float

    amount: float


# ==========================================
# REVIEW QUEUE
# ==========================================

class ReviewQueue(SQLModel, table=True):
    __tablename__ = "review_queue"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    invoice_id: Optional[int] = None

    reason: str

    ocr_confidence: float

    reviewer_notes: Optional[str] = None

    status: str = "PENDING"

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    file_name: Optional[str] = None

    pdf_path: Optional[str] = None

    extracted_data: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB)
    )