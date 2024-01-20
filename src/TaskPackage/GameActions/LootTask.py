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
        center_game_window_coordinate = Coordinate.from_screen_region(self.__widget.game_window())

        first_looting_point = Coordinate(center_game_window_coordinate.x, center_game_window_coordinate.y - 44)
        second_looting_point = Coordinate(center_game_window_coordinate.x + 44, first_looting_point.y)
        third_looting_point = Coordinate(center_game_window_coordinate.x + 44, center_game_window_coordinate.y)
        fourth_looting_point = Coordinate(third_looting_point.x, third_looting_point.y + 44)
        fifth_looting_point = Coordinate(center_game_window_coordinate.x, center_game_window_coordinate.y + 44)
        six_looting_point = Coordinate(center_game_window_coordinate.x - 44, fifth_looting_point.y)
        seven_looting_point = Coordinate(center_game_window_coordinate.x - 44, center_game_window_coordinate.y)
        eight_looting_point = Coordinate(seven_looting_point.x, center_game_window_coordinate.y - 44)

        looting_points = list([
            first_looting_point,
            second_looting_point,
            third_looting_point,
            fourth_looting_point,
            fifth_looting_point,
            six_looting_point,
            seven_looting_point,
            eight_looting_point
        ])

        random.shuffle(looting_points)

        return looting_points
