import numpy as np

from src.GamePackage import Player
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.LoggerPackage import Logger


class AttackTask(Task):
    def __str__(self) -> str:
        return f'AttackTask'

    def __init__(self, player: Player):
        super().__init__()
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing AttackTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.get_is_attacking() or context.get_pending_loot():
            self.success()

            return context

        context.get_creatures_in_range().sort(key=lambda enemy: enemy.priority())

        if not context.get_creatures_in_range():
            self.success()
            return context

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
