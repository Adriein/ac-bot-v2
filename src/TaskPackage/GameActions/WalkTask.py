import numpy as np

from src.SharedPackage import GameContext, Waypoint
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.GamePackage import Map, Player


class WalkTask(Task):
    FLOOR_CHANGE_TYPE = [
        Waypoint.HOLE_UP_TYPE,
        Waypoint.HOLE_DOWN_TYPE,
        Waypoint.STAIR_UP_TYPE,
        Waypoint.STAIR_DOWN_TYPE
    ]

    def __str__(self) -> str:
        return f'WalkTask'

    def __init__(self, map: Map, player: Player):
        super().__init__()
        self.__map = map
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing WalkTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        route = context.get_cave_route()

        real_current_position = context.get_current_waypoint()

        destination = route.peak_next()

        if destination is None:
            route.reset()

            destination = route.current

        walk_instructions = self.__map.find_shortest_path(real_current_position, destination)

        while walk_instructions.current is not None:
            command = walk_instructions.current.data

            self.__player.move(command)

        route.next()

        self.success()
        return context
