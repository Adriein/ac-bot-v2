import numpy as np

from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task


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

        self.__player.spell_heal('exura ico')

        self.succeed()
        return context

    def completed(self) -> bool:
        pass

    def succeed(self) -> bool:
        pass
