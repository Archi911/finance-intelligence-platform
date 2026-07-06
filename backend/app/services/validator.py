from datetime import date
from backend.app.services.extractor import InvoiceExtraction


def get_confidence(reason: str):

    confidence_map = {
    "Missing Invoice Number": 0.30,
    "Missing Vendor Name": 0.40,
    "Invalid Total Amount": 0.50,
    "Invalid GSTIN": 0.60,
    "No Line Items Found": 0.65,
    "GST / Total Mismatch": 0.75,
    "Future Invoice Date": 0.80,
    "Valid Invoice": 1.00
}

    return confidence_map.get(
        reason,
        0.70
    )


class InvoiceValidator:

    @staticmethod
    def validate(
        invoice: InvoiceExtraction
    ):

        if not invoice.invoice_number:
            return False, "Missing Invoice Number"
        
        if not invoice.invoice_date:
            return False, "Missing Invoice Date"

        if not invoice.vendor_name:
            return False, "Missing Vendor Name"

        if invoice.total_amount <= 0:
            return False, "Invalid Total Amount"

        expected_total = (
            invoice.subtotal +
            invoice.gst_amount
        )

        difference = abs(
            expected_total -
            invoice.total_amount
        )

        if difference > 1:
            return False, "GST / Total Mismatch"

        if invoice.invoice_date > date.today():
            return False, "Future Invoice Date"

        if (
            invoice.vendor_gstin
            and
            len(invoice.vendor_gstin) != 15
        ):
            return False, "Invalid GSTIN"

        if len(invoice.line_items) == 0:
            return False, "No Line Items Found"

        return True, "Valid Invoice"