import numpy as np

from src.GamePackage import Player
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver
from src.LoggerPackage import Logger


class AttackTask(Task):
    def __str__(self) -> str:
        return f'AttackTask'

    def __init__(self, resolver: TaskResolver, player: Player):
        super().__init__()
        self.__resolver = resolver
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing AttackTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.get_is_attacking():
            self.success()

            return context

        context.get_creatures_in_range().sort(key=lambda enemy: enemy.priority())

        target = context.get_creatures_in_range()[0]

        self.__player.precision_attack(target)

        context.set_is_attacking(True)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context

    def completed(self) -> bool:
        pass

    def succeed(self) -> bool:
        pass
