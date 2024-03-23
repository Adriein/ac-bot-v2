import numpy as np
import random

from src.GamePackage import Player
from src.SharedPackage import GameContext, Coordinate, Constants
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

        immediate_loot = False

        for dead_creature in context.get_pending_loot():
            if dead_creature.is_runner() and dead_creature.has_to_loot():
                immediate_loot = True

                break

        if not immediate_loot and context.get_creatures_in_range():
            self.success()

            return context

        looting_coordinates = self.__create_looting_area()

        self.__player.loot(looting_coordinates)

        immediate_loot = False

        context.reset_pending_loot()

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context

    def __create_looting_area(self) -> list[Coordinate]:
        looting_points = self.__widget.looting_area()

        looting_points_count = len(looting_points)

        random_index = random.randint(0, looting_points_count - 1)

        loot_directions = Constants.POSSIBLE_LOOT_DIRECTIONS

        random.shuffle(loot_directions)

        [direction, _] = loot_directions

        # [0,1,2,3,4,5,6,7]
        # [1,0,7,6,5,4,3,2]

        left_part = looting_points[0:random_index]  # [0,1]
        right_part = looting_points[random_index:looting_points_count]  # [2,3,4,5,6,7]

        if direction:
            left_part.reverse()
            right_part.reverse()

            return left_part + right_part

        return right_part + left_part
