import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.VendorPackage import PyAutoGui


class ExtractHealthDataTask(Task):
    def __str__(self) -> str:
        return f'ExtractHealthDataTask'

    def __init__(self, widget: GlobalGameWidgetContainer, pyautogui: PyAutoGui):
        super().__init__()
        self.__widget = widget
        self.__pyautogui = pyautogui
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            Logger.debug("Executing ExtractHealthDataTask")
            Logger.debug("Received context")
            Logger.debug(context, inspect_class=True)

            widget = self.__widget.health_widget()

            hp_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

            current_health = self.__pyautogui.number(hp_roi)
            # current_health = int(self.__tesseract.number_img_to_string(hp_roi))

            context.set_health(current_health)
            print(current_health)
            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()

            return context
