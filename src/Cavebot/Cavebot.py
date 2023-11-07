from src.TaskPackage.Battle.CheckBattleList import CheckBattleList
from src.TaskPackage.TaskResolver import TaskResolver


class Cavebot:

    def __new__(cls, resolver: TaskResolver):
        cls.__resolver = resolver

    def init(self) -> None:
        check_battle_list_task = CheckBattleList(self.__resolver)

        self.__resolver.queue(check_battle_list_task)

        self.__resolver.resolve()
