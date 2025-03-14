import numpy as np

from src.SharedPackage import GameContext, Waypoint
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.GamePackage import Map
from src.OperatingSystemPackage import Monitor
from src.VendorPackage.PyAutoGui.PyAutoGui import PyAutoGui


class SecurityTrainingFloorCheckTask(Task):
    def __str__(self) -> str:
        return f'SecurityTrainingFloorCheckTask'

    def __init__(self, game_map: Map, monitor: Monitor):
        super().__init__()
        self.__game_map = game_map
        self.__monitor = monitor
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing SecurityTrainingFloorCheckTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        check_screenshot = self.__monitor.screenshot()

        PyAutoGui.debug_image(check_screenshot)

        current_floor = self.__game_map.which_floor_am_i(check_screenshot)

        if current_floor is not 9:
            raise Exception

        context.set_current_floor(current_floor)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context
