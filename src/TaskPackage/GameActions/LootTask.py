import numpy as np
import random

from src.GamePackage import Player
from src.SharedPackage import GameContext, Coordinate
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer


class LootTask(Task):
    def __str__(self) -> str:
        return f'LootTask'

    def __init__(self, player: Player, widget: GlobalGameWidgetContainer):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing LootTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if not context.get_pending_loot():
            self.success()

            return context

        looting_coordinates = self.__create_looting_area()

        for coordinate in looting_coordinates:
            self.__player.loot(coordinate)

        context.set_pending_loot(False)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context

    def __create_looting_area(self) -> list[Coordinate]:
        looting_points = self.__widget.looting_area()

        random.shuffle(looting_points)

        return looting_points
