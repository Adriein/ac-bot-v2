import numpy as np

from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.SharedPackage import GameContext, Constants
from src.TaskPackage.Task import Task
from src.UtilPackage import Time, Number


class EatTask(Task):
    def __str__(self) -> str:
        return f'EatTask'

    def __init__(self, player: Player):
        super().__init__()

        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing EatTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if self.__is_time_to_eat(context):
            random_eat_times = Number.random(Constants.MIN_EAT_TIMES, Constants.MAX_EAT_TIMES)

            for _ in range(random_eat_times):
                self.__player.eat()

            context.set_last_meal_time(Time.now())

            random_minutes_to_next_meal = Number.random(
                Constants.MIN_MINUTES_WITHOUT_FOOD,
                Constants.MAX_MINUTES_WITHOUT_FOOD
            )

            scheduled_meal = Time.add_minutes(Time.now(), random_minutes_to_next_meal)

            context.set_next_meal_time(scheduled_meal)

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

        self.succeed()

        return context

    def __is_time_to_eat(self, context: GameContext) -> bool:
        return Time.now() > context.get_next_meal_time()

    def completed(self) -> bool:
        pass

    def succeed(self) -> bool:
        pass
