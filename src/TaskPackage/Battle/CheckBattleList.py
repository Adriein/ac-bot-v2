from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver


class CheckBattleList(Task):
    def __new__(cls, resolver: TaskResolver):
        cls.__resolver = resolver
        cls.__succeed = False
        cls.__completed = False

    def execute(self) -> None:
        pass

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
