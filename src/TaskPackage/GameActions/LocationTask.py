import numpy as np
import random

from src.GamePackage import Player
from src.SharedPackage import GameContext, Coordinate
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer


class LocationTask(Task):
    def __str__(self) -> str:
        return f'LocationTask'

    def __init__(self, player: Player, widget: GlobalGameWidgetContainer):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing LocationTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context
