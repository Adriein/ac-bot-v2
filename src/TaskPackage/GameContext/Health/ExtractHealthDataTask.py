import numpy as np
import pytesseract
import cv2
from PIL import Image

from src.SharedPackage import GameContext
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import PyAutoGui

from src.TaskPackage.Task import Task


class ExtractHealthDataTask(Task):
    def __str__(self) -> str:
        return f'ExtractHealthDataTask'

    def __init__(self, widget: GlobalGameWidgetContainer):
        super().__init__()
        self.__widget = widget
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        widget = self.__widget.health_widget()

        hp_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x + 150]
        grey_hp_roi = cv2.cvtColor(hp_roi, cv2.COLOR_BGR2GRAY)
        h, w, c = hp_roi.shape
        custom_config = r'--oem 3 --psm 8 outputbase digits'
        img = cv2.cvtColor(hp_roi, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        PyAutoGui.debug_image(img)
        print(pytesseract.image_to_string(im_pil, config=custom_config))
        self.success()
        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
