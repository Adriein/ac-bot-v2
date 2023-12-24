from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.TaskPackage.TaskResolver import TaskResolver


class AttackTask(Task):
    def __init__(self, resolver: TaskResolver):
        super().__init__()
        self.__resolver = resolver
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext) -> GameContext:
        pass

    def completed(self) -> bool:
        pass

    def succeed(self) -> bool:
        pass
