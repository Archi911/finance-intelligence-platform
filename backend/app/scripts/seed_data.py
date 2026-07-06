from datetime import date, timedelta
import random
import os
import sys
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from sqlmodel import Session

from backend.app.database.connection import engine
from backend.app.database.models import (
    Vendor,
    Invoice,
    InvoiceLineItem
)


vendors_data = [
    ("TCS", "29ABCDE1234F1Z5"),
    ("Infosys", "29ABCDE1234F1Z6"),
    ("Wipro", "29ABCDE1234F1Z7"),
    ("Accenture", "29ABCDE1234F1Z8"),
    ("Capgemini", "29ABCDE1234F1Z9"),
    ("IBM", "29ABCDE1234F1Z1"),
    ("HCL", "29ABCDE1234F1Z2"),
    ("Tech Mahindra", "29ABCDE1234F1Z3")
]


line_item_names = [
    "Cloud Services",
    "Software License",
    "Consulting",
    "Support Services",
    "Hardware Purchase",
    "Database Subscription",
    "Training Services",
    "Security Audit"
]


def seed_database():

    with Session(engine) as session:

        print("Creating Vendors...")

        vendors = []

        for name, gstin in vendors_data:

            vendor = Vendor(
                vendor_name=name,
                vendor_gstin=gstin
            )

            session.add(vendor)

            vendors.append(vendor)

        session.commit()

        for vendor in vendors:
            session.refresh(vendor)

        print("Creating Invoices...")

        start_date = date(2025, 1, 1)

        for i in range(1, 51):

            vendor = random.choice(vendors)

            invoice_date = (
                start_date +
                timedelta(days=random.randint(0, 500))
            )

            subtotal = random.randint(
                10000,
                200000
            )

            gst_amount = round(
                subtotal * 0.18,
                2
            )

            total_amount = round(
                subtotal + gst_amount,
                2
            )

            invoice = Invoice(
                invoice_number=f"INV-{i:04}",
                invoice_date=invoice_date,
                vendor_id=vendor.id,
                subtotal=subtotal,
                gst_amount=gst_amount,
                total_amount=total_amount,
                confidence_score=1.0,
                status="APPROVED"
            )

            session.add(invoice)

            session.commit()

            session.refresh(invoice)

            num_items = random.randint(2, 5)

            for _ in range(num_items):

                quantity = random.randint(1, 10)

                unit_price = random.randint(
                    1000,
                    50000
                )

                amount = quantity * unit_price

                line_item = InvoiceLineItem(
                    invoice_id=invoice.id,
                    description=random.choice(
                        line_item_names
                    ),
                    quantity=quantity,
                    unit_price=unit_price,
                    amount=amount
                )

                session.add(line_item)

            session.commit()

        print("Done.")
        print("Created:")
        print("8 Vendors")
        print("50 Invoices")
        print("~150-250 Line Items")


if __name__ == "__main__":
    seed_database()