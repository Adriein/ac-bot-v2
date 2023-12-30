import numpy as np

from src.GamePackage import Player
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task


class HealingTask(Task):
    def __str__(self) -> str:
        return f'HealingTask'

    def __init__(self, player: Player):
        super().__init__()

        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        self.__player.spell_heal('None')

        self.succeed()
        return context

    def completed(self) -> bool:
        pass

    def succeed(self) -> bool:
        pass
