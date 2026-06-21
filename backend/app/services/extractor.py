from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float


class InvoiceExtraction(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: date
    vendor_name: Optional[str] = None
    vendor_gstin: Optional[str] = None
    subtotal: float
    gst_amount: float
    total_amount: float
    line_items: List[LineItem]


def extract_invoice(raw_text: str):

    # -----------------------
    # OCR Safety Check
    # -----------------------

    if not raw_text.strip():

        raise ValueError(
            "OCR produced empty text"
        )

    client = Groq(
        api_key=os.getenv(
            "GROQ_API_KEY"
        )
    )

    with open(
        "services/prompts/extraction_system.txt",
        "r",
        encoding="utf-8"
    ) as f:

        system_prompt = f.read()

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": raw_text
            }
        ],

        temperature=0
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    print("\n===== LLM RESPONSE =====")
    print(content)
    print("========================\n")

    try:

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        data = json.loads(
            content
        )

    except Exception:

        raise ValueError(
            f"Failed to parse JSON.\n{content}"
        )

    invoice = InvoiceExtraction(
        **data
    )

    return invoice