import cv2
import numpy as np
import pyautogui

from src.SharedPackage import ScreenRegion


class PyAutoGui:
    def __init__(self):
        pass

    def locate_battle_list_widget(self, frame: np.ndarray) -> ScreenRegion:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        region = pyautogui.locate(
            'Wiki/Ui/Battle/battle_list.png',
            grey_scale_frame, confidence=0.8,
            grayscale=True
        )

        return ScreenRegion(region.left, region.top, region.width, region.height)
