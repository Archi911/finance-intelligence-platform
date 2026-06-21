import fitz  # PyMuPDF



class OCREngine:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extract text from a digital PDF.
        """
        document = fitz.open(pdf_path)

        full_text = ""

        for page in document:
            full_text += page.get_text()
        document.close()
        return full_text.strip()
    

    @staticmethod
    def extract_text(file_path):
        return OCREngine.extract_text_from_pdf(file_path)