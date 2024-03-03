import numpy as np

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.OperatingSystemPackage import GlobalGameWidgetContainer

from src.TaskPackage.GameContext.Battle.ExtractBattleListDataTask import ExtractBattleListDataTask
from src.TaskPackage.GameContext.Battle.ExtractAttackStatusBattleListTask import ExtractAttackStatusBattleListTask
from src.TaskPackage.GameContext.Battle.ExtractCombatStanceTask import ExtractCombatStanceTask
from src.TaskPackage.GameContext.Health.ExtractHealthDataTask import ExtractHealthDataTask
from src.TaskPackage.GameContext.Mana.ExtractManaDataTask import ExtractManaDataTask
from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver
from src.VendorPackage import TesseractOcr, PyAutoGui


class ExtractGameContextDataTask(Task):
    def __str__(self) -> str:
        return f"""ExtractGameContextDataTask(extract_battle_list_data, extract_health_data, extract_mana_data)"""

    def __init__(self, resolver: TaskResolver, widget: GlobalGameWidgetContainer, tesseract: TesseractOcr, pyautogui: PyAutoGui):
        super().__init__()
        self.__resolver = resolver
        self.__widget = widget
        self.__tesseract = tesseract
        self.__pyautogui = pyautogui

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing ExtractGameContextDataTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        Logger.debug("Queueing ExtractAttackStatusBattleListTask")
        extract_attack_status_battle_list_task = ExtractAttackStatusBattleListTask(self.__widget)
        self.__resolver.queue(extract_attack_status_battle_list_task)

        Logger.debug("Queueing ExtractBattleListDataTask")
        extract_battle_list_data_task = ExtractBattleListDataTask(self.__widget)
        self.__resolver.queue(extract_battle_list_data_task)

        Logger.debug("Queueing ExtractCombatStanceTask")
        extract_combat_stance_task = ExtractCombatStanceTask(self.__widget)
        self.__resolver.queue(extract_combat_stance_task)

        Logger.debug("Queueing ExtractHealthDataTask")
        extract_health_data_task = ExtractHealthDataTask(self.__widget, self.__pyautogui)
        #self.__resolver.queue(extract_health_data_task)

        Logger.debug("Queueing ExtractManaDataTask")
        extract_mana_data_task = ExtractManaDataTask(self.__widget, self.__tesseract)
        # self.__resolver.queue(extract_mana_data_task)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()

        return context
