import numpy as np

from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.SharedPackage import PyAutoGui


class ExtractBattleListDataTask(Task):
    def __init__(self, py_auto_gui: PyAutoGui):
        super().__init__()
        self.__py_auto_gui = py_auto_gui
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        battle_list = self.__py_auto_gui.locate_battle_list_widget(frame)



        self.success()
        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
