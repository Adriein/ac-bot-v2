import numpy as np

from src.SharedPackage import GameContext, Waypoint
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.GamePackage import Map


class LocationTask(Task):
    FLOOR_CHANGE_TYPE = [
        Waypoint.HOLE_UP_TYPE,
        Waypoint.HOLE_DOWN_TYPE,
        Waypoint.STAIR_UP_TYPE,
        Waypoint.STAIR_DOWN_TYPE
    ]

    def __str__(self) -> str:
        return f'LocationTask'

    def __init__(self, game_map: Map):
        super().__init__()
        self.__game_map = game_map
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing LocationTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.has_creatures_in_range():
            self.success()
            return context

        current_floor = self.__game_map.which_floor_am_i(frame)

        print(current_floor)

        map_position = self.__game_map.where_am_i(frame, context.get_current_waypoint(), context.get_current_floor())

        context.set_current_waypoint(map_position.waypoint)
        context.set_current_floor(current_floor)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context
