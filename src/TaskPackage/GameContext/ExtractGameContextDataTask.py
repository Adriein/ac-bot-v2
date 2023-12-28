import numpy as np

from src.SharedPackage import GameContext
from src.OperatingSystemPackage import GlobalGameWidgetContainer

from src.TaskPackage.GameContext.Battle.ExtractBattleListDataTask import ExtractBattleListDataTask
from src.TaskPackage.GameContext.Health.ExtractHealthDataTask import ExtractHealthDataTask
from src.TaskPackage.GameContext.Mana.ExtractManaDataTask import ExtractManaDataTask
from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver
from src.VendorPackage import TesseractOcr


class ExtractGameContextDataTask(Task):
    def __str__(self) -> str:
        return f'ExtractGameContextDataTask'

    def __init__(self, resolver: TaskResolver, widget: GlobalGameWidgetContainer, tesseract: TesseractOcr):
        super().__init__()
        self.__resolver = resolver
        self.__widget = widget
        self.__tesseract = tesseract

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        # 1. check battle list
        extract_battle_list_data_task = ExtractBattleListDataTask(self.__widget)
        self.__resolver.queue(extract_battle_list_data_task)

        # 2. check health
        extract_health_data_task = ExtractHealthDataTask(self.__widget, self.__tesseract)
        self.__resolver.queue(extract_health_data_task)

        # 3. check mana
        extract_mana_data_task = ExtractManaDataTask(self.__resolver)
        self.__resolver.queue(extract_mana_data_task)

        self.success()

        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
