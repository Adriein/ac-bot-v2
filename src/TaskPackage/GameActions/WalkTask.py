import numpy as np
import time

from src.SharedPackage import GameContext, MoveCommand
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger
from src.GamePackage import Map, Player
from src.OperatingSystemPackage import Monitor


class WalkTask(Task):
    def __str__(self) -> str:
        return f'WalkTask'

    def __init__(self, game_map: Map, player: Player, monitor: Monitor):
        super().__init__()
        self.__game_map = game_map
        self.__player = player
        self.__monitor = monitor
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

        print(destination)

        if destination.is_auto_floor_up() or destination.type == destination.STAIR_DOWN_TYPE:
            print('im here as i expected')
            self.__player.move(MoveCommand(1, 'north'))

            route.next()

            time.sleep(0.4)
            self.success()
            return context

        real_current_position = context.get_current_waypoint()

        walk_instructions = self.__game_map.find_shortest_path(real_current_position, destination)

        for instruction in walk_instructions:
            self.__player.move(instruction)
            time.sleep(0.4)

        check_screenshot = self.__monitor.screenshot()

        current_floor = self.__game_map.which_floor_am_i(check_screenshot)

        new_real_current_position = self.__game_map.where_am_i(check_screenshot, destination, current_floor).waypoint

        if new_real_current_position != destination:
            if not destination.is_floor_change_type():
                self.fail()

                return context

            delta = new_real_current_position.z - destination.z

            if destination.is_auto_floor_up() and delta != -1:
                self.fail()

                return context

            if destination.is_auto_floor_down() and delta != 1:
                self.fail()

                return context

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
