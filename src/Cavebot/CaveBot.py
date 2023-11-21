from src.TaskPackage.Battle.ExtractBattleListDataTask import ExtractBattleListDataTask
from src.TaskPackage.ExtractGameContextDataTask import ExtractGameContextDataTask
from src.TaskPackage.TaskResolver import TaskResolver


class CaveBot:

    def __new__(cls, resolver: TaskResolver):
        cls.__resolver = resolver

    def init(self) -> None:
        # 0. check game context
        extract_game_context_data_task = ExtractGameContextDataTask(self.__resolver)
        self.__resolver.queue(extract_game_context_data_task)



        self.__resolver.resolve()
