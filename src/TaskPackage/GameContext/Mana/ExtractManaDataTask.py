import numpy as np

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task

from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import TesseractOcr


class ExtractManaDataTask(Task):
    def __str__(self) -> str:
        return f'ExtractManaDataTask'

    def __init__(self, widget: GlobalGameWidgetContainer, tesseract: TesseractOcr):
        super().__init__()
        self.__widget = widget
        self.__tesseract = tesseract
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        try:
            Logger.debug("Executing ExtractManaDataTask")
            Logger.debug("Received context")
            Logger.debug(context, inspect_class=True)

            widget = self.__widget.mana_widget()

            mana_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

            current_mana = int(self.__tesseract.number_img_to_string(mana_roi))

            context.set_mana(current_mana)

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()

            return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
