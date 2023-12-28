import numpy as np
import cv2
import pytesseract
import re

from pytesseract import Output


class TesseractOcr:
    TESSERACT_EXTRACT_NUMBER_CONFIG = r'--oem 3 --psm 13 outputbase digits'

    def __init__(self):
        pass

    def number_img_to_string(self, frame: np.ndarray) -> str:
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        grey_img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Apply thresholding to separate the digits from the background
        _, thresholded = cv2.threshold(grey_img, 127, 255, cv2.THRESH_BINARY_INV)

        # Display the thresholded image
        cv2.imshow('Thresholded Image', thresholded)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        result = pytesseract.image_to_data(grey_img, config=self.TESSERACT_EXTRACT_NUMBER_CONFIG, output_type=Output.DICT)

        print(result)

        # digits_only = re.findall(r'\d', result)

        #return ''.join(digits_only)
        return '111111'
