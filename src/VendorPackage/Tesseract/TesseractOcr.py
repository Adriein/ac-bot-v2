import numpy as np
import cv2
import pytesseract
import re


class TesseractOcr:
    TESSERACT_EXTRACT_NUMBER_CONFIG = r'--oem 3 --psm 7 outputbase digits'

    def __init__(self):
        pass

    def number_img_to_string(self, frame: np.ndarray) -> str:
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = pytesseract.image_to_string(rgb_img, config=self.TESSERACT_EXTRACT_NUMBER_CONFIG)

        print(result)

        digits_only = re.findall(r'\d', result)

        return ''.join(digits_only)
