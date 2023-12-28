import numpy as np
import cv2
import pytesseract
import re


class TesseractOcr:
    TESSERACT_EXTRACT_NUMBER_CONFIG = r'--oem 3 --psm 13 outputbase digits'

    def __init__(self):
        pass

    def number_img_to_string(self, frame: np.ndarray) -> str:
        grey_img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Apply thresholding to separate the digits from the background
        _, thresholded = cv2.threshold(grey_img, 127, 255, cv2.THRESH_BINARY_INV)

        result = pytesseract.image_to_string(thresholded, config=self.TESSERACT_EXTRACT_NUMBER_CONFIG)

        digits_only = re.findall(r'\d', result)

        return ''.join(digits_only)
