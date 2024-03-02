import numpy as np

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
            Logger.debug("Executing ExtractHealthDataTask")
            Logger.debug("Received context")
            Logger.debug(context, inspect_class=True)

            widget = self.__widget.health_widget()

            hp_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

            PyAutoGui.debug_image(hp_roi)
            self.__pyautogui.number(0.6, hp_roi)
            # current_health = int(self.__tesseract.number_img_to_string(hp_roi))

            context.set_health(0)

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()

            return context
