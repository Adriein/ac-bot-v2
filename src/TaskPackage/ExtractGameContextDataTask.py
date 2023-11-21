from src.TaskPackage.Battle.ExtractBattleListDataTask import ExtractBattleListDataTask
from src.TaskPackage.Task import Task
from src.TaskPackage.GameContext import GameContext
from src.TaskPackage.TaskResolver import TaskResolver


class ExtractGameContextDataTask(Task):
    def __new__(cls, resolver: TaskResolver):
        cls.__resolver = resolver
        cls.__succeed = False
        cls.__completed = False

    def execute(self, context: GameContext) -> GameContext:
        # 1. check battle list
        extract_battle_list_data_task = ExtractBattleListDataTask(self.__resolver)
        self.__resolver.queue(extract_battle_list_data_task)

        # 2. check health

        # 3. check mana
        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
