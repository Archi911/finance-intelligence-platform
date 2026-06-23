import fitz
import numpy as np
import cv2
from pdf2image import convert_from_path
from paddleocr import PaddleOCR


POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"


class OCREngine:

    ocr = PaddleOCR(
        use_angle_cls=True,
        lang="en"
    )

    @staticmethod
    def extract_text(file_path: str) -> str:

        document = fitz.open(file_path)

        final_text = ""

        for page_num in range(len(document)):

            page = document[page_num]

            text = page.get_text().strip()

            # ====================================
            # DIGITAL PDF PAGE
            # ====================================

            if len(text) > 50:

                print(
                    f"Digital page {page_num + 1}"
                )

                final_text += text + "\n"

            # ====================================
            # SCANNED PDF PAGE
            # ====================================

            else:

                print(
                    f"OCR page {page_num + 1}"
                )

                images = convert_from_path(
                    file_path,
                    first_page=page_num + 1,
                    last_page=page_num + 1,
                    dpi=150,
                    poppler_path=POPPLER_PATH
                )

                image = images[0]

                image_np = np.array(image)
                # resizing the image 
                h, w = image_np.shape[:2]

                if w > 1200:
                    scale = 1200 / w

                    image_np = cv2.resize(
                        image_np,
                        None,
                        fx=scale,
                        fy=scale
                    )

                result = OCREngine.ocr.ocr(
                    image_np,
                    cls=True
                )

                page_text = ""

                if result and result[0]:

                    for line in result[0]:

                        try:

                            detected_text = (
                                line[1][0]
                            )

                            page_text += (
                                detected_text + "\n"
                            )

                        except Exception:
                            pass

                final_text += (
                    page_text + "\n"
                )

        document.close()

        return final_text.strip()