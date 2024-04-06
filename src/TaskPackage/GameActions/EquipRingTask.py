import numpy as np

from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task


class EquipRingTask(Task):
    def __str__(self) -> str:
        return f'EquipRingTask'

    def __init__(self, player: Player):
        super().__init__()

        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing EquipRingTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        # pending to inject the script and do it with the script config
        if not context.get_is_ring_equipped() and context.get_has_to_wear_ring():
            self.__player.use_stealth_ring()

        self.succeed()
        return context
