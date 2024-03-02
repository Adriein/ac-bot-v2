import numpy as np
import time

from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.GamePackage import Map, Player


class WalkTask(Task):
    def __str__(self) -> str:
        return f'WalkTask'

    def __init__(self, game_map: Map, player: Player):
        super().__init__()
        self.__game_map = game_map
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing WalkTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.has_creatures_in_range():
            self.success()
            return context

        route = context.get_cave_route()
        destination = route.current.data

        real_current_position = context.get_current_waypoint()

        walk_instructions = self.__game_map.find_shortest_path(real_current_position, destination)

        for instruction in walk_instructions:
            self.__player.move(instruction)
            time.sleep(0.4)

        if route.peak_next() is None:
            route.reset()

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)
            context.set_current_waypoint(destination)

            self.success()
            return context

        route.next()

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)
        context.set_current_waypoint(destination)

        self.success()
        return context
