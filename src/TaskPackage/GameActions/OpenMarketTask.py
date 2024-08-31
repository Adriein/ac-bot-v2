import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.VendorPackage import PyAutoGui


class OpenMarketTask(Task):
    def __str__(self) -> str:
        return f'OpenMarketTask'

    def __init__(self, widget: GlobalGameWidgetContainer):
        super().__init__()
        self.__widget = widget
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        try:
            Logger.debug("Executing OpenMarketTask")
            Logger.debug("Received context")
            Logger.debug(context, inspect_class=True)

            nearest_depot_position

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()

            return context
