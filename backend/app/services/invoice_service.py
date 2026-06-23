from sqlmodel import Session, select
from database.connection import engine
from database.models import (
    Vendor,
    Invoice,
    InvoiceLineItem
)

from services.extractor import InvoiceExtraction


class InvoiceService:
    @staticmethod
    def save_invoice(
        invoice_data: InvoiceExtraction,
        confidence_score: float = 1.0
    ):

        with Session(engine) as session:

            # -------------------------
            # Check Vendor
            # -------------------------

            vendor = session.exec(
                select(Vendor).where(
                    Vendor.vendor_name
                    == invoice_data.vendor_name
                )
            ).first()

            # Create vendor if missing

            if not vendor:

                vendor = Vendor(
                    vendor_name=invoice_data.vendor_name,
                    vendor_gstin=invoice_data.vendor_gstin
                )

                session.add(vendor)
                session.commit()
                session.refresh(vendor)


            # -------------------------
            # Check Duplicate Invoice
            # -------------------------

            existing_invoice = session.exec(
                select(Invoice).where(
                    Invoice.invoice_number == invoice_data.invoice_number,
                    Invoice.vendor_id == vendor.id
                )
            ).first()

            if existing_invoice:
                if existing_invoice:

                    return {
                        "invoice_id": existing_invoice.id,
                        "duplicate": True
                    }

            # -------------------------
            # Create Invoice
            # -------------------------

            invoice = Invoice(
                invoice_number=invoice_data.invoice_number,
                invoice_date=invoice_data.invoice_date,
                vendor_id=vendor.id,
                subtotal=invoice_data.subtotal,
                gst_amount=invoice_data.gst_amount,
                total_amount=invoice_data.total_amount,
                confidence_score=confidence_score,
                status="APPROVED"
            )

            session.add(invoice)
            session.commit()
            session.refresh(invoice)
            # -------------------------
            # Save Line Items
            # -------------------------

            for item in invoice_data.line_items:

                line_item = InvoiceLineItem(
                    invoice_id=invoice.id,
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    amount=item.amount
                )

                session.add(line_item)

            session.commit()

            return {
                "invoice_id": invoice.id,
                "duplicate": False
            }