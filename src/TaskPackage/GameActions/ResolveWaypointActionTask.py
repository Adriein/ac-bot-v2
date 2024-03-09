import numpy as np

from src.SharedPackage import GameContext, Waypoint, Coordinate
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.GamePackage import Map, Player


class ResolveWaypointActionTask(Task):
    FLOOR_CHANGE_TYPE = [
        Waypoint.HOLE_UP_TYPE,
        Waypoint.HOLE_DOWN_TYPE,
        Waypoint.STAIR_UP_TYPE,
        Waypoint.STAIR_DOWN_TYPE
    ]

    def __str__(self) -> str:
        return f'ResolveWaypointActionTask'

    def __init__(self, game_map: Map, player: Player, widget: GlobalGameWidgetContainer):
        super().__init__()
        self.__game_map = game_map
        self.__player = player
        self.__widget = widget
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing ResolveWaypointActionTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        current_waypoint = context.get_current_waypoint()

        if context.has_creatures_in_range() and not current_waypoint.is_floor_change_type():
            self.success()
            return context

        if current_waypoint.x == 32418 and current_waypoint.y == 32237 and current_waypoint.z == 7:
            print(current_waypoint.type)
            print(current_waypoint.type is Waypoint.STAIR_UP_TYPE)
            raise Exception

        game_window = self.__widget.game_window()
        if current_waypoint.is_floor_change_type():
            if current_waypoint.type is Waypoint.HOLE_UP_TYPE:
                self.__player.rope(Coordinate.from_screen_region(game_window))

                self.success()
                return context

            if current_waypoint.type is Waypoint.HAND_STAIR_UP_TYPE:
                self.__player.use_hand_stair(Coordinate.from_screen_region(game_window))

                self.success()
                return context

        self.success()
        return context
