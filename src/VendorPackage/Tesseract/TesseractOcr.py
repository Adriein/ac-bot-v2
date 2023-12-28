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


        # Apply thresholding to separate the number from the background
        _, thresholded = cv2.threshold(grey_img, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area (assuming the number is the largest object)
        largest_contour = max(contours, key=cv2.contourArea)

        # Create a mask for the largest contour
        mask = np.zeros_like(thresholded)
        cv2.drawContours(mask, [largest_contour], 0, 255, thickness=cv2.FILLED)

        # Bitwise AND operation to get the region of interest (ROI)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Display the result
        cv2.imshow('Result', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        result = pytesseract.image_to_data(grey_img, config=self.TESSERACT_EXTRACT_NUMBER_CONFIG, output_type=Output.DICT)

        print(result)

        # digits_only = re.findall(r'\d', result)

        #return ''.join(digits_only)
        return '111111'
