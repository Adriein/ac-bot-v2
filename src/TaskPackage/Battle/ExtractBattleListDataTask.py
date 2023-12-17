from src.TaskPackage.GameContext import GameContext
from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver


class ExtractBattleListDataTask(Task):
    def __init__(self, resolver: TaskResolver):
        self.__resolver = resolver
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext) -> GameContext:
        pass

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
