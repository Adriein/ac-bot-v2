from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver


class ExtractHealthDataTask(Task):
    def __init__(self, resolver: TaskResolver):
        super().__init__()
        self.__resolver = resolver
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext) -> GameContext:
        self.success()
        return context
    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
