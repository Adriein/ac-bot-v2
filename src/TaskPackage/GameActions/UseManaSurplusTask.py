import time

import numpy as np

from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.SharedPackage import GameContext, Constants
from src.TaskPackage.Task import Task
from src.UtilPackage import Number, Time


class UseManaSurplusTask(Task):
    def __str__(self) -> str:
        return f'UseManaSurplusTask'

    def __init__(self, player: Player):
        super().__init__()

        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing UseManaSurplusTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        random_spell_heal_times = Number.random(Constants.MIN_SPELL_HEAL_TIMES, Constants.MAX_SPELL_HEAL_TIMES)

        minutes_from_last_meal = Time.minutes_between(Time.now(), context.get_last_meal_time())

        if minutes_from_last_meal > 1:
            self.succeed()

            return context

        minutes_to_next_meal = Time.minutes_between(context.get_next_meal_time(), context.get_last_meal_time())

        if minutes_to_next_meal >= 8 and random_spell_heal_times <= 4:
            random_spell_heal_times = random_spell_heal_times + 10

        Logger.debug(f'Healing {random_spell_heal_times} times')

        for _ in range(3):
            self.__player.spell_heal(Constants.LIGHT_HEALING)
            time.sleep(2)

        self.succeed()
        return context
