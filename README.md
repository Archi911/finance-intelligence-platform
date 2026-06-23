# Invoice Intelligence Platform

An AI-powered invoice processing system that automates extraction, validation, storage, and analysis of invoice data from both digital and scanned PDF documents.

The project was built to reduce manual invoice entry efforts and provide a structured workflow for handling invoice approvals and financial analysis.

---

## What the project does

The system accepts invoice PDFs and automatically extracts important information such as invoice number, vendor details, dates, GST values, totals, and line items.

For digital PDFs, text is extracted directly. For scanned invoices, OCR is used before sending the content to the extraction pipeline.

Extracted invoices are validated using business rules. Valid invoices are stored in the database, while suspicious or incomplete invoices are sent to a review queue for manual verification.

---

## Features

* Upload and process invoice PDFs
* Support for both digital and scanned invoices
* OCR-based text extraction
* AI-powered structured data extraction
* Invoice validation and verification
* Duplicate invoice detection
* Review queue for manual approvals
* Financial dashboard with invoice statistics
* Natural language analytics assistant
* PostgreSQL-based invoice storage

---

## Tech Stack

### Backend

* FastAPI
* SQLModel
* SQLAlchemy
* PostgreSQL

### Frontend

* Streamlit

### OCR

* PyMuPDF
* PaddleOCR
* Poppler

### AI Extraction

* Groq API
* Llama 3.3 70B

### Data Processing

* Pandas
* NumPy
* Pydantic

---

## Workflow

1. User uploads an invoice PDF.
2. Text is extracted using PyMuPDF.
3. If the PDF is scanned, PaddleOCR is used.
4. Extracted text is sent to the LLM for structured extraction.
5. Validation checks are performed.
6. Approved invoices are stored in PostgreSQL.
7. Invalid invoices are moved to the Review Queue.
8. Stored invoices can be analyzed through the dashboard and analytics assistant.

---

## Project Structure

backend/

* api/
* database/
* services/
* uploads/
* main.py

frontend/

* views/
* services/
* app.py

samples/

* good_invoice.pdf
* bad_invoice.pdf
* scanned_invoice.pdf

---

## Sample Files

The repository contains sample invoices for testing:

* good_invoice.pdf → Expected to pass validation
* bad_invoice.pdf → Expected to be routed to review queue
* scanned_invoice.pdf → Used to test OCR pipeline

---

## Running the Project

### Backend

```bash
cd backend/app
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

### Frontend

```bash
streamlit run frontend/app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
GROQ_API_KEY=your_groq_api_key
UPLOAD_DIR=uploads
```

---

## Future Improvements

* OCR confidence tracking
* Processing time analytics
* Excel export support
* Vendor spending insights
* Automated approval workflows
* Cloud deployment

---

## Why I Built This

Manual invoice processing is repetitive and error-prone. This project explores how OCR, Large Language Models, and rule-based validation can work together to automate invoice handling while still keeping a human review process for uncertain cases.

The goal was to build a practical document intelligence system rather than just an extraction model.
