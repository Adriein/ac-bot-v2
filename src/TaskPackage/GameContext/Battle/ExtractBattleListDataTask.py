import numpy as np
import pytesseract
import cv2

from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer


class ExtractBattleListDataTask(Task):
    def __init__(self, container: GlobalGameWidgetContainer):
        super().__init__()
        self.__container = container
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        widget = self.__container.battle_list_widget()

        print(widget)

        battle_list_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

        battle_list_rgb = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2RGB)

        text = pytesseract.image_to_string(battle_list_rgb)

        print(text.split)

        self.success()
        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
