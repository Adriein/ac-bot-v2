import numpy as np

from src.SharedPackage import GameContext, Waypoint
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
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

    def __init__(self, map: Map, widget: GlobalGameWidgetContainer):
        super().__init__()
        self.__map = map
        self.__widget = widget
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing LocationTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.get_last_known_waypoint() in self.FLOOR_CHANGE_TYPE:
            current_floor = self.__map.which_floor_i_am()

        map_position = self.__map.where_am_i(frame, context.get_last_known_waypoint(), context.get_current_floor())

        context.set_last_known_waypoint(map_position.waypoint)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context
