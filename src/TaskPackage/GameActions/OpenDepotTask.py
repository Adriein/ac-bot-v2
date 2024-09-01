import numpy as np

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, Coordinate, ScreenRegion
from src.TaskPackage.Task import Task
from src.GamePackage import Player


class OpenDepotTask(Task):
    def __str__(self) -> str:
        return f'OpenDepotTask'

    def __init__(self, widget: GlobalGameWidgetContainer, player: Player):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        try:
            Logger.debug("Executing OpenDepotTask")
            Logger.debug("Received context")
            Logger.debug(context, inspect_class=True)

            nearest_depot_position = self.__widget.nearest_depot()

            self.__player.open(Coordinate.from_screen_region(nearest_depot_position))

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()

            return context
