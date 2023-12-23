from src.TaskPackage.GameContext.Battle.ExtractBattleListDataTask import ExtractBattleListDataTask
from src.TaskPackage.GameContext.Health.ExtractHealthDataTask import ExtractHealthDataTask
from src.TaskPackage.GameContext.Mana.ExtractManaDataTask import ExtractManaDataTask
from src.TaskPackage.Task import Task
from src.TaskPackage.GameContext.GameContext import GameContext
from src.TaskPackage.TaskResolver import TaskResolver


class ExtractGameContextDataTask(Task):
    def __init__(self, resolver: TaskResolver):
        super().__init__()
        self.__resolver = resolver
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext) -> GameContext:
        # 1. check battle list
        extract_battle_list_data_task = ExtractBattleListDataTask(self.__resolver)
        self.__resolver.queue(extract_battle_list_data_task)

        # 2. check health
        extract_health_data_task = ExtractHealthDataTask(self.__resolver)
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
